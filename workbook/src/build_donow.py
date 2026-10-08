#!/usr/bin/env python3
"""Render the seven "Do it now" openers as ONE standalone HTML file:

    python3 workbook/src/build_donow.py
    -> workbook/DoItNow.html

Same theme as the lab workbook (CSS from wb.py); content lives in donows.py."""
import os, sys

sys.path.insert(0, os.path.dirname(os.path.abspath(__file__)))
from wb import CHAPTERS, CSS, OUT, esc  # noqa: E402
from donows import DONOWS  # noqa: E402

FILENAME = "DoItNow.html"

EXTRA_CSS = r'''
.doc{max-width:1240px;margin:0 auto;padding-block:1.5rem 4rem;display:grid;grid-template-columns:minmax(0,1fr);gap:2rem}
@media (min-width:1060px){.doc{grid-template-columns:250px minmax(0,1fr)}}
.side{font-size:.88rem}
@media (min-width:1060px){.side{position:sticky;top:calc(env(safe-area-inset-top,0px) + 1rem);align-self:start;max-height:calc(100vh - 2rem);overflow:auto;padding-right:.5rem}}
@media (max-width:1059px){.side{border:1px solid var(--rule);border-radius:8px;padding:.8rem 1rem;background:var(--surface)}}
.side ol{list-style:none;margin:0;padding:0;display:grid;gap:.4rem}
.side a{text-decoration:none;color:var(--ink-2)} .side a:hover{color:var(--accent)}
.side .dn-link{font-family:var(--f-display);font-weight:700;color:var(--ink)}
.main{min-width:0;max-width:900px}
.doc-title{font-size:clamp(2.2rem,6vw,3.6rem)}
.dn-sec{margin-top:3rem}
.dn-sec:first-of-type{margin-top:1.5rem}
.dn-sec .labtag{font-size:.85rem;color:var(--ink-2)}
'''


def main():
    nav, cards = [], []
    for (slug, num, title), card in zip(CHAPTERS, DONOWS):
        n = int(num[2:])
        nav.append(f'<li><a class="dn-link" href="#dn{n}">DN {n} · {esc(title)}</a></li>')
        cards.append(f'''
<section class="dn-sec" id="dn{n}">
  <p class="labtag">Pairs with Lab {n} of 7 · <code>code/{num}-Lab.ipynb</code></p>
  {card}
</section>''')

    html = f'''<!doctype html>
<html lang="en">
<head>
<meta charset="utf-8">
<meta name="viewport" content="width=device-width, initial-scale=1, viewport-fit=cover">
<title>Do It Now · Agentic Security</title>
<style>{CSS}{EXTRA_CSS}</style>
</head>
<body>
<div class="doc">
  <nav class="side" aria-label="Do it now contents"><p class="eyebrow">Contents</p>
    <ol><li><a class="dn-link" href="#top">Overview</a></li>{"".join(nav)}</ol></nav>
  <main class="main">
<section id="top">
<p class="eyebrow">Course 1216 · AI and Cyber Security: Attack and Defend</p>
<h1 class="doc-title">Do It Now</h1>
<p class="lede" style="margin-top:1rem">Seven five-minute openers, one per lab, built for an online room. Run each at the start of its chapter, before anyone opens the notebook: a Mural board and the Zoom chat are all you need.</p>
<p>Every card has the same anatomy: a facts table with time, grouping, tools, and the exact capture format; a goal and a deliverable; timed steps that add to five minutes; a capture line with a "done when" check; an "In the news" box with a real incident on the same theme; a pattern and anti-pattern line; bulleted further reading; and a collapsible answer key with a sample answer and look-for points. The capture line each card produces is picked up again inside its lab.</p>
<ol class="steps">
<li><b>Before class</b>: build the Mural board the card's "You need" list calls for (one frame per zone or tier, sticky notes for the items to sort), and drop the board link in the Zoom chat as learners join.</li>
<li><b>In class</b>: run the steps as written; the timings add to five minutes. If Mural fails, paste the items as a numbered list in the Zoom chat and have learners reply with their sort line.</li>
<li><b>During the lab</b>: return to the capture line where the card's "Feeds" entry says it lands.</li>
<li><b>When debriefing</b>: open the card's answer key, and point learners to the news story and the further reading.</li>
</ol>
</section>
{"".join(cards)}
  </main>
</div>
</body>
</html>
'''
    path = os.path.join(OUT, FILENAME)
    open(path, "w").write(html)
    print(f"wrote workbook/{FILENAME} ({len(html)/1024:.0f} KB, {len(cards)} activities)")


if __name__ == "__main__":
    main()
