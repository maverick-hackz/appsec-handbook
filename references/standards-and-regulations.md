# Standards and Regulations

Frameworks, standards, and statutes commonly referenced in AppSec
programs, with scope and authority.

## International standards (ISO / IEC)

- **ISO/IEC 27001:2022** -- Information security management systems
  (ISMS). Defines requirements for an ISMS; the controls catalogue
  sits in ISO/IEC 27002.
- **ISO/IEC 27002:2022** -- Information security controls. Reference
  catalogue used to populate the ISMS Statement of Applicability.
- **ISO/IEC 27017** -- Cloud-service-specific controls extending
  27002.
- **ISO/IEC 27018** -- PII protection for public cloud processors.
- **ISO/IEC 27034** -- Application security guidelines.
- **ISO/IEC 27036** -- Supplier relationships, supply-chain security.
- **ISO/IEC 29147:2018** -- Vulnerability disclosure (receiving and
  publishing).
- **ISO/IEC 30111:2019** -- Vulnerability handling processes.

## NIST publications

- **NIST Cybersecurity Framework (CSF) 2.0** -- High-level framework
  (Govern, Identify, Protect, Detect, Respond, Recover).
- **NIST SP 800-53 Rev 5** -- Catalogue of security and privacy
  controls; the long-form complement to ISO 27002.
- **NIST SP 800-63B** -- Digital identity authenticator requirements.
- **NIST SP 800-63C** -- Federation and assertions.
- **NIST SP 800-92** -- Computer security log management.
- **NIST SP 800-145** -- Cloud computing definitions.
- **NIST SP 800-161 Rev 1** -- Cyber supply-chain risk management.
- **NIST SP 800-190** -- Application container security.
- **NIST SP 800-207** -- Zero Trust Architecture.
- **NIST SP 800-218 v1.1** -- Secure Software Development Framework
  (SSDF).

## OWASP standards

- **OWASP ASVS 5.0** -- Application Security Verification Standard.
- **OWASP MASVS** -- Mobile App Security Verification Standard.
- **OWASP SAMM 2.0** -- Software Assurance Maturity Model.
- **OWASP Top 10 (2025)** -- Top web-application risk categories.
- **OWASP API Security Top 10 (2023)** -- API-specific risks.
- **OWASP Top 10 for LLM Applications (2025)** -- Risks for
  applications that include LLMs.
- **OWASP Top 10 CI/CD Security Risks** -- Pipeline and supply-chain
  risks.
- **OWASP SCVS** -- Software Component Verification Standard.

## Regulatory regimes (selected)

Each item lists scope and what AppSec teams generally need to do.

- **GDPR (EU 2016/679)** -- Personal data of EU data subjects.
  AppSec scope: data minimization, purpose limitation, breach
  notification (72 hours), Article 32 ("appropriate technical and
  organisational measures"), data-subject rights.
- **HIPAA (US, 45 CFR Parts 160 / 164)** -- Protected health
  information. AppSec scope: Security Rule (administrative,
  physical, technical safeguards), Breach Notification Rule.
- **NIS2 Directive (EU 2022/2555)** -- Cybersecurity of essential and
  important entities across the EU. AppSec scope: risk management,
  incident reporting (24h / 72h), supply-chain security.
- **Cyber Resilience Act (EU 2024/2847)** -- Cybersecurity
  requirements for products with digital elements. AppSec scope:
  secure-by-default, SBOM, vulnerability handling over the product
  lifecycle.
- **DORA (EU 2022/2554)** -- Digital Operational Resilience Act,
  financial-services sector. AppSec scope: ICT risk management,
  third-party risk, threat-led penetration testing.
- **SOX (US Sarbanes-Oxley, 2002)** -- Financial reporting integrity.
  AppSec scope: change management, separation of duties, audit log.
- **LGPD (Brazil)** -- Personal data of Brazilian residents.
  Structurally similar to GDPR.
- **PIPL (China)** -- Personal Information Protection Law.
- **PIPEDA (Canada)** -- Personal Information Protection and
  Electronic Documents Act.

## Compliance audit frameworks

- **SOC 2 Type II** (AICPA) -- Trust Services Criteria
  (Security, Availability, Processing Integrity, Confidentiality,
  Privacy). Service-organisation audits.
- **ISO/IEC 27001** -- Certification of an ISMS against the standard.
- **FedRAMP** (US federal cloud services) -- NIST 800-53 controls
  authorisation for cloud service providers.

## Supply chain frameworks

- **SLSA** -- Supply-chain Levels for Software Artifacts. See
  [../devsecops/supply-chain/slsa-levels.md](../devsecops/supply-chain/slsa-levels.md).
- **in-toto** -- Attestation framework for software supply chains.
- **CycloneDX** -- OWASP SBOM standard.
- **SPDX** -- Linux Foundation SBOM standard (ISO/IEC 5962).

## What to do with this list

- Identify which standards apply to the product (regulatory
  jurisdiction, customer requirements, certification target).
- Map standard-level controls to the handbook's per-section
  artefacts via the [../frameworks/mapping-matrix.md](../frameworks/mapping-matrix.md).
- Track standard versions; each is revised periodically. NIST
  publications carry a revision number; ISO standards carry the
  year of revision.

## References

- NIST publications: <https://csrc.nist.gov/publications>
- OWASP projects index: <https://owasp.org/projects/>
- ISO catalogue: <https://www.iso.org/standards-catalogue/browse-by-tc.html>
- EUR-Lex (EU legislation): <https://eur-lex.europa.eu/>
- CISA -- standards and best practices: <https://www.cisa.gov/news-events/cybersecurity-advisories>
