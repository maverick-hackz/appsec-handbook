# Crypto Cheat Sheet

Architecture-level crypto choices: which primitive for which scenario,
with recommended parameters. The line-of-code companion is
[../secure-coding/crypto-do-and-dont.md](../secure-coding/crypto-do-and-dont.md).

## Symmetric encryption

| Scenario | Algorithm | Parameters |
| --- | --- | --- |
| Authenticated symmetric encryption at rest | AES-256-GCM | 256-bit key; 96-bit nonce from CSPRNG; 128-bit tag |
| Authenticated symmetric encryption in transit | ChaCha20-Poly1305 OR AES-256-GCM | as above |
| Disk encryption (block-mode) | AES-XTS-256 | 512-bit composite key; per-sector tweak |
| Streaming AEAD over chunks | ChaCha20-Poly1305 with chunk-counter nonce | per-chunk nonce derivation |

Avoid: AES-ECB, AES-CBC without Encrypt-then-MAC, CBC-MAC over
variable-length input, RC4, 3DES.

## Asymmetric

| Scenario | Algorithm | Parameters |
| --- | --- | --- |
| Digital signature (new system) | Ed25519 | 256-bit key |
| Digital signature (compatibility) | ECDSA P-256 or RSA-PSS | P-256 with SHA-256; RSA-2048+ with MGF1-SHA-256 |
| Public-key encryption (RSA) | RSA-OAEP-SHA-256 | RSA-2048+ |
| Hybrid encryption (KEM-DEM) | X25519 + AES-256-GCM | per-message X25519 ephemeral key |
| Key agreement | X25519 or ECDH P-256 | ephemeral keys (forward secrecy) |

Avoid: RSA <2048 bits, RSA with PKCS#1 v1.5 padding for new
signatures, RSA encryption padding PKCS#1 v1.5, DSA.

## Hashing and MAC

| Scenario | Algorithm | Parameters |
| --- | --- | --- |
| Cryptographic hash | SHA-256, SHA-512, SHA-3 family, BLAKE2/3 | -- |
| MAC | HMAC-SHA-256 (or larger), KMAC, Poly1305 (within ChaCha20-Poly1305) | -- |
| Password hashing | Argon2id | m=64 MiB, t=3, p=4 minimum; tune for ~250 ms per attempt |
| Password hashing (compat) | scrypt OR bcrypt OR PBKDF2-HMAC-SHA-256 | scrypt N=2^15, r=8, p=1; bcrypt cost 12; PBKDF2 600k iterations |

Avoid: MD5, SHA-1 (collisions practical), SHA-2 alone for password
storage.

## Key management

| Decision | Recommendation |
| --- | --- |
| Long-lived signing keys | HSM (FIPS 140-2/3 Level 2 or higher) |
| KMS for symmetric data keys (envelope encryption) | Cloud KMS (AWS KMS, GCP KMS, Azure Key Vault) or Vault transit engine |
| Per-tenant KMS keys (BYOK / HYOK) | Required for regulated data; one CMK per tenant |
| Key rotation cadence | KEK: annually or on incident; DEK: per write or per epoch |
| Key access audit | Every encrypt / decrypt logged to a tamper-resistant store |

## Randomness

| Use | API |
| --- | --- |
| Tokens, salts, nonces, IDs | Python: `secrets`; Go: `crypto/rand`; Java: `java.security.SecureRandom`; Node: `crypto.randomBytes` |
| UUIDs (sortable, time-based) | UUIDv7 from a CSPRNG implementation |
| Non-security shuffles, simulations | `random` / `Math.random` (not for tokens) |

Avoid for security: `Math.random()`, C `rand()`, `srand(time(0))`,
`java.util.Random` (LCG, predictable).

## TLS configuration

| Mode | Version |
| --- | --- |
| Recommended (new) | TLS 1.3 only |
| Compatibility (legacy clients) | TLS 1.2 minimum + TLS 1.3 |
| Forbidden | TLS 1.0, TLS 1.1, SSLv3 |

Cipher suite policy: Mozilla "Modern" for TLS 1.3-only deployments;
Mozilla "Intermediate" for 1.2 + 1.3.

Forbidden suites: any NULL cipher, RC4, 3DES, EXPORT, anonymous DH.

Mandatory: HSTS with `max-age >= 31536000; includeSubDomains;
preload`; OCSP stapling.

## Constant-time operations

For comparing tokens, signatures, MACs, or any secret-derived
value, use constant-time compare:

- Python: `hmac.compare_digest`
- Go: `crypto/subtle.ConstantTimeCompare`
- Java: `MessageDigest.isEqual`
- Node: `crypto.timingSafeEqual`

Plain `==` / `equals` / `bytes.Equal` is short-circuit and leaks
length / prefix via timing.

## Post-quantum readiness

Quantum-resistant primitives are progressing through NIST PQC
standardisation. Today's posture:

- Continue using ECDSA / Ed25519 / RSA for signatures.
- For long-lived secrets (encryption at rest, KEKs), watch the NIST
  PQC final selection and plan a hybrid migration (classical +
  PQ-KEM in parallel) when the standard ships.
- For TLS, hybrid key exchange (X25519 + ML-KEM) is appearing in
  browsers and servers; enable when both sides support it.

## What is OUT of scope here

- Cryptographic protocol design (TLS, Noise, MLS). Use vetted
  libraries; do not write protocols.
- Hardware random number generation internals.
- Constant-time implementations of higher-level operations (those
  belong in the library, not in application code).

## References

- NIST SP 800-131A Rev 2 (algorithm transitions): <https://csrc.nist.gov/publications/detail/sp/800-131a/rev-2/final>
- NIST SP 800-57 (key management): <https://csrc.nist.gov/projects/key-management/key-management-guidelines>
- NIST SP 800-63B (passwords): <https://pages.nist.gov/800-63-3/sp800-63b.html>
- NIST SP 800-38D (GCM): <https://csrc.nist.gov/publications/detail/sp/800-38d/final>
- RFC 8446 (TLS 1.3): <https://datatracker.ietf.org/doc/html/rfc8446>
- RFC 9106 (Argon2): <https://datatracker.ietf.org/doc/html/rfc9106>
- Mozilla TLS profiles: <https://wiki.mozilla.org/Security/Server_Side_TLS>
- OWASP Cryptographic Storage Cheat Sheet: <https://cheatsheetseries.owasp.org/cheatsheets/Cryptographic_Storage_Cheat_Sheet.html>
- NIST PQC standardisation: <https://csrc.nist.gov/projects/post-quantum-cryptography>
