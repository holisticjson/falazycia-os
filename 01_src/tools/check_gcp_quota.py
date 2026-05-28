import os
import sys
from google import genai
from google.genai import types

def test_vertex_connection():
    print("========================================")
    print("🔍 AUDYT POŁĄCZENIA Z GOOGLE CLOUD (VERTEX AI)")
    print("========================================\n")

    project = os.environ.get("GCP_PROJECT", "holistic-dashboard-dev")
    location = os.environ.get("GCP_LOCATION", "us-central1")
    sa_path = r"c:\Aplikacje MVP\Holistic Jason\holistic-dashboard-dev-dea2c872139e.json"

    print(f"1. Sprawdzam plik Service Account: {sa_path}")
    if not os.path.exists(sa_path):
        print("❌ BŁĄD: Plik Service Account nie istnieje! Roo Code nie będzie mógł się uwierzytelnić.")
        return
    else:
        print("✅ Plik znaleziony.")

    print("\n2. Konfiguruję środowisko dla Vertex AI...")
    os.environ["GOOGLE_APPLICATION_CREDENTIALS"] = sa_path
    
    try:
        client = genai.Client(vertexai=True, project=project, location=location)
        print("✅ Klient Vertex zainicjowany.")
    except Exception as e:
        print(f"❌ BŁĄD Inicjalizacji: {e}")
        return

    print("\n3. Próba wykonania lekkiego żądania do modelu (gemini-2.5-flash)...")
    try:
        response = client.models.generate_content(
            model='gemini-2.5-flash',
            contents='Powiedz "Ping Vertex OK" jeśli mnie słyszysz.'
        )
        print(f"✅ Odpowiedź z chmury: {response.text.strip()}")
    except Exception as e:
        print(f"❌ BŁĄD API (Quota/Limit lub Brak dostępu): {e}")
        print("\nWSKAZÓWKA DLA ROO CODE:")
        print("Jeśli widzisz tu błąd Quota, to znaczy, że wyczerpałeś limity testowe lub karta nie jest podpięta pod Google Cloud.")

    print("\n4. Próba wykonania żądania do ciężkiego modelu (gemini-2.5-pro)...")
    try:
        response_pro = client.models.generate_content(
            model='gemini-2.5-pro',
            contents='Zrób krótki test - napisz "PRO OK".'
        )
        print(f"✅ Odpowiedź z chmury (PRO): {response_pro.text.strip()}")
    except Exception as e:
        print(f"❌ BŁĄD API PRO (Często limit Throttling 429 lub Empty Response): {e}")
        print("Jeśli Roo Code się tnie, to ten sam błąd występuje u niego.")
        
    print("\n[ZAKOŃCZONO AUDYT]")

if __name__ == "__main__":
    test_vertex_connection()
