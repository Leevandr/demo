"""Helper for setup.bat. Runs inside the freshly created project venv."""
from __future__ import annotations

import argparse
import re
import shutil
import sys
from pathlib import Path


# Order matters: most likely target-machine credentials go first.
CANDIDATES = [
    {"host": "localhost", "port": 3306, "user": "root", "password": "root"},
    {"host": "localhost", "port": 3306, "user": "root", "password": ""},
    {"host": "localhost", "port": 3308, "user": "root", "password": ""},
]


def reconfigure_stdio() -> None:
    for stream in (sys.stdout, sys.stderr):
        try:
            stream.reconfigure(encoding="utf-8")
        except Exception:
            pass


def fail(message: str, hint: str | None = None):
    print(f"[FAIL] {message}")
    if hint:
        print(f"       {hint}")
    sys.exit(1)


def read_db_py(db_py: Path) -> dict:
    text = db_py.read_text(encoding="utf-8")
    def pick(pattern: str, default):
        m = re.search(pattern, text)
        return m.group(1) if m else default
    return {
        "host": pick(r'host\s*=\s*"([^"]*)"', "localhost"),
        "port": int(pick(r"port\s*=\s*(\d+)", "3306")),
        "user": pick(r'user\s*=\s*"([^"]*)"', "root"),
        "password": pick(r'password\s*=\s*"([^"]*)"', ""),
        "database": pick(r'database\s*=\s*"([^"]*)"', "shoes"),
    }


def patch_db_py(db_py: Path, new_creds: dict) -> bool:
    text = db_py.read_text(encoding="utf-8")
    original = text
    text = re.sub(r'(host\s*=\s*)"[^"]*"', rf'\1"{new_creds["host"]}"', text, count=1)
    text = re.sub(r'(port\s*=\s*)\d+', rf'\g<1>{new_creds["port"]}', text, count=1)
    text = re.sub(r'(user\s*=\s*)"[^"]*"', rf'\1"{new_creds["user"]}"', text, count=1)
    text = re.sub(r'(password\s*=\s*)"[^"]*"', rf'\1"{new_creds["password"]}"', text, count=1)
    if text == original:
        return False
    backup = db_py.with_suffix(db_py.suffix + ".bak")
    if not backup.exists():
        shutil.copy2(db_py, backup)
    db_py.write_text(text, encoding="utf-8")
    return True


def try_connect(creds: dict, database: str | None = None):
    import pymysql
    kwargs = dict(creds)
    if database:
        kwargs["database"] = database
    kwargs["connect_timeout"] = 3
    return pymysql.connect(**kwargs)


def find_working_creds(prefer: dict) -> dict | None:
    seq = [prefer] + [c for c in CANDIDATES if c != prefer]
    for c in seq:
        try:
            conn = try_connect(c)
            conn.close()
            return c
        except Exception:
            continue
    return None


def ensure_database(creds: dict, database: str) -> None:
    conn = try_connect(creds)
    try:
        with conn.cursor() as cur:
            cur.execute(
                f"CREATE DATABASE IF NOT EXISTS `{database}` "
                f"DEFAULT CHARACTER SET utf8mb4 COLLATE utf8mb4_unicode_ci"
            )
        conn.commit()
    finally:
        conn.close()


def restore_dump(creds: dict, database: str, dump_path: Path) -> int:
    from pymysql_dist.schema import execute_script
    sql_text = dump_path.read_text(encoding="utf-8")
    conn = try_connect(creds, database=database)
    try:
        return execute_script(conn, sql_text, commit=True)
    finally:
        conn.close()


def verify_imports() -> dict:
    import pymysql
    import pymysql_dist
    from PyQt6 import QtCore
    return {
        "pymysql": pymysql.__version__,
        "pymysql_dist": pymysql_dist.__version__,
        "PyQt6": QtCore.PYQT_VERSION_STR,
    }


def main() -> int:
    reconfigure_stdio()
    parser = argparse.ArgumentParser()
    parser.add_argument("--project", required=True)
    args = parser.parse_args()

    project = Path(args.project).resolve()

    db_py = project / "src" / "db.py"
    if not db_py.exists():
        fail(f"src/db.py not found in {project}",
             "Run setup.bat from the project root.")

    current = read_db_py(db_py)
    database = current["database"]

    prefer = {k: current[k] for k in ("host", "port", "user", "password")}
    creds = find_working_creds(prefer)
    if creds is None:
        fail(
            "Cannot connect to MySQL on any of the standard endpoints.",
            "Start OpenServer (green flag in tray), then re-run setup.bat. "
            "Tried: 3306 root/root, 3306 root/empty, 3308 root/empty.",
        )

    print(f"[OK] MySQL    : port {creds['port']}")

    try:
        ensure_database(creds, database)
    except Exception as exc:
        fail(f"Cannot create database '{database}': {exc}",
             "Check that root user has CREATE privilege.")

    dump = project / "sql" / "shoes.sql"
    if not dump.exists():
        fail(f"SQL dump not found: {dump}",
             "Project sql/shoes.sql is missing - did the clone succeed?")
    try:
        n = restore_dump(creds, database, dump)
    except Exception as exc:
        fail(f"Failed to restore dump: {exc}",
             f"Open {dump} and check for syntax errors.")
    print(f"[OK] Database : {database} ready")

    changed = patch_db_py(db_py, creds)

    try:
        versions = verify_imports()
    except Exception as exc:
        fail(f"Import verification failed: {exc}",
             "Try: rmdir /s /q .venv && setup.bat (forces clean install).")
    print(f"[OK] Imports  : verified")
    print()
    print(f"     port={creds['port']} user={creds['user']} pass={'set' if creds['password'] else 'empty'}")
    print(f"     restored {n} statements from {dump.name}")
    print(f"     PyQt6 {versions['PyQt6']}, PyMySQL {versions['pymysql']}, pymysql_dist {versions['pymysql_dist']}")
    print(f"     src/db.py: {'updated (backup: src/db.py.bak)' if changed else 'in sync'}")
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
