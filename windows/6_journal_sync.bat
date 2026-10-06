@echo off
setlocal
chcp 65001 >nul
set "PYTHONUTF8=1"
cd /d "%~dp0.."
title Crypto Signal Agent - journal sync setup
rem Optional: a GitHub token so your Telegram button choices and results reach the research (docs\WINDOWS_WATCHER.md, Journal sync).
if not exist ".venv\Scripts\python.exe" (
  echo Run 1_setup.bat first.
  pause
  exit /b 1
)
".venv\Scripts\python.exe" live_watcher.py --setup-github
if errorlevel 1 (
  echo.
  echo Journal sync is NOT on. Nothing was changed - the watcher works as before.
  pause
  exit /b 1
)
echo.
echo Restarting the watcher so it uses the token...
call "%~dp03_stop_watcher.bat" >nul
call "%~dp02_start_watcher.bat"
pause
