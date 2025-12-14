# Output Encoding

## Threat

Untrusted data is rendered into a context (HTML, attribute, URL, JavaScript,
CSS, shell, SQL, LDAP) without context-appropriate encoding. Each sink has
its own grammar; an encoding that is safe in one context is unsafe in another.

CWE: CWE-79 (XSS), CWE-89 (SQLi), CWE-78 (OS Command Injection), CWE-90
(LDAP Injection), CWE-91 (XML Injection), CWE-94 (Code Injection).

## Insecure

String concatenation into a sink:

```text
"<div>" + user + "</div>"                  // XSS
"SELECT * FROM users WHERE id=" + id       // SQLi
"sh -c 'ls " + dir + "'"                   // Command injection
"(&(uid=" + username + ")(pwd=" + pw + "))" // LDAPi
```

## Why it fails

- Concatenation drops the distinction between data and code; the sink parses
  the combined string as a program.
- Generic HTML-escape utilities do not protect attribute, URL, or JavaScript
  contexts; each context needs its own rules.
- "Sanitization" by removing characters depends on knowing every dangerous
  variant for every sink — fragile.

## Secure

- HTML body / attribute: templating engines with context-aware auto-escape
  (Jinja2 `autoescape=True`, Go `html/template`, React JSX, Thymeleaf).
- SQL: parameterized queries (`?` / `$1`). Never `String.format`, f-strings,
  or `+`. See [java/injection-sql-jdbc.md](java/injection-sql-jdbc.md),
  [python/injection-sql-orm.md](python/injection-sql-orm.md),
  [go/injection-sql-database-sql.md](go/injection-sql-database-sql.md).
- Shell: pass arguments as a list/array to `subprocess.run` / `exec.Command`.
  Never pass a string to a shell unless it is a trusted literal.
- URL: percent-encode user data (`encodeURIComponent`, `urllib.parse.quote`,
  `java.net.URLEncoder`).
- JSON: build with the library's serializer; never `'{"k":"' + v + '"}'`.
- LDAP: escape per RFC 4515 with the library's `escape` helper, or use a
  parameterized search API.

## Notes

- Auto-escape is not magic: it knows the surrounding context only via the
  engine's native interpolation. Manual `raw` / `safe` / `dangerouslySetInnerHTML`
  bypasses it. See [javascript-typescript/xss-react-vue.md](javascript-typescript/xss-react-vue.md).
- Encoding is sink-specific. `HtmlEncode(...)` does not make a string safe to
  paste into a JavaScript string literal or a URL parameter.

## References

- OWASP XSS Prevention Cheat Sheet: <https://cheatsheetseries.owasp.org/cheatsheets/Cross_Site_Scripting_Prevention_Cheat_Sheet.html>
- OWASP Injection Prevention Cheat Sheet: <https://cheatsheetseries.owasp.org/cheatsheets/Injection_Prevention_Cheat_Sheet.html>
- CWE-79: <https://cwe.mitre.org/data/definitions/79.html>
- CWE-89: <https://cwe.mitre.org/data/definitions/89.html>
