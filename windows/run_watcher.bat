@echo off
chcp 65001 >nul
set "PYTHONUTF8=1"
set "PYTHONUNBUFFERED=1"
cd /d "%~dp0.."
title Crypto Watcher - keep this window open (minimize it)
if exist STOP_WATCHER del STOP_WATCHER
if not exist ".venv\Scripts\python.exe" (
  echo The watcher is not installed yet - double-click windows\1_setup.bat first.
  pause
  exit /b 1
)
:loop
".venv\Scripts\python.exe" live_watcher.py
if errorlevel 3 if not errorlevel 4 (
  echo Another watcher is already running on this PC - this window closes in 15 seconds.
  timeout /t 15 >nul
  exit /b 0
)
if exist STOP_WATCHER goto end
echo The watcher stopped unexpectedly. It restarts in 30 seconds - close this window to stop it.
timeout /t 30 /nobreak >nul
if exist STOP_WATCHER goto end
goto loop
:end
del STOP_WATCHER 2>nul
echo Watcher stopped.
timeout /t 5 >nul
