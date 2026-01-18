# Secure SDLC

Security activities mapped to each phase of the software development
lifecycle: requirements, code review, gates, programs.

## Files

- [security-requirements-template.md](security-requirements-template.md) — reusable security requirement entries with example set
- [code-review-checklist.md](code-review-checklist.md) — per-category yes/no questions for security-focused review
- [definition-of-done-security.md](definition-of-done-security.md) — stage-by-stage DoD checklist
- [security-gates-by-stage.md](security-gates-by-stage.md) — what blocks at which stage
- [vulnerability-disclosure-policy-template.md](vulnerability-disclosure-policy-template.md) — VDP template per ISO/IEC 29147 and CERT/CC
- [security-champions-program.md](security-champions-program.md) — roles, responsibilities, training, metrics
- [third-party-software-intake.md](third-party-software-intake.md) — vendor / OSS / library evaluation checklist

## How this section relates to the rest

- The requirement IDs (e.g., `SR-AUTHN-001`) referenced here are the
  shape of requirements the [threat-modeling/](../threat-modeling/)
  output translates into.
- The code review checklist is the developer-facing companion to
  [secure-coding/](../secure-coding/) — the topic files explain the
  pattern; the checklist asks "did we apply it here?".
- DevSecOps gates ([devsecops/](../devsecops/)) are how the gates in
  `security-gates-by-stage.md` are mechanically enforced.

## What this section is NOT

- A pentest checklist. Offensive testing belongs in the companion
  [Workstation](https://github.com/maverick-hackz/Workstation) repository.
- A compliance manual. Maps to frameworks (ASVS, SAMM, SSDF) live in
  [frameworks/](../frameworks/).
