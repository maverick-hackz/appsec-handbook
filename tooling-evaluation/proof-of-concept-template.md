<!-- markdownlint-disable MD025 -->
# Proof-of-Concept Report Template

A standard structure for documenting a vendor PoC so the decision
makers can compare apples to apples.

---

# PoC Report: `<Tool Name>` -- `<Category, e.g., SAST>`

## Executive summary

`<2-3 sentences: what was tested, by whom, over what period, and the
recommendation.>`

Recommendation: `<Adopt | Adopt with conditions | Reject>`.

## Objectives

What gap was this PoC trying to close? Cite the
[../devsecops/tool-categories.md](../devsecops/tool-categories.md)
gap that motivated the evaluation.

`<TODO: state the gap>`

## Success criteria

The PoC was successful if all of the following held at the end of
the window:

1. `<concrete, measurable criterion>`
2. `<...>`

These criteria were set BEFORE the PoC began. They are not
adjusted after seeing results.

## Test corpus

| Source | Description | Used to measure |
| --- | --- | --- |
| `<repo / service>` | Representative of the team's stack | Precision, recall, integration |
| `<public benchmark>` | OWASP Benchmark / SARD / Juliet | Standardised comparison |
| `<past-CVE branch>` | Internal CVE fix on a specific commit | Tool's ability to catch known issues |

## Scoring matrix

| Criterion | Weight | Score (1-5) | Evidence |
| --- | --- | --- | --- |
| `<Criterion 1>` | `<%>` | `<n>` | `<one-line evidence>` |
| `<Criterion 2>` | `<%>` | `<n>` | `<...>` |
| ... | ... | ... | ... |
| **Weighted total** | 100% | `<n.n>` | -- |

Weights and criteria come from the relevant methodology file in this
section (SAST / SCA / DAST / MAST / ASPM).

## Findings

### Quantitative

| Metric | Result |
| --- | --- |
| Precision on own corpus | `<TP / total findings>` |
| Recall on benchmark | `<TP / known vulns>` |
| Scan time (representative repo) | `<minutes>` |
| Time to first finding in PR | `<seconds>` |
| Time to triage one finding (median) | `<minutes>` |
| False-positive rate on clean corpus | `<%>` |

### Qualitative

`<3-5 bullets: what was good, what was painful, what surprised you.>`

## Integration evidence

- CI integration: `<screenshot or YAML snippet>`
- PR annotation behaviour: `<example>`
- SARIF / report consumption: `<works / partial / no>`
- IDE plugin: `<works / partial / no>`
- SSO / RBAC: `<configured / partial / blocked>`

## Operational fit

| Concern | Verdict | Note |
| --- | --- | --- |
| Deployment (SaaS / self-host / air-gapped) | `<fit / partial / no>` | |
| Data residency | `<fit / partial / no>` | |
| Pricing model alignment | `<fit / partial / no>` | |
| Vendor security posture (SOC 2, pentest, DPA) | `<satisfactory / partial / no>` | |

## Risks

- `<concrete risk: lock-in, single-vendor dependency, EOL of feature, ...>`
- `<...>`

## Cost

| Item | Cost | Notes |
| --- | --- | --- |
| License (3-year total) | `<$>` | |
| Operational overhead (engineer days per quarter) | `<n>` | |
| Migration / integration effort (one-time) | `<n engineer days>` | |
| **Total 3-year TCO** | `<$>` | |

Compare to the next-best alternative's TCO; the gap should be
justified by the differential value.

## Recommendation

`<Adopt | Adopt with conditions | Reject>`.

Conditions (if any):

- `<concrete condition that must be met before rollout>`
- `<...>`

## Roll-out plan (if adopting)

1. Week 1-2: integrate into one repo / one team; baseline existing
   findings.
2. Week 3-4: triage baseline; tune suppression rules.
3. Month 2: expand to N repos; introduce in CI as advisory.
4. Month 3: turn on CI gating at HIGH+; communicate ahead.
5. Quarterly: review metrics (escape rate, MTTR).

## Off-boarding plan (if adopted)

Documented from day 1: how do we leave this vendor if it does not
work out?

- Data export: `<format, retention>`
- Replacement candidates: `<two alternatives>`
- Migration cost estimate: `<n engineer weeks>`

---

## How to use this template

- Fill out a copy per vendor under evaluation; keep the version that
  goes into the decision packet in the team's wiki / records.
- For internal compliance (SAMM Governance / Strategy & Metrics),
  the report is the evidence that the choice was made on data.
- Refresh the methodology file (SAST / SCA / ...) when criteria
  evolve; archive the template instance with the criteria it was
  scored against.
