---
title: Host preparation - POCDAPP314 (RHEL 10.2)
type: runbook
updated: 2026-07-28
tags: [dq-coe, evaluation, deployment, rhel, infrastructure]
---

# Host preparation: POCDAPP314

Everything that must exist on the server **before** the Skills Evaluation stack is
deployed. Deployment itself is `deploy/DEPLOY-POCDAPP314.md`; stop at section 8
here and switch to that.

- **Host:** POCDAPP314, 10.21.12.62, POCLAB
- **OS:** Red Hat Enterprise Linux 10.2 (Coughlan)
- **Access:** PuTTY / SSH, sudo required. RDP also available, not needed.
- **Egress:** available, directly or via proxy

> **Read section 1 before running anything.** RHEL does not ship Docker, and the
> whole design assumes Docker plus Compose. That has to be settled first.

---

## 1. The one thing to settle first: Docker on RHEL 10

Red Hat does not package Docker. RHEL ships **Podman** as its container engine,
and `docker` on a stock RHEL box is usually the `podman-docker` shim, not Docker.
Docker Engine has to come from Docker's own repository.

**Verify a build exists for RHEL 10 before committing.** RHEL 10 is recent and I
cannot confirm from here that Docker publishes an `el10` build yet:

    curl -fsSI https://download.docker.com/linux/rhel/10/x86_64/stable/ | head -1

A `200 OK` means proceed with section 3. A `403` or `404` means there is no el10
repository yet, and you have three options:

| Option | Trade-off |
|---|---|
| **Use the el9 repo on RHEL 10** | Often works, but is unsupported by Docker and by Red Hat. Acceptable for a POC, not for anything that needs a support statement. |
| **Use Podman instead** | Red Hat supported, already installed. But Portainer's support for Podman is limited compared with Docker, and git-backed Compose stacks are the weakest part of it. This would mean revisiting DEC-10, and I would want to redesign that piece rather than improvise it. |
| **Wait for the el10 build** | Cleanest, if the POC can wait. |

**Recommendation:** try the el10 repo, fall back to el9 for the POC, and record
which you used. If neither is acceptable, come back to me before starting on
Podman - swapping the container engine changes the deployment mechanism, not just
an install command, and that deserves a proper decision rather than a workaround.

Everything from section 3 onward assumes Docker Engine.

---

## 2. Component inventory

| # | Component | Source | Why it is needed |
|---|---|---|---|
| 1 | Docker Engine + CLI + containerd | Docker's own RHEL repo | Runs the app and database containers |
| 2 | Docker Compose plugin | same repo, `docker-compose-plugin` | The stack is defined as Compose |
| 3 | Kernel modules `iptable_nat`, `iptable_filter`, `br_netfilter`, `overlay` | `modprobe` + `/etc/modules-load.d/` | **Confirmed needed on this host.** Without `iptable_nat` there is no `nat` table, and dockerd dies with `RULE_APPEND failed (No such file or directory): rule in chain PREROUTING` |
| 4 | Docker daemon log rotation | `/etc/docker/daemon.json` | Container logs do not rotate by default and will fill the disk |
| 5 | nginx | RHEL AppStream (`dnf install nginx`) | TLS termination and reverse proxy for every app |
| 6 | SELinux boolean `httpd_can_network_connect` | `setsebool` | Without it SELinux blocks nginx proxying to a loopback port: every request 502s |
| 7 | firewalld rules for 80 and 443 | `firewall-cmd` | Inbound access. Nothing else gets opened |
| 8 | Certificate directory `/etc/nginx/certs` | created by hand | Holds the internal CA certificates and keys |
| 9 | Portainer CE | `deploy/portainer/docker-compose.yml` | Deploys and manages every application stack |
| 10 | chrony (time sync) | usually already present | Clock skew breaks TLS validation and session expiry |

Not needed: Python, Postgres, or Node on the host. All three live inside
containers. Do not install them.

---

## 3. Verify the host before changing it

    cat /etc/os-release
    uname -r
    getenforce                      # expect Enforcing on RHEL
    systemctl is-active firewalld
    df -h /var                      # container images and volumes live here
    timedatectl                     # confirm NTP synchronised

