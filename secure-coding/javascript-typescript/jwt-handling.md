# JWT Handling

## Threat

JWTs combine three failure modes: developers trust the `alg` header,
the verification function accepts any algorithm, and the same secret
is used for both signing and verifying across symmetric/asymmetric
key types. The combination yields `alg=none` accept-anything bypasses,
HS256/RS256 key-confusion attacks, and signature-stripping forgeries.

CWE: CWE-347 (Improper Verification of Cryptographic Signature),
CWE-321 (Use of Hard-coded Cryptographic Key). OWASP API Top 10:
API2:2023 (Broken Authentication).

## Insecure

```javascript
import jwt from "jsonwebtoken";

// Trusts whatever the token says.
const claims = jwt.verify(token, secret);             // no algorithms pin

// Treats any string as a public-key OR shared-secret.
const claims = jwt.verify(token, publicKey);          // attacker sends HS256, signed with publicKey
```

## Why it fails

- `jsonwebtoken.verify(token, key)` without `algorithms: [...]` accepts
  every algorithm the header advertises. `alg=none` historically
  bypassed verification entirely; library versions vary in coverage.
- When the verifier passes an RSA public key to an HS256 verifier, the
  public key is treated as the shared HMAC secret. An attacker who
  knows the public key (it is public!) forges valid HS256 tokens —
  the "key confusion" attack.

## Secure

```javascript
import jwt from "jsonwebtoken";
import { readFileSync } from "node:fs";

const pubKey = readFileSync("/etc/keys/jwt-pub.pem");

const claims = jwt.verify(token, pubKey, {
    algorithms: ["RS256"],                            // pin one or a closed set
    issuer: "https://issuer.example.com",
    audience: "api.example.com",
    clockTolerance: 30,
    maxAge: "15m",
});
```

For HS256 (shared secret) flows — use a long secret from a vault, not
a string in code:

```javascript
import { createSecretKey } from "node:crypto";

const key = createSecretKey(Buffer.from(process.env.JWT_HS256, "base64"));
const claims = jwt.verify(token, key, { algorithms: ["HS256"] });
```

Stronger posture (recommended for modern apps): use a library that does
not require the caller to pin `algorithms` per call, such as
`jose` with explicit `jwtVerify({ algorithms: [...], typ: "JWT" })`:

```javascript
import { jwtVerify, importSPKI } from "jose";

const key = await importSPKI(pubPem, "RS256");
const { payload } = await jwtVerify(token, key, {
    algorithms: ["RS256"],
    issuer: "https://issuer.example.com",
    audience: "api.example.com",
});
```

If the application needs encryption (confidentiality of claims), use
JWE — JWT alone is signed, not encrypted.

## Notes

- Never use `decode()` to make trust decisions. `decode()` does NOT
  verify the signature.
- Token storage in browsers: `HttpOnly; Secure; SameSite=Lax|Strict`
  cookies; `localStorage` exposes the token to XSS.
- Short-lived access tokens (5-15 minutes) with refresh tokens (rotated,
  with reuse detection) limit the blast radius of a stolen token.
- For multi-tenant systems, validate `iss` / `aud` / `tid` claims AND
  enforce that the principal in the token belongs to the tenant the
  request targets. See [../authorization.md](../authorization.md).
- Revoke compromised keys by rotating signing keys behind a JWKS
  endpoint with `kid`-based selection; pin the trusted JWKS URL and
  cache with a short TTL.
- "alg=none" — recent versions of `jsonwebtoken` reject this by default,
  but explicit `algorithms` pinning is the contract that survives
  library upgrades.

## References

- OWASP JWT Cheat Sheet for Java (applies broadly): <https://cheatsheetseries.owasp.org/cheatsheets/JSON_Web_Token_for_Java_Cheat_Sheet.html>
- RFC 7519 (JWT): <https://datatracker.ietf.org/doc/html/rfc7519>
- RFC 8725 (JWT Best Current Practices): <https://datatracker.ietf.org/doc/html/rfc8725>
- `jose` (Node JWT library): <https://github.com/panva/jose>
- `jsonwebtoken`: <https://github.com/auth0/node-jsonwebtoken>
- CWE-347: <https://cwe.mitre.org/data/definitions/347.html>
