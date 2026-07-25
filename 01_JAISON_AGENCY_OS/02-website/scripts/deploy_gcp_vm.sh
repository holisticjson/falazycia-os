#!/bin/bash
# 🚀 GCP VM PRODUCTION DEPLOYMENT SCRIPT (os.jaison.pl)

echo "=== Rozpoczęcie Wdrożenia Produkcyjnego Jaison OS na GCP VM ==="

# 1. Pobranie najnowszego kodu z GitHub
echo "[1/4] Pobieranie kodu z GitHub..."
cd /home/tomasz/holistic-jason || cd /app || exit 1
git pull origin main

# 2. Instalacja zależności Python
echo "[2/4] Instalacja zależności Python..."
pip install --upgrade pip
pip install -r 02-website/requirements.txt discord.py requests google-cloud-storage python-dotenv

# 3. Uruchomienie Bota Discorda w tle przez PM2
echo "[3/4] Uruchamianie Jaison OS Bot (Discord) w PM2..."
pm2 stop jaison-discord-bot || true
pm2 delete jaison-discord-bot || true
pm2 start 01_JAISON_AGENCY_OS/04-assets/discord_bot.py --name "jaison-discord-bot" --interpreter python3

# 4. Uruchomienie Streamlit Dashboardu w PM2
echo "[4/4] Uruchamianie Streamlit Dashboard na portach produkcyjnych..."
pm2 stop jaison-dashboard || true
pm2 delete jaison-dashboard || true
pm2 start "streamlit run 02-website/app.py --server.port 8501 --server.address 0.0.0.0" --name "jaison-dashboard"

# Zapamiętanie procesów PM2
pm2 save

echo "=== 🎉 DEPLOY PRODUKCYJNY ZAKOŃCZONY SUKCESEM! ==="
