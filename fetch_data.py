#!/usr/bin/env python3
"""Build the CICIDS-2017 teaching sample used by code/Ch01-Lab.ipynb.

Downloads the CICIDS-2017 MachineLearningCSV bundle (8 daily CSV files,
~2.8M labelled flows), cleans it, and writes a stratified sample to
``data/CICIDS-2017.csv``. If the download is unavailable (e.g. offline lab
machines), a seeded synthetic file with the same schema is generated
instead, so the notebook always has data to run on.

Full dataset (official source):
    https://www.unb.ca/cic/datasets/ids-2017.html
Mirror used for the download:
    https://huggingface.co/datasets/bencorn/CICIDS2017

Usage:
    python3 fetch_data.py                # real sample; mock fallback on failure
    python3 fetch_data.py --mock         # skip the download, write the mock
    python3 fetch_data.py --rows 50000   # target sample size (default 100000)

Requires pandas (+ numpy for the mock). Needs ~2 GB RAM while sampling;
the extracted raw CSVs are deleted afterwards, the zip is kept for re-runs.
"""

from __future__ import annotations

import argparse
import shutil
import sys
import urllib.request
import zipfile
from pathlib import Path

ROOT = Path(__file__).resolve().parent
DATA_DIR = ROOT / "data"
RAW_DIR = DATA_DIR / "raw"
ZIP_PATH = DATA_DIR / "MachineLearningCSV.zip"
OUT_PATH = DATA_DIR / "CICIDS-2017.csv"

MIRROR_URL = (
    "https://huggingface.co/datasets/bencorn/CICIDS2017"
    "/resolve/main/csvs/MachineLearningCSV.zip"
)
OFFICIAL_PAGE = "https://www.unb.ca/cic/datasets/ids-2017.html"
SEED = 42
CHUNKSIZE = 250_000
MIN_PER_CLASS = 500  # attack classes smaller than this are kept whole

# Canonical CICIDS-2017 MachineLearningCSV schema (column names stripped of
# the leading spaces the raw files ship with). Used for the mock file.
MOCK_COLUMNS = [
    "Destination Port", "Flow Duration", "Total Fwd Packets",
    "Total Backward Packets", "Total Length of Fwd Packets",
    "Total Length of Bwd Packets", "Fwd Packet Length Max",
    "Fwd Packet Length Min", "Fwd Packet Length Mean", "Fwd Packet Length Std",
    "Bwd Packet Length Max", "Bwd Packet Length Min", "Bwd Packet Length Mean",
    "Bwd Packet Length Std", "Flow Bytes/s", "Flow Packets/s", "Flow IAT Mean",
    "Flow IAT Std", "Flow IAT Max", "Flow IAT Min", "Fwd IAT Total",
    "Fwd IAT Mean", "Fwd IAT Std", "Fwd IAT Max", "Fwd IAT Min",
    "Bwd IAT Total", "Bwd IAT Mean", "Bwd IAT Std", "Bwd IAT Max",
    "Bwd IAT Min", "Fwd PSH Flags", "Bwd PSH Flags", "Fwd URG Flags",
    "Bwd URG Flags", "Fwd Header Length", "Bwd Header Length",
    "Fwd Packets/s", "Bwd Packets/s", "Min Packet Length", "Max Packet Length",
    "Packet Length Mean", "Packet Length Std", "Packet Length Variance",
    "FIN Flag Count", "SYN Flag Count", "RST Flag Count", "PSH Flag Count",
    "ACK Flag Count", "URG Flag Count", "CWE Flag Count", "ECE Flag Count",
    "Down/Up Ratio", "Average Packet Size", "Avg Fwd Segment Size",
    "Avg Bwd Segment Size", "Fwd Header Length.1", "Fwd Avg Bytes/Bulk",
    "Fwd Avg Packets/Bulk", "Fwd Avg Bulk Rate", "Bwd Avg Bytes/Bulk",
    "Bwd Avg Packets/Bulk", "Bwd Avg Bulk Rate", "Subflow Fwd Packets",
    "Subflow Fwd Bytes", "Subflow Bwd Packets", "Subflow Bwd Bytes",
    "Init_Win_bytes_forward", "Init_Win_bytes_backward", "act_data_pkt_fwd",
    "min_seg_size_forward", "Active Mean", "Active Std", "Active Max",
    "Active Min", "Idle Mean", "Idle Std", "Idle Max", "Idle Min", "Label",
]


def download() -> None:
    print(f"Downloading {MIRROR_URL}\n  -> {ZIP_PATH} (~224 MB) ...")
    req = urllib.request.Request(MIRROR_URL, headers={"User-Agent": "fetch_data.py"})
    with urllib.request.urlopen(req) as resp, open(ZIP_PATH, "wb") as fh:
        shutil.copyfileobj(resp, fh)
    print(f"Downloaded {ZIP_PATH.stat().st_size / 1e6:.0f} MB.")


def extract() -> None:
    print(f"Extracting {ZIP_PATH} -> {RAW_DIR} ...")
    RAW_DIR.mkdir(parents=True, exist_ok=True)
    with zipfile.ZipFile(ZIP_PATH) as zf:
        zf.extractall(RAW_DIR)


def load_clean(path: Path):
    """Read one raw daily CSV: strip column names, keep numeric features +
    Label (drops Flow ID / IP / Timestamp columns if present), drop inf/NaN."""
    import numpy as np
    import pandas as pd

    chunks = []
    for chunk in pd.read_csv(path, chunksize=CHUNKSIZE):
        chunk.columns = chunk.columns.str.strip()
        numeric = chunk.select_dtypes(include="number").columns.tolist()
        chunk = chunk[numeric + ["Label"]]
        chunk = chunk.replace([np.inf, -np.inf], np.nan).dropna()
        # the raw files ship U+FFFD where the original labels had an en dash
        chunk["Label"] = chunk["Label"].str.replace("�", "–", regex=False)
        chunks.append(chunk)
    return pd.concat(chunks, ignore_index=True)


