# Pre-commit Hooks

Local hook configuration to catch trivial security and quality issues
before they reach CI. The exact same hooks run in the CI templates,
so a "green pre-commit" predicts a "green CI" for the corresponding
checks.

## Hooks

| Hook | Purpose |
| --- | --- |
| `trailing-whitespace`, `end-of-file-fixer` | Source hygiene |
| `check-yaml`, `check-json`, `check-merge-conflict` | Syntax / merge-conflict markers |
| `check-added-large-files` | Block files larger than 500 KiB by default |
| `detect-private-key` | Block PEM / OpenSSH private keys |
| `gitleaks` | Pattern-based secret scanning over the diff |
| `detect-secrets` | Entropy-based secret scanning with baseline support |
| `ruff`, `ruff-format` | Python lint + format |
| `bandit` | Python SAST |
| `shellcheck` | Shell-script analysis |
| `hadolint` | Dockerfile linter |
| `yamllint` | YAML linter |
| `markdownlint-cli2` | Markdown linter (uses `.markdownlint.json`) |
| `semgrep` | Multi-language SAST with the project's custom rules |

## Install

```bash
python3 -m venv .venv
source .venv/bin/activate
pip install pre-commit
pre-commit install
pre-commit install --hook-type commit-msg
```

## Run

Against staged files (default on commit):

```bash
pre-commit run
```

Against the entire working tree (recommended after large refactors):

```bash
pre-commit run --all-files
```

Against a single hook:

```bash
pre-commit run gitleaks --all-files
pre-commit run semgrep --all-files
```

## Update hook versions

```bash
pre-commit autoupdate
```

Review the resulting diff carefully before committing; some hooks
change rule defaults between minor releases.

## Skipping a hook (rare, must be justified)

```bash
SKIP=ruff git commit -m "..."
```

Document every skip in the PR description. Routine skipping signals a
mistuned hook; fix the config or the rule rather than the workflow.

## CI parity

The CI templates under [../ci-templates/](../ci-templates/) run the
same scanners with the same configuration. If pre-commit passes but CI
fails (or vice versa), check version pins first: a divergent rev between
local and CI is the usual cause.

## References

- pre-commit: <https://pre-commit.com/>
- pre-commit hooks index: <https://pre-commit.com/hooks.html>
- OWASP DevSecOps Guideline: <https://owasp.org/www-project-devsecops-guideline/>
