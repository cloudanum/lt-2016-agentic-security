# Chapter 1 — AI Architecture & Agentic Foundations — lab run results

_Executed end-to-end on 2026-10-08 with a live OpenAI key (gpt-4o-mini / text-embedding-3-small); zero cell errors._

## Result highlights

- Isolation Forest on the shipped 103k-flow CICIDS-2017 sample: 1,030 outliers (1%); rare attacks (slowloris, Infiltration, Heartbleed) surface among unusual-but-benign flows.
- The cognitive loop triages the detector's real top-scored flow (score 0.736), enriches via CVE lookup, escalates on CVSS 10.0 — every tool call in the Zero Trust action log.
- Live LLM reasoner chose an action inside the perceive-interpret-reason-act-learn loop.

## Full cell outputs

### Setup

```
OpenAI key loaded — client ready (key not shown).
```

### Try it

```
cosine identical: 1.0
function-calling schema tool: lookup_cve
OK - see each function's docstring.
```

### Try it

```
Inlier / Outlier counts:
flag
inlier     101969
outlier      1030
Name: count, dtype: int64

True labels of the outliers:
Label
BENIGN           918
DoS slowloris     79
Infiltration      13
Heartbleed        11
DoS Hulk           4
Bot                4
PortScan           1
Name: count, dtype: int64

Top-scored flow: {'flow_id': 'flow-11389', 'score': 0.736, 'cve': 'CVE-2024-3094'} (true label: BENIGN)
```

### Live demo — a real reasoner inside the cognitive loop

```
LLM-chosen action : Investigate flow-11389 for unusual activity.
action-log entry  : ('Investigate flow-11389 for unusual activity.', 'executed: Investigate flow-11389 for unusual activity.')
```

### Worked flow: detector → alert → CVE lookup → triage

```
alert from the detector: {'flow_id': 'flow-11389', 'score': 0.736, 'cve': 'CVE-2024-3094'}
[ZT-LOG] tool=lookup_cve args={'cve_id': 'CVE-2024-3094'} -> {'cve': 'CVE-2024-3094', 'cvss': 10.0, 'severity': 'CRITICAL'}
[ZT-LOG] tool=triage     args={'verdict': 'escalate', 'cve': 'CVE-2024-3094'} -> {'final_verdict': 'escalate', 'cve': 'CVE-2024-3094'}
AGENT VERDICT: {'verdict': {'final_verdict': 'escalate', 'cve': 'CVE-2024-3094'}, 'tool_calls': 2}
```

### Quiz

```
Fill in the answers dict above (A/B/C/D) and re-run to grade.
```
