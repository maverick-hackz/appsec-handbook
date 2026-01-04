# When to Use What

Pick the methodology that matches the question being asked.

## Decision matrix

| Context | Recommended approach |
| --- | --- |
| Greenfield system design | STRIDE-per-element on DFD |
| Existing system, time-boxed | STRIDE-per-interaction or attack trees |
| Compliance-driven (HIPAA, GDPR, SOX) | PASTA (business risk anchored) |
| Privacy-sensitive (PII, health, biometric) | LINDDUN, layered on STRIDE |
| Single high-value asset, narrow attacker model | Attack trees rooted at the asset |
| New protocol or cryptographic design | STRIDE-per-interaction + formal review |
| CI/CD or supply-chain pipeline | STRIDE on the pipeline as a DFD; see [examples/ci-cd-pipeline.md](examples/ci-cd-pipeline.md) |
| Mobile client (Android / iOS) | STRIDE plus MASVS-driven control review |
| Post-incident root-cause-by-cause | Attack tree of the realised attack |

## What changes per stage

- Concept / requirements: list assets, attackers, and worst-case impact.
  No DFD required; outputs feed the design.
- Design: STRIDE-per-element on a DFD; informs control selection.
- Implementation: focused threat models on new components or changed
  interfaces only — do not redo the whole tree.
- Pre-release: a brief refresh; verify each STRIDE mitigation has a
  corresponding test or evidence.
- Operations / incident response: attack trees on the realised attack
  for blast-radius scoping and tabletop exercises.

## Anti-patterns

- "We did a threat model" as a deliverable, with no follow-up tracking
  of the threats. Each threat needs an owner and a status.
- One mega-model for the whole product. Split by service or trust
  boundary so the model stays small enough to review.
- Threat modeling AFTER the code is written, only. The cheapest fixes
  happen in design.
- Reaching for the most complex methodology first. STRIDE on a
  whiteboard finishes faster than PASTA, and most teams do not need
  the business-impact-up framing.

## References

- OWASP Threat Modeling Manifesto: <https://www.threatmodelingmanifesto.org/>
- Adam Shostack — Four Question Framework: <https://github.com/adamshostack/4QuestionFrame>
- OWASP Threat Modeling Cheat Sheet: <https://cheatsheetseries.owasp.org/cheatsheets/Threat_Modeling_Cheat_Sheet.html>
