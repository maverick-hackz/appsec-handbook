# Dependency Pinning

Pinning prevents a transitive update from landing without review. The
mechanics differ per ecosystem, but the goal is the same: the build
should be reproducible from a fixed manifest.

## Levels of pinning

| Level | What it pins | Example |
| --- | --- | --- |
| Range | major / minor version | `^4.0.0` (any 4.x.y) |
| Exact version | specific semver | `4.18.2` |
| Lockfile (resolved tree) | every direct + transitive version | `package-lock.json`, `yarn.lock`, `Pipfile.lock`, `go.sum` |
| Hash-pinning | content digest of each artifact | `--require-hashes` pip, npm with `integrity:` lock entry |
| Vendored | source tree of every dep checked in | Go `vendor/`, npm `node_modules/` in CI cache |

The recommended minimum: exact versions + lockfile committed.
Hash-pinning adds defence against registry compromise.

## Per ecosystem

### npm / pnpm / yarn

```bash
# Install with locked versions (CI):
npm ci

# Update a single dep with full transitive resolution:
npm install lodash@4.17.21 --save-exact

# Audit:
npm audit --omit=dev
```

`package-lock.json` records each version + content hash
(`integrity:`); commit it and require it in CI (`npm ci` errors when
lockfile is out of sync).

For scoped private packages, set the registry in `.npmrc`:

```text
registry=https://registry.internal.example.com
@myorg:registry=https://registry.internal.example.com
always-auth=true
```

This avoids dependency confusion (public registry returning a
typosquatted package for a name that should resolve internally).

### pip

```bash
# Exact versions
pip install --require-hashes -r requirements.txt

# Generate hashes from a high-level requirements file with pip-tools:
pip-compile --generate-hashes --output-file=requirements.txt requirements.in

# pipenv equivalent: Pipfile.lock with hashes
pipenv install
pipenv lock --requirements > requirements.txt
```

`requirements.txt` after `pip-compile --generate-hashes`:

```text
lodash==4.17.21 \
    --hash=sha256:679591c6f17b1cc83ef82d... \
    --hash=sha256:b1d1afb9b2cf60feac0bb5...
```

Each install verifies the hash; a poisoned mirror or registry cannot
substitute a malicious artifact.

### Go modules

```bash
# go.mod + go.sum (committed)
go mod tidy
go mod verify
go mod download    # populates module cache; verifies against go.sum
```

`go.sum` contains the SHA-256 of every module version used.
`GOFLAGS=-mod=readonly` in CI rejects builds that need to add modules.

For air-gapped or extra-paranoid setups, `go mod vendor` stages the
sources in `vendor/`, committed, and `GOFLAGS=-mod=vendor` builds
without contacting any proxy.

### Maven / Gradle

```xml
<!-- Maven: lock plugin and dependency-check -->
<dependency>
  <groupId>org.apache.commons</groupId>
  <artifactId>commons-lang3</artifactId>
  <version>3.14.0</version>
</dependency>
```

Gradle has `dependencyLocking` (per-configuration lockfiles in
`gradle.lockfile`).

Pin the Maven Wrapper / Gradle Wrapper itself by checksum.

## Automated update tools

| Tool | Strengths |
| --- | --- |
| Renovate | Multi-ecosystem, fine-grained scheduling, grouping rules |
| Dependabot (GitHub-native) | Zero setup for GitHub repos, security-only PRs |
| RenovateBot self-hosted | Same as Renovate, no SaaS dependency |

A reasonable cadence:

- **Security advisories** -- merge same day for HIGH/CRITICAL; auto-merge
  patch versions of known-good dependencies.
- **Patch versions** -- weekly batch.
- **Minor versions** -- weekly batch with CI green required.
- **Major versions** -- per-PR, with manual review and a changelog
  read.

## Renovate config (extract)

```json
{
  "$schema": "https://docs.renovatebot.com/renovate-schema.json",
  "extends": [
    "config:recommended",
    ":semanticCommits"
  ],
  "lockFileMaintenance": { "enabled": true, "schedule": ["before 4am on Monday"] },
  "vulnerabilityAlerts": { "labels": ["security"], "automerge": false },
  "packageRules": [
    {
      "matchUpdateTypes": ["patch"],
      "automerge": true
    },
    {
      "matchUpdateTypes": ["major"],
      "automerge": false,
      "reviewers": ["security-team"]
    }
  ]
}
```

## Anti-patterns

- A repo with `^x.y.z` ranges and no lockfile. The next deploy gets a
  different transitive set than the previous one.
- Committing `node_modules` without a lockfile. Inflates the repo
  without giving reproducibility (you cannot tell which set was
  intentional).
- Disabling Renovate / Dependabot to "stay green". The updates
  arrive in production sooner or later; better to face them in PRs
  than via a CVE.
- Pinning to a tag in a third-party Action workflow without a
  `# pin-tag` comment so audit tools can verify the immutable SHA.

## References

- npm semantic versioning: <https://semver.npmjs.com/>
- pip Hash-checking mode: <https://pip.pypa.io/en/stable/topics/secure-installs/>
- Go modules reference: <https://go.dev/ref/mod>
- Renovate documentation: <https://docs.renovatebot.com/>
- Dependabot documentation: <https://docs.github.com/en/code-security/dependabot>
- OWASP Dependency-Check: <https://owasp.org/www-project-dependency-check/>
