# Go Secure Coding

Go 1.21+ secure coding patterns. Each file follows the standard template
(Threat, Insecure, Why it fails, Secure, Notes, References).

## Files

- [SQL injection with `database/sql`](injection-sql-database-sql.md) — parameterization
- [Path traversal](path-traversal.md) — `filepath.Clean`, base-directory anchoring, `os.Root` (1.24+)
- [SSRF in `net/http`](ssrf-net-http.md) — outbound HTTP from user URLs
- [Cryptography: stdlib + `x/crypto`](crypto-stdlib.md) — `crypto/rand`, `crypto/cipher`, `x/crypto`
- [Concurrency pitfalls](concurrency-pitfalls.md) — races, TOCTOU, leaks

## Conventions

- Targeting Go 1.21+. Where a feature is newer (e.g., `os.Root` in 1.24,
  `crypto/ecdh` shape), the version is called out inline.
- Standard library is preferred. `golang.org/x/crypto` is used where the
  stdlib lacks the primitive (Argon2, NaCl box, bcrypt).
- Mark uncertain version-specific behaviour with
  `<!-- TODO: verify against <package> v<version> docs -->`.
