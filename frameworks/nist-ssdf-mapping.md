# NIST SSDF (SP 800-218 v1.1) Mapping

The Secure Software Development Framework (SSDF) organises secure
development practices into four groups:

- **PO** -- Prepare the Organization
- **PS** -- Protect the Software
- **PW** -- Produce Well-Secured Software
- **RV** -- Respond to Vulnerabilities

Each practice has tasks (e.g., `PW.4.4`). The table below maps each
task to the handbook section that operationalises it.

## PO -- Prepare the Organization

| Task | Practice | Handbook reference |
| --- | --- | --- |
| PO.1.1 | Define security requirements for software development | [../secure-sdlc/security-requirements-template.md](../secure-sdlc/security-requirements-template.md) |
| PO.1.2 | Implement roles and responsibilities | [../secure-sdlc/security-champions-program.md](../secure-sdlc/security-champions-program.md) |
| PO.1.3 | Provide training and education | [../secure-sdlc/security-champions-program.md](../secure-sdlc/security-champions-program.md) |
| PO.2.1 | Maintain toolchains | [../devsecops/](../devsecops/) |
| PO.2.2 | Track third-party software components | [../devsecops/supply-chain/](../devsecops/supply-chain/) |
| PO.3.1 | Implement supporting toolchains | [../devsecops/ci-templates/](../devsecops/ci-templates/) |
| PO.4.1 | Define criteria for software security | [../secure-sdlc/security-gates-by-stage.md](../secure-sdlc/security-gates-by-stage.md) |
| PO.5.1 | Implement and maintain secure environments | [../architecture/zero-trust-principles.md](../architecture/zero-trust-principles.md) |

## PS -- Protect the Software

| Task | Practice | Handbook reference |
| --- | --- | --- |
| PS.1.1 | Protect all forms of code | Branch protection; CODEOWNERS; SSO + MFA on source host |
| PS.2.1 | Verify the integrity of software releases | [../devsecops/supply-chain/slsa-levels.md](../devsecops/supply-chain/slsa-levels.md); cosign signing |
| PS.3.1 | Archive provenance data for each release | [../devsecops/supply-chain/sbom-generation.md](../devsecops/supply-chain/sbom-generation.md); cosign attest |
| PS.3.2 | Generate SBOM for each release | [../devsecops/supply-chain/sbom-generation.md](../devsecops/supply-chain/sbom-generation.md) |

## PW -- Produce Well-Secured Software

| Task | Practice | Handbook reference |
| --- | --- | --- |
| PW.1.1 | Design software to meet security requirements | [../threat-modeling/](../threat-modeling/); [../architecture/](../architecture/) |
| PW.1.2 | Perform threat modeling on the design | [../threat-modeling/methodology.md](../threat-modeling/methodology.md) |
| PW.1.3 | Reuse vetted software components | [../secure-sdlc/third-party-software-intake.md](../secure-sdlc/third-party-software-intake.md) |
| PW.2.1 | Use forms of risk modeling | [../threat-modeling/templates/attack-tree-template.md](../threat-modeling/templates/attack-tree-template.md) |
| PW.4.1 | Use secure design principles | [../architecture/](../architecture/) |
| PW.4.4 | Use vetted and approved components | SCA in CI; [../devsecops/supply-chain/dependency-pinning.md](../devsecops/supply-chain/dependency-pinning.md) |
| PW.5.1 | Adhere to secure coding practices | [../secure-coding/](../secure-coding/) |
| PW.6.1 | Configure compilation, interpretation, and build processes securely | [../devsecops/dockerfile-hardening.md](../devsecops/dockerfile-hardening.md); SAST in CI |
| PW.6.2 | Use compiler / interpreter / build hardening features | language-specific compiler flags; `-O2 -Wall`, `--strict`, `-fstack-protector-strong` |
| PW.7.1 | Determine whether code review meets criteria | [../secure-sdlc/code-review-checklist.md](../secure-sdlc/code-review-checklist.md) |
| PW.7.2 | Review and analyze code for vulnerabilities | SAST (Semgrep, CodeQL); [../devsecops/semgrep-rules/](../devsecops/semgrep-rules/) |
| PW.8.1 | Determine whether testing meets criteria | [../secure-sdlc/definition-of-done-security.md](../secure-sdlc/definition-of-done-security.md) |
| PW.8.2 | Use security testing | SAST + SCA + DAST + secret scan in CI |
| PW.9.1 | Configure software securely by default | [../secure-coding/java/spring-security-defaults.md](../secure-coding/java/spring-security-defaults.md); [../secure-coding/python/django-flask-defaults.md](../secure-coding/python/django-flask-defaults.md) |

## RV -- Respond to Vulnerabilities

| Task | Practice | Handbook reference |
| --- | --- | --- |
| RV.1.1 | Gather information about potential vulnerabilities | SBOM ingestion to Dependency-Track; CVE / EPSS / KEV monitoring |
| RV.1.2 | Provide a means for receiving vulnerability reports | [../secure-sdlc/vulnerability-disclosure-policy-template.md](../secure-sdlc/vulnerability-disclosure-policy-template.md) |
| RV.1.3 | Analyze each vulnerability | Severity triage; CVSS scoring; reachability analysis |
| RV.2.1 | Plan response to each vulnerability | Owner + target date per finding; integration with backlog |
| RV.2.2 | Develop and release vulnerability fixes | Hot-patch process; semantic-version policy |
| RV.3.1 | Analyze vulnerabilities to identify root causes | Post-mortem on each high-severity issue |
| RV.3.2 | Analyze the root causes for vulnerability patterns | Trend analysis per CWE class; quarterly review |
| RV.3.3 | Review the SDLC for opportunities to address | Feed back into the requirements template and code review checklist |
| RV.3.4 | Identify and implement mitigation for unfixable vulnerabilities | Compensating control plus disclosure |

## Audit posture

A team using this handbook can satisfy SSDF v1.1 by:

1. Pointing every task in the mapping above to a handbook artefact.
2. Producing evidence per task (signed SBOM, CI run, test report).
3. Reviewing the mapping yearly against the latest SSDF revision.

## References

- NIST SP 800-218 (SSDF v1.1): <https://csrc.nist.gov/Projects/ssdf>
- SSDF practices and tasks: <https://nvlpubs.nist.gov/nistpubs/SpecialPublications/NIST.SP.800-218.pdf>
- NIST Cybersecurity Framework: <https://www.nist.gov/cyberframework>
