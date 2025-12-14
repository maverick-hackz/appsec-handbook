# Python Secure Coding

Python 3.11+ secure coding patterns. Each file follows the standard template
(Threat, Insecure, Why it fails, Secure, Notes, References).

## Files

- [injection-sql-orm.md](injection-sql-orm.md) — SQLAlchemy and raw `psycopg` / `mysqlclient`
- [deserialization-pickle.md](deserialization-pickle.md) — `pickle`, `yaml.load`, `marshal`
- [ssti-jinja.md](ssti-jinja.md) — Jinja2 server-side template injection
- [crypto-cryptography-lib.md](crypto-cryptography-lib.md) — `cryptography`, `secrets`, `argon2-cffi`
- [django-flask-defaults.md](django-flask-defaults.md) — Django 5.x and Flask 3.x security defaults

## Conventions

- Python 3.11+ syntax; type hints by default.
- Standard library where possible; pinned third-party libraries (`cryptography`,
  `argon2-cffi`, `pyjwt`) when stdlib is insufficient.
- Mark uncertain version-specific behaviour with
  `<!-- TODO: verify against <library> v<version> docs -->`.
