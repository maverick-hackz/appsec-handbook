# Zero Trust Principles

Zero Trust shifts the security perimeter from the network to the
identity and request. "Trust but verify" becomes "never trust, always
verify". NIST SP 800-207 is the canonical reference.

## Core tenets (NIST SP 800-207 §2.1)

1. All data sources and computing services are considered resources.
2. All communication is secured regardless of network location.
3. Access to individual enterprise resources is granted on a
   per-session basis.
4. Access to resources is determined by dynamic policy -- including
   the observable state of client identity, application / service,
   and the requesting asset.
5. The enterprise monitors and measures the integrity and security
   posture of all owned and associated assets.
6. All resource authentication and authorization are dynamic and
   strictly enforced before access is allowed.
7. The enterprise collects as much information as possible about the
   current state of assets, network infrastructure, and communications
   and uses it to improve its security posture.

## Translating to architecture decisions

| Tenet | Concrete decision |
| --- | --- |
| All communication secured | mTLS service-to-service; TLS 1.3 external; never trust intra-cluster network alone |
| Per-session access | Short-lived access tokens (5-15 min) with refresh rotation; no long-lived API keys |
| Dynamic policy | Policy-as-code engine (OPA / Cedar) consulted at request time, not at deploy time |
| Observed posture in decision | Device attestation, geolocation, request risk signals as inputs to the policy |
| Dynamic authentication | Step-up auth for sensitive transactions; re-evaluate session on privilege change |
| Continuous monitoring | Log every access decision with the inputs that produced it |

## Architecture components

```text
+-------------+        +---------+         +----------+
|   Subject   |  ---> |   PEP   |  ----> |   PDP    |
| (user, svc) |        | (proxy / |        | (policy  |
+-------------+        |  gw)    |        |  engine) |
                       +---------+         +----------+
                            |                   ^
                            v                   |
                       +---------+    inputs    |
                       | Resource|              |
                       +---------+              |
                                                |
                                       +-----------------+
                                       | Posture signals |
                                       | (identity, dev, |
                                       |  threat intel)  |
                                       +-----------------+
```

- **Subject**: user or service principal.
- **PEP (Policy Enforcement Point)**: the gateway / sidecar / library
  that intercepts the request and asks for a decision.
- **PDP (Policy Decision Point)**: evaluates policy against subject,
  resource, and posture signals.
- **Resource**: the application / data the subject wants.

## What zero trust does NOT mean

- It does not mean "no network controls". Network segmentation is
  still defence-in-depth; it just stops being the primary control.
- It does not mean "every request hits a remote policy engine".
  Locally cached policy with short TTL is acceptable; the freshness
  trade-off is part of the design.
- It does not mean "MFA everywhere". MFA is one input to the policy;
  step-up only where the risk signal justifies the friction.

## Migrating an existing system

A pragmatic order, from cheapest to most invasive:

1. mTLS service-to-service (start in audit mode, then enforce).
2. Short-lived tokens replacing long-lived API keys.
3. Per-endpoint authorization at the data layer (closes BOLA / BFLA
   class).
4. Policy-as-code engine (OPA / Cedar) for non-trivial rules; start
   advisory.
5. Posture inputs (device, geolocation, threat-intel) feeding the
   policy.
6. Continuous policy evaluation across all components.

Each step delivers measurable risk reduction independently; do not
wait for the full picture to land before deploying step 1.

## References

- NIST SP 800-207 (Zero Trust Architecture): <https://csrc.nist.gov/publications/detail/sp/800-207/final>
- NIST SP 800-207A (Zero Trust Architecture for cloud-native applications): <https://csrc.nist.gov/pubs/sp/800/207/a/final>
- CISA Zero Trust Maturity Model: <https://www.cisa.gov/zero-trust-maturity-model>
- BeyondCorp (Google): <https://cloud.google.com/beyondcorp>
- Forrester ZTX framework: <https://www.forrester.com/report/the-forrester-wave-zero-trust-platform-providers/>
