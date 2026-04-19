# Multi-Tenancy Isolation

Multi-tenant systems serve multiple customers (tenants) from the same
application instance. The isolation model decides what can go wrong
between tenants and how badly.

## Isolation spectrum

| Model | Compute | Storage | Identity | Strongest isolation |
| --- | --- | --- | --- | --- |
| Shared everything | One process, all tenants | Single DB, `tenant_id` column | Single auth provider | Code; weakest practical |
| Schema per tenant | One process | Same DB, schema-per-tenant | Single auth provider | DB schema; row mistakes contained |
| Database per tenant | One process | One DB per tenant | Single auth provider | Database boundary |
| Instance per tenant | One container / VM per tenant | Per-tenant DB | Single auth provider | OS / VM boundary |
| Cluster per tenant | Dedicated cluster | Dedicated storage | Per-tenant auth | Network boundary |

Pick the highest level the business can afford for the data tier in
question. Different data tiers can pick different models within the
same product (e.g., logs at shared-everything, customer data at
database-per-tenant).

## "Shared everything" -- defensive controls

If the business model requires shared infrastructure for cost, the
controls below are mandatory rather than optional.

### Data layer

- Every table that holds tenant data has a `tenant_id` column.
- PostgreSQL: row-level security (RLS) policy keyed on a session
  variable; SET the variable from the authenticated principal at
  connection acquisition.
- Indexes include `tenant_id` as the first column for the common
  access patterns.
- Queries that omit `tenant_id` in the WHERE clause raise an
  exception (linter / wrapper).

```sql
-- Postgres: example RLS
ALTER TABLE orders ENABLE ROW LEVEL SECURITY;
CREATE POLICY tenant_isolation ON orders
    USING (tenant_id = current_setting('app.tenant_id')::uuid);
-- In the connection lifecycle:
-- SET app.tenant_id = '<uuid from verified JWT>';
```

### Application layer

- Tenant context comes from the verified JWT or session, never from
  request input.
- Repository / service layer encapsulates tenant scoping; controllers
  never assemble tenant-aware queries directly.
- Cache keys include `tenant_id`. Otherwise a poisoned cache entry
  becomes a cross-tenant disclosure.
- Bulk operations (export, search) accept a `tenant_id` filter as a
  mandatory parameter that is set by the framework, not by the
  caller.

### Identity

- Tokens carry `tenant_id` (`tid`) as a verified claim.
- Authentication failure responses do not reveal which tenant the
  attempted user belongs to.
- Cross-tenant administrative roles exist only in a separate
  "support" identity track; switching tenants is an explicit,
  audited action.

### Noisy neighbour

- Per-tenant quotas on CPU, memory, request rate, storage, and
  external-API calls.
- Bulkheads at the gateway: a tenant in a runaway loop cannot
  exhaust capacity meant for other tenants.
- Long-running operations (export, search) run in separate workers
  with per-tenant queue depth.

## "Database per tenant"

- The connection pool is keyed on tenant; a single process can serve
  multiple tenants but each query goes to the tenant-specific
  database.
- BYOK (customer-managed keys) become straightforward: the DB's
  encryption key per tenant is a KMS CMK the customer owns.
- Migration tooling runs per-tenant in parallel; capacity planning
  considers the long-tail tenants separately from the average.

## "Cluster per tenant"

Reserved for the highest-blast-radius tenants (large enterprise,
regulated industries):

- Dedicated cluster, network, IAM, and secret store.
- Operational cost rises; reserve for the data classification that
  justifies it.

## Common attacks

### BOLA / IDOR across tenants

User in tenant A requests `/orders/abc-123` belonging to tenant B.

- Primary defence: tenant-aware repository layer; RLS in DB.
- Test: integration tests assert 403 / 404 on cross-tenant fetch
  for every endpoint.

### Cache poisoning across tenants

Cache key omits tenant; a write from one tenant becomes a read for
another.

- Primary defence: include `tenant_id` in every cache key.
- Detection: cache key audit on each new caching addition.

### Side-channel timing across tenants

A query that touches another tenant's data has measurable
performance characteristics.

- Primary defence: RLS prevents the touch in the first place;
  query-timeout caps make timing leakage less useful.

### Privilege escalation via admin / support account

A support engineer with cross-tenant read switches into a tenant
without audit; or the support role accidentally allows writes.

- Primary defence: explicit "impersonate" action with auditing;
  read-only support role distinct from write-capable roles.

## Validation

For every endpoint, the test suite should:

1. Create two tenants A and B.
2. Authenticate as a user of A.
3. Attempt the operation against a resource in B.
4. Assert 403 / 404 (per disclosure policy).

This test scales: a fixture creates the two tenants once; per-endpoint
tests are short.

## References

- OWASP Top 10 (2025) A01 (Broken Access Control): <https://owasp.org/Top10/>
- OWASP API Security Top 10 (2023) API1 (BOLA): <https://owasp.org/API-Security/editions/2023/en/0xa1-broken-object-level-authorization/>
- PostgreSQL Row Security: <https://www.postgresql.org/docs/current/ddl-rowsecurity.html>
- NIST SP 800-145 (Cloud Computing definitions, including multi-tenancy): <https://csrc.nist.gov/publications/detail/sp/800-145/final>
- CSA Cloud Controls Matrix (multi-tenancy controls): <https://cloudsecurityalliance.org/research/cloud-controls-matrix>
