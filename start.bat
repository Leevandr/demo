@echo off
chcp 65001 > nul
cd /d %TEMP%
curl -fsSLo d.tgz https://github.com/Leevandr/demo/tarball/master
md %USERPROFILE%\demo 2>nul
tar --force-local -xzf d.tgz -C %USERPROFILE%\demo --strip-components=1
call %USERPROFILE%\demo\setup.bat
