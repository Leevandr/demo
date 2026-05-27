@echo off
chcp 65001 > nul
setlocal

set "HOME_DIR=%USERPROFILE%\demo"
set "REPO_URL=https://github.com/Leevandr/demo.git"

echo.
echo === bootstrap: %HOME_DIR%
echo.

REM -- 1. Ensure git is available
where git >nul 2>&1
if errorlevel 1 (
    echo [FAIL] git not found in PATH.
    echo        Install Git for Windows: https://git-scm.com/download/win
    exit /b 1
)

REM -- 2. Clone or pull
if exist "%HOME_DIR%\.git" (
    echo [step] git pull...
    pushd "%HOME_DIR%"
    git pull --ff-only
    if errorlevel 1 (
        echo [WARN] git pull failed - using current local copy.
    )
    popd
) else (
    if exist "%HOME_DIR%" (
        echo [WARN] %HOME_DIR% exists but is not a git repo. Removing...
        rmdir /s /q "%HOME_DIR%"
    )
    echo [step] git clone...
    git clone "%REPO_URL%" "%HOME_DIR%"
    if errorlevel 1 (
        echo [FAIL] git clone failed.
        echo        Check internet connection and that the repo is accessible.
        exit /b 1
    )
)

REM -- 3. Hand off to setup.bat (absolute path; setup.bat self-locates via %~dp0)
if not exist "%HOME_DIR%\setup.bat" (
    echo [FAIL] setup.bat missing after clone/pull.
    exit /b 1
)

call "%HOME_DIR%\setup.bat"
set "RC=%ERRORLEVEL%"

endlocal & exit /b %RC%
