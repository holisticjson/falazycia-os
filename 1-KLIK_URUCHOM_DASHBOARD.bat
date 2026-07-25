@echo off
title Jaison OS — Streamlit Dashboard Runner (VPN Compatible)
cd /d "C:\Aplikacje MVP\01_JAISON_AGENCY_OS\02-website"
echo ========================================================
echo   Uruchamianie Jaison OS Dashboard (VPN Compatible)
echo ========================================================
python -m streamlit run app.py --server.address 0.0.0.0 --server.port 8501 --browser.gatherUsageStats false
pause
