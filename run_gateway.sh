#!/bin/bash
# Skrypt startowy dla hermes gateway
cd /home/holisticjson/hermes-agent
export PATH=/home/holisticjson/.hermes/node/bin:/usr/local/sbin:/usr/local/bin:/usr/sbin:/usr/bin:/sbin:/bin
source .venv/bin/activate
set -a
source .env
set +a
# Uruchom jako gateway (serwer HTTP/API dla Studio i Telegram)
python3.11 hermes gateway
