# Mapping Matrix

A single-row-per-control crosswalk between this handbook and the
major frameworks. Use it to answer "for control X, what does ASVS
say, what does SAMM say, where in the handbook is the detail."

## Authentication and identity

| Handbook section | OWASP Top 10 (2025) | OWASP API Top 10 (2023) | ASVS 5.0 | SAMM v2 practice | NIST SSDF v1.1 | CWE |
| --- | --- | --- | --- | --- | --- | --- |
| [secure-coding/authentication.md](../secure-coding/authentication.md) | A07:2025 Authentication Failures | API2:2023 Broken Authentication | V6 Authentication; V9 Tokens | Design / Security Requirements | PW.1.1 | CWE-287, CWE-306, CWE-521 |
| [secure-coding/session-management.md](../secure-coding/session-management.md) | A07:2025 | API2:2023 | V7 Session management | Design / Security Requirements | PW.1.1 | CWE-384, CWE-613, CWE-352 |

## Authorization

| Handbook section | OWASP Top 10 (2025) | OWASP API Top 10 (2023) | ASVS 5.0 | SAMM v2 practice | NIST SSDF v1.1 | CWE |
| --- | --- | --- | --- | --- | --- | --- |
| [secure-coding/authorization.md](../secure-coding/authorization.md) | A01:2025 Broken Access Control | API1, API3, API5 | V8 Authorization | Design / Security Architecture | PW.1.1, PW.5.1 | CWE-862, CWE-863, CWE-285, CWE-639 |

## Input handling and output encoding

| Handbook section | OWASP Top 10 (2025) | ASVS 5.0 | SAMM v2 practice | NIST SSDF v1.1 | CWE |
| --- | --- | --- | --- | --- | --- |
| [secure-coding/input-validation.md](../secure-coding/input-validation.md) | A05:2025 Injection | V1, V2 | Verification / Security Testing | PW.5.1 | CWE-20 |
| [secure-coding/output-encoding.md](../secure-coding/output-encoding.md) | A05:2025 Injection | V1 | Verification / Security Testing | PW.5.1 | CWE-79, CWE-89, CWE-78, CWE-94 |
| [secure-coding/deserialization.md](../secure-coding/deserialization.md) | A08:2025 Software or Data Integrity Failures | V1, V4 | Verification / Security Testing | PW.5.1 | CWE-502 |

## Cryptography

| Handbook section | OWASP Top 10 (2025) | ASVS 5.0 | SAMM v2 practice | NIST SSDF v1.1 | CWE |
| --- | --- | --- | --- | --- | --- |
| [secure-coding/crypto-do-and-dont.md](../secure-coding/crypto-do-and-dont.md) | A04:2025 Cryptographic Failures | V11 Cryptography; V12 Communications | Design / Security Architecture | PW.5.1 | CWE-326, CWE-327, CWE-328, CWE-338 |
| [architecture/crypto-cheatsheet.md](../architecture/crypto-cheatsheet.md) | A04:2025 | V11, V12 | Design / Security Architecture | PW.1.1 | CWE-326, CWE-327 |
| [architecture/secrets-management.md](../architecture/secrets-management.md) | A04:2025; A02:2025 | V13 Configuration | Operations / Environment Management | PS.2.1, PW.5.1 | CWE-798, CWE-312, CWE-260 |
| [secure-coding/secrets-handling.md](../secure-coding/secrets-handling.md) | A04:2025; A02:2025 | V13 | Implementation / Secure Deployment | PS.2.1 | CWE-798, CWE-312 |

## Logging and error handling

| Handbook section | OWASP Top 10 (2025) | ASVS 5.0 | SAMM v2 practice | NIST SSDF v1.1 | CWE |
| --- | --- | --- | --- | --- | --- |
| [secure-coding/error-handling-logging.md](../secure-coding/error-handling-logging.md) | A09:2025 Security Logging and Alerting Failures; A10:2025 Mishandling of Exceptional Conditions | V14 | Operations / Incident Management | RV.1.1, RV.1.3 | CWE-209, CWE-532, CWE-117 |

## Threat modeling and architecture

| Handbook section | OWASP Top 10 (2025) | ASVS 5.0 | SAMM v2 practice | NIST SSDF v1.1 | CWE |
| --- | --- | --- | --- | --- | --- |
| [threat-modeling/methodology.md](../threat-modeling/methodology.md) | A06:2025 Insecure Design | (cross-cutting) | Design / Threat Assessment | PW.1.2 | (cross-cutting) |
| [architecture/zero-trust-principles.md](../architecture/zero-trust-principles.md) | A01:2025; A02:2025 | (cross-cutting) | Design / Security Architecture | PO.5.1, PW.1.1 | CWE-284 |

