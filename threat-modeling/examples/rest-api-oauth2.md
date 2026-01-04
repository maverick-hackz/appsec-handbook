# Threat Model: REST API with OAuth 2.0

## System overview

A multi-tenant REST API behind an API gateway. Clients are first-party
SPAs and third-party server-to-server integrations. Identity is
delegated to an OAuth 2.0 / OIDC provider. The API persists resources
in PostgreSQL, publishes domain events to a message bus, and reads
read-models from a cache.

## Assets

| Asset | Sensitivity | Owner |
| --- | --- | --- |
| Customer business data (orders, contacts) | Restricted | Product |
| OAuth refresh tokens for partner apps | Restricted | Platform |
| Service-to-service signing keys (mTLS, JWS) | Restricted | Platform |
| API request logs (with redacted PII) | Confidential | SRE |
| Public OpenAPI schema | Public | Product |

## Trust boundaries

1. `TB-1` Internet -> API gateway (TLS termination, WAF)
2. `TB-2` API gateway -> Application service (mTLS, gateway identity)
3. `TB-3` Application -> PostgreSQL (TLS, scoped DB role, row-level
   security for tenant isolation)
4. `TB-4` Application -> OIDC provider (HTTPS, JWKS validation)
5. `TB-5` Application -> Message bus (TLS, signed envelopes)
6. `TB-6` Tenant A data <-> Tenant B data (logical, enforced in SQL
   row-level security and in code)

## DFD (text form)

```text
[Client SPA] [Partner Server]
       \         /
        \       /
         v     v
==================== TB-1 INTERNET / DMZ ====
         |     |
         v     v
   (API Gateway) ----- bearer token ---> (OIDC Provider)
         |                          (JWKS / userinfo)
         |
==================== TB-2 NAMESPACE BOUNDARY ====
         |
         v   mTLS, signed request hdr
   (Orders API)
       |  |  \
       |  |   \-- publish event ----------> [[Event Bus]]
       |  |
       |  +-- TLS, parameterized SQL -----> [[Postgres]]
       |
       +------ TLS, key=tenant -----------> [[Redis read-model]]
```

## Assumptions

1. OIDC provider is operated by a third party with its own SOC 2; its
   compromise is out of scope here, captured under "supply chain risk
   acceptance".
2. The API gateway terminates TLS using a certificate issued by the
   organisation's CA; clients pin the gateway hostname only.
3. Postgres is in the same Kubernetes cluster network namespace; the
   only path to it is via the application service.
4. Tenant isolation is enforced by `tenant_id` filters in code AND
   PostgreSQL row-level security policies bound to the SET ROLE in use.

## STRIDE analysis

| # | Element | Threat | STRIDE | Mitigation | Status |
| --- | --- | --- | --- | --- | --- |
| 1 | Client SPA | Spoof as a different user | S | OAuth2 Authorization Code + PKCE; refresh-token rotation; reuse detection | Done |
| 2 | Partner server | Impersonate via leaked client credential | S | Client credentials rotated, scoped per partner; rate-limit per `client_id`; require mTLS for high-value scopes | Done |
| 3 | API gateway | Tamper with forwarded request | T | mTLS to API; gateway signs `X-Gateway-Signature` header bound to method+path+body hash | Done |
| 4 | Orders API process | Elevation via missing tenant check | E | Repository layer enforces `tenant_id` from the verified JWT; Postgres RLS as defence in depth; tests assert 403 for cross-tenant fetch | Done |
| 5 | Orders API process | BOLA: `GET /orders/{id}` returns any order | E | `findById` requires `owner.tenant_id == jwt.tenant_id` AND a relationship; integration test covers cross-tenant access | Done |
| 6 | Orders API process | Mass-assignment of `is_admin` flag | E | DTO only carries permitted fields; admin role mutated only via dedicated endpoint with elevated role | Done |
| 7 | TB-1 data flow | TLS strip / downgrade | T, I | HSTS preload; TLS 1.2 minimum; gateway pins HSTS and refuses old cipher suites | Done |
| 8 | Postgres | Direct read by compromised app | I | Encryption at rest (KMS-managed key), audit logging on DB; rotate role passwords via Vault dynamic secrets | Done |
| 9 | Event bus | Replay of stale event | T | Producer signs envelope (`alg=EdDSA`), consumer verifies; `event_id` deduplicated within 24 h window | Done |
| 10 | Orders API process | DoS via expensive query | D | Query timeout 5 s; per-tenant rate limit at gateway; LIMIT clamp to 100 in repository | Done |
| 11 | OIDC provider | Spoofed `iss` / wrong `aud` | S | API verifies `iss`, `aud`, `azp`, `exp`, `iat` on every request; key rotation honoured via JWKS with 5-min cache | Done |
| 12 | Application logs | Disclosure of PII | I | Field-level redaction in the logger; review on schema additions; logs encrypted at rest in central store | Partial — see Open questions |

## Residual risks

- Compromise of the OIDC provider grants the attacker the ability to
  forge access tokens for any tenant. Out of scope here; depends on
  the provider's controls and on the speed of key revocation.
- A long-lived refresh token issued to a partner is a high-impact
  secret. Even with rotation and reuse detection, a partner
  application's compromise yields immediate access until the token
  expires.
- Tenant isolation depends on correct `tenant_id` propagation through
  every async pathway (events, batch jobs). Reviews of new async paths
  are mandatory.

## Open questions

1. Is the field-level redaction in the logger covered by a unit test
   that fails when a new sensitive field is added? Acceptance: a CI
   check that flags log statements referencing fields tagged
   `@Sensitive`.
2. What is the retention policy for raw events on the event bus, and
   does it satisfy the data-residency requirement on EU tenants?
3. Are mTLS certificates rotated automatically (SPIFFE / spiffe-helper)
   or manually? If manual, what is the rotation cadence?

## References

- OWASP API Security Top 10 (2023): <https://owasp.org/API-Security/editions/2023/en/0x00-header/>
- OWASP Threat Modeling Cheat Sheet: <https://cheatsheetseries.owasp.org/cheatsheets/Threat_Modeling_Cheat_Sheet.html>
- RFC 6749 (OAuth 2.0): <https://datatracker.ietf.org/doc/html/rfc6749>
- RFC 9700 (OAuth 2.0 Security BCP): <https://datatracker.ietf.org/doc/html/rfc9700>
- OpenID Connect Core: <https://openid.net/specs/openid-connect-core-1_0.html>
- PostgreSQL Row Security Policies: <https://www.postgresql.org/docs/current/ddl-rowsecurity.html>
