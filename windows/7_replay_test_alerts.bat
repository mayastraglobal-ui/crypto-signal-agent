@echo off
setlocal
chcp 65001 >nul
set "PYTHONUTF8=1"
cd /d "%~dp0.."
title Crypto Signal Agent - TEST alert replay
rem The Signal Center safety check (docs\WINDOWS_WATCHER.md, TEST alerts): the last 14 days replayed with the TEST alert rules.
if not exist ".venv\Scripts\python.exe" (
  echo Run 1_setup.bat first.
  pause
  exit /b 1
)
echo Replaying the last 14 days with the TEST alert rules on real OKX candles (takes a few minutes)...
echo.
".venv\Scripts\python.exe" live_watcher.py --replay 14 --no-git
echo.
echo Nothing was sent to Telegram and nothing was changed.
pause
