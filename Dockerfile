# syntax=docker/dockerfile:1
#
# Skills Evaluation server. Single stage: the two apps are hand-written
# single-file HTML with no build step and no npm, so there is nothing to compile.
# The eval app is build output, so it is generated here rather than trusted from
# the build context.

FROM python:3.12-slim

# Non-root runtime user. Nothing runs as root past the USER line below.
RUN groupadd --gid 1000 syniti \
    && useradd --uid 1000 --gid syniti --create-home --shell /usr/sbin/nologin syniti

WORKDIR /app

COPY requirements.txt .
RUN pip install --no-cache-dir -r requirements.txt

# Filtered by .dockerignore: sources/ (1.4MB of PDF and xlsm), graphify-out/,
# build/build-scripts/ and build/legacy/ never enter the build context.
COPY . .

# Rebuild both apps from data/*.json so the image can never ship a stale
# embedded COMPS. Fails the build if a placeholder survives or an em dash
# appears (build.py's own guards).
RUN python build/build.py

USER syniti

ENV PORT=8000
EXPOSE 8000

# No curl in slim; plain stdlib against the unauthenticated /health route.
HEALTHCHECK --interval=30s --timeout=5s --start-period=10s --retries=3 \
    CMD ["python", "-c", "import os, urllib.request; urllib.request.urlopen('http://127.0.0.1:' + os.environ.get('PORT', '8000') + '/api/health', timeout=3)"]

# Shell form so ${PORT} expands; uvicorn's CLI does not read PORT itself.
#
# --proxy-headers makes uvicorn honour X-Forwarded-Proto/For from nginx, so the
# app sees the client's real scheme and address rather than the proxy hop.
# --forwarded-allow-ips="*" is safe ONLY because the container port is published
# on 127.0.0.1 (see docker-compose.yml): nothing but the host's nginx can reach
# it, and the Docker bridge gateway address it arrives from is not stable enough
# to pin. If that loopback binding is ever widened, this must be narrowed too.
CMD ["sh", "-c", "uvicorn server.app:app --host 0.0.0.0 --port ${PORT} --proxy-headers --forwarded-allow-ips=*"]
