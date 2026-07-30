FROM python:3.11-slim

WORKDIR /app

# Copy requirements and upgrade pip
COPY 02-website/requirements.txt .
RUN pip install --no-cache-dir --upgrade pip && pip install --no-cache-dir -r requirements.txt

# Copy knowledge base and website files
COPY 04-assets /app/04-assets
COPY 02-website /app/02-website

WORKDIR /app/02-website

ENV PORT=8080
EXPOSE 8080

CMD ["sh", "-c", "streamlit run dashboard.py --server.port=${PORT} --server.address=0.0.0.0 --server.enableCORS=false"]
