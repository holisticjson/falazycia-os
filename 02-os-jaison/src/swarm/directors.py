import os
import requests
import json
from dotenv import load_dotenv
from .workers import generate_video_reel, build_funnel_systeme_io, seo_analysis

load_dotenv()

OPENROUTER_API_KEY = os.getenv("OPENROUTER_API_KEY")

def call_llm(prompt: str, role_system_prompt: str) -> str:
    """Proste wywołanie modelu językowego przez OpenRouter (Gemini lub Claude)"""
    if not OPENROUTER_API_KEY:
        return f"[MOCK LLM] Brak klucza OPENROUTER_API_KEY. Odpowiedź dla: {prompt}"
        
    url = "https://openrouter.ai/api/v1/chat/completions"
    headers = {
        "Authorization": f"Bearer {OPENROUTER_API_KEY}",
        "Content-Type": "application/json"
    }
    data = {
        "model": "google/gemini-2.5-pro", # Używamy Gemini 2.5 Pro via OpenRouter
        "messages": [
            {"role": "system", "content": role_system_prompt},
            {"role": "user", "content": prompt}
        ]
    }
    
    try:
        import urllib3
        urllib3.disable_warnings(urllib3.exceptions.InsecureRequestWarning)
        response = requests.post(url, headers=headers, json=data, verify=False)
        response.raise_for_status()
        return response.json()["choices"][0]["message"]["content"]
    except Exception as e:
        return f"[BŁĄD LLM]: Nie udało się połączyć z API: {e}"

def run_ceo_agent(task_description: str) -> str:
    """CEO AI rozbija główne zadanie na podzadania dla specjalistów."""
    system_prompt = (
        "Jesteś CEO AI w agencji Holistic Jason. Otrzymujesz ogólne polecenie od właściciela (Tomasza). "
        "Twoim zadaniem jest rozbicie tego polecenia na 1-3 mniejsze zadania dla Twoich dyrektorów "
        "(głównie dla CMO AI, który zarządza Lejkami i Wideo). "
        "Bądź ekstremalnie zwięzły. Zwróć tylko listę kroków."
    )
    return call_llm(task_description, system_prompt)

def run_cmo_agent(ceo_plan: str) -> dict:
    """CMO AI interpretuje plan CEO i uruchamia odpowiednie narzędzia (Workers)."""
    system_prompt = (
        "Jesteś CMO AI. Patrząc na plan CEO, decydujesz, jakich specjalistów użyć. "
        "Jeśli plan wymaga wideo, użyj Video Makera. Jeśli lejka, użyj Funnel Buildera. "
        "Zwróć odpowiedź WYŁĄCZNIE w formacie JSON: {'tools_to_run': ['video', 'funnel', 'seo'], 'copywriting': 'Treść...'}"
    )
    
    # Próbujemy uzyskać strukturalną odpowiedź od LLM
    llm_response = call_llm(f"Plan CEO: {ceo_plan}. Zwróć JSON.", system_prompt)
    
    # Fallback / Proste parsowanie w ramach MVP
    tools_to_run = []
    if "video" in llm_response.lower() or "wideo" in ceo_plan.lower() or "rolka" in ceo_plan.lower():
        tools_to_run.append("video")
    if "funnel" in llm_response.lower() or "lejek" in ceo_plan.lower() or "stron" in ceo_plan.lower():
        tools_to_run.append("funnel")
    if "seo" in llm_response.lower() or "seo" in ceo_plan.lower():
        tools_to_run.append("seo")
        
    return {
        "analysis": llm_response,
        "tools_to_run": tools_to_run
    }
