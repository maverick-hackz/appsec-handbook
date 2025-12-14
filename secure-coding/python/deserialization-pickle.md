# Pickle, yaml.load, and Other Unsafe Deserializers

## Threat

`pickle`, `marshal`, and `yaml.load` without `SafeLoader` instantiate
arbitrary Python objects from the input byte stream. Constructing an
object that calls `os.system` (or any side-effecting callable) is the
canonical RCE pattern.

CWE: CWE-502 (Deserialization of Untrusted Data).

## Insecure

```python
import pickle
state = pickle.loads(request.body)              # arbitrary code execution

import yaml
cfg = yaml.load(open("config.yml"))             # !!python/object/...

import shelve
db = shelve.open("cache.db")                    # pickle under the hood
```

A minimal pickle gadget:

```python
class Exploit:
    def __reduce__(self):
        return (os.system, ("id",))

payload = pickle.dumps(Exploit())
pickle.loads(payload)   # runs `id` during loads
```

## Why it fails

- `pickle.loads` invokes `__reduce__` / `__setstate__` and constructs
  arbitrary classes named in the byte stream. The decision to run code
  is part of the format, not a misuse.
- `yaml.load` honours `!!python/object/...` tags by default and resolves
  to constructor calls.

## Secure

```python
# JSON for data: typed mapping into a dataclass / pydantic model
import json
from pydantic import BaseModel

class Order(BaseModel):
    sku: str
    qty: int

order = Order.model_validate_json(request.body)

# YAML for config: safe_load only
import yaml
cfg = yaml.safe_load(open("config.yml"))

# When stuck with pickle for trusted internal data:
#  - HMAC the bytes with a server-side key BEFORE writing
#  - Verify HMAC BEFORE pickle.loads
#  - Treat the HMAC key as a high-value secret (rotation, vault)
import hmac, hashlib
def verify(payload: bytes, mac: bytes, key: bytes) -> bool:
    expected = hmac.new(key, payload, hashlib.sha256).digest()
    return hmac.compare_digest(expected, mac)
```

For inter-service messaging, prefer a schema-typed format:
Protobuf, Avro, MessagePack with a strict schema, or JSON with a typed
parser (Pydantic, attrs + cattrs, msgspec).

## Notes

- `dill`, `cloudpickle`, `joblib.load`, `numpy.load(allow_pickle=True)`,
  `pandas.read_pickle` — all delegate to pickle.
- `tensorflow.keras.models.load_model` (HDF5 path) historically
  deserialized custom layers via pickle; verify with the current
  TensorFlow docs before relying on it for untrusted models.
  <!-- TODO: verify TensorFlow model loading behaviour against current docs -->
- `shelve`, `dbm` files round-trip through pickle and inherit the risk.
- "Signed pickle" inside an HMAC envelope is acceptable only when the
  key is treated as a top-tier secret and rotation is automated; even
  then, a key compromise still grants RCE.

## References

- OWASP Deserialization Cheat Sheet: <https://cheatsheetseries.owasp.org/cheatsheets/Deserialization_Cheat_Sheet.html>
- Python `pickle` module documentation (security warning): <https://docs.python.org/3/library/pickle.html>
- PyYAML — `yaml.safe_load`: <https://pyyaml.org/wiki/PyYAMLDocumentation>
- CWE-502: <https://cwe.mitre.org/data/definitions/502.html>
