# Threat Modeling

Methodology, templates, and worked examples for structured threat analysis
of software systems and pipelines.

## Files

- [methodology.md](methodology.md) — STRIDE, PASTA, attack trees, LINDDUN — what each is for
- [when-to-use-what.md](when-to-use-what.md) — decision matrix per context
- Templates:
  - [stride-per-element.md](templates/stride-per-element.md)
  - [pasta-stage-template.md](templates/pasta-stage-template.md)
  - [attack-tree-template.md](templates/attack-tree-template.md)
  - [dfd-conventions.md](templates/dfd-conventions.md)
- Examples (sanitized, generic systems):
  - [rest-api-oauth2.md](examples/rest-api-oauth2.md)
  - [mobile-messaging-app.md](examples/mobile-messaging-app.md)
  - [sso-oidc-broker.md](examples/sso-oidc-broker.md)
  - [ci-cd-pipeline.md](examples/ci-cd-pipeline.md)

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