Check what container tooling is already present. This matters: a pre-existing
Podman or a partial Docker install is the most likely source of confusing
failures later.

    rpm -qa | grep -Ei 'docker|podman|containerd|runc'
    which docker; docker --version 2>/dev/null
    systemctl is-active docker 2>/dev/null

**If Portainer is already running on this host, stop and reuse it.** Two Portainer
instances sharing one Docker socket will both claim the same containers and
stacks, and the result is confusing rather than broken-in-an-obvious-way.

    sudo docker ps --filter "name=portainer" 2>/dev/null

Budget roughly 5 GB in `/var` for images plus room for the database volume.

---

## 4. Install Docker Engine

### 4.1 Remove the conflicting shim

`podman-docker` installs a `/usr/bin/docker` wrapper that will shadow the real
client. Remove the shim only. Removing Podman itself is not required, and other
tooling on the box may depend on it, so check before you do.

    rpm -q podman-docker && sudo dnf -y remove podman-docker
    sudo dnf -y remove runc                 # only if present; conflicts with containerd.io

### 4.2 Add Docker's repository

**RHEL 10 uses dnf5, and `config-manager` changed syntax.** The command in most
online guides (`dnf config-manager --add-repo <url>`) is the dnf4 form and will
fail here. Use:

    sudo dnf -y install dnf-plugins-core
    sudo dnf config-manager addrepo --from-repofile=https://download.docker.com/linux/rhel/docker-ce.repo

Confirm what is actually on offer before installing:

    sudo dnf --disablerepo="*" --enablerepo="docker-ce-stable" list available docker-ce

If that returns nothing, the repo file points at an el10 path that does not exist
yet. Having decided in section 1 to fall back to el9, **pin the repo file** rather
than passing `--releasever=9` on each command - a per-command override works once,
then the next `dnf update` re-resolves against `$releasever=10` and breaks:

    sudo sed -i 's/\$releasever/9/g' /etc/yum.repos.d/docker-ce.repo
    sudo dnf makecache
    sudo dnf --disablerepo="*" --enablerepo="docker-ce-stable" list available docker-ce

Record in the change log that el9 packages were used on an el10 host. It is an
unsupported combination and the next person needs to know.

### 4.3 Install and enable

    sudo dnf -y install docker-ce docker-ce-cli containerd.io \
      docker-buildx-plugin docker-compose-plugin
    sudo systemctl enable --now docker
    sudo systemctl is-enabled docker        # must say "enabled" or nothing restarts after reboot
    sudo docker version
    sudo docker compose version             # note: "compose" as a subcommand, not docker-compose

### 4.4 Kernel modules (required - confirmed on this host)

RHEL 10 minimal and hardened images do not load the netfilter modules Docker
needs. dockerd starts, tries to build its NAT chains, and dies with:

    failed to start daemon: Error initializing network controller:
    RULE_APPEND failed (No such file or directory): rule in chain PREROUTING

`No such file or directory` there means the **`nat` table does not exist** because
`iptable_nat` is not loaded. `systemctl status docker` shows only the generic
"Failed to start Docker Application Container Engine"; the real line is in
`journalctl -u docker` or by running `sudo dockerd --debug` in the foreground,
which prints it immediately.

Load them, and restart:

    lsmod | grep -E 'iptable_nat|br_netfilter|overlay'      # likely empty
    sudo modprobe overlay
    sudo modprobe br_netfilter
    sudo modprobe iptable_nat
    sudo modprobe iptable_filter
    sudo systemctl restart docker
    systemctl is-active docker                              # expect: active

**Persist them, or the host comes back broken after a reboot** and checklist item
12 fails:

    printf 'overlay\nbr_netfilter\niptable_nat\niptable_filter\n' \
      | sudo tee /etc/modules-load.d/docker.conf >/dev/null

Container networking also needs these sysctls, which a hardened image may have
switched off:

    printf 'net.ipv4.ip_forward = 1\nnet.bridge.bridge-nf-call-iptables = 1\n' \
      | sudo tee /etc/sysctl.d/99-docker.conf >/dev/null
    sudo sysctl --system >/dev/null
    sysctl net.ipv4.ip_forward                              # expect: = 1

If a `modprobe` reports "module not found", the kernel package does not ship it:

    sudo dnf -y install kernel-modules-extra
    sudo modprobe iptable_nat && sudo systemctl restart docker

