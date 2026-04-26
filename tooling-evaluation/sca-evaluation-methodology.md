# SCA Evaluation Methodology

Software Composition Analysis identifies and risk-rates open-source
components. Tools differ in DB sources, transitive resolution,
ecosystem coverage, and reachability analysis.

## Criteria

| Criterion | What to measure | How |
| --- | --- | --- |
| Vulnerability DB sources | NVD, OSV, GHSA, vendor-specific, commercial enrichment | Catalogue per tool |
| Update frequency | DB refresh cadence; time from CVE publication to detection | Track over 30 days |
| Ecosystem coverage | npm, pip, Maven, Go modules, Gradle, NuGet, Cargo, Composer, etc. | Confirm for your stack |
| Transitive resolution accuracy | Does the tool understand the package manager's resolution rules? | Compare to `npm ls`, `pip list`, `go mod graph` |
| Lockfile support | Reads `package-lock.json`, `Pipfile.lock`, `go.sum`, etc.? | Test |
| License detection | SPDX identifier per component; copyleft warning | Inspect |
| Reachability analysis | Distinguishes "imported" from "called" | Try with a benign vulnerable transitive dep |
| EPSS / KEV integration | Prioritization signals | Verify |
| SBOM ingest / output | CycloneDX, SPDX read / write | Try generating + ingesting |
| VEX support | Read / write VEX statements for non-exploitable CVEs | Try |
| IDE / pre-commit integration | Local feedback before push | Hands-on |
| CI integration | SARIF / GitLab dependency_scanning report | Hands-on |
| Container image support | Scan OS packages + language packages in same scan | Try a multi-language image |
| IaC scan | Terraform / Helm / K8s manifests in same tool | Test if relevant |
| SSO / RBAC | SAML / OIDC; team-level scoping | Configure |
| Pricing model | Per developer / per repo / per project | Quote |

## Test corpus

- Your own service with the actual `package.json` / `requirements.txt`
  / `go.mod`.
- A "vulnerable dep" sample: `lodash@4.17.20`, `log4j-core@2.14.1`,
  `werkzeug@0.15.5`, `urllib3@1.25.8` -- any known-CVE versions.
  <!-- TODO: keep this list refreshed; pin to the current CVE landscape -->
- An image that mixes OS-level (`libc`, `openssl`) and language-level
  CVEs.

## Reachability analysis -- what to look for

A reachable vulnerability is one where the application's code path
actually invokes the vulnerable function. Two tools can give very
different prioritization:

- Tool A reports "lodash CVE-X applies", regardless of whether
  `_.template` is called.
- Tool B reports "lodash CVE-X applies AND `_.template` is reached
  from `src/router.ts:42`".

Tool B's signal is much higher value -- but only if the reachability
analysis is correct. Test with a few known-reachable AND
known-unreachable vulnerable deps and confirm the verdict.

False positives from reachability analysis are particularly damaging
because teams stop trusting "reachable" flags.

## Scoring matrix

| Criterion | Weight | Tool A | Tool B |
| --- | --- | --- | --- |
| Ecosystem coverage | 20% | 5 | 4 |
| Transitive resolution accuracy | 15% | 4 | 5 |
| DB sources + update freshness | 15% | 5 | 4 |
| Reachability analysis | 15% | 0 (not offered) | 4 |
| EPSS / KEV integration | 10% | 3 | 5 |
| SBOM in/out | 10% | 5 | 4 |
| VEX support | 5% | 0 | 3 |
| Operational fit | 5% | 5 | 3 |
| Pricing | 5% | 4 | 2 |
| Weighted total | -- | 3.8 | 4.0 |

## Pitfalls

- Confusing "number of CVEs detected" with quality. A tool that
  reports every transitive dep at HIGH due to a single CVE in a
  rarely-used method drowns the team in noise.
- Skipping the transitive accuracy test. Tools handle workspaces,
  optional dependencies, peer dependencies, and Go submodules
  differently; a tool that misses 20% of your transitive tree is
  useless.
- Choosing a SaaS-only tool when your environment requires
  on-prem / air-gapped. Confirm deployment options early.

## References

- OSV.dev (Google's open vulnerability database): <https://osv.dev/>
- NVD (NIST): <https://nvd.nist.gov/>
- GHSA (GitHub Advisory Database): <https://github.com/advisories>
- FIRST EPSS: <https://www.first.org/epss/>
- CISA KEV: <https://www.cisa.gov/known-exploited-vulnerabilities-catalog>
- OWASP Dependency-Check: <https://owasp.org/www-project-dependency-check/>
- OWASP CycloneDX: <https://cyclonedx.org/>
- OpenVEX: <https://github.com/openvex/spec>
