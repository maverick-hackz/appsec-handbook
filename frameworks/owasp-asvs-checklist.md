# OWASP ASVS 5.0 Checklist

A compressed checklist of OWASP ASVS 5.0 verification requirements,
organized by chapter. Each requirement carries a level indicator:

| Level | Use when |
| --- | --- |
| L1 | All applications. Baseline security; achievable via design review. |
| L2 | Most applications that handle sensitive transactions. |
| L3 | High-assurance applications: critical infrastructure, defence, very-high-value targets. |

This is a working subset; consult the full ASVS document for every
control. The chapter numbering reflects ASVS 5.0; see
<!-- TODO: verify chapter numbering against the published ASVS 5.0 release once stable -->
the official document for the full text and any revisions.

## Status field

For each requirement, the team records: `pass`, `fail`,
`not-applicable` (with justification), or `partial` (with follow-up
ticket).

## Chapters (high-level)

| ID | Chapter | Topic |
| --- | --- | --- |
| V1 | Encoding and sanitization | Input handling, output encoding |
| V2 | Validation and business logic | Schema validation, business-rule enforcement |
| V3 | Web frontend | DOM-side concerns, CSP, headers |
| V4 | API and web service | REST / GraphQL / gRPC verification |
| V5 | File handling | Upload, processing, storage |
| V6 | Authentication | Credentials, MFA, recovery |
| V7 | Session management | Cookies, tokens, lifecycle |
| V8 | Authorization | RBAC, ABAC, object- and function-level |
| V9 | Self-contained tokens | JWT, JWE, SAML assertions |
| V10 | OAuth and OIDC | Authorization Code + PKCE, Device Code |
| V11 | Cryptography | Key management, algorithm selection |
| V12 | Secure communications | TLS configuration, certificate validation |
| V13 | Configuration | Secrets, dependencies, server defaults |
| V14 | Logging and error handling | Audit log shape, error disclosure |
| V15 | Data protection | Classification, retention, redaction |
| V16 | Privacy | Personal data handling per GDPR / equivalent |

(Chapter set per ASVS 5.0; verify against the published document.)

## Sample requirements (illustrative)

| Req ID | Level | Requirement | Status | Verification |
| --- | --- | --- | --- | --- |
| V1.1.1 | L1 | Output encoding context-aware per sink (HTML, attribute, URL, JS). | | Code review; SAST |
| V2.1.1 | L1 | Schema-validate every untrusted input at the boundary; reject unknown fields. | | Code review; integration test |
| V4.1.1 | L1 | API enforces authorization on every resource access. | | Integration test (BOLA assertion) |
| V6.2.4 | L2 | Password hashing uses Argon2id / scrypt / bcrypt / PBKDF2 with adequate parameters. | | Code review; SAST rule |
| V6.4.1 | L2 | Multi-factor authentication for all accounts above a defined sensitivity tier. | | Penetration test; IdP policy review |
| V7.1.1 | L1 | Session identifiers are at least 128 bits of entropy from a CSPRNG. | | Code review |
| V7.4.2 | L2 | Session identifier rotates on login, MFA, and privilege change. | | Integration test |
| V8.2.1 | L2 | Authorization checks enforced at the data layer, not only at the controller. | | Code review; data-layer test |
| V9.4.1 | L2 | JWT verification pins the algorithm; rejects `alg=none` and key confusion. | | SAST rule; integration test |
| V10.2.1 | L2 | OAuth public clients use Authorization Code with PKCE; Implicit and ROPC are not used. | | Code review |
| V11.1.4 | L1 | Random values for security use the OS CSPRNG (`secrets`, `crypto/rand`). | | SAST rule |
| V11.2.1 | L2 | Symmetric encryption uses AEAD (AES-GCM, ChaCha20-Poly1305). | | SAST rule; code review |
| V12.1.1 | L1 | TLS 1.2 minimum, TLS 1.3 preferred; weak suites disabled. | | testssl.sh against staging |
| V13.1.1 | L1 | Secrets sourced from a vault or platform secret store; none in source. | | Secret scan; code review |
| V13.3.1 | L2 | SCA scan passes for dependencies with no unresolved HIGH/CRITICAL CVE. | | SCA in CI |
| V14.1.1 | L1 | User-facing errors omit stack traces and internal paths. | | DAST scan |
| V14.2.1 | L1 | Audit log captures principal, action, outcome, timestamp, correlation ID. | | Integration test |
| V15.1.1 | L2 | Persistent data is encrypted at rest via KMS-managed keys. | | Cloud config review |
| V16.1.1 | L2 | Personal data has documented retention and deletion-on-request paths. | | Policy review |

The compressed list above is a starting point; the team adds rows
from the full ASVS document for each chapter relevant to its
application.

## How to run a self-assessment

1. Choose the target level (L1 / L2 / L3) per asset, not per
   application; a single application can mix levels for different
   data classes.
2. For each requirement, record status with evidence (test ID, scan
   ID, code review link).
3. For `not-applicable` items, document why (e.g., "no file upload
   path in this service").
4. For `fail` / `partial`, create a backlog item with priority and
   owner.
5. Re-assess on major releases or quarterly, whichever is sooner.

## References

- OWASP ASVS 5.0: <https://owasp.org/www-project-application-security-verification-standard/>
- ASVS GitHub (source of record): <https://github.com/OWASP/ASVS>
- OWASP Cheat Sheet Series (per-requirement detail): <https://cheatsheetseries.owasp.org/>
