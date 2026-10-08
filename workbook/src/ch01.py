from wb import *

C = "Ch01"


def build():
    P = []

    # ------------------------------------------------------------ introduction
    P.append(("intro", "Introducing the lab", f'''
<p class="lede">An AI agent is a language model placed inside a loop: it perceives, interprets, reasons, acts through tools, and learns from the result. This lab builds a minimal but complete security agent and shows where its tools — and its attack surface — come from.</p>
<p>You start with the detectors that an agent calls as tools. You run four of them on the same real network traffic and see that each has a different blind spot. Then you wrap them in an agent: a cognitive loop, tools declared as JSON schemas, a gateway that enforces those schemas, and an audit log that records every call. Finally, you attack your own agent with hijacked tool calls and watch the gateway deny them.</p>
<p>The idea to carry forward from this lab: <strong>the agent is only as safe as the tools it is given and the checks around them</strong>. Every later chapter builds on the audit log you create here.</p>
<ul class="facts"><li><b>Time</b> about 1 h 25 min</li><li><b>Data</b> CICIDS-2017 sample, 102,999 flows</li><li><b>Libraries</b> numpy, pandas, scikit-learn</li><li><b>API key</b> optional (Part 3 only)</li></ul>
'''))

    # ------------------------------------------------------------ terms
    P.append(("terms", "Key terms", terms([
        ("AI agent", "A language model wrapped in a loop that lets it choose and run actions (tool calls) toward a goal, without a human approving each step."),
        ("Cognitive loop", "The agent's cycle: <em>perceive → interpret → reason → act → learn</em>. It descends from Boyd's OODA loop (observe, orient, decide, act)."),
        ("Autonomy ladder", "Chatbot → assistant → copilot → agent → multi-agent. Each rung adds capability and attack surface."),
        ("Tool / function calling", "The model emits a structured request, such as <code>{\"name\": \"lookup_cve\", \"arguments\": {...}}</code>, and the agent runs it."),
        ("Tool schema", "A JSON description of a tool: its name, purpose, and typed parameters. When enforced, it is the authorization boundary."),
        ("Model Context Protocol (MCP)", "An open standard for serving tools to agents: Host → Client → Server, over a transport such as <code>stdio</code>."),
        ("Isolation Forest", "An unsupervised detector that isolates points with random splits. Points isolated in few splits are anomalies. It needs no labels."),
        ("Supervised detector", "A classifier trained on labelled examples (here, a random forest). Strong on attacks it has seen, blind to new ones."),
        ("TF-IDF", "Term frequency × inverse document frequency. It turns text into a weighted word vector so a linear model can classify it."),
        ("Embedding & cosine similarity", "A vector representation of an item. Cosine similarity is near 1 for vectors that point the same way and near 0 for unrelated ones."),
        ("Autoencoder", "A network trained to reproduce its input through a narrow bottleneck. A high reconstruction error means the input is unlike the training data."),
        ("Lift", "The attack share among flagged items divided by the attack share overall. Above 1 means flags are better than random."),
        ("Typosquat", "A domain registered to look like a real one, such as <code>paypa1-secure.com</code> for <code>paypal.com</code>."),
        ("Excessive agency", "OWASP LLM06: an agent has more tools or permissions than its task needs, so a hijack does real damage."),
        ("Audit log", "A record of every tool call, allowed or denied. It is the evidence that Zero Trust verification runs on."),
    ])))

    # ------------------------------------------------------------ structure
    f = Flow(5, 2, cw=178, rh=110, bh=62)
    f.node("setup", 0, 0, "Setup", "key + CICIDS sample", kind="terminal")
    f.node("p1", 1, 0, "Part 1", "four detectors", kind="step")
    f.node("p2", 2, 0, "Part 2", "loop · gateway · log", kind="defend")
    f.node("p3", 3, 0, "Part 3", "live LLM reasoner", kind="step")
    f.node("wrap", 4, 0, "Quiz +\ntakeaways", kind="terminal")
    f.node("alert", 1, 1, "Top-scored flow", "the alert", kind="data")
    f.node("hijack", 2, 1, "Hijacked calls", "4 malicious", kind="attack")
    f.node("audit", 3, 1, "Audit log", "ALLOW / DENY", kind="data")
    f.edge("setup", "p1", "flows").edge("p1", "p2").edge("p2", "p3").edge("p3", "wrap")
    f.edge("p1", "alert", "emits").edge("alert", "p2", "triaged by")
    f.edge("hijack", "p2", "attacks").edge("p2", "audit", "writes")
    struct = figure(f, "The lab's flow. Part 1 produces a real alert (the Isolation Forest's top-scored flow); Part 2 triages it with an agent whose gateway also faces four hijacked calls; every call lands in the audit log; Part 3 swaps a live LLM into the Reason step.")
    P.append(("structure", "How the lab is structured", LEGEND + struct + f'''
<div class="tblwrap"><table class="tbl"><thead><tr><th>Part</th><th>You do</th><th>You produce</th></tr></thead><tbody>
<tr><td>Setup</td><td>Load the optional API key and the CICIDS-2017 sample</td><td><code>flows</code> DataFrame, <code>client</code> (or <code>None</code>)</td></tr>
<tr><td>1 · Detectors</td><td>Run Isolation Forest, a random forest, a TF-IDF phishing model, character-n-gram embeddings and an autoencoder</td><td>An alert, plus a measured blind spot for each detector</td></tr>
<tr><td>2 · The agent</td><td>Build the cognitive loop, a schema-enforcing <code>ToolRegistry</code> and an audit log, then attack it</td><td>A triage verdict and an audit log with ALLOW and DENY entries</td></tr>
<tr><td>3 · Live reasoner</td><td>Plug a real LLM into the Reason step</td><td>One LLM-chosen action, logged</td></tr>
</tbody></table></div>
<h3>Hands-on exercises</h3>
''' + exercises([
        ("Tune the typosquat screen", "Part 1.4", "Pick a threshold and an allowlist that flag exactly the five lookalike domains"),
        ("Add a least-privilege tool", "Part 2", "Declare a <code>geoip_lookup</code> schema whose pattern only accepts IPv4 addresses"),
    ])))

    # ------------------------------------------------------------ logic
    d = Flow(3, 3, cw=250, rh=92, bh=58)
    d.node("data", 0, 1, "CICIDS-2017", "102,999 flows · 78 features", kind="data")
    d.node("if", 1, 0, "Isolation Forest", "no labels", kind="step")
    d.node("rf", 1, 1, "Random forest", "labels", kind="step")
    d.node("ae", 1, 2, "Autoencoder", "benign-only training", kind="step")
    d.node("o1", 2, 0, "Finds the rare", "misses common attacks", kind="decision", w=200, h=74)
    d.node("o2", 2, 1, "Finds the known", "misses novel attacks", kind="decision", w=200, h=74)
    d.node("o3", 2, 2, "Finds 'not normal'", "needs a clean baseline", kind="decision", w=200, h=74)
    for a, b in [("data", "if"), ("data", "rf"), ("data", "ae")]:
        d.edge(a, b)
    d.edge("if", "o1").edge("rf", "o2").edge("ae", "o3")
    det = figure(d, "Same traffic, three detectors, three different blind spots. This is why an agent should weigh several detectors' evidence rather than act on one.")

    l = Flow(5, 3, cw=172, rh=104, bh=58)
    l.node("alert", 0, 0, "Alert", "flow-11389 · 0.736", kind="data")
    l.node("per", 1, 0, "Perceive", kind="step")
    l.node("int", 2, 0, "Interpret", kind="step")
    l.node("rea", 3, 0, "Reason", "LLM or rules", kind="step")
    l.node("inj", 4, 0, "Injected\ninstruction", kind="attack")
    l.node("gate", 3, 1, "Schema\nvalid?", kind="decision", w=130, h=78)
    l.node("act", 2, 1, "Act", "run the tool", kind="step")
    l.node("learn", 1, 1, "Learn", "append to memory", kind="step")
    l.node("deny", 4, 1, "DENY", "call never runs", kind="defend")
    l.node("log", 2, 2, "Audit log", "every call, both outcomes", kind="data")
    l.edge("alert", "per").edge("per", "int").edge("int", "rea").edge("inj", "rea", "steers", dashed=True)
    l.edge("rea", "gate", "tool call").edge("gate", "act", "yes").edge("gate", "deny", "no")
    l.edge("act", "learn").edge("learn", "per", "next cycle")
    l.edge("act", "log", "ALLOW").edge("deny", "log", "DENY", route="vh")
    loop = figure(l, "The cognitive loop with a gateway between Reason and Act. A hijacked Reason step can only propose a call; the gateway decides deterministically, and both outcomes are logged.")

    g = Flow(7, 2, cw=160, rh=112, bh=56)
    g.node("call", 0, 0, "Tool call", "name + args", kind="data", w=118)
    checks = [("reg", "registered?", "unknown tool"), ("req", "required\nargs?", "missing arg"),
              ("ext", "only known\nargs?", "extra arg"), ("typ", "types\nmatch?", "wrong type"),
              ("pat", "pattern\nmatch?", "fails pattern")]
    prev = "call"
    for i, (k, q, why) in enumerate(checks, start=1):
        g.node(k, i, 0, q, kind="decision", w=118, h=76)
        g.node(k + "d", i, 1, "DENY", why, kind="defend", w=112, h=50)
        g.edge(prev, k, "yes" if prev != "call" else None).edge(k, k + "d", "no")
        prev = k
    g.node("run", 6, 0, "Execute", "log ALLOW", kind="step", w=112)
    g.edge(prev, "run", "yes")
    gate = figure(g, "<code>ToolRegistry._validate</code> as a decision chain. The first failed check denies the call with a reason; only a call that passes all five executes. <code>re.fullmatch</code> makes the pattern check reject smuggled suffixes such as <code>; DROP TABLE</code>.")

    P.append(("logic", "The logic", f'''
<h3>Part 1 — Detectors are the agent's tools</h3>
<p>Each detector answers a different question about the same flows, so each fails in a different place.</p>
{LEGEND}{det}
{steps([
    "<b>Isolation Forest</b> fits 200 random trees to all 102,999 flows, scores each flow by how quickly it is isolated (<code>score = -score_samples</code>), and flags the top 1% (<code>contamination=0.01</code>). The highest-scoring flow becomes the <code>alert</code> the agent triages in Part 2.",
    "<b>Lift</b> compares the attack share among the flagged flows with the overall attack share (21.6%). It tells you whether a flag is worth an analyst's time.",
    "<b>Random forest</b> trains on labels (benign vs. attack) with a stratified 70/30 split. A second loop then removes one attack class from training entirely and measures recall on that class alone, simulating a novel attack.",
    "<b>TF-IDF phishing model</b> learns lure vocabulary from 16 inline emails and scores three test messages, one of them a business-email-compromise opener with no lure words.",
    "<b>Character n-gram embeddings</b> turn domain names into vectors; each new certificate is compared with four brand domains by cosine similarity against a threshold.",
    "<b>Autoencoder</b> (a scikit-learn MLP, 32-8-32) trains on 20,000 benign flows after a <code>log1p</code> transform and standardization, then scores every flow by reconstruction error. Its top 1% is compared with the forest's top 1%.",
])}
<h3>Part 2 — The agent: loop, gateway, and audit log</h3>
{loop}
{steps([
    "<code>cognitive_loop</code> runs <code>perceive → interpret → reason → act → learn</code> until <code>done(goal)</code>, calling <code>log(action, result)</code> on every iteration.",
    "Tools are declared as JSON schemas (<code>TOOLS</code>). The lab hardens <code>lookup_cve</code> with a <code>pattern</code> so <code>cve_id</code> must look like <code>CVE-YYYY-NNNN</code>.",
    "<code>ToolRegistry.call</code> validates every call before running it and appends an ALLOW or DENY record to <code>registry.audit</code>. A tool that raises an exception returns an error instead of crashing the agent.",
    "Five calls are replayed as if a hijacked model emitted them: an unregistered <code>run_shell</code>, argument smuggling, an extra <code>export_to</code> argument, a wrong type, and one legitimate call.",
    "The worked flow wires a deterministic reasoner and a read-only CVE tool into the loop: it enriches the real alert, reads CVSS 10.0, and escalates.",
    "<code>build_mcp_server</code> shows the same detector served as an MCP tool over <code>stdio</code>. It blocks while serving, so it runs as its own process, not in the notebook.",
])}
{gate}
<h3>Part 3 — A live reasoner</h3>
<p><code>LLMReasoner.reason</code> sends the interpreted state and goal to <code>gpt-4o-mini</code> and returns one short action, which the loop records. The notebook points out the flaw on purpose: the demo's <code>Tools.run</code> executes free text, which is the excessive-agency anti-pattern. In production, that output would pass through <code>ToolRegistry.call</code>.</p>
'''))

    # ------------------------------------------------------------ outcomes
    O = []
    O.append(outcome("Isolation Forest: the outliers and their true labels",
        out_block(output(C, "# Run the detector and keep its top-scored flow")),
        "<p>About 1% of flows (1,030) are flagged, and 918 of them are benign. The flagged attacks are the genuinely rare ones: slowloris, Infiltration and every Heartbleed flow. The top-scored flow, which becomes the agent's alert, is itself benign. That is the first lesson of the lab: <strong>anomaly is not attack</strong>, so every flag needs triage before anyone acts on it.</p>"))
    O.append(outcome("Lift below 1",
        out_block(output(C, "def lift(")),
        "<p>A flagged flow is <em>half</em> as likely to be an attack as a random flow (lift 0.50×). Isolation Forest assumes attacks are rare, but in this sample DDoS and PortScan account for thousands of flows each, so they form their own dense cluster and look normal. It still catches 11 of 11 Heartbleed flows and 13 of 36 Infiltration flows, the attacks that really are rare.</p>"))
    O.append(outcome("Supervised detection and novel attacks",
        out_block(output(C, "supervised_detector(X, y)")),
        "<p>With labels the random forest is near-perfect (F1 0.994), but remove one attack class from training and recall on that class collapses to 0% for Bot, FTP-Patator and Infiltration. Slowloris is partly caught (60%) because it resembles other DoS traffic in the training set. Supervised detectors recognize yesterday's attacks; the unsupervised forest, with no labels at all, caught a third of Infiltration. The two fail differently, so a defender runs both.</p>"))
    O.append(outcome("Phishing: the lure without lure words",
        out_block(output(C, "EMAILS = [")),
        "<p>The classic lure scores 0.80. The business-email-compromise opener scores 0.44, below the 0.5 line, so it would be delivered. It uses none of the vocabulary the model learned. A bag-of-words model encodes known attacks, and a language model can write lures that avoid them.</p>"))
    O.append(outcome("Typosquat similarity",
        out_block(output(C, "BRANDS = [")),
        "<p>Real lookalikes score high (<code>rnicrosoft.com</code> 0.72, <code>pypal.com</code> 0.67). But the legitimate <code>gitlab.com</code> scores 0.40, the same as the <code>paypa1-secure.com</code> lookalike, and <code>okta-sso.help</code> falls below the threshold. No single threshold separates them. The exercise fixes it with a lower threshold for recall plus an allowlist of known-good domains to remove the known false positive.</p>"))
    O.append(outcome("Autoencoder vs. Isolation Forest",
        out_block(output(C, "def autoencoder_scores")),
        "<p>The autoencoder's top 1% is 90% real attacks, against 11% for the forest. Two design choices explain it: it learned from a <em>known-benign</em> baseline, and log-scaling stopped huge byte counts from dominating. The two detectors agree on only 28 flows because they measure different things. That is why combining them adds coverage.</p>"))
    O.append(outcome("The gateway against a hijacked reasoner",
        out_block(output(C, "hijacked_calls = [")),
        "<p>Four DENY records and one ALLOW, each with a reason, all in the audit log. The model was never asked whether a call was safe; the gateway decided deterministically. This pattern returns in Chapter 6 as the <em>determinism sandwich</em>.</p>"))
    O.append(outcome("Worked triage of the real alert",
        out_block(output(C, "# alert is REAL")),
        "<p>Two tool calls, both logged: the agent enriches the alert with a read-only CVE lookup, sees CVSS 10.0 and escalates. A single read-only tool gives a small, auditable action surface. This is least privilege in its simplest form.</p>"))
    O.append(outcome("Live reasoner (Part 3)",
        out_block("LLM-chosen action : Investigate flow-11389 for unusual activity.\n"
                  "action-log entry  : ('Investigate flow-11389 for unusual activity.', 'executed: Investigate flow-11389 for unusual activity.')", live=True),
        "<p>With a key, the model proposes a sensible next step and the loop logs it. Without a key the cell prints <code>skipped (no API key)</code>. Notice that <code>Tools.run</code> “executes” the free-text action. That is exactly what Part 2's gateway exists to prevent.</p>"))
    P.append(("outcomes", "Expected outcomes and what they mean", "".join(O)))

    # ------------------------------------------------------------ takeaways
    P.append(("takeaways", "Key takeaways", takeaways([
        "An agent is a perceive → interpret → reason → act → learn loop over tools; autonomy means every tool call is a decision to secure.",
        "Detectors are the agent's tools, and each has a blind spot: unsupervised misses common attacks, supervised misses novel ones. Use both and weigh agreement.",
        "Anomaly is not attack. Measure lift before trusting a detector's flags.",
        "A tool schema is a boundary only when a gateway enforces it. Unregistered tools, smuggled arguments and wrong types are denied deterministically.",
        "Logging every call, allowed or denied, is the foundation every later governance control builds on.",
    ])))
    return P
