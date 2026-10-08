# Lab notebooks

Seven **standalone** teaching notebooks, one per chapter:
**`Ch01-Lab.ipynb` … `Ch07-Lab.ipynb`**.

Each notebook is fully self-contained and makes **no reference to slides, an
exercise manual, course setup, or any external file** (other than Ch01's
`CICIDS-2017.csv`, which ships here). Every function is defined inline, so a
notebook runs top-to-bottom with nothing else present.

## How each notebook flows

1. **Objective** and **Summary** — what you will build and why it matters.
2. **Lab roadmap** — the chapter arc and a table of numbered *Parts* with time
   estimates (each lab is 1–1¾ hours).
3. **The big picture** — key concepts and frameworks, with an original inline
   SVG diagram of the chapter's signature idea.
4. **Setup** — dependencies, and (for chapters that use a model) a cell that
   loads the OpenAI key from `/home/student/keys/key.txt` or `OPENAI_API_KEY`.
   The key is **never printed** and is **not** stored in the notebook.
5. **Parts 1…N** — each concept is *explained → defined → run → interpreted*
   right where it is introduced (no "define everything, run it at the end").
   Every attack is followed by the defense that stops it, run against the same
   traffic, and **Security lens** / **real-world case** callouts tie each idea to
   OWASP, MITRE ATLAS, NIST, and real incidents.
6. **✅ Checkpoints** — what you should have seen before moving on.
7. **🧪 Your turn** — 1–3 hands-on exercises per chapter. Each has a `# TODO`
   section, a self-check that prints ✓ or a hint, and a collapsible
   **Show a solution** cell underneath.
8. **Quiz** — six scenario-style multiple-choice questions plus an
   **auto-graded** cell (answers base64-encoded so they are not obvious).
9. **Key takeaways** and a pointer to the next chapter.

## What each lab does

| Lab | Attack you run | Defense you build |
|---|---|---|
| Ch01 Foundations | Novel attacks vs. detectors; hijacked tool calls | Four detectors on CICIDS-2017; a schema-enforcing tool gateway with an audit log |
| Ch02 GenAI SecOps | RAG extraction; knowledge-base poisoning | ACL + provenance-checked retrieval, ingestion filtering, DLP on both paths, cost-based thresholds, a risk register |
| Ch03 Hacking agents | Five injection variants, prompt leak, jailbreak, FGSM, deepfake fraud | Input guard → spotlighting → output guard, adversarial training, out-of-band verification |
| Ch04 Attack surface | Targeted poisoning, model extraction, timing side channel, payload splitting, slopsquatting, process hollowing | Label-consistency check, query budgets, constant-time padding, session moderation, import/PyPI audit, lookalike triage |
| Ch05 Autonomous SecOps | Unapproved destructive actions, malformed tickets, log tampering | Planner → Executor → Verifier with an approval queue, bus-driven triage, schema validation, HMAC hash-chain verification |
| Ch06 Governance | Ungoverned go-live | EU AI Act tiering, checklist scoring, RACI validation, Zero-Trust gate, determinism sandwich, PQC inventory |
| Ch07 Capstone | — | Maturity assessment, what-if leverage analysis, 30/60/90-day roadmap, self-assessment |

## Running

```bash
jupyter lab                       # open any Ch0N-Lab.ipynb and Run All

# or headless (writes outputs back into the notebook):
jupyter nbconvert --to notebook --execute --inplace Ch05-Lab.ipynb
```

All seven execute cleanly on **numpy + scikit-learn** (Ch01 also uses
**pandas**). Heavier libraries (`torch`, `mcp`, `kafka`, `presidio`, `OTXv2`)
are imported lazily inside the functions that use them, and each has a
runnable fallback (a scikit-learn autoencoder, a schema-enforcing registry, an
in-process bus, a regex scrubber). Chapters 6 and 7 are pure standard library.

**Without an API key** every notebook still runs: live-LLM cells print
`skipped`, and Ch03's red-team and defenses run on replies recorded from a real
`gpt-4o-mini` run. **With a key**, the live cells (Ch01 reasoner, Ch02 answer,
Ch03 red-team + layered defense, Ch04 triage / slopsquat / splitting replay,
Ch05 extractor + playbook) call the model.

Ch04's import audit queries `pypi.org` when the network is reachable and
reports "verify by hand" when it is not.

## Editing

The notebooks are the deliverable — edit them directly. Each exercise cell
stores its reference solution in the cell metadata (`metadata.solution`), so a
solution can be spliced in before the `# ---- self-check ----` marker to
confirm the self-check passes.
