# Node.js Supply Chain

## Threat

The npm ecosystem is the largest in any language; the dependency tree
of a small Express app commonly exceeds a thousand packages. Each is a
candidate for typosquatting, account takeover, malicious post-install
scripts, dependency confusion, and pinning rot. The author's own
package is usually a small share of the risk surface.

CWE: CWE-829 (Inclusion of Functionality from Untrusted Control Sphere),
CWE-1357 (Insufficient Verification of Source Authenticity), CWE-494
(Download of Code Without Integrity Check). OWASP: A06:2021
(Vulnerable and Outdated Components), A08:2021 (Software and Data
Integrity Failures).

## Insecure baseline

- `package.json` uses caret ranges (`"express": "^4.18.0"`) and no
  lockfile, so each `npm install` resolves differently.
- `npm install --production` in the container build pulls dev
  dependencies' transitive code at install time via post-install
  scripts.
- CI runs against the public registry directly, with no allowlist of
  scopes and no offline cache.
- No SBOM, no SCA scan in PRs.

## Why it fails

- Without `package-lock.json`, transitive versions float; a malicious
  update to a deep dependency lands in the next deploy.
- Post-install scripts execute with the privileges of the npm process,
  often the build agent. Typosquatted packages run code as soon as
  they are installed.
- Dependency confusion: a public package with the same name as a
  private internal one (and a higher version) is preferred by npm
  unless the registry resolution is scoped.

## Secure baseline

- Commit `package-lock.json` (or `pnpm-lock.yaml` / `yarn.lock`).
  Treat lockfile changes as code review-able.
- Install with `npm ci` in CI: refuses to run if `package-lock.json`
  is out of sync with `package.json`; installs deterministically.
- Disable lifecycle scripts by default during install where possible:

```bash
npm config set ignore-scripts true
# Or, project-scoped, in .npmrc:
echo "ignore-scripts=true" >> .npmrc
```

  Re-enable per package only when audited (`npm install foo --ignore-scripts=false`).

- Pin to a specific registry and use scoped packages for internal code:

```text
# .npmrc
registry=https://registry.internal.example.com
@my-org:registry=https://registry.internal.example.com
always-auth=true
```

- Run `npm audit` (or `pnpm audit`, `yarn audit`) and a stronger SCA
  scanner (Trivy, Snyk, OSV-Scanner) in PR CI; fail on CRITICAL/HIGH.
  See [../../devsecops/ci-templates/github-actions/sca-trivy-fs.yml](../../devsecops/ci-templates/github-actions/sca-trivy-fs.yml).

- Generate an SBOM (CycloneDX or SPDX) per build and store it with the
  image; tools: `npm sbom` (recent npm), `syft`, `cyclonedx-npm`. See
  [../../devsecops/supply-chain/sbom-generation.md](../../devsecops/supply-chain/sbom-generation.md).

- Verify package provenance where publishers participate (npm
  provenance attestations via Sigstore); pin known-good versions for
  critical dependencies (`express`, `pino`, `dotenv`).
  <!-- TODO: confirm npm provenance verification CLI flags against the current npm docs -->

- Automate dependency updates with Renovate / Dependabot; group safe
  patches, separate-PR major bumps, require CI green before merge.

## Notes

- For build-time secrets (npm tokens), use OIDC-backed short-lived
  credentials in CI rather than long-lived `NPM_TOKEN` environment
  variables.
- Avoid `npx <package>` against untrusted networks; it fetches and
  runs the latest version with no review. Pin via `npx -p foo@1.2.3 foo`.
- Container images: install dependencies in a build stage with
  `--ignore-scripts` and copy only `node_modules/` plus the bundle to
  a distroless runtime stage; see [../../devsecops/dockerfile-hardening.md](../../devsecops/dockerfile-hardening.md).
- Browser bundles: subresource integrity (SRI) for CDN-served scripts;
  prefer self-hosting bundles with content-addressed names.

## References

- OWASP A06:2021 (Vulnerable and Outdated Components): <https://owasp.org/Top10/A06_2021-Vulnerable_and_Outdated_Components/>
- OWASP CycloneDX: <https://cyclonedx.org/>
- npm — Provenance overview: <https://docs.npmjs.com/generating-provenance-statements>
- SLSA: <https://slsa.dev/>
- Sigstore: <https://docs.sigstore.dev/>
- OSV-Scanner: <https://github.com/google/osv-scanner>
