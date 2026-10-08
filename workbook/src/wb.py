"""Shared template, SVG flowchart helper, and notebook-output extraction for the
lab workbook. Content lives in chNN.py; run build_workbook.py to render."""
import html, json, os, re

ROOT = os.path.dirname(os.path.dirname(os.path.dirname(os.path.abspath(__file__))))
CODE = os.path.join(ROOT, "code")
OUT = os.path.join(ROOT, "workbook")

esc = html.escape

# ------------------------------------------------------------------ outputs

_nb_cache = {}

def _nb(chap):
    if chap not in _nb_cache:
        _nb_cache[chap] = json.load(open(os.path.join(CODE, f"{chap}-Lab.ipynb")))
    return _nb_cache[chap]

def output(chap, marker, keep=None, drop=None, max_lines=40):
    """Text output of the first code cell whose source contains `marker`.
    keep/drop: optional regexes to filter lines."""
    for c in _nb(chap)["cells"]:
        if c["cell_type"] == "code" and marker in "".join(c["source"]):
            t = ""
            for o in c.get("outputs", []):
                if o["output_type"] == "stream":
                    t += "".join(o["text"])
                elif o["output_type"] in ("execute_result", "display_data"):
                    t += "".join(o["data"].get("text/plain", ""))
            lines = t.rstrip().splitlines()
            if keep:
                lines = [l for l in lines if re.search(keep, l)]
            if drop:
                lines = [l for l in lines if not re.search(drop, l)]
            if len(lines) > max_lines:
                lines = lines[:max_lines] + ["…"]
            if not lines:
                raise ValueError(f"{chap}: cell with {marker!r} has no output")
            return "\n".join(lines)
    raise KeyError(f"{chap}: no code cell contains {marker!r}")


# ------------------------------------------------------------------ SVG flowcharts

