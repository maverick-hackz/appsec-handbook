# OPA Gatekeeper Constraint Templates

Three production-relevant ConstraintTemplate / Constraint pairs.
Gatekeeper enforces Rego policies at admission time; the templates
below define reusable policy shapes that can be instantiated multiple
times with different parameters.

## 1. Disallow privileged containers

ConstraintTemplate:

```yaml
apiVersion: templates.gatekeeper.sh/v1
kind: ConstraintTemplate
metadata:
  name: k8spspprivilegedcontainer
spec:
  crd:
    spec:
      names:
        kind: K8sPSPPrivilegedContainer
  targets:
    - target: admission.k8s.gatekeeper.sh
      rego: |
        package k8spspprivileged

        violation[{"msg": msg}] {
          c := input_containers[_]
          c.securityContext.privileged
          msg := sprintf("Container <%v> in pod <%v> runs as privileged", [c.name, input.review.object.metadata.name])
        }

        input_containers[c] { c := input.review.object.spec.containers[_] }
        input_containers[c] { c := input.review.object.spec.initContainers[_] }
        input_containers[c] { c := input.review.object.spec.ephemeralContainers[_] }
```

Constraint (instantiates the template for the cluster):

```yaml
apiVersion: constraints.gatekeeper.sh/v1beta1
kind: K8sPSPPrivilegedContainer
metadata:
  name: psp-privileged-container
spec:
  match:
    kinds:
      - apiGroups: [""]
        kinds: ["Pod"]
    excludedNamespaces:
      - kube-system
      - gatekeeper-system
```

## 2. Require team and cost-center labels

ConstraintTemplate:

```yaml
apiVersion: templates.gatekeeper.sh/v1
kind: ConstraintTemplate
metadata:
  name: k8srequiredlabels
spec:
  crd:
    spec:
      names:
        kind: K8sRequiredLabels
      validation:
        openAPIV3Schema:
          type: object
          properties:
            labels:
              type: array
              items: { type: string }
  targets:
    - target: admission.k8s.gatekeeper.sh
      rego: |
        package k8srequiredlabels

        violation[{"msg": msg}] {
          missing := input.parameters.labels[_]
          not input.review.object.metadata.labels[missing]
          msg := sprintf("Missing required label %v", [missing])
        }
```

Constraint:

```yaml
apiVersion: constraints.gatekeeper.sh/v1beta1
kind: K8sRequiredLabels
metadata:
  name: workload-labels
spec:
  match:
    kinds:
      - apiGroups: [""]
        kinds: ["Pod"]
      - apiGroups: ["apps"]
        kinds: ["Deployment", "StatefulSet", "DaemonSet"]
  parameters:
    labels:
      - team
      - cost-center
      - service
```

## 3. Restrict allowed image registries

ConstraintTemplate:

```yaml
apiVersion: templates.gatekeeper.sh/v1
kind: ConstraintTemplate
metadata:
  name: k8sallowedrepos
spec:
  crd:
    spec:
      names:
        kind: K8sAllowedRepos
      validation:
        openAPIV3Schema:
          type: object
          properties:
            repos:
              type: array
              items: { type: string }
  targets:
    - target: admission.k8s.gatekeeper.sh
      rego: |
        package k8sallowedrepos

        violation[{"msg": msg}] {
          container := input_containers[_]
          not allowed(container.image)
          msg := sprintf("Image <%v> is not from an allowed registry", [container.image])
        }

        allowed(image) {
          allowed_repo := input.parameters.repos[_]
          startswith(image, allowed_repo)
        }

        input_containers[c] { c := input.review.object.spec.containers[_] }
        input_containers[c] { c := input.review.object.spec.initContainers[_] }
```

Constraint:

```yaml
apiVersion: constraints.gatekeeper.sh/v1beta1
kind: K8sAllowedRepos
metadata:
  name: allowed-image-repos
spec:
  match:
    kinds:
      - apiGroups: [""]
        kinds: ["Pod"]
    namespaces:
      - default
      - production
  parameters:
    repos:
      - "ghcr.io/myorg/"
      - "registry.internal.example.com/myorg/"
```

## Apply and audit

Install Gatekeeper, apply the ConstraintTemplate first (defines the
CRD), then the Constraint (instantiates it). Run in `enforcementAction:
dryrun` to surface violations without blocking; promote to
`deny` once the cluster is clean.

```yaml
spec:
  enforcementAction: dryrun     # or 'deny' once clean
```

## Audit results

```bash
kubectl get constraints
kubectl describe k8sallowedrepos allowed-image-repos
```

## Kyverno alternative

For teams without Rego experience, Kyverno expresses the same policies
in YAML and is operationally simpler. The trade-off is less
expressiveness than Rego for complex policies.

## References

- OPA Gatekeeper documentation: <https://open-policy-agent.github.io/gatekeeper/website/docs/>
- Gatekeeper Policy Library: <https://open-policy-agent.github.io/gatekeeper-library/website/>
- Rego language reference: <https://www.openpolicyagent.org/docs/latest/policy-language/>
- Kyverno: <https://kyverno.io/docs/>
- Kubernetes admission controllers: <https://kubernetes.io/docs/reference/access-authn-authz/admission-controllers/>
