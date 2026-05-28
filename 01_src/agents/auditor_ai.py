import sys
import os
import json
from pathlib import Path

# Add root to path
sys.path.append(os.getcwd())

from google import genai
from google.genai import types

# Konfiguracja Google Auth
SA_KEY_PATH = r"c:\Aplikacje MVP\Holistic Jason\holistic-dashboard-dev-dea2c872139e.json"
if os.path.exists(SA_KEY_PATH):
    os.environ["GOOGLE_APPLICATION_CREDENTIALS"] = SA_KEY_PATH

def run_world_class_audit():
    print("[AUDITOR] Inicjalizacja Audytora Swiatowej Klasy (Gemini 2.5 Pro)...")
    
    # ... (kod zbierania kontekstu pozostaje bez zmian) ...
    # 1. Zbieranie kontekstu (kod + pliki stanu)
    files_to_audit = [
        "holistic_ceo.py",
        "skills/shadow_operator.py",
        "ai_influencer.py",
        "market_radar.py",
        "Baza_Wiedzy/ADHD/Stan_Gry_Holistic.md",
        "Baza_Wiedzy/Syntetyczna/Shadow_Operator_Master.md"
    ]
    
    code_context = ""
    for f_path in files_to_audit:
        if os.path.exists(f_path):
            with open(f_path, "r", encoding="utf-8", errors="replace") as f:
                code_context += f"\n\n--- PLIK: {f_path} ---\n{f.read()[:10000]}" 

    audit_prompt = f"""Jesteś światowej klasy ekspertem od orkiestracji agentów AI, systemów SaaS i UX/UI (poziom Mirka Skwarka i najlepszych twórców z USA/EU).
    
    TWOJE ZADANIE: Wykonaj głęboki audyt i research rynkowy dla systemu "Holistic CEO Dashboard".
    
    KONTEKST SYSTEMU (KOD I STRUKTURA):
    {code_context}
    
    ZAKRES AUDYTU:
    1. ANALIZA RYNKOWA (RESEARCH 2026): Przeanalizuj rozwiązania takie jak FunnelStar.io, Localo, GHL oraz trendy w "Autonomous Agents Dashboards".
    2. AUDYT LOGIKI: Czy orkiestracja CEO -> Dyrektorzy jest optymalna? Gdzie są wąskie gardła?
    3. UX/UI & USER FLOW: Czy interfejs "InFlow" jest user-friendly? Czy proces od "Intake" do "Raportu" jest płynny?
    4. ZALECENIA EKSPERCKIE: Co dodać? Jakie "Quick Ideas" (chmurki z podpowiedziami) wdrożyć, aby ułatwić życie użytkownikowi?
    5. INTEGRACJA LOCALO: Jak lepiej zintegrować wiedzę o Local SEO i zarządzaniu wizytówkami (Sebastian/Localo) w Social Plannerze?
    
    OCZEKIWANY REZULTAT: 
    Raport w formacie Markdown zawierający sekcje: [ANALIZA KONKURENCJI], [AUDYT LOGIKI], [REKOMENDACJE UX/UI], [PLAN ROZWOJU (IDEATION)].
    
    Bądź surowy, profesjonalny i dawaj konkretne "actionable steps". Pisz po polsku.
    """
    
    try:
        client = genai.Client(vertexai=True, project="holistic-dashboard-dev", location="us-central1")
        response = client.models.generate_content(
            model='gemini-2.5-pro',
            contents=audit_prompt,
            config=types.GenerateContentConfig(temperature=0.3)
        )
        audit_text = response.text
    except Exception as e:
        audit_text = f"Blad Gemini: {e}"
    
    # 4. Zapisanie raportu
    report_path = Path("Baza_Wiedzy/Raporty/Audit_Swiatowej_Klasy_2026.md")
    report_path.parent.mkdir(parents=True, exist_ok=True)
    
    with open(report_path, "w", encoding="utf-8") as f:
        f.write(audit_text)
        
    print(f"[AUDITOR] Audyt zakonczony. Raport zapisany w: {report_path}")
    return response

if __name__ == "__main__":
    run_world_class_audit()
