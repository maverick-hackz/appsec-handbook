# DFD Conventions

A Data Flow Diagram (DFD) shows how data moves through a system. It
is the substrate STRIDE walks. Keep the diagram small enough to fit
on one screen; if it does not, split by service or trust boundary.

## Elements

| Element | Notation in text form | Notation on a whiteboard |
| --- | --- | --- |
| External entity | `[User]` square brackets | Rectangle |
| Process | `(API)` parentheses | Rounded rectangle or circle |
| Data flow | `-->` arrow with label | Labeled arrow |
| Data store | `[[DB]]` doubled brackets | Two horizontal parallel lines |
| Trust boundary | `===` row of equals across flows | Dashed line cutting the flow |

This handbook uses the text form throughout examples so models can be
diffed in git.

## Text DFD example

```text
[User]
   |
   |  HTTPS, OAuth2 access token
   v
====================== INTERNET / DMZ BOUNDARY ===
   |
   v
(API Gateway)
   |
   |  mTLS, request signed by gateway identity
   v
====================== KUBERNETES NAMESPACE ===
   |
   v
(Orders Service) -- TLS, parameterized SQL --> [[Orders DB]]
   |
   |  publish: order.events (TLS, signed)
   v
[[Event Bus]]
```

## Conventions

- One direction per arrow. If data flows both ways on the same channel,
  draw two arrows or annotate "request / response".
- Label every flow with the transport (HTTPS, mTLS, gRPC) AND the
  authentication mechanism (bearer token, mTLS cert, API key).
- Number trust boundaries (`TB-1`, `TB-2`) when there are more than
  two; reference numbers in the STRIDE table.
- Distinguish "data store" from "process". A managed database is a
  store; an authorization service the team owns is a process even if
  it is "just storage" of policy.
- Keep external dependencies (third-party APIs) as external entities,
  not as processes, even if they have rich behaviour. The team does
  not control them.

## Trust boundaries

A trust boundary is anywhere the system stops trusting the source. Each
crossing is the spot where validation, authentication, and authorization
have to be re-verified.

Examples of trust boundaries:

- Public internet -> DMZ
- DMZ -> internal network
- Kubernetes namespace A -> namespace B
- Customer tenant A -> customer tenant B
- Application process -> the database (when DB lives in a different
  privilege domain)
- CI build environment -> production deployment target

Flows that cross a trust boundary should be re-numbered in the
STRIDE table; the threats on those flows are typically higher
impact than the intra-zone ones.

## What NOT to put in the DFD

- Implementation details (functions, classes). The DFD is at the
  service / component granularity.
- Every transient cache or in-memory queue. Include only the data
  stores that survive the request.
- Sequence steps. A DFD shows topology, not order. Use a sequence
  diagram for protocol flows.

## References

- Adam Shostack — Threat Modeling: Designing for Security (Wiley, 2014), Chapter 2 (DFDs)
- Microsoft Threat Modeling — DFD elements: <https://learn.microsoft.com/en-us/azure/security/develop/threat-modeling-tool>
- OWASP — Application Threat Modeling: <https://owasp.org/www-community/Application_Threat_Modeling>
