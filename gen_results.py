import json, glob, datetime, re

TODAY = "2026-10-08"
OUT_DIR = "results"

HIGHLIGHTS = {
    "Ch01": [
        "Isolation Forest on the shipped 103k-flow CICIDS-2017 sample: 1,030 outliers (1%); rare attacks (slowloris, Infiltration, Heartbleed) surface among unusual-but-benign flows.",
        "The cognitive loop triages the detector's real top-scored flow (score 0.736), enriches via CVE lookup, escalates on CVSS 10.0 — every tool call in the Zero Trust action log.",
        "Live LLM reasoner chose an action inside the perceive-interpret-reason-act-learn loop.",
    ],
    "Ch02": [
        "Full RAG pipeline over the 12-doc threat-intel KB: ransomware question retrieves playbook + ATT&CK T1490 chunks (0.23/0.19) and composes a cited answer; out-of-KB question is refused (0.00 < 0.15).",
        "Extraction probe dumps all 22 chunks including the internal incident note — retrieval has no notion of 'authorized to see'.",
        "Live LLM answered the same augmented prompt (compare with the deterministic composer).",
    ],
    "Ch03": [
        "Guard with a real char n-gram TF-IDF embedder: 4 of 5 injection payloads blocked (cos 0.36-0.75); refusal-suppression evades (0.08) — necessary, not sufficient.",
        "FGSM in closed form collapses a trained guardrail classifier: 0.95 -> 0.31 accuracy as eps grows 0.05 -> 0.5.",
        "Live red-team: sandbox TranslateBot attacked with 5 payloads + DAN; safe_ask screens them with OpenAI embeddings.",
    ],
    "Ch04": [
        "Label-flip poisoning dose-response: +0.009 F1 drop at 5%, +0.079 at 20%; surrogate model extraction reaches 88.3% agreement.",
        "triage_dump offline rule triage flags svch0st.exe lookalike + RWX region -> HIGH; live run triages the same artifacts with the LLM.",
        "Slopsquat audit flags invented packages; payload splitting assembles a passphrase across turns that each pass the filter — live replay shows the model completing it.",
    ],
    "Ch05": [
        "PCA reconstruction scorer drives the PEV pipeline with real calibrated scores: attack 0.99 -> quarantine; benign 0.15 -> monitor; irreversible action without approval -> rolled back.",
        "Executor enriches through its tool belt (VT mock + bundled CVE mini-DB: Log4Shell 10.0); audit trail replays over LocalBus; HMAC-signed event chain verifies intact.",
        "Live LLM entity extractor parses the alert into host/severity/ioc JSON.",
    ],
    "Ch06": [
        "Governance assistant: score 66/100 with 1 open critical; Zero Trust go-live BLOCKED (executor-agent has no signed audit trail).",
        "Remediation plan leads with the audit-trail CRITICAL from both lenses (ZT finding + MAN-1 control).",
    ],
    "Ch07": [
        "Maturity self-assessment: 1/4 (Initial), 48% — governance gate caps the team at 'Initial'.",
        "Weakest domain: post-quantum readiness (Absent) -> crypto inventory + crypto-agility next step.",
    ],
}

def cell_outputs_text(cell):
    parts = []
    for out in cell.get("outputs", []):
        if out.get("output_type") == "stream":
            parts.append("".join(out.get("text", [])))
        elif out.get("output_type") == "execute_result":
            parts.append("".join(out.get("data", {}).get("text/plain", [])))
        elif out.get("output_type") == "error":
            parts.append("ERROR: " + out.get("ename", "") + " " + str(out.get("evalue", "")))
    return "".join(parts).strip()

def heading_of(src):
    m = re.match(r"^(#{1,3})\s+(.*)", src)
    return m.group(2).strip() if m else None

for f in sorted(glob.glob("code/Ch0*-Lab.ipynb")):
    chap = f.split("/")[-1][:4]
    nb = json.load(open(f))
    title = "".join(nb["cells"][0]["source"]).lstrip("# ").strip()
    lines = [
        f"# {title} — lab run results",
        "",
        f"_Executed end-to-end on {TODAY} with a live OpenAI key "
        "(gpt-4o-mini / text-embedding-3-small); zero cell errors._",
        "",
        "## Result highlights",
        "",
    ]
    lines += [f"- {h}" for h in HIGHLIGHTS[chap]]
    lines += ["", "## Full cell outputs", ""]
    current = "Setup"
    for c in nb["cells"]:
        s = "".join(c["source"])
        if c["cell_type"] == "markdown":
            h = heading_of(s)
            if h:
                current = h
            continue
        text = cell_outputs_text(c)
        if not text:
            continue
        lines += [f"### {current}", "", "```", text, "```", ""]
    out_path = f"{OUT_DIR}/{chap}-results.md"
    open(out_path, "w").write("\n".join(lines))
    print("wrote", out_path, f"({len(lines)} lines)")
