#!/bin/bash
export PATH=/home/holisticjson/.hermes/node/bin:$PATH

echo "=== 1. Kill everything ==="
pm2 delete all || true
pkill -9 -f litellm || true
pkill -9 -f 'hermes gateway' || true
rm -f /home/holisticjson/.hermes/gateway.pid

echo "=== 2. Create PM2 startup script for LiteLLM ==="
cat << 'EOF' > /home/holisticjson/run_litellm.sh
#!/bin/bash
cd /home/holisticjson/litellm
source venv/bin/activate
set -a; source .env; set +a
litellm --config config.yaml --port 4000
EOF
chmod +x /home/holisticjson/run_litellm.sh

echo "=== 3. Create PM2 startup script for Gateway ==="
cat << 'EOF' > /home/holisticjson/run_gateway.sh
#!/bin/bash
cd /home/holisticjson/hermes-agent
source .venv/bin/activate

# --- HOTFIX: Wczytanie kluczy API dla Telegram Bota ---
if [ -f /home/holisticjson/.env ]; then
  set -a; source /home/holisticjson/.env; set +a
fi
if [ -f /home/holisticjson/litellm.env ]; then
  set -a; source /home/holisticjson/litellm.env; set +a
fi
# --------------------------------------------------------

export GATEWAY_ALLOW_ALL_USERS=true
export API_SERVER_ENABLED=true

# Usuń stary plik blokady, jeśli istnieje
rm -f /home/holisticjson/.hermes/gateway.pid

# Uruchom BEZ opcji replace
hermes gateway run
EOF
chmod +x /home/holisticjson/run_gateway.sh

echo "=== 3.5. Create PM2 startup script for Brain Dump API ==="
cat << 'EOF' > /home/holisticjson/run_brain_dump.sh
#!/bin/bash
cd /home/holisticjson/
source .venv/bin/activate
python brain_dump_api.py
EOF
chmod +x /home/holisticjson/run_brain_dump.sh

echo "=== 4. Start all via PM2 ==="
pm2 start /home/holisticjson/run_litellm.sh --name litellm
pm2 start /home/holisticjson/run_gateway.sh --name hermes-gateway
pm2 start /home/holisticjson/run_brain_dump.sh --name brain-dump-api

cd /home/holisticjson/hermes-studio
pm2 start "npm run start" --name hermes-studio || pm2 start node --name hermes-studio -- server-entry.js

pm2 save
sleep 5
ss -tlnp | grep -E '4000|8642|3002'
