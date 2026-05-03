# Finding: `<Title>`

## Summary

`<1-2 sentences describing what the issue is and where it manifests.>`

## Severity

- CVSS 3.1 vector: `CVSS:3.1/AV:.../AC:.../PR:.../UI:.../S:.../C:.../I:.../A:...`
- Base score: `<X.X>` (`<Critical | High | Medium | Low>`)
- CWE: `CWE-XXX -- <description>`

## Affected component

`<Stack, library, version range, and the configuration that triggers
the issue. Be specific: language, framework, library name with
versions.>`

## Reproduction

Sanitized steps. Never include real targets, customer data, or
unredacted tokens.

```text
1. <step>
2. <step>
3. <step>
```

Expected vs observed:

- Expected: `<what should happen>`
- Observed: `<what actually happens>`

## Root cause

`<Technical explanation: which code path runs, which library function
is invoked, which configuration value flips the behaviour, which
assumption is broken.>`

## Impact

`<Concrete consequences: data exposed, privilege gained, scope of
affected users, regulatory implications if relevant.>`

## Remediation

1. **Short-term (workaround / mitigation)**: `<deploy now>`
2. **Long-term (fix in code / config)**: `<correct fix; reference the
   secure-coding entry in this handbook.>`

## Detection

- SAST signature: `<rule ID or pattern>`
- SCA detection: `<package + version range>`
- DAST signature: `<active or passive check name>`
- Runtime / log signal: `<event pattern>`

## References

- CVE: `CVE-XXXX-XXXXX` (link to NVD)
- OWASP Cheat Sheet: `<title and URL>`
- Original advisory: `<URL>`
- Related secure-coding entry: `<../secure-coding/...>`
