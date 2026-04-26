# ASPM Comparison Criteria

Application Security Posture Management (ASPM) platforms aggregate
findings across SAST, SCA, DAST, IaC scanners, runtime tools, and
ticketing systems. They dedupe, prioritize, and route to engineering.

The category overlaps with Vulnerability Management (CVE-centric) and
DevSecOps platforms (CI-centric). For new programs, an ASPM is the
natural single pane of glass; for established programs, the question
is "do we need a platform, or a custom workflow that the team owns?".

## Criteria

| Criterion | What to measure | How |
| --- | --- | --- |
| Connector coverage | SAST / SCA / DAST tools your team uses + the cloud + ticketing | Check matrix |
| Asset inventory | Repositories / services / images / cloud resources | Try ingest |
| Deduplication | Same vuln from 3 scanners -> one issue | Test with overlapping scanners |
| Prioritization | EPSS / KEV / reachability / business context | Inspect ranking |
| Ticket integration | Jira / GitHub Issues / Linear; bi-directional sync | Try |
| Workflow customisation | Per-team SLA, severity adjustment, ownership rules | Try |
| Triage UX | One-click suppression with justification; bulk actions | Hands-on |
| Metrics | Mean time to fix, fix rate, escape rate, coverage | Inspect dashboards |
| Compliance reporting | OWASP Top 10 / ASVS / SAMM / SSDF rollup | Inspect |
| SBOM ingest | CycloneDX / SPDX; continuous CVE matching against archived SBOMs | Try |
| Reachability / runtime signal | Confirms which findings actually run | Inspect feature |
| SSO / RBAC | SAML / OIDC; team hierarchy | Configure |
| Audit log | Every triage decision logged with actor and timestamp | Inspect |
| Deployment | SaaS / self-host / hybrid | Confirm fit |
| Data residency | Per-region storage if regulatory | Confirm |

## Test corpus

- One repository wired through SAST + SCA + secret scan.
- One service wired through DAST.
- One cloud account wired through CSPM.
- Run for 1-2 weeks; measure dedup quality (how many issues that
  should be one are one).

## Prioritization signals

A good ASPM consumes multiple signals into a single ranking:

- **Severity** (CVSS) -- the score the CVE was issued with.
- **EPSS** -- predicted exploitation probability.
- **KEV** -- present in CISA's Known Exploited Vulnerabilities.
- **Reachability** -- the vulnerable code is actually called.
- **Asset context** -- internet-facing? Holds regulated data?
- **Business context** -- tier 0 critical infrastructure vs tier 3
  internal tool.

Tools that surface only CVSS are 2010 technology. Modern signals
make the priority list 10x smaller.

## Ticket routing

- Per-team ownership rules (CODEOWNERS-equivalent).
- Auto-create tickets at HIGH+ severity with team context (sprint,
  on-call, escalation path).
- Auto-close on PR merge that closes the issue.
- Bi-directional sync so engineering comments on Jira are visible
  in ASPM.

## Common pitfalls

- Buying ASPM before having scanners that produce useful findings.
  The platform's value is dedup + routing; if the inputs are noisy,
  the output is noisy.
- Treating ASPM as a scanner. It is an aggregator; the underlying
  scanners produce findings.
- Choosing on the UI demo. The UI matters less than the connectors,
  dedup quality, and SLA workflow over a 6-month run.

## Build vs buy

A custom workflow (DefectDojo + scripts + dashboards) covers 60-70%
of ASPM for a small program and stays in the team's control. Commercial
ASPM justifies its cost when:

- Scanners > 6 different vendors.
- Cross-team SLA tracking is a board-reported metric.
- Compliance reporting against multiple frameworks is required.
- Dedicated AppSec team has the capacity for it.

For early-stage programs, DefectDojo (open-source) is a sensible
default.

## Scoring matrix

| Criterion | Weight | Tool A | Tool B (OSS / DefectDojo) |
| --- | --- | --- | --- |
| Connector coverage | 20% | 5 (40+ connectors) | 3 (community connectors) |
| Deduplication | 15% | 4 | 3 |
| Prioritization (EPSS / KEV / reachability) | 15% | 5 | 2 (CVSS only OOTB) |
| Ticket integration | 10% | 5 (bi-directional Jira) | 3 |
| Metrics / reporting | 10% | 5 | 3 |
| Operational deployment (self-host) | 5% | 3 (SaaS-only) | 5 |
| Triage UX | 10% | 5 | 3 |
| Customisation | 5% | 4 | 5 (full open-source) |
| TCO (license + ops) | 10% | 2 | 5 |
| Weighted total | -- | 4.2 | 3.4 |

## References

- OWASP DefectDojo: <https://www.defectdojo.org/>
- OWASP Dependency-Track: <https://dependencytrack.org/>
- Gartner / Forrester ASPM market scans (vendor-specific landscape)
- OWASP Software Assurance Maturity Model (SAMM) v2 -- maturity track this platform supports: <https://owaspsamm.org/>
