# Finding: Prototype Pollution via Merge

## Summary

A Node.js application uses a recursive merge utility (an older
`lodash.merge` / `defaultsDeep` / a custom helper) to combine
user-supplied JSON with an internal options object. The helper
follows the `__proto__` (or `constructor.prototype`) keys in the
attacker's payload and writes onto `Object.prototype`. Subsequent
reads from any plain object inherit the polluted property; gadget
chains in template engines, command builders, or option-parsing
libraries turn this into bypass or remote code execution.

## Severity

- CVSS 3.1 vector: `CVSS:3.1/AV:N/AC:L/PR:N/UI:N/S:U/C:N/I:H/A:H`
- Base score: 9.1 (Critical) -- mirrors NVD's scoring of the canonical
  lodash `defaultsDeep` CVE.
- CWE: CWE-1321 -- Improperly Controlled Modification of Object
  Prototype Attributes

Reference public vulnerabilities:

- CVE-2018-3721 -- lodash `defaultsDeep`, `merge`, `mergeWith`
  before 4.17.5. CVSS 6.5 (Medium) at NVD.
- CVE-2019-10744 -- lodash `defaultsDeep` before 4.17.12.
  CVSS 9.1 (Critical) at NVD.
- CVE-2020-8203 -- lodash `set`, `setWith`, `update`, etc. before
  4.17.20.

## Affected component

Node.js applications (server-side) that:

- Use lodash `merge`, `defaultsDeep`, `mergeWith`, `set`, `setWith`,
  `update`, or `defaults` against attacker-controlled JSON, in a
  version published before the corresponding patch.
- Use a hand-rolled deep-merge that walks `for ... in` (which
  includes inherited / prototype-named keys) without filtering.
- Use a query-string parser that converts `?__proto__[isAdmin]=1` to
  a nested object and feeds it to a merge helper (`qs` in some
  configurations).

Client-side variants exist in browser-side bundles; impact differs
but the bug class is the same.

## Reproduction

```text
Setup
  - Express app with body-parser; POST /config accepts a JSON body
    and merges it with defaults: const cfg = _.merge({}, body).
  - lodash version <= 4.17.4 (CVE-2018-3721 patch boundary).
  - Downstream code reads cfg.isAdmin (or any property) without
    own-property check.

Steps
  1. Send POST /config with body: {"__proto__":{"isAdmin":true}}
  2. Observe that the merge completes without error.
  3. Send GET /me; downstream handler reads opts.isAdmin from a
     freshly created object.
  4. Observed: opts.isAdmin === true even though opts was created
     with {}; Object.prototype.isAdmin was polluted in step 1.

Code execution variant
  - Some libraries read Function.prototype.constructor.options
    indirectly; pollution of those keys executes attacker-controlled
    code at the next call.
```

## Root cause

Object literals in JavaScript inherit from `Object.prototype`.
A deep-merge that:

1. Iterates with `for (const k in source) { ... }` (which includes
   `__proto__` as a writable key) and
2. Walks into the value when the value is an object

writes to `target.__proto__[...]`, which is `Object.prototype` for a
plain target. Every plain object created after that point inherits
the polluted properties unless it explicitly shadows them.

The bug surfaces wherever a downstream feature reads from an object
without `hasOwnProperty` checks (template engines, command-line
parsers, default option resolution).

## Impact

- Bypass of feature flags / privilege flags read from default
  options.
- Tampering of cached configuration shared across the process.
- Gadget-chained RCE via library-specific paths
  (`child_process.exec` shell flag, `compileFunction` options, etc.).
- Denial of service via pollution of well-known properties used in
  hot paths.

## Remediation

1. **Short-term (workaround)**:
   - Upgrade lodash (or the merge library) to the patched version.
     `lodash >= 4.17.21` is safe for the merge family of functions.
   - Reject prototype-chain keys at the boundary:

     ```javascript
     const FORBIDDEN = new Set(["__proto__", "prototype", "constructor"]);
     for (const k of Object.keys(body)) {
         if (FORBIDDEN.has(k)) throw new Error("invalid key");
     }
     ```

2. **Long-term (fix)**:
   - Use `Object.create(null)` for any object that will hold user
     input; it has no prototype chain.
   - Freeze `Object.prototype` and `Array.prototype` early in the
     process lifecycle: `Object.freeze(Object.prototype)`.
   - For typed inputs, use a schema validator
     (Zod / ajv with `additionalProperties: false`) that converts
     attacker JSON into a known shape; reject the request when the
     shape does not match.
   - See [../secure-coding/javascript-typescript/prototype-pollution.md](../secure-coding/javascript-typescript/prototype-pollution.md).

## Detection

- SAST: flag uses of `_.merge`, `_.defaultsDeep`, `_.mergeWith`,
  `_.set`, and similar against any function argument that touches
  request data.
- SCA: alert on lodash versions vulnerable to CVE-2018-3721 /
  CVE-2019-10744 / CVE-2020-8203 in production dependencies.
- DAST: probe state-changing endpoints with payloads such as
  `{"__proto__":{"polluted":1}}` and read a known endpoint
  afterwards for the polluted property.
- Runtime: instrument `Object.defineProperty` calls on the prototypes
  in development; warn on any non-startup-time writes.

## References

- CVE-2018-3721: <https://nvd.nist.gov/vuln/detail/CVE-2018-3721>
- CVE-2019-10744: <https://nvd.nist.gov/vuln/detail/CVE-2019-10744>
- CVE-2020-8203: <https://nvd.nist.gov/vuln/detail/CVE-2020-8203>
- CWE-1321: <https://cwe.mitre.org/data/definitions/1321.html>
- OWASP -- Prototype Pollution: <https://owasp.org/www-community/attacks/Prototype_Pollution>
- PortSwigger Web Security Academy -- Prototype pollution: <https://portswigger.net/web-security/prototype-pollution>
- Node.js security best practices: <https://nodejs.org/en/learn/getting-started/security-best-practices>
- `../secure-coding/javascript-typescript/prototype-pollution.md`
