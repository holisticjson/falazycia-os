@echo off
title GCS Mirror Sync — Download from Cloud
cd /d "C:\Aplikacje MVP\01_JAISON_AGENCY_OS\02-website"
echo ========================================================
echo   Pobieranie najnowszych plikow z GCP Storage na ten komputer
echo ========================================================
python scripts/gcs_mirror_sync.py --download
echo.
echo === Synchronizacja zakaczona! ===
pause
