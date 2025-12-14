# Cryptography with JCA / JCE

## Threat

JCA exposes both safe and unsafe primitives behind the same `Cipher` /
`MessageDigest` API. Names like `AES`, `DES`, `RSA` accept transformation
strings that silently default to insecure modes (`AES` alone = ECB on
some providers).

CWE: CWE-327 (Use of a Broken or Risky Cryptographic Algorithm),
CWE-326 (Inadequate Encryption Strength), CWE-338 (Use of Cryptographically
Weak PRNG), CWE-916 (Use of Password Hash With Insufficient Computational
Effort).

## Insecure

```java
Cipher c = Cipher.getInstance("AES");                 // ECB by default
c.init(Cipher.ENCRYPT_MODE, key);

MessageDigest md = MessageDigest.getInstance("MD5");  // broken
md.update(password.getBytes());

Random r = new Random();                              // not for crypto
byte[] iv = new byte[16];
r.nextBytes(iv);
```

## Why it fails

- `AES` with no mode resolves to `AES/ECB/PKCS5Padding` on many providers.
  ECB leaks plaintext structure across blocks.
- MD5 / SHA-1 are collision-broken; SHA-256 alone over a password is
  too fast (no work factor, no salt).
- `java.util.Random` is a linear congruential generator. Predictable
  from a handful of outputs.

## Secure

Symmetric AEAD (AES-256-GCM):

```java
SecureRandom rng = new SecureRandom();
byte[] iv = new byte[12]; // 96-bit nonce for GCM
rng.nextBytes(iv);

SecretKey key = new SecretKeySpec(keyBytes32, "AES"); // 256-bit key
Cipher c = Cipher.getInstance("AES/GCM/NoPadding");
c.init(Cipher.ENCRYPT_MODE, key, new GCMParameterSpec(128, iv));
c.updateAAD(associatedData);  // bind metadata to the ciphertext
byte[] ciphertext = c.doFinal(plaintext);
// Ship: iv || ciphertext  (iv is not secret; do not reuse with same key)
```

CSPRNG everywhere security depends on randomness:

```java
SecureRandom rng = new SecureRandom();
byte[] token = new byte[32];
rng.nextBytes(token);
```

Password hashing (Argon2id via Spring Security 6 `Argon2PasswordEncoder`):

```java
PasswordEncoder enc = new Argon2PasswordEncoder(
        16,     // saltLength bytes
        32,     // hashLength bytes
        1,      // parallelism
        65536,  // memory KiB
        3);     // iterations
String hash = enc.encode(password);
boolean ok = enc.matches(submitted, hash);
```

`Argon2PasswordEncoder` requires Bouncy Castle (`bcprov-jdk18on`) on the
classpath in current Spring Security versions.
<!-- TODO: verify Argon2PasswordEncoder parameter defaults and Bouncy Castle requirement against Spring Security current GA docs -->

RSA-OAEP for asymmetric encryption when hybrid encryption is overkill:

```java
Cipher c = Cipher.getInstance("RSA/ECB/OAEPWithSHA-256AndMGF1Padding");
c.init(Cipher.ENCRYPT_MODE, rsaPublicKey,
        new OAEPParameterSpec("SHA-256", "MGF1",
                MGF1ParameterSpec.SHA256, PSource.PSpecified.DEFAULT));
```

## Notes

- Never reuse a GCM IV under the same key. Generate per message; for very
  high message rates per key, rotate keys before IV exhaustion.
- For signing prefer Ed25519 (JDK 15+) or ECDSA P-256 / RSA-PSS over
  PKCS#1 v1.5 signatures.
- Constant-time compare for tokens: `MessageDigest.isEqual(a, b)`.
- Avoid `String.getBytes()` for sensitive material; it uses platform
  default charset. Specify `StandardCharsets.UTF_8`.
- Long-lived keys belong in an HSM or cloud KMS; do not load them from
  the filesystem in production.

## References

- OWASP Cryptographic Storage Cheat Sheet: <https://cheatsheetseries.owasp.org/cheatsheets/Cryptographic_Storage_Cheat_Sheet.html>
- OWASP Password Storage Cheat Sheet: <https://cheatsheetseries.owasp.org/cheatsheets/Password_Storage_Cheat_Sheet.html>
- Java Cryptography Architecture (Oracle): <https://docs.oracle.com/en/java/javase/17/security/java-cryptography-architecture-jca-reference-guide.html>
- RFC 9106 (Argon2): <https://datatracker.ietf.org/doc/html/rfc9106>
- NIST SP 800-38D (GCM): <https://csrc.nist.gov/publications/detail/sp/800-38d/final>
