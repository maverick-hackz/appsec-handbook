# Threat Model: SSO / OIDC Broker

## System overview

An internal broker mediates between a single corporate IdP (employees)
and a fleet of downstream applications (custom apps, vendor SaaS,
internal tools). The broker exchanges the IdP's OIDC assertion for a
service-specific token tailored to the downstream protocol (OIDC,
SAML, API key, signed JWT). Group memberships in the IdP map to roles
in the downstream app.

## Assets

| Asset | Sensitivity | Owner |
| --- | --- | --- |
| Employee identity assertions in flight | Restricted | IT |
| Broker signing key (per-downstream issuer) | Restricted | Platform Security |
| Role mapping policy (group -> role) | Confidential | Platform Security |
| Audit log of broker decisions | Confidential | IT |
| Service registration metadata (redirect URIs, allowed scopes) | Internal | Platform Security |

## Trust boundaries

1. `TB-1` Browser <-> IdP (TLS, IdP-managed CA)
2. `TB-2` Browser <-> Broker (TLS, organisation CA)
3. `TB-3` Broker <-> IdP back-channel (TLS, signed JWT client assertion)
4. `TB-4` Broker -> Downstream apps (TLS, signed JWT or SAML assertion)
5. `TB-5` Broker -> Policy store (mTLS)
6. `TB-6` Broker -> Audit sink (one-way write, signed)

## DFD (text form)

```text
[Employee Browser]
       |
       v
============== TB-1 / TB-2 ==
       |
       +-----> (IdP)
       |          ^ (back-channel: client assertion)
       v          |
   (Broker) ------+
       |
       +-- mTLS --> [[Policy Store]]
       |
       +-- signed JWT / SAML --> (Downstream App)
       |
       +-- one-way append ----> [[Audit Sink]]
```

## Assumptions

1. The IdP is operated by the same organisation and trusted to assert
   identity faithfully. Compromise of the IdP is out of scope here.
2. The broker is the only path into the downstream applications;
   direct password sign-in to downstreams is disabled.
3. Downstream applications validate the broker's signature on the
   issued assertion AND check `iss`, `aud`, `exp`, `nbf`, `nonce`.
4. The policy store is the source of truth for group-to-role mapping;
   changes go through code review and audit.

## STRIDE analysis

| # | Element | Threat | STRIDE | Mitigation | Status |
| --- | --- | --- | --- | --- | --- |
| 1 | Employee Browser | Spoofed IdP page (phishing) | S | Phishing-resistant MFA (WebAuthn) enforced by IdP; AAD/IdP shows a known origin | Done |
| 2 | Browser <-> Broker | Open redirect via `state` / `redirect_uri` | T | `redirect_uri` strict exact-match against pre-registered values per client; `state` opaque, single-use, bound to session | Done |
| 3 | Browser <-> Broker | CSRF on broker login flow | E | `state` parameter with CSRF-token semantics; SameSite=Lax cookies on the broker; PKCE on public clients | Done |
| 4 | Broker <-> IdP back-channel | Spoofed client identity | S | Broker authenticates to IdP with `private_key_jwt` (signed assertion); key rotation via JWKS; client secrets disabled | Done |
| 5 | Broker | Algorithm confusion on incoming IdP JWT | S, T | Verify `alg` is the IdP-pinned set (e.g., `RS256` only); verify against the JWKS `kid`; reject `alg=none`; pin acceptable `iss` / `aud` | Done |
| 6 | Broker | Replay of legitimate IdP token | T | Nonce + `iat` window; one-time consumption tracked in a short TTL cache | Done |
| 7 | Broker | Role inflation via policy bypass | E | Policy decisions logged with input claims and resolved roles; policy change requires PR review and CI test; deny-by-default if policy fetch fails | Done |
| 8 | Broker | Signing-key compromise | I | Keys stored in HSM/KMS; broker never sees plaintext private key; signing operations rate-limited; key rotation on schedule and on incident | Done |
| 9 | Broker -> Downstream | Aud confusion (token reused on wrong service) | S, E | `aud` set to the downstream service's identifier; downstream validates `aud`; broker refuses to issue for non-registered audiences | Done |
| 10 | Policy Store | Tamper with role mapping | T | mTLS read; writes only via signed admin tool; change history immutable and shipped to Audit Sink | Done |
| 11 | Audit Sink | Tampering with broker logs | T, R | One-way append; daily Merkle root signed and stored off-host; restore drill | Done |
| 12 | Broker process | DoS via signature flood | D | Per-IP and per-client rate limit; circuit breaker on signing latency; resource quotas in the namespace | Done |
| 13 | Inactive employee | Stale group still grants access | E | IdP de-provisioning event invalidates broker session cache; downstream tokens short-lived (5-15 min); refresh requires fresh IdP introspection | Done |
| 14 | Insider with broker code access | Insert backdoor in policy | E, R | Two-person review on policy module; signed releases; CI verifies the deployed image matches the signed artifact | Done |

## Residual risks

- IdP compromise grants the attacker the ability to forge identity
  assertions for any employee. Detection rides on anomaly signals in
  the audit log; the broker cannot independently verify "Is this
  really Alice?" beyond what the IdP asserts.
- A misconfigured downstream that does not validate the broker's
  assertion (no `aud` / `iss` checks) is vulnerable to token reuse if
  one of its sibling apps is compromised. Onboarding tests should
  catch this; an external pen test is the second line.
- An employee with administrative role in the broker's policy module
  is a high-impact insider; offset with separation of duties and
  audit log immutability.

## Open questions

1. Is the policy module covered by integration tests that assert "the
   audit log entry matches the policy decision input"?
2. What is the rotation period for the broker's per-downstream signing
   keys, and is the JWKS endpoint distributing both `current` and
   `next` during overlap windows so downstreams update without an
   outage?
3. Does the broker enforce a per-session bind such that a refresh
   stops working when the IdP de-provisioning event arrives, even
   within the access token's TTL?

## References

- RFC 6749 (OAuth 2.0): <https://datatracker.ietf.org/doc/html/rfc6749>
- RFC 9700 (OAuth 2.0 Security BCP): <https://datatracker.ietf.org/doc/html/rfc9700>
- OpenID Connect Core: <https://openid.net/specs/openid-connect-core-1_0.html>
- SAML 2.0 Core: <https://docs.oasis-open.org/security/saml/v2.0/saml-core-2.0-os.pdf>
- OWASP — SAML Security Cheat Sheet: <https://cheatsheetseries.owasp.org/cheatsheets/SAML_Security_Cheat_Sheet.html>
- NIST SP 800-63C (Federation): <https://pages.nist.gov/800-63-3/sp800-63c.html>
