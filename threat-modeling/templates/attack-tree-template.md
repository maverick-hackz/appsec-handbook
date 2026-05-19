# Attack Tree Template

A tree with the attacker's goal at the root, sub-goals as internal
nodes, and concrete attack steps as leaves. Nodes are annotated to
expose the cheapest path.

## Example: "Exfiltrate another tenant's data from a SaaS platform"

```text
GOAL: Read records belonging to a target tenant the attacker is not a member of
|
+-- OR: Become an authenticated user of the target tenant
|       |
|       +-- Phish a target-tenant employee                   [cost=L, skill=L, detect=M]
|       +-- Reuse password from a public breach              [cost=L, skill=L, detect=M]
|       +-- Steal session cookie via XSS                     [cost=M, skill=M, detect=H]
|       +-- AND: Defeat MFA
|              +-- SIM swap                                  [cost=M, skill=M, detect=L]
|              +-- TOTP phishing in real time                [cost=M, skill=M, detect=M]
|
+-- OR: Exploit cross-tenant access in the application
|       |
|       +-- BOLA on /api/records/{id} (no tenant check)      [cost=L, skill=L, detect=H]
|       +-- SQLi that bypasses tenant_id filter              [cost=M, skill=M, detect=H]
|       +-- Cache key collision across tenants               [cost=M, skill=M, detect=M]
|       +-- Path traversal in shared object storage          [cost=M, skill=M, detect=M]
|
+-- OR: Compromise the underlying data store directly
        |
        +-- SQLi in an internal reporting endpoint           [cost=H, skill=H, detect=H]
        +-- Compromise an SRE workstation with DB creds      [cost=H, skill=H, detect=L]
        +-- Insider with cross-tenant DBA role abuses access [cost=L, skill=L, detect=L]
```

## Notation conventions

- `OR` nodes: any one child achieves the parent. Default for branches
  that present alternative paths.
- `AND` nodes: all children must succeed. Mark explicitly; default
  reading is OR.
- Leaves: concrete attacks the team can recognise and mitigate.
- Annotations on leaves and internal nodes:
  - `cost`: L / M / H for attacker effort (time, resources, and risk
    to the attacker).
  - `skill`: L / M / H for required attacker capability.
  - `detect`: L / M / H for likelihood the system detects the attempt.
  - Add `mitigation: <ID>` once mitigations are mapped.

Quantitative variants (probability per year, expected loss) work
when the program has the data to populate them; otherwise the
L/M/H scale is enough.

## How to read

The cheapest path is the lowest cumulative cost on any OR branch.
Mitigations should target the cheapest paths first; making one
expensive path cheaper does not help.

## Output integration

- Each mitigation is tracked in the same backlog as STRIDE
  mitigations; carry the leaf ID into the ticket.
- For high-value assets, refresh the tree when a leaf's `detect`
  changes (a new alert deployed) or when a leaf becomes infeasible
  (a control retired).

## References

- Bruce Schneier — Attack Trees (Dr. Dobb's, Dec 1999): <https://www.schneier.com/academic/archives/1999/12/attack_trees.html>
- Adam Shostack — Threat Modeling: Designing for Security (Wiley, 2014), Chapter 4
- Mauw and Oostdijk — Foundations of Attack Trees: <https://satoss.uni.lu/members/sjouke/papers/MaOo05.pdf>
