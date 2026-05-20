# Kubernetes Policies

Cluster-level security controls that complement the container hardening
in [Dockerfile hardening](../dockerfile-hardening.md).

## Files

- [Pod Security Admission](pod-security-admission.md) -- profiles and namespace labels
- [Default-deny NetworkPolicy](network-policy-default-deny.yaml) -- baseline manifest
- [OPA Gatekeeper constraints](opa-gatekeeper-constraints.md) -- three OPA Gatekeeper constraint templates
- [Falco rules starter](falco-rules-starter.md) -- five Falco runtime-detection rules

## Layered controls

| Layer | Control | Where to enforce |
| --- | --- | --- |
| Admission: PodSpec shape | Pod Security Admission `restricted` profile | API server (built-in since K8s 1.25) |
| Admission: image provenance | cosign signature + SLSA attestation | Kyverno or Sigstore policy controller |
| Admission: custom policy | OPA Gatekeeper / Kyverno ConstraintTemplate | Custom admission webhook |
| Networking | Default-deny NetworkPolicy + per-workload allow rules | CNI plugin (Calico, Cilium, Antrea) |
| Runtime detection | Falco rules | Per-node daemon |
| Service-to-service authn | mTLS (mesh) or SPIFFE/SPIRE | Service mesh (Linkerd, Istio) or SPIRE |

## Defence in depth

A pod that escapes its container should hit:

1. NetworkPolicy denying its egress.
2. Falco rule alerting on the new behaviour.
3. PSA restriction preventing privileged escalation.
4. Cluster-level RBAC denying API access from the escaped credential.

No single layer is sufficient.

## References

- Kubernetes Pod Security Standards: <https://kubernetes.io/docs/concepts/security/pod-security-standards/>
- Kubernetes NetworkPolicy: <https://kubernetes.io/docs/concepts/services-networking/network-policies/>
- OPA Gatekeeper: <https://open-policy-agent.github.io/gatekeeper/website/docs/>
- Kyverno: <https://kyverno.io/docs/>
- Falco: <https://falco.org/docs/>
- CNCF Cloud-Native Security Whitepaper: <https://tag-security.cncf.io/community/resources/security-whitepaper/>
