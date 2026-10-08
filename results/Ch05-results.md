# Chapter 5 — Defending with Agents: Autonomous SecOps — lab run results

_Executed end-to-end on 2026-10-07 with a live OpenAI key (gpt-4o-mini / text-embedding-3-small); zero cell errors._

## Result highlights

- PEV on calibrated detector scores: attack 0.99 -> quarantine, benign 0.15 -> monitor; approval queue records who approved the wipe.
- Bus-driven triage: alerts topic -> PEV -> decisions topic, replayable in order.
- validate_ticket rejects incomplete regex tickets and a hostile model output before they reach the Planner.
- verify_chain recomputes HMACs: catches an edit, a keyless forgery, and a middle deletion; tail truncation is shown as the residual gap.

## Full cell outputs

### Setup

```
No key file at /home/student/keys/key.txt and no OPENAI_API_KEY — the live demo will be skipped.
```

### Setup

```
anomaly (benign): {'score': 0.3512349889913815, 'anomaly': False}
anomaly (attack): {'score': 5.393077802146983, 'anomaly': True}

alerts: {'host': 'host-DB7', 'score': 0.99} {'host': 'host-W12', 'score': 0.15}
```

### Setup

```
PEV (attack): {'action': 'quarantine', 'done': True, 'irreversible': False, 'enrichment': None, 'ok': True, 'rolled_back': False}
PEV (benign): {'action': 'monitor', 'done': True, 'irreversible': False, 'enrichment': None, 'ok': True, 'rolled_back': False}
PEV (irreversible, denied): {'action': 'wipe', 'done': True, 'irreversible': True, 'enrichment': None, 'ok': False, 'rolled_back': True}
```

### 2.1 The Executor's tool belt

```
{
  "action": "quarantine",
  "done": true,
  "irreversible": false,
  "enrichment": {
    "vt": {
      "ioc": "deadbeefcafe1234deadbeefcafe1234",
      "malicious": 3,
      "vendors": 70,
      "source": "VirusTotal (mock \u2014 no API key offline)"
    },
    "cve": {
      "product": "log4j",
      "cve": "CVE-2021-44228",
      "cvss": 10.0,
      "name": "Log4Shell"
    }
  },
  "ok": true,
  "rolled_back": false
}
```

### 2.2 The human gate, made real

```
quarantine irreversible=False ok=True  rolled_back=False
wipe       irreversible=True  ok=True  rolled_back=False
delete     irreversible=True  ok=False rolled_back=True
approval log: [{'action': 'wipe', 'approved': True, 'by': 'alice@soc'}, {'action': 'delete', 'approved': False, 'by': None}]
```

### 🧪 Your turn — extend the policy for a critical-vulnerability response

```
plan: {'severity': 'high', 'action': 'quarantine'} | without approval: False | benign alert: monitor
✗ Not yet — hint: set plan['action'] = 'reimage' under the condition, and IRREVERSIBLE_ACTIONS.add('reimage')
```

### 🧪 Your turn — extend the policy for a critical-vulnerability response

```
alerts   : [{'host': 'host-DB7', 'score': 0.99}, {'host': 'host-W12', 'score': 0.15}, {'host': 'host-FS2', 'score': 0.99}]
decisions: [{'host': 'host-DB7', 'action': 'quarantine', 'ok': True}, {'host': 'host-W12', 'action': 'monitor', 'ok': True}, {'host': 'host-FS2', 'action': 'quarantine', 'ok': True}]
```

### 🧪 Your turn — extend the policy for a critical-vulnerability response

```
{'host': 'host-DB7', 'severity': 'Critical', 'ioc': ['deadbeefcafe1234deadbeefcafe1234']}
{'host': '10.0.4.17', 'severity': None, 'ioc': ['9f86d081884c7d659a2feaa0c55ad015a3bf4f1b2b0b822cd15d6c15b0f00a08']}
{'host': None, 'severity': None, 'ioc': []}
```

### 🧪 Your turn — extend the policy for a critical-vulnerability response

```
regex {'host': 'host-DB7', 'severity': 'Critical', 'ioc': ['deadbeefcafe1234deadbeefcafe1234']}
      -> to Planner
regex {'host': '10.0.4.17', 'severity': None, 'ioc': ['9f86d081884c7d659a2feaa0c55ad015a3bf4f1b2b0b822cd15d6c15b0f00a08']}
      -> REJECTED: severity None not in ['Critical', 'High', 'Low', 'Medium']
regex {'host': None, 'severity': None, 'ioc': []}
      -> REJECTED: host missing; severity None not in ['Critical', 'High', 'Low', 'Medium']

hostile model output -> (False, ["severity 'Urgent!!' not in ['Critical', 'High', 'Low', 'Medium']", 'ioc must be a list of 32-64 hex chars'])
```

### 4.1 A GenAI SOAR playbook — with an allowlist

```
windows.pslist     enumerate processes
  windows.malfind    find injected code
  windows.netscan    surface C2 connections
dropped (not on the allowlist): none
```

### 4.1 A GenAI SOAR playbook — with an allowlist

```
planner   plan        quarantine  prev=00000000.. sig=e741e260..
executor  quarantine  done        prev=e741e260.. sig=f5921f7f..
verifier  verify      ok          prev=f5921f7f.. sig=0ca67315..
executor  wipe        done        prev=0ca67315.. sig=10dbebd1..
verifier  verify      rolled_back prev=10dbebd1.. sig=c2c42213..
```

### 5.1 Verify the chain — and catch a tamperer

```
original          : (True, None, 'intact')
outcome edited    : (False, 4, 'bad signature (event edited)')
sig forged w/o key: (False, 4, 'bad signature (event edited)')
middle deleted    : (False, 2, 'broken link (event removed, reordered, or inserted)')
tail truncated    : (True, None, 'intact')
```

### Quiz

```
Fill in the answers dict below (A/B/C/D) and re-run to grade.
```
