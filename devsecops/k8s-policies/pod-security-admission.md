# Pod Security Admission (PSA)

Built-in Kubernetes admission controller (stable since 1.25) that
checks Pod specs against one of three profiles: `privileged`,
`baseline`, or `restricted`. Selected per namespace via labels.

## Profiles at a glance

| Profile | Use when | Allows |
| --- | --- | --- |
| `privileged` | trusted system workloads (CNI, CSI, monitoring agents) | everything; no restrictions |
| `baseline` | general workloads; minimal break risk | reasonable defaults; blocks the most exploitable patterns (privileged, hostPath, hostNetwork) |
| `restricted` | hardened workloads | strict; non-root, drop ALL capabilities, seccomp RuntimeDefault, read-only root filesystem etc. |

## Apply per namespace

PSA evaluates the labels on the Pod's namespace at admission time:

```yaml
apiVersion: v1
kind: Namespace
metadata:
  name: my-service
  labels:
    # Enforce: block non-compliant pods from being created.
    pod-security.kubernetes.io/enforce: restricted
    pod-security.kubernetes.io/enforce-version: latest

    # Audit: log warnings about non-compliant pods (does not block).
    pod-security.kubernetes.io/audit: restricted
    pod-security.kubernetes.io/audit-version: latest

    # Warn: return a warning to the kubectl client on apply.
    pod-security.kubernetes.io/warn: restricted
    pod-security.kubernetes.io/warn-version: latest
```

Three modes:

- `enforce` -- blocks non-compliant pods (apply this in steady state).
- `audit` -- writes a violation event to the audit log; useful for
  rollout.
- `warn` -- returns a warning to the user submitting the pod; useful
  for developer feedback.

## Rollout

Walk one namespace at a time:

1. Set `audit: restricted` and `warn: restricted`.
2. Watch the audit log and developer warnings for a couple of weeks.
3. Fix the workloads that fail.
4. Promote to `enforce: restricted`.

## Compliant Pod template (restricted)

```yaml
apiVersion: v1
kind: Pod
metadata:
  name: my-app
spec:
  automountServiceAccountToken: false
  securityContext:
    runAsNonRoot: true
    runAsUser: 65532
    runAsGroup: 65532
    fsGroup: 65532
    seccompProfile:
      type: RuntimeDefault
  containers:
    - name: app
      image: ghcr.io/myorg/svc@sha256:<digest>
      securityContext:
        allowPrivilegeEscalation: false
        readOnlyRootFilesystem: true
        runAsNonRoot: true
        capabilities:
          drop: ["ALL"]
      resources:
        requests: { cpu: "100m", memory: "128Mi" }
        limits: { cpu: "500m", memory: "256Mi" }
      ports:
        - containerPort: 8080
```

## Exemptions

For system workloads that legitimately need elevated privileges
(CNI agents, node-monitor daemons), put them in a namespace labeled
`enforce: privileged` and lock down namespace creation via RBAC and a
ConstraintTemplate (see [opa-gatekeeper-constraints.md](opa-gatekeeper-constraints.md)).

## What PSA does NOT cover

- Image provenance (signature, SBOM, SLSA attestation). Use a
  separate admission controller (Kyverno cosign rules, Sigstore policy
  controller, or a custom webhook).
- Identity and access (RBAC). PSA is about Pod spec shape only.
- Network policy. PSA does not change packet flow.

## References

- Kubernetes Pod Security Standards: <https://kubernetes.io/docs/concepts/security/pod-security-standards/>
- Pod Security Admission: <https://kubernetes.io/docs/concepts/security/pod-security-admission/>
- Migrating from PSP to PSA: <https://kubernetes.io/docs/tasks/configure-pod-container/migrate-from-psp/>
- CIS Kubernetes Benchmark: <https://www.cisecurity.org/benchmark/kubernetes>
