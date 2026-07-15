#!/bin/bash

# Setup Script for 'hermes-broker-core' VPS VM
# Target OS: Ubuntu 22.04 LTS
# Specs: e2-standard-2 (8GB RAM, 50GB SSD)
# Brand: Holistyczny Broker (REVOLTO GROUP)

set -e

# Kolory dla ładnego outputu
RED='\033[0;31m'
GREEN='\033[0;32m'
YELLOW='\033[1;33m'
CYAN='\033[0;36m'
NC='\033[0;41m' # No Color
RESET='\033[0m'

echo -e "${CYAN}====================================================================${RESET}"
echo -e "${CYAN}   HOLISTYCZNY BROKER - INICJALIZACJA VPS (e2-standard-2)${RESET}"
echo -e "${CYAN}====================================================================${RESET}"

# 1. Sprawdzenie uprawnień root
if [ "$EUID" -ne 0 ]; then
  echo -e "${RED}[BŁĄD] Uruchom ten skrypt jako root (użyj: sudo ./setup_vps.sh)${RESET}"
  exit 1
fi

# 2. Aktualizacja pakietów systemowych
echo -e "\n${CYAN}[1/8] Aktualizacja pakietów systemowych Ubuntu...${RESET}"
apt-get update && apt-get upgrade -y

# 3. Instalacja podstawowych paczek narzędziowych
echo -e "\n${CYAN}[2/8] Instalacja podstawowych narzędzi systemowych...${RESET}"
apt-get install -y curl wget git unzip build-essential ufw nginx python3-pip python3-venv certbot python3-certbot-nginx

# 4. Konfiguracja Firewalla (UFW)
echo -e "\n${CYAN}[3/8] Konfiguracja zabezpieczeń sieciowych (UFW)...${RESET}"
ufw default deny incoming
ufw default allow outgoing
ufw allow 22/tcp comment 'SSH Secure'
ufw allow 80/tcp comment 'HTTP'
ufw allow 443/tcp comment 'HTTPS'
echo "y" | ufw enable
ufw status verbose

# 5. Instalacja Docker i Docker Compose
echo -e "\n${CYAN}[4/8] Instalacja silnika Docker i Docker Compose...${RESET}"
if ! [ -x "$(command -v docker)" ]; then
  curl -fsSL https://get.docker.com -o get-docker.sh
  sh get-docker.sh
  usermod -aG docker $USER || true
  rm get-docker.sh
  echo -e "${GREEN}[SUKCES] Docker został zainstalowany!${RESET}"
else
  echo -e "${YELLOW}Docker jest już zainstalowany w systemie.${RESET}"
fi

# 6. Konfiguracja i generowanie .env dla n8n
echo -e "\n${CYAN}[5/8] Konfiguracja plików konfiguracyjnych n8n...${RESET}"
mkdir -p /opt/n8n-broker
cp docker-compose.yml /opt/n8n-broker/docker-compose.yml

# Generowanie bezpiecznego hasła dla bazy danych n8n
SECURE_PASSWORD=$(openssl rand -base64 18 | tr -dc 'a-zA-Z0-9' | head -c 18)

cat <<EOF > /opt/n8n-broker/.env
DB_USER=n8n_admin
DB_PASSWORD=$SECURE_PASSWORD
DB_NAME=n8n_database
N8N_HOST=n8n.holistycznybroker.pl
EOF

echo -e "${GREEN}[SUKCES] Wygenerowano bezpieczne pliki .env w /opt/n8n-broker/${RESET}"

# 7. Konfiguracja Nginx Reverse Proxy dla n8n
echo -e "\n${CYAN}[6/8] Konfiguracja serwera Nginx jako Reverse Proxy...${RESET}"
NGINX_CONF="/etc/nginx/sites-available/n8n.holistycznybroker.pl"

cat <<EOF > $NGINX_CONF
server {
    listen 80;
    server_name n8n.holistycznybroker.pl;

    location / {
        proxy_pass http://127.0.0.1:5678;
        proxy_set_header Host \$host;
        proxy_set_header X-Real-IP \$remote_addr;
        proxy_set_header X-Forwarded-For \$proxy_add_x_forwarded_for;
        proxy_set_header X-Forwarded-Proto \$scheme;
        
        # Obsługa WebSockets (kluczowa dla działania interfejsu n8n)
        proxy_http_version 1.1;
        proxy_set_header Upgrade \$http_upgrade;
        proxy_set_header Connection "Upgrade";
        proxy_read_timeout 86400;
    }
}
EOF

ln -sf $NGINX_CONF /etc/nginx/sites-enabled/
rm -f /etc/nginx/sites-enabled/default || true

nginx -t
systemctl restart nginx
echo -e "${GREEN}[SUKCES] Nginx został skonfigurowany pod n8n.holistycznybroker.pl!${RESET}"

# 8. Uruchomienie kontenerów n8n & PostgreSQL
echo -e "\n${CYAN}[7/8] Uruchamianie n8n w kontenerach Docker w tle...${RESET}"
cd /opt/n8n-broker
docker compose up -d

echo -e "${GREEN}[SUKCES] n8n wystartował pomyślnie!${RESET}"

# 9. Podsumowanie i instrukcja Certbota
echo -e "\n${GREEN}====================================================================${RESET}"
echo -e "${GREEN}   INSTALACJA ZAKOŃCZONA SUKCESEM! TWÓJ VPS JEST GOTOWY!            ${RESET}"
echo -e "${GREEN}====================================================================${RESET}"
echo -e "\n${YELLOW}CO NALEŻY TERAZ ZROBIĆ:${RESET}"
echo -e "1. Skieruj u swojego rejestratora DNS rekord A dla ${CYAN}n8n.holistycznybroker.pl${RESET} na IP tego serwera."
echo -e "2. Po propagacji DNS, uruchom Certbota, aby wdrożyć darmowy certyfikat SSL Let's Encrypt:"
echo -e "   ${CYAN}sudo certbot --nginx -d n8n.holistycznybroker.pl${RESET}"
echo -e "3. Wejdź na: ${GREEN}https://n8n.holistycznybroker.pl${RESET} i stwórz swoje pierwsze konto administratora n8n!"
echo -e "4. Skopiuj wygenerowany webhook produkcyjny i ustaw go w Cloud Run jako ${CYAN}LEAD_WEBHOOK_URL${RESET}."
echo -e "\n${CYAN}Życzymy udanych automatyzacji! - Zespół Antigravity AI${RESET}"

chmod +x /opt/n8n-broker/setup_vps.sh || true

