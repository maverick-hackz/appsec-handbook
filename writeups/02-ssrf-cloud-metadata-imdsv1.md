# Finding: SSRF Against Cloud Metadata (IMDSv1)

## Summary

An application takes a URL or hostname from user input and fetches
it server-side. By targeting the cloud provider's instance metadata
service on the link-local address `169.254.169.254`, the attacker
reads the workload's instance profile and short-lived IAM
credentials. With IMDSv1 (the legacy AWS metadata service), the
request requires no headers and no proof of intent. The leaked
credentials grant whatever the instance role permits, often broad
read access to internal resources.

## Severity

- CVSS 3.1 vector: `CVSS:3.1/AV:N/AC:L/PR:N/UI:N/S:C/C:H/I:H/A:N`
- Base score: 10.0 (Critical) -- when the leaked credentials give
  access to customer data buckets / databases via the workload's
  IAM role. Lower for narrowly-scoped roles.
- CWE: CWE-918 -- Server-Side Request Forgery (SSRF)

Variants apply to GCP (`http://metadata.google.internal/`) and
Azure (`http://169.254.169.254/metadata/`); the IMDSv1 designation is
AWS-specific.

## Affected component

Any application that:

- Accepts a URL (or scheme + host + path) from user input.
- Fetches it server-side with a default HTTP client.
- Runs on an EC2 instance with IMDSv1 reachable (default before
  IMDSv2 was made strict).
- Optionally attaches an instance profile with non-trivial IAM
  permissions (S3 read, DynamoDB read, etc.).

Common entry points:

- "Fetch image from URL" / avatar import.
- Webhook target URL configured by tenant.
- Server-side rendering of user-supplied URLs.
- "Fetch sitemap from URL" / link unfurling.

## Reproduction

```text
Setup
  - Workload on EC2 with IMDSv1 enabled (default on older AMIs).
  - Endpoint /api/fetch?url=<url> on the workload, no input
    validation on the URL.

Steps
  1. From a public address, send:
     GET /api/fetch?url=http://169.254.169.254/latest/meta-data/iam/security-credentials/
  2. Response contains the role name (e.g., "app-instance-role").
  3. Send:
     GET /api/fetch?url=http://169.254.169.254/latest/meta-data/iam/security-credentials/app-instance-role
  4. Response contains a JSON object with AccessKeyId, SecretAccessKey,
     Token, and Expiration.
  5. Use the credentials with the AWS CLI / SDK from the attacker
     environment to call APIs the role permits.

Observed
  - Short-lived AWS credentials exfiltrated.
  - Subsequent API calls inherit the workload's IAM permissions.
```

## Root cause

Two failures compose:

1. The application fetches arbitrary URLs without restricting the
   destination. The `http://169.254.169.254/...` request is treated
   the same as any other.
2. IMDSv1 does not require proof of intent. A simple GET to the
   metadata endpoint returns the response. IMDSv2 introduced a token
   handshake that defeats trivial SSRF.

A correct outbound HTTP client validates the resolved destination
against an allowlist (or denylist of private and link-local ranges)
AND respects redirect behaviour so that a 302 to
`169.254.169.254` cannot smuggle the attacker past the check.

## Impact

- Exfiltration of short-lived IAM credentials for the instance role.
- API calls from the attacker against the cloud account with those
  credentials, limited only by the role's permissions.
- Often a stepping stone to broader access if the role can read
  secrets (Secrets Manager, Parameter Store) or assume other roles.
- Audit-log attribution looks like the workload, not the attacker.

## Remediation

1. **Short-term (workaround)**:
   - Enforce IMDSv2 with the metadata service required to use a token
     (set `HttpTokens=required` and `HttpPutResponseHopLimit=1`).
     IMDSv1-only requests are then rejected at the cloud layer.
   - Reduce the instance role to the minimum permissions; rotate any
     credentials that may already be compromised.
2. **Long-term (fix)**:
   - Validate every outbound URL: parse, resolve, reject loopback /
     private / link-local / metadata ranges, reject redirects to
     forbidden ranges, time-bound the resolved address (defend
     against DNS rebinding).
   - Run the outbound HTTP through a sandboxed proxy that enforces an
     egress allowlist; the workload cannot reach metadata even if it
     tries.
   - See [../secure-coding/go/ssrf-net-http.md](../secure-coding/go/ssrf-net-http.md).

## Detection

- SAST: flag uses of HTTP clients that take user-supplied URLs
  without going through a validation helper.
- DAST: include `169.254.169.254`, `[::ffff:127.0.0.1]`,
  `0177.0.0.1`, `metadata.google.internal`, and Azure's `169.254.169.254/metadata/`
  in the SSRF probe set.
- Runtime / VPC flow logs: alert on outbound to the link-local
  metadata range from workload subnets (the workload itself talks to
  metadata, but the volume / pattern of human-triggered requests is
  distinct from agent / SDK polling).
- WAF / egress proxy: deny `Host:` or `:authority` headers naming
  link-local or private addresses.

## References

- CWE-918: <https://cwe.mitre.org/data/definitions/918.html>
- OWASP SSRF Prevention Cheat Sheet: <https://cheatsheetseries.owasp.org/cheatsheets/Server_Side_Request_Forgery_Prevention_Cheat_Sheet.html>
- AWS IMDSv2: <https://docs.aws.amazon.com/AWSEC2/latest/UserGuide/configuring-instance-metadata-service.html>
- GCP metadata server: <https://cloud.google.com/compute/docs/metadata/overview>
- Azure Instance Metadata Service: <https://learn.microsoft.com/en-us/azure/virtual-machines/instance-metadata-service>
- PortSwigger Web Security Academy -- SSRF: <https://portswigger.net/web-security/ssrf>
- `../secure-coding/go/ssrf-net-http.md`
