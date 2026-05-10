# Glossary

Short definitions of AppSec / DevSecOps acronyms and terms used
throughout this handbook.

## A

- **ABAC** -- Attribute-Based Access Control. Authorization based on
  attributes of the subject, resource, environment, and action.
- **AEAD** -- Authenticated Encryption with Associated Data.
  Provides confidentiality and integrity in one primitive
  (AES-GCM, ChaCha20-Poly1305).
- **APPSEC** -- Application Security. The practice of finding and
  fixing security defects in software.
- **ASPM** -- Application Security Posture Management. Platform that
  aggregates, deduplicates, and prioritizes findings across security
  tools.
- **ASVS** -- OWASP Application Security Verification Standard.
  Verification requirements at three levels (L1, L2, L3).
- **AAL** -- Authenticator Assurance Level (NIST 800-63B). AAL1
  baseline, AAL2 with MFA, AAL3 phishing-resistant.

## B

- **BCP** -- Best Current Practice (IETF document type).
- **BFLA** -- Broken Function Level Authorization. OWASP API Top 10
  category for missing role checks on privileged endpoints.
- **BOLA** -- Broken Object Level Authorization. OWASP API Top 10
  category for missing per-object access checks.
- **BOPLA** -- Broken Object Property Level Authorization. OWASP API
  Top 10 category for mass-assignment and over-disclosure.
- **BSIMM** -- Building Security In Maturity Model. Synopsys-curated
  industry maturity benchmark.

## C

- **CSP** -- Content Security Policy. Browser-enforced policy
  limiting script / style / connection sources.
- **CSPM** -- Cloud Security Posture Management. Continuous
  evaluation of cloud-account configuration against best practices.
- **CSPRNG** -- Cryptographically Secure Pseudo-Random Number
  Generator.
- **CWE** -- Common Weakness Enumeration. MITRE catalogue of software
  weakness types.
- **CWPP** -- Cloud Workload Protection Platform. Runtime protection
  for cloud workloads (containers, VMs).
- **CVE** -- Common Vulnerabilities and Exposures. Specific
  vulnerability instances; identified by CVE-YYYY-NNNN.
- **CVSS** -- Common Vulnerability Scoring System. Severity score for
  a CVE (Base / Temporal / Environmental).

## D

- **DAST** -- Dynamic Application Security Testing. Scans a running
  application from the outside.
- **DLP** -- Data Loss Prevention.
- **DPA** -- Data Processing Agreement (GDPR contractual instrument).

## E

- **EPSS** -- Exploit Prediction Scoring System. Probability that a
  CVE will be exploited in the next 30 days.

## F

- **FIDO2 / WebAuthn** -- Phishing-resistant authentication standard
  using public-key cryptography.
- **FIPS** -- US Federal Information Processing Standards.

## H

- **HSTS** -- HTTP Strict Transport Security. Browser policy that
  forces HTTPS.

## I

- **IAM** -- Identity and Access Management.
- **IAST** -- Interactive Application Security Testing. Runtime
  agent in the test environment that combines SAST and DAST signals.
- **IdP** -- Identity Provider (SAML / OIDC issuer).
- **IDOR** -- Insecure Direct Object Reference. Older name for BOLA.
- **IMDS** -- Instance Metadata Service. Cloud metadata endpoint at
  `169.254.169.254`.

## J

- **JWT** -- JSON Web Token (RFC 7519). Signed token format used
  in OAuth / OIDC.
- **JWE** -- JSON Web Encryption (RFC 7516). Encrypted JWT variant.
- **JWS** -- JSON Web Signature (RFC 7515). Detached signature for
  JWT.

## K

- **KDF** -- Key Derivation Function. Argon2id / scrypt / bcrypt /
  PBKDF2 for password hashing.
- **KEK / DEK** -- Key Encryption Key / Data Encryption Key. Envelope
  encryption pattern: the DEK encrypts data; the KEK encrypts the
  DEK.
- **KEV** -- Known Exploited Vulnerabilities. CISA-maintained
  catalogue of CVEs known to be exploited in the wild.
