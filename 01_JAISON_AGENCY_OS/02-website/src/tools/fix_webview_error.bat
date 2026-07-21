@echo off
title Naprawa Webview Antigravity - Holistic Jason
echo ====================================================================
echo 🛠️  NAPRAWA BLEDU WEBVIEW W EDYTORZE ANTIGRAVITY (SERVICE WORKER)
echo ====================================================================
echo.
echo Krok 1: Zamykanie aktywnych procesow edytora Antigravity...
taskkill /f /im Antigravity.exe >nul 2>&1
timeout /t 2 /nobreak >nul

echo Krok 2: Czyszczenie uszkodzonej pamieci podrecznej i bazy Service Worker...
del /q /f /s "%APPDATA%\Antigravity\Service Worker\*" >nul 2>&1
rmdir /q /s "%APPDATA%\Antigravity\Service Worker\Database" >nul 2>&1
rmdir /q /s "%APPDATA%\Antigravity\Service Worker\ScriptCache" >nul 2>&1

del /q /f /s "%APPDATA%\Antigravity\Cache\*" >nul 2>&1
del /q /f /s "%APPDATA%\Antigravity\GPUCache\*" >nul 2>&1
del /q /f /s "%APPDATA%\Antigravity\Code Cache\*" >nul 2>&1

echo Krok 3: Czyszczenie sesji i danych tymczasowych...
rmdir /q /s "%APPDATA%\Antigravity\Session Storage" >nul 2>&1

echo.
echo ====================================================================
echo ✅ Gotowe! Uszkodzone pliki pamieci podrecznej zostaly usuniete.
echo Edytor Antigravity uruchomi sie ponownie za chwile...
echo ====================================================================
echo.

:: Uruchomienie Antigravity ponownie z wylaczona akceleracja sprzetowa
start "" "%USERPROFILE%\AppData\Local\Programs\Antigravity\Antigravity.exe" --disable-gpu

timeout /t 3 >nul
exit
