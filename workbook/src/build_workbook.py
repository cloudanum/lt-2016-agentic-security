#!/usr/bin/env python3
"""Render the lab workbook as ONE self-contained HTML file:

    python3 workbook/src/build_workbook.py
    -> workbook/Agentic-Security-Lab-Workbook.html

No external resources: system fonts, inline CSS, inline SVG diagrams. Expected
outputs are read from the executed notebooks in code/, so re-run this after
re-executing the notebooks (for example with a live API key)."""
import importlib, os, sys

sys.path.insert(0, os.path.dirname(os.path.abspath(__file__)))
from wb import CHAPTERS, CSS, OUT, Flow, assemble, esc, figure  # noqa: E402

FILENAME = "Agentic-Security-Lab-Workbook.html"

BLURBS = {
    "ch01": "Run four detectors on real traffic, build the cognitive loop, and enforce tool schemas with an audit log.",
    "ch02": "Build a grounded RAG assistant, then extract and poison its knowledge base and defend the store.",
    "ch03": "Test a sandbox agent's guardrails and build independent layers of defense around it.",
    "ch04": "Measure attacks on training data, the model, the inference channel and the host, each paired with its fix.",
    "ch05": "Assemble an auditable Planner-Executor-Verifier pipeline with a human gate and signed audit events.",
    "ch06": "Turn frameworks into code: EU AI Act tiers, a scored checklist, a RACI, and a Zero-Trust go-live gate.",
    "ch07": "Score a program across six domains, find the highest-leverage step, and plan the next 90 days.",
}

EXTRA_CSS = r'''
.doc{max-width:1240px;margin:0 auto;padding-block:1.5rem 4rem;display:grid;grid-template-columns:minmax(0,1fr);gap:2rem}
@media (min-width:1060px){.doc{grid-template-columns:250px minmax(0,1fr)}}
.side{font-size:.88rem}
@media (min-width:1060px){.side{position:sticky;top:calc(env(safe-area-inset-top,0px) + 1rem);align-self:start;max-height:calc(100vh - 2rem);overflow:auto;padding-right:.5rem}}
@media (max-width:1059px){.side{border:1px solid var(--rule);border-radius:8px;padding:.8rem 1rem;background:var(--surface)}}
.side ol{list-style:none;margin:0;padding:0}
.side > ol{display:grid;gap:.6rem}
.side ol ol{margin:.25rem 0 0 .9rem;display:grid;gap:.2rem}
.side a{text-decoration:none;color:var(--ink-2)} .side a:hover{color:var(--accent)}
.side .lab-link{font-family:var(--f-display);font-weight:700;color:var(--ink)}
@media (max-width:1059px){.side ol ol{display:none}}
.main{min-width:0;max-width:900px}
.lab{margin-top:5rem;padding-top:2rem;border-top:6px solid var(--ink)}
.lab-head{display:flex;flex-wrap:wrap;justify-content:space-between;gap:.4rem 1rem;align-items:baseline}
.lab-head .nb{font-size:.85rem;color:var(--ink-2)}
.lab h1{margin-block:.3rem 0}
.totop{display:inline-block;margin-top:2.5rem;font-family:var(--f-display);font-weight:700;text-decoration:none}
.doc-title{font-size:clamp(2.2rem,6vw,3.6rem)}
'''


