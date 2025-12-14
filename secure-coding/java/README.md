# Java Secure Coding

JDK 17+ secure coding patterns. Each file follows the standard template
(Threat, Insecure, Why it fails, Secure, Notes, References).

## Files

- [injection-sql-jdbc.md](injection-sql-jdbc.md) — SQL injection via JDBC and JPA
- [deserialization-jackson.md](deserialization-jackson.md) — polymorphic deserialization
- [xxe-jaxb.md](xxe-jaxb.md) — XML external entity in JAXB / DocumentBuilder / SAX
- [crypto-jca.md](crypto-jca.md) — JCA / JCE: AES-GCM, SecureRandom, password hashing
- [spring-security-defaults.md](spring-security-defaults.md) — Spring Security 6 baseline

## Conventions

- All examples target JDK 17+ and use modern Java idioms (records,
  switch expressions, `var` where it clarifies).
- Spring examples target Spring Boot 3.x / Spring Security 6.x.
- Vendor docs are the primary source; specific library versions are
  cited in each file. Mark uncertain version-specific behaviour with
  `<!-- TODO: verify against <library> v<version> docs -->`.
