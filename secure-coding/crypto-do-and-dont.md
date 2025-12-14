# Cryptography: Do and Don't

## Threat

Choosing a weak primitive or misusing a strong one. The standard library and
common third-party libraries make safe choices easy and unsafe choices subtle;
this table is the short version. See per-language files for working code.

CWE: CWE-327 (Use of a Broken or Risky Cryptographic Algorithm),
CWE-326 (Inadequate Encryption Strength), CWE-328 (Use of Weak Hash),
CWE-338 (Use of Cryptographically Weak PRNG).

## Do / Don't

| Use case | Use | Avoid |
| --- | --- | --- |
| Password hashing | Argon2id > scrypt > bcrypt > PBKDF2-HMAC-SHA256 with high iteration count | PBKDF2-SHA1 with low iterations; MD5/SHA-1/SHA-256/SHA-512 without a KDF |
| Symmetric encryption | AES-256-GCM, ChaCha20-Poly1305 | AES-ECB, AES-CBC without HMAC-then-decrypt (encrypt-then-MAC), DES, 3DES, RC4 |
| Asymmetric signing | Ed25519, ECDSA P-256, RSA-PSS (RSA-2048 or larger) | RSA-1024, DSA, RSA with PKCS#1 v1.5 padding for new signatures |
| Asymmetric encryption | RSA-OAEP (SHA-256), or hybrid KEM (X25519 + AEAD) | RSA with PKCS#1 v1.5 encryption padding, ElGamal |
| Key agreement | X25519, ECDH (P-256 or larger) | Static DH with small groups, anonymous DH |
| Hashing for integrity | SHA-256, SHA-512, SHA-3, BLAKE2/3 | MD5, SHA-1 (collisions are practical) |
| MAC | HMAC-SHA-256 (or larger), KMAC | CBC-MAC over variable-length input, custom MACs |
| TLS | TLS 1.3; TLS 1.2 minimum during migration | TLS 1.0, TLS 1.1, SSLv3, NULL-cipher suites, EXPORT suites |
| Random for security | OS CSPRNG: `secrets` (Python), `crypto/rand` (Go), `java.security.SecureRandom`, `crypto.randomBytes` (Node) | `Math.random()`, `rand()`, `srand(time(0))`, `java.util.Random` |

## Notes

- Argon2id parameter recommendations vary by deployment; RFC 9106 §4 documents
  the framework for choosing memory cost, time cost, and parallelism.
  <!-- TODO: verify Argon2id default parameters against RFC 9106 §4 for the next pass -->
- Always use AEAD (GCM, ChaCha20-Poly1305) for new symmetric protocols.
  Encrypt-then-MAC is acceptable only when the construction is well-reviewed.
- Never reuse a nonce/IV under the same key with GCM. Generate per message
  from a CSPRNG (96-bit / 12-byte) or use a deterministic counter scheme that
  is provably unique.
- "Custom crypto" includes encoding sensitive data in JWT and trusting it
  blind: JWT is authenticated, not encrypted — use JWE if you need both.

## References

- OWASP Cryptographic Storage Cheat Sheet: <https://cheatsheetseries.owasp.org/cheatsheets/Cryptographic_Storage_Cheat_Sheet.html>
- OWASP Password Storage Cheat Sheet: <https://cheatsheetseries.owasp.org/cheatsheets/Password_Storage_Cheat_Sheet.html>
- OWASP Transport Layer Security Cheat Sheet: <https://cheatsheetseries.owasp.org/cheatsheets/Transport_Layer_Security_Cheat_Sheet.html>
- NIST SP 800-131A Rev 2 (transitions): <https://csrc.nist.gov/publications/detail/sp/800-131a/rev-2/final>
- NIST SP 800-63B (passwords and MFA): <https://pages.nist.gov/800-63-3/sp800-63b.html>
- RFC 9106 (Argon2): <https://datatracker.ietf.org/doc/html/rfc9106>
- RFC 8446 (TLS 1.3): <https://datatracker.ietf.org/doc/html/rfc8446>
