# Authentication

## Threat

Weak or missing proof of identity allows account takeover, credential
stuffing, password spraying, and session impersonation. Authentication is
distinct from authorization (what the principal can do); both must be
enforced.

CWE: CWE-287 (Improper Authentication), CWE-307 (Improper Restriction of
Excessive Authentication Attempts), CWE-521 (Weak Password Requirements),
CWE-798 (Use of Hard-coded Credentials).

## Insecure

Login compares the plaintext password from the request against an MD5
column. No rate limit, no lockout, no MFA. Reset link is a sequential
integer; password change does not invalidate other sessions.

## Why it fails

- MD5 (or any fast hash) lets an attacker test billions of passwords per
  second per GPU against a leaked database.
- No rate limiting on login enables credential stuffing; no lockout enables
  per-account brute force.
- Predictable reset tokens are brute-forceable; non-invalidated sessions
  let a compromised credential stay valid after rotation.

## Secure

- Hash passwords with a KDF: Argon2id (preferred), scrypt, bcrypt, or
  PBKDF2-HMAC-SHA-256 with NIST-recommended iteration counts. See
  [crypto-do-and-dont.md](crypto-do-and-dont.md).
- Enforce a length minimum (NIST SP 800-63B §5.1.1.2 recommends >= 8) and
  block known-breached passwords (e.g., Have I Been Pwned password range API).
- Rate-limit by username AND by IP/ASN. Use an exponential delay or a
  CAPTCHA after N failures; permanent lockout enables a denial of service.
- Offer MFA: TOTP (RFC 6238) or WebAuthn (FIDO2). For privileged accounts,
  enforce phishing-resistant MFA (WebAuthn).
- Reset / verify tokens: at least 128-bit entropy from a CSPRNG, short TTL
  (15-60 min), single-use, bound to the account.
- On password change or MFA reset: invalidate other sessions and refresh
  tokens.
- Hide whether an account exists in error messages and timing.

## Notes

- Password rotation policies that force changes on a fixed schedule
  decrease security; NIST SP 800-63B §5.1.1.2 advises against them.
- "Security questions" are usually weaker than the password itself.
- For machine-to-machine auth, prefer mTLS or short-lived OIDC tokens over
  long-lived API keys. See [architecture/mtls-patterns.md](../architecture/mtls-patterns.md)
  and [architecture/oauth2-oidc-flows.md](../architecture/oauth2-oidc-flows.md).

## References

- OWASP Authentication Cheat Sheet: <https://cheatsheetseries.owasp.org/cheatsheets/Authentication_Cheat_Sheet.html>
- OWASP Password Storage Cheat Sheet: <https://cheatsheetseries.owasp.org/cheatsheets/Password_Storage_Cheat_Sheet.html>
- NIST SP 800-63B (Authenticator and Verifier Requirements): <https://pages.nist.gov/800-63-3/sp800-63b.html>
- CWE-287: <https://cwe.mitre.org/data/definitions/287.html>
- RFC 6238 (TOTP): <https://datatracker.ietf.org/doc/html/rfc6238>
- W3C WebAuthn: <https://www.w3.org/TR/webauthn-2/>