def sample_file(path: Path, budget: int):
    """Stratified sample of one daily file: proportional per label, with rare
    attack classes kept whole (up to MIN_PER_CLASS rows each)."""
    import pandas as pd

    df = load_clean(path)
    parts = []
    for label, group in df.groupby("Label"):
        share = max(MIN_PER_CLASS, round(budget * len(group) / len(df)))
        take = min(len(group), share)
        parts.append(group.sample(n=take, random_state=SEED))
    out = pd.concat(parts, ignore_index=True)
    print(f"  {path.name}: {len(df):>7,} flows -> sample {len(out):>6,}")
    return out


def build_real(rows: int) -> None:
    import pandas as pd

    if not ZIP_PATH.exists():
        download()
    csvs = sorted(RAW_DIR.rglob("*.csv"))
    if not csvs:
        extract()
        csvs = sorted(RAW_DIR.rglob("*.csv"))
    if not csvs:
        raise RuntimeError(f"no CSV files found under {RAW_DIR}")

    print(f"Sampling ~{rows:,} flows from {len(csvs)} daily files ...")
    budget = max(1, rows // len(csvs))
    parts = [sample_file(p, budget) for p in csvs]
    df = pd.concat(parts, join="inner", ignore_index=True)
    df = df.sample(frac=1.0, random_state=SEED, ignore_index=True)  # mix days
    df["Label"] = df.pop("Label")  # keep Label as the last column
    df.to_csv(OUT_PATH, index=False)
    print(f"Wrote {OUT_PATH} ({len(df):,} rows, "
          f"{OUT_PATH.stat().st_size / 1e6:.1f} MB)")
    print(df["Label"].value_counts().to_string())
    shutil.rmtree(RAW_DIR, ignore_errors=True)
    print(f"Removed {RAW_DIR} (kept {ZIP_PATH.name} for re-runs).")


def _mock_column(name: str, n: int, rng):
    import numpy as np

    low = name.lower()
    if "win_bytes" in low:
        return rng.integers(-1, 65535, n)
    if low.endswith("/s") and "bytes" in low:
        return rng.lognormal(10, 1.5, n)
    if low.endswith("/s"):
        return rng.lognormal(5, 1.5, n)
    if "ratio" in low:
        return rng.uniform(0, 5, n).round(2)
    if "flag" in low or "cwe" in low:
        return rng.binomial(1, 0.05, n)
    if "iat" in low or "duration" in low or "active" in low or "idle" in low:
        return rng.lognormal(10, 2.0, n).clip(0)
    if "port" in low:
        return rng.choice([80, 443, 53, 22, 8080, 3389], n)
    if "packets" in low and "bytes" not in low:
        return rng.poisson(4, n) + 1
    # lengths, byte counts, sizes, bulk rates
    return rng.lognormal(6, 1.2, n).clip(0)


def build_mock(rows: int) -> None:
    import numpy as np
    import pandas as pd

    print(f"Generating {rows:,} synthetic flows with the CICIDS-2017 schema ...")
    rng = np.random.default_rng(SEED)
    df = pd.DataFrame({c: _mock_column(c, rows, rng) for c in MOCK_COLUMNS[:-1]})
    df["Label"] = "BENIGN"

    # ~2% attacks with shifted signatures an anomaly detector should catch.
    ddos = rng.choice(rows, rows // 100, replace=False)
    rest = np.setdiff1d(rng.choice(rows, rows // 50, replace=False), ddos)
    df.loc[ddos, "Label"] = "DDoS"
    df.loc[ddos, "Flow Duration"] = rng.lognormal(6, 1.0, len(ddos)).clip(1)
    df.loc[ddos, "Flow Packets/s"] = rng.lognormal(12, 1.0, len(ddos))
    df.loc[ddos, "Total Fwd Packets"] = rng.poisson(200, len(ddos))
    df.loc[rest, "Label"] = "PortScan"
    df.loc[rest, "Flow Duration"] = rng.lognormal(5, 1.0, len(rest)).clip(1)
    df.loc[rest, "Total Fwd Packets"] = 1
    df.loc[rest, "Total Backward Packets"] = 0
    df.loc[rest, "SYN Flag Count"] = 1

    df.to_csv(OUT_PATH, index=False)
    print(f"Wrote mock {OUT_PATH} ({len(df):,} rows, "
          f"{OUT_PATH.stat().st_size / 1e6:.1f} MB)")
    print(df["Label"].value_counts().to_string())


def main() -> None:
    ap = argparse.ArgumentParser(description=__doc__,
                                 formatter_class=argparse.RawDescriptionHelpFormatter)
    ap.add_argument("--mock", action="store_true",
                    help="skip the download and write the synthetic file")
    ap.add_argument("--rows", type=int, default=100_000,
                    help="target number of flows (default 100000)")
    args = ap.parse_args()

    DATA_DIR.mkdir(exist_ok=True)
    if not args.mock:
        try:
            build_real(args.rows)
            return
        except Exception as exc:  # offline mirror, corrupt zip, ...
            print(f"Real-data build failed ({exc}).\n"
                  f"Falling back to the synthetic mock.\n"
                  f"Full dataset: {OFFICIAL_PAGE}", file=sys.stderr)
    build_mock(args.rows)


if __name__ == "__main__":
    main()
