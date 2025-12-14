# Input Validation

## Threat

Untrusted input flowing into security-sensitive sinks: queries, paths, command
arguments, deserialization, template rendering, redirects. Validation alone
does not prevent injection; output encoding and parameterized APIs are
mandatory complements at the sink.

CWE: CWE-20 (Improper Input Validation), CWE-1284 (Improper Validation of
Specified Quantity in Input).

## Insecure

A request parameter `country` flows directly into a JDBC query, a filesystem
path, and an HTML response with no length, type, charset, or canonical-form
check.

## Why it fails

- Blacklists miss cases. Unicode normalization, percent-encoding, and case
  variants expand the rule set to where every implementation has gaps.
- Validation at the entry point alone leaves internal sinks unprotected when
  data is later combined with other untrusted inputs.
- Client-side validation is UX, not security; an attacker bypasses it
  trivially with a manual request.

## Secure

- Validate at the trust boundary AND use safe APIs at the sink (parameterized
  queries, base-directory-anchored paths, template auto-escape).
- Define an allowlist per field: type, length, character class, semantic
  range. Reject everything else.
- Canonicalize before validating (decode percent-encoding, Unicode NFC/NFKC)
  so the check reasons about the actual bytes the sink will receive.
- Use strict schemas: JSON Schema, OpenAPI, Pydantic, struct tags. Reject
  extra/unknown fields by default.
- Enforce size limits early — request body, header count, JSON depth, list
  length, file size.

## Notes

- Validation is necessary, not sufficient. Pair with the sink-specific
  control: see [output-encoding.md](output-encoding.md),
  [go/path-traversal.md](go/path-traversal.md),
  [deserialization.md](deserialization.md).
- Use the language's native parser to reject malformed input instead of
  regex-guessing structure (e.g., JSON, XML, URI, email).

## References

- OWASP Input Validation Cheat Sheet: <https://cheatsheetseries.owasp.org/cheatsheets/Input_Validation_Cheat_Sheet.html>
- OWASP ASVS V5 (Validation, Sanitization, Encoding): <https://owasp.org/www-project-application-security-verification-standard/>
- CWE-20: <https://cwe.mitre.org/data/definitions/20.html>
