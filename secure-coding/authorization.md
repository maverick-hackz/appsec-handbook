# Authorization

## Threat

The application authenticates a user but fails to check that this user is
allowed to perform the requested action on the requested object. The most
common bug class in modern web apps.

CWE: CWE-862 (Missing Authorization), CWE-863 (Incorrect Authorization),
CWE-285 (Improper Authorization), CWE-639 (Authorization Bypass Through
User-Controlled Key). OWASP API Top 10 BOLA (API1:2023) and BFLA (API5:2023).

## Insecure

`GET /api/orders/{id}` looks up the order and returns it. There is an
authentication middleware but no check that `order.owner_id == current_user.id`.

## Why it fails

- Hidden URLs are not access control. Enumerable IDs reveal everything.
- "Frontend hides the button" is not access control. The HTTP endpoint is
  the boundary.
- Role checks at the menu level miss direct API calls.

## Secure

- Enforce authorization on every request that touches a resource, in the
  same layer as data access (repository / service), not the controller.
- Default deny: a new endpoint requires an explicit policy decision before
  it returns data.
- Use a policy-as-code engine for non-trivial rules (Casbin, OPA/Rego,
  Cedar). Keep policies in version control.
- Prefer ABAC (attribute-based) or ReBAC (relationship-based) over a frozen
  RBAC table when the model has tenants, ownership, or sharing.
- Object-level: every `findById` returns the object only if the principal
  has a relationship to it (owner, member of org, role on resource).
- Function-level: a privileged operation checks role/permission server-side
  even when the UI gates the call.
- Use opaque, non-sequential identifiers (UUIDv4 or v7) for resources to
  reduce enumeration impact, but do NOT rely on this as the control.

## Notes

- Authorization tests belong in unit / integration suites: for every endpoint,
  assert that a non-owner / wrong-role principal gets 403 (or 404 to hide
  existence, depending on disclosure policy).
- Cache authorization decisions only with the principal+resource as part of
  the cache key, and a TTL short enough to reflect revocation needs.
- For multi-tenant systems, also enforce isolation at the data layer (row-level
  security in the database). See [architecture/multi-tenancy-isolation.md](../architecture/multi-tenancy-isolation.md).

## References

- OWASP Authorization Cheat Sheet: <https://cheatsheetseries.owasp.org/cheatsheets/Authorization_Cheat_Sheet.html>
- OWASP API Security Top 10 (2023): <https://owasp.org/API-Security/editions/2023/en/0x00-header/>
- CWE-862: <https://cwe.mitre.org/data/definitions/862.html>
- CWE-863: <https://cwe.mitre.org/data/definitions/863.html>
