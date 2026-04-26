# DAST Evaluation Methodology

DAST scanners exercise the running application. They differ in how
they discover the surface (crawler vs replay vs schema-driven), how
they handle authentication, and what they do with single-page apps
and APIs.

## Criteria

| Criterion | What to measure | How |
| --- | --- | --- |
| Coverage approach | Crawler-only, replay (from proxy capture), schema-driven (OpenAPI / GraphQL), or hybrid | Inspect docs + hands-on |
| Authenticated scanning | Form login, OIDC, SAML, custom auth scripts | Try each |
| Session handling | Anti-CSRF token capture, JWT refresh, cookie rotation | Try |
| SPA support | Detects client-side routes; can drive a headless browser | Try on a real SPA |
| API testing | REST via OpenAPI, GraphQL via introspection / schema, gRPC | Try |
| WebSocket / SSE | Discovers and tests streaming endpoints | Try if relevant |
| Out-of-band testing | Burp Collaborator-style for SSRF / blind XXE | Look for it |
| Rule coverage | OWASP Top 10 / WSTG categories | Inspect |
| False-positive rate | On a known-clean app | Run baseline against a hardened sample |
| CI integration | SARIF or vendor format; gate by severity | Hands-on |
| Reporting | Severity, CVSS, evidence (request/response), repro steps | Inspect a real finding |
| Throttling / rate limit awareness | Pause / back-off on 429 | Try with a small target |
| Distributed scanning | Scale across multiple worker nodes | Confirm if relevant |
| Operational deployment | SaaS / self-host / agent-based | Confirm fit |

## Test corpus

- A staging deployment of one of your services.
- WebGoat / Juice Shop / NodeGoat / DVWA for known-vuln baselines.
- An OpenAPI 3.x specification of your API -- pass to API-aware
  scanners to compare coverage to crawler-only.
- A GraphQL service for schema-driven API DAST.

See [benchmark-projects.md](benchmark-projects.md) for the full set.

## Authenticated scanning -- what to test

Authentication is where most DAST tools struggle. Confirm:

- Tool can complete an OIDC code+PKCE login (the common modern auth).
- Tool can refresh tokens during a long scan.
- Tool can handle CSRF tokens that rotate per page.
- Tool can scan beyond the home page after login (some get stuck on
  the post-login landing).

A scanner that can only test the public surface misses most of the
application.

## API-aware vs crawler-only

A modern application served by an SPA has very little server-rendered
HTML for a crawler to discover. The actual surface is the API the SPA
talks to. Two paths:

- Provide the OpenAPI spec; the scanner enumerates from the schema.
- Capture traffic from real usage and replay it.

Tools that lack both fall back to crawling the SPA's HTML and miss
most endpoints.

## Common pitfalls

- Comparing on a public demo target. Demo targets are tuned to
  reveal specific bugs the vendor wants to highlight; the precision
  / recall mix on real code is the metric.
- Skipping rate-limit testing. A scanner that hammers a per-IP
  limit triggers WAFs and produces noise instead of findings.
- Ignoring out-of-band detection. SSRF, blind XXE, blind SQLi need
  out-of-band correlation; a scanner without it misses an entire
  vulnerability class.
- Forgetting fork / non-standard frameworks. Some scanners handle
  Express better than Django / FastAPI / Spring; test on your actual
  framework.

## Operational considerations

- DAST scans on staging, not on production. Confirm staging mirrors
  production configuration.
- Schedule full scans during low-traffic windows; baseline scans
  per-PR are quick (passive + a few active probes).
- Carve out a dedicated test tenant / account for scanning so the
  scanner's noise does not pollute real data.

## Scoring matrix

| Criterion | Weight | Tool A | Tool B |
| --- | --- | --- | --- |
| API DAST (OpenAPI-driven) | 20% | 5 | 3 |
| Authenticated scanning | 20% | 4 | 4 |
| SPA support (headless browser) | 15% | 5 | 4 |
| Out-of-band testing | 10% | 5 (Collaborator) | 0 |
| CI integration | 10% | 4 | 5 |
| False-positive rate | 10% | 4 | 4 |
| Operational deployment | 10% | 3 (SaaS) | 5 (self-host) |
| Pricing | 5% | 3 | 4 |
| Weighted total | -- | 4.2 | 3.8 |

## References

- OWASP Web Security Testing Guide (WSTG): <https://owasp.org/www-project-web-security-testing-guide/>
- OWASP ZAP: <https://www.zaproxy.org/docs/>
- Burp Suite Professional: <https://portswigger.net/burp/documentation>
- Nuclei: <https://docs.projectdiscovery.io/tools/nuclei/overview>
- Schemathesis (API DAST): <https://schemathesis.readthedocs.io/>
- OWASP Vulnerability Scanning Tools: <https://owasp.org/www-community/Vulnerability_Scanning_Tools>
