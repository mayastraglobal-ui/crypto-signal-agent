@echo off
del "%APPDATA%\Microsoft\Windows\Start Menu\Programs\Startup\CryptoWatcher.bat" 2>nul
echo The watcher no longer starts by itself with Windows. (Start it with 2_start_watcher.bat.)
timeout /t 8 >nul
