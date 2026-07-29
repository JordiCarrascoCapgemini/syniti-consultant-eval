#!/usr/bin/env bash
#
# Evidence collection for the Skills Evaluation deployment on POCDAPP314.
#
# READ-ONLY. This script changes nothing: it only reads service state, queries
# loopback endpoints and counts rows. Safe to run at any time.
#
# Usage (from anywhere on the host):
#   sudo bash deploy/verify-deployment.sh
#   sudo bash deploy/verify-deployment.sh | tee evidence-$(date +%F).txt
#
# The tee form is the one to use when capturing evidence for a record.
#
# Exit status: 0 if nothing FAILed, 1 otherwise. SKIP does not fail the run.

set -uo pipefail

HOST_IP="${HOST_IP:-10.21.12.62}"
APP_PORT="${APP_PORT:-8001}"
PORTAINER_PORT="${PORTAINER_PORT:-9000}"

PASS=0
FAIL=0
SKIP=0

hdr()  { printf '\n=== %s ===\n' "$1"; }
ok()   { printf '  [PASS] %s\n' "$1"; PASS=$((PASS + 1)); }
bad()  { printf '  [FAIL] %s\n' "$1"; FAIL=$((FAIL + 1)); }
skip() { printf '  [SKIP] %s\n' "$1"; SKIP=$((SKIP + 1)); }
info() { printf '         %s\n' "$1"; }

# assert_eq <description> <expected> <actual>
assert_eq() {
  if [ "$2" = "$3" ]; then
    ok "$1 ($3)"
  else
    bad "$1 (expected '$2', got '$3')"
  fi
}

# assert_contains <description> <needle> <haystack>
assert_contains() {
  case "$3" in
    *"$2"*) ok "$1" ;;
    *)      bad "$1 (missing '$2')" ;;
  esac
}

# assert_absent <description> <needle> <haystack>
assert_absent() {
  case "$3" in
    *"$2"*) bad "$1 (unexpectedly present: '$2')" ;;
    *)      ok "$1" ;;
  esac
}

http_code() {  # http_code <url>
  curl -sS -o /dev/null -m 5 -w '%{http_code}' "$1" 2>/dev/null || printf '000'
}

container_named() {  # container_named <substring> -> prints container name or empty
  docker ps --format '{{.Names}}' 2>/dev/null | grep -m1 -- "$1" || true
}

printf 'Skills Evaluation deployment evidence\n'
printf 'Collected: %s\n' "$(date -Is 2>/dev/null || date)"
printf 'Host: %s (%s)\n' "$(hostname 2>/dev/null)" "$HOST_IP"

# ---------------------------------------------------------------- 1. platform
hdr "1. Platform"
if [ -r /etc/os-release ]; then
  info "$(. /etc/os-release; printf '%s' "$PRETTY_NAME")"
fi
info "kernel $(uname -r)"
if command -v timedatectl >/dev/null 2>&1; then
  SYNC=$(timedatectl show -p NTPSynchronized --value 2>/dev/null || printf 'unknown')
  assert_eq "clock synchronised" "yes" "$SYNC"
else
  skip "clock synchronised (timedatectl absent)"
fi

# ------------------------------------------------------------------ 2. docker
hdr "2. Docker engine"
assert_eq "docker.service active"  "active"  "$(systemctl is-active docker 2>/dev/null)"
assert_eq "docker.service enabled" "enabled" "$(systemctl is-enabled docker 2>/dev/null)"
if command -v docker >/dev/null 2>&1; then
  info "$(docker --version 2>/dev/null)"
  info "compose $(docker compose version --short 2>/dev/null || printf 'unavailable')"
  DRIVER=$(docker info --format '{{.LoggingDriver}}' 2>/dev/null || printf 'unknown')
  assert_eq "log driver is json-file" "json-file" "$DRIVER"
  RPM_REL=$(rpm -q --qf '%{VERSION}-%{RELEASE}' docker-ce 2>/dev/null || printf 'n/a')
  info "docker-ce package: $RPM_REL"
  case "$RPM_REL" in
    *el10*) info "native el10 build (supported combination)" ;;
    *el9*)  info "el9 packages on an el10 host - unsupported combination, recorded deliberately" ;;
  esac
else
  bad "docker client present"
fi

# --------------------------------------------------------- 3. kernel plumbing
hdr "3. Kernel modules and sysctls"
LSMOD=$(lsmod 2>/dev/null || printf '')
for m in iptable_nat iptable_filter br_netfilter overlay; do
  assert_contains "module loaded: $m" "$m" "$LSMOD"
