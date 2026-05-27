@echo off
chcp 65001 > nul
setlocal enabledelayedexpansion

set "PROJECT_DIR=%CD%"
set "HELPER=%PROJECT_DIR%\setup_helper.py"

echo.
echo === Project setup: %PROJECT_DIR%
echo.

REM -- 1. Project layout check
if exist "%PROJECT_DIR%\src\main.py" (
    set "MAIN_MODULE=src.main"
    goto :main_ok
)
if exist "%PROJECT_DIR%\main.py" (
    set "MAIN_MODULE=main"
    goto :main_ok
)
echo [FAIL] No main.py found in %PROJECT_DIR%
echo        Run setup.bat from the project root (folder that contains src\main.py).
exit /b 1
:main_ok

REM -- 2. py launcher check
where py >nul 2>&1
if errorlevel 1 (
    echo [FAIL] 'py' launcher not found in PATH.
    echo        Install Python 3.12 or 3.13 from https://www.python.org/downloads/
    echo        Tick: "Add python.exe to PATH" and "Install launcher for all users".
    exit /b 1
)

REM -- 3. Python version check (3.10-3.13)
py -c "import sys; sys.exit(0 if (3,10) <= sys.version_info[:2] <= (3,13) else 1)" 2>nul
if errorlevel 1 (
    echo [FAIL] Python version not supported. Need 3.10-3.13.
    py --version
    exit /b 1
)

REM -- 4. Helper script must exist
if not exist "%HELPER%" (
    echo [FAIL] Helper script missing: %HELPER%
    echo        Make sure the clone completed successfully.
    exit /b 1
)

REM -- 5. Cleanup old venv and caches
if exist "%PROJECT_DIR%\.venv" (
    rmdir /s /q "%PROJECT_DIR%\.venv"
)
for /d /r "%PROJECT_DIR%" %%d in (__pycache__) do (
    if exist "%%d" rmdir /s /q "%%d"
)

REM -- 6. Create venv
py -m venv "%PROJECT_DIR%\.venv"
if errorlevel 1 (
    echo [FAIL] Failed to create venv at %PROJECT_DIR%\.venv
    exit /b 1
)
echo [OK] Venv     : created
set "PY=%PROJECT_DIR%\.venv\Scripts\python.exe"

REM -- 7. Install packages (online from PyPI)
"%PY%" -m pip install --upgrade --disable-pip-version-check --quiet pip setuptools wheel
"%PY%" -m pip install --disable-pip-version-check --quiet "PyQt6==6.11.0" "PyQt6-Qt6==6.11.1" "PyQt6-sip==13.11.1" "PyMySQL>=1.1,<2" "pymysql-dist>=0.1.2"
if errorlevel 1 (
    echo [FAIL] pip install failed. Showing detailed log:
    "%PY%" -m pip install --disable-pip-version-check "PyQt6==6.11.0" "PyQt6-Qt6==6.11.1" "PyQt6-sip==13.11.1" "PyMySQL>=1.1,<2" "pymysql-dist>=0.1.2"
    echo        Check internet connection. If no internet, see README_SETUP.md for offline mode.
    exit /b 1
)
echo [OK] Packages : installed

REM -- 8. Configure database + verify imports
"%PY%" "%HELPER%" --project "%PROJECT_DIR%"
if errorlevel 1 (
    exit /b 1
)

REM -- 9. Final banner
echo.
echo     SETUP COMPLETE
echo.
echo     PyCharm interpreter: %PROJECT_DIR%\.venv\Scripts\python.exe
echo.

REM -- 10. Optional run
set "RUN="
set /p RUN=Run application now? [Y/N]:
if /i "%RUN%"=="Y" (
    pushd "%PROJECT_DIR%"
    "%PY%" -m %MAIN_MODULE%
    popd
)

endlocal
exit /b 0
