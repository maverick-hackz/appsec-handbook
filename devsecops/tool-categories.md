# Tool Categories

A glossary and evaluation lens for the AppSec automation landscape.
Pick a category to address a specific gap; do not try to buy "an
AppSec tool" generically.

## Static analysis

| Category | Inputs | Outputs | When to use | Examples |
| --- | --- | --- | --- | --- |
| SAST | source code | findings with location and severity | every PR | Semgrep, CodeQL, SonarQube, Bandit, gosec |
| SCA | dep manifests + lockfiles | vulnerable component list | every PR + daily | Trivy, Snyk, OSV-Scanner, Dependabot |
| Secret scanning | source + git history | leaked credentials | every PR + scheduled history scan | gitleaks, trufflehog, detect-secrets |
| IaC scanning | Terraform / K8s / Dockerfile | misconfigurations | every PR | Checkov, tfsec, kube-linter, hadolint |
| License compliance | dep manifests | SPDX license per component | every PR | Trivy, ScanCode, FOSSA |

## Dynamic analysis

| Category | When | Examples |
| --- | --- | --- |
| DAST | against a running staging app | OWASP ZAP, Burp Suite Professional, Nuclei |
| API DAST | against an OpenAPI / GraphQL endpoint | ZAP API scan, Schemathesis |
| MAST | against a mobile binary + emulator | MobSF, Frida, objection, Drozer |
| IAST | runtime agent in the test environment | Contrast, Seeker |

## Container and runtime

| Category | When | Examples |
| --- | --- | --- |
| Image scanning | after build | Trivy, Grype, Snyk Container |
| Admission control | at deploy time | Kyverno, OPA Gatekeeper, Cosign policy controller |
| Runtime detection | in-cluster | Falco, Tetragon, Sysdig |
| CSPM (Cloud Posture) | continuous | Prowler, ScoutSuite, vendor-native CSPM |

## Supply chain

| Category | When | Examples |
| --- | --- | --- |
| SBOM generation | per build | Syft, `npm sbom`, cdxgen, Microsoft `sbom-tool` |
| Signing | per artifact | cosign (Sigstore), GnuPG (legacy) |
| Provenance attestation | per build | SLSA, in-toto, GitHub OIDC + cosign |
| Verification | at admission | `cosign verify`, slsa-verifier, Kyverno cosign rule |

## Aggregation and posture

| Category | Purpose | Examples |
| --- | --- | --- |
| ASPM | dedupe findings across tools, prioritize, route tickets | DefectDojo, Phoenix Security, Apiiro |
| SBOM management | ingest, diff, alert on new CVEs against existing SBOMs | OWASP Dependency-Track, Anchore Enterprise |
| Bug bounty / VDP platform | external researcher pipeline | HackerOne, Bugcrowd, Intigriti |

## Choosing per gap

A gap is "we cannot detect class X today". The right tool category
maps to the gap directly:

| Gap | Category |
| --- | --- |
| Inject patterns are sneaking past review | SAST |
| Vulnerable dep landed in production yesterday | SCA + ASPM (visibility) |
| Hard-coded secret in a commit two years ago | Secret scanning (full history) |
| Cluster runs containers as root | Admission control (Kyverno / OPA) |
| Suspicious behaviour from a workload at runtime | Runtime detection (Falco) |
| Cannot prove a given binary was built from this source | Provenance + signing |
| 5,000 findings across 4 tools and no triage | ASPM |

## What this list omits

- Vendor-specific marketing categories ("next-gen", "agentic") that do
  not correspond to a clear input-output contract.
- Penetration-testing services. Methodology for evaluating those
  belongs in [../tooling-evaluation/](../tooling-evaluation/).

## References

- OWASP DevSecOps Guideline: <https://owasp.org/www-project-devsecops-guideline/>
- NIST SSDF (SP 800-218): <https://csrc.nist.gov/Projects/ssdf>
- OWASP Source Code Analysis Tools: <https://owasp.org/www-community/Source_Code_Analysis_Tools>
- OWASP Vulnerability Scanning Tools: <https://owasp.org/www-community/Vulnerability_Scanning_Tools>
- CNCF Security TAG resources: <https://github.com/cncf/tag-security>
