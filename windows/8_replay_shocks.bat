@echo off
setlocal
chcp 65001 >nul
set "PYTHONUTF8=1"
cd /d "%~dp0.."
title Crypto Signal Agent - shock alarm replay
rem The shock alarm's check (docs\SHOCK_ALARM.md): the last 14 days replayed minute by minute with its rules.
if not exist ".venv\Scripts\python.exe" (
  echo Run 1_setup.bat first.
  pause
  exit /b 1
)
echo Replaying the last 14 days with the shock alarm's rules on real OKX 1-minute candles (takes about 10 minutes)...
echo.
".venv\Scripts\python.exe" live_watcher.py --shock-replay 14 --no-git
echo.
echo Nothing was sent to Telegram and nothing was changed.
pause
