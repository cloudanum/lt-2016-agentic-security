from wb import *

C = "Ch04"


def build():
    P = []
    P.append(("intro", "Introducing the lab", '''
<p class="lede">Attacks on AI systems are not one thing. This lab works through the layers of the AI attack surface (training data, the model, the inference channel, the software supply chain and the host) and, for each, measures an attack on your own sandbox and runs the control that counters it.</p>
<p>Every demonstration runs on a synthetic dataset or sample artifacts you own. The emphasis is on <em>measurement</em>: how much damage, at what cost to the attacker, and how much a specific control gives back. The chapter closes with a kill-chain table that pairs each attack with its MITRE ATLAS technique and the defense you built.</p>
<p>The idea to carry forward: <strong>every layer has a measurable weakness and a measurable defense</strong>, and one intrusion can chain several layers together.</p>
<ul class="facts"><li><b>Time</b> about 1 h 40 min</li><li><b>Data</b> synthetic 12-feature classifier data · sample memory artifacts</li><li><b>Libraries</b> numpy, scikit-learn</li><li><b>API key</b> optional (LLM triage and import audit)</li></ul>
'''))

    P.append(("donow", "Do it now", donow(4, "Name the surface",
        "Individual",
        "Paper or the chat window; the sketch on the board",
        "Chat line: <code>S1-data: ... | S2-model: ... | S3-channel: ... | S4-host: ...</code>",
        "Parts 1–4 of this lab: each surface you label becomes one attack lane you run and then defend, and the four lanes close in the kill-chain table",
        "Take a simple sketched LLM application and mark the four places an attacker can touch it, with one attack idea for each. This is threat modelling in miniature: start from where the attacker can reach, not from the defenses you happen to have.",
        "One chat line naming all four surfaces and one attack per surface, in the exact capture format below.",
        [
            "The sketch, drawn on the board or posted in chat: <code>user → API → model → tools</code>, a <b>training-data store</b> feeding the model, and everything running on a <b>host VM</b>.",
            "Paper and a pen, or just the chat window.",
        ],
        [
            (1, "<b>Copy</b> the sketch: user → API → model → tools across the top, the training-data store feeding the model, and a box underneath labelled <i>host VM</i> that holds all of it."),
            (1, "<b>Label</b> the four surfaces an attacker can touch, using the lab's names: <code>S1</code> training data, <code>S2</code> the model, <code>S3</code> the inference channel (the request path user → API → model → tools), <code>S4</code> the host."),
            (2, "<b>Attack</b>: next to each label, write one attack idea as a short attacker action — not a defense, not a worry. Example shape: <i>flip training labels so the model waves malware through</i>."),
            (1, "<b>Post</b> your capture line in chat: <code>S1-data: &lt;attack&gt; | S2-model: &lt;attack&gt; | S3-channel: &lt;attack&gt; | S4-host: &lt;attack&gt;</code>"),
        ],
        "All four surfaces are labelled on your sketch, each carries one attack idea phrased as something the attacker <i>does</i>, and your line is in chat.",
        [
            ("Before class", "Draw the sketch on the board before learners arrive and paste the ASCII version plus the capture-line template into chat, so nobody retypes it. The lab has not been opened yet — that is the point."),
            ("Watch for", "Four variations of prompt injection, one per surface. It is the only AI attack most learners can name, so everything lands on the channel. Ask: what can an attacker do <i>before any user sends a prompt</i> (training data), and what does the model physically run on (host)? Also watch for “steal the API key” filed under the model — that is a credential problem; ask where the key lives."),
            ("Fallback", "No board or a remote room: post the ASCII sketch in chat and have learners reply with their labelled copy and capture line. Same five minutes, same deliverable."),
        ],
        "<i>Attack the diagram first:</i> a threat model starts from where the attacker can touch the system, and the lab then works one layer at a time down exactly those surfaces.",
        "<i>One-surface thinking:</i> treating “AI security” as prompt injection and leaving the training data and the host unguarded — the two surfaces this lab shows are quiet and cheap to attack.",
        [
            ("https://atlas.mitre.org/", "MITRE ATLAS", "MITRE"),
            ("https://owasp.org/www-project-top-10-for-large-language-model-applications/", "OWASP Top 10 for LLM Applications", "OWASP"),
            ("https://www.nist.gov/itl/ai-risk-management-framework", "NIST AI Risk Management Framework", "NIST"),
        ],
        """Sketch: user -> API -> model -> tools
        training-data store -> model (training)
        all of it inside the host VM

S1-data: flip labels so the model learns to wave malware through (poisoning)
S2-model: query the prediction API thousands of times and train a copy (extraction)
S3-channel: split a blocked request across turns so no single message trips the filter
S4-host: hollow a legitimate process on the VM and run the implant in memory only""",
        [
            "Four surfaces at four distinct layers: the data <i>before</i> training, the model itself, the request path every user shares, and the machine it all runs on.",
            "Attack ideas phrased as attacker actions (<i>flip labels</i>, <i>train a surrogate</i>, <i>split the payload</i>), not defenses or vague worries like “hack the AI”.",
            "The instructive wrong answer is prompt injection on every surface — use it to ask what an attacker can do before any prompt is ever sent.",
            "“Steal the API key” belongs on the host or credential store, not the model; bonus to anyone who also marks the tools as part of the channel surface.",
        ])))

    P.append(("terms", "Key terms", terms([
        ("Attack surface", "Everything an attacker can touch. For AI: training data, model, inference channel, supply chain, and the host the model runs on."),
        ("Label-flip poisoning", "Changing labels in training data so the trained model learns the wrong boundary. MITRE ATLAS AML.T0020."),
        ("Targeted poisoning", "Flipping labels of one class only (malicious → benign) so the model misses exactly that class."),
        ("Recall (malicious class)", "The share of truly malicious samples the model catches. The metric targeted poisoning attacks."),
        ("Label-consistency check", "Flagging training rows whose nearest neighbours mostly carry a different label, then removing them before training."),
        ("Model extraction", "Training a copy (a surrogate) from a model's API outputs alone. MITRE ATLAS AML.T0024.002."),
        ("Agreement", "The share of test inputs on which the surrogate and the real model give the same answer."),
        ("Query budget", "A cap on how many predictions one client may request; it caps how good a stolen surrogate can get."),
        ("Side channel", "Information leaked by how a system behaves (time, size, power) rather than by what it returns."),
        ("Constant-time response", "Padding every response to a fixed minimum duration so timing no longer reveals internal work."),
        ("Payload splitting", "Spreading content across several turns so that no single message trips a per-message filter."),
        ("Session-level moderation", "Evaluating the whole conversation for patterns, not each message alone."),
        ("Slopsquatting", "Registering a package name that language models tend to invent, so developers who trust generated code install it. Supply chain: AML.T0010."),
        ("Import name vs. package name", "What code imports (<code>nmap</code>) can differ from what pip installs (<code>python-nmap</code>)."),
        ("Memory forensics", "Analysing a RAM image (here with Volatility 3 plugins such as <code>pslist</code> and <code>malfind</code>) to find code that never touched disk."),
        ("Process hollowing", "Starting a legitimate process and replacing its memory with other code. ATT&amp;CK T1055.012."),
        ("RWX region", "Memory that is readable, writable and executable at once, a classic sign of injected code."),
    ])))

    f = Flow(7, 2, cw=150, rh=112, bh=62)
    f.node("setup", 0, 0, "Setup", "shared dataset", kind="terminal")
    f.node("p1", 1, 0, "Part 1", "training data")
    f.node("p2", 2, 0, "Part 2", "the model")
    f.node("p3", 3, 0, "Part 3", "inference channel")
    f.node("p4", 4, 0, "Part 4", "host & memory")
    f.node("kc", 5, 0, "Kill chain", "attack ↔ defense", kind="data")
    f.node("wrap", 6, 0, "Quiz +\ntakeaways", kind="terminal")
    f.node("d1", 1, 1, "Label check", kind="defend")
    f.node("d2", 2, 1, "Query budget", kind="defend")
    f.node("d3", 3, 1, "Padding · session\nmoderation · audit", kind="defend", h=64)
    f.node("d4", 4, 1, "Lookalike triage", kind="defend")
    for a, b in [("setup", "p1"), ("p1", "p2"), ("p2", "p3"), ("p3", "p4"), ("p4", "kc"), ("kc", "wrap")]:
        f.edge(a, b)
    for a, b in [("p1", "d1"), ("p2", "d2"), ("p3", "d3"), ("p4", "d4")]:
        f.edge(a, b, "countered by")
    P.append(("structure", "How the lab is structured", LEGEND + figure(f,
        "The lab walks down the attack surface one layer per part. Each part measures an attack, then runs the control beneath it; the kill-chain table at the end collects all the pairs.") + '''
<div class="tblwrap"><table class="tbl"><thead><tr><th>Part</th><th>Measured attack</th><th>Control you run</th></tr></thead><tbody>
<tr><td>1 · Training data</td><td>Random vs. targeted label flips at equal budgets</td><td>Nearest-neighbour label check, sanitize, retrain</td></tr>
<tr><td>2 · Model</td><td>Surrogate agreement vs. number of queries</td><td><code>GuardedAPI</code> per-client query budget</td></tr>
<tr><td>3 · Inference channel</td><td>Latency vs. hidden length; split turns vs. a per-message filter; invented imports</td><td>Constant-time padding; <code>session_moderator</code>; import + PyPI audit</td></tr>
<tr><td>4 · Host &amp; memory</td><td>Lookalike process with an injected RWX region (sample artifacts)</td><td>Rule triage, optional LLM triage, edit-distance lookalike detector</td></tr>
</tbody></table></div>
<h3>Hands-on exercise</h3>''' + exercises([
        ("A lookalike detector that generalises", "Part 4", "Write <code>is_lookalike</code> with <code>difflib</code> similarity against known Windows process names"),
    ])))

    a = Flow(5, 2, cw=176, rh=112, bh=60)
    a.node("tr", 0, 0, "Training labels", kind="data")
    a.node("fl", 1, 0, "Flip 10% of rows", "random or targeted", kind="attack")
    a.node("knn", 2, 0, "k = 10 neighbours", "standardized features", kind="defend")
    a.node("dis", 3, 0, "≥ 60%\ndisagree?", kind="decision", h=86)
    a.node("drop", 3, 1, "Drop row", kind="defend")
    a.node("keep", 4, 0, "Retrain on\nremaining rows", kind="step")
    a.node("eval", 4, 1, "Clean test set", "trusted", kind="data")
    a.edge("tr", "fl").edge("fl", "knn").edge("knn", "dis").edge("dis", "keep", "no").edge("dis", "drop", "yes").edge("eval", "keep", "measures")
    pois = figure(a, "Finding poisoned labels. A flipped label sits among neighbours that mostly disagree with it. The check runs on the training data before training, and the result is judged on a clean, trusted test set.")

    b = Flow(5, 2, cw=170, rh=112, bh=60)
    b.node("q", 0, 0, "Random queries", "scaled to the feature stats", kind="attack")
    b.node("api", 1, 0, "budget\nleft?", kind="decision", h=86)
    b.node("model", 2, 0, "Victim model", "predict()")
    b.node("lab", 3, 0, "Labelled queries", kind="data")
    b.node("sur", 4, 0, "Surrogate", "random forest", kind="attack")
    b.node("deny", 1, 1, "Refuse + log", "PermissionError", kind="defend")
    b.edge("q", "api").edge("api", "model", "yes").edge("model", "lab", "labels").edge("lab", "sur", "fit").edge("api", "deny", "no")
    ext = figure(b, "Model extraction through the prediction API, and the query budget in front of it. Agreement grows with queries, so capping queries caps the copy.")

    c = Flow(4, 2, cw=200, rh=110, bh=60)
    c.node("t", 0, 0, "Conversation turns", kind="data")
    c.node("pm", 1, 0, "Per-message\nfilter", "each turn alone", kind="step")
    c.node("pass", 2, 0, "Every turn passes", kind="attack")
    c.node("sm", 1, 1, "Session moderator", "all turns joined", kind="defend")
    c.node("sig", 2, 1, "≥ 3 signals?", "fragments · assembly ·\nsensitive · framing", kind="decision", h=96, w=210)
    c.node("blk", 3, 1, "BLOCK", kind="defend")
    c.edge("t", "pm").edge("pm", "pass").edge("t", "sm", route="vh").edge("sm", "sig").edge("sig", "blk", "yes")
    split = figure(c, "Why session-level moderation catches what per-message filters miss: the signals only co-occur in the combined conversation.")

    d = Flow(4, 2, cw=200, rh=110, bh=60)
    d.node("imp", 0, 0, "Import name", "parsed with ast", kind="data")
    d.node("std", 1, 0, "standard\nlibrary?", kind="decision", h=86)
    d.node("ins", 2, 0, "installed\nlocally?", kind="decision", h=86)
    d.node("py", 3, 0, "on PyPI?", "real package name", kind="decision", h=86)
    d.node("ok", 1, 1, "stdlib", kind="defend")
    d.node("vet", 2, 1, "installed", "vet the package", kind="step")
    d.node("res", 3, 1, "Exists → vet · missing →\nlikely invented", kind="defend", h=64)
    d.edge("imp", "std").edge("std", "ok", "yes").edge("std", "ins", "no").edge("ins", "vet", "yes").edge("ins", "py", "no").edge("py", "res")
    imp = figure(d, "<code>audit_imports</code>. Generated code is parsed, never executed. The import name is mapped to the package name before PyPI is asked; with no network the verdict is “verify by hand”.")

    P.append(("logic", "The logic", f'''
<h3>Part 1 — Training data</h3>
{LEGEND}
{steps([
    "<code>poison_labels</code> flips a fraction of labels, either across all rows or only within one class (<code>target=1</code>), and returns the flipped indices so detection can be scored.",
    "To compare fairly, both variants flip the same share of <em>all</em> training rows (5%, 10%, 20%); the targeted rate is divided by the malicious share to get there.",
    "<code>suspicious_labels</code> standardizes the features, finds each row's 10 nearest neighbours, and flags rows where at least 60% of neighbours disagree. Dropping the flagged rows and retraining is the sanitize step.",
])}
{pois}
<h3>Part 2 — The model</h3>
{ext}
{steps([
    "<code>extract_surrogate</code> draws random inputs at the feature scale an outsider could estimate, labels them with the victim's <code>predict</code>, and fits a random-forest surrogate. Agreement is averaged over three runs per budget.",
    "<code>GuardedAPI</code> counts predictions per client and raises <code>PermissionError</code> once the budget (25 here) is spent, logging the refusal.",
])}
<h3>Part 3 — The inference channel</h3>
{steps([
    "<b>Timing.</b> <code>median_latency</code> times a stand-in generator whose work grows with a hidden length, taking the median of repeated calls. <code>padded</code> wraps it so no response returns before 4 ms (a busy-wait, because <code>sleep</code> is too coarse at this scale).",
    "<b>Splitting.</b> A per-message blocklist passes every turn of a three-turn story that assembles a harmless passphrase. <code>session_moderator</code> joins all turns and counts four pattern signals; three or more blocks the session.",
    "<b>Supply chain.</b> <code>audit_imports</code> classifies each import as standard library, installed, on PyPI, or missing from PyPI. With a key, the script it audits is generated live.",
])}
{split}
{imp}
<h3>Part 4 — Host and memory</h3>
<p><code>triage_dump</code> collects process and injected-memory artifacts with Volatility 3 when given a dump, and otherwise uses bundled sample artifacts. Its deterministic triage applies two rules, a lookalike process name and a region that is both writable and executable, and returns a risk level with next steps. With a key, the same artifacts go to a language model whose answer is a suggestion for the analyst. The exercise replaces the hard-coded lookalike table with edit similarity, which catches names nobody listed in advance.</p>
'''))

    O = []
    O.append(outcome("Random vs. targeted poisoning at the same budget",
        out_block(output(C, "# Same attacker budget")),
        "<p>With 20% of rows tampered, random flips reduce malicious recall from 0.84 to 0.74; targeted flips reduce it to 0.42. Random noise is partly averaged away by the forest, while targeted flips teach the detector to miss exactly one class. At small budgets the numbers are noisy (random 10% even shows a slight rise), which is why poisoning is measured across several rates.</p>"))
    O.append(outcome("Finding and removing the poison",
        out_block(output(C, "def suspicious_labels")),
        "<p>The neighbourhood check flags 92 rows and finds 82% of the 56 flipped labels, at the cost of removing some clean rows (50% precision). Retraining on what remains recovers recall from 0.70 to 0.79, most of the way back to the clean 0.84. The check only works because the test set is clean and trusted, so evaluation data needs the same protection as the model.</p>"))
    O.append(outcome("Extraction grows with queries",
        out_block(output(C, "def extract_surrogate")),
        "<p>Agreement climbs from 69% at 25 queries to 93% at 6,400. Most of the gain comes in the first few hundred queries. That curve is the attacker's cost model, and it is what a query budget acts on.</p>"))
    O.append(outcome("The query budget",
        out_block(output(C, "class GuardedAPI")),
        "<p>The 6,400-query attempt is refused and logged, and the best copy possible inside a 25-query budget agrees only 69% of the time. In production this is a rate limit per client and time window, plus monitoring for query patterns that do not look like real traffic.</p>"))
    O.append(outcome("Timing side channel and padding",
        out_block(output(C, "def padded(")),
        "<p>Raw latency rises with the hidden length (0.18 → 0.73 → 1.49 ms), so timing reveals internal work. With a 4 ms floor every response takes 4.0 ms and the signal is gone. The floor must sit above the slowest legitimate case; the cost is a small, fixed delay.</p>"))
    O.append(outcome("Per-message filter vs. session moderation",
        out_block(output(C, "# A naive per-message", keep=r"passes|assembled") + "\n\n" + output(C, "SPLIT_SIGNALS = {")),
        "<p>Each turn passes the per-message filter. The session moderator allows turn 1, then blocks at turn 2, when fragment definitions, a sensitive target and piecewise framing appear together. A benign two-turn story raises no signals. This is a heuristic; an LLM judge over the whole session is the stronger version of the same idea.</p>"))
    O.append(outcome("Import audit",
        out_block(output(C, "IMPORT_TO_PACKAGE")),
        "<p><code>cvelookup</code> has no PyPI project, so it is likely invented and must not be installed. <code>nmap</code> exists, but as <code>python-nmap</code>; it still needs vetting. “Not installed here” is not the same as “does not exist”, and that distinction is what the audit encodes.</p>"))
    O.append(outcome("Memory triage",
        out_block(output(C, "print(triage_dump())")),
        "<p>Two independent rules point at the same process: a name one character away from <code>svchost.exe</code>, and a memory region that is writable and executable. The recommended next steps preserve evidence before anything else. With a key, the LLM explains the same findings at length; the rules are what make the verdict reproducible.</p>"))
    O.append(outcome("The kill chain",
        out_block(output(C, "KILL_CHAIN = [")),
        "<p>Every layer has an attack you measured and a defense you ran. Use this table as a coverage checklist when you threat-model a real system.</p>"))
    P.append(("outcomes", "Expected outcomes and what they mean", "".join(O)))

    P.append(("takeaways", "Key takeaways", takeaways([
        "The AI attack surface has layers (training data, model, inference channel, supply chain, host) and one intrusion can chain them.",
        "Targeted poisoning is the real threat; label-consistency checks on training data and a trusted test set are the counter.",
        "Extraction, timing and splitting all use the normal API; query budgets, constant-time responses and session-level moderation close it.",
        "Generated code is a supply-chain input: audit imports and verify packages before anyone installs them.",
        "In forensics, LLM triage explains and deterministic rules reproduce. Use both.",
    ])))
    return P
