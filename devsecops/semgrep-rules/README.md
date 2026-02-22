# Custom Semgrep Rules

Project-specific Semgrep rules. Each rule lives in `<name>.yml` with a
matching `<name>.test.yaml` documenting positive and negative cases.
Combine with public rulesets (`p/owasp-top-ten`, `p/cwe-top-25`) in CI.

## Rules

| Rule | Languages | CWE | Detail |
| --- | --- | --- | --- |
| [hardcoded-jwt-secret](hardcoded-jwt-secret.yml) | py, js, ts, go, java | CWE-798 | Hardcoded JWT signing secret |
| [python-unsafe-yaml-load](python-unsafe-yaml-load.yml) | python | CWE-502 | `yaml.load` without a safe loader |
| [python-eval-exec](python-eval-exec.yml) | python | CWE-94 | `eval` / `exec` call |
| [go-sql-string-concat](go-sql-string-concat.yml) | go | CWE-89 | Concatenated SQL into `db.Query` / `db.Exec` |
| [js-disabled-tls-verification](js-disabled-tls-verification.yml) | js, ts | CWE-295 | `rejectUnauthorized: false` or equivalent |

## Run against the codebase

```bash
# Validate the rule syntax
semgrep --config devsecops/semgrep-rules/ --validate

# Scan the repository with the local rules
semgrep --config devsecops/semgrep-rules/ .

# Scan with public rulesets + local rules
semgrep --config p/owasp-top-ten \
        --config p/cwe-top-25 \
        --config devsecops/semgrep-rules/ \
        --error \
        .
```

## Writing tests

Semgrep's `--test` looks for language-specific files next to the rule
file, with inline annotations on each line:

- `# ruleid: <rule-id>` (Python / Go), `// ruleid: <rule-id>` (JS / Java) -- expected match
- `# ok: <rule-id>` -- expected non-match

Example layout for a Python rule:

```text
semgrep-rules/
├── python-eval-exec.yml
├── python-eval-exec.test.yaml      # this YAML, human-readable cases
└── python-eval-exec.py             # actual Semgrep test fixtures
```

The `.test.yaml` files in this directory document positive and
negative cases in a copy-pasteable form. To run `semgrep --test`,
materialise the cases into language files alongside the rule:

```bash
semgrep --config devsecops/semgrep-rules/ --test devsecops/semgrep-rules/
```

## Adding a new rule

1. Create `<rule-id>.yml` following the structure of an existing rule.
   Required `metadata` keys: `cwe`, `owasp` (if applicable),
   `confidence` (HIGH | MEDIUM | LOW), `category: security`.
2. Set `severity` to ERROR for findings that must block, WARNING for
   informational.
3. Document positive and negative cases in `<rule-id>.test.yaml`.
4. Run `semgrep --config devsecops/semgrep-rules/ --validate` and
   add at least one test fixture in the appropriate language.

## References

- Semgrep documentation: <https://semgrep.dev/docs/>
- Writing rules: <https://semgrep.dev/docs/writing-rules/overview/>
- Semgrep registry (public rulesets): <https://semgrep.dev/explore>
- OWASP Top 10: <https://owasp.org/Top10/>
- MITRE CWE: <https://cwe.mitre.org/>
