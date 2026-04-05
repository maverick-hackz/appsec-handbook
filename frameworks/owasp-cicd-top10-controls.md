# OWASP Top 10 CI/CD Security Risks Controls

Risks specific to the build and delivery pipeline itself. Each item
below lists controls; cross-reference the
[../devsecops/](../devsecops/) section for implementation.

## CICD-SEC-1 -- Insufficient Flow Control Mechanisms

Anyone with write access to source can trigger a deploy; one approval
suffices for production; no merge queue.

Controls:

- Branch protection requiring at least one non-author approving
  review, signed commits, and a passing required-checks set.
- CODEOWNERS for sensitive paths.
- Two-person review for changes that touch the pipeline itself.
- Merge queue ensures the merged state is the tested state.

## CICD-SEC-2 -- Inadequate Identity and Access Management

Shared service accounts in CI; long-lived PATs; same identity used
for build and deploy; no per-pipeline scoping.

Controls:

- Short-lived OIDC-federated credentials (no static cloud secret).
- Separate identities for build vs deploy.
- Scope CI tokens to one repository / workflow.
- Off-board promptly; audit token usage.

## CICD-SEC-3 -- Dependency Chain Abuse

Typosquatting, namespace squatting, dependency confusion, poisoned
upstream packages.

Controls:

- Internal registry / scope for first-party packages.
- Pinned versions in lockfiles; hash-pinning where supported.
- SCA on every PR with HIGH/CRITICAL block.
- See [../devsecops/supply-chain/dependency-pinning.md](../devsecops/supply-chain/dependency-pinning.md).

## CICD-SEC-4 -- Poisoned Pipeline Execution (PPE)

A PR (often from a fork or an internal contributor) modifies the
pipeline definition itself and exfiltrates secrets or alters the
build output.

Controls:

- Pipeline definition stored in code and protected by branch policy.
- Pull-request workflows do NOT receive production secrets.
- Workflows triggered by `pull_request_target` (with elevated context)
  carefully audited; prefer `pull_request` for untrusted contributors.
- Reusable workflows pinned by SHA, not by tag.

## CICD-SEC-5 -- Insufficient PBAC (Pipeline-Based Access Controls)

A single pipeline identity has access to every environment; a
compromise in one workflow becomes a compromise everywhere.

Controls:

- Per-environment identities with environment-scoped secrets and
  manual approval gates for production.
- Read-only credentials in PR pipelines; write credentials only on
  protected-branch builds.
- Least privilege on every job: `permissions:` block declares the
  minimum required scopes.

## CICD-SEC-6 -- Insufficient Credential Hygiene

Long-lived tokens; secrets in code / config; no rotation; high-scope
PATs.

Controls:

- OIDC federation; ephemeral credentials per build.
- Vault / cloud secret manager for any required long-lived secret.
- Secret scanning on every PR and on a schedule.
- Documented rotation cadence per secret class.
- See [../secure-coding/secrets-handling.md](../secure-coding/secrets-handling.md)
  and [../devsecops/ci-templates/github-actions/secrets-gitleaks.yml](../devsecops/ci-templates/github-actions/secrets-gitleaks.yml).

## CICD-SEC-7 -- Insecure System Configuration

CI runners with persistent disks across jobs; debug shells exposed;
running unpatched runners.

Controls:

- Ephemeral runners per job (GitHub-hosted, GitLab SaaS, or
  self-hosted with per-job isolation).
- No persistent shared filesystem across PR jobs.
- Patch / refresh runner images on a schedule.

## CICD-SEC-8 -- Ungoverned Usage of Third-Party Services

Workflows pull in unaudited third-party Actions, plugins, or external
CI integrations.

Controls:

- Allowlist of approved third-party Actions; deny by default at
  org level.
- Pin Actions by SHA digest, not by floating tag.
- Inventory all third-party services per workflow; review changes.
- Use trusted-publisher patterns for first-party Actions.

## CICD-SEC-9 -- Improper Artifact Integrity Validation

Artifact published without signing; consumer pulls by mutable tag;
no provenance attestation; admission accepts unsigned images.

Controls:

- Cosign signing (Sigstore keyless) on every published artifact.
- SLSA provenance attestation.
- Admission controller verifies signature AND OIDC subject.
- Deploy by digest, not by tag.
- See [../devsecops/ci-templates/github-actions/sign-cosign.yml](../devsecops/ci-templates/github-actions/sign-cosign.yml)
  and [../devsecops/supply-chain/slsa-levels.md](../devsecops/supply-chain/slsa-levels.md).

## CICD-SEC-10 -- Insufficient Logging and Visibility

Pipeline events are not logged or shipped to a tamper-resistant store;
no alerting on suspicious patterns (workflow modification, secret
access).

Controls:

- Audit logs from CI (workflow runs, secret access) streamed off-host
  to an append-only store.
- Alert on workflow definition changes, secret read events outside
  expected workflows, and run-as-different-actor anomalies.
- Retention sized to the incident-response window.

## References

- OWASP Top 10 CI/CD Security Risks: <https://owasp.org/www-project-top-10-ci-cd-security-risks/>
- SLSA: <https://slsa.dev/spec/>
- GitHub Actions security hardening: <https://docs.github.com/en/actions/security-guides/security-hardening-for-github-actions>
- GitLab CI/CD security: <https://docs.gitlab.com/ee/ci/yaml/>
- CNCF Software Supply Chain Best Practices: <https://github.com/cncf/tag-security>
