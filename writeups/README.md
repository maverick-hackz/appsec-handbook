# Finding Writeups

Sanitized writeups of vulnerability classes, structured for the
template at [template.md](template.md). The intent is to document
the class of bug, its impact, and the remediation pattern -- not to
attribute findings to specific products or organizations.

## Files

- [template.md](template.md) -- shared shape
- [01-jwt-key-confusion-rs256-to-hs256.md](01-jwt-key-confusion-rs256-to-hs256.md)
- [02-ssrf-cloud-metadata-imdsv1.md](02-ssrf-cloud-metadata-imdsv1.md)
- [03-prototype-pollution-merge.md](03-prototype-pollution-merge.md)
- [04-deserialization-jackson-polymorphic.md](04-deserialization-jackson-polymorphic.md)

## Conventions

- Every writeup uses sanitized hostnames (`example.com`,
  `attacker.example`) and synthetic data only.
- CVE numbers cited are verified against the public NVD entry at
  write time; CVSS scores quoted are the NVD-published values.
- Each writeup ends with `## References` linking to canonical
  documentation (OWASP cheat sheets, RFCs, NVD entries, vendor docs).
- Each writeup links to the relevant
  [../secure-coding/](../secure-coding/) section that documents
  the defensive pattern.

## Adding a new writeup

1. Copy [template.md](template.md) to a new file numbered in
   sequence (`05-...md`).
2. Use only verifiable references (NVD, OWASP, RFC, vendor
   advisory). Mark unconfirmed details with
   `<!-- TODO: verify -->`.
3. Cite the secure-coding entry that prevents the class.
4. Submit per [../CONTRIBUTING.md](../CONTRIBUTING.md).
