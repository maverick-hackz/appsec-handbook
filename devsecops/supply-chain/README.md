# Supply Chain Security

Inventory, integrity, and provenance for software artifacts -- from
source through build to deployment.

## Files

- [sbom-generation.md](sbom-generation.md) -- generating CycloneDX and SPDX SBOMs with Syft
- [dependency-pinning.md](dependency-pinning.md) -- lockfiles, hash-pinning, Renovate / Dependabot
- [slsa-levels.md](slsa-levels.md) -- SLSA v1.0 levels and how to reach each

## Operational summary

| Activity | When | Tool examples |
| --- | --- | --- |
| Generate SBOM | per build | Syft, `npm sbom`, cdxgen, Microsoft sbom-tool |
| Store SBOM | per release | OCI artifact alongside image, OWASP Dependency-Track |
| Vulnerability match | continuous (against SBOM) | Grype, Trivy SBOM scan, Dependency-Track |
| Sign artifact | per build | cosign (Sigstore), GPG (legacy) |
| Attest provenance | per build | SLSA + in-toto, cosign attest |
| Verify at admission | per deployment | cosign verify, slsa-verifier, Kyverno cosign rule |
| Pin dependencies | continuously enforced | lockfiles, hash-pinning, Renovate / Dependabot |

## Threat model

What this set of controls mitigates:

| Threat | Mitigation |
| --- | --- |
| Compromised upstream package (npm typosquat, malicious update) | SCA + pinned versions + provenance verification |
| Tampered artifact between build and registry | Signing + verification at admission |
| Unknown component in production | SBOM inventory + continuous CVE matching |
| Insider modifies build to inject a backdoor | Two-person review on build pipeline; reproducible builds; SLSA Level 3 |
| Build server compromise | SLSA Level 3 (hosted, isolated, single-tenant builder) |
| Tag mutation in the registry | Deploy by digest; admission requires the signed digest, not the tag |

## What this section is NOT

- A CSPM / cloud-posture guide. Those controls live at the cloud
  provider, not in the artifact lifecycle.
- An SCA tool selection guide (see [../tool-categories.md](../tool-categories.md))
  or evaluation methodology (see [../../tooling-evaluation/](../../tooling-evaluation/)).

## References

- SLSA: <https://slsa.dev/spec/>
- Sigstore: <https://docs.sigstore.dev/>
- CycloneDX: <https://cyclonedx.org/>
- SPDX: <https://spdx.dev/>
- OWASP CycloneDX BOM Standard: <https://owasp.org/www-project-cyclonedx/>
- NIST SP 800-161 Rev 1 (Cyber Supply Chain Risk Management): <https://csrc.nist.gov/Projects/cyber-supply-chain-risk-management>
- Executive Order 14028 -- Software Supply Chain Security: <https://www.cisa.gov/securebydesign>
