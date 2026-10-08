# Chapter 5 — Defending with Agents: Autonomous SecOps — lab run results

_Executed end-to-end on 2026-10-08 with a live OpenAI key (gpt-4o-mini / text-embedding-3-small); zero cell errors._

## Result highlights

- PCA reconstruction scorer drives the PEV pipeline with real calibrated scores: attack 0.99 -> quarantine; benign 0.15 -> monitor; irreversible action without approval -> rolled back.
- Executor enriches through its tool belt (VT mock + bundled CVE mini-DB: Log4Shell 10.0); audit trail replays over LocalBus; HMAC-signed event chain verifies intact.
- Live LLM entity extractor parses the alert into host/severity/ioc JSON.

## Full cell outputs

### Setup

```
OpenAI key loaded — client ready (key not shown).
```

### Try it

```
anomaly (benign): {'score': 0.3512349889913815, 'anomaly': False}
anomaly (attack): {'score': 5.393077802146983, 'anomaly': True}

alert from detector: {'host': 'host-DB7', 'score': 0.99}
PEV (attack): {'action': 'quarantine', 'done': True, 'irreversible': False, 'enrichment': None, 'ok': True, 'rolled_back': False}
PEV (benign): {'action': 'monitor', 'done': True, 'irreversible': False, 'enrichment': None, 'ok': True, 'rolled_back': False}
PEV (irreversible, denied): {'action': 'wipe', 'done': True, 'irreversible': True, 'enrichment': None, 'ok': False, 'rolled_back': True}

bus audit log: [{'host': 'host-DB7', 'score': 0.99}, {'host': 'host-W12', 'score': 0.15}]

extract: {'host': 'host-DB7', 'severity': 'Critical', 'ioc': ['deadbeefcafe1234deadbeefcafe1234']}
```

### Live demo — the LLM incident-report extractor

```
regex stand-in : {'host': 'host-DB7', 'severity': 'Critical', 'ioc': ['deadbeefcafe1234deadbeefcafe1234']}
LLM extractor  : {'host': 'DB7', 'severity': 'Critical', 'ioc': ['deadbeefcafe1234deadbeefcafe1234']}
```

### Executor enrichment and a GenAI SOAR playbook

```
decision: {'action': 'quarantine', 'done': True, 'irreversible': False, 'enrichment': {'vt': {'ioc': 'deadbeefcafe1234deadbeefcafe1234', 'malicious': 3, 'vendors': 70, 'source': 'VirusTotal (mock — no API key offline)'}, 'cve': {'product': 'log4j', 'cve': 'CVE-2021-44228', 'cvss': 10.0, 'name': 'Log4Shell'}}, 'ok': True, 'rolled_back': False}
cve miss : {'product': 'not-in-db', 'cve': None, 'note': 'not in the bundled mini-DB'}
playbook: [
  {
    "plugin": "windows.pslist",
    "why": "enumerate processes"
  },
  {
    "plugin": "windows.malfind",
    "why": "find injected code"
  },
  {
    "plugin": "windows.netscan",
    "why": "surface C2 connections"
  }
]
```

### Zero-Trust signed audit events

```
planner   plan        quarantine  prev=00000000.. sig=e741e260..
executor  quarantine  done        prev=e741e260.. sig=f5921f7f..
verifier  verify      ok          prev=f5921f7f.. sig=0ca67315..
executor  wipe        done        prev=0ca67315.. sig=10dbebd1..
verifier  verify      rolled_back prev=10dbebd1.. sig=c2c42213..
chain intact: True
```

### Quiz

```
Fill in the answers dict above (A/B/C/D) and re-run to grade.
```