Confirm the whole path works before moving on:

    sudo docker run --rm hello-world

### 4.5 Optional: run docker without sudo

    sudo usermod -aG docker "$USER"
    # log out and back in, then:
    docker ps

**Be aware of what this grants.** The docker group is root-equivalent: a member
can start a container that mounts the host filesystem. Add only accounts that are
already trusted with root on this box. If in doubt, skip this and use `sudo`.

---

## 5. Docker daemon configuration

### 5.1 Log rotation (do this now, not later)

Container logs do not rotate by default. This is the fix, and it closes an open
item from the deployment risk list.

    sudo mkdir -p /etc/docker
    printf '{\n  "log-driver": "json-file",\n  "log-opts": { "max-size": "10m", "max-file": "3" }\n}\n' \
      | sudo tee /etc/docker/daemon.json >/dev/null
    python3 -c "import json; json.load(open('/etc/docker/daemon.json')); print('JSON OK')"
    sudo systemctl restart docker
    sudo docker info --format '{{.LoggingDriver}}'

**Do not use a heredoc for this from an indented copy-paste.** A `<<'EOF'` heredoc
needs its terminating `EOF` at column zero; pasted with leading spaces it never
terminates, and you end up with a malformed `daemon.json`. dockerd then fails to
start with `unable to configure the Docker daemon` and
`systemctl is-active docker` reports `failed`. The `printf` form above is
indentation-safe, and the `json.load` line proves the file parses before the
restart.

### 5.2 Proxy, only if this host uses one

Docker does **not** read the shell's proxy variables. Pulls will fail with
confusing DNS or timeout errors if this is missed.

    sudo mkdir -p /etc/systemd/system/docker.service.d
    printf '[Service]\nEnvironment="HTTP_PROXY=http://PROXY_HOST:PORT"\nEnvironment="HTTPS_PROXY=http://PROXY_HOST:PORT"\nEnvironment="NO_PROXY=localhost,127.0.0.1,10.21.12.62,.poclab.local"\n' \
      | sudo tee /etc/systemd/system/docker.service.d/http-proxy.conf >/dev/null
    sudo systemctl daemon-reload
    sudo systemctl restart docker

**`dnf` and `curl` need the proxy too, and they need it first.** Configuring only
the Docker daemon leaves `dnf config-manager addrepo` unable to fetch Docker's
`.repo` file, which fails in a way that looks like a missing repository rather
than a network problem:

    sudo grep -q '^proxy=' /etc/dnf/dnf.conf || \
      echo 'proxy=http://PROXY_HOST:PORT' | sudo tee -a /etc/dnf/dnf.conf

Substitute the real proxy. Keep loopback and the local domain in `NO_PROXY`, or
container-to-container and nginx-to-app traffic can be sent to the proxy.

### 5.3 Prove pulls work

    sudo docker pull hello-world && sudo docker run --rm hello-world

Then pre-pull the three images this deployment needs, so a later failure is a
deployment problem rather than a network problem:

    sudo docker pull python:3.12-slim
    sudo docker pull postgres:16-alpine
    sudo docker pull portainer/portainer-ce:2.21.4

---

## 6. SELinux and firewall

### 6.1 SELinux

RHEL runs SELinux enforcing. nginx is **not** permitted to open network
connections by default, so proxying to `127.0.0.1:8001` fails and every request
returns 502 with `Permission denied` in the nginx error log. This one boolean is
the fix and it is the single most commonly missed step on RHEL:

    getsebool httpd_can_network_connect
    sudo setsebool -P httpd_can_network_connect 1
    getsebool httpd_can_network_connect        # must now be "on"

Do not disable SELinux to work around this.

### 6.2 firewalld

Open only 80 and 443.

    sudo firewall-cmd --permanent --add-service=http
    sudo firewall-cmd --permanent --add-service=https
    sudo firewall-cmd --reload
    sudo firewall-cmd --list-all

**Do not open 8001 or 9000.** Those are loopback-bound by design; opening them
would expose the app over plain HTTP and the Portainer admin UI directly on the
lab network, defeating the point of the reverse proxy.

---

## 7. Install nginx

    sudo dnf -y install nginx
    nginx -v
    sudo systemctl enable --now nginx
    curl -sI http://127.0.0.1/ | head -1

