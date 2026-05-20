# Threat Modeling

Methodology, templates, and worked examples for structured threat analysis
of software systems and pipelines.

## Files

- [Methodology](methodology.md) — STRIDE, PASTA, attack trees, LINDDUN — what each is for
- [When to use what](when-to-use-what.md) — decision matrix per context

### Templates

- [STRIDE per element](templates/stride-per-element.md)
- [PASTA stage template](templates/pasta-stage-template.md)
- [Attack tree template](templates/attack-tree-template.md)
- [DFD conventions](templates/dfd-conventions.md)

### Examples

Sanitized, generic systems:

- [REST API with OAuth 2.0](examples/rest-api-oauth2.md)
- [Mobile messaging app](examples/mobile-messaging-app.md)
- [SSO / OIDC broker](examples/sso-oidc-broker.md)
- [CI/CD pipeline](examples/ci-cd-pipeline.md)

## When to model

- During design, BEFORE code lands; the cheapest time to redesign.
- On any architectural change that crosses a trust boundary.
- After a serious incident in the same domain, to validate that
  controls would have prevented or detected it.
- Annually as a refresh for high-value systems.

## Output

A threat model is a document, not a ceremony. Each example in this
section follows a fixed shape: system overview, assets, trust boundaries,
DFD, assumptions, STRIDE table, residual risks, open questions, references.
The same shape applies regardless of which methodology produced the
threats.
