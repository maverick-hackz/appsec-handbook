# JavaScript and TypeScript Secure Coding

Node 20+ and modern browser secure coding patterns. Each file follows the
standard template (Threat, Insecure, Why it fails, Secure, Notes, References).

## Files

- [Prototype pollution](prototype-pollution.md) — `Object.prototype` writes via merge / set helpers
- [XSS in React and Vue](xss-react-vue.md) — template auto-escape gaps
- [NoSQL injection](nosql-injection.md) — MongoDB query-operator injection
- [JWT handling](jwt-handling.md) — `alg=none`, key confusion, library pitfalls
- [Node.js supply chain](node-supply-chain.md) — `npm`, lockfiles, provenance, audit

## Conventions

- Targeting Node.js 20 LTS (or later) and TypeScript 5+.
- React 18+, Vue 3+, Express 4+, Fastify 4+.
- Mark uncertain version-specific behaviour with
  `<!-- TODO: verify against <library> v<version> docs -->`.