**Check the version.** The vhosts in `deploy/nginx/` use the `http2 on;`
directive, which needs **nginx 1.25.1 or newer**. RHEL 10 AppStream is expected to
ship 1.26.x, which is fine, but confirm rather than assume. If it is older, each
vhost has a comment at that line explaining the one-line change
(`listen 443 ssl http2;` and delete `http2 on;`).

Create the certificate directory now; the actual certificates are requested in
the deployment runbook.

    sudo install -d -m 750 -o root -g root /etc/nginx/certs
    sudo install -d -m 755 /etc/nginx/snippets

RHEL's default `nginx.conf` includes `/etc/nginx/conf.d/*.conf`, which is where
the app vhosts go. Confirm, and note that RHEL ships a default welcome page
server block that can shadow a vhost:

    grep -n "include */etc/nginx/conf.d" /etc/nginx/nginx.conf
    grep -rn "server_name" /etc/nginx/nginx.conf

If `nginx.conf` contains its own `server { ... default_server ... }` block, our
`00-default.conf` catch-all will conflict with it. Comment out the stock block
rather than ours.

---

## 8. Install Portainer

Portainer is the one stack deployed from the shell, because it cannot deploy
itself. It needs the repository present on the host, so clone it first.

    sudo install -d -m 755 /opt/syniti
    cd /opt/syniti
    sudo git clone <repo-url> syniti-consultant-eval
    cd syniti-consultant-eval/deploy/portainer
    sudo docker compose up -d
    sudo docker compose ps

`git` is usually present on RHEL; if not, `sudo dnf -y install git`.

Now create the Portainer admin account **immediately**. Portainer locks initial
setup if no admin is created within a few minutes of first start, and recovery
means restarting the container. nginx is not configured for it yet, so reach it
over an SSH local forward instead of opening a port:

- In PuTTY: **Connection > SSH > Tunnels**, source port `9000`, destination
  `127.0.0.1:9000`, then **Add**, and reconnect the session.
- Browse to `http://127.0.0.1:9000` on your workstation.

Treat that admin password as equivalent to root on this host, because Portainer
holds the Docker socket. Store it in a password manager, not in a ticket.

Confirm it is not reachable from the network:

    curl -m 3 http://10.21.12.62:9000/    # MUST fail to connect

---

## 9. Pre-deployment checklist

Every line must pass before you start `DEPLOY-POCDAPP314.md`.

| # | Check | Command | Expected |
|---|---|---|---|
| 1 | Docker running and enabled | `systemctl is-active docker; systemctl is-enabled docker` | `active`, `enabled` |
| 2 | Compose plugin present | `sudo docker compose version` | a version prints |
| 3 | Log rotation configured | `sudo docker info --format '{{.LoggingDriver}}'` | `json-file` with limits in daemon.json |
| 4 | Images pulled | `sudo docker images` | python, postgres, portainer present |
| 4b | Netfilter modules persisted | `cat /etc/modules-load.d/docker.conf` | overlay, br_netfilter, iptable_nat, iptable_filter |
| 4c | Container networking works | `sudo docker run --rm hello-world` | runs and exits cleanly |
| 5 | SELinux boolean set | `getsebool httpd_can_network_connect` | `on` |
| 6 | Firewall open for web only | `sudo firewall-cmd --list-services` | `http https`, nothing else added |
| 7 | nginx running, version OK | `nginx -v; systemctl is-active nginx` | >= 1.25.1, `active` |
| 8 | Cert and snippet dirs exist | `ls -ld /etc/nginx/certs /etc/nginx/snippets` | both present |
| 9 | Portainer up, admin created | `sudo docker ps --filter name=portainer` | running, and you can log in |
| 10 | Portainer not on the network | `curl -m 3 http://10.21.12.62:9000/` | connection refused |
| 11 | Clock synchronised | `timedatectl` | `System clock synchronized: yes` |
| 12 | Reboot survival | reboot, then re-run 1 and 9 | both return by themselves |

### Row 12 in full: the reboot test

Four things configured during host prep only survive a reboot if they were made
persistent: the netfilter kernel modules, the two sysctls, the SELinux boolean,
and the services being `enabled` rather than merely started. A reboot is the only
honest way to confirm all four, and it is far cheaper to discover a problem now
than during a demo.

