# Secure Coding

Language-specific secure coding guidelines. Every entry follows the same
template: Threat, Insecure example, Why it fails, Secure example, Notes,
References.

## Cross-cutting

- [Common pitfalls](common-pitfalls.md) — recurring mistakes across stacks
- [Input validation](input-validation.md)
- [Output encoding](output-encoding.md)
- [Cryptography: do and don't](crypto-do-and-dont.md)
- [Authentication](authentication.md)
- [Authorization](authorization.md)
- [Session management](session-management.md)
- [Error handling and logging](error-handling-logging.md)
- [Secrets handling](secrets-handling.md)
- [Insecure deserialization](deserialization.md)

## Per language

- [Java](java/) — JDK 17+
- [Python](python/) — Python 3.11+
- [Go](go/) — Go 1.21+
- [JavaScript and TypeScript](javascript-typescript/) — Node 20+

## File template

See the [contributing guide](../CONTRIBUTING.md) for the file template and
PR validation checklist.
