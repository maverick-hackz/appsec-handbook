# SBOM Generation

A Software Bill of Materials (SBOM) is a machine-readable inventory of
components in a piece of software. The two widely adopted formats are
CycloneDX (OWASP, vendor-neutral) and SPDX (Linux Foundation,
license-focused). Generate one per build, ship it with the artifact,
and ingest it into a continuous CVE-matching tool.

## Formats

| Format | Maintainer | Strength |
| --- | --- | --- |
| CycloneDX | OWASP | Vulnerability and risk metadata; broad tool support |
| SPDX | Linux Foundation | License and provenance; mature ecosystem |

Most modern toolchains can emit both. CycloneDX is the default in this
handbook; emit SPDX if a downstream consumer requires it.

## Syft (multi-source SBOM generator)

```bash
# From a directory (source tree)
syft scan dir:./ -o cyclonedx-json=sbom.cdx.json

# From a Docker image (after pulling or via registry pull)
syft scan ghcr.io/myorg/svc@sha256:<digest> -o cyclonedx-json=sbom.cdx.json

# From a container image archive
syft scan docker-archive:image.tar -o cyclonedx-json=sbom.cdx.json

# SPDX output if a downstream consumer requires it
syft scan ghcr.io/myorg/svc@sha256:<digest> -o spdx-json=sbom.spdx.json
```

Multi-format in one run:

```bash
syft scan ghcr.io/myorg/svc@sha256:<digest> \
  -o cyclonedx-json=sbom.cdx.json \
  -o spdx-json=sbom.spdx.json
```

## Language-native generators

| Ecosystem | Command |
| --- | --- |
| Node.js (npm 10+) | `npm sbom --sbom-format=cyclonedx --omit=dev > sbom.cdx.json` |
| Node.js (alt) | `npx @cyclonedx/cdxgen -o sbom.cdx.json` |
| Python (pip) | `cyclonedx-py environment -o sbom.cdx.json` |
| Java (Maven) | `mvn org.cyclonedx:cyclonedx-maven-plugin:makeAggregateBom` |
| Java (Gradle) | `gradle cyclonedxBom` |
| Go | `cyclonedx-gomod mod -output sbom.cdx.json` |
| .NET | `dotnet CycloneDX <project.csproj>` |

A language-native tool produces a higher-fidelity SBOM than a generic
filesystem scanner because it understands the dependency resolution
rules of its ecosystem. Use both -- language-native for completeness,
Syft for cross-language consolidation.

## CI integration

See [../ci-templates/github-actions/sbom-syft.yml](../ci-templates/github-actions/sbom-syft.yml)
for a filesystem-source SBOM workflow, and
[../ci-templates/github-actions/sign-cosign.yml](../ci-templates/github-actions/sign-cosign.yml)
for image-source SBOM with a cosign attestation that ships with the
image.

## Storage

- Per-build: GitHub release asset / GitLab job artifact, retention >= 90 days.
- Per-release artifact: cosign attestation attached to the image
  digest, so the SBOM travels with the image and is queryable via
  `cosign download attestation`.
- Per-organisation: OWASP Dependency-Track ingests every SBOM and
  continuously matches against new CVEs, EPSS, and KEV signals.

## Vulnerability matching against an SBOM

```bash
# Grype reads the SBOM (no need to re-discover components)
grype sbom:./sbom.cdx.json --output table --fail-on high

# Trivy can do the same
trivy sbom ./sbom.cdx.json --severity HIGH,CRITICAL --exit-code 1

# OWASP Dependency-Track (REST API ingestion)
curl -X POST -H "X-Api-Key: $DT_API_KEY" \
  -H "Content-Type: multipart/form-data" \
  -F "project=$DT_PROJECT_UUID" \
  -F "bom=@sbom.cdx.json" \
  https://dt.example.com/api/v1/bom
```

## VEX (Vulnerability Exploitability eXchange)

A CVE found in the SBOM is not necessarily exploitable in the deployed
configuration. VEX is the document format for asserting "this CVE
does NOT apply to this product because `<reason>`", reviewed and signed
by the producer.

Formats: OpenVEX, CycloneDX VEX, CSAF VEX (CISA).

Emit VEX statements at release time for known-non-exploitable CVEs in
the SBOM; consumers can suppress them automatically.

## What an SBOM does NOT do

- Catch first-party bugs. SBOMs are inventory of components; first-
  party code review and SAST cover the home-grown side.
- Indicate exploitability without VEX or reachability analysis. A
  CVE in a transitive dep that is never called is noise.
- Prove the SBOM matches reality without a signed attestation. Bind
  the SBOM to the artifact digest via cosign attest.

## References

- CycloneDX: <https://cyclonedx.org/>
- SPDX: <https://spdx.dev/>
- Syft: <https://github.com/anchore/syft>
- Grype: <https://github.com/anchore/grype>
- OWASP Dependency-Track: <https://dependencytrack.org/>
- OpenVEX: <https://github.com/openvex/spec>
- CSAF VEX: <https://www.csaf.io/>
- NIST SP 800-161 Rev 1: <https://csrc.nist.gov/Projects/cyber-supply-chain-risk-management>
- CISA SBOM resources: <https://www.cisa.gov/sbom>
