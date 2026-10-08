from wb import *

C = "Ch06"


def build():
    P = []
    P.append(("intro", "Introducing the lab", '''
<p class="lede">Governance is where frameworks become code that can block a release. This lab builds a small governance assistant in pure standard-library Python and uses it to take an agentic system from <em>blocked</em> to <em>cleared</em> for go-live.</p>
<p>You classify use cases into EU AI Act risk tiers, score a system against a blended NIST AI RMF / OWASP checklist, validate an accountability (RACI) matrix, and run a Zero-Trust audit whose exit criterion is that every component is logged. The findings merge into one ordered remediation plan, and in the exercise you fix the system until both gates clear. Two closing parts put governance into the runtime (the determinism sandwich) and look ahead with a post-quantum crypto inventory.</p>
<p>The idea to carry forward: <strong>a high score with a missing audit trail still blocks go-live</strong>. If an action was not logged, you cannot prove what happened.</p>
<ul class="facts"><li><b>Time</b> about 1 h 25 min</li><li><b>Data</b> a sample system profile and component list</li><li><b>Libraries</b> standard library only</li><li><b>API key</b> not used</li></ul>
'''))

    P.append(("terms", "Key terms", terms([
        ("EU AI Act risk tiers", "Unacceptable (prohibited, Art. 5) → high (Annex III uses) → limited (transparency, Art. 50) → minimal. The lab's classifier is a simplified teaching model, not legal advice."),
        ("Annex III", "The EU AI Act's list of high-risk uses, including employment, credit scoring, education and critical infrastructure."),
        ("NIST AI RMF", "Govern (the foundation) wrapping Map → Measure → Manage."),
        ("OWASP LLM governance checklist", "OWASP's building blocks for deploying LLM applications responsibly; each control here maps to one."),
        ("Control weight / critical control", "Weight 1–3 sets a control's share of the score. A critical control that is missing is a hard gap whatever the score."),
        ("Gap analysis", "Scoring each control met (full weight), partial (half) or missing (none), and ranking the gaps by severity."),
        ("RACI", "Responsible (does the work), Accountable (owns the outcome, exactly one), Consulted, Informed."),
        ("Zero Trust (NIST SP 800-207)", "Never trust, always verify: each component has its own identity, least privilege, an audit trail, and a human gate on irreversible actions."),
        ("Exit criterion", "A condition that must hold before go-live. Here: every component emits a signed audit trail."),
        ("Remediation plan", "Checklist gaps and Zero-Trust findings merged into one list, critical items first."),
        ("Determinism sandwich", "Deterministic input checks and deterministic output checks around a probabilistic model, with every decision signed."),
        ("Harvest now, decrypt later", "Recording encrypted traffic today to decrypt once a cryptographically relevant quantum computer exists."),
        ("ML-KEM / ML-DSA / SLH-DSA", "NIST's post-quantum standards: key encapsulation (FIPS 203) and signatures (FIPS 204, FIPS 205)."),
        ("Mosca's inequality", "If secrecy lifetime + migration time &gt; time until a quantum threat, you are already late."),
        ("Crypto-agility", "The ability to swap algorithms without redesigning the system; checklist control PQC-1."),
    ])))

    f = Flow(8, 2, cw=136, rh=112, bh=62)
    names = [("p1", "Part 1", "classify"), ("p2", "Part 2", "score"), ("p3", "Part 3", "assign"),
             ("p4", "Part 4", "audit"), ("p5", "Part 5", "remediate"), ("p6", "Part 6", "build it in"),
             ("p7", "Part 7", "look ahead"), ("wrap", "Quiz +\ntakeaways", None)]
    for i, (k, a, b) in enumerate(names):
        f.node(k, i, 0, a, b, kind="terminal" if k == "wrap" else ("defend" if k in ("p4", "p6") else "step"))
    for (a, *_), (b, *_) in zip(names, names[1:]):
        f.edge(a, b)
    f.node("ga", 1, 1, "Score + gaps", kind="data")
    f.node("zt", 3, 1, "Go-live gate", "BLOCKED → CLEARED", kind="decision", h=86)
    f.node("rp", 4, 1, "Remediation plan", kind="data")
    f.edge("p2", "ga").edge("p4", "zt").edge("zt", "rp", "findings").edge("p5", "rp", "writes")
    P.append(("structure", "How the lab is structured", LEGEND + figure(f,
        "The lab follows a governance review: classify the system, score it, assign owners, audit it, then fix it. Parts 6 and 7 move from review to design.") + '''
<div class="tblwrap"><table class="tbl"><thead><tr><th>Part</th><th>You do</th><th>You produce</th></tr></thead><tbody>
<tr><td>1 · Classify</td><td>Place four use cases in EU AI Act tiers</td><td>A tier and duty list per use case</td></tr>
<tr><td>2 · Score</td><td>Run <code>gap_analysis</code> on a partially governed profile</td><td>66/100, one open critical, ranked gaps</td></tr>
<tr><td>3 · Assign</td><td>Print and validate the RACI</td><td>A validation finding in the course's own RACI</td></tr>
<tr><td>4 · Audit</td><td>Run <code>zero_trust_audit</code> on three components</td><td>Go-live BLOCKED, with findings</td></tr>
<tr><td>5 · Remediate</td><td>Merge findings into one plan; fix the system</td><td>An ordered plan, then CLEARED at 80/100</td></tr>
<tr><td>6 · Build it in</td><td>Wrap a model in deterministic input and output checks</td><td>Allow/deny decisions, each signed</td></tr>
<tr><td>7 · Look ahead</td><td>Triage a crypto inventory</td><td>MIGRATE NOW / UPGRADE / PLAN / OK per item</td></tr>
</tbody></table></div>
<h3>Hands-on exercises</h3>''' + exercises([
        ("Repair a RACI", "Part 3", "Give every activity exactly one Accountable and at least one Responsible"),
        ("Get this agent to go-live", "Part 5", "Fix the executor and gateway, mark the controls met, and reach CLEARED with no critical gaps"),
    ])))

    t = Flow(5, 2, cw=170, rh=112, bh=60)
    t.node("u", 0, 0, "Use case", kind="data")
    t.node("pr", 1, 0, "prohibited\npractice?", kind="decision", h=88)
    t.node("an", 2, 0, "Annex III\nuse?", kind="decision", h=88)
    t.node("pub", 3, 0, "faces public or\ngenerates content?", kind="decision", h=96, w=180)
    t.node("min", 4, 0, "MINIMAL", "no AI-Act duties", kind="step")
    t.node("un", 1, 1, "UNACCEPTABLE", "not on EU market", kind="attack")
    t.node("hi", 2, 1, "HIGH", "logging · oversight · …", kind="defend")
    t.node("li", 3, 1, "LIMITED", "disclose AI", kind="step")
    t.edge("u", "pr").edge("pr", "an", "no").edge("an", "pub", "no").edge("pub", "min", "no")
    t.edge("pr", "un", "yes").edge("an", "hi", "yes").edge("pub", "li", "yes")
    tier = figure(t, "<code>eu_ai_act_tier</code>, a simplified teaching model: the first matching question sets the tier, and the tier sets the duties.")

    g = Flow(5, 2, cw=176, rh=118, bh=60)
    g.node("prof", 0, 0, "System profile", "met / partial / missing", kind="data")
    g.node("ga", 1, 0, "gap_analysis", "weighted score")
    g.node("comp", 0, 1, "Components", "identity · privilege · audit · gate", kind="data")
    g.node("zt", 1, 1, "zero_trust_audit")
    g.node("rem", 2, 0, "remediation_plan", "critical first", kind="defend")
    g.node("gate", 3, 1, "every component\nlogged?", kind="decision", h=92, w=190)
    g.node("go", 4, 1, "CLEARED", kind="defend")
    g.node("blk", 3, 0, "BLOCKED", "regardless of score", kind="attack")
    g.edge("prof", "ga").edge("comp", "zt").edge("ga", "rem", "gaps").edge("zt", "rem", "findings")
    g.edge("zt", "gate").edge("gate", "go", "yes").edge("gate", "blk", "no")
    gates = figure(g, "Two independent gates. The checklist score is process-level; the Zero-Trust audit is component-level. A missing audit trail blocks go-live no matter how high the score.")

    s = Flow(6, 2, cw=160, rh=112, bh=60)
    s.node("req", 0, 0, "Request", kind="data")
    s.node("ic", 1, 0, "input\ncheck?", "length · injection", kind="decision", h=92)
    s.node("m", 2, 0, "Model", "probabilistic", kind="decision", h=70)
    s.node("oc", 3, 0, "output\ncheck?", "tool allowlist · schema", kind="decision", h=92)
    s.node("ok", 4, 0, "Allow", kind="defend")
    s.node("aud", 2, 1, "Signed audit", "allow and deny alike", kind="data")
    s.node("d1", 1, 1, "Deny", kind="defend")
    s.node("d2", 3, 1, "Deny", kind="defend")
    s.edge("req", "ic").edge("ic", "m", "pass").edge("m", "oc", "tool call").edge("oc", "ok", "pass")
    s.edge("ic", "d1", "fail").edge("oc", "d2", "fail").edge("d2", "aud").edge("d1", "aud")
    sand = figure(s, "The determinism sandwich. The bread is deterministic; only the filling is probabilistic. Every outcome, allowed or denied, is signed into the audit trail. The output check catches what the input check could not predict.")

    P.append(("logic", "The logic", f'''
<h3>Part 1 — Classify</h3>
{LEGEND}{tier}
<h3>Parts 2–5 — Score, assign, audit, remediate</h3>
{gates}
{steps([
    "<code>CHECKLIST</code> holds 13 controls, each mapped to an RMF function and an OWASP block, with a weight of 1–3; four are critical (GOV-1, MAP-1, MAN-1, MAN-2).",
    "<code>gap_analysis</code> earns full weight for <em>met</em>, half for <em>partial</em>, none for <em>missing</em>, and reports the percentage. A critical control that is missing is escalated to CRITICAL severity; a partial one drops one level.",
    "<code>validate_raci</code> counts Accountable and Responsible codes per activity; <code>A/R</code> counts as both.",
    "<code>zero_trust_audit</code> checks each component for an audit trail (CRITICAL if absent, and it sets the go-live block), a distinct identity, least privilege, and a human gate on irreversible actions.",
    "<code>remediation_plan</code> puts Zero-Trust criticals first, then checklist gaps by severity. The same root cause can appear twice (the executor's missing audit trail and control MAN-1), seen from the engineering and the governance side.",
])}
<h3>Part 6 — Build it in</h3>
{sand}
<p>The stand-in model has been quietly steered: for any request mentioning a backup it proposes <code>delete_snapshots</code>. The input check sees an innocent request and passes it; the output check rejects a tool that is not on the allowlist.</p>
<h3>Part 7 — Look ahead</h3>
{steps([
    "Each inventory row names a component, its algorithm, its use, and how many years the protected data must stay secret.",
    "<code>pqc_triage</code> marks post-quantum and hybrid algorithms OK, AES-128 as UPGRADE, quantum-safe symmetric and hash algorithms OK, and quantum-vulnerable public-key algorithms PLAN, or MIGRATE NOW for key exchange when Mosca's inequality says the data outlives the migration window.",
    "Planning assumptions are explicit: 4 years to migrate, 10 years to a quantum threat. Change them and the triage changes.",
])}
'''))

    O = []
    O.append(outcome("EU AI Act tiers",
        out_block(output(C, "PROHIBITED = {")),
        "<p>The SOC agent built in Labs 1–5 is minimal-risk, so the Act asks little of it. A CV-screening agent is high-risk with logging and oversight duties, and workplace emotion recognition is prohibited. Your security controls should not depend on the tier: liability for what an autonomous agent does sits with its operator either way.</p>"))
    O.append(outcome("Checklist score and ranked gaps",
        out_block(output(C, "profile = {")),
        "<p>66/100 looks like a pass, but one critical control is open: MAN-1, signed audit events. The ranked list is the order to work in.</p>"))
    O.append(outcome("RACI validation",
        out_block(output(C, "def validate_raci")),
        "<p>The validator finds a real gap in the course's own RACI: <em>Define AI use policy</em> has an accountable owner (Legal/Privacy) but nobody responsible for doing the work. It reads fine by eye, which is why you validate a RACI like code.</p>"))
    O.append(outcome("Zero-Trust audit",
        out_block(output(C, "components = [")),
        "<p>The executor has no signed audit trail, so go-live is BLOCKED. It is also over-privileged, and the tool gateway has no identity of its own. The planner is clean.</p>"))
    O.append(outcome("The governance report",
        out_block(output(C, "governance_report(profile, components);")),
        "<p>The same root cause leads the plan twice, once as a component finding and once as a checklist gap. In the exercise, fixing the executor and the gateway and recording MAN-1 and MAN-3 as met clears go-live at 80/100 with no critical gaps. Both gates had to agree.</p>"))
    O.append(outcome("The determinism sandwich",
        out_block(output(C, "def sandwich")),
        "<p>The legitimate CVE lookup and host isolation pass. The injection is stopped at input. The hijacked <code>delete_snapshots</code> call came from an innocent-looking request and is stopped at output. All four decisions are signed into the audit trail. The model was never trusted to police itself.</p>"))
    O.append(outcome("Post-quantum triage",
        out_block(output(C, "QUANTUM_VULNERABLE")),
        "<p>ECDH on the agent-to-tool link protects data that must stay secret for 7 years; with 4 years to migrate and 10 to a quantum threat, it should migrate now. AES-128 needs an upgrade to AES-256. RSA-2048 signing goes on the roadmap. The HMAC audit chain and the hybrid ML-KEM VPN are already fine.</p>"))
    P.append(("outcomes", "Expected outcomes and what they mean", "".join(O)))

    P.append(("takeaways", "Key takeaways", takeaways([
        "Classify first: the EU AI Act tier sets the legal floor, but your security controls should not depend on it.",
        "Governance is a deployable control layer: data plus a few functions that can block a release.",
        "One control is a hard gate. No signed audit trail blocks go-live regardless of the score.",
        "A RACI names exactly one accountable owner per activity; validate it like code.",
        "The determinism sandwich puts governance in the runtime: deterministic checks around the model, every decision signed.",
        "Post-quantum readiness starts with an inventory; key exchange protecting long-lived data moves first.",
    ])))
    return P
