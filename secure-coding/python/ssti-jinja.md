# Server-Side Template Injection in Jinja2

## Threat

Rendering an attacker-controlled string AS a template (not WITH a template)
exposes the Python runtime. The classic `{{ self.__init__.__globals__ }}`
gadget walks from a sandboxed expression to `os.popen` or `subprocess`.

CWE: CWE-1336 (Improper Neutralization of Special Elements Used in a Template
Engine). OWASP: A03:2021 (Injection).

## Insecure

```python
from jinja2 import Environment

env = Environment()                                   # autoescape OFF
def render(req):
    template_string = req.args["message"]             # attacker-controlled
    return env.from_string(template_string).render(
            user=req.user)
```

A request such as `?message={{ config.__class__.__init__.__globals__["os"].popen("id").read() }}`
yields the command output.

## Why it fails

- `env.from_string(user_input)` compiles attacker bytes as a template.
- Jinja2's sandbox is opt-in (`SandboxedEnvironment`) and even then is
  defence-in-depth, not a hard boundary.
- Concatenating user input into a static template string before
  rendering has the same effect: `env.from_string(f"Hi {name}")`.

## Secure

```python
from jinja2 import Environment, FileSystemLoader, select_autoescape

env = Environment(
    loader=FileSystemLoader("templates"),
    autoescape=select_autoescape(["html", "htm", "xml"]),
)

def render(req):
    tmpl = env.get_template("greeting.html")          # template name, not body
    return tmpl.render(name=req.args["name"])         # data, not code
```

Rules:

- Templates live on disk and are loaded by name.
- User input is a value passed into `render(...)`, never the template body.
- Auto-escape is on for HTML / XML output.
- Disable raw / safe filters in the project conventions; use `Markup(...)`
  only for known-trusted constants.

If a feature genuinely needs user-supplied templates (rare):

```python
from jinja2.sandbox import SandboxedEnvironment

env = SandboxedEnvironment(
    autoescape=True,
    enable_async=False,
)
# Plus: timeouts, memory limits, disallowed globals, no I/O builtins,
# and rendering in an isolated process with seccomp / nsjail.
```

## Notes

- The same class of bug exists in Mako, Genshi, Django's template
  language (`Template(s).render(Context(...))` on a string), and
  in mail / SMS template features that accept user-edited bodies.
- For markdown / WYSIWYG content, render markdown first to HTML and
  then pass that HTML through a sanitizer (`bleach` with an allowlist),
  never feed the body into a Jinja-style engine.

## References

- OWASP Server-Side Template Injection notes: <https://owasp.org/www-project-web-security-testing-guide/v42/4-Web_Application_Security_Testing/07-Input_Validation_Testing/18-Testing_for_Server-side_Template_Injection>
- PortSwigger Web Security Academy — Server-side template injection: <https://portswigger.net/web-security/server-side-template-injection>
- Jinja2 documentation (autoescape, sandbox): <https://jinja.palletsprojects.com/en/latest/>
- CWE-1336: <https://cwe.mitre.org/data/definitions/1336.html>
