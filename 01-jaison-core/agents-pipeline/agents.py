import os
import time
from google import genai
from google.genai import types

def run_agency_pipeline(client_brief: str):
    """
    Uruchamia stanowy łańcuch wieloagentowy (CEO -> CMO -> CPO -> CTO)
    z użyciem oficjalnego, najnowszego Google GenAI Interactions API i modelu gemini-3.5-flash.
    """
    # Sprawdzenie obecności klucza API (zabezpieczenie)
    api_key = os.environ.get("GEMINI_API_KEY")
    if api_key:
        client = genai.Client(api_key=api_key)
    else:
        # Próba inicjalizacji z domyślnego środowiska (np. ADC lub GEMINI_API_KEY w os.environ)
        try:
            client = genai.Client()
        except Exception as e:
            raise ValueError("Brak klucza API dla Gemini. Upewnij się, że plik .env zawiera GEMINI_API_KEY lub że jesteś zalogowany.")

    # Słownik wynikowy dla interfejsu Streamlit
    results = {
        "status": "success",
        "ceo_analysis": "",
        "cmo_strategy": "",
        "cpo_branding": "",
        "cto_prompts": "",
        "execution_time_seconds": 0.0
    }
    
    start_time = time.time()
    
    try:
        # 1. CEO Agent: Analiza briefu i dekompozycja celów
        ceo_instruction = (
            "Jesteś CEO AI Jaison Agency (jaison.pl). Twoim celem jest dekompozycja chaotycznych, "
            "surowych informacji od klienta na czynniki pierwsze. "
            "1. Sklasyfikuj branżę, profil i wyzwania klienta.\n"
            "2. Zdefiniuj 3 mierzalne cele kampanii.\n"
            "3. Pisz zwięźle, w punktach, w profesjonalnym, biznesowym tonie."
        )
        interaction_ceo = client.interactions.create(
            model="gemini-3.5-flash",
            input=f"Oto brief / zmapowane procesy klienta:\n{client_brief}",
            system_instruction=ceo_instruction
        )
        results["ceo_analysis"] = interaction_ceo.output_text
        ceo_id = interaction_ceo.id
        
        # 2. CMO Agent: Strategia marketingowa i harmonogram (Thought Leadership)
        cmo_instruction = (
            "Jesteś CMO AI Jaison Agency (jaison.pl), ekspertem od budowy lejków B2B i e-mail marketingu. "
            "Na podstawie analizy celów CEO przygotuj:\n"
            "1. Propozycję 3 głównych filarów tematycznych (Content Pillars).\n"
            "2. Gotowy, 2-tygodniowy kalendarz postów (tematy, haczyki [Hooks] i sugerowane call-to-action).\n"
            "3. Pisz w duchu 'Thought Leadership' – merytorycznie i bez lania wody."
        )
        interaction_cmo = client.interactions.create(
            model="gemini-3.5-flash",
            input="Zbuduj kompletną strategię marketingową i kalendarz social media na podstawie celów CEO.",
            previous_interaction_id=ceo_id,
            system_instruction=cmo_instruction
        )
        results["cmo_strategy"] = interaction_cmo.output_text
        cmo_id = interaction_cmo.id
        
        # 3. CPO Agent: Wytyczne wizualne i Brand Book
        cpo_instruction = (
            "Jesteś CPO AI Jaison Agency (jaison.pl), dyrektorem artystycznym i strażnikiem visual anchoringu. "
            "Na podstawie strategii marketingowej CMO przygotuj wytyczne wizualne:\n"
            "1. Rekomendację palety kolorystycznej (2-3 luksusowe kolory HEX).\n"
            "2. Wybór par czcionek (np. Outfit, Atkinson, Montserrat) z uzasadnieniem.\n"
            "3. Kompozycję i styl grafik / slajdów karuzeli, aby przyciągały wzrok i zapobiegały paraliżowi kognitywnemu."
        )
        interaction_cpo = client.interactions.create(
            model="gemini-3.5-flash",
            input="Przeanalizuj strategię i stwórz dla tej kampanii wytyczne wizualne i estetyczne.",
            previous_interaction_id=cmo_id,
            system_instruction=cpo_instruction
        )
        results["cpo_branding"] = interaction_cpo.output_text
        cpo_id = interaction_cpo.id
        
        # 4. CTO Agent: Narzędzia, prompty i automatyzacja
        cto_instruction = (
            "Jesteś CTO AI Jaison Agency (jaison.pl), inżynierem technologii i automatyzacji. "
            "Twoim zadaniem jest przełożenie strategii i wytycznych brandingowych na konkretne paczki "
            "dla skryptów generujących:\n"
            "1. Gotowy prompt dla generatora karuzeli Pillow (podział slajdów za pomocą '---').\n"
            "2. Rekomendację lektora Edge-TTS (np. pl-PL-MarekNeural lub pl-PL-ZofiaNeural) i zarys skryptu wideo.\n"
            "3. Sugestie automatyzacji w n8n dla dystrybucji tych materiałów."
        )
        interaction_cto = client.interactions.create(
            model="gemini-3.5-flash",
            input="Przygotuj paczkę promptów konfiguracyjnych i techniczne wytyczne dla generatorów multimedialnych.",
            previous_interaction_id=cpo_id,
            system_instruction=cto_instruction
        )
        results["cto_prompts"] = interaction_cto.output_text
        
    except Exception as e:
        results["status"] = "error"
        results["error_message"] = str(e)
        
    results["execution_time_seconds"] = round(time.time() - start_time, 2)
    return results
