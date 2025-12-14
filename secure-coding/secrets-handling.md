# Secrets Handling

## Threat

Credentials, API keys, signing keys, and database URIs embedded in source
or shipped in config get scraped by source-leak crawlers, committed by
developers into public forks, and persisted in container layers.

CWE: CWE-798 (Use of Hard-coded Credentials), CWE-312 (Cleartext Storage
of Sensitive Information), CWE-260 (Password in Configuration File).

## Insecure

`config.py` contains `DB_URL = "postgres://app:hunter2@db/app"`. The same
file is committed to a public mirror; the CI image bakes the file into a
layer; the README pastes the key in a curl example.

## Why it fails

- Public forks of internal repos are common (developer mirrors, vendor
  audits). Crawlers find committed secrets within hours.
- Layered container images preserve removed files in earlier layers;
  `docker history` shows them.
- Rotating a leaked secret in code requires a deploy; rotating a leaked
  secret in a vault requires only a vault operation.

## Secure

- Source-of-truth secret stores: HashiCorp Vault, AWS Secrets Manager,
  GCP Secret Manager, Azure Key Vault. The application reads at startup
  (or on-demand) over an authenticated channel.
- Identity at the workload level: cloud IAM (IRSA, GCP Workload Identity,
  Azure Managed Identity) or SPIFFE/SPIRE for service identity. The
  workload presents identity, the vault returns scoped secrets.
- Local development: a `.env` file outside the repo, plus `.env.example`
  in the repo with placeholder values. Never commit `.env`.
- Rotate on a schedule, on every off-boarding, and on every suspected
  exposure. Short-lived database creds (Vault dynamic secrets) eliminate
  many rotation events.
- Pre-commit and CI secret scanning: gitleaks, trufflehog, GitHub Secret
  Scanning. Block commits that match high-confidence patterns.
- For container images: pass secrets as runtime environment / mounted
  files, not as `ARG` or `COPY .env`. Use BuildKit secret mounts for
  build-time only secrets.

## Notes

- "Encrypted in git" (sops, git-crypt, ansible-vault) is acceptable for low
  blast-radius config; high-value secrets belong in a vault with audit logs.
- A secret that has been pushed to a public repo is leaked even after the
  commit is removed; GitHub keeps reflogs and proxies cache. Always rotate.
- Watch out for accidental logging: pin a redaction layer in the logger
  before request middleware.

## References

- OWASP Secrets Management Cheat Sheet: <https://cheatsheetseries.owasp.org/cheatsheets/Secrets_Management_Cheat_Sheet.html>
- CWE-798: <https://cwe.mitre.org/data/definitions/798.html>
- CWE-312: <https://cwe.mitre.org/data/definitions/312.html>
- NIST SP 800-57 Part 1 (Key Management): <https://csrc.nist.gov/publications/detail/sp/800-57-part-1/rev-5/final>
