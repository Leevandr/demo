@echo off
chcp 65001 > nul
cd /d %TEMP%
echo === downloading project archive...
curl -fsSLo d.tgz https://github.com/Leevandr/demo/tarball/master
if errorlevel 1 (
    echo [FAIL] curl failed - check internet connection.
    exit /b 1
)
md %USERPROFILE%\demo 2>nul
echo === extracting...
tar --force-local -xzf d.tgz -C %USERPROFILE%\demo --strip-components=1
if errorlevel 1 (
    echo [FAIL] tar failed.
    exit /b 1
)
call %USERPROFILE%\demo\setup.bat
