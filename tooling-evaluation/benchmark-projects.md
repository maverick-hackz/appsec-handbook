# Benchmark Projects

Public deliberately-vulnerable applications and test corpora for
evaluating AppSec tools. Use a mix of standardised benchmarks
(comparable precision / recall numbers) and realistic apps
(end-to-end workflows).

## Standardised benchmarks

| Project | Languages | Purpose |
| --- | --- | --- |
| OWASP Benchmark Project | Java | Standardised SAST precision / recall reporting; widely cited |
| NIST SARD | Multiple | Curated set of true-positive / false-positive samples per weakness |
| Juliet Test Suite | C/C++, Java, C# | NIST-curated CWE-tagged samples |
| SecBench | Multiple | Real CVE-derived patches across many languages |

## Web applications -- deliberately vulnerable

| Project | Stack | Strong at |
| --- | --- | --- |
| OWASP WebGoat | Java | Server-side vulns, classic XSS / SQLi / IDOR |
| OWASP Juice Shop | Node.js + Angular | Modern SPA + REST; broad OWASP Top 10 coverage |
| OWASP NodeGoat | Node.js + Express | OWASP Top 10 in a Node setting |
| RailsGoat | Ruby on Rails | Rails-specific patterns |
| Damn Vulnerable Web Application (DVWA) | PHP | Classic; useful for fuzz-style discovery |
| bWAPP | PHP | Long list of categories; aging but broad |
| WebGoat.NET | .NET | .NET-specific patterns |
| Hacker101 CTF (HackerOne) | Various | Bug-bounty-style challenges |

## API and GraphQL

| Project | Stack | Strong at |
| --- | --- | --- |
| Damn Vulnerable GraphQL Application (DVGA) | Node.js + GraphQL | Introspection, depth, batching, IDOR over GraphQL |
| crAPI (OWASP) | Java + Python + Vue | API-specific vulnerabilities aligned to API Top 10 |
| Pixi (OWASP) | Node.js | REST API misconfiguration |
| VAmPI | Python + Flask | Vulnerable API with OpenAPI spec |

## Containers and infrastructure

| Project | Purpose |
| --- | --- |
| Bad-Pods (BishopFox) | Vulnerable Kubernetes pod configurations |
| Sock Shop (Weaveworks) | Realistic microservice demo (use for DAST coverage) |
| Vulhub | Docker-Compose stacks of vulnerable software versions |
| Damn Vulnerable Docker | Container-escape and image-scan benchmarks |

## Mobile

| Project | Platform | Purpose |
| --- | --- | --- |
| OWASP iGoat-Swift | iOS | iOS-specific weaknesses |
| OWASP MSTG-Hacking-Playground | iOS + Android | Multi-platform |
| DIVA (Damn Insecure and Vulnerable App) | Android | Android-specific weaknesses |
| AndroGoat | Android | Storage, network, IPC, WebView weaknesses |
| DVIA-v2 | iOS | Storage, IPC, keychain |

## CI/CD and supply chain

| Project | Purpose |
| --- | --- |
| Vulnado | Java + insecure build |
| Argo CD demo apps | GitOps anti-pattern demonstrations |

## How to use this list

- **Standardised benchmarks** (OWASP Benchmark, SARD, Juliet) give
  precision / recall numbers that are comparable across tools.
  Vendors often quote OWASP Benchmark.
- **Realistic apps** (WebGoat, Juice Shop, crAPI) test the
  end-to-end workflow: discovery, triage, reporting. Run a full
  scan + triage + ticket-creation cycle on at least one of these
  before adopting any tool.
- **Past-CVE corpus** (your own previous fixes) is the best signal
  for "would this tool have caught the issue we already had". Use
  alongside the public benchmarks.

## Operational notes

- Run all targets in isolated environments. Do not expose
  deliberately-vulnerable hosts to the internet.
- Mirror the apps' source AND a built artefact (image, APK) so SAST,
  SCA, and DAST can all share a corpus.
- Snapshot the corpus version; refresh quarterly. Vulnerable apps
  evolve; pin to a specific tag for reproducible numbers.

## References

- OWASP Benchmark: <https://owasp.org/www-project-benchmark/>
- NIST SARD: <https://samate.nist.gov/SARD/>
- Juliet Test Suite (NIST): <https://samate.nist.gov/SARD/test-suites>
- OWASP WebGoat: <https://owasp.org/www-project-webgoat/>
- OWASP Juice Shop: <https://owasp.org/www-project-juice-shop/>
- OWASP crAPI: <https://owasp.org/www-project-crapi/>
- OWASP DVGA: <https://owasp.org/www-project-damn-vulnerable-graphql-application/>
- OWASP iGoat: <https://owasp.org/www-project-igoat-tool/>
- VulHub: <https://vulhub.org/>
