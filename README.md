# Agentic Security — Lab Notebooks

Seven self-contained Jupyter notebooks for the Agentic Security course, one per
chapter. Each notebook opens with an **objective, summary, and outline**, teaches
the chapter's concepts with runnable code and an original diagram, weaves in
security-lens notes and real-world case studies, and ends with an **auto-graded
quiz**.

## Contents

- `code/Ch01-Lab.ipynb … Ch07-Lab.ipynb` — the lab notebooks (details in
  [`code/README.md`](code/README.md))
- `code/make_notebooks.py` — the generator that builds them
- `start-jupyter.sh` — launches JupyterLab for this course (port 8889)

## Running

```bash
./start-jupyter.sh          # starts JupyterLab and opens the code/ folder
```

Or open any `code/Ch0N-Lab.ipynb` and **Run All**. They run on
**numpy + scikit-learn**; Chapters 6–7 are pure standard library. Notebooks that
call a language model read an OpenAI key from `/home/student/keys/key.txt` at
runtime — the key is **never printed or stored** in the notebooks.

Datasets live under `data/` (git-ignored — large, fetched separately).
