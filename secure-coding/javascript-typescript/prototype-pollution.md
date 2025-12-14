# Prototype Pollution

## Threat

Code that recursively merges or sets properties from attacker-controlled
JSON can write to `Object.prototype` by traversing the `__proto__`,
`constructor.prototype`, or class `prototype` chains. Subsequent reads of
ordinary objects inherit polluted properties, which often translates to
gadget execution in template engines, command-construction libraries, or
config parsers.

CWE: CWE-1321 (Improperly Controlled Modification of Object Prototype
Attributes). OWASP API Top 10: API8:2023 (Security Misconfiguration).

## Insecure

```javascript
// Recursive merge that walks attacker-supplied keys.
function merge(target, source) {
    for (const k in source) {
        if (typeof source[k] === "object" && source[k] !== null) {
            target[k] = target[k] || {};
            merge(target[k], source[k]);
        } else {
            target[k] = source[k];
        }
    }
    return target;
}

const userInput = JSON.parse(req.body);
const config = merge({}, userInput);

// Subsequent code:
const opts = {};
if (opts.isAdmin) { /* now true because Object.prototype.isAdmin was set */ }
```

A payload like `{"__proto__":{"isAdmin":true}}` or
`{"constructor":{"prototype":{"isAdmin":true}}}` pollutes `Object.prototype`.

## Why it fails

- JavaScript object literals inherit from `Object.prototype`; setting a
  property on the prototype affects every plain object that does not
  shadow that key.
- Recursive helpers that auto-vivify intermediate objects
  (`target[k] || {}`) follow the `__proto__` chain when the source key is
  the literal string `"__proto__"`.

## Secure

Pick one (or all) of:

```javascript
// 1) Reject prototype-chain keys at the boundary.
const FORBIDDEN = new Set(["__proto__", "prototype", "constructor"]);

function safeMerge(target, source) {
    for (const k of Object.keys(source)) {        // own keys only
        if (FORBIDDEN.has(k)) continue;
        const v = source[k];
        if (v && typeof v === "object" && !Array.isArray(v)) {
            target[k] = safeMerge(
                Object.create(null),               // null-prototype
                v,
            );
        } else {
            target[k] = v;
        }
    }
    return target;
}

// 2) Use null-prototype objects everywhere user input is held.
const cfg = Object.create(null);

// 3) Freeze critical prototypes early in the process lifecycle.
Object.freeze(Object.prototype);
Object.freeze(Array.prototype);
```

Library posture:

- `lodash.merge` is safe from prototype pollution since 4.17.21; do
  not use older versions. Use `Object.assign` or `structuredClone` for
  shallow / deep copies of trusted data.
  <!-- TODO: verify the precise patched lodash version for each affected function (merge, set, defaultsDeep) -->
- `Object.assign({}, ...)` is shallow and safe; user-controlled deep
  merge needs explicit guards.
- For JSON parsing of untrusted data into a typed shape, prefer a
  schema validator (Zod, ajv with `additionalProperties: false`) over
  spreading into an object.

## Notes

- Prototype pollution often becomes RCE indirectly: a polluted
  `compileFunction.options` in `eval`-using template engines, a polluted
  `child_process.exec.shell` setting, or a polluted property read by a
  gadget on `Object.prototype` during library bootstrapping.
- Express middleware that uses `req.body` directly with naive merge
  helpers (`hpp`, `qs` with custom options) is a common entry point;
  pin to versions that disable prototype keys (see library docs).
- `qs` parses query strings: `?__proto__[isAdmin]=true` — confirm
  `allowPrototypes: false` (default in recent versions) is not overridden.

## References

- OWASP — Prototype Pollution: <https://owasp.org/www-community/attacks/Prototype_Pollution>
- CWE-1321: <https://cwe.mitre.org/data/definitions/1321.html>
- Node.js security best practices: <https://nodejs.org/en/learn/getting-started/security-best-practices>
- Snyk research: prototype pollution overview: <https://snyk.io/research/>
