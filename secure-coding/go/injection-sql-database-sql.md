# SQL Injection with `database/sql`

## Threat

`database/sql` exposes both safe and unsafe APIs through similar method
names. `Query(sql, args...)` parameterizes; `Query(fmt.Sprintf(...))`
does not. Compile-time constants make the unsafe path indistinguishable
from the safe one without reading the code.

CWE: CWE-89 (Improper Neutralization of Special Elements used in an SQL
Command).

## Insecure

```go
// String concatenation
rows, err := db.Query("SELECT id FROM users WHERE name = '" + name + "'")

// Sprintf
rows, err := db.Query(fmt.Sprintf(
    "SELECT id FROM users WHERE id = %d", uid))

// ORM with raw SQL: GORM
db.Raw("SELECT * FROM users WHERE name = '" + name + "'").Scan(&users)
```

## Why it fails

- `Query(sql)` ignores any subsequent `args ...interface{}` if the SQL
  has no placeholders. Concatenation produces the unsafe SQL itself.
- The placeholder syntax is driver-specific (`?` for MySQL/SQLite, `$1`
  for PostgreSQL, `@p1` for some MS-SQL drivers). Mixing them produces
  a confusing runtime error rather than silent injection — useful, but
  not a defence.

## Secure

```go
// Parameterized query — driver substitutes the placeholder.
var id int64
err := db.QueryRowContext(
    ctx,
    "SELECT id FROM users WHERE name = ? LIMIT 1",        // MySQL / SQLite
    name,
).Scan(&id)

err := db.QueryRowContext(
    ctx,
    "SELECT id FROM users WHERE name = $1 LIMIT 1",        // PostgreSQL
    name,
).Scan(&id)

// Prepared once, executed many.
stmt, err := db.PrepareContext(ctx,
    "INSERT INTO audit (actor, action) VALUES (?, ?)")
defer stmt.Close()
for _, e := range events {
    if _, err := stmt.ExecContext(ctx, e.Actor, e.Action); err != nil {
        return err
    }
}

// GORM with bound parameters
db.Where("name = ?", name).Find(&users)
db.Raw("SELECT id FROM users WHERE name = ?", name).Scan(&users)
```

Dynamic column names or `ORDER BY` values that cannot be bound — validate
against an allowlist:

```go
var allowedSort = map[string]struct{}{
    "id": {}, "created_at": {}, "name": {},
}

sort, ok := allowedSort[req.Sort]
if !ok {
    sort = "id"
}
q := fmt.Sprintf("SELECT id FROM users ORDER BY %s LIMIT ?", sort)
rows, err := db.QueryContext(ctx, q, req.Limit)
```

## Notes

- Pass a `context.Context` and use `*Context` method variants so canceled
  requests release connections promptly.
- `database/sql` does not protect against SQL injection that lives
  inside a stored-procedure body. Audit procedures separately.
- `LIKE` patterns still need parameterization; escape `%` / `_` if a
  literal match matters.
- For multi-statement SQL (some drivers permit `;` separation), keep
  each statement parameterized; do not pass the whole batch through a
  format string.

## References

- OWASP SQL Injection Prevention Cheat Sheet: <https://cheatsheetseries.owasp.org/cheatsheets/SQL_Injection_Prevention_Cheat_Sheet.html>
- CWE-89: <https://cwe.mitre.org/data/definitions/89.html>
- `database/sql` package: <https://pkg.go.dev/database/sql>
- Go Wiki — SQL Database Drivers: <https://github.com/golang/go/wiki/SQLDrivers>
