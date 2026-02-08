# Pipeline Reference Architecture

A paved-road template for a service-level CI/CD pipeline. Stages are
platform-agnostic; the [ci-templates/](ci-templates/) folder provides
concrete GitHub Actions and GitLab CI fragments per stage.

## Stages

```text
[ developer push / PR ]
       |
       v
+--------------------------+
|     1. PRE-COMMIT        |   local hooks: gitleaks, lint, format
+--------------------------+
       |
       v
+--------------------------+
|     2. CI: ANALYSIS      |   SAST | SCA | secret scan | IaC scan
+--------------------------+
       |
       v
+--------------------------+
|     3. CI: TEST          |   unit + integration + authorization tests
+--------------------------+
       |
       v   (push to protected branch only)
+--------------------------+
|     4. BUILD             |   image build, SBOM, sign, push by digest
+--------------------------+
       |
       v
+--------------------------+
|     5. DEPLOY: STAGING   |   admission verify + smoke + DAST baseline
+--------------------------+
       |
       v
+--------------------------+
|     6. DEPLOY: PROD      |   admission verify, canary, monitor
+--------------------------+
```

## Stage details

### 1. Pre-commit (local)

Hooks: gitleaks, ruff / golangci-lint / eslint, markdownlint, yamllint,
hadolint, shellcheck, plus a project-local semgrep config.

Goal: catch trivial mistakes before they reach CI. See
[pre-commit/](pre-commit/).

### 2. CI Analysis

- SAST: Semgrep + CodeQL where the language is supported.
  See [ci-templates/github-actions/sast-semgrep.yml](ci-templates/github-actions/sast-semgrep.yml).
- SCA: Trivy filesystem or OSV-Scanner.
  See [ci-templates/github-actions/sca-trivy-fs.yml](ci-templates/github-actions/sca-trivy-fs.yml).
- Secret scan: Gitleaks on diff (PR) and full history (scheduled).
  See [ci-templates/github-actions/secrets-gitleaks.yml](ci-templates/github-actions/secrets-gitleaks.yml).
- IaC scan: Checkov for Terraform / Kubernetes / Dockerfile.
  See [ci-templates/github-actions/iac-checkov.yml](ci-templates/github-actions/iac-checkov.yml).

All scanners upload SARIF; severity thresholds per
[../secure-sdlc/security-gates-by-stage.md](../secure-sdlc/security-gates-by-stage.md).

### 3. CI Test

- Unit and integration tests, including the security-critical paths
  (auth check, validation reject, error path) called out in
  [../secure-sdlc/code-review-checklist.md](../secure-sdlc/code-review-checklist.md).
- Coverage targeted at security decision points rather than line
  percentage.

### 4. Build

- Multi-stage Dockerfile per [dockerfile-hardening.md](dockerfile-hardening.md).
- Trivy image scan after build:
  [ci-templates/github-actions/container-trivy-image.yml](ci-templates/github-actions/container-trivy-image.yml).
- CycloneDX SBOM per build:
  [ci-templates/github-actions/sbom-syft.yml](ci-templates/github-actions/sbom-syft.yml).
- Keyless cosign signing of the image AND an SBOM attestation:
  [ci-templates/github-actions/sign-cosign.yml](ci-templates/github-actions/sign-cosign.yml).
- Push by content digest, not by floating tag.

### 5. Deploy: Staging

- Admission controller verifies the cosign signature AND the OIDC
  subject of the signer. See [k8s-policies/](k8s-policies/).
- Smoke tests cover the authentication flow and the new endpoints.
- DAST baseline against the deployed staging:
  [ci-templates/github-actions/dast-zap-baseline.yml](ci-templates/github-actions/dast-zap-baseline.yml).

### 6. Deploy: Production

- Same admission verification as staging.
- Canary: a small percentage of traffic to the new revision; promote
  on a green error-budget window.
- Monitor: alerting on authentication-failure spikes, error rate, and
  latency on the new endpoints.

## Cross-cutting

- **Permissions**: every job declares the minimum permissions it
  needs. `contents: read` is the default; bump per job.
- **OIDC, not long-lived secrets**: short-lived federated credentials
  to cloud providers and the registry; no PAT / static cloud secret.
- **Ephemeral runners**: each job runs on a fresh runner with no
  persistent disk; no state shared between jobs.
- **Dependency cache** keyed by lockfile hash and toolchain version;
  never reuse the cache across PRs from external contributors.
- **PR forks**: workflows triggered by `pull_request` from forks must
  not have access to deploy / push secrets.

## References

- OWASP DevSecOps Guideline: <https://owasp.org/www-project-devsecops-guideline/>
- OWASP Top 10 CI/CD Security Risks: <https://owasp.org/www-project-top-10-ci-cd-security-risks/>
- SLSA Specification: <https://slsa.dev/spec/>
- GitHub Actions security hardening: <https://docs.github.com/en/actions/security-guides/security-hardening-for-github-actions>
- GitLab CI/CD security: <https://docs.gitlab.com/ee/ci/yaml/>
