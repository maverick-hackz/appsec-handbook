# Finding: JWT Key Confusion (RS256 -> HS256)

## Summary

A JWT-verifying endpoint accepts the algorithm declared in the
token header without pinning it to the algorithm the issuer uses.
An attacker substitutes `alg: HS256` for the expected `alg: RS256`
and signs the forged token using the issuer's public key as the HMAC
secret. The verifier accepts the forged token as authentic.

## Severity

- CVSS 3.1 vector: `CVSS:3.1/AV:N/AC:L/PR:N/UI:N/S:U/C:H/I:H/A:H`
- Base score: 9.8 (Critical)
- CWE: CWE-347 -- Improper Verification of Cryptographic Signature

Score reflects the canonical scenario where the forged JWT grants
arbitrary identity to an unauthenticated remote attacker. The
historical reference vulnerability in the `jsonwebtoken` Node.js
library was published as CVE-2015-9235 with the same CVSS profile.

## Affected component

Any JWT verifier that:

- Does not pass an `algorithms: [...]` allowlist to the verify
  function (or its language equivalent).
- Selects the verification key by `alg` rather than by `kid` against
  a trusted JWKS.
- Loads an RSA public key as a generic "secret" and forwards it to a
  verifier that derives the algorithm from the token header.

Historical examples (now patched; remain in legacy code):

- `jsonwebtoken` (Node) < 4.2.2 -- CVE-2015-9235.
- `jwt-simple` (Node) <= 0.3.0 -- CVE-2016-10555.
- Multiple libraries across PyJWT, ruby-jwt, java-jwt have had
  variants of the same issue in older versions.

## Reproduction

```text
Setup
  - The server expects RS256-signed JWTs and verifies with a public
    key it fetches from a JWKS or hard-codes locally.
  - The server calls jwt.verify(token, key) without `algorithms`.

Steps
  1. Capture a valid JWT issued to a low-privilege account.
  2. Recover the issuer's RSA public key (public by definition;
     usually exposed at /.well-known/jwks.json).
  3. Construct a new header: { "alg": "HS256", "typ": "JWT" }.
  4. Construct a new payload elevating role: { ..., "role": "admin" }.
  5. Compute HMAC-SHA256 over `base64url(header).base64url(payload)`
     using the public key bytes as the HMAC secret.
  6. Submit base64url(header).base64url(payload).base64url(mac).

Observed
  - The server verifies the token successfully and grants admin
    access.
```

## Root cause

The verify function selects the algorithm from the token header
(attacker-controlled) rather than the verifier's policy. When the
caller passes "the public key" as a generic key parameter and the
header says HS256, the HMAC verifier treats those bytes as a shared
secret and recomputes the MAC over the attacker-supplied content. The
public key is, by design, public; the attacker computes a valid MAC.

The semantic mismatch is at the API boundary: the verify function
needs the algorithm pinned independently of the token's header.

## Impact

- Forgery of any identity claims (`sub`, `role`, `tenant_id`).
- Bypass of every downstream authorization check that trusts the
  claims (BFLA / BOLA become trivial once any identity can be forged).
- Persistence for the validity window of the forged token, repeatable
  while the public key remains in service.

## Remediation

1. **Short-term (workaround)**: pin the verify call to a closed
   algorithm set. Refuse `alg=none` and any HS\* algorithm when the
   issuer is asymmetric:

   ```javascript
   jwt.verify(token, publicKey, { algorithms: ["RS256"] });
   ```

   ```python
   jwt.decode(token, public_key, algorithms=["RS256"])
   ```

2. **Long-term (fix)**: use a library that does not accept algorithm
   from the token header for trust decisions
   (e.g., `jose` in Node, `python-jose`), and pin the algorithm at
   the verify boundary. See
   [../secure-coding/javascript-typescript/jwt-handling.md](../secure-coding/javascript-typescript/jwt-handling.md).

   Move to JWKS with `kid`-based key selection over a trusted issuer
   URL; verify `iss`, `aud`, `exp`, `iat`, `nbf` on every call.

## Detection

- SAST signature: any call to `jwt.verify` or `jwt.decode` without an
  `algorithms` (or equivalent) argument. The custom rule
  [hardcoded-jwt-secret](../devsecops/semgrep-rules/hardcoded-jwt-secret.yml)
  detects the related "hardcoded JWT secret" pattern; algorithm
  pinning lints belong in a Semgrep rule keyed on the verify call.
- DAST: send a token with `alg=none` and a token with `alg=HS256`
  signed by the public key; flag if either is accepted.
- Runtime: log every verify decision with the asserted algorithm;
  alert on receipt of an HS\* token in a service that issues RS\*.

## References

- CVE-2015-9235 (`jsonwebtoken`): <https://nvd.nist.gov/vuln/detail/CVE-2015-9235>
- CVE-2016-10555 (`jwt-simple`): <https://nvd.nist.gov/vuln/detail/CVE-2016-10555>
- RFC 7519 (JSON Web Token): <https://datatracker.ietf.org/doc/html/rfc7519>
- RFC 8725 (JWT Best Current Practices): <https://datatracker.ietf.org/doc/html/rfc8725>
- OWASP JWT for Java Cheat Sheet: <https://cheatsheetseries.owasp.org/cheatsheets/JSON_Web_Token_for_Java_Cheat_Sheet.html>
- `../secure-coding/javascript-typescript/jwt-handling.md`
