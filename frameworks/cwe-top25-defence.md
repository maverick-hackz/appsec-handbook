# CWE Top 25 (2025) -- Defence

The MITRE CWE Top 25 ranks the most dangerous and prevalent software
weaknesses based on real-world CVE data. The 2025 edition is the
current release. For each weakness: short description, primary
defence, secondary (defence-in-depth) control, and a link to the
handbook entry where the control is detailed.

## 1. CWE-79 -- Cross-Site Scripting

User-controlled data rendered into an HTML / attribute / URL / JS
context without context-appropriate encoding.

- Primary: context-aware auto-escape in the template engine.
- Secondary: Content-Security-Policy with `script-src 'self' 'nonce-...'`.
- See [../secure-coding/output-encoding.md](../secure-coding/output-encoding.md),
  [../secure-coding/javascript-typescript/xss-react-vue.md](../secure-coding/javascript-typescript/xss-react-vue.md).

## 2. CWE-89 -- SQL Injection

Concatenation of user input into SQL.

- Primary: parameterized queries.
- Secondary: least-privilege DB role; query timeout; SAST rules.
- See [../secure-coding/output-encoding.md](../secure-coding/output-encoding.md)
  and the per-language injection files.

## 3. CWE-352 -- Cross-Site Request Forgery

State-changing request authenticated by ambient credentials (cookie)
without an additional anti-CSRF token.

- Primary: SameSite cookie (Lax / Strict) + CSRF token on state-changing requests.
- Secondary: re-authentication for sensitive actions.
- See [../secure-coding/session-management.md](../secure-coding/session-management.md).

## 4. CWE-862 -- Missing Authorization

No authorization check on a resource access.

- Primary: enforce authorization at the data layer; default-deny.
- Secondary: integration tests assert 403 for cross-tenant / wrong-role.
- See [../secure-coding/authorization.md](../secure-coding/authorization.md).

## 5. CWE-787 -- Out-of-bounds Write

Memory-unsafe operation writes outside an allocated buffer (C / C++).

- Primary: memory-safe language (Rust, Go, managed runtimes).
- Secondary: fuzzing; AddressSanitizer; bounds-checking compile flags.

## 6. CWE-22 -- Path Traversal

User input flows into a filesystem path without anchoring to a base directory.

- Primary: anchor to a base directory; reject `..`; in Go 1.24+, `os.Root`.
- Secondary: container-level read-only filesystem; minimal base image.
- See [../secure-coding/go/path-traversal.md](../secure-coding/go/path-traversal.md).

## 7. CWE-416 -- Use After Free

Memory referenced after free in C / C++.

- Primary: memory-safe language or smart-pointer discipline (RAII).
- Secondary: fuzzing; AddressSanitizer.

## 8. CWE-125 -- Out-of-bounds Read

Read beyond an allocated buffer (C / C++).

- Primary: memory-safe language; bounds-check at parse time.
- Secondary: AddressSanitizer / Valgrind.

## 9. CWE-78 -- OS Command Injection

User input flows into a shell command without separation.

- Primary: argument-array invocation (`subprocess.run([...])`, `exec.Command(...)`).
- Secondary: SAST rule for `os.system` / `shell=True`.
- See [../secure-coding/output-encoding.md](../secure-coding/output-encoding.md).

## 10. CWE-94 -- Code Injection

User input evaluated as code (`eval`, `exec`, `Function`).

- Primary: do not evaluate untrusted strings; use structured parsers.
- Secondary: SAST rule for `eval` / `exec`.
- See [../devsecops/semgrep-rules/python-eval-exec.yml](../devsecops/semgrep-rules/python-eval-exec.yml).

## 11. CWE-120 -- Classic Buffer Overflow

`strcpy`-style copy without size check.

- Primary: memory-safe language or `strncpy_s` / `snprintf`.
- Secondary: `-fstack-protector-strong`; FORTIFY_SOURCE.

## 12. CWE-434 -- Unrestricted File Upload

File upload accepts dangerous types (.php, .jsp) or executes via web
server misconfiguration.

- Primary: allowlist by extension AND content type AND magic-byte sniff.
- Secondary: store uploads outside the web root; serve via a separate
  domain; randomise on-disk filenames.

## 13. CWE-476 -- NULL Pointer Dereference

C / C++ null pointer access.