Tell anyone else using the host first, then:

    sudo systemctl reboot

The SSH session drops. Reconnect after a minute or two and run this one block:

    echo "== services =="; systemctl is-active docker nginx; systemctl is-enabled docker nginx
    echo "== modules =="; lsmod | grep -E 'iptable_nat|iptable_filter|br_netfilter|overlay' | awk '{print $1}'
    echo "== sysctl =="; sysctl -n net.ipv4.ip_forward net.bridge.bridge-nf-call-iptables
    echo "== selinux =="; getenforce; getsebool httpd_can_network_connect
    echo "== firewall =="; sudo firewall-cmd --list-services
    echo "== portainer =="; sudo docker ps --filter name=portainer --format '{{.Status}} | {{.Ports}}'
    echo "== loopback =="; curl -sS -o /dev/null -w '%{http_code}\n' http://127.0.0.1:9000/

Expected:

| Section | Expected |
|---|---|
| services | `active` twice, then `enabled` twice |
| modules | all four names listed |
| sysctl | `1` and `1` |
| selinux | `Enforcing` or `Permissive`, then `httpd_can_network_connect --> on` |
| firewall | includes `http https` |
| portainer | `Up ...` and `127.0.0.1:9000->9000/tcp` |
| loopback | HTTP 200 or a 300-range redirect |

**`docker` returning `active` unaided is the critical result.** It proves the
kernel-module persistence held. If `/etc/modules-load.d/docker.conf` were missing
or wrong, dockerd would fail on boot with the same
`RULE_APPEND failed ... chain PREROUTING` as on first install.

Where to fix each failure: modules and sysctls in section 4.4, the SELinux boolean
in 6.1, firewall services in 6.2, and `enabled` state with
`sudo systemctl enable <unit>`.

Note that `restart: unless-stopped` on a container only helps if the Docker
service itself is enabled at boot.

---

## 10. Actions on other teams

Start these early; they gate the deployment, not this preparation.

- **DNS:** A records `skills-eval.<zone>` and `portainer.<zone>`, both to
  10.21.12.62. Also confirm the actual POCLAB DNS zone - every config file
  currently carries the placeholder `poclab.local`.
- **PKI / internal CA:** server certificates for both hostnames. The CSR commands
  are in the deployment runbook.
- **Network / firewall:** inbound TCP 80 and 443 to 10.21.12.62 from the user
  population.
- **Security:** the administrator subnet range, for the IP allow-list on the
  Portainer vhost.

---

## 11. Troubleshooting

### `systemctl is-enabled docker` returns `not-found`

`not-found` does not mean the service is stopped. It means **there is no
`docker.service` unit on the host**, so Docker Engine is not installed and
`systemctl start` cannot help. Paired with `is-active` returning `inactive`, this
is the signature of a failed or skipped section 4.

Two causes account for almost all of it on RHEL 10: the `el10` repository does not
exist yet so `dnf install docker-ce` failed, or `docker` on PATH is the
`podman-docker` shim, which provides `/usr/bin/docker` but no service.

Diagnose in one pass:

    rpm -q docker-ce docker-ce-cli containerd.io docker-compose-plugin
    systemctl list-unit-files | grep -i docker
    which docker && rpm -qf $(which docker)
    dnf repolist | grep -i docker

| What you see | Situation | Action |
|---|---|---|
| No packages, no `docker-ce-stable` repo | Repo add or install failed | Repo fallback below |
| `rpm -qf` says `podman-docker` | The Podman shim, not Docker | `sudo dnf -y remove podman-docker`, then the fallback below |
| `docker-ce` installed, unit listed | Genuinely just not started | `sudo systemctl enable --now docker` |

### Repo fallback: no el10 build

Confirm whether Docker publishes for this release at all:

    sudo dnf --disablerepo="*" --enablerepo="docker-ce-stable" list available docker-ce

If that returns nothing, use the el9 packages. **Pin the repo file rather than
passing `--releasever=9` per command**, or the next `dnf update` re-resolves
against `$releasever=10` and breaks the install:

    sudo dnf config-manager addrepo --from-repofile=https://download.docker.com/linux/rhel/docker-ce.repo
    sudo sed -i 's/\$releasever/9/g' /etc/yum.repos.d/docker-ce.repo
    sudo dnf makecache
    sudo dnf -y install docker-ce docker-ce-cli containerd.io \
      docker-buildx-plugin docker-compose-plugin
    sudo systemctl enable --now docker
    systemctl is-active docker; systemctl is-enabled docker