class Flow:
    """Grid-placed flowchart. Nodes are placed by (col, row) in grid units;
    edges are straight or elbowed, clipped to node borders, optionally labelled.
    Colours come from page CSS classes, so diagrams follow the theme."""

    def __init__(self, cols, rows, cw=180, rh=96, pad=20, bw=None, bh=54):
        self.cw, self.rh, self.pad = cw, rh, pad
        self.bw, self.bh = bw or cw - 64, bh
        self.W = pad * 2 + cols * cw
        self.H = pad * 2 + rows * rh
        self.nodes, self.edges, self.extras = {}, [], []

    def node(self, id, col, row, label, sub=None, kind="step", w=None, h=None):
        w = w or self.bw
        h = h or self.bh
        need = max([7.4 * len(l) for l in label.split("\n")] + [6.6 * len(sub or "")]) + 22
        if kind == "decision":
            need *= 1.45
        w = max(w, need)
        self.nodes[id] = dict(col=col, row=row, w=w, h=h, label=label, sub=sub, kind=kind)
        return self

    def _layout(self):
        """Column width grows so the widest box still leaves room for edge labels."""
        cols = max(n["col"] for n in self.nodes.values()) + 1
        colw = [max([n["w"] for n in self.nodes.values() if n["col"] == c] or [self.cw - 72]) + 72
                for c in range(cols)]
        left = [self.pad + sum(colw[:c]) for c in range(cols)]
        self.W = self.pad * 2 + sum(colw)
        for n in self.nodes.values():
            n["cx"] = left[n["col"]] + colw[n["col"]] / 2
            n["cy"] = self.pad + n["row"] * self.rh + self.rh / 2

    def edge(self, a, b, label=None, route="straight", dashed=False, lpos=0.5):
        self.edges.append((a, b, label, route, dashed, lpos))
        return self

    def note(self, x, y, text, anchor="middle"):
        self.extras.append(f'<text x="{x:.0f}" y="{y:.0f}" class="d-note" text-anchor="{anchor}">{esc(text)}</text>')
        return self

    def band(self, row0, row1, label):
        """A labelled background band spanning rows row0..row1 (inclusive)."""
        y = self.pad + row0 * self.rh + 4
        h = (row1 - row0 + 1) * self.rh - 8
        self.extras.insert(0, f'<rect x="4" y="{y:.0f}" width="{self.W-8}" height="{h:.0f}" rx="10" class="d-band"/>'
                              f'<text x="14" y="{y+16:.0f}" class="d-bandlabel">{esc(label)}</text>')
        return self

    @staticmethod
    def _clip(n, px, py):
        """Point where the segment centre->(px,py) leaves node n's box."""
        dx, dy = px - n["cx"], py - n["cy"]
        if dx == 0 and dy == 0:
            return n["cx"], n["cy"]
        hw, hh = n["w"] / 2 + 3, n["h"] / 2 + 3
        if n["kind"] == "decision":
            t = 1 / (abs(dx) / hw + abs(dy) / hh)
        else:
            t = min(hw / abs(dx) if dx else 1e9, hh / abs(dy) if dy else 1e9)
        return n["cx"] + dx * t, n["cy"] + dy * t

    def _edge_svg(self, a, b, label, route, dashed, lpos):
        A, B = self.nodes[a], self.nodes[b]
        if route == "straight":
            pts = [self._clip(A, B["cx"], B["cy"]), self._clip(B, A["cx"], A["cy"])]
        else:  # "hv": horizontal first, then vertical; "vh": vertical first
            corner = (B["cx"], A["cy"]) if route == "hv" else (A["cx"], B["cy"])
            pts = [self._clip(A, *corner), corner, self._clip(B, *corner)]
        d = " ".join(f"{x:.1f},{y:.1f}" for x, y in pts)
        cls = "d-edge d-dash" if dashed else "d-edge"
        s = f'<polyline points="{d}" class="{cls}" marker-end="url(#{self.mid})"/>'
        if label:
            # label on the longest segment
            segs = list(zip(pts, pts[1:]))
            (x1, y1), (x2, y2) = max(segs, key=lambda s: abs(s[0][0]-s[1][0]) + abs(s[0][1]-s[1][1]))
            lx, ly = x1 + (x2 - x1) * lpos, y1 + (y2 - y1) * lpos
            tw = 6.4 * len(label) + 10
            s += (f'<rect x="{lx-tw/2:.0f}" y="{ly-9:.0f}" width="{tw:.0f}" height="18" rx="4" class="d-lblbg"/>'
                  f'<text x="{lx:.0f}" y="{ly+4:.0f}" class="d-lbl" text-anchor="middle">{esc(label)}</text>')
        return s

    def _node_svg(self, n):
        x, y, w, h = n["cx"] - n["w"] / 2, n["cy"] - n["h"] / 2, n["w"], n["h"]
        k = n["kind"]
        if k == "decision":
            cx, cy = n["cx"], n["cy"]
            shape = (f'<polygon points="{cx},{y} {x+w},{cy} {cx},{y+h} {x},{cy}" class="d-node k-decision"/>')
        else:
            rx = 26 if k == "terminal" else 8
            shape = f'<rect x="{x:.0f}" y="{y:.0f}" width="{w:.0f}" height="{h:.0f}" rx="{min(rx, h/2):.0f}" class="d-node k-{k}"/>'
        lines = n["label"].split("\n")
        total = len(lines) + (1 if n["sub"] else 0)
        y0 = n["cy"] - (total - 1) * 8 + 4
        t = "".join(f'<text x="{n["cx"]:.0f}" y="{y0 + i*16:.0f}" class="d-t k-{k}-t" text-anchor="middle">{esc(l)}</text>'
                    for i, l in enumerate(lines))
        if n["sub"]:
            t += f'<text x="{n["cx"]:.0f}" y="{y0 + len(lines)*16:.0f}" class="d-sub k-{k}-t" text-anchor="middle">{esc(n["sub"])}</text>'
        return shape + t

    _count = 0

    def svg(self, aria):
        Flow._count += 1
        self.mid = f"ah{Flow._count}"
        self._layout()
        body = "".join(self.extras)
        body += "".join(self._edge_svg(*e) for e in self.edges)
        body += "".join(self._node_svg(n) for n in self.nodes.values())
        return (f'<svg viewBox="0 0 {self.W:.0f} {self.H:.0f}" role="img" aria-label="{esc(aria)}" '
                f'style="min-width:{min(self.W, 860):.0f}px">'
                f'<defs><marker id="{self.mid}" viewBox="0 0 10 10" refX="9" refY="5" markerWidth="7" markerHeight="7" '
                'orient="auto-start-reverse"><path d="M0,0 L10,5 L0,10 z" fill="currentColor"/></marker></defs>'
                f'{body}</svg>')


