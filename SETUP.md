# One-command setup

## On exam machine (cmd.exe in PyCharm — Alt+F12)

### Option A — without git (curl + built-in tar)

```cmd
curl -fsSL https://github.com/Leevandr/demo/archive/refs/heads/master.tar.gz -o %TEMP%\d.tgz && mkdir %USERPROFILE%\demo 2>nul & tar --force-local -xzf %TEMP%\d.tgz -C %USERPROFILE%\demo --strip-components=1 && %USERPROFILE%\demo\setup.bat
```

Notes:
- Requires only built-in `curl.exe` and `tar.exe` (Windows 10 1803+).
- `--force-local` tells bsdtar to treat `C:\...` as local path, not `host:path`.
- Re-run is safe — `tar -xzf` overwrites tracked files, `setup.bat` then rebuilds `.venv` and DB.
- Built-in tar on Windows does **not** support ZIP, so we fetch `.tar.gz` instead.

### Option B — with git (if git is available)

```cmd
git clone https://github.com/Leevandr/demo %USERPROFILE%\demo && %USERPROFILE%\demo\setup.bat
```

Both options produce identical state in `C:\Users\<user>\demo`, venv created, MySQL connected, database restored, ready to run. Takes ~30 seconds.

### Re-run setup later (refresh venv + DB)

```cmd
%USERPROFILE%\demo\setup.bat
```

### Pull latest code from GitHub

```cmd
cd /d %USERPROFILE%\demo && git pull && setup.bat
```

### Forced full re-init (when something is broken)

```cmd
powershell -Command "Remove-Item -Recurse -Force $env:USERPROFILE\demo -ErrorAction SilentlyContinue" && git clone https://github.com/Leevandr/demo %USERPROFILE%\demo && %USERPROFILE%\demo\setup.bat
```

(PowerShell is used for `Remove-Item` because `rmdir` can't handle long paths inside `.venv`.)

## What setup.bat does

1. Locates itself via `%~dp0` — works regardless of CWD.
2. Verifies `py` launcher (Python 3.10–3.13).
3. Wipes old `.venv\` and `__pycache__\`.
4. Creates fresh `.venv` via `py -m venv`.
5. Installs `PyQt6==6.11.0`, `PyQt6-Qt6==6.11.1`, `PyQt6-sip==13.11.1`, `PyMySQL`, `pymysql-dist>=0.1.2` from PyPI.
6. Hands off to `setup_helper.py`:
   - Tries MySQL endpoints in this order:
     | # | host | port | user | password |
     |---|---|---|---|---|
     | 1 | localhost | 3306 | root | root |
     | 2 | localhost | 3306 | root | (empty) |
     | 3 | localhost | 3308 | root | (empty) |
   - First match wins. `src/db.py` is patched in place; original is saved as `src/db.py.bak`.
   - Creates database `shoes` if missing.
   - Restores `sql/shoes.sql` via `pymysql_dist.schema.execute_script`.
   - Verifies imports (`PyQt6`, `PyMySQL`, `pymysql_dist`).
7. Prompts: `Run application now? [Y/N]` → `Y` launches the GUI via `python -m src.main`.

## Why `%USERPROFILE%\demo`

Picked because it's the user profile (not `%TEMP%` or `Downloads/`) — survives the cleanup tools exam machines often run between sessions.

## PyCharm interpreter (if you want debugging)

After setup completes:

```
File → Settings → Project → Python Interpreter → Add → Existing → %USERPROFILE%\demo\.venv\Scripts\python.exe
```

## Requirements on target machine

- Windows 10+
- Git for Windows (`git --version` works)
- Python 3.10–3.13 (`py --version` works)
- Internet (for `pip install` and `git clone`)
- MySQL/MariaDB running on one of the endpoints above

If `py` is missing → install Python 3.13 from <https://www.python.org/downloads/>. Tick **"Add python.exe to PATH"** and **"Install launcher for all users"**.

## Troubleshooting

| Symptom | Fix |
|---|---|
| `'git' is not recognized` | Install Git: <https://git-scm.com/download/win> |
| `'py' is not recognized` | Install Python 3.13. |
| `[FAIL] Cannot connect to MySQL` | Start OpenServer (green flag in tray). |
| `[FAIL] pip install failed` | Check internet. Run `py -m pip install --upgrade pip`. |
| `destination path 'demo' already exists` | Use the forced full re-init command above. |
| Want to revert `src/db.py` to original | `copy src\db.py.bak src\db.py /Y` |