def overview(built):
    f = Flow(5, 1, cw=184, rh=110, bh=64)
    kinds = ["step", "step", "attack", "defend", "defend"]
    names = ["Understand", "Build", "Attack", "Defend", "Govern"]
    for i, (name, labs) in enumerate(zip(names, ["Lab 1", "Lab 2", "Labs 3–4", "Lab 5", "Labs 6–7"])):
        f.node(name, i, 0, name, labs, kind=kinds[i])
    for a, b in zip(names, names[1:]):
        f.edge(a, b)
    arc = figure(f, "The course arc. Every attack in Labs 3–4 has a defense built in Lab 5 and a governance control in Lab 6; Lab 7 measures the whole program.")
    cards = ""
    for slug, num, title in CHAPTERS:
        n = int(num[2:])
        if slug in built:
            cards += (f'<a class="card" href="#lab{n}"><span class="num">{n:02d}</span>'
                      f'<h3>{esc(title)}</h3><p>{esc(BLURBS[slug])}</p></a>')
        else:
            cards += (f'<div class="card" style="opacity:.6"><span class="num">{n:02d}</span>'
                      f'<h3>{esc(title)}</h3><p>Chapter in preparation.</p></div>')
    return f'''
<section id="top">
<p class="eyebrow">Course 1216 · AI and Cyber Security: Attack and Defend</p>
<h1 class="doc-title">Agentic Security Lab Workbook</h1>
<p class="lede" style="margin-top:1rem">This workbook accompanies the seven lab notebooks in <code>code/</code>. Read a chapter before you open its notebook, keep it beside you while you work, and use its outcomes section to check what you see.</p>
<p>Each chapter follows the same five steps:</p>
<ol class="steps">
<li><b>Introducing the lab</b>: what you will build and why it matters.</li>
<li><b>Key terms</b>: every term the notebook uses, defined in plain language.</li>
<li><b>How the lab is structured</b>: a flowchart of the parts and what passes between them.</li>
<li><b>The logic</b>: the mechanism of each part, with diagrams of the key decisions.</li>
<li><b>Expected outcomes</b>: the actual notebook output, what it represents, and the key takeaways.</li>
</ol>
<p>In the diagrams, red marks an attack, green a defense or control, purple data or an artifact, and amber a decision.</p>
{arc}
<div class="cards">{cards}</div>
<p style="color:var(--ink-2);font-size:.9rem">Outputs are from the most recent full run of the notebooks. Cells that call a language model are marked <em>recorded live run</em>; your wording will differ, but the behaviour should match.</p>
</section>'''


def main():
    labs, nav, built = [], [], set()
    for slug, num, title in CHAPTERS:
        try:
            mod = importlib.import_module(slug)
        except ModuleNotFoundError:
            continue
        built.add(slug)
        n = int(num[2:])
        body, toc = assemble(mod.build(), prefix=f"l{n}-")
        labs.append(f'''
<article class="lab" id="lab{n}">
  <div class="lab-head"><p class="eyebrow">Lab {n} of 7</p><span class="nb">Companion to <code>code/{num}-Lab.ipynb</code></span></div>
  <h1>{esc(title)}</h1>
  {body}
  <a class="totop" href="#top">↑ Back to the overview</a>
</article>''')
        sub = "".join(f'<li><a href="#{a}">{esc(t)}</a></li>' for a, t in toc)
        nav.append(f'<li><a class="lab-link" href="#lab{n}">Lab {n} · {esc(title)}</a><ol>{sub}</ol></li>')

    html = f'''<!doctype html>
<html lang="en">
<head>
<meta charset="utf-8">
<meta name="viewport" content="width=device-width, initial-scale=1, viewport-fit=cover">
<title>Agentic Security Lab Workbook</title>
<style>{CSS}{EXTRA_CSS}</style>
</head>
<body>
<div class="doc">
  <nav class="side" aria-label="Workbook contents"><p class="eyebrow">Contents</p>
    <ol><li><a class="lab-link" href="#top">Overview</a></li>{"".join(nav)}</ol></nav>
  <main class="main">{overview(built)}{"".join(labs)}</main>
</div>
</body>
</html>
'''
    os.makedirs(OUT, exist_ok=True)
    path = os.path.join(OUT, FILENAME)
    open(path, "w").write(html)
    print(f"wrote workbook/{FILENAME} ({len(html)/1024:.0f} KB, labs: {sorted(built)})")


if __name__ == "__main__":
    main()
