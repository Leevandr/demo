# One-command setup

## On exam machine (cmd.exe)

```cmd
curl -fsSL https://raw.githubusercontent.com/Leevandr/demo/master/run.cmd -o %TEMP%\run.cmd && %TEMP%\run.cmd
```

What happens:

1. `curl` downloads `run.cmd` to `%TEMP%`.
2. `run.cmd` clones (or pulls) this repo into `%USERPROFILE%\demo`.
3. `setup.bat` creates a venv, installs PyQt6 / PyMySQL / pymysql-dist from PyPI, connects to MySQL, restores `sql/shoes.sql` into database `shoes`, patches `src/db.py` with the working credentials, verifies imports.
4. Prompt: `Run application now? [Y/N]` — answer `Y` to launch the GUI.

Clone location is `%USERPROFILE%\demo`, which survives `%TEMP%`/`Downloads` cleanup.

## MySQL endpoints tried (in order)

| # | host | port | user | password |
|---|---|---|---|---|
| 1 | localhost | 3306 | root | root |
| 2 | localhost | 3306 | root | (empty) |
| 3 | localhost | 3308 | root | (empty) |

First matching set is used. `src/db.py` is patched in place; original is preserved as `src/db.py.bak`.

## Requirements on target machine

- Windows 10+
- Git for Windows (`git --version` works)
- Python 3.10-3.13 (`py --version` works)
- Internet for `pip install`
- MySQL/MariaDB running on one of the endpoints above

## Re-run after a change

```cmd
%TEMP%\run.cmd
```

The bootstrap is idempotent: clone if missing, otherwise pull, then re-run setup.

## Manual fallback (if curl missing)

```cmd
git clone https://github.com/Leevandr/demo %USERPROFILE%\demo
cd /d %USERPROFILE%\demo
setup.bat
```
