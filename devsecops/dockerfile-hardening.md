# Dockerfile Hardening

Container image baseline. The checklist below is what `hadolint`,
`trivy image`, and the K8s admission policies expect.

## Checklist

- [ ] Multi-stage build: a `builder` stage with the toolchain, a final
      runtime stage with only the binary and runtime dependencies.
- [ ] Pinned base image by digest:
      `FROM image@sha256:<digest>`, not `FROM image:tag`.
- [ ] Minimal base for the runtime stage: distroless, alpine, or scratch
      where the application allows.
- [ ] Non-root user: numeric UID/GID (e.g., `10001:10001`) with
      `USER 10001:10001`. Avoid `USER nobody` (UID varies by base).
- [ ] No secrets in any layer. Use BuildKit secret mounts for
      build-time credentials; runtime secrets come from the orchestrator.
- [ ] `.dockerignore` mirrors `.gitignore` plus build-time outputs.
- [ ] `HEALTHCHECK` instruction set (or equivalent at the orchestrator
      level if it overrides image health-checks).
- [ ] `COPY --chown=<uid>:<gid>` instead of `COPY` + `chown` (avoids an
      extra layer carrying the previous ownership).
- [ ] `apk add --no-cache` / `apt-get -y --no-install-recommends` plus
      cleanup of the package index in the same `RUN`.
- [ ] No `ADD <url>` (use `RUN curl ... && verify-checksum` so the
      verification step is reviewable).
- [ ] Drop capabilities at runtime via Kubernetes
      `securityContext.capabilities.drop: ["ALL"]`. See
      [k8s-policies/pod-security-admission.md](k8s-policies/pod-security-admission.md).

## Insecure example

```dockerfile
FROM node:18                                  # mutable tag
RUN apt-get update && apt-get install -y curl # bloat, no cleanup
COPY . /app                                   # root-owned, includes .env
WORKDIR /app
RUN npm install                               # network at build, no audit
ENV NPM_TOKEN=ghp_abcd...                     # secret in layer history
EXPOSE 3000
CMD ["node", "server.js"]                     # runs as root
```

## Secure example

```dockerfile
# syntax=docker/dockerfile:1.7

# ---- Builder stage --------------------------------------------------
FROM node:20-bookworm-slim@sha256:<digest> AS builder

WORKDIR /app
COPY --link package.json package-lock.json ./

# BuildKit secret mount: NPM_TOKEN available only for this RUN, never
# baked into a layer or visible in `docker history`.
RUN --mount=type=secret,id=npm_token \
    NPM_TOKEN="$(cat /run/secrets/npm_token)" \
    npm ci --ignore-scripts \
 && npm audit --omit=dev --audit-level=high

COPY --link . .
RUN npm run build

# ---- Runtime stage --------------------------------------------------
FROM gcr.io/distroless/nodejs20-debian12@sha256:<digest>

# Non-root numeric user; distroless ships a `nonroot` (65532) account.
USER 65532:65532

WORKDIR /app
COPY --from=builder --chown=65532:65532 /app/dist /app/dist
COPY --from=builder --chown=65532:65532 /app/node_modules /app/node_modules
COPY --from=builder --chown=65532:65532 /app/package.json /app/

EXPOSE 3000
HEALTHCHECK --interval=30s --timeout=5s --start-period=10s --retries=3 \
  CMD ["node", "dist/healthcheck.js"]

ENTRYPOINT ["node", "dist/server.js"]
```

Build:

```bash
echo -n "$NPM_TOKEN" | docker build \
  --secret id=npm_token,src=- \
  -t myorg/svc:$(git rev-parse --short HEAD) .
```

## `.dockerignore`

```text
.git/
.github/
.gitignore
*.md
.env
.env.*
node_modules/
dist/
coverage/
.vscode/
.idea/
.DS_Store
Dockerfile
docker-compose*.yml
```

## Validate before merge

- `hadolint Dockerfile` -- lint
- `trivy config Dockerfile` -- misconfiguration scan
- `trivy image <built-image>` -- vulnerability scan against the final image
- `docker scout cves` -- alternative CVE scanner (vendor-specific)

## At runtime (Kubernetes)

The container alone is not the boundary. Pair the hardened image with
restricted Pod Security Admission:

```yaml
securityContext:
  runAsNonRoot: true
  runAsUser: 65532
  runAsGroup: 65532
  allowPrivilegeEscalation: false
  capabilities:
    drop: ["ALL"]
  readOnlyRootFilesystem: true
  seccompProfile:
    type: RuntimeDefault
```

See [k8s-policies/](k8s-policies/) for the full set of cluster-level
controls.

## References

- OWASP Docker Security Cheat Sheet: <https://cheatsheetseries.owasp.org/cheatsheets/Docker_Security_Cheat_Sheet.html>
- CIS Docker Benchmark: <https://www.cisecurity.org/benchmark/docker>
- Docker BuildKit secrets: <https://docs.docker.com/build/building/secrets/>
- Distroless images: <https://github.com/GoogleContainerTools/distroless>
- hadolint rules: <https://github.com/hadolint/hadolint/wiki>
- Trivy: <https://aquasecurity.github.io/trivy/>
