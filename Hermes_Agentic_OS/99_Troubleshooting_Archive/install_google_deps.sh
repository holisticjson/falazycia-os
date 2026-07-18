#!/bin/bash
set -e

# Znajdz aktywne archiwum uv gdzie dziala litellm
LITELLM_ARCHIVE=$(ls -d /home/holisticjson/.cache/uv/archive-v0/*/bin/litellm 2>/dev/null | head -1 | sed 's|/bin/litellm||')

if [ -z "$LITELLM_ARCHIVE" ]; then
    echo "[ERROR] Nie mozna znalezc archiwum litellm!"
    exit 1
fi

PYTHON="$LITELLM_ARCHIVE/bin/python"
echo "[INFO] Archiwum LiteLLM: $LITELLM_ARCHIVE"
echo "[INFO] Python: $PYTHON"

# Sprawdz czy google juz jest
$PYTHON -c "import google.auth" 2>/dev/null && echo "[OK] google.auth juz zainstalowany" && exit 0

echo "[ACTION] Instaluje google-cloud-aiplatform do archiwum litellm..."
$PYTHON -m pip install \
    google-cloud-aiplatform \
    google-auth \
    google-cloud-storage \
    --quiet --no-warn-script-location

echo "[VERIFY]"
$PYTHON -c "import google.auth; import google.cloud.aiplatform; print('[SUCCESS] google-cloud-aiplatform zainstalowany!')"

echo "[ACTION] Weryfikacja polaczenia z Vertex AI..."
$PYTHON -c "
import os
os.environ['GOOGLE_APPLICATION_CREDENTIALS'] = '/home/holisticjson/gcp-sa-key.json'
import google.auth
creds, project = google.auth.default()
print(f'[SUCCESS] Credentials OK | Project: {project}')
"

echo "[DONE] Gotowe!"
