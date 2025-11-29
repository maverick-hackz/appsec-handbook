# Contributing

## File conventions

- Every file follows the template documented in the README of its parent section.
- Naming: kebab-case, English, `.md` extension for documentation files.
- Every file containing commands, payloads, or configuration ends with a
  `## References` section that links to OWASP, NIST, MITRE, RFC, or vendor
  documentation. Blog posts are supporting material, not primary sources.
- No internal or proprietary data. Sanitize hostnames, IP addresses, identifiers,
  and any organization-specific terminology before adding examples.
- Plain technical prose. No emoji, no marketing tone, no first-person voice.

## Validation before opening a PR

Run the relevant local checks for the files touched:

- Markdown: `markdownlint "**/*.md"` or `npx markdownlint-cli2 "**/*.md"`
- YAML under `devsecops/`: `yamllint .`
- Custom Semgrep rules under `devsecops/semgrep-rules/`:
  `semgrep --config devsecops/semgrep-rules/ --validate` and
  `semgrep --config devsecops/semgrep-rules/ --test`
- Kubernetes manifests: `kubectl --dry-run=client apply -f <file>` against a
  cluster you own, or `kubeconform` for offline schema validation.

Tools should be installed in a local virtual environment or via project-local
package managers; do not require global installation.

## Pull request description

A PR description should answer four questions:

1. What changed?
2. Which sections of the handbook were touched and why?
3. What are the primary sources for new claims (OWASP, NIST, MITRE, RFC, vendor docs)?
4. What validation was run (markdownlint, yamllint, semgrep --test, kubectl --dry-run)?

## What is not accepted

- Internal or proprietary documentation.
- Hostnames, IP addresses, or identifiers from real production systems other
  than vendor documentation references.
- Claims without verifiable references.
- Offensive payloads or pentest cheatsheets. Those belong in the companion
  repository: <https://github.com/maverick-hackz/Workstation>
- Auto-generated content without sources.
