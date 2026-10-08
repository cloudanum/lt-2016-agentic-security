# Chapter 6 — AI Governance & Zero Trust for Agents — lab run results

_Executed end-to-end on 2026-10-08 with a live OpenAI key (gpt-4o-mini / text-embedding-3-small); zero cell errors._

## Result highlights

- Governance assistant: score 66/100 with 1 open critical; Zero Trust go-live BLOCKED (executor-agent has no signed audit trail).
- Remediation plan leads with the audit-trail CRITICAL from both lenses (ZT finding + MAN-1 control).

## Full cell outputs

### Try it

```
=== AI Governance Assistant ===
Governance score: 66/100   (open critical controls: 1)
Zero Trust go-live: BLOCKED

Top gaps:
  - (CRITICAL) MAN-1: Every agent action emits a signed audit event
  - (MEDIUM  ) MAN-3: Least-privilege agent identity; no shared god-credential
  - (MEDIUM  ) MAP-1: AI asset inventory (SBOM + MLBOM) is current
  - (MEDIUM  ) MAP-3: Data provenance + lawful basis (GDPR Art.6/22) documented
  - (LOW     ) GOV-2: AI use policy, acceptable-use + legal/regulatory sign-off

AI RACI (Approve go-live): {'Product Owner': 'A', 'ML Eng': 'C', 'Security': 'R', 'Legal/Privacy': 'R', 'SRE/Ops': 'C'}

Remediation plan:
  1. (CRITICAL) [executor-agent] no signed audit trail (ZT exit criterion)
  2. (CRITICAL) [MAN-1/Manage] Every agent action emits a signed audit event
  3. (MEDIUM) [MAN-3/Manage] Least-privilege agent identity; no shared god-credential
  4. (MEDIUM) [MAP-1/Map] AI asset inventory (SBOM + MLBOM) is current
  5. (MEDIUM) [MAP-3/Map] Data provenance + lawful basis (GDPR Art.6/22) documented
  6. (LOW) [GOV-2/Govern] AI use policy, acceptable-use + legal/regulatory sign-off

Exit criterion: go-live is BLOCKED until every component is logged (NIST SP 800-207). 'executor-agent' has no audit trail.
```

### Quiz

```
Fill in the answers dict above (A/B/C/D) and re-run to grade.
```