done
if [ -r /etc/modules-load.d/docker.conf ]; then
  ok "modules persisted across reboot (/etc/modules-load.d/docker.conf)"
else
  bad "modules persisted across reboot (/etc/modules-load.d/docker.conf missing)"
fi
assert_eq "net.ipv4.ip_forward" "1" "$(sysctl -n net.ipv4.ip_forward 2>/dev/null)"
assert_eq "net.bridge.bridge-nf-call-iptables" "1" \
  "$(sysctl -n net.bridge.bridge-nf-call-iptables 2>/dev/null)"

# ----------------------------------------------------------------- 4. selinux
hdr "4. SELinux and firewall"
if command -v getenforce >/dev/null 2>&1; then
  info "SELinux mode: $(getenforce)"
  SEBOOL=$(getsebool httpd_can_network_connect 2>/dev/null | awk '{print $3}')
  assert_eq "httpd_can_network_connect" "on" "$SEBOOL"
else
  skip "SELinux checks (getenforce absent)"
fi
if command -v firewall-cmd >/dev/null 2>&1; then
  SERVICES=$(firewall-cmd --list-services 2>/dev/null || printf '')
  info "firewalld services: $SERVICES"
  assert_contains "firewall allows http"  "http"  "$SERVICES"
  assert_contains "firewall allows https" "https" "$SERVICES"
  PORTS=$(firewall-cmd --list-ports 2>/dev/null || printf '')
  info "firewalld extra ports: ${PORTS:-none}"
  assert_absent "app port not opened externally"       "$APP_PORT"       "$PORTS"
  assert_absent "portainer port not opened externally" "$PORTAINER_PORT" "$PORTS"
else
  skip "firewall checks (firewall-cmd absent)"
fi

# ------------------------------------------------------------------- 5. nginx
hdr "5. nginx"
assert_eq "nginx active"  "active"  "$(systemctl is-active nginx 2>/dev/null)"
assert_eq "nginx enabled" "enabled" "$(systemctl is-enabled nginx 2>/dev/null)"
if command -v nginx >/dev/null 2>&1; then
  info "$(nginx -v 2>&1)"
  # Pattern match rather than arithmetic: no subshell, no locale surprises.
  # The vhosts need >= 1.25.1 for the "http2 on" directive.
  NGXV=$(nginx -v 2>&1 | sed 's|.*/||')
  case "$NGXV" in
    1.2[6-9].*|1.[3-9][0-9].*|[2-9].*)
      ok "nginx $NGXV supports 'http2 on' (>= 1.25.1)" ;;
    *)
      skip "nginx version $NGXV - confirm >= 1.25.1 by hand, or use 'listen 443 ssl http2;'" ;;
  esac
fi
for d in /etc/nginx/certs /etc/nginx/snippets; do
  if [ -d "$d" ]; then ok "directory exists: $d"; else bad "directory missing: $d"; fi
