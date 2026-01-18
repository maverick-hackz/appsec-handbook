# Definition of Done — Security

Stage-by-stage checklist of what must be closed before a piece of
work advances. The DoD does not replace the threat model or the code
review; it is the audit-trail that confirms both happened.

## Design

- [ ] Security requirements (`SR-*`) listed in the feature spec.
- [ ] Threat model updated for any change that crosses a trust
      boundary; new STRIDE rows linked to mitigation owners.
- [ ] Sensitive-data classification confirmed (public / internal /
      confidential / restricted) for every persisted field.
- [ ] Auth model confirmed: who calls this, with what credential
      type, under which scope.
- [ ] Crypto choices reviewed against
      [secure-coding/crypto-do-and-dont.md](../secure-coding/crypto-do-and-dont.md).
- [ ] Logging / audit plan: what is logged, what is redacted, where
      it ships.

## Implementation

- [ ] PR description references the `SR-*` IDs the change satisfies.
- [ ] Author has run through the
      [code-review-checklist.md](code-review-checklist.md).
- [ ] Pre-commit hooks (lint, secret scan, format) pass locally.
- [ ] Unit tests cover the security-critical paths
      (auth check, validation reject, error path).
- [ ] No new hard-coded secrets, no `verify=False` /
      `rejectUnauthorized: false` / `InsecureSkipVerify: true` in
      production code paths.

## Test

- [ ] SAST clean of HIGH+ findings, or each finding has a documented
      suppression with a ticket and rationale.
- [ ] SCA clean of HIGH / CRITICAL CVEs in dependencies, or each one
      has a documented exception.
- [ ] Secret scan clean (gitleaks / trufflehog) on the full commit
      history of the branch.
- [ ] DAST baseline scan green for new endpoints (or scheduled for
      the next full scan if non-public).
- [ ] Authorization tests cover cross-tenant / wrong-role scenarios.
- [ ] Negative tests cover invalid input, malformed input, and
      oversized input.

## Pre-prod (staging)

- [ ] Container image scanned (Trivy / Grype) and signed
      (cosign / Sigstore).
- [ ] SBOM generated and stored with the artifact.
- [ ] Configuration validated for prod parity
      (no `DEBUG=True`, no `ALLOWED_HOSTS=*`, security headers
      present, TLS at least 1.2).
- [ ] Secrets sourced from the vault / secret manager, not from
      source.
- [ ] Logs reaching the central store without PII / token leakage —
      sampled review on staging.
- [ ] Rollback plan documented.

## Production

- [ ] Admission controller enforces signature + SBOM presence (or
      equivalent for the deployment target).
- [ ] Alerting in place for auth failure spikes, error rate, latency
      anomalies on the new code paths.
- [ ] Monitoring dashboard updated with new endpoints / metrics.
- [ ] Incident response runbook section added if the change
      introduces a new failure mode that needs a specific response.

## Post-release

- [ ] Threat model marked "verified" against the deployed state.
- [ ] Open security follow-ups filed as tickets with owners and
      target dates.
- [ ] Any requirement that downgraded (P0 -> P1, etc.) is documented
      with the rationale and the new acceptance criteria.

## References

- OWASP SAMM v2 — Build / Verify / Deploy practices: <https://owaspsamm.org/>
- NIST SSDF (SP 800-218) Practice RV (Respond to Vulnerabilities): <https://csrc.nist.gov/Projects/ssdf>
- OWASP DevSecOps Verification Standard: <https://owasp.org/www-project-devsecops-guideline/>