def figure(flow, caption, aria=None):
    return (f'<figure class="diagram"><div class="scroll">{flow.svg(aria or caption)}</div>'
            f'<figcaption>{caption}</figcaption></figure>')

LEGEND = ('<div class="legend" aria-hidden="true">'
          '<span><i class="sw k-step"></i>step</span><span><i class="sw k-attack"></i>attack</span>'
          '<span><i class="sw k-defend"></i>defense / control</span><span><i class="sw k-data"></i>data or artifact</span>'
          '<span><i class="sw k-decision"></i>decision</span></div>')


# ------------------------------------------------------------------ page parts

def terms(items):
    rows = "".join(f'<div class="term"><dt>{t}</dt><dd>{d}</dd></div>' for t, d in items)
    return f'<dl class="glossary">{rows}</dl>'

def out_block(text, label="Notebook output", live=False):
    tag = '<span class="tag live">recorded live run · wording varies</span>' if live else ""
    return (f'<div class="output"><div class="out-head"><span>{label}</span>{tag}</div>'
            f'<pre><code>{esc(text)}</code></pre></div>')

def code_block(text, label="Code"):
    return (f'<div class="codeblk"><div class="out-head"><span>{label}</span></div>'
            f'<pre><code>{esc(text.strip())}</code></pre></div>')

def steps(items):
    return '<ol class="steps">' + "".join(f"<li>{i}</li>" for i in items) + "</ol>"

def callout(kind, title, body):
    return f'<aside class="callout c-{kind}"><p class="c-title">{title}</p>{body}</aside>'

def outcome(title, output_html, meaning):
    return (f'<section class="outcome"><h4>{title}</h4>{output_html}'
            f'<div class="meaning"><p class="eyebrow">What it represents</p>{meaning}</div></section>')


CHAPTERS = [
    ("ch01", "Ch01", "AI Architecture & Agentic Foundations"),
    ("ch02", "Ch02", "Generative AI for SecOps & Risk Management"),
    ("ch03", "Ch03", "Hacking AI Agents: Adversarial Techniques"),
    ("ch04", "Ch04", "Exploiting the AI Attack Surface"),
    ("ch05", "Ch05", "Defending with Agents: Autonomous SecOps"),
    ("ch06", "Ch06", "AI Governance & Zero Trust for Agents"),
    ("ch07", "Ch07", "Secure-Agent Maturity: Course Capstone"),
]


def page(slug, num, title, sections, toc):
    i = [c[0] for c in CHAPTERS].index(slug)
    prev = CHAPTERS[i - 1] if i > 0 else None
    nxt = CHAPTERS[i + 1] if i < len(CHAPTERS) - 1 else None
    nav = '<nav class="pager">'
    nav += (f'<a href="{prev[0]}.html">← Lab {prev[1][2:]}: {esc(prev[2])}</a>' if prev else '<a href="index.html">← Workbook home</a>')
    nav += (f'<a href="{nxt[0]}.html">Lab {nxt[1][2:]}: {esc(nxt[2])} →</a>' if nxt else '<a href="index.html">Workbook home →</a>')
    nav += "</nav>"
    toc_html = "".join(f'<li><a href="#{a}">{esc(t)}</a></li>' for a, t in toc)
    body = f'''
<header class="top">
  <a class="home" href="index.html">Agentic Security · Lab Workbook</a>
  <span class="nb">Companion to <code>code/{num}-Lab.ipynb</code></span>
</header>
<main class="wrap">
  <div class="hero">
    <p class="eyebrow">Lab {int(num[2:])} of 7</p>
    <h1>{esc(title)}</h1>
  </div>
  <div class="layout">
    <nav class="toc" aria-label="On this page"><p class="eyebrow">On this page</p><ol>{toc_html}</ol></nav>
    <article class="content">{sections}</article>
  </div>
  {nav}
</main>'''
    return shell(f"Lab {int(num[2:])} Workbook · {title}", body)


