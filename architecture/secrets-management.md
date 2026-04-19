# Secrets Management

Architecture-level patterns for storing, distributing, and rotating
secrets across services. The application-side companion is
[../secure-coding/secrets-handling.md](../secure-coding/secrets-handling.md).

## Tiers of secrets

| Tier | Examples | Blast radius |
| --- | --- | --- |
| T0 (root) | Root CA private key; KMS master key | Entire organisation |
| T1 (high) | Signing keys for tokens; cloud admin credentials; CMKs | One product or environment |
| T2 (medium) | Service-to-service API keys; database master credentials | One service |
| T3 (low) | Per-tenant tokens for third-party SaaS; per-job CI tokens | One tenant / one job |

Rotation cadence and storage class scale with tier:

- T0: HSM only; rotation event with documented playbook; multi-party
  approval.
- T1: HSM or KMS-backed; quarterly rotation or on incident.
- T2: Vault / KMS; monthly rotation; dynamic where supported (Vault
  database secrets).
- T3: Short-lived (minutes to hours); auto-rotated by the system that
  uses them.

## Architecture

```text
+---------------------+
|  Identity provider  |   (cloud IAM, SPIRE, Vault auth methods)
+---------------------+
           |  authenticates workload
           v
+---------------------+
|  Secret store       |
|  (Vault / KMS /     |
|   Secrets Manager)  |
+---------------------+
           |  returns scoped, short-lived secret
           v
+---------------------+
|  Workload           |   never stores plaintext secret to disk
+---------------------+
```

The workload authenticates to the secret store with its workload
identity (cloud IAM, SPIFFE, or pre-shared agent token), then fetches
the scoped secret it needs.

## Patterns by store

### HashiCorp Vault

- Auth methods: Kubernetes (TokenReview), AWS IAM, GCP IAM, Azure
  managed identity, AppRole (for legacy / on-prem).
- Secret engines:
  - `kv` (v2) for static secrets with versioning.
  - `database` for dynamic per-request DB credentials with TTL.
  - `pki` for issuing short-lived TLS certs.
  - `transit` for application-level encryption (BYOK without
    exposing keys).
- Sealed at rest: Vault's storage is encrypted; the unseal key is
  split (Shamir Secret Sharing) or auto-unsealed via cloud KMS.
- Policies define which path each role can read; deny by default.

### Cloud-native secret managers

| Cloud | Service |
| --- | --- |
| AWS | Secrets Manager (KMS-backed); Parameter Store (SecureString) for cheaper, lower-feature use |
| GCP | Secret Manager (KMS-backed) |
| Azure | Key Vault |

Workloads authenticate with cloud IAM (IRSA, GCP Workload Identity,
Azure Managed Identity). No long-lived credentials to fetch the
secrets.

### Sealed Secrets / SOPS for GitOps

For low-tier secrets that should live alongside config in git:

- SOPS encrypts YAML / JSON / INI files using a KMS-managed key.
  The encrypted file is in git; only those with the KMS key can
  decrypt.
- Sealed Secrets (Bitnami): a Kubernetes controller decrypts
  `SealedSecret` resources into regular `Secret` resources at
  apply time.

Use these for medium / low-tier secrets where the GitOps workflow
matters. T0 / T1 secrets belong in a vault, not in git even
encrypted.

## Distribution

- **At process start**: workload reads from the vault / KMS into
  memory. Avoid writing to disk.
- **Per request (dynamic)**: Vault database engine creates a unique
  DB user per session; expires automatically.
- **Mounted as a volume**: CSI driver (Vault CSI, Secrets Store CSI)
  mounts a tmpfs file with the secret. Convenient but the file
  exists; protect with restrictive permissions.
- **Sidecar agent**: Vault Agent or cloud-specific sidecar handles
  token refresh and writes to a tmpfs path the workload reads.

## Rotation

- Static credential rotation: scheduled job rotates and pushes the
  new value. Workloads pick up the new value on the next read; some
  workloads require a restart.
- Dynamic credential rotation: handled automatically by the secret
  engine; the workload requests a new credential on demand.
- Key rotation for envelope encryption: KEK rotated; existing DEKs
  remain encrypted under the previous KEK version. Re-encryption
  scheduled or on-access.

A rotation that no one notices is the goal. Alert on rotation
failures (cert expiry, agent failure to refresh).

## Anti-patterns

- `.env` files in the container image. Visible in `docker history`
  and prevents per-environment configuration.
- Storing secrets in K8s `ConfigMap`. ConfigMap is not encrypted at
  rest by default; use `Secret` (still base64-only by default --
  encrypt etcd) or mount from a vault.
- One long-lived "admin" cloud credential used by every CI workflow.
  Use OIDC federation per workflow with the scope it needs.
- Rotating the secret but not the cached / pre-issued tokens derived
  from it. Confidence drops over time.

## What this section does NOT cover

- Application-side handling (never log, redact in error paths, no
  hardcoding) lives in
  [../secure-coding/secrets-handling.md](../secure-coding/secrets-handling.md).
- CI pipeline secret hygiene lives in
  [../devsecops/ci-templates/](../devsecops/ci-templates/).

## References

- HashiCorp Vault: <https://developer.hashicorp.com/vault/docs>
- AWS Secrets Manager: <https://docs.aws.amazon.com/secretsmanager/>
- GCP Secret Manager: <https://cloud.google.com/secret-manager/docs>
- Azure Key Vault: <https://learn.microsoft.com/en-us/azure/key-vault/>
- Mozilla SOPS: <https://github.com/getsops/sops>
- Bitnami Sealed Secrets: <https://github.com/bitnami-labs/sealed-secrets>
- NIST SP 800-57 (Key Management): <https://csrc.nist.gov/projects/key-management/key-management-guidelines>
- OWASP Secrets Management Cheat Sheet: <https://cheatsheetseries.owasp.org/cheatsheets/Secrets_Management_Cheat_Sheet.html>
