import streamlit as st
import boto3
import json
import os
from pathlib import Path
from dotenv import load_dotenv

def get_bedrock_client():
    load_dotenv()
    aws_access_key = os.getenv("AWS_ACCESS_KEY_ID")
    aws_secret_key = os.getenv("AWS_SECRET_ACCESS_KEY")
    aws_region = os.getenv("AWS_REGION", "us-east-1")
    
    # Usuwamy SSLKEYLOGFILE z env jeśli sprawia problemy z antywirusem (np. AVG)
    if "SSLKEYLOGFILE" in os.environ:
        del os.environ["SSLKEYLOGFILE"]

    if not aws_access_key or not aws_secret_key:
        return None, "Brak kluczy AWS w pliku .env"

    try:
        client = boto3.client(
            'bedrock-runtime',
            region_name=aws_region,
            aws_access_key_id=aws_access_key,
            aws_secret_access_key=aws_secret_key
        )
        return client, "Połączono z AWS Bedrock"
    except Exception as e:
        return None, f"Błąd połączenia: {e}"

def invoke_claude(client, prompt, system_prompt="", model_id="anthropic.claude-3-5-sonnet-20240620-v1:0"):
    # Fallback/default na Claude 3.5 Sonnet w eu-central-1
    try:
        body = {
            "anthropic_version": "bedrock-2023-05-31",
            "max_tokens": 8000,
            "temperature": 0.2,
            "system": system_prompt,
            "messages": [
                {"role": "user", "content": prompt}
            ]
        }
        
        response = client.invoke_model(
            modelId=model_id,
            body=json.dumps(body)
        )
        response_body = json.loads(response.get('body').read())
        return response_body['content'][0]['text']
    except Exception as e:
        return f"Błąd wywołania modelu: {e}"

def render_funnel_hacker():
    st.title("🏴‍☠️ Funnel Hacker (Reverse Engineering)")
    st.markdown("Automatyczna inżynieria wsteczna lejków sprzedażowych z użyciem AWS Bedrock (Claude 3.5+).")

    client, status = get_bedrock_client()
    
    if client:
        st.success(f"✅ {status} (Region: {os.getenv('AWS_REGION', 'us-east-1')})")
    else:
        st.error(f"❌ {status}")
        st.stop()

    tab1, tab2 = st.tabs(["1. Konsola Testowa AWS", "2. Ekstrakcja i Klonowanie Lejka"])

    with tab1:
        st.subheader("Test połączenia z modelem Claude")
        # Lista najpopularniejszych ID Modeli On-Demand w AWS Bedrock (Stan na Maj 2026).
        # Uwaga: Niektóre modele mogą wymagać zmiany regionu w pliku .env (us-east-1 to N. Virginia)
        model_selector = st.selectbox("Wybierz model AWS Bedrock:", [
            "anthropic.claude-sonnet-4-6",    # Claude Sonnet 4.6 (zrzut ekranu AWS - Maj 2026)
            "anthropic.claude-haiku-4-5-20251001-v1:0",      # Claude Haiku 4.5
            "anthropic.claude-opus-4-7",      # Najpotężniejszy model: Claude Opus 4.7
            "anthropic.claude-3-5-sonnet-20241022-v2:0",   # Starszy 3.5 Sonnet v2
            "us.anthropic.claude-3-5-sonnet-20241022-v2:0",# Cross-Region US 3.5 Sonnet
            "eu.anthropic.claude-3-5-sonnet-20240620-v1:0" # Cross-Region EU 3.5 Sonnet
        ])
        
        test_prompt = st.text_area("Twój prompt do AWS Bedrock:", value="Napisz krótki wierszyk o lejku sprzedażowym, który konwertuje.")
        
        if st.button("Wyślij test do Claude"):
            with st.spinner("Oczekiwanie na odpowiedź z AWS..."):
                odp = invoke_claude(client, test_prompt, model_id=model_selector)
                st.write(odp)

    with tab2:
        st.subheader("Klonowanie Lejka (Wkrótce)")
        st.info("Tutaj zostanie zintegrowany Subagent Przeglądarki do pobierania kodu i przekazywania go do AWS.")
        target_url = st.text_input("URL lejka do sklonowania:")
        if st.button("Rozpocznij Ekstrakcję (Beta)", disabled=True):
            st.write("Moduł w przygotowaniu...")

if __name__ == "__main__":
    render_funnel_hacker()
