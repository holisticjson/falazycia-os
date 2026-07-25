@echo off
title Jaison OS — POBIERZ NAJNOWSZE PLIKI Z GITHUBA
cd /d "C:\Aplikacje MVP"
echo ========================================================
echo   Pobieranie i synchronizacja najnowszego stanu z GitHub
echo ========================================================
powershell.exe -ExecutionPolicy Bypass -File "C:\Aplikacje MVP\git_sync.ps1"
echo.
echo ========================================================
echo   Wymuszanie pobrania plikow (Git Fetch & Reset)...
echo ========================================================
git fetch origin main
git pull --rebase origin main
echo.
echo === POBIERANIE ZAKONCZONE SUKCESEM! ===
pause
