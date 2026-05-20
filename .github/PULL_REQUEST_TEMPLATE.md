<!--
  Per CONTRIBUTING.md, a pull request description should answer four
  questions. Replace each prompt below with a concise answer.
-->

## 1. What changed?

<!-- One or two sentences. -->

## 2. Which sections of the handbook were touched and why?

<!-- List the affected paths (secure-coding/, devsecops/, frameworks/, ...)
     and the motivation for each. -->

## 3. Primary sources

<!-- OWASP, NIST, MITRE, RFC, vendor documentation. Blogs are supporting
     material, not primary sources. -->

## 4. Validation

- [ ] `markdownlint-cli2 "**/*.md"` (or affected files only)
- [ ] `yamllint .` (if any `.yml` / `.yaml` under `devsecops/` was touched)
- [ ] `semgrep --config devsecops/semgrep-rules/ --validate` (if rules touched)
- [ ] `semgrep --config devsecops/semgrep-rules/ --test` (if rules touched)
- [ ] `kubectl --dry-run=client apply -f <file>` or `kubeconform` (if K8s
      manifests touched)
- [ ] `lychee --offline <files>` (internal relative links resolve)

## Notes for the reviewer

<!-- Anything that affects how this should be evaluated: known limitations,
     follow-ups planned in a separate PR, related issues. -->
