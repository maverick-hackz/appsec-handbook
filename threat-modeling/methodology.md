# Methodology

Four methodologies cover most cases. Each emphasises a different lens;
they are complements rather than alternatives.

## STRIDE

A mnemonic for six threat categories applied to elements of a Data Flow
Diagram (DFD):

| Letter | Threat | Counter-property |
| --- | --- | --- |
| S | Spoofing | Authentication |
| T | Tampering | Integrity |
| R | Repudiation | Non-repudiation |
| I | Information disclosure | Confidentiality |
| D | Denial of service | Availability |
| E | Elevation of privilege | Authorization |

Two execution styles:

- **STRIDE-per-element**: enumerate which letters apply to each element
  type (process, data flow, data store, external entity) and walk every
  element. Coverage-first; longer.
- **STRIDE-per-interaction**: walk each pair (source, destination, data)
  and ask which letters apply. Smaller surface; misses element-local
  threats that have no interaction.

Best when: greenfield design, an architect can sketch a DFD, and the
team needs broad coverage of "what can go wrong" categories.

## PASTA (Process for Attack Simulation and Threat Analysis)

A seven-stage risk-centric methodology anchored in business impact, not
just technical threats. Stages: define objectives, define technical
scope, decompose the application, threat analysis, vulnerability and
weakness analysis, attack modeling, risk and impact analysis.

Best when: compliance or business risk is the driver (HIPAA, GDPR,
NIS2, regulated industries) and the output has to map technical risk
to SLAs and regulatory exposure for an executive audience.

## Attack Trees

A goal-rooted tree: the attacker's objective is the root, intermediate
nodes are sub-goals, and leaves are concrete attacks. Nodes are
annotated with cost, skill, likelihood, detectability.

Best when: a specific high-value asset has a small number of
well-known attacker goals (e.g., "exfiltrate the customer database",
"impersonate another tenant"), and the team wants to compare
mitigations by their effect on the lowest-cost path.

## LINDDUN

A privacy-focused mirror of STRIDE: Linkability, Identifiability,
Non-repudiation (as a privacy harm, opposite to STRIDE's "R"),
Detectability, Disclosure of information, Unawareness, Non-compliance.
Applied per DFD element like STRIDE.

Best when: the system processes personal data and a regulator (GDPR,
HIPAA, LGPD, PIPEDA) will judge controls; complements STRIDE rather
than replacing it.

## Picking one

See [when-to-use-what.md](when-to-use-what.md) for the matrix.

A pragmatic default for a typical SaaS engineering team: STRIDE-per-element
during design, attack trees on the top-1-or-2 high-value assets to
prioritise mitigations, and LINDDUN added on top wherever personal
data flows.

## References

- Adam Shostack — Threat Modeling: Designing for Security (Wiley, 2014)
- OWASP Threat Modeling Process: <https://owasp.org/www-community/Threat_Modeling_Process>
- Microsoft Threat Modeling — STRIDE: <https://learn.microsoft.com/en-us/azure/security/develop/threat-modeling-tool-threats>
- PASTA (UcedaVelez and Morana): <https://owasp.org/www-pdf-archive/AppSecEU2012_PASTA.pdf>
- Schneier on Attack Trees (Dr. Dobb's, 1999): <https://www.schneier.com/academic/archives/1999/12/attack_trees.html>
- LINDDUN: <https://www.linddun.org/>
