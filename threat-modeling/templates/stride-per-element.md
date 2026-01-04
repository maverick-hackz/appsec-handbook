# STRIDE-Per-Element Template

Walk every element of the DFD and apply only the STRIDE letters that
the element type can suffer. Reduces noise versus applying STRIDE-all
to every element.

## Element-to-threat matrix

| Element type | S | T | R | I | D | E |
| --- | --- | --- | --- | --- | --- | --- |
| External entity (user, third party) | yes | - | yes | - | - | - |
| Process (service, function) | yes | yes | yes | yes | yes | yes |
| Data flow (line on the DFD) | - | yes | - | yes | yes | - |
| Data store (DB, queue, cache) | - | yes | yes | yes | yes | - |

Trust boundaries are not elements; they amplify the threats on flows
that cross them.

## Per-element prompts

### External entity (S, R)

- **Spoofing**: how does the system verify this entity's identity?
  Strength, freshness, revocation?
- **Repudiation**: if the entity denies the action, what evidence
  exists? Logs signed? Timestamps from a trusted source?

### Process (full STRIDE)

- **S**: is the process callable by anonymous parties? How is its
  identity verified by callers (mTLS, signed JWT, mutual SPIFFE ID)?
- **T**: can a caller submit input that mutates the process's state
  in unexpected ways (deserialization, prototype pollution, SQLi)?
- **R**: are administrative actions logged with the principal,
  timestamp, action, before/after state?
- **I**: what does the process disclose in errors, logs, side-channels,
  or response timing?
- **D**: rate limits, quotas, expensive operations, recursive parsers,
  unbounded allocation?
- **E**: privilege boundaries inside the process — does an
  authenticated user become an admin via parameter tampering, IDOR,
  or role inflation?

### Data flow (T, I, D)

- **T**: integrity in transit — TLS, signed envelopes, message
  authentication codes?
- **I**: confidentiality in transit — TLS version, cipher policy,
  certificate validation?
- **D**: can the channel be saturated, throttled, or blackholed?

### Data store (T, R, I, D)

- **T**: WORM / append-only requirements? Schema drift detection?
- **R**: audit log retention, immutability (hashing, signing,
  off-host shipping)?
- **I**: encryption at rest (envelope, KEK/DEK), access logging,
  row/column-level controls, KMS audit?
- **D**: backups, replicas, restore drills, quota / disk-pressure
  monitoring?

## Output format

Record each threat with a stable ID. Recommended columns:

| # | Element | Threat | STRIDE | Likelihood | Impact | Mitigation | Status | Owner |
| --- | --- | --- | --- | --- | --- | --- | --- | --- |

Likelihood and impact ratings: a simple Low / Medium / High is enough
for most teams; FAIR-style quantification is overhead for typical SaaS.

## References

- Adam Shostack — Threat Modeling: Designing for Security (Wiley, 2014), Chapter 3
- Microsoft — Threat Modeling Tool threats: <https://learn.microsoft.com/en-us/azure/security/develop/threat-modeling-tool-threats>
- OWASP Threat Modeling Cheat Sheet: <https://cheatsheetseries.owasp.org/cheatsheets/Threat_Modeling_Cheat_Sheet.html>