## Supply chain and SDLC

| Handbook section | OWASP Top 10 (2025) | OWASP CI/CD Top 10 | ASVS 5.0 | SAMM v2 practice | NIST SSDF v1.1 | CWE |
| --- | --- | --- | --- | --- | --- | --- |
| [devsecops/supply-chain/sbom-generation.md](../devsecops/supply-chain/sbom-generation.md) | A03:2025 Software Supply Chain Failures | CICD-SEC-3, CICD-SEC-9 | V13 | Implementation / Secure Build | PS.3.2 | CWE-829, CWE-1357 |
| [devsecops/supply-chain/dependency-pinning.md](../devsecops/supply-chain/dependency-pinning.md) | A03:2025 | CICD-SEC-3 | V13 | Implementation / Secure Build | PW.4.4 | CWE-829, CWE-494 |
| [devsecops/supply-chain/slsa-levels.md](../devsecops/supply-chain/slsa-levels.md) | A08:2025; A03:2025 | CICD-SEC-9 | V13 | Implementation / Secure Build | PS.2.1, PS.3.1 | CWE-1357 |
| [secure-sdlc/security-requirements-template.md](../secure-sdlc/security-requirements-template.md) | (cross-cutting) | (cross-cutting) | (cross-cutting) | Governance / Strategy and Metrics | PO.1.1 | (cross-cutting) |
| [secure-sdlc/code-review-checklist.md](../secure-sdlc/code-review-checklist.md) | (cross-cutting) | (cross-cutting) | (cross-cutting) | Verification / Security Testing | PW.7.1, PW.7.2 | (cross-cutting) |
| [secure-sdlc/security-gates-by-stage.md](../secure-sdlc/security-gates-by-stage.md) | (cross-cutting) | (cross-cutting) | (cross-cutting) | Implementation / Secure Deployment | PO.4.1 | (cross-cutting) |
| [secure-sdlc/vulnerability-disclosure-policy-template.md](../secure-sdlc/vulnerability-disclosure-policy-template.md) | (cross-cutting) | (cross-cutting) | (cross-cutting) | Operations / Incident Management | RV.1.2 | (cross-cutting) |

## Web frontend / API specifics

| Handbook section | OWASP Top 10 (2025) | OWASP API Top 10 (2023) | ASVS 5.0 | NIST SSDF v1.1 | CWE |
| --- | --- | --- | --- | --- | --- |
| [secure-coding/javascript-typescript/xss-react-vue.md](../secure-coding/javascript-typescript/xss-react-vue.md) | A05:2025 | (cross-cutting) | V1 | PW.5.1 | CWE-79 |
| [secure-coding/javascript-typescript/prototype-pollution.md](../secure-coding/javascript-typescript/prototype-pollution.md) | A05:2025; A02:2025 | API8:2023 | V1 | PW.5.1 | CWE-1321 |
| [secure-coding/javascript-typescript/jwt-handling.md](../secure-coding/javascript-typescript/jwt-handling.md) | A02:2025; A07:2025 | API2:2023 | V9 | PW.5.1 | CWE-347, CWE-321 |
| [secure-coding/javascript-typescript/nosql-injection.md](../secure-coding/javascript-typescript/nosql-injection.md) | A05:2025 | API8:2023 | V1 | PW.5.1 | CWE-943 |
| [secure-coding/javascript-typescript/node-supply-chain.md](../secure-coding/javascript-typescript/node-supply-chain.md) | A03:2025 | (cross-cutting) | V13 | PW.4.4 | CWE-829 |

## How to use

- Pick a control row; the linked handbook section gives the detail.
- For audit / regulatory evidence: collect output of the controls
  per row, mapped against the regulatory citation.
- For gap analysis: ask "for each handbook row, do we have evidence
  in the last 90 days?". Rows without evidence are gaps.

## References

- OWASP ASVS: <https://owasp.org/www-project-application-security-verification-standard/>
- OWASP SAMM: <https://owaspsamm.org/>
- OWASP Top 10 (2025): <https://owasp.org/Top10/>
- OWASP API Security Top 10 (2023): <https://owasp.org/API-Security/editions/2023/en/0x00-header/>
- OWASP Top 10 CI/CD Security Risks: <https://owasp.org/www-project-top-10-ci-cd-security-risks/>
- NIST SSDF (SP 800-218 v1.1): <https://csrc.nist.gov/Projects/ssdf>
- CWE: <https://cwe.mitre.org/>
