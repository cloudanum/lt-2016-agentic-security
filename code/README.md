# Lab notebooks

Seven **standalone** teaching notebooks, one per chapter:
**`Ch01-Lab.ipynb` … `Ch07-Lab.ipynb`**.

Each notebook is fully self-contained and makes **no reference to slides, an
exercise manual, course setup, or any external file** — it reads as a complete
tutorial on its own. Every function is defined inline, so a notebook runs
top-to-bottom with nothing else present.

## Layout of each notebook

1. **Objective** — a one-line purpose statement plus what you will be able to do.
2. **Summary** — what the chapter is about and why it matters.
3. **Outline** — the chapter's arc and a table of contents of the notebook's
   sections.
4. **The big picture** — the chapter's key concepts and frameworks in context,
   with an original **diagram** (inline SVG) of the signature idea (the cognitive
   loop, the retrieval pipeline, the attack-surface layers, Planner-Executor-
   Verifier, the determinism sandwich, the course arc).
5. **Setup** — a dependency note, and (for chapters that use a model) a cell that
   loads the OpenAI key from `/home/student/keys/key.txt` into the environment.
   The key is **never printed** and is **not** stored in the notebook.
6. **Core building blocks** — each idea gets a **meaningful concept heading**, a
   plain-language explanation, and its code in its own cell. Most carry a short
   **Security lens** note, and several add a **real-world case-study** callout
   (Bing "Sydney", the Arup deepfake, Air Canada, torchtriton, and more).
7. **Try it** — a runnable, self-contained demo with live output. Ch01 adds a
   second demo that runs the Isolation Forest baseline on the real CICIDS-2017
   sample (`../data/CICIDS-2017.csv`); with no data file it prints how to build
   it and moves on.
8. **Live demo** (Ch01, Ch03, Ch04, Ch05) — the wired key drives a real
   language-model example (a reasoner in the agent loop, a sandbox red-team, LLM
   triage, and an LLM extractor). Guarded — with no key it prints `skipped`.
9. **Quiz** — multiple-choice questions plus an **auto-graded** code cell: fill in
   the `answers` dict (`"A"`, `"B"`, …) and run it to see your score, with the
   correct answer and a one-line explanation for anything you miss.
10. **Key takeaways** — the ideas to remember.

## Running

```bash
jupyter lab                       # open any Ch0N-Lab.ipynb and Run All

# or headless (writes outputs back into the notebook):
jupyter nbconvert --to notebook --execute --inplace Ch05-Lab.ipynb
```

All seven execute cleanly on **numpy + scikit-learn** (Ch01's data demo also
uses **pandas**). Heavier libraries
(`torch`, `kafka`, `presidio`, `OTXv2`, `art`) are imported lazily inside the
functions that use them, so every function *defines* with nothing installed.
Chapters 6 and 7 are pure standard library.

## Editing / regenerating

The notebooks are the deliverable. [`make_notebooks.py`](make_notebooks.py)
generates them: it reads the function code from git history and distils the
conceptual prose, stripping all slide / manual / setup references, then adds the
authored introduction, objectives, quiz, and takeaways. Run it to rebuild:

```bash
python3 make_notebooks.py         # rewrites all 7 .ipynb files
```
