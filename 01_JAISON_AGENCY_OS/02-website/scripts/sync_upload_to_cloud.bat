@echo off
title GCS Mirror Sync — Upload to Cloud
cd /d "C:\Aplikacje MVP\01_JAISON_AGENCY_OS\02-website"
echo ========================================================
echo   Wysylanie nowych plikow z tego urzadzenia do GCP Storage
echo ========================================================
python scripts/gcs_mirror_sync.py --upload
echo.
echo === Synchronizacja zakaczona! ===
pause
