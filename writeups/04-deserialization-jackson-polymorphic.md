# Finding: Polymorphic Deserialization in Jackson (CVE-2017-7525 class)

## Summary

A Java service uses Jackson's polymorphic deserialization
(`enableDefaultTyping`, or `@JsonTypeInfo` with a base type set to
`Object` / `Serializable`) to parse a JSON payload from a network
peer. The JSON includes a type discriminator that names a class
present on the classpath; Jackson constructs that class. A "gadget"
class -- one whose constructor / setter performs a side-effecting
operation -- triggers code execution during the parse. The result is
remote code execution from a single HTTP request.

## Severity

- CVSS 3.1 vector: `CVSS:3.1/AV:N/AC:L/PR:N/UI:N/S:U/C:H/I:H/A:H`
- Base score: 9.8 (Critical)
- CWE: CWE-502 -- Deserialization of Untrusted Data

Reference vulnerability: CVE-2017-7525
(`jackson-databind` before 2.6.7.1 / 2.7.9.1 / 2.8.9). A long line of
follow-on CVEs (CVE-2017-15095, CVE-2017-17485, CVE-2018-5968, etc.)
patched specific gadgets one at a time before the broader
`PolymorphicTypeValidator` API was introduced. New gadgets continue
to surface against permissive configurations.

## Affected component

Java services that:

- Use `jackson-databind` to parse untrusted JSON.
- Have called `enableDefaultTyping()` or `activateDefaultTyping()`
  with a permissive validator.
- Have declared `@JsonTypeInfo(use = Id.CLASS)` on a base type that
  is broader than a closed, sealed set of subtypes.
- Have a gadget class on the classpath -- any class with side
  effects in a constructor, setter, or factory method invoked during
  deserialization. Common transitive dependencies (Spring,
  Hibernate, Apache Commons Collections) have historically supplied
  gadgets.

Versions before the patched line for CVE-2017-7525 are directly
vulnerable; versions with a permissive `PolymorphicTypeValidator` are
indirectly vulnerable.

## Reproduction

```text
Setup
  - Spring Boot service with jackson-databind <= 2.8.8 (or later
    with default typing globally enabled).
  - Controller accepts application/json and deserializes into
    Object: @PostMapping String handle(@RequestBody Object body).
  - Classpath includes a known gadget (e.g., older Apache
    commons-collections or Logback).

Steps
  1. Send POST /api/event with:
     {
       "@class": "com.example.GadgetClass",
       "command": ["sh","-c","id > /tmp/pwn"]
     }
     The class name targets a known gadget that runs a Runtime.exec
     or equivalent during construction.
  2. Server's ObjectMapper reads `@class`, instantiates the gadget,
     and invokes the side-effecting setter.
  3. The command runs inside the service's process.

Observed
  - File /tmp/pwn created with output of id (proves code execution).
  - No authentication required if the endpoint is unauthenticated.
```

## Root cause

`jackson-databind`'s default typing instructs the parser to honour a
type discriminator embedded in the JSON and instantiate that type
from the classpath. The construction sequence triggers any
side-effecting code in the constructor or in setters invoked during
deserialization. Even when the application's own DTOs are not
dangerous, transitively included libraries can supply a gadget.

The semantic flaw is that the security boundary lives inside the
parser (which classes are permitted), not at the application's
public interface.

## Impact

- Remote code execution in the service process, with whatever
  privileges that process has.
- Lateral movement: credentials in memory, mounted secrets,
  surrounding service identities.
- Persistence via shell on the host or a malicious in-memory hook.
- The classpath can change with any dependency update, so a
  previously safe application becomes vulnerable when a new gadget
  ships.

## Remediation

1. **Short-term (workaround)**:
   - Upgrade `jackson-databind` to the latest patched line.
     2.10+ defaults to a stricter `PolymorphicTypeValidator`.
   - Disable default typing if it was opted in:
     `mapper.deactivateDefaultTyping();` (or remove
     `enableDefaultTyping` calls).
   - Remove unused libraries from the classpath; a smaller
     classpath has fewer gadgets.

2. **Long-term (fix)**:
   - Do not deserialize untrusted data with polymorphic typing.
     Map JSON into typed DTOs explicitly.
   - If polymorphism is genuinely required, declare a closed set of
     subtypes with `@JsonSubTypes` on a sealed base type, and use a
     strict `PolymorphicTypeValidator` rooted at that type.
   - See [../secure-coding/java/deserialization-jackson.md](../secure-coding/java/deserialization-jackson.md).

## Detection

- SAST: flag any use of `enableDefaultTyping`,
  `activateDefaultTyping`, and broad `@JsonTypeInfo(use = Id.CLASS)`
  base types.
- SCA: alert on `jackson-databind` versions vulnerable to the
  Jackson polymorphic-deserialization CVE chain (CVE-2017-7525 and
  follow-ons).
- DAST: probe JSON endpoints with malformed type discriminators and
  watch for class-not-found / instantiation-error behaviour that
  signals polymorphic deserialization paths.
- Runtime: instrument `ObjectMapper.readValue` and log the actual
  resolved type per call; alert on unexpected resolutions.

## References

- CVE-2017-7525: <https://nvd.nist.gov/vuln/detail/CVE-2017-7525>
- CWE-502: <https://cwe.mitre.org/data/definitions/502.html>
- jackson-databind security advisories: <https://github.com/FasterXML/jackson-databind/security/advisories>
- OWASP Deserialization Cheat Sheet: <https://cheatsheetseries.owasp.org/cheatsheets/Deserialization_Cheat_Sheet.html>
- Moritz Bechler -- "Java Unmarshaller Security" (2017): <https://github.com/mbechler/marshalsec>
- `../secure-coding/java/deserialization-jackson.md`
- `../secure-coding/deserialization.md`