- Primary: check return values from allocation / lookup; use modern
  language facilities (`Option`, `optional`).
- Secondary: static analysis with null-pointer flow.

## 14. CWE-121 -- Stack-based Buffer Overflow

Overflow on a stack-allocated buffer.

- Primary: memory-safe language; bounds-checked operations.
- Secondary: `-fstack-protector-strong`; canary checks.

## 15. CWE-502 -- Deserialization of Untrusted Data

`pickle.loads`, Java `ObjectInputStream`, Jackson polymorphic on
untrusted bytes.

- Primary: do not deserialize untrusted; use JSON + typed DTO.
- Secondary: allowlist of permitted subtypes if polymorphism is
  required.
- See [../secure-coding/deserialization.md](../secure-coding/deserialization.md),
  [../secure-coding/java/deserialization-jackson.md](../secure-coding/java/deserialization-jackson.md),
  [../secure-coding/python/deserialization-pickle.md](../secure-coding/python/deserialization-pickle.md).

## 16. CWE-122 -- Heap-based Buffer Overflow

Heap-allocated buffer overflow.

- Primary: memory-safe language.
- Secondary: hardened allocator (e.g., scudo); ASan.

## 17. CWE-863 -- Incorrect Authorization

Authorization check present but flawed (wrong attribute checked,
wrong order of comparison).

- Primary: policy-as-code engine (OPA / Cedar) with tests.
- Secondary: integration tests for the privilege matrix.
- See [../secure-coding/authorization.md](../secure-coding/authorization.md).

## 18. CWE-20 -- Improper Input Validation

Untrusted input reaches a sink without validation.

- Primary: schema-validate every untrusted input at the boundary.
- Secondary: per-sink defence (parameterization for SQL, encoding for
  HTML, anchoring for paths).
- See [../secure-coding/input-validation.md](../secure-coding/input-validation.md).

## 19. CWE-284 -- Improper Access Control

Broad category covering missing or flawed access checks.

- Primary: explicit deny-by-default policies; policy engine.
- Secondary: regular access-control review.

## 20. CWE-200 -- Information Exposure to Unauthorized Actor

Sensitive data returned in responses, error pages, debug endpoints,
or logs.

- Primary: response-shape DTOs; redaction in logger.
- Secondary: DAST and SAST on response paths.
- See [../secure-coding/error-handling-logging.md](../secure-coding/error-handling-logging.md).

## 21. CWE-306 -- Missing Authentication for Critical Function

Privileged endpoint exposed without auth.

- Primary: deny by default; explicit `authenticated` per route.
- Secondary: integration test for unauthenticated access on each
  endpoint.

## 22. CWE-918 -- Server-Side Request Forgery

Endpoint fetches user-supplied URLs without restriction.

- Primary: per-host allowlist; reject private / loopback / link-local.
- Secondary: egress network policy.
- See [../secure-coding/go/ssrf-net-http.md](../secure-coding/go/ssrf-net-http.md).

## 23. CWE-77 -- Command Injection (general)

Like CWE-78 but broader (any command interpreter).

- Primary: argument-array invocation.
- Secondary: deny shell entirely when invoking subprocess.

## 24. CWE-639 -- Authorization Bypass Through User-Controlled Key

The key identifying the object comes from the client and the server
uses it without checking ownership.

- Primary: derive the key from the verified principal; never from
  request input alone.
- Secondary: tenant-scoped row-level security in the database.

## 25. CWE-770 -- Allocation of Resources Without Limits

Endpoint consumes unbounded memory / CPU on attacker input.

- Primary: size limits on request body / header count / file size;
  result-size caps; query timeouts.
- Secondary: per-tenant quotas at the gateway.

## Coverage check

For each weakness above:

1. Is there a SAST rule, a code-review checklist item, or a design-
   review question?
2. If yes, is the rule mapped in the team's SAST configuration?
3. If no, is the weakness applicable to the team's stack? (CWE-787
   / CWE-416 / CWE-121 / CWE-122 are unlikely for Go / Python / Java
   web applications, for example.)

## References

- CWE Top 25 (2025): <https://cwe.mitre.org/top25/>
- CWE catalogue: <https://cwe.mitre.org/data/>
- CWE-CAPEC mapping (attack patterns per weakness): <https://capec.mitre.org/>
- OWASP Cheat Sheet Series: <https://cheatsheetseries.owasp.org/>
