from wb import *

C = "Ch05"


def build():
    P = []
    P.append(("intro", "Introducing the lab", '''
<p class="lede">This lab turns the earlier attacks into defenses. You assemble an autonomous security-operations pipeline that acts at machine speed on reversible actions, stops for a person on irreversible ones, and can prove afterwards exactly what it did.</p>
<p>A detector raises calibrated alerts. A Planner decides, an Executor enriches and acts, and a Verifier gates the outcome, with a real approval queue that records who approved what. The pipeline runs off an append-only event bus. Free-text incident reports become structured tickets, and a schema check stands between any model's output and the Planner. Every step emits a signed, hash-chained audit event, and you finish by tampering with the log and watching verification catch it.</p>
<p>The idea to carry forward: <strong>bounded autonomy</strong>. Reversible actions run automatically; irreversible ones wait for a recorded human decision; everything is signed.</p>
<ul class="facts"><li><b>Time</b> about 1 h 30 min</li><li><b>Data</b> synthetic traffic vectors · sample incident reports</li><li><b>Libraries</b> numpy, scikit-learn, standard library</li><li><b>API key</b> optional (LLM extractor and playbook)</li></ul>
'''))

    P.append(("terms", "Key terms", terms([
        ("SOC spine", "Collection → detection → triage → investigation → response. AI can speed up every stage."),
        ("Reconstruction scorer", "<code>ReconAnomalyScorer</code>: PCA trained on benign traffic; inputs it reconstructs badly are anomalies. A portable stand-in for an autoencoder."),
        ("Calibration", "Mapping a raw score to a 0–1 alert score: here, reconstruction error divided by twice the anomaly threshold, capped at 0.99."),
        ("Planner → Executor → Verifier (PEV)", "Planner assesses severity and picks an action; Executor enriches and acts; Verifier validates and gates."),
        ("Reversible / irreversible action", "Reversible: undoable (quarantine, block an IP). Irreversible: destroys state or evidence (wipe, delete, reimage)."),
        ("Human-in-the-loop gate", "An irreversible action runs only after a person approves it; otherwise the Verifier rolls it back."),
        ("Approval queue", "Where gated actions wait for a decision. It records the action, the decision and who made it."),
        ("Enrichment", "Adding context before acting: threat-intel reputation (VirusTotal, mocked) and CVE severity from a bundled database."),
        ("CVSS", "Common Vulnerability Scoring System, 0–10. Log4Shell (CVE-2021-44228) scores 10.0."),
        ("Event bus / topic", "An ordered, append-only stream that agents publish to and consume from (Kafka in production, <code>LocalBus</code> here)."),
        ("Schema validation", "A deterministic check that a ticket has a host, an allowed severity and well-formed indicators before it can drive actions."),
        ("SOAR playbook", "Security Orchestration, Automation and Response: an ordered list of response steps, here Volatility plugins."),
        ("HMAC", "A keyed hash. Only someone holding the key can produce a valid signature."),
        ("Hash chain", "Each event stores the previous event's signature in <code>prev</code>, so editing or removing one breaks the links after it."),
        ("Anchoring", "Storing the latest signature somewhere the attacker cannot write, so truncating the end of the log is detectable too."),
    ])))

    f = Flow(7, 2, cw=150, rh=112, bh=62)
    f.node("p1", 0, 0, "Part 1", "detect", kind="step")
    f.node("p2", 1, 0, "Part 2", "decide & act", kind="defend")
    f.node("p3", 2, 0, "Part 3", "event bus")
    f.node("p4", 3, 0, "Part 4", "text → ticket")
    f.node("p5", 4, 0, "Part 5", "signed audit", kind="defend")
    f.node("wrap", 5, 0, "Quiz +\ntakeaways", kind="terminal")
    f.node("al", 0, 1, "Alerts", "host + score", kind="data")
    f.node("aq", 1, 1, "Approval log", kind="data")
    f.node("dec", 2, 1, "decisions topic", kind="data")
    f.node("ch", 4, 1, "Event chain", "prev → sig", kind="data")
    for a, b in [("p1", "p2"), ("p2", "p3"), ("p3", "p4"), ("p4", "p5"), ("p5", "wrap")]:
        f.edge(a, b)
    f.edge("p1", "al", "emits").edge("p2", "aq", "records").edge("p3", "dec", "publishes").edge("p5", "ch", "signs")
    P.append(("structure", "How the lab is structured", LEGEND + figure(f,
        "The lab builds the pipeline in the order data flows through it. Each part leaves an artifact behind: alerts, an approval log, a decisions topic, and a signed event chain.") + '''
<div class="tblwrap"><table class="tbl"><thead><tr><th>Part</th><th>You do</th><th>You produce</th></tr></thead><tbody>
<tr><td>1 · Detect</td><td>Fit the reconstruction scorer on benign traffic; calibrate scores</td><td><code>det_alert</code> (0.99), <code>det_alert2</code> (0.15)</td></tr>
<tr><td>2 · Decide &amp; act</td><td>Run PEV, add the tool belt, add a real approval queue</td><td>Decisions with enrichment and an approval log</td></tr>
<tr><td>3 · Bus</td><td>Publish alerts, consume them with a triage handler</td><td><code>alerts</code> and <code>decisions</code> topics</td></tr>
<tr><td>4 · Tickets</td><td>Extract fields from messy reports; validate; generate an allowlisted playbook</td><td>Accepted or rejected tickets, a playbook</td></tr>
<tr><td>5 · Audit</td><td>Sign events; verify; tamper four ways</td><td>Verification results that locate each tamper</td></tr>
</tbody></table></div>
<h3>Hands-on exercise</h3>''' + exercises([
        ("Extend the policy", "Part 2", "Plan <code>reimage</code> for high-severity alerts with CVSS ≥ 9.0, and add it to <code>IRREVERSIBLE_ACTIONS</code>"),
    ])))

    p = Flow(5, 2, cw=160, rh=118, bh=60)
    p.node("al", 0, 0, "Alert", "host · score", kind="data")
    p.node("pl", 1, 0, "Planner", "score ≥ 0.8 → high")
    p.node("ex", 2, 0, "Executor", "enrich + act")
    p.node("irr", 3, 0, "irreversible?", kind="decision", h=86)
    p.node("hum", 3, 1, "human\napproved?", kind="decision", h=86)
    p.node("rb", 4, 1, "Roll back", "ok = False", kind="defend")
    p.node("ok", 4, 0, "Done", "ok = True", kind="step")
    p.node("tools", 2, 1, "Tool belt", "VirusTotal (mock) · CVE DB", kind="data")
    p.edge("al", "pl").edge("pl", "ex", "plan").edge("ex", "irr").edge("irr", "hum", "yes").edge("hum", "ok", "yes").edge("hum", "rb", "no")
    p.edge("irr", "ok", "no").edge("tools", "ex", "enrichment")
    pev = figure(p, "Planner → Executor → Verifier. The Verifier's two questions are the whole of bounded autonomy: reversible actions skip the human; irreversible ones roll back without approval. <code>IRREVERSIBLE_ACTIONS</code> holds the policy in one place.")

    b = Flow(5, 1, cw=172, rh=110, bh=60)
    b.node("det", 0, 0, "Detector agent", kind="step")
    b.node("t1", 1, 0, "alerts topic", "append-only", kind="data")
    b.node("tri", 2, 0, "Triage agent", "runs PEV", kind="defend")
    b.node("t2", 3, 0, "decisions topic", "append-only", kind="data")
    b.node("rep", 4, 0, "Replay", "same order, same result", kind="step")
    b.edge("det", "t1", "publish").edge("t1", "tri", "consume").edge("tri", "t2", "publish").edge("t2", "rep")
    bus = figure(b, "The pipeline driven by the bus. Agents never call each other directly; the ordered topics are both the transport and the record.")

    t = Flow(5, 2, cw=170, rh=112, bh=60)
    t.node("txt", 0, 0, "Free-text report", kind="data")
    t.node("ext", 1, 0, "Extractor", "regex or LLM")
    t.node("val", 2, 0, "schema\nvalid?", "host · severity · ioc", kind="decision", h=96)
    t.node("pl", 3, 0, "Planner", kind="step")
    t.node("rej", 2, 1, "Reject", "list the problems", kind="defend")
    t.edge("txt", "ext").edge("ext", "val", "ticket").edge("val", "pl", "yes").edge("val", "rej", "no")
    tick = figure(t, "The deterministic output boundary. Whether the extractor is a brittle regex or a model that was confused or manipulated, an invalid ticket never reaches the Planner.")

    v = Flow(6, 2, cw=160, rh=112, bh=60)
    v.node("ev", 0, 0, "Event i", kind="data")
    v.node("lk", 1, 0, "prev = sig\nof i−1?", kind="decision", h=86)
    v.node("hm", 2, 0, "HMAC(key, event)\n= sig?", kind="decision", h=92, w=170)
    v.node("nx", 3, 0, "Next event", kind="step")
    v.node("ok", 4, 0, "Intact", kind="defend")
    v.node("b1", 1, 1, "Broken link", "removed / reordered", kind="attack")
    v.node("b2", 2, 1, "Bad signature", "edited / forged", kind="attack")
    v.edge("ev", "lk").edge("lk", "hm", "yes").edge("hm", "nx", "yes").edge("nx", "ok", "end").edge("lk", "b1", "no").edge("hm", "b2", "no")
    ver = figure(v, "<code>verify_chain</code> checks two things per event and returns the index of the first failure. Recomputing the HMAC is what defeats a forger without the key; checking links is what catches deletions in the middle.")

    P.append(("logic", "The logic", f'''
<h3>Part 1 — Detect</h3>
{steps([
    "<code>ReconAnomalyScorer.fit</code> learns 6 principal components of 500 benign 16-dimensional vectors and sets the threshold at the 99th percentile of benign reconstruction error.",
    "<code>score</code> returns the raw error and whether it exceeds the threshold. <code>to_alert</code> calibrates it to 0–0.99 so the Planner's 0.8 cut-off is meaningful.",
])}
<h3>Part 2 — Decide and act</h3>
{LEGEND}{pev}
{steps([
    "<code>soc_tools</code> is the Executor's tool belt: a mocked VirusTotal lookup and a bundled CVE mini-database (Log4Shell, xz-utils, Heartbleed).",
    "<code>ApprovalQueue</code> replaces the stand-in <code>human_ok</code>. It answers from the on-call person's recorded decisions and logs each one with the approver's name.",
    "In the exercise, the planner gains <code>reimage</code>. The policy set must change in the same edit, or the Verifier treats the new destructive action as reversible.",
])}
<h3>Part 3 — Wire it to a bus</h3>
{bus}
<h3>Part 4 — Free text in, ticket out</h3>
{tick}
{steps([
    "<code>extract_entities</code> uses regexes for host, severity and hash indicators. It misses informal wording such as <code>sev is crit</code>.",
    "<code>extract_entities_llm</code> asks a model for JSON with the same three keys. Its output is untrusted input.",
    "<code>validate_ticket</code> requires a non-empty host, a severity from the allowed set, and indicators of 32–64 hex characters.",
    "<code>gen_playbook</code> keeps only Volatility plugins on <code>ALLOWED_PLUGINS</code> and falls back to a fixed, reviewed playbook with no model.",
])}
<h3>Part 5 — Prove what happened</h3>
<p><code>sign_event</code> builds each event with the previous signature in <code>prev</code> and signs it with HMAC-SHA256 over the sorted JSON. The genesis event chains to 64 zeros.</p>
{ver}
'''))

    O = []
    O.append(outcome("Detector output and calibrated alerts",
        out_block(output(C, "scorer = ReconAnomalyScorer().fit")),
        "<p>The attack vector reconstructs about 15 times worse than the benign one and crosses the threshold. After calibration the alerts read 0.99 and 0.15, which the Planner turns into <em>high</em> and <em>low</em>.</p>"))
    O.append(outcome("PEV decisions",
        out_block(output(C, 'print("PEV (attack)')),
        "<p>The attack alert is quarantined and the benign one monitored, both reversible, so neither waits for a person. The irreversible wipe without approval is rolled back.</p>"))
    O.append(outcome("The approval queue",
        out_block(output(C, "class ApprovalQueue")),
        "<p>Quarantine never reaches the queue. The wipe runs because <code>alice@soc</code> approved it; the delete is rolled back because nobody did. The approval log records who decided, which is what an auditor will ask for.</p>"))
    O.append(outcome("Bus-driven triage",
        out_block(output(C, "bus = LocalBus()")),
        "<p>Three alerts in, three decisions out, in order. Replaying the alerts topic reproduces every decision. The record is only as trustworthy as its storage, which is what Part 5 addresses.</p>"))
    O.append(outcome("Tickets and the schema check",
        out_block(output(C, "def validate_ticket")),
        "<p>Only the well-formed report reaches the Planner. The other two are rejected with specific problems, and so is a hostile model output with an invented severity and a shell command as an indicator. With a key, the LLM extractor handles the messy reports; one recorded run returned <code>{'host': 'DB7', ...}</code> without the <code>host-</code> prefix, a reminder that model output needs normalization as well as validation.</p>"))
    O.append(outcome("Tamper detection",
        out_block(output(C, "def verify_chain")),
        "<p>The edited outcome and the forgery without the key both fail at event 4; deleting a middle event breaks the link at event 2. Truncating the tail still verifies, because a shortened chain is internally consistent. Anchoring the latest signature outside the attacker's reach closes that gap.</p>"))
    P.append(("outcomes", "Expected outcomes and what they mean", "".join(O)))

    P.append(("takeaways", "Key takeaways", takeaways([
        "Defense is a Planner → Executor → Verifier pipeline: reversible actions run automatically, irreversible ones stop for a recorded human decision.",
        "Keep policy (what is irreversible) in one place, and change it in the same edit that gives an agent a new capability.",
        "An ordered, append-only event log is both the inter-agent bus and the forensic record.",
        "Model output is untrusted input: schema checks and allowlists sit between the model and anything that acts.",
        "Signed, hash-chained events make the trail evidence; anchor the head of the chain externally.",
    ])))
    return P
