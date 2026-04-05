# OWASP Top 10 for LLM Applications (2025) Controls

Risks specific to applications that include LLMs in the request path.
For each: short description and the typical control.

## LLM01:2025 -- Prompt Injection

User input (or third-party content the model retrieves) overrides the
system prompt, instructions, or guard rails.

Controls:

- System instructions in a separate channel (system role) when
  supported; never concatenate untrusted text into the system prompt.
- Output validation: deny tool calls and side-effecting actions when
  the model emits them outside the expected schema.
- Treat retrieved content (RAG documents, web pages, files) as
  untrusted; sandbox or sanitise before inclusion.
- Use a smaller, focused model as a "validator" downstream of the
  primary model when the action surface is large.

## LLM02:2025 -- Sensitive Information Disclosure

Model emits PII, secrets, or proprietary information present in
training data, prompts, or retrieved context.

Controls:

- Output redaction / PII detection before returning to the user.
- Retrieval allowlist; per-user authorization at retrieval time.
- Training-data hygiene; do not train on raw user inputs without
  consent and minimisation.

## LLM03:2025 -- Supply Chain

Models, model weights, prompts, datasets, and tool integrations have
the same supply-chain risks as code. Includes provenance of the
weights and reproducibility of training.

Controls:

- Verify model artifacts by hash; prefer providers with signed
  releases.
- Pin model versions in production; track in the SBOM-equivalent
  inventory.
- Vendor security review on model-as-a-service providers.
- See [../devsecops/supply-chain/](../devsecops/supply-chain/) for the
  general supply-chain patterns.

## LLM04:2025 -- Data and Model Poisoning

Adversary contributes manipulated data into training, fine-tuning, or
the RAG corpus, biasing or backdooring outputs.

Controls:

- Provenance per data source; signed corpus updates.
- Differential testing of model outputs before promoting a new
  version.
- Anomaly detection on RAG ingestion (sudden new sources, abnormal
  document size or language patterns).

## LLM05:2025 -- Improper Output Handling

Downstream code trusts the model's output and treats it as HTML / SQL
/ code without parsing as a value.

Controls:

- Treat model output as untrusted input to the next stage.
- Apply the same encoding / parameterisation / validation as for
  user input.
- Tool-call boundaries: define explicit schemas (JSON Schema for
  tool arguments) and validate strictly.

## LLM06:2025 -- Excessive Agency

The model can invoke tools or actions with broader scope than
necessary; a misled call has real-world consequences.

Controls:

- Least-privilege tool design: each tool's scope is the minimum
  needed.
- Human in the loop for high-impact actions.
- Per-tool rate limits and aggregate per-conversation quotas.
- Cap the agentic loop (max-iterations) to prevent runaway costs.

## LLM07:2025 -- System Prompt Leakage

System prompt is extracted by the user and reveals instructions,
credentials embedded by mistake, or proprietary methodology.

Controls:

- Treat the system prompt as semi-public; do not store secrets
  there.
- Filter responses that echo the system prompt structure.
- Defence-in-depth: assume the prompt is leaked; rely on actual
  controls (auth, authorization, validation), not prompt obscurity.

## LLM08:2025 -- Vector and Embedding Weaknesses

Embeddings / vector stores leak training data, can be poisoned, or
allow membership-inference attacks.

Controls:

- Encryption at rest for vector stores.
- Access control on vector retrieval (tenant scoping).
- Differential privacy where the use case warrants.
- Sanitise sensitive content before embedding generation.

## LLM09:2025 -- Misinformation

Model emits incorrect, fabricated, or harmful content; downstream
treats it as authoritative.

Controls:

- Output labelling: clear UX that the response is AI-generated.
- Citation / source-grounding via RAG with provenance.
- Domain-specific evaluators (medical, legal, financial) gating
  high-stakes outputs.
- Human review on irreversible / high-impact decisions.

## LLM10:2025 -- Unbounded Consumption

Model usage exhausts resources (tokens, cost, GPU time, downstream
APIs) due to recursion or adversarial inputs.

Controls:

- Per-account and per-conversation token / request budgets.
- Maximum response length and tool-iteration count enforced server-side.
- Cost alerting per tenant.
- Reject inputs that exceed a defined size before invoking the model.

## Mapping to MITRE ATLAS

LLM-specific TTPs live in MITRE ATLAS (the AI/ML counterpart of
ATT&CK). Each Top 10 entry above maps to one or more ATLAS techniques;
use ATLAS for adversary modelling, the Top 10 for control framing.

## References

- OWASP Top 10 for LLM Applications (2025): <https://genai.owasp.org/llm-top-10/>
- OWASP LLM AI Security and Governance Checklist: <https://genai.owasp.org/>
- MITRE ATLAS: <https://atlas.mitre.org/>
- NIST AI Risk Management Framework: <https://www.nist.gov/itl/ai-risk-management-framework>
