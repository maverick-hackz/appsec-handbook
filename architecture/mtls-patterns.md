# mTLS Patterns

Mutual TLS authenticates both sides of a TLS handshake. For
service-to-service traffic inside an organisation, mTLS is the simplest
way to make every connection authenticated.

## When to use mTLS

- All service-to-service communication inside a cluster or VPC.
- Partner integrations where the partner has a stable identity and a
  client certificate can be issued.
- Critical service-to-database traffic (the database verifies the
  client cert as proof of service identity).
- Webhooks delivered from your service to the partner: pin your
  client certificate to the partner; pin their server certificate to
  you.

## Service-to-service architecture

```text
[ Service A ] --(mTLS)--> [ Service B ]
     ^                          ^
     |                          |
     +-- client cert ---+       +-- server cert
     +-- server cert    +-- client cert
                        |
                +------------------+
                | CA (issuer for   |
                |  both directions)|
                +------------------+
```

Both services present a certificate; both verify the peer against a
trusted CA. The CA is operated internally; certificates are short-lived
(minutes to hours, not days) and rotated automatically.

## SPIFFE / SPIRE

SPIFFE (Secure Production Identity Framework For Everyone) is the
open-source standard for service identity. SPIRE is a reference
implementation that issues short-lived X.509 (or JWT) credentials per
workload.

SPIFFE identifiers use the `spiffe://` scheme:

```text
spiffe://trust-domain.example.com/ns/production/sa/orders-service
```

The trust domain is the organization; the path encodes the namespace
and identity of the workload. Service mesh (Istio, Linkerd) sidecars
fetch SPIFFE identities from SPIRE and use them as the TLS client
certificate without the application doing anything.

## Certificate rotation

| Component | Cadence | Mechanism |
| --- | --- | --- |
| Workload certificate (SPIRE) | 1 hour | Automatic from SPIRE agent |
| Service-mesh internal CA | 24 hours | Rotated by mesh control plane |
| External-facing TLS cert | 90 days | Let's Encrypt / cert-manager / ACME |
| Root CA (internal) | Years | Manual; rotation event with overlap period |

Short cert lifetimes are a feature, not a bug: revocation becomes
trivial (just stop renewing), CRLs / OCSP become less load-bearing,
and stolen credentials expire on their own.

## Service-mesh integration

| Mesh | mTLS posture |
| --- | --- |
| Linkerd | mTLS enabled by default, transparent to the application |
| Istio | mTLS via `PeerAuthentication` (per namespace / cluster); modes: `STRICT`, `PERMISSIVE`, `DISABLE` |
| Consul Connect | mTLS via Connect intentions; identity from SPIFFE |
| Cilium | mTLS via WireGuard or Envoy proxy; SPIFFE identity |

Recommended rollout:

1. Enable mTLS in `PERMISSIVE` (or equivalent) mode across the namespace.
2. Confirm traffic is encrypted via observability (peer cert visible
   on flows).
3. Promote to `STRICT` (block plain-text); each service now requires
   a peer cert.

## Without a mesh

For services that cannot run in a mesh (managed services like
PostgreSQL, S3, Vault), use vendor-native mTLS:

- PostgreSQL: `ssl_ca_file`, `ssl_cert_file`, `ssl_key_file`;
  client cert mapped to a Postgres role.
- Vault: TLS auth method; client cert authenticates to a Vault role.
- Cloud storage: client-cert authentication where supported; otherwise
  short-lived IAM credentials via OIDC.

## Common attacks

### Stolen client certificate

A leaked certificate authenticates as that workload until expiry.
Defence: short lifetime + automatic rotation; ensure the workload's
private key never leaves the workload (Secure Enclave, hardware
security module, SPIRE keystore).

### Compromised CA

If the internal CA is compromised, every certificate it ever issued
becomes suspect. Defence: keep the CA in an HSM; offline root CA with
short-lived intermediate; document key-recovery and rotation procedure.

### Misconfigured `InsecureSkipVerify`

A client that disables certificate verification accepts any server.
Defence: forbid `InsecureSkipVerify` / `rejectUnauthorized: false` in
production code paths; see
[../secure-coding/javascript-typescript/jwt-handling.md](../secure-coding/javascript-typescript/jwt-handling.md)
(rule is the same for TLS verification in general).

## References

- RFC 8446 (TLS 1.3): <https://datatracker.ietf.org/doc/html/rfc8446>
- SPIFFE: <https://spiffe.io/>
- SPIRE: <https://spiffe.io/docs/latest/spire-about/>
- Istio mTLS: <https://istio.io/latest/docs/concepts/security/#mutual-tls-authentication>
- Linkerd mTLS: <https://linkerd.io/2/features/automatic-mtls/>
- cert-manager: <https://cert-manager.io/>
- ACME (Let's Encrypt): <https://datatracker.ietf.org/doc/html/rfc8555>
