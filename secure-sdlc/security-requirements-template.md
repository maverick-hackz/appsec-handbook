# Security Requirements Template

A security requirement is a testable statement about behaviour or
property of the system, with a rationale and a verification method.
Capture them alongside functional requirements in the same backlog,
prefixed `SR-` so they survive scope changes.

## Field schema

| Field | Description |
| --- | --- |
| ID | `SR-<DOMAIN>-NNN` (AUTHN, AUTHZ, SESS, CRYPTO, INPUT, OUTPUT, LOG, SECRET, DEPS, TLS, ERR) |
| Requirement | One sentence. Use MUST / SHOULD / MUST NOT (RFC 2119). Singular and testable. |
| Rationale | Why the requirement exists. Reference framework (ASVS Vx.x.x, SSDF PW.4.x), CWE, or incident. |
| Priority | P0 (release-blocking) / P1 (next release) / P2 (backlog) |
| Verification | How the team confirms compliance: code review, SAST rule, integration test, pentest, design review. |

## Example requirement set

| ID | Requirement | Rationale | Priority | Verification |
| --- | --- | --- | --- | --- |
| SR-AUTHN-001 | All authentication flows MUST enforce MFA for privileged accounts. | NIST SP 800-63B AAL2/AAL3; reduces account-takeover risk. | P0 | Penetration test; review IdP policy. |
| SR-AUTHN-002 | Failed login responses MUST be indistinguishable between unknown user and wrong password, in both body and timing. | OWASP ASVS V3.2.3; username-enumeration class. | P1 | Integration test that compares status + body + median latency. |
| SR-AUTHN-003 | Account lockout MUST be temporary (e.g., exponential delay) rather than permanent to avoid denial-of-service via login abuse. | NIST SP 800-63B §5.2.2. | P1 | Manual review; load test. |
| SR-AUTHZ-001 | Every resource fetch MUST verify the principal has a relationship with the resource, not only that the principal is authenticated. | OWASP API1:2023 (BOLA). | P0 | Integration test asserts 403 (or 404) for cross-tenant fetch. |
| SR-AUTHZ-002 | Privileged operations MUST be checked server-side independently of UI gating. | OWASP API5:2023 (BFLA). | P0 | Integration test calls privileged endpoint with non-privileged JWT. |
| SR-SESS-001 | Session identifiers MUST be at least 128 bits of entropy from a CSPRNG. | CWE-330; OWASP Session Management Cheat Sheet. | P0 | Code review; review CSPRNG usage. |
| SR-SESS-002 | Session identifiers MUST rotate on login, MFA challenge, and privilege change. | CWE-384 (Session Fixation); OWASP Session Management Cheat Sheet. | P0 | Integration test that compares cookie before / after login. |
| SR-SESS-003 | Cookies that carry session state MUST set `Secure`, `HttpOnly`, and `SameSite=Lax` or stricter. | OWASP ASVS V3.4.1-3. | P0 | DAST baseline scan; manual review of `Set-Cookie`. |
| SR-CRYPTO-001 | Passwords MUST be hashed with Argon2id (m=64 MiB, t=3, p=4 minimum) or scrypt / bcrypt / PBKDF2-HMAC-SHA-256 with NIST-recommended work factors. | OWASP ASVS V2.4.1; RFC 9106. | P0 | Code review; SAST rule on hashing call sites. |
| SR-CRYPTO-002 | Symmetric encryption MUST use AEAD (AES-256-GCM or ChaCha20-Poly1305). AES-ECB and unauthenticated CBC are prohibited. | OWASP ASVS V6.2.4-6; NIST SP 800-38D. | P0 | SAST rule for `AES/ECB/*` and `Cipher("AES")` strings; code review. |
| SR-CRYPTO-003 | Random values used for security purposes MUST come from the OS CSPRNG (`secrets`, `crypto/rand`, `java.security.SecureRandom`). | CWE-338. | P0 | SAST rule that flags `Math.random`, `rand()`, `java.util.Random`. |
| SR-INPUT-001 | All untrusted input MUST be validated against an allowlist (type, length, character class, semantic range) at the trust boundary. | OWASP ASVS V5.1; CWE-20. | P0 | Code review; schema validation tests. |
| SR-OUTPUT-001 | All user-controlled data rendered into HTML, attributes, URLs, or JavaScript contexts MUST go through context-appropriate encoding. | CWE-79; OWASP XSS Prevention Cheat Sheet. | P0 | SAST rules for `dangerouslySetInnerHTML`, `v-html`, manual review. |
| SR-OUTPUT-002 | SQL queries that include user input MUST use parameterized APIs; string concatenation into SQL is prohibited. | CWE-89; OWASP SQL Injection Prevention Cheat Sheet. | P0 | SAST rule; code review on every `db.Query` / `execute` call. |
| SR-LOG-001 | Logs MUST NOT contain passwords, tokens, API keys, full government ID numbers, or private keys. | OWASP ASVS V7.1.1; CWE-532. | P0 | Code review of log statements; field-level redaction in logger config. |
| SR-LOG-002 | Authentication events (login success, login failure, MFA challenge, password change) MUST be logged with principal ID, timestamp, action, outcome, and correlation ID. | OWASP ASVS V7.1; NIST SP 800-92. | P0 | Integration test asserts log entry shape for each event. |
| SR-SECRET-001 | Secrets MUST NOT be committed to source. All deployed secrets MUST come from a vault or platform secret store. | OWASP ASVS V14.3.3; CWE-798. | P0 | Pre-commit and CI secret scanning (gitleaks, trufflehog). |
| SR-DEPS-001 | Direct and transitive dependencies MUST have no unresolved HIGH or CRITICAL CVEs at release time. | OWASP A06:2021. | P0 | SCA scan (Trivy / Snyk / OSV-Scanner) in CI; fail on HIGH or CRITICAL. |
| SR-DEPS-002 | A CycloneDX SBOM MUST be generated for each release artifact and stored alongside the artifact. | NIST SSDF PS.3.2; CycloneDX 1.x. | P1 | CI step generates and uploads SBOM; admission policy verifies presence. |
| SR-TLS-001 | All external network communication MUST use TLS 1.2 or 1.3; TLS 1.0, 1.1, SSLv3, RC4, and 3DES are prohibited. | OWASP ASVS V9.1.2; NIST SP 800-52 Rev 2. | P0 | DAST scan; vendor TLS-test (testssl.sh) on each public endpoint. |
| SR-ERR-001 | User-facing error responses MUST NOT include stack traces, internal paths, or query fragments. | CWE-209. | P0 | DAST scan; integration test for unhandled exception path. |

The example set is not exhaustive. Add domain-specific requirements
(healthcare, sensitive personal data, regulated industries) as they
arise; keep them in the same shape.

## How to use

- During design, list applicable requirements per component.
- During implementation, link each PR's "Closes" to the requirement
  IDs satisfied.
- During pre-release, walk the requirement list and confirm each
  verification method has produced evidence.
- Stale requirements: when a control changes, update the requirement;
  do not let it drift.

## References

- OWASP ASVS: <https://owasp.org/www-project-application-security-verification-standard/>
- NIST SSDF (SP 800-218): <https://csrc.nist.gov/Projects/ssdf>
- NIST SP 800-63B (Authenticator Requirements): <https://pages.nist.gov/800-63-3/sp800-63b.html>
- NIST SP 800-52 Rev 2 (TLS guidance): <https://csrc.nist.gov/publications/detail/sp/800-52/rev-2/final>
- RFC 2119 (MUST / SHOULD): <https://datatracker.ietf.org/doc/html/rfc2119>
- RFC 9106 (Argon2): <https://datatracker.ietf.org/doc/html/rfc9106>
