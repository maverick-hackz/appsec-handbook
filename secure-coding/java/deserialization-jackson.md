# Polymorphic Deserialization with Jackson

## Threat

Jackson's polymorphic deserialization, when enabled globally or applied
to attacker-controlled JSON, accepts a `@class` (or similar) discriminator
and instantiates that class. Gadget chains on the classpath turn this into
remote code execution. The class of bug is the subject of a long line of
CVEs against Jackson and against applications that misconfigure it.

CWE: CWE-502 (Deserialization of Untrusted Data).

## Insecure

```java
ObjectMapper mapper = new ObjectMapper();
mapper.activateDefaultTyping(
        BasicPolymorphicTypeValidator.builder().build(),
        ObjectMapper.DefaultTyping.NON_FINAL);
Object o = mapper.readValue(request.getBody(), Object.class);
```

Or equivalently, the legacy `enableDefaultTyping()` (deprecated, removed in
recent versions but still found in older code).

## Why it fails

- "DefaultTyping" instructs Jackson to honour a type discriminator
  embedded in JSON and instantiate any class on the classpath.
- A "global" `PolymorphicTypeValidator` that permits a broad base class
  (e.g., `Object`, `Serializable`) is equivalent to no validator.
- Once a gadget class (any class with side effects in a constructor or
  setter) is reachable on the classpath, the parse triggers code.

## Secure

```java
// 1) No default typing. Map JSON into typed DTOs.
record CreateOrder(@NotBlank String sku, @Positive int qty) {}

CreateOrder req = mapper.readValue(json, CreateOrder.class);
```

When polymorphism is required, declare a closed set:

```java
@JsonTypeInfo(use = JsonTypeInfo.Id.NAME, property = "type")
@JsonSubTypes({
    @JsonSubTypes.Type(value = EmailNotification.class, name = "email"),
    @JsonSubTypes.Type(value = SmsNotification.class, name = "sms")
})
sealed interface Notification permits EmailNotification, SmsNotification {}
```

If global polymorphism is mandatory for a legacy contract, use a strict
`PolymorphicTypeValidator` rooted at a sealed base type:

```java
PolymorphicTypeValidator ptv = BasicPolymorphicTypeValidator.builder()
        .allowIfBaseType(Notification.class)
        .build();
```

## Notes

- The application's own DTOs are not the only risk. Jackson modules pulled
  in transitively (e.g., for Spring, Hibernate) can extend the set of
  reachable types.
- Disable autoConfiguration of unsafe modules in Spring Boot.
- Consider `FAIL_ON_UNKNOWN_PROPERTIES = true` to reject unexpected fields
  during integration testing; treat unknown fields as a deserialization
  contract violation.
- For inter-service RPC, prefer schema-typed formats (Protobuf, Avro)
  where polymorphism is opt-in and well-typed.

## References

- OWASP Deserialization Cheat Sheet: <https://cheatsheetseries.owasp.org/cheatsheets/Deserialization_Cheat_Sheet.html>
- Jackson documentation on polymorphic deserialization: <https://github.com/FasterXML/jackson-docs/wiki/JacksonPolymorphicDeserialization>
- CWE-502: <https://cwe.mitre.org/data/definitions/502.html>
- Jackson security advisories: <https://github.com/FasterXML/jackson-databind/security/advisories>
