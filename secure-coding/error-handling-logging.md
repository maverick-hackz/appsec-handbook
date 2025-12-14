# Error Handling and Logging

## Threat

Two opposing failures: errors that reveal too much to the caller (stack
traces, internal paths, SQL fragments) and logs that record too much for
internal viewers (secrets, tokens, PII).

CWE: CWE-209 (Information Exposure Through an Error Message), CWE-532
(Insertion of Sensitive Information into Log File), CWE-117 (Improper
Output Neutralization for Logs).

## Insecure

An unhandled exception bubbles up; the framework renders a debug page with
source snippets and environment variables. Elsewhere, the login handler
logs `INFO logged in user=%s password=%s` to ship to the central log
aggregator.

## Why it fails

- Stack traces leak library versions (vulnerability scoping), query
  structure (SQLi shaping), and filesystem layout.
- Verbose errors help an attacker iterate. "Invalid username" vs "wrong
  password" is a username oracle.
- Secrets and PII in logs broaden the blast radius of any log-aggregator
  compromise and complicate GDPR / data-residency obligations.

## Secure

- User-facing: a generic message and a correlation ID. Surface no internal
  details. Wire `application/problem+json` (RFC 7807) responses with stable
  `type` URIs.
- Server-side: structured logs (JSON) with a fixed schema. Include the
  correlation ID, principal ID, action, outcome, and an error class.
- Never log: passwords, tokens (session, JWT, OAuth), API keys, full
  government ID numbers, secrets, private keys, or full request/response
  bodies of authenticated endpoints.
- Mask or hash identifiers used for correlation that contain PII (email
  hashed with a salt, last 4 of phone).
- Log-injection: log frameworks must serialize user input as a value, not
  template it into the format string. Disable CRLF in the format pipeline,
  or strip control characters at write time.
- Centralize logs to a tamper-resistant store; restrict read access by role
  and purpose.

## Notes

- Stack traces are useful — for the engineer, not the user. Capture them in
  the log; do not return them to the caller.
- Alert on log-volume anomalies; high-cardinality `ERROR` floods often map
  to abuse or exploit attempts.

## References

- OWASP Error Handling Cheat Sheet: <https://cheatsheetseries.owasp.org/cheatsheets/Error_Handling_Cheat_Sheet.html>
- OWASP Logging Cheat Sheet: <https://cheatsheetseries.owasp.org/cheatsheets/Logging_Cheat_Sheet.html>
- CWE-209: <https://cwe.mitre.org/data/definitions/209.html>
- CWE-532: <https://cwe.mitre.org/data/definitions/532.html>
- RFC 7807 (Problem Details for HTTP APIs): <https://datatracker.ietf.org/doc/html/rfc7807>
