# Security Champions Program

A security champion is a developer embedded in a product team who
acts as the first line of security review and the liaison to the
central security team. The role does not turn a developer into a
security engineer; it turns part of every team into a security ally.

## Why

- Security review at the speed of code review.
- Threat-model and design-review participation without scheduling
  through the central security team for every change.
- A two-way translation layer: product context for the security
  team, security context for the product team.

## Selection

- One champion per product team (more for teams above 8 engineers).
- Volunteer-first; manager-nominated if no volunteer.
- Tenure: at least 6 months, with a documented handover when the
  champion rotates.
- Time allocation: 10-20% of the champion's working hours, ring-fenced
  by the manager and visible on the sprint board.

## Responsibilities

- Review every PR in the team for security implications before
  merge, using
  [code-review-checklist.md](code-review-checklist.md).
- Run a recurring (monthly or per-sprint) threat-model workshop on
  upcoming work; output recorded in the team's
  [threat-modeling/](../threat-modeling/) sibling area.
- Triage SAST / SCA / DAST findings for the team's services;
  decide locally for LOW / MEDIUM; escalate HIGH / CRITICAL.
- Maintain the team's security backlog and report progress at the
  weekly champion sync.
- Be the contact point for incidents that touch the team's surface.

## Out of scope

- Authoritative decisions on policy. Champions implement and
  contextualize policy; they do not set it.
- Penetration testing. Engagements are run by the central security
  team or contracted to specialists.
- Cryptographic design or cryptanalysis. Recommendations come from
  the central security team or external review.

## Onboarding

A new champion completes, in the first 30 days:

1. OWASP Top 10 (current edition) and OWASP API Top 10 (current
   edition) reading.
2. Walk-through of this handbook's
   [secure-coding/](../secure-coding/) and
   [threat-modeling/](../threat-modeling/) sections.
3. Pair on two real PR reviews with an experienced champion or with
   the central security team.
4. Participate in one threat-modeling workshop as an observer.
5. Set up the team's SAST / SCA / DAST dashboards in their tooling.

## Cadence

- Weekly: champion sync (60 minutes); rotating chair; backlog review
  and pattern sharing across teams.
- Monthly: deep-dive on one topic with prep reading
  (e.g., a new framework's auth model, a CVE post-mortem).
- Quarterly: maturity self-assessment against OWASP SAMM by each
  team's champion; rolled up by the central security team.

## Metrics

- Coverage: percentage of teams with an active champion.
- Throughput: median time from finding identified to ticket created
  and from ticket created to merged.
- Quality: ratio of valid champion-raised findings to false
  positives at PR review time.
- Engagement: percentage of champions attending the weekly sync over
  a rolling 4-week window.
- Retention: median tenure; reason given when a champion steps down.

## Recognition

- Champion time appears on the sprint board and counts against
  product capacity.
- Public acknowledgement at all-hands when a champion ships a
  high-impact security improvement.
- Career-ladder language explicitly recognizes champion contributions
  as evidence for promotion criteria around impact and collaboration.

## When the program is failing

- Champions resign without a replacement: the manager has not
  protected the time allocation. Escalate to leadership.
- Findings pile up unactioned: triage is happening but execution is
  not prioritized. Negotiate dedicated capacity for security work
  per sprint.
- Champion sync becomes a status meeting only: rotate the agenda to
  one focused topic per week; cap status updates at 5 minutes.

## References

- OWASP Security Champions Playbook: <https://github.com/c0rdis/security-champions-playbook>
- OWASP SAMM v2 (Education and Guidance practice): <https://owaspsamm.org/model/governance/education-and-guidance/>
- BSIMM (Strategy and Metrics, Training): <https://www.bsimm.com/>
