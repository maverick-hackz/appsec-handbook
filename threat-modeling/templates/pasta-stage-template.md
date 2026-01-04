# PASTA Stage Template

Seven stages, each with a small number of prompts. Output of each
stage feeds the next; PASTA is sequential.

## Stage 1: Define business objectives

- What does this system do for the business? Top three measurable
  outcomes (e.g., process N transactions/min, retain customer data
  for K years).
- What regulatory regimes apply (GDPR, HIPAA, NIS2, SOX, ISO/IEC 27001)?
- What is the worst-case business impact (revenue, regulatory fine,
  reputational damage) if a tier-1 risk is realised?

## Stage 2: Define technical scope

- Components, services, third parties, deployment topology.
- Data classifications: public, internal, confidential, restricted.
- Inventory of external interfaces (APIs, file ingestion, partner
  channels).

## Stage 3: Application decomposition

- DFD with trust boundaries.
- Use cases (intended) and abuse cases (out-of-spec).
- Entry points: every place untrusted input or untrusted code can
  reach a process boundary.

## Stage 4: Threat analysis

- Threat intelligence: relevant TTPs from MITRE ATT&CK for the
  industry segment.
- Active threats specific to the stack (CVE feed for the components
  in scope, public IoCs).
- Insider threat: roles with elevated access, separation of duties.

## Stage 5: Vulnerability and weakness analysis

- SAST / SCA / DAST output, pen-test findings, code review findings.
- Architectural weaknesses (single point of failure, weak crypto
  choices, missing defence-in-depth).
- Map findings to CWE for taxonomy.

## Stage 6: Attack modeling

- For each threat, the attack path: entry point -> sequence of steps
  -> objective. Attack trees ([attack-tree-template.md](attack-tree-template.md))
  fit here.
- Note prerequisites: what the attacker must already possess (network
  access, credentials, software footing).

## Stage 7: Risk and impact analysis

- Combine likelihood and impact for each attack into a risk score.
- For each risk above tolerance: mitigation, owner, deadline,
  residual risk after mitigation.
- Report to the business audience defined in Stage 1.

## When PASTA fits

- Regulated industries where every risk needs a dollar value or a
  regulatory clause attached.
- Mature security programs with the staffing to run all seven stages.
- Engagements where the executive audience wants a business-anchored
  story, not a technical taxonomy.

When the team needs only a structured "what can go wrong" pass on a
new design, STRIDE finishes faster.

## References

- UcedaVelez, Morana — Risk Centric Threat Modeling: Process for Attack Simulation and Threat Analysis (Wiley, 2015)
- OWASP — PASTA primer: <https://owasp.org/www-pdf-archive/AppSecEU2012_PASTA.pdf>
- MITRE ATT&CK: <https://attack.mitre.org/>
- MITRE CAPEC: <https://capec.mitre.org/>
