FROM python:3.12-slim

WORKDIR /app

# Instalacja zależności systemowych (build-essential, curl dla healthcheck, oraz ffmpeg dla MoviePy)
RUN apt-get update && apt-get install -y --no-install-recommends \
    build-essential \
    curl \
    ffmpeg \
    && rm -rf /var/lib/apt/lists/*

# Instalacja zależności Python
COPY requirements.txt .
RUN pip install --no-cache-dir -r requirements.txt

# Kopiowanie plików aplikacji do kontenera z nowego katalogu 02-os-jaison
COPY 02-os-jaison/app.py .
COPY 02-os-jaison/mindmap_visualizer.html .
COPY 02-os-jaison/webhook_api.py .
COPY .streamlit/ .streamlit/
COPY 02-os-jaison/src/ 01_src/
COPY 02-os-jaison/src/ src/

# Utworzenie folderów na dane
RUN mkdir -p /app/reports /app/generated_media /app/clients /app/influencers

# Port Cloud Run (domyślnie 8080)
EXPOSE 8080

# Healthcheck
HEALTHCHECK CMD curl --fail http://localhost:8080/_stcore/health || exit 1

# Uruchom Streamlit na porcie Cloud Run z app.py jako punktem wejścia
ENTRYPOINT ["streamlit", "run", "app.py", \
    "--server.port=8080", \
    "--server.address=0.0.0.0", \
    "--server.headless=true", \
    "--browser.gatherUsageStats=false"]
