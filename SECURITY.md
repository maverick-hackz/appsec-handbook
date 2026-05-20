# Security Policy

## Scope

This repository contains documentation, Semgrep rules, and CI/CD templates for
application security education. It is not a deployable application: there is no
runtime code, no service, no data store.

The security policy below covers defects in the materials themselves:

- Inaccurate or unsafe guidance in `secure-coding/`, `threat-modeling/`,
  `secure-sdlc/`, `architecture/`, or `frameworks/`.
- False positive or false negative behaviour in Semgrep rules under
  `devsecops/semgrep-rules/`.
- Insecure defaults in CI/CD templates under `devsecops/ci-templates/`
  (for example, excessive `permissions` blocks, unpinned actions, secrets
  exposed via logs).
- Kubernetes policies under `devsecops/k8s-policies/` that fail open or that
  contradict their stated intent.

The templates and policies in this repository are starting points. They are
not validated for any specific production environment, regulatory regime,
or threat model. Adapt before deployment.

## Reporting a vulnerability

Email: <shevchuk.savva@gmail.com>

Optional PGP encryption is supported. Fingerprint:

<!-- TODO: replace with a published PGP key fingerprint -->
`<PGP fingerprint to be published>`

Please include:

- Affected file path and line range or rule identifier.
- A description of the issue and the security impact (what assumption breaks,
  what an attacker gains).
- A primary source for the corrected guidance (RFC, OWASP, NIST, MITRE, or
  vendor documentation).
- Proof-of-concept input or counter-example for Semgrep rule defects, if
  applicable.

## Service levels

- Acknowledgement within 7 days of receipt.
- Triage decision (fix, accept-with-note, or decline-with-reason) within 30 days.
- Coordinated disclosure on request. The default is public attribution in the
  fix commit unless the reporter requests anonymity.

## Out of scope

- Vulnerabilities in third-party tools referenced in the handbook
  (Semgrep, Trivy, Falco, kube-bench, mkdocs-material, lychee, and others).
  Report those to their respective maintainers.
- Generic style or wording preferences not affecting correctness.
- Reports generated solely by automated tooling without human review.

## Acknowledgements

Reporters who follow this policy and request attribution will be listed in
`references/acknowledgements.md` once that file is introduced.
