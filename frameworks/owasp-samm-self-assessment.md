# OWASP SAMM v2 Self-Assessment

OWASP SAMM (Software Assurance Maturity Model) measures a software
security programme's maturity along 5 business functions, each with
3 security practices, each with 3 maturity streams (A, B, C) at 3
levels.

## Scoring

| Level | Definition |
| --- | --- |
| 0 | Practice not in place |
| 1 | Initial: ad-hoc and inconsistent |
| 2 | Defined: documented and applied consistently across teams |
| 3 | Optimised: measured, continuously improved, automated where possible |

For each cell, score 0-3 with one short evidence line.

## Self-assessment grid

### Governance

| Practice | Stream A | Stream B | Stream C |
| --- | --- | --- | --- |
| Strategy and Metrics | Build and maintain a strategic plan | Establish measurable goals | Manage program operationally |
| Policy and Compliance | Identify policy framework | Apply policy to operations | Continuously audit and govern |
| Education and Guidance | Provide training | Build culture and skill | Maintain expert capability |

### Design

| Practice | Stream A | Stream B | Stream C |
| --- | --- | --- | --- |
| Threat Assessment | Application risk profile | Threat modelling | Threat-modelling automation |
| Security Requirements | Software requirements | Supplier security | Risk-driven requirements |
| Security Architecture | Architecture design | Technology management | Reference architectures |

### Implementation

| Practice | Stream A | Stream B | Stream C |
| --- | --- | --- | --- |
| Secure Build | Build process | Software dependencies | Build hardening |
| Secure Deployment | Deployment process | Secret management | Deployment integrity |
| Defect Management | Defect tracking | Metrics and feedback | Process integration |

### Verification

| Practice | Stream A | Stream B | Stream C |
| --- | --- | --- | --- |
| Architecture Assessment | Architecture validation | Architecture mitigation | Scalable baseline |
| Requirements-driven Testing | Control verification | Misuse / abuse testing | Continuous verification |
| Security Testing | Scalable baseline | Deep understanding | Continuous improvement |

### Operations

| Practice | Stream A | Stream B | Stream C |
| --- | --- | --- | --- |
| Incident Management | Incident detection | Incident response | Incident analysis |
| Environment Management | Configuration hardening | Patch and update | Configuration monitoring |
| Operational Management | Data protection | System decommissioning | Legacy management |

## Filling the grid

For each cell, score 0-3 plus one evidence note. Example fragment:

| Cell | Score | Evidence |
| --- | --- | --- |
| Threat Assessment / Stream A (application risk profile) | 2 | Risk classification documented in product-spec template; applied since 2024-09 |
| Secure Build / Stream B (software dependencies) | 3 | Renovate + SCA + SBOM + cosign signing on every build; verified by admission |
| Secure Deployment / Stream B (secret management) | 2 | Vault for prod; legacy services still read from .env in two namespaces (ticket APPSEC-412) |
| Defect Management / Stream B (metrics and feedback) | 1 | Counts dashboard exists; not yet reviewed in a recurring forum |

## Roll-up

Aggregate per practice: mean of the three streams. Aggregate per
business function: mean of the three practices. The single number
is less useful than the cell-by-cell view; report both.

## Rolling out

- Year 1: target maturity 1 across the board; close obvious gaps.
- Year 2: targeted 2 in Design / Implementation / Verification.
- Year 3+: pursue 3 where the cost is justified by the asset risk.

Not every cell needs to reach 3. A regulated-data product may need 3
on Threat Assessment and Security Architecture; a low-blast-radius
internal tool can sit at 1 on most cells indefinitely.

## How this relates to ASVS

ASVS verifies application controls at a specific instant. SAMM
measures the programme that produces and maintains those controls.
A team at SAMM 1 across the board likely cannot consistently pass
ASVS L2 on all its applications; conversely, a team at SAMM 3 will
produce L2 / L3-compliant applications by default.

## References

- OWASP SAMM v2: <https://owaspsamm.org/>
- SAMM Toolbox (spreadsheet self-assessment): <https://owaspsamm.org/about/>
- BSIMM (alternative maturity model): <https://www.bsimm.com/>
