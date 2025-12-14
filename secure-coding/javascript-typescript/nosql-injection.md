# NoSQL Injection (MongoDB-flavoured)

## Threat

MongoDB queries are JSON objects. When the framework deserializes a
request body or query string into JavaScript objects without filtering,
an attacker can substitute query operators (`$gt`, `$ne`, `$where`,
`$expr`, `$regex`) for primitive values.

CWE: CWE-943 (Improper Neutralization of Special Elements in Data
Query Logic). OWASP A03:2021 (Injection).

## Insecure

```javascript
// Express + Mongoose: req.body is parsed JSON.
app.post("/login", async (req, res) => {
    const { username, password } = req.body;
    const user = await User.findOne({ username, password });
    if (!user) return res.status(401).end();
    // ...
});
```

A request body of `{ "username": "alice", "password": { "$ne": null } }`
matches any user with a non-null password.

```javascript
// Query string with qs (Express default since v4): nested objects allowed.
// GET /search?name[$ne]=
const results = await User.find({ name: req.query.name });
```

```javascript
// $where with attacker control
await User.find({ $where: `this.role === '${role}'` });
```

## Why it fails

- `findOne({ username, password })` compares using the operator embedded
  in the value when the value is itself an operator object.
- `qs` parses bracket notation into nested objects (`name[$ne]=` becomes
  `{ name: { $ne: "" } }`), so query-string injection is just as easy
  as body injection.
- `$where` and `$function` evaluate JavaScript server-side; concatenation
  produces script injection in addition to data injection.

## Secure

- Hash passwords; never query by password equality. Look up by username,
  then verify the hash:

```javascript
const user = await User.findOne({ username: req.body.username });
if (!user) return generic401(res);
const ok = await argon2.verify(user.passwordHash, req.body.password);
if (!ok) return generic401(res);
```

- Validate request shape with a schema before it touches the DB:

```javascript
import { z } from "zod";

const LoginSchema = z.object({
    username: z.string().min(1).max(64),
    password: z.string().min(1).max(256),
});
const { username, password } = LoginSchema.parse(req.body);
```

- Coerce expected primitives explicitly:

```javascript
const id = String(req.query.id);                      // forces primitive
await User.findById(id);
```

- Avoid `$where` and `$function` on attacker-controlled data. If
  dynamic logic is required, build the query object from a closed set
  of operators that the application picks, not the user.

- Configure the Express query parser to refuse nested objects on the
  endpoints that do not need them:

```javascript
app.set("query parser", "simple");                    // disables qs nesting
```

- Mongoose-specific: `mongoose-sanitize` (or `express-mongo-sanitize`)
  strips keys beginning with `$` and `.` from request inputs at the
  middleware layer. Belt-and-braces with schema validation.

## Notes

- The same class of bug exists in other operator-rich query languages:
  Elasticsearch DSL, Redis JSONPath, GraphQL filters that proxy to
  Mongo.
- Authorization checks must still run AFTER the schema validates the
  shape, on the resolved object (not the query).
- Logging the raw request body during incident response: redact keys
  matching `password`, `token`, `secret`.

## References

- OWASP — NoSQL Injection: <https://owasp.org/www-community/Injection_Flaws>
- MongoDB Operator Restrictions / query operators: <https://www.mongodb.com/docs/manual/reference/operator/query/>
- `express-mongo-sanitize`: <https://github.com/fiznool/express-mongo-sanitize>
- CWE-943: <https://cwe.mitre.org/data/definitions/943.html>
