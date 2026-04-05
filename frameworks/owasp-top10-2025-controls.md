# OWASP Top 10 (2025) Controls

The OWASP Top 10 names the most common and impactful web application
security risk classes, refreshed periodically. The 2025 edition is the
current release.

For each category: short description, typical control, and a link to
the handbook entry where the control is detailed.

## A01:2025 -- Broken Access Control

The application authenticates a user but fails to check that the user
is allowed to perform the requested action on the requested resource.
Includes BOLA / IDOR, BFLA, and missing tenant isolation.

Controls:

- Enforce authorization at the data layer; default deny.
- Object-level checks on every resource read and write.
- Server-side role checks independent of UI gating.
- See [../secure-coding/authorization.md](../secure-coding/authorization.md)
  and [../secure-coding/common-pitfalls.md](../secure-coding/common-pitfalls.md).

## A02:2025 -- Security Misconfiguration

Default credentials, debug endpoints exposed, unnecessary services
enabled, missing security headers, overly verbose error pages.

Controls:

- Hardened framework defaults (Spring Security, Django, Flask
  Talisman).
- Configuration-as-code with IaC scanning (Checkov / tfsec).
- Removal of debug endpoints in production builds.
- Security headers: HSTS, CSP, X-Content-Type-Options, frame-ancestors.
- See [../secure-coding/java/spring-security-defaults.md](../secure-coding/java/spring-security-defaults.md),
  [../secure-coding/python/django-flask-defaults.md](../secure-coding/python/django-flask-defaults.md),
  [../devsecops/dockerfile-hardening.md](../devsecops/dockerfile-hardening.md).

## A03:2025 -- Software Supply Chain Failures

Vulnerable, malicious, or unverified dependencies. Includes typosquats,
dependency confusion, namespace squatting, tampered upstream packages,
and untrusted build environments.

Controls:

- SCA scanning on every PR (Trivy / OSV-Scanner / Dependabot).
- Lockfile + hash-pinning per ecosystem.
- SBOM generation per build (CycloneDX / SPDX) with continuous CVE
  matching against the SBOM.
- Signed artifacts (cosign / Sigstore) with attestations.
- SLSA provenance at L2 or L3.
- See [../devsecops/supply-chain/](../devsecops/supply-chain/).

## A04:2025 -- Cryptographic Failures

Sensitive data in transit or at rest without adequate cryptographic
protection. Includes weak hashes, broken algorithms, hard-coded keys,
predictable RNG.

Controls:

- AEAD for symmetric encryption (AES-GCM, ChaCha20-Poly1305).
- KDF for password storage (Argon2id, scrypt, bcrypt, PBKDF2).
- CSPRNG for all security-purpose random values.
- KMS / HSM for long-lived keys; vault for symmetric / API secrets.
- See [../secure-coding/crypto-do-and-dont.md](../secure-coding/crypto-do-and-dont.md)
  and the per-language `crypto-*` files.

## A05:2025 -- Injection

User input flows into a sink (SQL, OS command, LDAP, template,
deserialization, expression evaluator) without separation between data
and code.

Controls:

- Parameterized queries.
- Argument-array subprocess invocation (no shell strings).
- Template engine auto-escape; no `safe` / `raw` / `dangerouslySetInnerHTML`
  on user data.
- Schema-validated input at the trust boundary.
- See [../secure-coding/output-encoding.md](../secure-coding/output-encoding.md)
  and the per-language injection files.

## A06:2025 -- Insecure Design

Class of defects rooted in design omissions: missing rate limits,
weak threat model, implicit-trust assumptions across services, lack
of business-logic validation.

Controls:

- Threat modelling on every design that crosses a trust boundary.
- Abuse-case enumeration alongside use cases.
- Reference architecture per common pattern (REST API, SSO broker,
  mobile client, CI pipeline).
- See [../threat-modeling/](../threat-modeling/) and
  [../architecture/](../architecture/).

## A07:2025 -- Authentication Failures

Weak password policy, missing MFA, broken account recovery, session
fixation, no rate limit on login.

Controls:

- MFA for privileged accounts; phishing-resistant MFA (WebAuthn) where possible.
- Strong password storage (Argon2id).
- Session ID rotation on login, MFA, privilege change.
- Rate limit + lockout on login; constant-time generic error.
- See [../secure-coding/authentication.md](../secure-coding/authentication.md)
  and [../secure-coding/session-management.md](../secure-coding/session-management.md).

## A08:2025 -- Software or Data Integrity Failures

Integrity failures across the SDLC: unsigned releases, unverified
deserialization, mutable references in CI, signed-but-unverified
content.

Controls:

- Signed images / artifacts with admission-time verification.
- SLSA provenance attestations.
- Schema-typed deserialisation; no `pickle` / `ObjectInputStream` on
  network bytes.
- Pin third-party Actions / Docker images by SHA digest.
- See [../secure-coding/deserialization.md](../secure-coding/deserialization.md)
  and [../devsecops/supply-chain/slsa-levels.md](../devsecops/supply-chain/slsa-levels.md).

## A09:2025 -- Security Logging and Alerting Failures

Insufficient or untrustworthy audit trail; lack of detection on
auth-failure spikes, privilege-change events, abnormal data access.

Controls:

- Structured audit logs with principal / action / outcome / correlation.
- No secrets / PII in logs.
- Centralised tamper-resistant log store with retention per policy.
- Alerting on auth-failure spikes, privilege escalation events.
- See [../secure-coding/error-handling-logging.md](../secure-coding/error-handling-logging.md).

## A10:2025 -- Mishandling of Exceptional Conditions

Errors handled poorly: stack traces returned to caller, sensitive
details disclosed in exception messages, swallowed exceptions hiding
attacks, fail-open behaviour where fail-closed was required.

Controls:

- User-facing errors generic and stable (RFC 7807 Problem Details).
- Detailed exception captured server-side with correlation ID.
- Default to fail-closed on auth / authorization / admission errors.
- No silent exception swallowing in code review checklist.
- See [../secure-coding/error-handling-logging.md](../secure-coding/error-handling-logging.md)
  and [../secure-sdlc/code-review-checklist.md](../secure-sdlc/code-review-checklist.md).

## Changes from 2021

- Software Supply Chain Failures (A03:2025) broadens 2021's "Vulnerable and Outdated Components" to cover the full supply-chain surface.
- Security Misconfiguration moved from A05:2021 to A02:2025.
- Mishandling of Exceptional Conditions (A10:2025) is new; replaces 2021's SSRF as a top-level entry. SSRF remains a sub-category of broken access control / injection in modern editions.
- "Identification and Authentication Failures" renamed to "Authentication Failures" (A07:2025).
- "Security Logging and Monitoring Failures" renamed to "Security Logging and Alerting Failures" (A09:2025).

## References

- OWASP Top 10 (2025): <https://owasp.org/Top10/>
- OWASP Top 10 (2021) for comparison: <https://owasp.org/Top10/2021/>
- OWASP Cheat Sheet Series: <https://cheatsheetseries.owasp.org/>
- CWE Top 25 (2025): <https://cwe.mitre.org/top25/>
