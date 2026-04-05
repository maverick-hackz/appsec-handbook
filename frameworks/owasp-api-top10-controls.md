# OWASP API Security Top 10 (2023) Controls

The 2023 edition focuses on REST / GraphQL / gRPC APIs as
distinct from web frontends. Each item below lists typical
controls and a pointer to the handbook section that elaborates.

## API1:2023 -- Broken Object Level Authorization (BOLA)

The endpoint authenticates the user but does not check that the user
owns or has access to the requested object.

Controls:

- Object-level authorization in the repository / service layer.
- UUID identifiers (non-enumerable) plus the check; never rely on
  obscurity alone.
- Integration test: assert 403 / 404 for cross-tenant fetch.
- See [../secure-coding/authorization.md](../secure-coding/authorization.md).

## API2:2023 -- Broken Authentication

Weak or missing authentication on API endpoints; tokens with no
algorithm pinning; long-lived bearer tokens for machine-to-machine.

Controls:

- Algorithm pin on JWT verification; reject `alg=none`.
- Short-lived access tokens with refresh rotation and reuse detection.
- mTLS or OIDC client credentials for machine clients.
- See [../secure-coding/authentication.md](../secure-coding/authentication.md),
  [../secure-coding/javascript-typescript/jwt-handling.md](../secure-coding/javascript-typescript/jwt-handling.md).

## API3:2023 -- Broken Object Property Level Authorization

Mass-assignment: client can set fields they should not (`is_admin`).
Or excessive data exposure: response includes fields the user should
not see.

Controls:

- DTO with explicit input / output field allowlists.
- Server-side projection of response by the authenticated principal.
- Distinct DTOs for admin vs user vs public response shapes.

## API4:2023 -- Unrestricted Resource Consumption

No rate limits or quotas on expensive operations (export, search,
pagination, computational endpoints).

Controls:

- Per-principal AND per-IP rate limit (token bucket / leaky bucket).
- Query timeouts and result-size caps.
- Per-tenant quotas on storage / requests / external calls.
- Pagination with maximum page size enforced server-side.

## API5:2023 -- Broken Function Level Authorization (BFLA)

User can call privileged functions because the role check is on the
UI only.

Controls:

- Server-side role check on every privileged endpoint.
- Distinct paths for privileged operations (`/admin/...`) so they are
  visible in audits.
- Integration test: non-privileged JWT cannot reach privileged
  endpoint.
- See [../secure-coding/authorization.md](../secure-coding/authorization.md).

## API6:2023 -- Unrestricted Access to Sensitive Business Flows

Automation abuses a legitimate flow (purchase, signup, follow) at
scale, beyond intent.

Controls:

- Per-account velocity limits and CAPTCHA-equivalents.
- Anomaly detection on sensitive flows (signup rate by IP / ASN,
  signup-from-new-IP).
- Step-up authentication on transactions above a threshold.

## API7:2023 -- Server Side Request Forgery (SSRF)

Endpoint accepts a URL or hostname from the client and fetches it
server-side without restriction; targets cloud metadata, internal
admin interfaces, private ranges.

Controls:

- Per-host allowlist; reject loopback / private / link-local ranges.
- Disable redirects, or re-validate the destination after each
  redirect.
- Network egress allowlist as defence in depth.
- See [../secure-coding/go/ssrf-net-http.md](../secure-coding/go/ssrf-net-http.md).

## API8:2023 -- Security Misconfiguration

Verbose errors, default credentials, missing security headers,
out-of-date components, debug endpoints exposed.

Controls:

- Hardened framework defaults; IaC scanning; container hardening.
- Production-only configuration with no `DEBUG`, no `ALLOWED_HOSTS=*`.
- Health endpoint authenticated or scoped to the orchestrator.
- See [../secure-coding/java/spring-security-defaults.md](../secure-coding/java/spring-security-defaults.md),
  [../devsecops/dockerfile-hardening.md](../devsecops/dockerfile-hardening.md).

## API9:2023 -- Improper Inventory Management

Old API versions kept alive; staging endpoints reachable from prod;
undocumented endpoints; no per-route SCA / DAST coverage.

Controls:

- API inventory generated from OpenAPI / GraphQL schema in CI.
- Deprecation policy with sunset dates and 410 Gone responses.
- DAST scan keyed off the inventory, not free-form crawling.
- See [../tooling-evaluation/dast-evaluation-methodology.md](../tooling-evaluation/dast-evaluation-methodology.md).

## API10:2023 -- Unsafe Consumption of APIs

Client trusts a third-party API response without validating it; can
chain RCE / SSRF / data corruption.

Controls:

- Treat third-party API responses as untrusted; schema-validate.
- Pin TLS, validate certificates; no `InsecureSkipVerify`.
- Apply the same parameterisation / injection-prevention rules to
  data coming from third parties as to user input.

## How to use this list

- Cross-check each API endpoint against API1, API3, API5 (the three
  authorization-class entries); BOLA / BFLA bugs are the most common
  modern API findings.
- Pair API4 / API6 controls in the API gateway, not in every
  service; central enforcement is cheaper to operate and audit.
- Combine API7 controls (per-service) with egress network policy
  (per-cluster).

## References

- OWASP API Security Top 10 (2023): <https://owasp.org/API-Security/editions/2023/en/0x00-header/>
- OWASP Cheat Sheet Series: <https://cheatsheetseries.owasp.org/>
- OWASP Threat Modeling Manifesto: <https://www.threatmodelingmanifesto.org/>
