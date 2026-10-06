@echo off
setlocal
rem The update replaces this file too, so it runs from a copy in the TEMP folder.
if /i not "%~1"=="--from-temp" (
  copy /y "%~f0" "%TEMP%\crypto-agent-update.bat" >nul
  "%TEMP%\crypto-agent-update.bat" --from-temp "%~dp0"
  exit /b
)
set "WDIR=%~2"
cd /d "%WDIR%.."
set "ROOTDIR=%CD%"
title Crypto Signal Agent - update
echo Stopping the watcher...
call "%WDIR%3_stop_watcher.bat" >nul
echo Downloading the newest version from GitHub...
powershell -NoProfile -Command "$ErrorActionPreference='Stop'; $z=Join-Path $env:TEMP 'crypto-agent.zip'; $d=Join-Path $env:TEMP 'crypto-agent-update'; Invoke-WebRequest -UseBasicParsing 'https://github.com/mayastraglobal-ui/crypto-signal-agent/archive/refs/heads/main.zip' -OutFile $z; if (Test-Path $d) { Remove-Item $d -Recurse -Force }; Expand-Archive $z $d -Force"
if errorlevel 1 (
  echo Download failed - check the internet connection and try again. Nothing was changed.
  pause
  exit /b 1
)
robocopy "%TEMP%\crypto-agent-update\crypto-signal-agent-main" "%ROOTDIR%" /E /XD .venv logs journal .git /XF telegram.env STOP_WATCHER live_watcher_state.json /NFL /NDL /NJH /NJS /NP >nul
if errorlevel 8 (
  echo Copying the new files failed. Nothing important was lost - try again.
  pause
  exit /b 1
)
echo Updating the Python packages...
".venv\Scripts\python.exe" -m pip install -q -r requirements.txt
echo.
echo Updated. Your Telegram settings were kept.
choice /C YN /M "Start the watcher again now"
if not errorlevel 2 start "Crypto Watcher" /min "%WDIR%run_watcher.bat"
