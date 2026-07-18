#!/bin/bash
export GOOGLE_APPLICATION_CREDENTIALS=/home/holisticjson/gcp-sa-key.json
export GOOGLE_CLOUD_PROJECT=holistic-broker
export PATH="/home/holisticjson/.hermes/node/bin:$PATH"
pkill -9 -f litellm || true
pkill -9 uvx || true
pm2 restart litellm
pm2 save
echo "DONE"
