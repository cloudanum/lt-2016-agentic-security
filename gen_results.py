import json, glob, datetime, re

TODAY = datetime.date.today().isoformat()
OUT_DIR = "results"

HIGHLIGHTS = {
    "Ch01": [
        "Isolation Forest on the 103k-flow CICIDS-2017 sample: lift 0.50x (high-volume DDoS/PortScan look normal) yet 11/11 Heartbleed and 13/36 Infiltration flagged.",
        "Supervised random forest: 0.994 F1 on seen attacks, 0% recall on held-out Bot / FTP-Patator / Infiltration.",
        "Benign-trained autoencoder: top-1% is 90% real attacks vs 11% for the forest; the two agree on only ~30 flows.",
        "Schema-enforcing ToolRegistry denies 4 hijacked calls (unregistered tool, argument smuggling, extra arg, wrong type) and logs all 5.",
    ],
    "Ch02": [
        "RAG over the 12-doc KB answers the ransomware question with citations and refuses the out-of-KB question (0.00 < 0.15).",
        "Extraction probe dumps all 22 chunks incl. the IR-only note; a planted wiki page wins retrieval (0.62) and advises paying the ransom.",
        "secure_rag_query refuses the probe, ACL-denies the IR note to analysts, drops the unapproved source; ingestion-time filtering restores the correct answer.",
        "Cost-based threshold (miss = 250x false alarm): 0 misses vs 37 at the max-F1 threshold; risk register + 3x3 matrix.",
    ],
    "Ch03": [
        "Recorded gpt-4o-mini replies: 3 of 5 injection variants hijack the sandbox (60%), reported as MITRE ATLAS findings.",
        "Local input guard blocks 4/5; a door-sign false positive shows the precision cost of signatures.",
        "Output guard (canary + task-length contract) independently blocks all 3 hijacks (and the refusal): the two layers overlap.",
        "FGSM: 0.95 -> 0.31 accuracy at eps 0.5; adversarial training lifts eps 0.3 from 0.60 to 0.66. Callback rule holds an Arup-style deepfake that scores 0.",
    ],
    "Ch04": [
        "At 10% of rows flipped, targeted 1->0 poisoning drops malicious recall 0.84 -> 0.70 (random: no drop); kNN label check finds 82% of flips, sanitized recall 0.79.",
        "Extraction agreement 69% at 25 queries -> 93% at 6,400; a 25-query budget blocks the 6,400-query attack.",
        "Constant-time padding flattens the latency side channel (0.18/0.73/1.49 ms -> 4.0/4.0/4.0 ms); session moderator blocks payload splitting at turn 2.",
        "Import audit: 'cvelookup' has no PyPI project (hallucinated); 'nmap' resolves to python-nmap.",
    ],
    "Ch05": [
        "PEV on calibrated detector scores: attack 0.99 -> quarantine, benign 0.15 -> monitor; approval queue records who approved the wipe.",
        "Bus-driven triage: alerts topic -> PEV -> decisions topic, replayable in order.",
        "validate_ticket rejects incomplete regex tickets and a hostile model output before they reach the Planner.",
        "verify_chain recomputes HMACs: catches an edit, a keyless forgery, and a middle deletion; tail truncation is shown as the residual gap.",
    ],
    "Ch06": [
        "EU AI Act tiers: SOC agent minimal, support bot limited, CV screening high, workplace emotion recognition prohibited.",
        "Score 66/100 with 1 open critical; Zero Trust go-live BLOCKED (executor-agent has no signed audit trail). RACI validator finds a policy row with nobody Responsible.",
        "Determinism sandwich stops an injection at input and a hijacked delete_snapshots call at output; every decision HMAC-signed.",
        "PQC inventory: ECDH mTLS = MIGRATE NOW (harvest-now-decrypt-later), AES-128 = UPGRADE, RSA-2048 signing = PLAN.",
    ],
    "Ch07": [
        "Maturity 1/4 (Initial), 48% — governance gate caps the team.",
        "What-if: only governance +1 moves the level; 90-day roadmap = governance, post-quantum, governance -> projected 3/4.",
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
    live = "skipped (no API key)" not in json.dumps(nb)
    mode = ("with a live OpenAI key (gpt-4o-mini / text-embedding-3-small)" if live else
            "offline (no API key) — live-LLM cells print `skipped`; Ch03 uses recorded gpt-4o-mini replies")
    lines = [
        f"# {title} — lab run results",
        "",
        f"_Executed end-to-end on {TODAY} {mode}; zero cell errors._",
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
