# Chapter 7 — Secure-Agent Maturity: Course Capstone — lab run results

_Executed end-to-end on 2026-10-07 with a live OpenAI key (gpt-4o-mini / text-embedding-3-small); zero cell errors._

## Result highlights

- Maturity 1/4 (Initial), 48% — governance gate caps the team.
- What-if: only governance +1 moves the level; 90-day roadmap = governance, post-quantum, governance -> projected 3/4.

## Full cell outputs

### Setup

```
ch   attack                                     defense                                    control
Ch1  hijacked tool call / argument smuggling    schema-enforcing tool gateway              MAN-3 least privilege
Ch2  RAG extraction and KB poisoning            ACL + provenance-checked retrieval, DLP    MAP-3 data provenance
Ch3  prompt injection, jailbreak, FGSM          input guard + spotlighting + output guard  ZT-1 input validation
Ch4  poisoning, extraction, side channels       label checks, query budgets, padding       MEA-1 red-team results
Ch5  unapproved destructive action, log edits   PEV human gate, signed hash chain          MAN-1 / MAN-2
Ch6  ungoverned go-live                         ZT audit gate, determinism sandwich        GOV-1 accountable owner
```

### 2.1 The six domains

```
0 Absent      nothing in place
1 Initial     ad hoc — depends on individuals
2 Developing  documented and partly implemented
3 Managed     implemented, measured, and owned
4 Optimized   automated and continuously improved
```

### 2.4 From score to next step

```
=== Secure-Agent Maturity Self-Assessment ===
Overall maturity: 1/4 (Initial), 48%
  ! Capped at 'Initial': governance/audit-trail is the gate (Zero Trust exit criterion, NIST SP 800-207).

Per-domain:
  [###.] Managed     Architecture & AI literacy  (Ch1)
  [###.] Managed     GenAI risk & SecOps toolkit  (Ch2)
  [###.] Managed     Adversarial / red-team readiness  (Ch3-4)
  [##..] Developing  Detection & autonomous response  (Ch5)
  [#...] Initial     Governance & Zero Trust  (Ch6)
  [....] Absent      Post-quantum & future readiness  (Ch6)

Weakest domain: Post-quantum & future readiness (now: Absent)
  Next step:     Inventory crypto, adopt crypto-agility toward FIPS 203/204/205
  Certification: Follow NIST PQC + AIRC
```

### 2.4 From score to next step

```
raise by one step                     level   pct
Governance & Zero Trust                  +1    +6
Post-quantum & future readiness          +0    +4
Detection & autonomous response          +0    +4
Architecture & AI literacy               +0    +4
GenAI risk & SecOps toolkit              +0    +4
Adversarial / red-team readiness         +0    +4
```

### 2.4 From score to next step

```
Days 1-30   Governance & Zero Trust            Initial -> Developing
            Enforce the audit-trail exit criterion + run the OWASP gov checklist
Days 31-60  Post-quantum & future readiness    Absent -> Initial
            Inventory crypto, adopt crypto-agility toward FIPS 203/204/205
Days 61-90  Governance & Zero Trust            Developing -> Managed
            Enforce the audit-trail exit criterion + run the OWASP gov checklist

projected after 90 days: 3/4 (Managed), 63%
```

### 🧪 Your turn — score your team

```
✗ Not yet — hint: every domain needs an integer from 0 to 4 (use the rubric in 2.1)
```

### Quiz

```
Fill in the answers dict below (A/B/C/D) and re-run to grade.
```