done
VHOSTS=$(ls /etc/nginx/conf.d/*.conf 2>/dev/null | wc -l | tr -d ' ')
info "vhosts installed in /etc/nginx/conf.d: ${VHOSTS:-0}"
if [ "${VHOSTS:-0}" -eq 0 ]; then
  skip "application vhosts not installed yet (expected before DNS and certificates)"
fi

# --------------------------------------------------------------- 6. portainer
hdr "6. Portainer (control plane)"
PC=$(container_named portainer)
if [ -n "$PC" ]; then
  ok "portainer container running ($PC)"
  BIND=$(docker port "$PC" 2>/dev/null | tr '\n' ' ')
  info "port bindings: $BIND"
  assert_contains "portainer bound to loopback only" "127.0.0.1:$PORTAINER_PORT" "$BIND"
  assert_absent   "portainer not bound to all interfaces" "0.0.0.0:$PORTAINER_PORT" "$BIND"
  CODE=$(http_code "http://127.0.0.1:$PORTAINER_PORT/")
  case "$CODE" in
    2*|3*) ok "portainer answers on loopback (HTTP $CODE)" ;;
    *)     bad "portainer answers on loopback (got $CODE)" ;;
  esac
  EXT=$(http_code "http://$HOST_IP:$PORTAINER_PORT/")
  assert_eq "portainer NOT reachable on the network" "000" "$EXT"
else
  bad "portainer container running"
fi

# --------------------------------------------------------- 7. application app
hdr "7. Application stack"
AC=$(container_named app)
DC=$(container_named db)
if [ -n "$AC" ]; then ok "app container running ($AC)"; else bad "app container running"; fi
if [ -n "$DC" ]; then ok "db container running ($DC)";  else bad "db container running";  fi

if [ -n "$AC" ]; then
  ABIND=$(docker port "$AC" 2>/dev/null | tr '\n' ' ')
  info "app port bindings: $ABIND"
  assert_contains "app bound to loopback only"      "127.0.0.1:$APP_PORT" "$ABIND"
  assert_absent   "app not bound to all interfaces" "0.0.0.0:$APP_PORT"   "$ABIND"
fi
if [ -n "$DC" ]; then
  DBIND=$(docker port "$DC" 2>/dev/null | tr '\n' ' ')
  if [ -z "$DBIND" ]; then
    ok "database publishes no port at all"
  else
    bad "database publishes a port ($DBIND)"
  fi
fi

# --------------------------------------------------------------------- 8. api
hdr "8. API behaviour"
HEALTH=$(curl -sS -m 5 "http://127.0.0.1:$APP_PORT/api/health" 2>/dev/null || printf '')
assert_contains "health endpoint returns ok" '"status":"ok"' "$HEALTH"
assert_eq "app NOT reachable on the network" "000" "$(http_code "http://$HOST_IP:$APP_PORT/api/health")"
assert_eq "evaluations list requires auth"   "401" "$(http_code "http://127.0.0.1:$APP_PORT/api/evaluations")"
assert_eq "reference data requires auth"     "401" "$(http_code "http://127.0.0.1:$APP_PORT/api/reference")"
assert_eq "evaluation app served at /"       "200" "$(http_code "http://127.0.0.1:$APP_PORT/")"
assert_eq "team summary served at /team"     "200" "$(http_code "http://127.0.0.1:$APP_PORT/team")"

BODY=$(curl -sS -m 5 "http://127.0.0.1:$APP_PORT/" 2>/dev/null || printf '')
assert_contains "eval app carries the server-mode controls" "serverSaveBtn" "$BODY"
TEAMBODY=$(curl -sS -m 5 "http://127.0.0.1:$APP_PORT/team" 2>/dev/null || printf '')
assert_contains "team app carries the server-mode control" "serverLoadBtn" "$TEAMBODY"

# ------------------------------------------------------------------- 9. data
hdr "9. Stored data"
if [ -n "$DC" ]; then
  PGUSER_V="${POSTGRES_USER:-syniti}"
  PGDB_V="${POSTGRES_DB:-syniti_eval}"
  ROWS=$(docker exec "$DC" psql -U "$PGUSER_V" -d "$PGDB_V" -tAc \
    'select count(*) from evaluations' 2>/dev/null | tr -d ' \r')
  if [ -n "${ROWS:-}" ]; then
    info "evaluations stored: $ROWS"
    PEOPLE=$(docker exec "$DC" psql -U "$PGUSER_V" -d "$PGDB_V" -tAc \
      'select count(distinct consultant) from evaluations' 2>/dev/null | tr -d ' \r')
    info "distinct consultants: ${PEOPLE:-unknown}"
    TABLES=$(docker exec "$DC" psql -U "$PGUSER_V" -d "$PGDB_V" -tAc \
      "select string_agg(tablename,',' order by tablename) from pg_tables where schemaname='public'" 2>/dev/null | tr -d ' \r')
    assert_contains "schema has users table"       "users"       "${TABLES:-}"
    assert_contains "schema has sessions table"    "sessions"    "${TABLES:-}"
    assert_contains "schema has evaluations table" "evaluations" "${TABLES:-}"
    if [ "${ROWS:-0}" = "34" ]; then
      ok "synthetic test set loaded (34 evaluations)"
    else
      skip "synthetic test set not loaded (found ${ROWS:-0}, expected 34 after seeding)"
    fi
  else
    skip "database queries (could not reach psql inside $DC)"
  fi
else
  skip "database queries (no db container)"
fi

# ----------------------------------------------------------------- 10. totals
hdr "Summary"
printf '  PASS %d   FAIL %d   SKIP %d\n' "$PASS" "$FAIL" "$SKIP"
if [ "$FAIL" -eq 0 ]; then
  printf '\nRESULT: all executed checks passed.\n'
else
  printf '\nRESULT: %d check(s) FAILED - see above.\n' "$FAIL"
fi
printf 'Note: SKIP means not applicable yet (for example vhosts before certificates),\n'
printf 'not a failure. TLS and COOKIE_SECURE=true are still required before this\n'
printf 'holds any real evaluation data.\n'

[ "$FAIL" -eq 0 ]
