@echo off
cd /d "%~dp0.."
type nul > STOP_WATCHER
powershell -NoProfile -Command "Get-CimInstance Win32_Process | Where-Object { $_.Name -like 'python*.exe' -and $_.CommandLine -like '*live_watcher.py*' } | ForEach-Object { Stop-Process -Id $_.ProcessId -Force }"
echo The watcher is stopped. Start it again with 2_start_watcher.bat.
timeout /t 8 >nul
