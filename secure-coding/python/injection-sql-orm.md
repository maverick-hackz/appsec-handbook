# SQL Injection with SQLAlchemy and Raw Drivers

## Threat

Any string-built SQL — through `psycopg`, `sqlite3`, `mysqlclient`,
SQLAlchemy `text(...)`, or Django `raw(...)` — exposes the application to
SQL injection. ORMs do not prevent it when the developer drops back to a
string.

CWE: CWE-89 (Improper Neutralization of Special Elements used in an SQL
Command).

## Insecure

```python
# psycopg, sqlite3 — Python string formatting into the SQL
cur.execute(f"SELECT * FROM users WHERE id = {user_id}")
cur.execute("SELECT * FROM users WHERE id = %s" % user_id)
cur.execute("SELECT * FROM users WHERE id = " + str(user_id))

# SQLAlchemy Core — text() with f-string
session.execute(text(f"SELECT * FROM users WHERE name = '{name}'"))

# Django ORM
User.objects.raw(f"SELECT * FROM users WHERE id = {uid}")
```

## Why it fails

- `%s` in DB-API `execute()` is the placeholder syntax — it is NOT
  Python's `%` operator. `"... = %s" % uid` substitutes BEFORE handing
  the string to the driver, which then receives the literal value
  inlined into the SQL.
- f-strings and `+` concatenation bypass every safe API.
- ORMs expose `text()`, `raw()`, and `execute()` for cases the typed API
  cannot express; both still need bound parameters.

## Secure

```python
# psycopg / sqlite3 / mysqlclient — driver placeholders (DB-API 2.0)
cur.execute("SELECT id, email FROM users WHERE id = %s", (user_id,))
cur.execute("SELECT id, email FROM users WHERE id = ?", (user_id,))   # sqlite3

# SQLAlchemy Core
session.execute(
    text("SELECT id FROM users WHERE name = :name"),
    {"name": name},
)

# SQLAlchemy ORM (typed API)
session.scalars(select(User).where(User.name == name)).all()

# Django ORM
User.objects.filter(id=uid)
User.objects.raw("SELECT * FROM users WHERE id = %s", [uid])
```

For dynamic column or table names that cannot be parameterized, validate
against an allowlist:

```python
ALLOWED_SORT = {"id", "created_at", "name"}
sort = req_sort if req_sort in ALLOWED_SORT else "id"
cur.execute(f"SELECT id FROM users ORDER BY {sort} LIMIT %s", (limit,))
```

## Notes

- Different drivers use different placeholder syntaxes: `?` for sqlite3,
  `%s` for psycopg / mysqlclient, `:name` for SQLAlchemy `text()`.
  Mixing them produces a runtime error, which is helpful — but only after
  exposure to the wrong query first.
- `LIKE` patterns still need parameters; escape `%` / `_` in the
  user-supplied fragment if literal characters matter.
- Audit `.filter(<raw>)`, `.extra(...)` (deprecated in Django but present
  in legacy code), and `select_for_update(...)` calls that include raw
  fragments.
- For DB migrations and admin scripts, the same rules apply.

## References

- OWASP SQL Injection Prevention Cheat Sheet: <https://cheatsheetseries.owasp.org/cheatsheets/SQL_Injection_Prevention_Cheat_Sheet.html>
- CWE-89: <https://cwe.mitre.org/data/definitions/89.html>
- PEP 249 (Python DB-API 2.0): <https://peps.python.org/pep-0249/>
- SQLAlchemy textual SQL guide: <https://docs.sqlalchemy.org/en/20/core/tutorial.html#using-textual-sql>
- Django SQL injection guidance: <https://docs.djangoproject.com/en/stable/topics/security/#sql-injection-protection>
