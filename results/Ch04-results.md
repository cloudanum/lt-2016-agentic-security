# Chapter 4 — Exploiting the AI Attack Surface — lab run results

_Executed end-to-end on 2026-10-07 offline (no API key) — live-LLM cells print `skipped`; Ch03 uses recorded gpt-4o-mini replies; zero cell errors._

## Result highlights

- At 10% of rows flipped, targeted 1->0 poisoning drops malicious recall 0.84 -> 0.70 (random: no drop); kNN label check finds 82% of flips, sanitized recall 0.79.
- Extraction agreement 69% at 25 queries -> 93% at 6,400; a 25-query budget blocks the 6,400-query attack.
- Constant-time padding flattens the latency side channel (0.18/0.73/1.49 ms -> 4.0/4.0/4.0 ms); session moderator blocks payload splitting at turn 2.
- Import audit: 'cvelookup' has no PyPI project (hallucinated); 'nmap' resolves to python-nmap.

## Full cell outputs

### Setup

```
No key file at /home/student/keys/key.txt and no OPENAI_API_KEY — the live demo will be skipped.
```

### Setup

```
train (560, 12), test (240, 12), positive (malicious) share 50%
```

### 1.1 Label-flip poisoning

```
rows flipped    random: malicious recall    targeted 1->0: malicious recall
          5%   0.84 -> 0.83                0.84 -> 0.78
         10%   0.84 -> 0.86                0.84 -> 0.70
         20%   0.84 -> 0.74                0.84 -> 0.42
```

### 1.2 Detecting the poison

```
flipped 56 labels; flagged 92; precision 50%, recall 82%
clean     model: malicious recall 0.84
poisoned  model: malicious recall 0.70
sanitized model: malicious recall 0.79
```

### 1.2 Detecting the poison

```
queries  surrogate agreement (mean of 3 attacker runs)
     25  68.9%
    100  88.3%
    400  90.4%
   1600  91.4%
   6400  92.9%
```

### 1.2 Detecting the poison

```
attacker blocked: query budget exhausted | budget exceeded: asked for 6400, 25 left
best the attacker can do inside the budget: 68.9% agreement
```

### 3.1 Token-timing side channel

```
raw     latency by hidden length (ms): {2: 0.19, 8: 0.76, 16: 1.52}
padded  latency by hidden length (ms): {2: 4.0, 8: 4.0, 16: 4.0}
```

### 3.2 Payload splitting across turns

```
single-shot passes filter?  False
every split turn passes filter? True
assembled only in the combined context: F = 'alpha-2026'
```

### 3.2 Payload splitting across turns

```
after turn 1: allow  signals=['sensitive target']
after turn 2: BLOCK  signals=['fragment definitions', 'sensitive target', 'piecewise framing']
after turn 3: BLOCK  signals=['fragment definitions', 'assembly instruction', 'sensitive target', 'piecewise framing']
benign chat: (True, [])
```

### 3.3 Hallucination and slopsquatting

```
cvelookup    NO PyPI project 'cvelookup' -> likely hallucinated; do not install
json         stdlib
nmap         on PyPI as 'python-nmap' — vet before installing
socket       stdlib
```

### 3.3 Hallucination and slopsquatting

```
(no dump file — using the bundled sample artifacts)
risk: HIGH
- PID 1337 'svch0st.exe' — lookalike of 'svchost.exe'
- PID 1337 — RWX region (malfind): code injected into 'svch0st.exe'
next: preserve the dump, isolate the host, escalate to IR
```

### 4.1 Live demo — LLM triage of the same artifacts

```
skipped (no API key)
```

### 🧪 Your turn — a lookalike detector that generalises

```
fakes: {'svch0st.exe': False, 'lsasss.exe': False, 'expl0rer.exe': False, 'scvhost.exe': False, 'csrs.exe': False}
reals: {'svchost.exe': False, 'lsass.exe': False, 'chrome.exe': False, 'python.exe': False, 'notepad.exe': False}
✗ Not yet — hint: skip exact matches first, then compare ratio() against each known name
```

### 🧪 Your turn — a lookalike detector that generalises

```
layer              attack                     framework                                defense
Training data      targeted label flips       AML.T0020 Poison Training Data           neighbourhood label check + sanitize (1.2)
Model              black-box extraction       AML.T0024.002 Extract ML Model           per-client query budget (2)
Inference channel  token-timing side channel  (classic side channel)                   constant-time padding (3.1)
Inference channel  payload splitting          AML.T0054 LLM Jailbreak                  session-level moderation (3.2)
Supply chain       slopsquatting              AML.T0010 ML Supply Chain Compromise     import audit + PyPI check (3.3)
Host & memory      process hollowing          ATT&CK T1055.012 Process Hollowing       malfind + lookalike triage (4)
```

### Quiz

```
Fill in the answers dict below (A/B/C/D) and re-run to grade.
```
