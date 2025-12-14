# Common Pitfalls

## Threat

Patterns that recur across stacks and produce vulnerabilities regardless of
language. Each pitfall maps to a CWE class detailed in its dedicated file.

## Recurring mistakes

| Pitfall | CWE | Detail |
| --- | --- | --- |
| Trust client input | CWE-20 | [input-validation.md](input-validation.md) |
| String concatenation into queries or HTML | CWE-89, CWE-79 | [output-encoding.md](output-encoding.md) |
| Hard-coded credentials in source | CWE-798 | [secrets-handling.md](secrets-handling.md) |
| Weak crypto choices (MD5, RC4, RSA without OAEP) | CWE-327 | [crypto-do-and-dont.md](crypto-do-and-dont.md) |
| Missing authorization checks | CWE-862 | [authorization.md](authorization.md) |
| Verbose error messages and stack traces | CWE-209 | [error-handling-logging.md](error-handling-logging.md) |
| Insecure deserialization of untrusted data | CWE-502 | [deserialization.md](deserialization.md) |
| Session fixation, predictable IDs | CWE-384, CWE-330 | [session-management.md](session-management.md) |
| `Math.random()` / `rand()` for security | CWE-338 | [crypto-do-and-dont.md](crypto-do-and-dont.md) |
| Cleartext storage of credentials | CWE-312 | [secrets-handling.md](secrets-handling.md) |

## Anti-patterns to delete on sight

- `try/except` (or `catch`) that swallows the exception with no log and no rethrow.
- "Custom crypto": hand-rolled hash, XOR "encryption", obscurity for keys.
- `TODO: sanitize later` (or similar) left in shipped code.
- Disabling TLS verification (`verify=False`, `rejectUnauthorized: false`,
  `InsecureSkipVerify: true`) outside test code.
- IP allowlists as the only access control for sensitive endpoints.
- Auth decisions based on `User-Agent`, `Referer`, or `Origin` alone.
- `eval`, `Function()`, `exec`, `pickle.loads`, `ObjectInputStream` on
  attacker-controlled bytes.

## References

- OWASP Top 10 (2021): <https://owasp.org/Top10/>
- CWE Top 25: <https://cwe.mitre.org/top25/>
- OWASP ASVS: <https://owasp.org/www-project-application-security-verification-standard/>
