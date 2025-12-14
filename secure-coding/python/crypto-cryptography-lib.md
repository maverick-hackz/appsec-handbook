# Cryptography in Python: `cryptography`, `secrets`, `argon2-cffi`

## Threat

The Python standard library exposes both safe (`secrets`, `hashlib.scrypt`)
and unsafe (`random.random` for security, `hashlib.md5` for passwords)
primitives behind similar names. The third-party `cryptography` library
provides a vetted high-level API; `pycrypto` and `pycryptodomex` are not
covered here.

CWE: CWE-327, CWE-326, CWE-328, CWE-338, CWE-916.

## Insecure

```python
import random, hashlib
token = "%032x" % random.getrandbits(128)             # MT, not CSPRNG
password_hash = hashlib.sha256(password.encode()).hexdigest()

from Crypto.Cipher import AES                         # ECB defaults vary
c = AES.new(key, AES.MODE_ECB)
```

## Why it fails

- `random` is a Mersenne Twister; given a few outputs the state is
  recoverable.
- A single SHA-256 over a password runs in microseconds; offline cracking
  is trivial.
- AES-ECB encrypts identical plaintext blocks to identical ciphertext —
  see the canonical penguin image.

## Secure

Randomness for tokens, IDs, salts, IVs:

```python
import secrets

token = secrets.token_urlsafe(32)         # URL-safe base64
api_key = secrets.token_hex(32)
nonce_12 = secrets.token_bytes(12)        # for GCM/ChaCha20-Poly1305
```

Password hashing with Argon2id (`argon2-cffi`):

```python
from argon2 import PasswordHasher
from argon2.exceptions import VerifyMismatchError

ph = PasswordHasher(
    time_cost=3,
    memory_cost=64 * 1024,                # 64 MiB
    parallelism=4,
    hash_len=32,
    salt_len=16,
)
stored = ph.hash(password)                # encodes params; portable string

try:
    ph.verify(stored, submitted)
    if ph.check_needs_rehash(stored):
        stored = ph.hash(submitted)       # bump params on next login
except VerifyMismatchError:
    raise AuthFailure()
```
<!-- TODO: verify Argon2 parameter targets against the deployment's measured timing and RFC 9106 §4 guidance -->

Symmetric AEAD with the `cryptography` package:

```python
from cryptography.hazmat.primitives.ciphers.aead import AESGCM

key = AESGCM.generate_key(bit_length=256)
aesgcm = AESGCM(key)
nonce = secrets.token_bytes(12)
aad = b"order-id:42"
ct = aesgcm.encrypt(nonce, plaintext, aad)            # auth tag appended
pt = aesgcm.decrypt(nonce, ct, aad)
```

For files / messages where simplicity matters and key management is
local, `cryptography.fernet.Fernet` provides AES-128-CBC + HMAC-SHA-256
with versioned tokens.

Asymmetric:

```python
from cryptography.hazmat.primitives.asymmetric.ed25519 import (
    Ed25519PrivateKey, Ed25519PublicKey,
)

sk = Ed25519PrivateKey.generate()
sig = sk.sign(b"message")
sk.public_key().verify(sig, b"message")
```

```python
from cryptography.hazmat.primitives.asymmetric import rsa, padding
from cryptography.hazmat.primitives import hashes

priv = rsa.generate_private_key(public_exponent=65537, key_size=2048)
ct = priv.public_key().encrypt(
    plaintext,
    padding.OAEP(
        mgf=padding.MGF1(algorithm=hashes.SHA256()),
        algorithm=hashes.SHA256(),
        label=None,
    ),
)
```

## Notes

- `secrets.compare_digest` for constant-time comparison of MACs and
  tokens.
- Never reuse a GCM nonce with the same key. 12-byte CSPRNG nonces are
  the simplest path; counter-based nonces are acceptable if uniqueness
  is provable.
- For envelope encryption with cloud KMS, only the data encryption key
  (DEK) is in process memory; the key-encryption-key (KEK) stays inside
  the KMS / HSM.
- `cryptography.hazmat.*` carries a "hazardous" prefix as a signal: the
  API is low-level. Prefer `Fernet` / `AESGCM` over `Cipher(AES(...))`
  unless you specifically need the lower layer.

## References

- OWASP Cryptographic Storage Cheat Sheet: <https://cheatsheetseries.owasp.org/cheatsheets/Cryptographic_Storage_Cheat_Sheet.html>
- OWASP Password Storage Cheat Sheet: <https://cheatsheetseries.owasp.org/cheatsheets/Password_Storage_Cheat_Sheet.html>
- `cryptography` documentation: <https://cryptography.io/en/latest/>
- `secrets` module documentation: <https://docs.python.org/3/library/secrets.html>
- `argon2-cffi` documentation: <https://argon2-cffi.readthedocs.io/en/stable/>
- RFC 9106 (Argon2): <https://datatracker.ietf.org/doc/html/rfc9106>
