from wb import *

C = "Ch02"


def build():
    P = []
    P.append(("intro", "Introducing the lab", '''
<p class="lede">Once you can build an agent, the first job is a defensive toolkit. This lab builds a threat-intelligence assistant that answers from your own documents, then attacks its knowledge store in both directions and defends it.</p>
<p>You build a retrieval-augmented generation (RAG) pipeline over twelve playbooks and threat-intel notes, one of them an internal incident note restricted to the IR team. The assistant cites its sources and refuses when retrieval confidence is low. Then you attack the store twice: an <strong>extraction</strong> query reads everything out, and a <strong>poisoned</strong> wiki page rewrites the answer to a ransomware question. Neither attack needs the model to misbehave, so the defenses go where the attacks happen: in retrieval and on the data paths. The lab ends by tuning a detector threshold on cost and recording the findings in a risk register.</p>
<p>The idea to carry forward: <strong>grounding and provenance are powerful and leaky at the same time</strong>. The store is an asset to protect, not just a feature.</p>
<ul class="facts"><li><b>Time</b> about 1 h 45 min</li><li><b>Data</b> 12 inline documents → 22 chunks</li><li><b>Libraries</b> numpy, scikit-learn</li><li><b>API key</b> optional (one live answer)</li></ul>
'''))

    P.append(("donow", "Do it now", donow(
        2, "Who may read this?",
        "Individual",
        "Paper or chat — no code",
        "<code>SORT: D1-P, D2-I, ... | STAR: D# because ___</code>",
        "Part 3 — the <code>DOC_ACL</code> table and the <code>APPROVED_SOURCES</code> provenance allowlist inside <code>secure_rag_query</code>",
        "Decide, before any store is built, which roles may read each document the assistant will ingest. "
        "The sort you produce here is exactly the shape of the <code>DOC_ACL</code> table you write in Part 3, "
        "and the starred call is where an access decision is hardest to make.",
        "One line with all eight documents zoned and your least-certain call starred with a reason: "
        "<code>SORT: D1-P, D2-I, ... | STAR: D# because ___</code> (P = PUBLIC, I = INTERNAL, R = IR-TEAM-ONLY).",
        [
            "The three zone definitions, least to most restricted: <b>PUBLIC</b> (anyone, including outside the organization), "
            "<b>INTERNAL</b> (any staff member), <b>IR-TEAM-ONLY</b> (the incident-response team, need-to-know).",
            "The eight document descriptions, posted in chat or on the board:<br>"
            "<b>D1</b> A vendor's public blog advisory on the Q3 finance-malware campaign. · "
            "<b>D2</b> Your SOC's ransomware playbook: isolate the host, check shadow copies, first response steps. · "
            "<b>D3</b> The incident note for IR-2026-014 — hostnames, timeline, customer impact — marked <i>INTERNAL — IR TEAM ONLY</i>. · "
            "<b>D4</b> The MITRE ATT&amp;CK page for T1490, Inhibit System Recovery. · "
            "<b>D5</b> The phishing playbook, including the lure templates your SOC reuses in awareness training. · "
            "<b>D6</b> A community threat-intel pulse from an open feed listing typosquat domains. · "
            "<b>D7</b> An HR note naming the employee whose privileged account appears in the insider-risk playbook. · "
            "<b>D8</b> A draft of next quarter's public security-awareness blog post, not yet approved by comms.",
            "Paper or a chat window. The notebook stays closed.",
        ],
        [
            (1, "<b>Read</b> the three zones and D1–D8. For each document ask one question: <i>if this leaked tomorrow, who is harmed?</i>"),
            (2, "<b>Sort</b> every document into a zone, writing your line as <code>SORT: D1-P, D2-I, ...</code> using P, I, R. No blanks and no ties — commit to one zone per document."),
            (1, "<b>Star</b> the call you are least sure about and finish the line: <code>| STAR: D# because ___</code>. One reason, in your own words."),
            (1, "<b>Check</b> your sort against the key as the instructor reveals it, and ask about your starred item."),
        ],
        "Your line is posted: all eight documents zoned, one starred with a reason.",
        [
            ("Before class", "Post the three zone definitions and the eight one-line descriptions in chat, or write them on the board, so nobody retypes them. Keep the key hidden until the reveal minute."),
            ("Watch for", "D8 in PUBLIC because it is “basically public already” — a draft is internal until comms approves it; classification follows the document's state today. And D7 in INTERNAL because it is “just an HR note” — personal data attached to an active investigation is need-to-know. If D6 is starred, check the reason: readable by anyone is not the same as trusted to ingest."),
            ("Fallback", "No board or chat: read the documents aloud one at a time and have learners hold up P, I or R fingers, then cold-call for the starred call. Collect sorts on paper and read two aloud at the reveal."),
        ],
        "<i>Classify before you index:</i> decide who may read a source before it enters the store, while the decision is still cheap.",
        "<i>Retrieve first, restrict later:</i> discovering the IR note in everyone's answers after the store has already served it.",
        [
            ("https://owasp.org/www-project-top-10-for-large-language-model-applications/", "OWASP Top 10 for LLM Applications", "OWASP — see LLM02 Sensitive Information Disclosure"),
            ("https://atlas.mitre.org/techniques/AML.T0070", "RAG Poisoning (AML.T0070)", "MITRE ATLAS"),
            ("https://csrc.nist.gov/publications/detail/fips/199/final", "FIPS 199, Security Categorization of Information and Information Systems", "NIST"),
        ],
        """SORT: D1-P, D2-I, D3-R, D4-P, D5-I, D6-P, D7-R, D8-I
STAR: D8 because it is meant to become public,
but until comms approves the draft only staff
should read it.""",
        [
            "D3 <b>and</b> D7 in IR-TEAM-ONLY: the incident note is marked, and the HR note mixes personal data with an active investigation — both are need-to-know.",
            "D8 in INTERNAL, not PUBLIC: “will be public” is not public. Classification follows the document's state today, not its destination.",
            "D6 zoned PUBLIC for read access, with the nuance noted if the learner starred it: anyone may read a community feed, but Part 3's <code>APPROVED_SOURCES</code> allowlist is what decides whether it may be <b>ingested</b>.",
            "A star with a reason, not just a star — the reason is what turns into an ACL entry or an exception request later.",
        ],
    )))

    P.append(("terms", "Key terms", terms([
        ("Retrieval-augmented generation (RAG)", "Answering from documents retrieved at query time instead of from the model's memory. Pipeline: chunk → embed → store → retrieve → augment → generate."),
        ("Chunk", "A slice of a document (here about 300 characters with 60 overlapping) that is embedded and retrieved on its own. Each chunk keeps its <code>source</code> tag."),
        ("Provenance", "Where a piece of content came from. Per-chunk source tags let answers cite sources and let defenders filter by origin."),
        ("Grounding", "Constraining an answer to retrieved evidence, and refusing when the evidence is too weak."),
        ("Top-k retrieval", "Returning the k chunks most similar to the query. With no other check, k is the only limit on what comes back."),
        ("Confabulation", "A fluent answer with no basis in evidence, often called hallucination."),
        ("Extraction attack", "A query designed to make retrieval return as much of the store as possible (OWASP LLM02, Sensitive Information Disclosure)."),
        ("Knowledge-base poisoning", "Planting text in a source the store ingests so it wins retrieval and changes answers (OWASP LLM04 and LLM08; MITRE ATLAS RAG Poisoning)."),
        ("Access control list (ACL)", "The roles allowed to read each source. Here the IR note is readable only by <code>ir-team</code>."),
        ("Provenance allowlist", "The set of sources approved at ingestion. Anything else is dropped before it can be served."),
        ("Data-loss prevention (DLP)", "Detecting and redacting sensitive values (PII, secrets) in text. Here it runs on the prompt going in and the answer going out."),
        ("F1 score", "The harmonic mean of precision and recall. It treats a miss and a false alarm as equally bad."),
        ("Cost-based threshold", "The detector threshold that minimizes misses × cost of a miss + false alarms × cost of a false alarm."),
        ("Risk register", "A list of risks scored the same way (here likelihood × impact × cost), placed on a likelihood-versus-impact matrix, each with a treatment."),
        ("NIST AI RMF", "The NIST AI Risk Management Framework: Govern wrapping Map → Measure → Manage."),
    ])))

    f = Flow(6, 2, cw=168, rh=112, bh=62)
    f.node("setup", 0, 0, "Setup", "optional key", kind="terminal")
    f.node("p1", 1, 0, "Part 1", "grounded assistant", kind="step")
    f.node("p2", 2, 0, "Part 2", "attack the store", kind="attack")
    f.node("p3", 3, 0, "Part 3", "defend the store", kind="defend")
    f.node("p4", 4, 0, "Part 4", "measure & manage", kind="step")
    f.node("wrap", 5, 0, "Quiz +\ntakeaways", kind="terminal")
    f.node("kb", 1, 1, "THREAT_KB", "12 docs · 22 chunks", kind="data")
    f.node("find", 2, 1, "Findings", "leak · poisoned answer", kind="attack")
    f.node("reg", 4, 1, "Risk register", "R1–R5", kind="data")
    for a, b in [("setup", "p1"), ("p1", "p2"), ("p2", "p3"), ("p3", "p4"), ("p4", "wrap")]:
        f.edge(a, b)
    f.edge("kb", "p1", "indexed").edge("p2", "find", "produces").edge("find", "p3", "drive", route="hv")
    f.edge("p4", "reg", "records")
    P.append(("structure", "How the lab is structured", LEGEND + figure(f,
        "The lab's flow. The knowledge base built in Part 1 is the target in Part 2; the two findings shape the controls in Part 3; Part 4 turns them into a threshold decision and register entries.") + '''
<div class="tblwrap"><table class="tbl"><thead><tr><th>Part</th><th>You do</th><th>You produce</th></tr></thead><tbody>
<tr><td>1 · Build</td><td>Chunk and embed the KB; retrieve, augment and generate; ask an in-scope and an out-of-scope question</td><td><code>kb</code>, a cited answer, a refusal</td></tr>
<tr><td>2 · Attack</td><td>Run an over-retrieving extraction probe; plant a poisoned wiki page</td><td>The IR note leaked; a harmful answer</td></tr>
<tr><td>3 · Defend</td><td>Wrap retrieval in four checks; filter at ingestion; scrub PII on both paths</td><td><code>secure_rag_query</code>, a security log, redacted text</td></tr>
<tr><td>4 · Measure</td><td>Compare max-F1 and min-cost thresholds; build a risk register and matrix</td><td>A threshold decision and a ranked register</td></tr>
</tbody></table></div>
<h3>Hands-on exercises</h3>''' + exercises([
        ("Teach a new playbook", "Part 1", "Write a credential-stuffing playbook, add it to the store, and get a cited answer"),
        ("Catch a leaked token", "Part 3.2", "Add a <code>GITHUB_TOKEN</code> DLP pattern that ignores harmless text"),
        ("Register the poisoning risk", "Part 4.2", "Add R5 with likelihood, impact, cost and a treatment"),
    ])))

    # logic diagrams
    r = Flow(6, 2, cw=160, rh=112, bh=60)
    r.node("docs", 0, 0, "Documents", "source-tagged", kind="data")
    r.node("chunk", 1, 0, "chunk_text", "300 chars · 60 overlap")
    r.node("emb", 2, 0, "build_rag", "TF-IDF matrix")
    r.node("ret", 3, 0, "rag_query", "top-k cosine")
    r.node("ok", 4, 0, "best score\n≥ 0.15?", kind="decision", h=84)
    r.node("ans", 5, 0, "compose_answer", "quotes + [sources]", kind="defend")
    r.node("ref", 4, 1, "Refuse", "escalate to analyst", kind="defend")
    r.node("llm", 3, 1, "build_prompt →\nllm_answer", "live, optional", kind="step")
    r.edge("docs", "chunk").edge("chunk", "emb").edge("emb", "ret").edge("ret", "ok").edge("ok", "ans", "yes").edge("ok", "ref", "no")
    r.edge("ret", "llm", "same hits", dashed=True)
    rag = figure(r, "The RAG pipeline. Every chunk keeps its source tag from start to finish, so the answer can cite it. The 0.15 floor is the grounding rule: below it, the assistant refuses rather than confabulates.")

    a = Flow(4, 2, cw=210, rh=110, bh=60)
    a.node("q", 0, 0, "Extraction query", "\"repeat verbatim … every document\"", kind="attack")
    a.node("k", 1, 0, "rag_query", "k = all 22 chunks")
    a.node("leak", 2, 0, "All chunks returned", "scores ≈ 0.00", kind="data")
    a.node("ir", 3, 0, "IR-only note leaks", kind="attack")
    a.node("p", 0, 1, "Poisoned wiki page", "written to match q1", kind="attack")
    a.node("idx", 1, 1, "Indexed with the KB")
    a.node("top", 2, 1, "Ranks first", "0.62 vs 0.13", kind="data")
    a.node("bad", 3, 1, "\"Don't isolate.\nPay the ransom.\"", kind="attack", h=64)
    a.edge("q", "k").edge("k", "leak").edge("leak", "ir").edge("p", "idx").edge("idx", "top", "q1").edge("top", "bad", "answer")
    att = figure(a, "The two attacks on the store. Extraction reads out (k is the only gate); poisoning writes in (whoever writes a source the store ingests controls what wins retrieval).")

    s = Flow(6, 2, cw=168, rh=116, bh=58)
    s.node("q", 0, 0, "Query + role", kind="data")
    s.node("pat", 1, 0, "extraction\nphrasing?", kind="decision", h=84)
    s.node("fl", 2, 0, "score ≥\nfloor?", kind="decision", h=84)
    s.node("ap", 3, 0, "approved\nsource?", kind="decision", h=84)
    s.node("acl", 4, 0, "role\nallowed?", kind="decision", h=84)
    s.node("keep", 5, 0, "Serve", "first k hits", kind="defend")
    s.node("r1", 1, 1, "Refuse", "log extraction-attempt", kind="defend")
    s.node("r2", 2, 1, "Skip chunk", kind="step")
    s.node("r3", 3, 1, "Drop", "log unapproved-source", kind="defend")
    s.node("r4", 4, 1, "Drop", "log acl-deny", kind="defend")
    s.edge("q", "pat").edge("pat", "fl", "no").edge("fl", "ap", "yes").edge("ap", "acl", "yes").edge("acl", "keep", "yes")
    s.edge("pat", "r1", "yes").edge("fl", "r2", "no").edge("ap", "r3", "no").edge("acl", "r4", "no")
    sec = figure(s, "<code>secure_rag_query</code>. The phrase check runs once per query; the other three run per chunk. Only the phrase check depends on the attacker's wording, which makes it the weakest of the four.")

    d = Flow(5, 1, cw=180, rh=104, bh=60)
    d.node("u", 0, 0, "User prompt", "SSN · card · email", kind="data")
    d.node("s1", 1, 0, "scrub()", "input path", kind="defend")
    d.node("m", 2, 0, "Assistant", "retrieve + answer")
    d.node("s2", 3, 0, "scrub()", "output path", kind="defend")
    d.node("c", 4, 0, "Destination", "e.g. company channel", kind="data")
    d.edge("u", "s1").edge("s1", "m", "<ENTITY> tags").edge("m", "s2").edge("s2", "c")
    dlp = figure(d, "DLP on both paths. The input scrub protects what reaches the model vendor; the output scrub is the back-stop when retrieval over-returns. Which entities to redact depends on the destination.")

    P.append(("logic", "The logic", f'''
<h3>Part 1 — Build a grounded assistant</h3>
{LEGEND}{rag}
{steps([
    "<code>chunk_text</code> slides a 300-character window with 60 characters of overlap, snapping both ends to word boundaries so no chunk starts mid-word. Each chunk gets an id such as <code>playbook-ransomware#1</code>.",
    "<code>build_rag</code> fits a TF-IDF vectorizer (unigrams and bigrams, English stop words removed) and keeps the matrix as the store. Rows are L2-normalized, so a dot product is the cosine similarity.",
    "<code>rag_query</code> scores every chunk against the question and returns the top k (default 4).",
    "<code>build_prompt</code> packs the hits, each with its <code>[source]</code>, under an instruction to answer only from the context. This is exactly what a live model would see.",
    "<code>compose_answer</code> is the deterministic generator. It keeps hits scoring at least 0.15, quotes the sentence from each that shares the most words with the question, and lists the sources. With no hit above the floor it refuses.",
    "<code>ingest_otx</code> shows how a live threat-intel feed would produce documents of the same shape. It is optional and not run.",
])}
<h3>Part 2 — Attack your own store</h3>
{att}
{steps([
    "<code>extraction_probe</code> sends an instruction-style query and asks for k = 22, the size of the store. TF-IDF finds almost no overlap, so every score is about 0.00, but top-k still returns every chunk.",
    "The poisoned page reuses the exact words of the ransomware question (<em>ransomware, file server, shadow copies, first steps</em>). After re-indexing it scores 0.62 against the question, far above the genuine playbook's 0.13.",
])}
<h3>Part 3 — Defend the store</h3>
{sec}
{steps([
    "<code>DOC_ACL</code> maps a source to the roles that may read it; sources not listed are readable by everyone.",
    "<code>APPROVED_SOURCES</code> is fixed at ingestion time from the twelve trusted documents, so the planted <code>wiki-ransomware-faq</code> is not on it.",
    "Every decision is appended to <code>SECURITY_LOG</code> with its reason, role and source.",
    "Retrieval-time filtering leaves the poison in the index, where it still skews the TF-IDF weights. Filtering at ingestion, so unapproved text never enters the index, restores the normal answer.",
])}
{dlp}
<p><code>get_scrubber</code> uses Presidio when it is installed and otherwise the regex scrubber. The regex patterns run from most to least specific (SSN and card numbers before phone numbers) so a card number is not half-matched as a phone number.</p>
<h3>Part 4 — Measure and manage risk</h3>
{steps([
    "2,000 synthetic alerts are drawn with 5% malicious; malicious scores come from Beta(5, 2), benign from Beta(2, 5), so the distributions overlap as real detector scores do.",
    "<code>best_threshold</code> scans 17 thresholds for the highest F1. <code>best_threshold_by_cost</code> scans 19 thresholds for the lowest expected cost, with a miss at $50,000 and a false alarm at $200.",
    "<code>register</code> scores each risk with <code>risk_score</code> (likelihood × impact × cost) and sorts them; <code>matrix</code> places each in a 3 × 3 likelihood-versus-impact grid with cut-offs at 0.33 / 0.66 and 3 / 7.",
])}
'''))

    O = []
    O.append(outcome("The store is built",
        out_block(output(C, "THREAT_KB = [")),
        "<p>Twelve documents become 22 overlapping chunks; the long ransomware playbook alone becomes three. Every chunk carries its source, which is what the citations and, later, the access controls rely on.</p>"))
    O.append(outcome("A grounded answer and a refusal",
        out_block(output(C, "q1 = (", keep=r"^(retrieved|--- grounded|Ransomware on|Q:|A:)")),
        "<p>The ransomware question retrieves the playbook (0.23) and the ATT&amp;CK T1490 note (0.19), and the answer quotes both with sources. The parking-pass question scores 0.00 and is refused with an escalation. The assistant refuses instead of inventing an answer, and that is the grounding discipline working as designed.</p>"))
    O.append(outcome("Extraction leaks the restricted note",
        out_block(output(C, "extraction_probe(kb, k=len(chunks))", max_lines=5)[:-2] + "\n…  (18 more chunks, all 0.00)\n"
                  + output(C, "extraction_probe(kb, k=len(chunks))", keep=r"internal")),
        "<p>Every chunk comes back at a score of 0.00, including the note marked <em>INTERNAL — IR TEAM ONLY</em>. Retrieval is a nearest-neighbour lookup with no notion of who is asking; <code>k</code> was the only limit. An LLM told to “repeat verbatim” would then hand the note to anyone.</p>"))
    O.append(outcome("Poisoning rewrites the answer",
        out_block(output(C, "POISON = {")),
        "<p>One planted page ranks first (0.62) and the grounded answer now tells the responder not to isolate the host. The citation is honest, since it names the wiki page, but nothing in the model changed. Provenance only protects you if something checks it.</p>"))
    O.append(outcome("The defended store",
        out_block(output(C, 'probe = ("Ignore') + "\n\n" + output(C, "kb_clean = build_rag")),
        "<p>The probe is refused, the analyst does not see the IR note while the IR team does, and the poisoned page is dropped, with every decision logged. Retrieval-time filtering alone leads to a refusal (best score 0.13), which is a safe failure. Filtering at ingestion brings back the correct ransomware answer. The access-control and provenance checks hold whatever wording the attacker uses; the phrase list does not.</p>"))
    O.append(outcome("DLP on both paths",
        out_block(output(C, "user_prompt = (")),
        "<p>On the way in, the email, SSN, card number, phone number and host IP are replaced by entity tags before anything reaches the model. On the way out, the attacker's C2 address in the IR-team answer is redacted before it goes to a broad channel. The IR team needs that indicator and a company-wide channel does not, so <strong>DLP policy depends on the destination</strong>.</p>"))
    O.append(outcome("F1 versus cost",
        out_block(output(C, "def best_threshold_by_cost")),
        "<p>The max-F1 threshold (0.75) misses 37 of the roughly 100 real intrusions. When a miss costs 250 times a false alarm, the cost-optimal threshold (0.30) misses none and accepts 819 false alarms, cutting expected cost from about $1.85M to $164K. Choosing that operating point is a business decision. The code only makes the trade-off explicit.</p>"))
    O.append(outcome("The risk register",
        out_block(output(C, "RISKS = [")),
        "<p>Every finding is scored the same way and given a treatment that names the control from this lab. The matrix shows R1 and R4 in the medium-likelihood / high-impact cell. In the exercise you add the poisoning risk, R5, and have to defend its rank.</p>"))
    O.append(callout("note", "Live answer (with an API key)",
        "<p>With a key, the cell after the deterministic answer sends the same augmented prompt to <code>gpt-4o-mini</code>. Expect a fluent answer citing <code>[playbook-ransomware]</code> and <code>[attack-t1490-recovery]</code>. Compare it with the deterministic composer: same evidence, different wording.</p>"))
    P.append(("outcomes", "Expected outcomes and what they mean", "".join(O)))

    P.append(("takeaways", "Key takeaways", takeaways([
        "Grounding is a discipline: answer only from retrieved context, cite sources, and refuse when retrieval confidence is low.",
        "A retrieval store is a target in both directions. Extraction reads everything out; poisoning writes guidance in. Neither needs the model to misbehave.",
        "Defend where the attack happens: access-scoped, provenance-checked retrieval, and filtering at ingestion. Prefer controls that do not depend on the attacker's wording.",
        "DLP belongs on both the input and output paths, and the right policy depends on where the output goes.",
        "Thresholds and risk rankings are business decisions; make the costs explicit and record them in a register.",
    ])))
    return P
