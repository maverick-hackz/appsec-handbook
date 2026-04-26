# Tooling Evaluation

Evaluation methodology for AppSec scanners and posture-management
platforms. The goal is to make a decision from evidence (test corpus
results, integration trials) rather than from a vendor pitch.

## Files

- [sast-evaluation-methodology.md](sast-evaluation-methodology.md) -- SAST: precision / recall on a real corpus
- [sca-evaluation-methodology.md](sca-evaluation-methodology.md) -- SCA: vuln DB sources, transitive resolution, reachability
- [dast-evaluation-methodology.md](dast-evaluation-methodology.md) -- DAST: coverage, auth, API testing
- [mast-evaluation-methodology.md](mast-evaluation-methodology.md) -- MAST: static + dynamic; MASVS alignment
- [aspm-comparison-criteria.md](aspm-comparison-criteria.md) -- ASPM aggregation / prioritization platforms
- [benchmark-projects.md](benchmark-projects.md) -- public deliberately-vulnerable corpora for testing tools
- [proof-of-concept-template.md](proof-of-concept-template.md) -- vendor PoC report structure

## Cross-cutting principles

- **Test on YOUR code, not on demo apps.** Vendor demos are tuned
  to make a specific tool look good. A representative sample of the
  team's actual code is the only valid corpus.
- **Measure precision AND recall.** A tool with 90% precision and
  10% recall (low noise but misses things) is very different from
  one with 30% precision and 80% recall (catches a lot, but
  swamps the team).
- **Time-to-triage matters as much as accuracy.** A finding that
  takes 30 minutes to confirm cancels the value of a tool that
  caught it.
- **Operational fit:** SSO, RBAC, ticket integration, on-prem
  option, residency requirements -- these decide whether the tool
  is operable in your environment, regardless of how good its
  engine is.
- **Total cost of ownership beats list price.** Include the cost of
  triage, false-positive suppression, and the engineering time to
  integrate.

## Evaluation flow

```text
1. Define gap to close       (see ../devsecops/tool-categories.md)
2. Shortlist 2-3 tools       (cover commercial + OSS where applicable)
3. Define test corpus        (your code + public benchmarks)
4. Define scoring matrix     (precision, recall, integration, cost)
5. Run a time-boxed PoC      (2-4 weeks per tool, parallel where possible)
6. Score; document; decide
7. Roll out gradually        (one team / one repo first)
```

The same flow applies to SAST, SCA, DAST, MAST, and ASPM, with the
metrics adjusted per category in the per-class files.
