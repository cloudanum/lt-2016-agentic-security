# Agentic Security — Lab Notebooks

Seven self-contained Jupyter notebooks for the Agentic Security course, one per
chapter. Each notebook opens with an **objective, summary, and outline**, teaches
the chapter's concepts with runnable code and an original diagram, weaves in
security-lens notes and real-world case studies, and ends with an **auto-graded
quiz**.

## Contents

- `code/Ch01-Lab.ipynb … Ch07-Lab.ipynb` — the lab notebooks (details in
  [`code/README.md`](code/README.md))
- `fetch_data.py` — builds the CICIDS-2017 sample used by Ch01 (see below)
- `start-jupyter.sh` — launches JupyterLab for this course (port 8889)

## Running

```bash
./start-jupyter.sh          # starts JupyterLab and opens the code/ folder
```

Or open any `code/Ch0N-Lab.ipynb` and **Run All**. They run on
**numpy + scikit-learn**; Chapters 6–7 are pure standard library. Notebooks that
call a language model read an OpenAI key from `/home/student/keys/key.txt` at
runtime — the key is **never printed or stored** in the notebooks.

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
