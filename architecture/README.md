# Architecture

Design-level security patterns: trust models, identity protocols,
service-to-service authentication, cryptography, secrets management,
multi-tenancy.

## Files

- [Zero trust principles](zero-trust-principles.md) -- NIST SP 800-207 applied to typical architectures
- [API gateway security](api-gateway-security.md) -- authn / rate limits / schema validation at the gateway
- [OAuth 2.0 / OIDC flows](oauth2-oidc-flows.md) -- OAuth 2.0 / OIDC flows with sequence diagrams
- [SAML flows](saml-flows.md) -- SP-init / IdP-init flows and signature-wrapping defences
- [mTLS patterns](mtls-patterns.md) -- service-to-service mTLS, cert rotation, SPIFFE / SPIRE
- [Crypto cheatsheet](crypto-cheatsheet.md) -- extended algorithm selection table with recommended parameters
- [Secrets management](secrets-management.md) -- Vault / KMS patterns, sealing, rotation
- [Multi-tenancy isolation](multi-tenancy-isolation.md) -- strong vs weak isolation, partitioning, noisy neighbour

## Relationship to other sections

- The [secure coding](../secure-coding/) entries are line-of-code
  controls. The files here are component-level designs that those
  controls plug into.
- The [threat modeling](../threat-modeling/) examples are concrete
  systems; this section is the inventory of reusable patterns those
  examples pull from.

## When to consult

- During design review for a new system or for a substantial
  architectural change.
- When evaluating whether the team's identity protocol of choice
  fits a new use case (e.g., a partner integration adding device-code
  flow).
- When picking a default for a new project (mTLS, secret store, KMS
  posture).
