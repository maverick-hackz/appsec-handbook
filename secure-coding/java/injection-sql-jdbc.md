# SQL Injection in JDBC / JPA

## Threat

String-concatenated SQL exposes the application to arbitrary query
modification, including data exfiltration, authentication bypass, and
DBMS-level OS command execution on some database engines.

CWE: CWE-89 (Improper Neutralization of Special Elements used in an SQL
Command).

## Insecure

```java
// JDBC
String sql = "SELECT * FROM users WHERE id = " + request.getParameter("id");
try (Statement st = conn.createStatement();
     ResultSet rs = st.executeQuery(sql)) {
    // ...
}

// JPA / Hibernate
String hql = "FROM User WHERE name = '" + name + "'";
em.createQuery(hql, User.class).getResultList();
```

## Why it fails

- Concatenation hands the database engine attacker-controlled SQL tokens.
  `id = 1 OR 1=1 --` bypasses every WHERE.
- Hibernate HQL is SQL-shaped; the same mistake applies. `createQuery`
  with a string template is no safer than `createSQLQuery`.

## Secure

```java
// JDBC: PreparedStatement with positional parameters
String sql = "SELECT id, email FROM users WHERE id = ?";
try (PreparedStatement ps = conn.prepareStatement(sql)) {
    ps.setLong(1, id);
    try (ResultSet rs = ps.executeQuery()) {
        // ...
    }
}

// JPA: named parameters
TypedQuery<User> q = em.createQuery(
        "SELECT u FROM User u WHERE u.name = :name", User.class);
q.setParameter("name", name);
List<User> users = q.getResultList();
```

For dynamic column names or LIMIT / OFFSET values that cannot be bound:
build them from a closed allowlist.

```java
private static final Set<String> ALLOWED_SORT =
        Set.of("id", "created_at", "name");

String sort = ALLOWED_SORT.contains(req) ? req : "id";
String sql = "SELECT id FROM users ORDER BY " + sort + " LIMIT ?";
```

## Notes

- `Statement.executeQuery(sql)` and `EntityManager.createNativeQuery(sql)`
  with concatenated strings are both unsafe. Use `PreparedStatement` or
  the parameterized JPA APIs.
- ORMs do NOT make SQL injection impossible: `@Query(value = "...")` and
  Hibernate `Session.createSQLQuery` allow concatenation just as easily.
- `LIKE` patterns with user input still need parameterization; escape
  `%` / `_` inside the user-supplied fragment if a literal match matters.
- For batch operations, prefer `addBatch()` over building one giant SQL
  string.

## References

- OWASP SQL Injection Prevention Cheat Sheet: <https://cheatsheetseries.owasp.org/cheatsheets/SQL_Injection_Prevention_Cheat_Sheet.html>
- CWE-89: <https://cwe.mitre.org/data/definitions/89.html>
- JDBC tutorial (Oracle): <https://docs.oracle.com/javase/tutorial/jdbc/basics/prepared.html>
- Jakarta Persistence specification: <https://jakarta.ee/specifications/persistence/>
