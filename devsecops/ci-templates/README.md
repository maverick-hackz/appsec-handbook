# CI Templates

Drop-in security workflows for GitHub Actions and GitLab CI. Each file
is syntactically valid and starts with a comment header documenting
purpose, required permissions, and required secrets.

## GitHub Actions ([github-actions/](github-actions/))

| File | Purpose |
| --- | --- |
| [sast-semgrep.yml](github-actions/sast-semgrep.yml) | Semgrep SAST on push and PR, SARIF upload to Code Scanning |
| [sca-trivy-fs.yml](github-actions/sca-trivy-fs.yml) | Trivy filesystem SCA on dependency manifests |
| [secrets-gitleaks.yml](github-actions/secrets-gitleaks.yml) | Gitleaks: PR diff + scheduled full-history scan |
| [iac-checkov.yml](github-actions/iac-checkov.yml) | Checkov for Terraform / K8s / Dockerfile / CloudFormation |
| [container-trivy-image.yml](github-actions/container-trivy-image.yml) | Trivy image scan after build |
| [sbom-syft.yml](github-actions/sbom-syft.yml) | CycloneDX SBOM generation per build |
| [sign-cosign.yml](github-actions/sign-cosign.yml) | Sigstore keyless signing of image and SBOM attestation |
| [dast-zap-baseline.yml](github-actions/dast-zap-baseline.yml) | OWASP ZAP baseline DAST against staging |

## GitLab CI ([gitlab-ci/](gitlab-ci/))

| File | Purpose |
| --- | --- |
| [sast-semgrep.gitlab-ci.yml](gitlab-ci/sast-semgrep.gitlab-ci.yml) | Semgrep SAST stage |
| [sca-trivy.gitlab-ci.yml](gitlab-ci/sca-trivy.gitlab-ci.yml) | Trivy filesystem and image scan stages |
| [secrets-gitleaks.gitlab-ci.yml](gitlab-ci/secrets-gitleaks.gitlab-ci.yml) | Gitleaks stage |

## Version pinning

All actions and Docker images use specific version tags (or major
version aliases such as `@v6`). Verify against the current GA
marketplace before merging; refresh quarterly. Renovate / Dependabot
can manage these automatically for `.github/workflows/*.yml`.

## Required permissions and secrets

Each workflow file declares its required `permissions` block at the
workflow or job level. Common patterns:

- `contents: read` for read-only analysis.
- `security-events: write` for SARIF upload to Code Scanning.
- `id-token: write` for Sigstore keyless OIDC.
- `packages: write` for pushing to GHCR (cosign signing workflow only).

No long-lived secrets are required for the templates as written. The
gitleaks and ZAP templates accept optional license / token secrets via
named environment variables; absence falls back to the open-source
behaviour.