def shell(title, body):
    return f'''<!doctype html>
<html lang="en">
<head>
<meta charset="utf-8">
<meta name="viewport" content="width=device-width, initial-scale=1, viewport-fit=cover">
<title>{esc(title)}</title>
<style>{CSS}</style>
</head>
<body>{body}
</body>
</html>
'''


CSS = r'''
/* Layout: a lab-manual page: narrow reading column, sticky contents rail on wide screens,
   wide figures and output blocks that scroll inside their own frames. */
:root{
  --bg:#f5f7f8; --surface:#ffffff; --ink:#14212b; --ink-2:#4a5b67; --rule:#d6dee3;
  --accent:#0b6c86; --accent-soft:#e0eff3;
  --attack:#b42318; --attack-bg:#fbe9e7; --defend:#11724a; --defend-bg:#e3f4ea;
  --data:#6b4fa8; --data-bg:#eee9f8; --decide:#8a5a00; --decide-bg:#fbf1dc;
  --code-bg:#eef2f4; --live:#8a5a00;
  --f-display:"Avenir Next Condensed", "Helvetica Neue", "Arial Narrow", "Roboto Condensed", system-ui, sans-serif;
  --f-body:system-ui, -apple-system, "Segoe UI", Roboto, "Helvetica Neue", Arial, sans-serif;
  --f-mono:ui-monospace, "SF Mono", Menlo, Consolas, "Liberation Mono", monospace;
  color-scheme:light;
}
@media (prefers-color-scheme: dark){:root:not([data-theme="light"]){
  --bg:#0e1519; --surface:#152027; --ink:#e3eaee; --ink-2:#9db0bc; --rule:#2a3a44;
  --accent:#5ec1dc; --accent-soft:#16323b;
  --attack:#ff8a7a; --attack-bg:#3a1d1a; --defend:#5fd39c; --defend-bg:#15322a;
  --data:#b9a2f0; --data-bg:#2a2340; --decide:#f0c060; --decide-bg:#3a2e14;
  --code-bg:#111b21; --live:#f0c060; color-scheme:dark}}
:root[data-theme="dark"]{
  --bg:#0e1519; --surface:#152027; --ink:#e3eaee; --ink-2:#9db0bc; --rule:#2a3a44;
  --accent:#5ec1dc; --accent-soft:#16323b;
  --attack:#ff8a7a; --attack-bg:#3a1d1a; --defend:#5fd39c; --defend-bg:#15322a;
  --data:#b9a2f0; --data-bg:#2a2340; --decide:#f0c060; --decide-bg:#3a2e14;
  --code-bg:#111b21; --live:#f0c060; color-scheme:dark}
*{box-sizing:border-box}
html{-webkit-text-size-adjust:100%}
body{margin:0;background:var(--bg);color:var(--ink);font:17px/1.6 var(--f-body);padding-inline:16px}
a{color:var(--accent)} a:focus-visible{outline:2px solid var(--accent);outline-offset:2px;border-radius:3px}
code{font-family:var(--f-mono);font-size:.86em;background:var(--code-bg);padding:.08em .32em;border-radius:4px}
h1,h2,h3,h4{font-family:var(--f-display);text-wrap:balance;line-height:1.15;margin:0}
h1{font-size:clamp(2rem,5vw,3.1rem);font-weight:800;font-stretch:80%;letter-spacing:-.01em}
h2{font-size:1.75rem;font-weight:750;font-stretch:85%;margin-block:3rem 1rem;padding-top:1rem;border-top:2px solid var(--ink)}
h3{font-size:1.25rem;font-weight:700;margin-block:2rem .6rem}
h4{font-size:1.05rem;font-weight:700;margin-block:0 .6rem}
p{margin-block:0 1rem}
.eyebrow{font-family:var(--f-display);font-size:.78rem;font-weight:700;letter-spacing:.09em;text-transform:uppercase;color:var(--ink-2);margin:0 0 .35rem}
.top{max-width:1180px;margin:0 auto;display:flex;flex-wrap:wrap;gap:.4rem 1.2rem;justify-content:space-between;align-items:baseline;padding-block:1rem;border-bottom:1px solid var(--rule)}
.top .home{font-family:var(--f-display);font-weight:700;text-decoration:none;color:var(--ink)}
.top .nb{font-size:.85rem;color:var(--ink-2)}
.wrap{max-width:1180px;margin:0 auto;padding-block:1.5rem 4rem}
.hero{padding-block:1.5rem 1rem}
.layout{display:grid;grid-template-columns:minmax(0,1fr);gap:2rem}
@media (min-width:1000px){.layout{grid-template-columns:220px minmax(0,1fr)}}
.toc{font-size:.9rem}
.toc ol{list-style:none;margin:0;padding:0;display:grid;gap:.35rem}
.toc a{text-decoration:none;color:var(--ink-2)} .toc a:hover{color:var(--accent)}
@media (min-width:1000px){.toc{position:sticky;top:calc(env(safe-area-inset-top,0px) + 1rem);align-self:start}}
@media (max-width:999px){.toc{border:1px solid var(--rule);border-radius:8px;padding:.8rem 1rem;background:var(--surface)}.toc ol{grid-template-columns:repeat(auto-fill,minmax(180px,1fr))}}
.content{min-width:0;max-width:880px}
.content > p, .content li{max-width:68ch}
.lede{font-size:1.15rem;color:var(--ink)}
.facts{display:flex;flex-wrap:wrap;gap:.5rem 1.6rem;margin:1rem 0 0;padding:0;list-style:none;font-size:.92rem;color:var(--ink-2)}
.facts b{color:var(--ink);font-weight:700}
.glossary{display:grid;grid-template-columns:repeat(auto-fit,minmax(min(100%,330px),1fr));gap:.1rem 1.6rem;margin:0}
.term{padding-block:.7rem;border-top:1px solid var(--rule)}
.term dt{font-family:var(--f-display);font-weight:700;font-size:1rem}
.term dd{margin:.15rem 0 0;color:var(--ink-2);font-size:.95rem;line-height:1.5}
.diagram{margin:1.4rem 0 1.8rem}
.diagram .scroll{overflow-x:auto;background:var(--surface);border:1px solid var(--rule);border-radius:10px;padding:10px}
.diagram svg{display:block;width:100%;height:auto;color:var(--ink-2)}
figcaption{font-size:.9rem;color:var(--ink-2);margin-top:.5rem;max-width:68ch}
.d-node{stroke-width:1.5}
.k-step{fill:var(--surface);stroke:var(--ink-2)} .k-step-t{fill:var(--ink)}
.k-terminal{fill:var(--accent-soft);stroke:var(--accent)} .k-terminal-t{fill:var(--ink)}
.k-attack{fill:var(--attack-bg);stroke:var(--attack)} .k-attack-t{fill:var(--ink)}
.k-defend{fill:var(--defend-bg);stroke:var(--defend)} .k-defend-t{fill:var(--ink)}
.k-data{fill:var(--data-bg);stroke:var(--data)} .k-data-t{fill:var(--ink)}
.k-decision{fill:var(--decide-bg);stroke:var(--decide)} .k-decision-t{fill:var(--ink)}
.d-t{font:600 13px var(--f-body)} .d-sub{font:12px var(--f-body);opacity:.8}
.d-edge{fill:none;stroke:currentColor;stroke-width:1.6} .d-dash{stroke-dasharray:5 4}
.d-lblbg{fill:var(--surface)} .d-lbl{font:11.5px var(--f-mono);fill:var(--ink-2)}
.d-note{font:italic 12px var(--f-body);fill:var(--ink-2)}
.d-band{fill:var(--bg);stroke:var(--rule)} .d-bandlabel{font:700 11px var(--f-display);letter-spacing:.08em;text-transform:uppercase;fill:var(--ink-2)}
.legend{display:flex;flex-wrap:wrap;gap:.4rem 1.1rem;font-size:.82rem;color:var(--ink-2);margin:-.6rem 0 1.4rem}
.legend span{display:inline-flex;align-items:center;gap:.4rem}
.sw{display:inline-block;width:14px;height:14px;border-radius:3px;border:1.5px solid}
.sw.k-step{background:var(--surface);border-color:var(--ink-2)} .sw.k-attack{background:var(--attack-bg);border-color:var(--attack)}
.sw.k-defend{background:var(--defend-bg);border-color:var(--defend)} .sw.k-data{background:var(--data-bg);border-color:var(--data)}
.sw.k-decision{background:var(--decide-bg);border-color:var(--decide);transform:rotate(45deg) scale(.8)}
.steps{padding-left:1.3rem;display:grid;gap:.45rem;margin:0 0 1.2rem}
.steps li::marker{font-family:var(--f-display);font-weight:700;color:var(--accent)}
.output,.codeblk{margin:1rem 0;border:1px solid var(--rule);border-radius:8px;overflow:hidden;background:var(--code-bg)}
.out-head{display:flex;flex-wrap:wrap;gap:.5rem;justify-content:space-between;align-items:center;font:700 .72rem var(--f-display);letter-spacing:.08em;text-transform:uppercase;color:var(--ink-2);padding:.45rem .8rem;border-bottom:1px solid var(--rule);background:var(--surface)}
.output pre,.codeblk pre{margin:0;padding:.8rem .9rem;overflow-x:auto;font:13px/1.5 var(--f-mono);font-variant-numeric:tabular-nums}
.output pre code,.codeblk pre code{background:none;padding:0;font-size:inherit}
.tag{font-weight:700;letter-spacing:.04em;text-transform:none;font-size:.78rem;padding:.1rem .45rem;border-radius:99px;border:1px solid}
.tag.live{color:var(--live);border-color:var(--live)}
.outcome{margin:1.6rem 0 2.2rem}
.meaning{border-left:3px solid var(--accent);padding:.2rem 0 .2rem 1rem}
.meaning p:last-child{margin-bottom:0}
.callout{margin:1.2rem 0;padding:.9rem 1.1rem;border-radius:8px;border:1px solid var(--rule);background:var(--surface)}
.callout .c-title{font-family:var(--f-display);font-weight:700;margin-bottom:.3rem}
.callout p:last-child{margin-bottom:0}
.c-attack{border-color:var(--attack)} .c-attack .c-title{color:var(--attack)}
.c-defend{border-color:var(--defend)} .c-defend .c-title{color:var(--defend)}
.c-note .c-title{color:var(--accent)}
.takeaways{list-style:none;padding:0;margin:0;display:grid;gap:.7rem;counter-reset:t}
.takeaways li{counter-increment:t;display:grid;grid-template-columns:2.2rem minmax(0,1fr);gap:.5rem;padding-block:.6rem;border-top:1px solid var(--rule)}
.takeaways li::before{content:counter(t);font:800 1.5rem/1 var(--f-display);color:var(--accent)}
table.tbl{border-collapse:collapse;width:100%;font-size:.92rem}
.tblwrap{overflow-x:auto;margin:1rem 0}
.tbl th,.tbl td{text-align:left;padding:.5rem .7rem;border-bottom:1px solid var(--rule);vertical-align:top}
.tbl th{font-family:var(--f-display);font-size:.8rem;letter-spacing:.06em;text-transform:uppercase;color:var(--ink-2)}
.pager{display:flex;flex-wrap:wrap;justify-content:space-between;gap:1rem;margin-top:4rem;padding-top:1.2rem;border-top:2px solid var(--ink);font-family:var(--f-display);font-weight:700}
.pager a{text-decoration:none}
.cards{display:grid;grid-template-columns:repeat(auto-fill,minmax(min(100%,300px),1fr));gap:1rem;margin:1.5rem 0}
.card{display:flex;flex-direction:column;gap:.4rem;padding:1.1rem 1.2rem;border:1px solid var(--rule);border-radius:10px;background:var(--surface);text-decoration:none;color:var(--ink)}
.card:hover{border-color:var(--accent)}
.card .num{font:800 2rem/1 var(--f-display);color:var(--accent)}
.card h3{margin:0;font-size:1.15rem}
.card p{margin:0;color:var(--ink-2);font-size:.93rem}
.dn-card{border:1px solid var(--rule);border-left:5px solid var(--accent);border-radius:10px;background:var(--surface);padding:1.1rem 1.2rem;margin:1.2rem 0}
.dn-card h3{margin-block:.2rem .6rem}
.dn-card h4{margin-block:1.1rem .4rem}
.dn-badge{display:inline-block;background:var(--accent);color:var(--bg);font:800 .9rem/1 var(--f-display);border-radius:5px;padding:.3rem .5rem;margin-right:.35rem}
.dn-facts{border-collapse:collapse;width:100%;font-size:.9rem;margin:.4rem 0 1rem}
.dn-facts th,.dn-facts td{text-align:left;padding:.35rem .6rem;border-bottom:1px solid var(--rule);vertical-align:top}
.dn-facts th{font-family:var(--f-display);font-size:.75rem;letter-spacing:.06em;text-transform:uppercase;color:var(--ink-2);white-space:nowrap}
.dn-need{margin:0 0 .4rem;padding-left:1.3rem;display:grid;gap:.3rem}
.dn-steps .t{width:3rem;text-align:center;font-variant-numeric:tabular-nums;color:var(--ink-2)}
.dn-done{border:1px solid var(--defend);background:var(--defend-bg);border-radius:8px;padding:.7rem .95rem;margin:1rem 0}
.dn-done p{margin:0 0 .4rem} .dn-done p:last-child{margin-bottom:0}
.dn-info{border:1px solid var(--accent);background:var(--accent-soft);border-radius:8px;padding:.7rem .95rem;margin:1rem 0}
.dn-info-title{font-family:var(--f-display);font-weight:700;font-size:.78rem;letter-spacing:.09em;text-transform:uppercase;color:var(--accent);margin:0 0 .35rem}
.dn-info p{margin:0 0 .4rem} .dn-info p:last-child{margin-bottom:0}
.dn-pattern{font-size:.9rem;color:var(--ink-2)}
.dn-reading{font-size:.9rem;color:var(--ink-2);margin:.6rem 0}
.dn-reading-title{font-family:var(--f-display);font-weight:700;font-size:.8rem;letter-spacing:.08em;text-transform:uppercase;margin:0 0 .25rem}
.dn-reading ul{margin:0;padding-left:1.2rem;display:grid;gap:.2rem}
details.dn-answer{border-top:1px solid var(--rule);margin-top:.8rem;padding-top:.5rem}
details.dn-answer summary{cursor:pointer;font-family:var(--f-display);font-weight:700;color:var(--accent)}
details.dn-answer pre{background:var(--code-bg);border:1px solid var(--rule);border-radius:8px;padding:.7rem .85rem;overflow-x:auto;white-space:pre-wrap;font:13px/1.5 var(--f-mono);margin:.5rem 0}
details.dn-answer ul{margin:.2rem 0 .6rem;padding-left:1.3rem;display:grid;gap:.25rem;font-size:.93rem}
@media print{.toc,.pager,.top .nb{display:none}.layout{display:block}body{background:#fff}}
@media (prefers-reduced-motion:reduce){*{scroll-behavior:auto!important}}
html{scroll-behavior:smooth}
'''


