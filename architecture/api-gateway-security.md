# API Gateway Security

The API gateway is the policy enforcement point on the edge: it
terminates TLS, authenticates the caller, applies rate limits and
quotas, validates the request shape, and forwards to a backend. A
well-configured gateway eliminates a class of bugs from every service
behind it.

## Responsibilities

| Layer | Responsibility |
| --- | --- |
| Transport | TLS termination; HSTS; cipher policy |
| Identity | Validate access token (JWT or opaque); enforce algorithm pin; populate principal context |
| Authorization | Coarse-grained policy (which token type can hit which route); fine-grained left to the service |
| Schema | Validate the request against OpenAPI / GraphQL schema; reject unknown fields |
| Rate limit | Per principal AND per IP / ASN |
| Quotas | Per tenant; longer-window aggregate caps |
| Headers | Strip / pin sensitive headers; inject signed gateway identity for downstream verification |
| Logging | Structured log per request with correlation ID; sample full body only with redaction |

## Concrete patterns

### TLS termination

- TLS 1.3; TLS 1.2 minimum during migration. Disable everything older.
- Cipher suites: modern profile (Mozilla "Intermediate" or "Modern").
- HSTS with `max-age >= 31536000; includeSubDomains; preload`.
- OCSP stapling enabled; certificate from a public CA for external
  endpoints.

### Identity

- JWT verification pins the algorithm (RS256 / ES256 / EdDSA).
- Reject `alg=none`; pin the issuer; verify `aud` against the gateway's
  identifier; honour `nbf`, `iat`, `exp`.
- Cache the JWKS for a short TTL (5-15 minutes); fail closed on
  fetch failure with a slightly longer fallback.
- Authentication failure: respond `401` with a generic body; no
  details about why the token failed.

### Request signing for downstream

After verifying the caller, the gateway re-issues a signed envelope
the downstream service can verify cheaply:

```text
X-Gateway-Identity: gw-edge-01
X-Gateway-Signature: <ed25519 over canonical request + timestamp>
X-Principal-Id: <subject from access token>
X-Tenant-Id: <claim from access token>
X-Request-Id: <ulid>
```

The downstream service:

1. Verifies `X-Gateway-Signature` -- if invalid, the request did not
   come from the gateway (defends against direct backend access).
2. Trusts `X-Principal-Id` and `X-Tenant-Id` only after step 1.
3. Records `X-Request-Id` in every log line.

### Schema validation

- OpenAPI 3.x for REST; the gateway has the schema loaded.
- Reject request bodies that:
  - Exceed a size limit.
  - Contain unknown fields (set `additionalProperties: false` in the
    schema).
  - Violate type / format / range constraints.
- For GraphQL: depth limit, complexity / cost limits, introspection
  policy (disabled in production for non-public schemas).

### Rate limiting

- Token bucket or leaky bucket per principal AND per IP / ASN.
- Limits scale by route: read-heavy endpoints get higher limits than
  state-changing ones.
- Per-tenant quotas at a longer window (per hour, per day).
- Distinguish "throttling" (`429 Too Many Requests` with `Retry-After`)
  from "abuse" (`403` or hard ban).

### Header hygiene

- Strip every request header the gateway does not need to pass
  through. Maintain an allowlist, not a denylist.
- Inject `Strict-Transport-Security`, `X-Content-Type-Options: nosniff`,
  `Referrer-Policy`, `Content-Security-Policy` on responses where the
  service does not.

## Anti-patterns

- A "passthrough" gateway with no token validation. The backend
  becomes the only line of defence and inherits every gateway-class
  control.
- Per-route allow lists with `*` for some routes "for the rollout".
  Either the route is authorized or it is not; remove the asterisk
  before merging.
- Long-lived per-user API keys at the gateway. Use short-lived OAuth
  tokens, or scoped client credentials with rotation.
- Logging full request and response bodies for sensitive endpoints
  without redaction. The gateway log is a high-value compromise
  target.

## Reference architectures

- Cloud-native: NGINX Ingress / Istio Gateway / Envoy Gateway / Kong
  / Tyk -- pick one and standardise the policy bundle.
- Serverless: AWS API Gateway with a Lambda authorizer; GCP API
  Gateway; Azure API Management.
- Self-hosted: Envoy with WASM extensions; HAProxy with Lua filters.

For service-to-service inside the cluster, mTLS via a mesh (Linkerd,
Istio) covers most of the same ground without per-route gateway
config. See [mtls-patterns.md](mtls-patterns.md).

## References

- OWASP API Security Top 10 (2023): <https://owasp.org/API-Security/editions/2023/en/0x00-header/>
- OWASP API Security Cheat Sheet: <https://cheatsheetseries.owasp.org/cheatsheets/REST_Security_Cheat_Sheet.html>
- NIST SP 800-95 (Web service security guidelines): <https://csrc.nist.gov/publications/detail/sp/800-95/final>
- Mozilla TLS configuration profiles: <https://wiki.mozilla.org/Security/Server_Side_TLS>
- OpenAPI Specification: <https://swagger.io/specification/>
