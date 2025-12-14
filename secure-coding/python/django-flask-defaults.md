# Django and Flask Security Defaults

## Threat

Both frameworks ship sensible defaults that get overridden during
development. `DEBUG = True`, `ALLOWED_HOSTS = ["*"]`, disabled CSRF in
Flask views, and missing security headers are the usual production
landmines.

CWE: CWE-200 (Information Exposure), CWE-352 (CSRF), CWE-693 (Protection
Mechanism Failure), CWE-1004 (Sensitive Cookie Without HttpOnly).

## Django (5.x) checklist

```python
# settings.py — production
DEBUG = False
ALLOWED_HOSTS = ["app.example.com"]
SECRET_KEY = os.environ["DJANGO_SECRET_KEY"]            # not in source

# HTTPS
SECURE_PROXY_SSL_HEADER = ("HTTP_X_FORWARDED_PROTO", "https")
SECURE_SSL_REDIRECT = True
SESSION_COOKIE_SECURE = True
CSRF_COOKIE_SECURE = True
SECURE_HSTS_SECONDS = 31_536_000                        # 1 year
SECURE_HSTS_INCLUDE_SUBDOMAINS = True
SECURE_HSTS_PRELOAD = True

# Other headers / cookies
SECURE_REFERRER_POLICY = "strict-origin-when-cross-origin"
SESSION_COOKIE_HTTPONLY = True
CSRF_COOKIE_HTTPONLY = True
SESSION_COOKIE_SAMESITE = "Lax"
X_FRAME_OPTIONS = "DENY"

# Content Security Policy via django-csp:
CSP_DEFAULT_SRC = ("'self'",)
CSP_OBJECT_SRC = ("'none'",)
CSP_BASE_URI = ("'self'",)

# Password hashing — Argon2 first; bcrypt as fallback for legacy.
PASSWORD_HASHERS = [
    "django.contrib.auth.hashers.Argon2PasswordHasher",
    "django.contrib.auth.hashers.PBKDF2PasswordHasher",
    "django.contrib.auth.hashers.BCryptSHA256PasswordHasher",
]

# Logging — never log secrets / tokens.
LOGGING = {...}
```

Run `python manage.py check --deploy` before each release; it surfaces
every misconfiguration above.

## Flask (3.x) checklist

```python
import os
from flask import Flask
from flask_wtf import CSRFProtect
from flask_talisman import Talisman

app = Flask(__name__)
app.config.update(
    SECRET_KEY=os.environ["FLASK_SECRET_KEY"],
    SESSION_COOKIE_SECURE=True,
    SESSION_COOKIE_HTTPONLY=True,
    SESSION_COOKIE_SAMESITE="Lax",
    PERMANENT_SESSION_LIFETIME=3600,
    PREFERRED_URL_SCHEME="https",
)

CSRFProtect(app)                                         # enable globally

Talisman(
    app,
    force_https=True,
    strict_transport_security=True,
    strict_transport_security_max_age=31_536_000,
    strict_transport_security_include_subdomains=True,
    strict_transport_security_preload=True,
    content_security_policy={
        "default-src": ["'self'"],
        "object-src": ["'none'"],
        "base-uri": ["'self'"],
    },
    referrer_policy="strict-origin-when-cross-origin",
    frame_options="DENY",
)
```

Templates render with `flask.render_template(...)` from disk; auto-escape
is on for `.html` / `.htm` / `.xml` / `.xhtml` by default.
For HTML built in Python, use `markupsafe.escape(...)` rather than `+`.

## Why misconfigurations fail

- `DEBUG = True` exposes the WSGI environment, code snippets, and an
  interactive console on errors.
- `ALLOWED_HOSTS = ["*"]` accepts Host-header forgery, enabling
  password-reset poisoning.
- A missing `SECURE_PROXY_SSL_HEADER` behind a TLS-terminating proxy
  makes the application believe it speaks HTTP; cookies set without
  `Secure` end up on the wire as plaintext on a redirect.
- Flask views decorated with `@csrf.exempt` without a matching auth
  scheme (mTLS, bearer-only) are CSRF-vulnerable when cookies are
  present.

## Notes

- For SPAs talking to a Django REST API, prefer bearer tokens with a
  short TTL and refresh tokens with rotation; if cookies are used,
  combine `SameSite=Strict` (or `Lax`) with a CSRF token on
  state-changing requests.
- `pip-audit` and `safety` flag known-vulnerable dependencies; integrate
  one into CI. See [../../devsecops/ci-templates/github-actions/sca-trivy-fs.yml](../../devsecops/ci-templates/github-actions/sca-trivy-fs.yml).
- Pin `Content-Security-Policy` to `'self'` plus a nonce/hash allowlist
  for inline scripts; `unsafe-inline` defeats the policy.

## References

- Django security overview: <https://docs.djangoproject.com/en/stable/topics/security/>
- Django deployment checklist: <https://docs.djangoproject.com/en/stable/howto/deployment/checklist/>
- Flask security considerations: <https://flask.palletsprojects.com/en/stable/web-security/>
- OWASP Secure Headers Project: <https://owasp.org/www-project-secure-headers/>
- OWASP Django Security Cheat Sheet: <https://cheatsheetseries.owasp.org/cheatsheets/Django_Security_Cheat_Sheet.html>