def assemble(parts, prefix=""):
    """parts: list of (anchor, title, html). Returns (html, toc) with anchors prefixed."""
    body = "".join(f'<section id="{prefix}{a}"><h2>{esc(t)}</h2>{h}</section>' for a, t, h in parts)
    return body, [(prefix + a, t) for a, t, _ in parts]

def exercises(rows):
    body = "".join(f"<tr><td>{a}</td><td>{b}</td><td>{c}</td></tr>" for a, b, c in rows)
    return ('<div class="tblwrap"><table class="tbl"><thead><tr><th>Exercise</th><th>Where</th>'
            f'<th>What you change</th></tr></thead><tbody>{body}</tbody></table></div>')

def takeaways(items):
    return '<ol class="takeaways">' + "".join(f"<li><span>{i}</span></li>" for i in items)


def donow(num, title, grouping, tools, capture, feeds, goal, deliverable, need,
          steps, done_when, news, pattern, antipattern, reading, answer, lookfor):
    """A five-minute "Do it now" opener card (pattern: course 1258 activities).
    steps: list of (minutes, html); minutes must sum to 5.
    news: (headline, html) for the "In the news" infobox;
    reading: list of (url, label, source), rendered as bullets;
    answer: preformatted sample answer; lookfor: list of html items."""
    mins = [m for m, _ in steps]
    assert sum(mins) == 5, f"DN {num}: step minutes {mins} do not sum to 5"
    facts = (f'<tr><th>Time</th><td>5 min</td><th>Grouping</th><td>{grouping}</td></tr>'
             f'<tr><th>Tools</th><td>{tools}</td><th>Capture</th><td>{capture}</td></tr>'
             f'<tr><th>Feeds</th><td colspan="3">{feeds}</td></tr>')
    need_html = "".join(f"<li>{n}</li>" for n in need)
    step_rows = "".join(f'<tr><td class="t">{m}</td><td>{s}</td></tr>' for m, s in steps)
    headline, news_body = news
    refs = "".join(f'<li><a href="{u}">{esc(label)}</a> ({src})</li>' for u, label, src in reading)
    look = "".join(f"<li>{l}</li>" for l in lookfor)
    return f'''<div class="dn-card">
<p class="eyebrow">Lab {num} · Do it now · 5 minutes</p>
<h3><span class="dn-badge">DN {num}</span> {title}</h3>
<table class="dn-facts">{facts}</table>
<p><b>Goal.</b> {goal}</p>
<p><b>Deliverable.</b> {deliverable}</p>
<h4>You need</h4>
<ul class="dn-need">{need_html}</ul>
<h4>Steps</h4>
<div class="tblwrap"><table class="tbl dn-steps"><thead><tr><th>Min</th><th>Step</th></tr></thead><tbody>{step_rows}</tbody></table></div>
<div class="dn-done"><p><b>Capture.</b> {capture}</p><p><b>Done when.</b> {done_when}</p></div>
<div class="dn-info"><p class="dn-info-title">In the news</p><p><b>{headline}.</b> {news_body}</p></div>
<p class="dn-pattern"><b>Pattern.</b> {pattern} <b>Anti-pattern.</b> {antipattern}</p>
<div class="dn-reading"><p class="dn-reading-title">Further reading</p><ul>{refs}</ul></div>
<details class="dn-answer"><summary>Answer key</summary>
<p class="eyebrow">Sample answer</p>
<pre>{esc(answer)}</pre>
<p class="eyebrow">Look for</p>
<ul>{look}</ul>
</details>
</div>'''
