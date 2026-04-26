# SAST Evaluation Methodology

A practical procedure to compare SAST tools without trusting the
vendor's benchmark.

## Criteria

| Criterion | What to measure | How |
| --- | --- | --- |
| Precision | True positives / total findings | Manual review of a sampled batch of findings |
| Recall (sensitivity) | Known vulns flagged / known vulns present | Run against a corpus where the truth is known |
| Language support | Languages your stack uses, including DSLs (Terraform, IaC) | Try each |
| CWE coverage | Which CWEs the rule set actually addresses | Catalogue per tool |
| IDE integration | LSP / IntelliJ / VS Code plugin; PR annotation | Hands-on |
| CI integration | SARIF output; PR comment / status-check posting | Hands-on |
| Custom rule authoring | Pattern, taint, dataflow; documentation; testability | Write a small rule per tool |
| Suppression / baselining | Per-line, per-rule, baseline files; reviewable | Try suppressing 5 representative findings |
| False-positive triage UX | One-click "not a real issue" with justification | Time the workflow |
| SSO / RBAC | SAML / OIDC; team / role hierarchy | Configure |
| Compliance reporting | OWASP Top 10 / ASVS / CWE Top 25 dashboards | Inspect |
| Deployment options | SaaS, self-host, air-gapped | Confirm fit with operational policy |
| Performance | Scan time on the project | Time it |
| Pricing model | Per developer, per LOC, per repo | Get a quote; estimate at 3-year horizon |

## Test corpus

| Corpus | Purpose |
| --- | --- |
| Your own code (representative service) | Real-world precision + integration |
| OWASP Benchmark (Java) | Standardised precision / recall reporting (Java) |
| NIST SARD (multilang) | Curated true-positive samples |
| Juliet Test Suite (C/C++, Java, C#) | NIST-curated CWE-tagged samples |
| WebGoat (Java) / NodeGoat / RailsGoat / Damn Vulnerable GraphQL App | End-to-end vulnerabilities for triage workflow |
| Past CVE corpus (your own) | Tool's ability to catch issues you already know about |

See [benchmark-projects.md](benchmark-projects.md) for the full set
with URLs.

## Scoring matrix

Score each criterion 1-5 with one evidence line. Weight by importance
to the organization; sum.

Example (truncated):

| Criterion | Weight | Tool A | Tool B | Tool C |
| --- | --- | --- | --- | --- |
| Precision (own corpus) | 25% | 4 (78% TP) | 3 (62%) | 5 (88%) |
| Recall (OWASP Benchmark) | 15% | 4 (82%) | 5 (90%) | 3 (68%) |
| Language coverage (Go, Python, TS) | 15% | 5 (all) | 4 (no TS) | 5 (all) |
| Custom rule authoring | 10% | 5 (Semgrep-style) | 2 (limited DSL) | 3 (Rego-based) |
| PR integration | 10% | 5 | 4 | 5 |
| Triage UX | 10% | 4 | 3 | 5 |
| Operational fit (self-host) | 10% | 5 | 5 | 3 (SaaS only) |
| Pricing | 5% | 3 (mid) | 5 (low) | 2 (high) |
| Weighted total | -- | 4.3 | 3.7 | 4.1 |

## Running a PoC

1. **Define corpus** (~1 day): pick 3 services from your codebase
   covering languages and architectural patterns. Include one
   recent past-CVE-fix branch where the truth is known.
2. **Install each tool** (1-2 days per tool): run baseline scan.
3. **Run the same scan against the benchmarks** (1 day): generate
   precision / recall numbers.
4. **Triage 20 findings per tool** (2-3 days): record TP / FP and
   time-to-decision.
5. **Author a custom rule per tool** (1 day): how easy is it to
   express a project-specific pattern (e.g., "API endpoint missing
   authorization decorator")?
6. **CI integration** (1 day per tool): SARIF upload, PR
   annotations, severity gates.
7. **Score and decide** (1 day).

Total: 2-4 weeks for 2-3 tools, run in parallel.

## Common pitfalls in SAST evaluation

- Comparing default rule sets. Custom rules are where the value
  is over a multi-year horizon; evaluate that capability.
- Counting findings as a metric. A tool that reports 5,000 findings
  is not necessarily better than one that reports 500; precision is
  the relevant number.
- Ignoring time-to-triage. A tool with a 1-click suppression and a
  thoughtful UI saves more engineering time than a 5% precision
  improvement on its own.
- Skipping IDE integration. Developers fix what they see at write
  time; CI-only feedback is too late for many bug classes.

## References

- OWASP Benchmark Project: <https://owasp.org/www-project-benchmark/>
- NIST SARD: <https://samate.nist.gov/SARD/>
- Juliet Test Suite: <https://samate.nist.gov/SARD/test-suites>
- OWASP Source Code Analysis Tools: <https://owasp.org/www-community/Source_Code_Analysis_Tools>
- NIST SAMATE: <https://samate.nist.gov/>
