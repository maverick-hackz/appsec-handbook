# Threat Model: CI / CD Pipeline

A sanitized model of a typical microservice pipeline: code in a Git
host, build / test in a hosted CI, container image to a registry,
deploy to a Kubernetes cluster via GitOps.

## System overview

Developers push to a Git repository. A protected branch policy requires
review and green CI. The CI runner builds the container, runs unit and
integration tests, runs SAST / SCA / secret scanning, signs the image
with Sigstore, and pushes to the registry. A GitOps controller in the
cluster watches the registry and applies the new image to the
deployment.

## Assets

| Asset | Sensitivity | Owner |
| --- | --- | --- |
| Source repository contents | Confidential | Engineering |
| Long-lived deploy credentials (rare; OIDC preferred) | Restricted | Platform |
| Signing key material (cosign / Fulcio identity) | Restricted | Platform |
| Image registry contents | Confidential | Platform |
| Production cluster | Restricted | SRE |
| Audit logs of pipeline runs and admissions | Confidential | SRE |

## Trust boundaries

1. `TB-1` Developer workstation -> Git host (HTTPS, signed commits)
2. `TB-2` Git host -> CI runner (HTTPS webhooks, mutual auth)
3. `TB-3` CI runner -> Registry (OIDC-federated token, scoped push)
4. `TB-4` CI runner -> Sigstore (OIDC identity -> short-lived cert)
5. `TB-5` Registry -> GitOps controller (TLS, pull policy)
6. `TB-6` GitOps controller -> Kubernetes API (RBAC, mTLS)
7. `TB-7` Cluster admission -> Cosign verification (policy controller)

## DFD (text form)

```text
[Developer]
    |
    | signed commit, push over HTTPS
    v
============== TB-1 ==
    |
    v
(Git Host) -- webhook --> (CI Runner)
                            |
                            +-- read repo (clone)
                            +-- OIDC -> [[Sigstore (Fulcio + Rekor)]]
                            +-- OIDC -> push --> [[Registry]]
                            +-- OIDC -> attest provenance --> [[Rekor]]
                            +-- write status --> (Git Host)

[[Registry]] <-- pull --> (GitOps Controller) -- apply --> (Kubernetes API)
                                                                |
                                            admission controller verifies
                                            cosign signature + SLSA attestation
                                                                |
                                                                v
                                                          (Workload pods)
```

## Assumptions

1. The CI runner is hosted (GitHub-hosted runner, GitLab SaaS) with
   well-known isolation properties; a dedicated self-hosted runner with
   network egress would change the model.
2. Sigstore is used in keyless mode (Fulcio + Rekor + OIDC). The
   organisation accepts Sigstore's trust root.
3. The cluster's admission controller verifies cosign signatures AND
   SLSA provenance before scheduling pods.
4. Branch protection on the default branch requires a passing CI run
   and an approving review.

## STRIDE analysis

| # | Element | Threat | STRIDE | Mitigation | Status |
| --- | --- | --- | --- | --- | --- |
| 1 | Developer | Compromised account pushes malicious change | S, E | Required code review (>= 1 approving review by non-author); signed commits; merge queue; CODEOWNERS for sensitive paths | Done |
| 2 | Git host | Token / SSH key leaked from developer machine | S | Short-lived tokens (SSO-backed); ssh-key rotation; secret-scanning on pushes; hardware-keys for human auth where supported | Done |
| 3 | Git host | Webhook spoofed to trigger CI | T | Webhook signing secret; CI verifies HMAC; events outside expected branches dropped | Done |
| 4 | CI runner | Untrusted PR builds with full secrets | E | PR builds run on isolated runners with no deploy credentials; secrets gated to `push` events on protected branches | Done |
| 5 | CI runner | Lateral movement via build script | E | Single-use ephemeral runners; no persistent disk; minimal base image; explicit egress allowlist | Done |
| 6 | CI runner | Dependency confusion / typosquatted pull | T | Pinned dependencies, lockfiles, allowlist of internal scopes, registry pinned to internal mirror | Done |
| 7 | CI runner -> Registry | Long-lived static credential | S, E | OIDC-federated short-lived credentials (`id-token: write` permission scope-limited per workflow); rotated automatically | Done |
| 8 | Sigstore signing | Wrong identity signs the image | S | OIDC subject pinned in admission policy (`subject == "repo:<org>/<repo>:..."`); per-environment identity granularity | Done |
| 9 | Registry | Tag mutated to point at malicious image | T | Pull by digest in the deployment manifest; tag pushes restricted to CI identity; tag immutability where supported | Done |
| 10 | GitOps controller | Reads wrong manifest source | T, E | Single trusted GitOps source repository; controller authenticated; manifest signing optional belt-and-braces | Done |
| 11 | Admission controller | Bypassed by privileged role | E | Cluster RBAC: only the controller's ServiceAccount can apply to production namespace; ImagePolicyWebhook enforces signature verification on every Pod | Done |
| 12 | Audit logs | Tampered by compromised CI | T, R | Logs streamed to off-host append-only store; CI does not have write access to the audit sink | Done |
| 13 | Build cache | Poisoned content reused across runs | T | Cache key includes lockfile hash and toolchain version; trusted cache layer separate from PR contributions | Done |
| 14 | Production cluster | Out-of-band kubectl apply | E | RBAC denies humans direct write to production namespace except break-glass; break-glass requires MFA and is recorded | Done |

## Residual risks

- Compromise of Sigstore's Fulcio or Rekor would invalidate keyless
  verification. The trust root rotation procedure is documented; out
  of scope to enumerate here.
- A bug in the admission controller's policy engine could let a
  malformed image through. Periodic policy-engine tests against
  known-bad inputs.
- Insider with both `merge` rights and the ability to disable branch
  protection is high impact; offset with audit log and a separate
  break-glass channel that triggers an alert.

## Open questions

1. Are PR builds running on a separate runner pool with no production
   secrets? Verify via a deliberately failing test that tries to read
   a deploy token in a PR build and confirm it fails.
2. Is the cluster admission policy fail-closed? On admission webhook
   timeout, does the cluster refuse to schedule (correct) or proceed
   (dangerous)?
3. Is the GitOps controller's source repository protected with the
   same branch policy as application source, including required
   review for manifest changes?

## References

- SLSA: <https://slsa.dev/spec/>
- Sigstore: <https://docs.sigstore.dev/>
- cosign: <https://docs.sigstore.dev/cosign/signing/overview/>
- OWASP Top 10 CI/CD Security Risks: <https://owasp.org/www-project-top-10-ci-cd-security-risks/>
- GitHub Actions security hardening: <https://docs.github.com/en/actions/security-guides/security-hardening-for-github-actions>
- Kubernetes ImagePolicyWebhook: <https://kubernetes.io/docs/reference/access-authn-authz/admission-controllers/#imagepolicywebhook>
- CNCF Software Supply Chain Best Practices: <https://tag-security.cncf.io/community/working-groups/supply-chain-security/supply-chain-security-paper-v2/Software_Supply_Chain_Practices_whitepaper_v2.pdf>
