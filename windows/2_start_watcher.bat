@echo off
cd /d "%~dp0.."
start "Crypto Watcher" /min "%~dp0run_watcher.bat"
echo The watcher is starting in its own window (minimized on the taskbar).
echo Telegram says "Live watcher started" within a minute or two.
timeout /t 8 >nul
