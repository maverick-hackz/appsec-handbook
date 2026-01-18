# Code Review Checklist (Security-Focused)

For the developer's own review and for the peer reviewer. Yes / no
questions; "no" needs a comment in the PR or a follow-up ticket.

This list does NOT cover offensive testing (that lives in the
companion [Workstation](https://github.com/maverick-hackz/Workstation)
repository) and does not replace SAST. It complements both at the
point of code review.

## Authentication

- [ ] Does this PR introduce or modify an authentication flow?
- [ ] Are passwords stored only via a vetted KDF (Argon2id / scrypt /
      bcrypt / PBKDF2)?
- [ ] Is MFA enforced where required, or is the deferral documented?
- [ ] Is the login response indistinguishable between unknown user
      and wrong password (body + timing)?
- [ ] Are rate limits and lockout applied per username AND per IP / ASN?
- [ ] Are reset tokens generated from a CSPRNG, single-use, with a
      short TTL, and bound to the account?
- [ ] On password change or MFA reset, are other sessions invalidated?

## Authorization

- [ ] Does the new endpoint enforce authorization on every request?
- [ ] Is the authorization check at the data layer (repository /
      service), not only at the controller?
- [ ] For object-level access (`GET /things/{id}`), is the
      principal's relationship to the object verified?
- [ ] For privileged operations, is the role check server-side and
      independent of UI gating?
- [ ] If multi-tenant: is `tenant_id` derived from the verified token
      and not from request input?

## Input validation

- [ ] Is untrusted input validated against an allowlist (type,
      length, character class, range) at the boundary?
- [ ] Is input canonicalised (Unicode normalisation, percent-decoding)
      before validation?
- [ ] Are unknown fields rejected by default in JSON / form parsers?
- [ ] Are file upload paths anchored to a base directory; are file
      names server-generated; is the MIME type validated AND the
      content type re-checked server-side?

## Output encoding

- [ ] Is user data rendered via the templating engine's auto-escape
      mechanism, with no `raw` / `safe` / `dangerouslySetInnerHTML` /
      `v-html`?
- [ ] If `v-html` / `dangerouslySetInnerHTML` is necessary, is the
      string sanitized with a vetted library (DOMPurify) using an
      allowlist?
- [ ] Are URLs validated against a scheme allowlist
      (`http`, `https`)? Are `javascript:`, `data:text/html`, and
      `vbscript:` rejected?

## Injection (parameterized APIs)

- [ ] Are SQL queries parameterized; is no string concatenation
      reaching `Query` / `Execute` / `executeQuery`?
- [ ] Are OS commands invoked with argument lists, not shell strings?
- [ ] For NoSQL: is request input shape-validated before reaching the
      query? Are operator keys (`$ne`, `$gt`, `$where`) rejected from
      user-provided objects?
- [ ] For LDAP / XML / template engines: is the appropriate library
      escape applied?

## Cryptography

- [ ] Are random values for security purposes from the CSPRNG only?
- [ ] Is symmetric encryption AEAD (AES-GCM, ChaCha20-Poly1305)?
- [ ] Are GCM nonces unique per message and never reused with the
      same key?
- [ ] Are private keys loaded from the secret store, not from source?
- [ ] Is there no custom crypto (hand-rolled hash, XOR "encryption",
      home-grown MAC)?

## Secrets

- [ ] Does this PR contain no hard-coded secrets, tokens, or keys?
- [ ] Are new secrets registered in the secret store with documented
      rotation?
- [ ] Are `.env`, `.env.local`, `*.pem`, `*.key`, and `*.p12` in
      `.gitignore` and absent from the diff?

## Logging

- [ ] Do new log statements avoid passwords, tokens, API keys, full
      government ID numbers, secrets, and private keys?
- [ ] Are PII identifiers masked or hashed where possible?
- [ ] Are log values escaped against CRLF / log-injection?

## Error handling

- [ ] Do user-facing errors omit stack traces, internal paths, and
      query fragments?
- [ ] Is sensitive context captured in the server log (with
      correlation ID) rather than returned to the caller?
- [ ] Are exceptions not silently swallowed?

## Dependencies

- [ ] Are new dependencies pinned (lockfile) and added with a clear
      reason in the PR description?
- [ ] Is the SCA scan passing (Trivy / Snyk / OSV-Scanner)?
- [ ] For internal scopes: is the registry / scope correct to avoid
      dependency confusion?
- [ ] If a transitive dep is at HIGH or CRITICAL, is there a
      documented exception or a follow-up ticket?

## Configuration

- [ ] Are framework security defaults retained
      (`DEBUG=False`, CSRF on for cookie-based apps,
      Spring Security CSRF on, Django security middleware on)?
- [ ] Are `ALLOWED_HOSTS` / host allowlist set to the production
      hostname, not `*`?
- [ ] Are security headers configured (HSTS, X-Content-Type-Options,
      X-Frame-Options or `frame-ancestors`, CSP)?
- [ ] Are CORS allowlists explicit, with `Access-Control-Allow-Origin`
      not set to `*` for credentialed endpoints?

## Threat-model coverage

- [ ] If this PR changes a trust boundary or introduces a new
      external interface, is the threat model updated?
- [ ] If this PR mitigates a STRIDE item, is the requirement ID
      referenced in the description?

## References

- OWASP ASVS: <https://owasp.org/www-project-application-security-verification-standard/>
- OWASP Code Review Guide v2: <https://owasp.org/www-project-code-review-guide/>
- NIST SSDF Practice PW.7 (Review and Analyze Code): <https://csrc.nist.gov/Projects/ssdf>
- OWASP Cheat Sheet Series: <https://cheatsheetseries.owasp.org/>
