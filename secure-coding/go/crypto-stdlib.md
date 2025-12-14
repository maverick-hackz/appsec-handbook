# Cryptography in Go: stdlib + `x/crypto`

## Threat

`math/rand` is fast but predictable. `crypto/cipher` packages expose
both safe (AEAD) and unsafe (raw ECB-equivalent block APIs) modes. The
stdlib does not ship a password hashing KDF — Argon2id comes from
`golang.org/x/crypto/argon2`.

CWE: CWE-327, CWE-326, CWE-328, CWE-338, CWE-916.

## Insecure

```go
import "math/rand"

token := fmt.Sprintf("%x", rand.Int63())         // predictable

// Plain block cipher — no mode, no auth tag
block, _ := aes.NewCipher(key)
ciphertext := make([]byte, len(plaintext))
block.Encrypt(ciphertext, plaintext)             // ECB equivalent
```

## Why it fails

- `math/rand` is seeded from a known source unless explicitly reseeded
  with `crypto/rand`. Even when reseeded, the algorithm is not designed
  for unpredictability under adversarial conditions.
- `cipher.Block.Encrypt` operates on a single block; using it in a loop
  without a mode is ECB. ECB leaks structure.

## Secure

CSPRNG everywhere randomness matters:

```go
import "crypto/rand"

token := make([]byte, 32)
if _, err := rand.Read(token); err != nil {
    return err
}

// crypto/rand.Int for bounded values.
n, err := rand.Int(rand.Reader, big.NewInt(1000))
```

Symmetric AEAD (AES-256-GCM):

```go
import (
    "crypto/aes"
    "crypto/cipher"
    "crypto/rand"
)

block, err := aes.NewCipher(key32)              // 32 bytes -> AES-256
if err != nil { return err }
aead, err := cipher.NewGCM(block)
if err != nil { return err }

nonce := make([]byte, aead.NonceSize())          // 12 bytes
if _, err := rand.Read(nonce); err != nil { return err }

ciphertext := aead.Seal(nil, nonce, plaintext, associatedData)
// Ship: nonce || ciphertext   (nonce is not secret; never reuse with same key)

// Decrypt
plain, err := aead.Open(nil, nonce, ciphertext, associatedData)
```

ChaCha20-Poly1305 alternative (`crypto/cipher.NewChaCha20Poly1305` in
recent Go releases; otherwise via `golang.org/x/crypto/chacha20poly1305`).

Password hashing with Argon2id:

```go
import "golang.org/x/crypto/argon2"

salt := make([]byte, 16)
if _, err := rand.Read(salt); err != nil { return nil, err }

hash := argon2.IDKey(
    []byte(password),
    salt,
    3,             // time cost
    64*1024,       // 64 MiB memory cost
    4,             // parallelism
    32,            // hash length in bytes
)
// Encode salt + parameters alongside the hash so verify can reproduce them.
```
<!-- TODO: verify Argon2id parameter targets against measured timing and RFC 9106 §4 -->

Signing — Ed25519 from the standard library:

```go
import "crypto/ed25519"

pub, priv, err := ed25519.GenerateKey(rand.Reader)
sig := ed25519.Sign(priv, message)
ok := ed25519.Verify(pub, message, sig)
```

Constant-time comparison for MACs and tokens:

```go
import "crypto/subtle"

if subtle.ConstantTimeCompare(expected, got) != 1 {
    return errAuthFailed
}
```

## Notes

- `crypto/rand.Read` is the unique source of cryptographic randomness;
  every `nonce`, salt, key, and bearer token comes from it.
- Never reuse a GCM nonce with the same key. Generate per message; if
  message rates per key are very high, rotate the key.
- For TLS configuration, set `tls.Config.MinVersion = tls.VersionTLS12`
  at minimum; `tls.VersionTLS13` for new deployments. Set `InsecureSkipVerify`
  only in test code that you can detect at build time.
- `bcrypt` (`golang.org/x/crypto/bcrypt`) is acceptable for legacy
  compatibility; Argon2id is the modern default.

## References

- Go `crypto/rand`: <https://pkg.go.dev/crypto/rand>
- Go `crypto/cipher`: <https://pkg.go.dev/crypto/cipher>
- Go `crypto/ed25519`: <https://pkg.go.dev/crypto/ed25519>
- `golang.org/x/crypto/argon2`: <https://pkg.go.dev/golang.org/x/crypto/argon2>
- OWASP Cryptographic Storage Cheat Sheet: <https://cheatsheetseries.owasp.org/cheatsheets/Cryptographic_Storage_Cheat_Sheet.html>
- RFC 9106 (Argon2): <https://datatracker.ietf.org/doc/html/rfc9106>
- NIST SP 800-38D (GCM): <https://csrc.nist.gov/publications/detail/sp/800-38d/final>