Both must return `active` and `enabled`. `enabled` is what brings the stack back
after a reboot, which is checklist item 12.

Record in the change log that el9 packages were used on an el10 host, and why. It
is an unsupported combination and the next person needs to know.

### Install errors

- **`containerd.io` conflicts with `runc`:** `sudo dnf -y remove runc`, then retry.
- **Unsatisfiable dependencies from the el9 packages:** this is the real signal
  that el9-on-el10 is not viable. Stop rather than forcing it with
  `--nobest` or `--skip-broken`, and revisit the container-engine decision
  (section 1). A half-satisfied Docker install is worse than Podman.

### dockerd fails with `RULE_APPEND failed ... chain PREROUTING`

The `nat` table does not exist because `iptable_nat` is not loaded. See section
4.4. This was hit on POCDAPP314 during first install, so treat 4.4 as mandatory
rather than optional on any RHEL 10 host.

`systemctl status docker` only shows the generic "Failed to start Docker
Application Container Engine". To get the real cause quickly, run the daemon in
the foreground - the fatal line prints on screen and needs no journal navigation:

    sudo dockerd --debug        # read the last line, then Ctrl+C

### Portainer: "Your Portainer instance timed out for security purposes"

Portainer disables initial setup if no admin account is created within a few
minutes of first start. Hit on POCDAPP314 during install, because reaching the UI
needed an SSH tunnel to be worked out first. It is a deliberate security
behaviour, not a fault, and the only recovery is a container restart.

Have the password generated and to hand BEFORE restarting, then do not step away
between the restart and the browser:

    openssl rand -base64 24          # Portainer requires 12+ characters
    sudo docker restart $(sudo docker ps -aq --filter name=portainer)

Refresh the UI immediately and create the account. That password is equivalent to
root on this host; store it in a password manager, not a ticket.

To remove the race on future hosts, set the password at startup instead of
interactively, using Portainer's `--admin-password-file`. Prefer that on any host
where reaching the UI is not instant.

### Reaching the Portainer UI when the host is not directly routable

POCDAPP314 is not reachable from a laptop; access is RDP to a POCLAB box and then
PuTTY from there. Two consequences that cost time on first install:

- **A tunnel lives on the machine running the SSH client.** Confirm where that is
  with `echo $SSH_CLIENT` inside the session - it prints the client IP. The
  browser must run on that same machine, not on your laptop.
- **The forward must be Local (`-L`), not Remote.** In PuTTY the entry has to read
  `L9000` in the forwarded-ports list. A Remote forward connects without error and
  silently does nothing on the client side.

    ssh -L 9000:127.0.0.1:9000 -L 8001:127.0.0.1:8001 USER@10.21.12.62

Tunnels attach only at connection time, so reopen the session after adding one.
In PuTTY, load a saved profile rather than retyping the hostname, or the tunnels
are not applied.

This is a stopgap for the window before ingress exists. Once nginx, DNS and the
certificates are in place, Portainer is reached at `https://portainer.<zone>` from
anywhere that can resolve the name, and no tunnel is needed.

### 502 on every request once nginx is running

SELinux. See section 6.1: `sudo setsebool -P httpd_can_network_connect 1`. The
nginx error log will show `Permission denied` connecting upstream.

---

## 12. Honest limits of this document

- **Nothing here has been executed.** It is written for RHEL 10.2 from the
  documented behaviour of these packages, not from a run on your box. Expect at
  least one surprise.
- **I cannot confirm current package availability**, specifically whether Docker
  publishes an el10 build (section 1) or which nginx version RHEL 10.2 AppStream
  carries. Both have verification commands rather than assumptions.
- **dnf5 command syntax** differs from most published guides. I have flagged the
  `config-manager` case, which is the one that will bite first, but there may be
  others.
- **If Docker turns out to be unavailable for RHEL 10**, do not improvise a
  Podman deployment. It changes the deployment mechanism rather than one command,
  and the Portainer git-stack decision (DEC-10) would need revisiting properly.
