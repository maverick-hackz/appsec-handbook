# Security Gates by Stage

A gate is a check the pipeline (or a human) runs at a stage, with a
known outcome that either lets the work proceed or blocks it. Each
row below is one gate.

"Blocking severity" is the highest finding severity that stops the
pipeline. Anything below is recorded as a warning and triaged later.

## Gates

| Stage | Gate | Mandatory checks | Blocking severity |
| --- | --- | --- | --- |
| Pre-commit | Local lint / secret scan | gitleaks, ruff / golangci-lint / eslint, markdownlint | Any high-confidence secret match |
| PR open | Branch policy | At least one approving review by non-author; CODEOWNERS satisfied on sensitive paths | Missing review |
| PR CI | SAST | Semgrep with the team's ruleset; CodeQL for languages where it is enabled | HIGH (with exception process for documented exceptions) |
| PR CI | SCA | Trivy / Snyk / OSV-Scanner on dependency manifests | HIGH or CRITICAL CVE in direct dependencies (with documented exception) |
| PR CI | Secret scan | gitleaks on the full PR diff and history of the branch | Any high-confidence secret match |
| PR CI | IaC scan | Checkov / tfsec on Terraform; kube-linter / kubescape on K8s manifests | HIGH misconfiguration |
| PR CI | Unit + integration tests | Coverage of security-critical paths (auth, validation, error) | Any failing test |
| Merge to main | Branch protection | Required status checks: SAST, SCA, secret scan, tests; required review; merge queue | Any required check failing |
| Build | Container scan | Trivy image scan on the built image | CRITICAL CVE in OS / language packages |
| Build | SBOM generation | Syft / `npm sbom` / `cdxgen` -> CycloneDX or SPDX artifact | Missing SBOM artifact |
| Build | Image signing | cosign keyless via OIDC; provenance attestation (SLSA Level 3 target) | Missing signature or provenance |
| Deploy to staging | Config validation | TLS, security headers, no debug, no wildcard hosts; secrets sourced from vault | Any missing required setting |
| Deploy to staging | DAST baseline | ZAP baseline scan; nuclei templates | HIGH finding on new endpoints |
| Deploy to staging | Admission policy | Image signature verification; image-policy webhook (`ImagePolicyWebhook` or Kyverno / OPA) | Unsigned image or unknown signer |
| Deploy to production | Admission policy | Same as staging plus SLSA provenance verification | Missing or wrong signer |
| Deploy to production | Change management | Production change record; rollback plan; on-call notified | Missing change record |
| Post-deploy | Smoke + canary | Health checks; auth flow smoke test; error budget threshold | Smoke fail or canary error budget exceeded |
| Continuous | Vulnerability watch | Daily SCA on the dependency-graph; KEV / EPSS monitoring | KEV-listed CVE applies to a deployed component |
| Continuous | Secret scan (org-wide) | GitHub secret scanning; gitleaks on a schedule | High-confidence secret in any branch |
| Continuous | Posture review | Quarterly SAMM / ASVS self-assessment | Decline in a maturity score |

## Severity definitions

- **CRITICAL**: known-exploited or trivially exploitable; remote code
  execution, authentication bypass, secret exfiltration. Stops the
  pipeline at every gate that lists it.
- **HIGH**: exploitable with attacker effort; SQLi, SSRF, deserialisation
  on a privileged endpoint, missing authorization on sensitive data.
- **MEDIUM**: defence-in-depth gap; missing security header, weak but
  not broken crypto choice, verbose error.
- **LOW**: informational; outdated dependency without known
  exploitability, style.

The team owns the exception process: any blocking finding can be
overridden by an approval from the security owner with a ticketed
follow-up and target date.

## Anti-patterns

- A gate that everyone overrides. If a gate is overridden weekly,
  the threshold is wrong or the tool is mistuned; fix it.
- Adding gates without owners. A gate without a triage owner becomes
  noise.
- Mixing severities into a single gate. Keep CRITICAL strict; allow
  MEDIUM / LOW to flow through with periodic backlog grooming.

## References

- OWASP DevSecOps Verification Standard: <https://owasp.org/www-project-devsecops-guideline/>
- NIST SSDF Practice PW.7 (Review code), PW.8 (Test code): <https://csrc.nist.gov/Projects/ssdf>
- CISA Known Exploited Vulnerabilities (KEV): <https://www.cisa.gov/known-exploited-vulnerabilities-catalog>
- FIRST EPSS: <https://www.first.org/epss/>
- SLSA levels: <https://slsa.dev/spec/>
