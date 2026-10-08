from wb import *

C = "Ch07"


def build():
    P = []
    P.append(("intro", "Introducing the lab", '''
<p class="lede">The capstone turns the whole course into one repeatable measurement. You score an agentic-AI program across six domains, see how the governance gate caps the result, work out which single improvement moves the needle, and leave with a 90-day roadmap for your own team.</p>
<p>The lab opens with a table of everything the course built: each attack you ran, the defense you built against it, and the governance control it evidences. It then scores a sample team, runs a what-if analysis that raises each domain one step at a time, and plans three 30-day windows. In the final part you score your own program.</p>
<p>The idea to carry forward: <strong>the weakest domain and the highest-leverage step are different questions</strong>, and the assessment is a cadence, not a grade.</p>
<ul class="facts"><li><b>Time</b> about 1 h 5 min</li><li><b>Data</b> a sample team's scores, then yours</li><li><b>Libraries</b> standard library only</li><li><b>API key</b> not used</li></ul>
'''))

    P.append(("donow", "Do it now", donow(
        7, "Score your own shop",
        "Individual",
        "Paper or course notes file; chat. No notebook, no code.",
        "<code>SCORE: inv-# data-# adv-# def-# gov-# mon-# | FIRST: &lt;domain&gt; because &lt;reason&gt;</code>",
        "Part 5 · Assess your own program — today's 0–2 quick score becomes your evidence-based 0–4 scoring in <code>MY_SCORES</code>, and your FIRST pick is tested against the what-if analysis in Part 3.",
        "Give yourself an honest baseline on six agentic-security domains before the lab formalizes the scoring, and practice the question the capstone is built around: not where the biggest gap is, but which single fix moves you most.",
        "One chat line with six 0–2 scores and one FIRST pick with a reason, plus the same line saved in your notes for Part 5.",
        [
            "Paper or your course notes file, open to a new heading <code>DN7 BASELINE</code>.",
            "A target to score: your own team or organization, or the fictional org the instructor posts in chat.",
            "The six-domain rubric (posted in chat): <b>inventory</b> (you can list every AI agent and what it can reach), <b>data controls</b> (what agents may read and send is bounded), <b>adversarial testing</b> (agents are probed before go-live), <b>layered defenses</b> (no single control failure is fatal), <b>governance</b> (an audit trail of agent actions exists), <b>monitoring</b> (agent behavior is logged and reviewed). Score each <b>0</b> = not in place, <b>1</b> = partial or ad hoc, <b>2</b> = in place and you can show the evidence.",
        ],
        [
            (1, "<b>Pick your target.</b> Your own shop if you know it well enough; otherwise the fictional org in chat. Read the six domain lines once through."),
            (2, "<b>Score all six domains</b> 0, 1, or 2, in the order given: inventory, data controls, adversarial testing, layered defenses, governance, monitoring. The honesty rule: if you cannot point to the artifact (the list, the test report, the log), score the level below."),
            (1, "<b>Pick your FIRST:</b> the single domain where one step of improvement would most improve your posture. Write one line saying why — tied to risk or evidence, not to what would be easiest."),
            (1, "<b>Post your line</b> in chat in the exact format, and copy it into your notes under <code>DN7 BASELINE</code>: <code>SCORE: inv-# data-# adv-# def-# gov-# mon-# | FIRST: &lt;domain&gt; because &lt;reason&gt;</code>."),
        ],
        "Your line is in chat with six scores and exactly one FIRST domain with a reason, and the same line is saved in your notes for Part 5.",
        [
            ("Before class", "Post the six domain lines and the 0/1/2 rubric in chat, plus a two-sentence fictional org for learners with nothing real to score, for example: <i>Acme Analytics, 200 staff, two LLM copilots in production, no one owns AI security.</i> Nothing else to stage — this runs before any notebook is opened."),
            ("Watch for", "Straight 2s justified with <i>we have a policy</i> — ask what artifact proves it. Also watch for FIRST chosen because it is the cheapest fix, and for learners who reflexively pick their lowest score: the lab's whole point (Part 3) is that the weakest domain and the highest-leverage step are different questions. Note those names."),
            ("Fallback", "No chat: draw six columns on the whiteboard (INV DATA ADV DEF GOV MON) and have learners post initials under each score, then read three FIRST picks aloud. No shared board either: collect the lines on paper and read two."),
        ],
        "<i>Evidence or it didn't happen:</i> a score you cannot back with an artifact is a wish, so score the level below.",
        "<i>Policy theater:</i> scoring 2 because a document exists that nobody follows — the same inflation the governance gate punishes in the lab.",
        [
            ("https://genai.owasp.org/", "OWASP GenAI Security Project", "OWASP"),
            ("https://www.nist.gov/itl/ai-risk-management-framework", "NIST AI Risk Management Framework", "NIST"),
            ("https://atlas.mitre.org/", "MITRE ATLAS", "MITRE"),
        ],
        """SCORE: inv-1 data-1 adv-0 def-2 gov-1 mon-1 | FIRST: adv because both copilots went live with no prompt-injection testing and every other control assumes they behave""",
        [
            "Six scores in the stated order, each 0–2, and a FIRST line naming exactly one domain with a reason tied to risk or evidence — not to convenience.",
            "Honest 0s are a strong answer: a named 0 with a gap beats an unevidenced 2 every time.",
            "The instructive wrong answer is all 2s backed by <i>we have a policy</i>: ask which artifact proves it (the inventory list, the test report, the audit log).",
            "Second instructive wrong answer: FIRST equals the lowest score by reflex. Hold that thought — Part 3's what-if analysis shows the gate (governance ≤ 1) can outrank the weakest domain.",
        ],
    )))

    P.append(("terms", "Key terms", terms([
        ("Maturity level", "0 Absent, 1 Initial, 2 Developing, 3 Managed, 4 Optimized."),
        ("Rubric", "What each level means in evidence: from <em>nothing in place</em> to <em>automated and continuously improved</em>. If you cannot show the evidence, score the level below."),
        ("Domain", "One of six areas scored 0–4: architecture, GenAI risk tooling, red-team readiness, detection and response, governance, and post-quantum readiness."),
        ("Weighted score", "The domain average with governance weighted 1.5× and the others 1×, reported as a level and a percentage."),
        ("Governance gate", "If governance scores 0 or 1 (no audit trail), the overall level is capped at Initial whatever the other domains score."),
        ("Weakest domain", "The lowest-scoring domain: where the biggest gap is."),
        ("What-if analysis", "Raising each domain by one step, one at a time, and measuring the change in level and percentage."),
        ("Highest-leverage step", "The single improvement that most improves the overall result. While the gate is closed, that is governance."),
        ("Greedy roadmap", "Each 30-day window takes the best step from the current state, assumes it lands, and re-plans; no domain twice in a row."),
    ])))

    f = Flow(7, 2, cw=150, rh=112, bh=62)
    f.node("p1", 0, 0, "Part 1", "what you built")
    f.node("p2", 1, 0, "Part 2", "score")
    f.node("p3", 2, 0, "Part 3", "what-if", kind="decision", h=80)
    f.node("p4", 3, 0, "Part 4", "90-day plan", kind="defend")
    f.node("p5", 4, 0, "Part 5", "your program", kind="defend")
    f.node("wrap", 5, 0, "Quiz +\ntakeaways", kind="terminal")
    f.node("sc", 1, 1, "Sample scores", "3·3·3·2·1·0", kind="data")
    f.node("my", 4, 1, "MY_SCORES", "your evidence", kind="data")
    for a, b in [("p1", "p2"), ("p2", "p3"), ("p3", "p4"), ("p4", "p5"), ("p5", "wrap")]:
        f.edge(a, b)
    f.edge("sc", "p2", "input").edge("my", "p5", "input")
    P.append(("structure", "How the lab is structured", LEGEND + figure(f,
        "The capstone runs the same three tools twice: first on a sample team, then on yours.") + '''
<div class="tblwrap"><table class="tbl"><thead><tr><th>Part</th><th>You do</th><th>You produce</th></tr></thead><tbody>
<tr><td>1 · What you built</td><td>Read the attack → defense → control table</td><td>The course in one view</td></tr>
<tr><td>2 · Score</td><td>Run <code>assess</code>, <code>weakest_domain</code>, <code>recommend</code> through <code>report</code></td><td>Level 1/4, 48%, gated</td></tr>
<tr><td>3 · What-if</td><td>Raise each domain one step and compare</td><td>The highest-leverage step</td></tr>
<tr><td>4 · Plan</td><td>Run <code>roadmap</code> for three 30-day windows</td><td>A plan and a projected level</td></tr>
<tr><td>5 · Your program</td><td>Score your own team against the rubric</td><td>Your report and roadmap</td></tr>
</tbody></table></div>
<h3>Hands-on exercise</h3>''' + exercises([
        ("Score your team", "Part 5", "Fill in <code>MY_SCORES</code> with an integer 0–4 per domain, backed by evidence"),
    ])))

    a = Flow(5, 2, cw=180, rh=118, bh=60)
    a.node("s", 0, 0, "Six domain scores", "0–4 each", kind="data")
    a.node("w", 1, 0, "Weighted mean", "governance × 1.5")
    a.node("r", 2, 0, "Round to level", "0–4")
    a.node("g", 3, 0, "governance\n≤ 1?", kind="decision", h=88)
    a.node("cap", 3, 1, "Cap at Initial", kind="attack")
    a.node("lvl", 4, 0, "Overall level", "+ percentage", kind="defend")
    a.edge("s", "w").edge("w", "r").edge("r", "g").edge("g", "lvl", "no").edge("g", "cap", "yes").edge("cap", "lvl", route="hv")
    asm = figure(a, "<code>assess</code>. The gate is applied after the weighted average, so strong scores elsewhere cannot buy their way past a missing audit trail.")

    w = Flow(5, 2, cw=180, rh=112, bh=60)
    w.node("s", 0, 0, "Current scores", kind="data")
    w.node("each", 1, 0, "Raise one domain\nby one step", kind="step")
    w.node("as", 2, 0, "assess()", "new level, new %")
    w.node("rank", 3, 0, "Rank", "level gain → weaker → % gain", kind="decision", h=90, w=200)
    w.node("pick", 4, 0, "Take the top step", "for this window", kind="defend")
    w.node("upd", 4, 1, "Update scores", "skip same domain next", kind="step")
    w.edge("s", "each").edge("each", "as", "×6").edge("as", "rank").edge("rank", "pick").edge("pick", "upd").edge("upd", "s", "next window", route="hv")
    road = figure(w, "<code>what_if</code> inside <code>roadmap</code>. Each window re-plans from the state the previous step left behind.")

    P.append(("logic", "The logic", f'''
<h3>Part 1 — What you built</h3>
<p><code>COURSE</code> lists, for each chapter, the attack you ran, the defense you built and the checklist control it evidences. It is the throughline of the course: every attack has a defense and a governance control.</p>
<h3>Part 2 — Score the program</h3>
{LEGEND}{asm}
{steps([
    "<code>DOMAINS</code> lists the six domains with their chapter, a next step and a certification to pursue.",
    "<code>weakest_domain</code> returns the lowest score; <code>recommend</code> turns it into a next step and a certification.",
    "<code>report</code> prints the level, the gate warning, per-domain bars and the recommendation.",
])}
<h3>Parts 3–4 — Leverage and the roadmap</h3>
{road}
<p>Ranking puts level gain first, then the weaker domain, then percentage gain. While the gate is closed, only governance can raise the level, so it ranks first. Once it opens, the weakest domain comes next.</p>
'''))

    O = []
    O.append(outcome("The course in one table",
        out_block(output(C, "COURSE = [")),
        "<p>Six chapters, six attack-defense-control triples. Every row is something you ran rather than read about.</p>"))
    O.append(outcome("The rubric",
        out_block(output(C, "RUBRIC = {")),
        "<p>The same five levels apply to every domain, so scores are comparable across domains and across quarters.</p>"))
    O.append(outcome("The sample team's assessment",
        out_block(output(C, "def report(")),
        "<p>Three domains are Managed, but governance is at 1, so the program is capped at Initial (48%). The report names post-quantum as the weakest domain. That is true, and Part 3 shows why it is not the first thing to fix.</p>"))
    O.append(outcome("What-if analysis",
        out_block(output(C, "def what_if")),
        "<p>Only governance moves the level (+1). Every other domain adds about 4 percentage points and leaves the team at Initial. The weakest domain shows the biggest gap; the gate shows what unlocks the next level.</p>"))
    O.append(outcome("The 90-day roadmap",
        out_block(output(C, "def roadmap")),
        "<p>Gate first, then the weakest domain, then governance again, for a projected 3/4 (Managed). Bring the roadmap from Part 5 to your next planning session, and re-score next quarter: the trend is the measurement.</p>"))
    P.append(("outcomes", "Expected outcomes and what they mean", "".join(O)))

    P.append(("takeaways", "Key takeaways", takeaways([
        "Every attack in this course has a defense you built and a governance control it evidences.",
        "Maturity is a weighted average of six domains; governance is weighted heaviest and acts as a gate.",
        "The weakest domain and the highest-leverage step are different questions; what-if analysis answers the second.",
        "Plan in 30-day steps and re-plan after each one. Clear the gate first.",
        "Re-run the assessment every quarter; posture is a trend, not a grade.",
    ])))
    return P
