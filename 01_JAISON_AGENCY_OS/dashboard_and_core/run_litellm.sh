#!/bin/bash
cd /home/holisticjson/litellm
source /home/holisticjson/litellm/venv/bin/activate
# Ladujemy zmienne srodowiskowe
set -a
source .env
set +a
exec litellm --config config.yaml --port 4000