- **KMS** -- Key Management Service. Cloud-managed key custody and
  use.

## L

- **LDAP** -- Lightweight Directory Access Protocol.
- **LLM** -- Large Language Model.

## M

- **MAST** -- Mobile Application Security Testing.
- **MASVS** -- OWASP Mobile Application Security Verification
  Standard.
- **MASTG** -- OWASP Mobile Application Security Testing Guide.
- **MFA** -- Multi-Factor Authentication.
- **mTLS** -- Mutual TLS. Both client and server present a
  certificate.

## N

- **NIST** -- National Institute of Standards and Technology (US).
- **NVD** -- National Vulnerability Database (NIST).

## O

- **OIDC** -- OpenID Connect. Identity layer on top of OAuth 2.0.
- **OAuth 2.0** -- Delegated authorization protocol (RFC 6749).
- **OPA** -- Open Policy Agent. General-purpose policy engine using
  Rego.

## P

- **PASTA** -- Process for Attack Simulation and Threat Analysis.
  Seven-stage risk-centric threat modeling methodology.
- **PEP / PDP / PAP / PIP** -- Policy Enforcement / Decision /
  Administration / Information Point. XACML / ABAC roles.
- **PII** -- Personally Identifiable Information.
- **PKCE** -- Proof Key for Code Exchange (RFC 7636). OAuth
  extension preventing authorization-code interception.
- **PoLP** -- Principle of Least Privilege.
- **PSA** -- Pod Security Admission (Kubernetes).

## R

- **RASP** -- Runtime Application Self-Protection. In-process agent
  that observes and blocks attacks.
- **RBAC** -- Role-Based Access Control.
- **ReBAC** -- Relationship-Based Access Control.
- **RFC** -- Request for Comments (IETF document type).
- **RPO / RTO** -- Recovery Point Objective / Recovery Time Objective.

## S

- **SAML** -- Security Assertion Markup Language (SSO protocol).
- **SAMM** -- OWASP Software Assurance Maturity Model.
- **SAST** -- Static Application Security Testing.
- **SBOM** -- Software Bill of Materials. CycloneDX / SPDX formats.
- **SCA** -- Software Composition Analysis. Scans dependencies for
  known CVEs.
- **SDLC** -- Software Development Lifecycle.
- **SIEM** -- Security Information and Event Management.
- **SLSA** -- Supply-chain Levels for Software Artifacts.
- **SOAR** -- Security Orchestration, Automation, and Response.
- **SP** -- Service Provider (SAML); Special Publication (NIST).
- **SPIFFE / SPIRE** -- Secure Production Identity Framework For
  Everyone (standard) and its reference implementation.
- **SSDF** -- NIST Secure Software Development Framework
  (SP 800-218).
- **SSO** -- Single Sign-On.
- **SSRF** -- Server-Side Request Forgery.
- **SSPM** -- SaaS Security Posture Management.

## T

- **TPM** -- Trusted Platform Module. Hardware root of trust on
  endpoints.
- **TLS** -- Transport Layer Security (1.2 minimum, 1.3 preferred).
- **TOTP** -- Time-based One-Time Password (RFC 6238).
- **TTP** -- Tactics, Techniques, and Procedures (MITRE ATT&CK).

## V

- **VDP** -- Vulnerability Disclosure Policy.
- **VEX** -- Vulnerability Exploitability eXchange. Assertion that a
  CVE in an SBOM is (or is not) exploitable.

## W

- **WAF** -- Web Application Firewall.
- **WSTG** -- OWASP Web Security Testing Guide.

## X

- **XSS** -- Cross-Site Scripting.
- **XSW** -- XML Signature Wrapping (SAML attack class).
- **XXE** -- XML External Entity.

## Z

- **ZTA** -- Zero Trust Architecture (NIST SP 800-207).

## References

- NIST glossary: <https://csrc.nist.gov/glossary>
- ENISA glossary: <https://www.enisa.europa.eu/topics/risk-management/current-risk/risk-management-inventory/glossary>
- OWASP Glossary (per project): <https://owasp.org/>
