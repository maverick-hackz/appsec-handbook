# Secure SDLC

Security activities mapped to each phase of the software development
lifecycle: requirements, code review, gates, programs.

## Files

- [Security requirements template](security-requirements-template.md) — reusable security requirement entries with example set
- [Code review checklist](code-review-checklist.md) — per-category yes/no questions for security-focused review
- [Definition of done (security)](definition-of-done-security.md) — stage-by-stage DoD checklist
- [Security gates by stage](security-gates-by-stage.md) — what blocks at which stage
- [Vulnerability disclosure policy template](vulnerability-disclosure-policy-template.md) — VDP template per ISO/IEC 29147 and CERT/CC
- [Security champions program](security-champions-program.md) — roles, responsibilities, training, metrics
- [Third-party software intake](third-party-software-intake.md) — vendor / OSS / library evaluation checklist

## How this section relates to the rest

- The requirement IDs (e.g., `SR-AUTHN-001`) referenced here are the
  shape of requirements the [threat modeling](../threat-modeling/)
  output translates into.
- The code review checklist is the developer-facing companion to
  [secure coding](../secure-coding/) — the topic files explain the
  pattern; the checklist asks "did we apply it here?".
- DevSecOps gates ([devsecops](../devsecops/)) are how the gates in
  `security-gates-by-stage.md` are mechanically enforced.

## What this section is NOT

- A pentest checklist. Offensive testing belongs in the companion
  [Workstation](https://github.com/maverick-hackz/Workstation) repository.
- A compliance manual. Maps to frameworks (ASVS, SAMM, SSDF) live in
  [frameworks](../frameworks/).
