# Student setup — Windows, macOS, Ubuntu

Install the Agentic Security labs on your own machine in about 10 minutes.
Everything the labs need ships in this repository — the notebooks run even
without an API key or an internet connection.

You need: **Python 3.10 or newer** and **Git**.

---

## 1. Install Python and Git

### Windows

1. Install Python from <https://www.python.org/downloads/>. During setup,
   **tick "Add python.exe to PATH"** — this is the step everyone misses.
2. Install Git from <https://git-scm.com/download/win> (defaults are fine).
   This also gives you **Git Bash**, a Linux-style terminal.
3. Open a **new** PowerShell or Command Prompt and check:

   ```bat
   python --version
   git --version
   ```

### macOS

1. Open **Terminal** and run:

   ```bash
   xcode-select --install      # gives you git and the compiler tools
   ```

2. Install Python 3 with Homebrew (<https://brew.sh>) — or use the installer
   from <https://www.python.org/downloads/>:

   ```bash
   brew install python
   ```

3. Check:

   ```bash
   python3 --version
   git --version
   ```

### Ubuntu / Debian

```bash
sudo apt update
sudo apt install -y python3 python3-venv python3-pip git
python3 --version
```

---

## 2. Get the code

```bash
git clone https://github.com/cloudanum/lt-2016-agentic-security.git
cd lt-2016-agentic-security
```

(Or download the ZIP from GitHub → **Code → Download ZIP** and unzip it,
then open a terminal in that folder.)

---

## 3. Create a virtual environment and install

A virtual environment keeps the course packages separate from the rest of
your system.

### Windows (PowerShell)

```bat
python -m venv .venv
.venv\Scripts\Activate.ps1
python -m pip install --upgrade pip
pip install -r requirements.txt
```

If PowerShell refuses to run the activate script, run this once first:

```bat
Set-ExecutionPolicy -ExecutionPolicy RemoteSigned -Scope CurrentUser
```

(Command Prompt instead of PowerShell? Use `.venv\Scripts\activate.bat`.)

### macOS / Ubuntu

```bash
python3 -m venv .venv
source .venv/bin/activate
python -m pip install --upgrade pip
pip install -r requirements.txt
```

Your prompt now shows `(.venv)`. Every time you come back to the course in a
new terminal, re-activate it from the course folder:

- Windows: `.venv\Scripts\Activate.ps1`
- macOS / Ubuntu: `source .venv/bin/activate`

---

## 4. Start the labs

```bash
jupyter lab
```

Your browser opens on the course folder. Open `code/Ch01-Lab.ipynb`, then
**Run → Run All Cells** — or work through the Parts one cell at a time with
Shift+Enter. Work through the chapters in order, Ch01 → Ch07.

---

## 5. Optional: add an OpenAI API key

The labs run **without a key** — live-model cells print `skipped`, and Ch03
uses replies recorded from a real `gpt-4o-mini` run. With a key, those cells
call the model live. The key is **never printed or saved** into the
notebooks.

Pick **one** of these (the notebooks check them in order):

1. A file at `~/keys/key.txt` containing just the key
   (`C:\Users\<you>\keys\key.txt` on Windows), or
2. A `keys/key.txt` file inside the folder where you start Jupyter, or
3. The `OPENAI_API_KEY` environment variable:

   - Windows PowerShell: `$env:OPENAI_API_KEY = "sk-..."` (current session) or
     set it permanently via *Settings → Environment Variables*.
   - macOS / Ubuntu: `export OPENAI_API_KEY="sk-..."` (add to `~/.zshrc` or
     `~/.bashrc` to keep it).

---

## Troubleshooting

| Symptom | Fix |
|---|---|
| `'python' is not recognized` (Windows) | Reinstall Python and tick **Add to PATH**; or use `py` instead of `python`. |
| `externally-managed-environment` (Ubuntu) | You skipped step 3 — always install inside the `.venv`. |
| `jupyter: command not found` | The venv is not active — re-run the activate command from step 3. |
| A cell says `skipped` | No API key configured — expected; the lab still runs fully (see step 5). |
| Kernel keeps dying | Close other notebooks, or restart with **Kernel → Restart Kernel and Run All**. |
| `pip install` fails on `scikit-learn` (Windows) | `python -m pip install --upgrade pip setuptools wheel`, then retry. |
| Nothing opens in the browser | Copy the `http://localhost:8888/...` URL from the terminal into your browser. |
