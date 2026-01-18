# Third-Party Software Intake

Process and checklist for evaluating third-party software (commercial
products, SaaS, OSS libraries) before adoption. The depth scales with
the risk tier of the data the software touches.

## Risk tiers

- **T1 — Restricted data, customer-facing**: vendor sees or stores
  restricted-class data (PII, secrets, regulated data) or is in the
  critical request path. Full intake.
- **T2 — Internal data, internal tools**: vendor processes internal
  data or supports critical workflows. Light intake.
- **T3 — No regulated data, low blast radius**: developer tooling,
  documentation, marketing-only. Minimal intake.

Decide the tier first; the checklist depth follows.

## T1 intake — full review

### Vendor security posture

- [ ] SOC 2 Type II report (or ISO/IEC 27001 certificate) within the
      last 12 months, reviewed by security team.
- [ ] Penetration test report from an independent firm within the
      last 12 months, with remediation evidence.
- [ ] Published security page, security.txt, and incident-disclosure
      history.
- [ ] Bug bounty or vulnerability disclosure program.
- [ ] Sub-processor list available; new sub-processors notified to us
      before they go live.
- [ ] Incident history reviewed; any public incidents have
      satisfactory post-mortems.

### Data handling

- [ ] Data residency: region pinning available where required.
- [ ] Data classification accepted at the vendor matches our
      classification.
- [ ] Encryption in transit (TLS 1.2+), at rest (KMS-backed), with
      key management documented.
- [ ] Customer-managed keys (BYOK / HYOK) available if required.
- [ ] Retention policy aligned with our policy; data export and
      deletion on request documented.
- [ ] Data-protection agreement (DPA) in place; standard contractual
      clauses (SCCs) for cross-border transfers if applicable.

### Identity and access

- [ ] SSO via SAML 2.0 or OIDC supported.
- [ ] SCIM for user provisioning / de-provisioning.
- [ ] Role-based access with documented role definitions.
- [ ] Audit log export to our log store (or syslog / S3 / event bus).
- [ ] MFA available and enforceable; phishing-resistant MFA
      (WebAuthn) for admin accounts.

### Integration and supply chain

- [ ] SBOM (CycloneDX or SPDX) of the vendor's software, where
      installed on our infrastructure.
- [ ] Signed releases (cosign / Sigstore / GPG) where applicable.
- [ ] API surface reviewed for authentication scheme, rate limits,
      versioning, deprecation policy.
- [ ] Data flows diagrammed; entry and exit through documented
      interfaces only.

### Operational

- [ ] SLAs documented; on-call contact for severity-1 incidents.
- [ ] Backup, restore, and disaster recovery procedures documented.
- [ ] Off-boarding plan: data export format, retention after
      termination, key revocation.
- [ ] Pricing structure understood; renewal terms documented.

### Legal

- [ ] License compatible with how we will use the software.
- [ ] Indemnification, limitation of liability, audit rights as
      required.
- [ ] Choice-of-law and dispute-resolution clauses reviewed.

## T2 intake — light review

- [ ] Vendor security posture (SOC 2 OR ISO/IEC 27001 OR equivalent).
- [ ] Encryption in transit and at rest.
- [ ] SSO / SCIM supported.
- [ ] DPA in place if any personal data is involved.
- [ ] Off-boarding plan documented.

## T3 intake — minimal review

- [ ] License compatible (SPDX identifier confirmed).
- [ ] No restricted data routed through the tool.
- [ ] Adoption recorded in the inventory.

## OSS library intake

A library is in scope when added as a dependency. Evaluate before
adding:

- [ ] License (SPDX): permissive (MIT, BSD, Apache-2.0) or copyleft
      compatible with our distribution model.
- [ ] Recent activity: last release within the last 12 months OR
      maintained by a long-running project with clear maintainership.
- [ ] Maintainer signal: more than one maintainer, or affiliated with
      a foundation / company; not a single-developer project for
      high-impact dependencies.
- [ ] Security history: known CVEs, response time on past advisories,
      published security policy.
- [ ] Provenance: published with provenance attestation
      (npm provenance, Sigstore) for critical dependencies.
- [ ] Transitive footprint: dependency tree depth and breadth
      acceptable; no obvious typosquats or namespace squats.
- [ ] Pinned by hash or by exact version in the lockfile.
- [ ] SCA scan clean on the version being adopted.

For evaluating libraries against well-known typosquatting patterns,
see
[../secure-coding/javascript-typescript/node-supply-chain.md](../secure-coding/javascript-typescript/node-supply-chain.md)
and
[../devsecops/supply-chain/dependency-pinning.md](../devsecops/supply-chain/dependency-pinning.md).

## Records to keep

- Tier decision and justification.
- Completed checklist (above) with dates and reviewer names.
- Copies of evidence documents (SOC 2 report, pentest report, DPA).
- Renewal calendar entry for each item that expires.

## References

- NIST SP 800-161 (Supply-chain risk management): <https://csrc.nist.gov/Projects/cyber-supply-chain-risk-management>
- NIST SP 800-53 SR (Supply-chain risk management family): <https://csrc.nist.gov/projects/risk-management/sp800-53-controls/release-search>
- ISO/IEC 27001:2022: <https://www.iso.org/standard/27001>
- AICPA SOC 2: <https://www.aicpa-cima.com/topic/audit-assurance/audit-and-assurance-greater-than-soc-2>
- OWASP Software Component Verification Standard (SCVS): <https://owasp.org/www-project-software-component-verification-standard/>
- SLSA: <https://slsa.dev/spec/>
