# Java Secure Coding

JDK 17+ secure coding patterns. Each file follows the standard template
(Threat, Insecure, Why it fails, Secure, Notes, References).

## Files

- [SQL injection via JDBC and JPA](injection-sql-jdbc.md)
- [Polymorphic deserialization with Jackson](deserialization-jackson.md)
- [XXE in JAXB / DocumentBuilder / SAX](xxe-jaxb.md)
- [Cryptography with JCA / JCE](crypto-jca.md) — AES-GCM, SecureRandom, password hashing
- [Spring Security 6 defaults](spring-security-defaults.md) — Spring Security 6 baseline

## Conventions

- All examples target JDK 17+ and use modern Java idioms (records,
  switch expressions, `var` where it clarifies).
- Spring examples target Spring Boot 3.x / Spring Security 6.x.
- Vendor docs are the primary source; specific library versions are
  cited in each file. Mark uncertain version-specific behaviour with
  `<!-- TODO: verify against <library> v<version> docs -->`.
