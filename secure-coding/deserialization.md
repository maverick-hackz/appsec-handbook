# Insecure Deserialization

## Threat

Deserialization of attacker-controlled bytes by a format that allows
arbitrary types or includes deserialization-time side effects yields
remote code execution or DoS. The class of bug spans `pickle`, Java
`ObjectInputStream`, .NET `BinaryFormatter`, PHP `unserialize`, YAML
`load`, and JSON when libraries inject polymorphism by type tag.

CWE: CWE-502 (Deserialization of Untrusted Data). OWASP Top 10:
A08:2021 (Software and Data Integrity Failures).

## Insecure

- Python: `pickle.loads(request.body)`
- YAML: `yaml.load(payload)` (no `SafeLoader`)
- Java: `new ObjectInputStream(stream).readObject()` over an HTTP body
- Jackson: `@JsonTypeInfo(use=Id.CLASS)` + `enableDefaultTyping()`
- PHP: `unserialize($_POST['data'])`

## Why it fails

- These formats encode arbitrary types and graph edges. A gadget chain
  (existing classes with side-effecting methods invoked during
  deserialization) executes during the parse, not after a check.
- "Allowlist by class name" implemented as a string comparison after
  deserialization is too late — side effects ran during parse.

## Secure

- Default: do not deserialize untrusted data. Choose JSON without type
  tags (`{"id": 1, "amount": 12.0}`) and map fields explicitly into a
  typed DTO.
- When you must accept polymorphism: register an explicit allowlist of
  permitted subtypes BEFORE deserialization. Reject unknown types at
  parse time.
- Sign the payload (HMAC or signature) and verify before parsing, OR
  fetch it from an authenticated source — but do not rely on signing
  alone if the signer can be tricked.
- Per language:
  - Python: `json` module; `yaml.safe_load` only.
  - Java: do not use `ObjectInputStream` on network data. With Jackson,
    leave default typing off and use `@JsonTypeInfo` only with
    `@JsonSubTypes` for an explicit closed set.
    See [java/deserialization-jackson.md](java/deserialization-jackson.md).
  - .NET: use `System.Text.Json`, not `BinaryFormatter` (removed/obsolete
    in modern .NET).
  - PHP: avoid `unserialize` on user input; prefer JSON.
- For internal trusted RPC, prefer schema-defined formats (Protobuf,
  Avro, MessagePack with strict schemas) where polymorphism is opt-in
  and well-typed.

## Notes

- "Signed pickle" used as a session format has been a recurring CVE
  source (e.g., Flask-Session-style patterns). Even with a valid HMAC,
  if the signing key leaks, RCE follows.
- Deserialization gadgets sometimes hide in transitive deps; a clean
  classpath review is part of the SCA process. See [../devsecops/supply-chain/README.md](../devsecops/supply-chain/README.md).

## References

- OWASP Deserialization Cheat Sheet: <https://cheatsheetseries.owasp.org/cheatsheets/Deserialization_Cheat_Sheet.html>
- CWE-502: <https://cwe.mitre.org/data/definitions/502.html>
- OWASP Top 10 A08:2021: <https://owasp.org/Top10/A08_2021-Software_and_Data_Integrity_Failures/>
