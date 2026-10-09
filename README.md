# Agentic Security — Lab Notebooks

Seven self-contained Jupyter notebooks for the Agentic Security course, one per
chapter (about 1–1¾ hours each). Every notebook follows the same flow: an
objective and a **lab roadmap** of timed Parts; each concept explained, run, and
interpreted on the spot; every **attack paired with the defense that stops it**;
**✅ checkpoints**; hands-on **🧪 Your turn** exercises with self-checks and
hidden solutions; and an **auto-graded quiz**.

## Contents

- `code/Ch01-Lab.ipynb … Ch07-Lab.ipynb` — the lab notebooks (details in
  [`code/README.md`](code/README.md))
- `demos/pyrit-red-team.ipynb` — tool-spotlight demo: red-team the Lab 3
  translation bot with Microsoft's [PyRIT](https://github.com/Azure/PyRIT)
  (one-shot campaign, Crescendo multi-turn, then the same campaign against the
  defended pipeline). Needs `pip install pyrit openai`; runs offline with
  scripted stand-ins when no API key is set.
- `results/Ch0N-results.md` — highlights plus every cell output from the latest
  full run of each notebook (regenerate with `python3 gen_results.py`; the
  header states whether the run used a live key)
- `workbook/Agentic-Security-Lab-Workbook.html` — the companion workbook: one
  self-contained HTML file (no external resources) with, for each lab, an
  introduction, key terms, SVG flowcharts of the lab's structure and logic,
  and the expected outputs with what they mean. Rebuild it after re-running the
  notebooks with `python3 workbook/src/build_workbook.py`
- `fetch_data.py` — builds the CICIDS-2017 sample used by Ch01 (see below)
- `start-jupyter.sh` — launches JupyterLab for this course (port 8889)

## Running

**On your own machine (Windows / macOS / Ubuntu):** see [`SETUP.md`](SETUP.md)
— install Python, `pip install -r requirements.txt`, then `jupyter lab`.

**On the course lab VM:**

```bash
./start-jupyter.sh          # starts JupyterLab and opens the code/ folder
```

Or open any `code/Ch0N-Lab.ipynb` and **Run All**. They run on
**numpy + scikit-learn**; Chapters 6–7 are pure standard library. Notebooks
that call a language model read an OpenAI key from
`/home/student/keys/key.txt`, or from `OPENAI_API_KEY` if it is already set —
the key is **never printed or stored** in the notebooks. Without a key every
notebook still runs end to end: live cells print `skipped`, and Ch03 falls back
to replies recorded from a real `gpt-4o-mini` run.

Ch01's anomaly-detection demo reads `code/CICIDS-2017.csv` — a 100k-flow
sample of the [CIC-IDS2017 dataset](https://www.unb.ca/cic/datasets/ids-2017.html)
that **ships in the repo**, so a plain clone has everything the labs need.
Rebuilding it is only needed to change the sample:

```bash
python3 fetch_data.py          # downloads ~224 MB and rewrites the sample
python3 fetch_data.py --mock   # offline: same schema, synthetic flows
```

If the download fails the script falls back to the synthetic file
automatically, so the notebook always has data. Download intermediates live
under `data/` (git-ignored).
