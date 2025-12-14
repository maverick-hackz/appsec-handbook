# Session Management

## Threat

Predictable, leaky, or non-rotating session identifiers let an attacker
impersonate a user. Sessions that outlive their useful life (and survive
password change, logout, or privilege change) widen the blast radius of a
single credential leak.

CWE: CWE-384 (Session Fixation), CWE-613 (Insufficient Session Expiration),
CWE-330 (Use of Insufficiently Random Values), CWE-352 (CSRF — when session
identifier is ambient-authenticated).

## Insecure

The application accepts a `sessionid` query parameter on first request and
stores it server-side. The cookie has no `Secure`, no `HttpOnly`, no
`SameSite`. There is no rotation on login; the same identifier persists for
30 days.

## Why it fails

- Accepting a session ID from the URL enables session fixation: an attacker
  sends a victim a link with a known ID, then uses it after login.
- Missing `Secure` lets the cookie travel over plaintext; missing `HttpOnly`
  exposes it to XSS; missing `SameSite` enables CSRF on browsers without
  the modern default.
- No rotation means a captured cookie remains valid through password change.

## Secure

- Generate session IDs with a CSPRNG (>= 128 bits of entropy).
- Cookie flags: `Secure`, `HttpOnly`, `SameSite=Lax` (or `Strict` for
  high-sensitivity), `Path=/`, no `Domain` unless cross-subdomain is
  required, sensible `Max-Age` / `Expires`.
- Rotate the session ID on login, MFA challenge, and privilege change.
- Idle timeout (e.g., 15-30 min for sensitive apps) AND absolute timeout
  (e.g., 8-12 hours).
- Invalidate the server-side session record on logout, password change,
  and MFA reset.
- For SPAs talking to APIs over `Authorization: Bearer`, use short-lived
  access tokens (5-15 min) and refresh tokens with rotation and reuse
  detection.
- CSRF protection: SameSite cookies plus a synchronizer token (or
  double-submit cookie) for state-changing requests authenticated by cookie.

## Notes

- Storing session state purely in a signed JWT shifts the revocation problem
  to a deny-list or to making the access token TTL short enough that
  revocation latency is acceptable.
- Bearer tokens in `localStorage` are exposed to XSS; use `HttpOnly` cookies
  or a tightly scoped service worker if you can.
- For machine principals (CI, services), prefer mTLS or short-lived OIDC
  tokens; long-lived bearer tokens are the riskiest pattern.

## References

- OWASP Session Management Cheat Sheet: <https://cheatsheetseries.owasp.org/cheatsheets/Session_Management_Cheat_Sheet.html>
- OWASP CSRF Prevention Cheat Sheet: <https://cheatsheetseries.owasp.org/cheatsheets/Cross-Site_Request_Forgery_Prevention_Cheat_Sheet.html>
- CWE-384: <https://cwe.mitre.org/data/definitions/384.html>
- RFC 6265bis (Cookies): <https://datatracker.ietf.org/doc/html/draft-ietf-httpbis-rfc6265bis>
