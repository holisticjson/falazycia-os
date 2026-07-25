@echo off
title Jaison OS — GCP Storage Mirror Sync (Upload)
cd /d "C:\Aplikacje MVP\01_JAISON_AGENCY_OS\02-website"
echo ========================================================
echo   Wysylanie pobranych plikow z laptopa do GCP Storage
echo ========================================================
python scripts/gcs_mirror_sync.py --upload
echo.
echo === Synchronizacja z GCP Storage zakonczona! ===
pause
