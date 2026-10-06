@echo off
setlocal
chcp 65001 >nul
set "PYTHONUTF8=1"
cd /d "%~dp0.."
title Crypto Signal Agent - setup
echo ==========================================================
echo   Crypto Signal Agent - live watcher setup (Windows)
echo   Guide: docs\WINDOWS_WATCHER.md
echo ==========================================================
echo.

echo [1/5] Looking for Python 3.10 or newer...
set "PY="
py -3 -c "import sys; sys.exit(0 if sys.version_info >= (3, 10) else 1)" >nul 2>nul && set "PY=py -3"
if not defined PY python -c "import sys; sys.exit(0 if sys.version_info >= (3, 10) else 1)" >nul 2>nul && set "PY=python"
if not defined PY (
  echo Python is not installed yet. Installing it now with winget - say Yes if Windows asks...
  winget install -e --id Python.Python.3.12 --accept-package-agreements --accept-source-agreements
  echo.
  echo ----------------------------------------------------------
  echo  Python was installed. CLOSE this window, then double-click
  echo  1_setup.bat again to continue.
  echo  If it failed: install Python from https://www.python.org/downloads/
  echo  and tick "Add python.exe to PATH" on the first screen.
  echo ----------------------------------------------------------
  pause
  exit /b 1
)
echo       found: %PY%

echo.
echo [2/5] Installing the agent's Python packages (2-5 minutes the first time)...
if not exist ".venv\Scripts\python.exe" %PY% -m venv .venv
if not exist ".venv\Scripts\python.exe" (
  echo Could not create the Python environment. See docs\WINDOWS_WATCHER.md - "Problems".
  pause
  exit /b 1
)
".venv\Scripts\python.exe" -m pip install -q --upgrade pip
".venv\Scripts\python.exe" -m pip install -q -r requirements.txt
if errorlevel 1 (
  echo Installing the packages failed - check the internet connection and run 1_setup.bat again.
  pause
  exit /b 1
)
echo       done.

echo.
echo [3/5] Telegram...
".venv\Scripts\python.exe" live_watcher.py --test-telegram >nul 2>nul
if errorlevel 1 (
  ".venv\Scripts\python.exe" live_watcher.py --setup-telegram
  if errorlevel 1 (
    echo Telegram is not set up yet - run 1_setup.bat again when you are ready.
    pause
    exit /b 1
  )
) else (
  echo       already working - a test message was just sent to Telegram.
)

echo.
echo [4/5] Keep the PC awake while it is plugged in (needed for alerts day and night).
choice /C YN /M "      Set sleep to Never when plugged in"
if not errorlevel 2 (
  powercfg /change standby-timeout-ac 0
  powercfg /change hibernate-timeout-ac 0
  echo       done - the screen may still turn off, that is fine.
)

echo.
echo [5/5] Start the watcher by itself every time you sign in to Windows.
choice /C YN /M "      Start automatically with Windows"
if not errorlevel 2 (
  > "%APPDATA%\Microsoft\Windows\Start Menu\Programs\Startup\CryptoWatcher.bat" echo @start "Crypto Watcher" /min "%~dp0run_watcher.bat"
  echo       done - remove it any time with windows\5_remove_autostart.bat
)

echo.
".venv\Scripts\python.exe" live_watcher.py --sync
echo.
echo ==========================================================
echo   Setup complete.
echo ==========================================================
choice /C YN /M "Start the watcher now"
if not errorlevel 2 start "Crypto Watcher" /min "%~dp0run_watcher.bat"
echo.
echo You can close this window.
pause
