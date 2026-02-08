# DevSecOps

CI/CD security automation: pipeline reference architecture, tool
categories, ready-to-fork templates for GitHub Actions and GitLab CI,
pre-commit hooks, custom Semgrep rules, Kubernetes policies, and
supply-chain integrity.

## Files

- [tool-categories.md](tool-categories.md) — SAST / SCA / DAST / MAST / IAST / RASP / ASPM
- [pipeline-reference-architecture.md](pipeline-reference-architecture.md) — paved-road pipeline shape
- [dockerfile-hardening.md](dockerfile-hardening.md) — container image baseline
- [ci-templates/](ci-templates/) — drop-in YAML for GitHub Actions and GitLab CI
- [pre-commit/](pre-commit/) — local hook config (gitleaks, ruff, hadolint, ...)
- [semgrep-rules/](semgrep-rules/) — custom rules with `--test` cases
- [k8s-policies/](k8s-policies/) — Pod Security Admission, NetworkPolicy, OPA Gatekeeper, Falco
- [supply-chain/](supply-chain/) — SBOM, dependency pinning, SLSA

## Conventions

- All YAML templates are syntactically valid and runnable. Version pins
  are taken from the upstream marketplace at write time; refresh on
  adoption against the current GA tag.
- Permissions are minimized per workflow / job (`contents: read` default;
  `security-events: write` only where SARIF is uploaded;
  `id-token: write` only where Sigstore OIDC is required).
- PR-trigger workflows analyse the merge-result ref where supported,
  so the pipeline sees the post-merge state, not the contributor branch
  alone.
- Secret scanning and SAST run on every PR; signing and SBOM generation
  run on the protected branch only.

## What this section is NOT

- A list of specific scanners with "buy this one" advice. Tool
  selection lives in [../tooling-evaluation/](../tooling-evaluation/),
  driven by evaluation methodology rather than vendor pitches.
- A replacement for the team's existing CI. The templates are
  drop-in references; adapt them to the platform you ship from.
