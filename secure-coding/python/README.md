# Python Secure Coding

Python 3.11+ secure coding patterns. Each file follows the standard template
(Threat, Insecure, Why it fails, Secure, Notes, References).

## Files

- [SQL injection with SQLAlchemy and raw drivers](injection-sql-orm.md) — `psycopg`, `mysqlclient`
- [Insecure deserialization](deserialization-pickle.md) — `pickle`, `yaml.load`, `marshal`
- [SSTI in Jinja2](ssti-jinja.md) — server-side template injection
- [Cryptography library](crypto-cryptography-lib.md) — `cryptography`, `secrets`, `argon2-cffi`
- [Django and Flask defaults](django-flask-defaults.md) — Django 5.x and Flask 3.x security defaults

## Conventions

- Python 3.11+ syntax; type hints by default.
- Standard library where possible; pinned third-party libraries (`cryptography`,
  `argon2-cffi`, `pyjwt`) when stdlib is insufficient.
- Mark uncertain version-specific behaviour with
  `<!-- TODO: verify against <library> v<version> docs -->`.
