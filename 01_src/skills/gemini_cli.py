"""
🧠 Gemini CLI Companion v1.0 — Holistic Architect Edition
Natywne wsparcie dla Vertex AI (GCP) i Bazy Wiedzy "Umiejętności Jutra".
"""
import os
import sys
import argparse
from pathlib import Path
from google import genai
from google.genai import types

import io
sys.stdout = io.TextIOWrapper(sys.stdout.buffer, encoding='utf-8', errors='replace')

# Poświadczenia
SA_KEY_PATH = r"c:\Aplikacje MVP\Holistic Jason\01_src\config\holistic-dashboard-dev-dea2c872139e.json"

if os.path.exists(SA_KEY_PATH):
    os.environ["GOOGLE_APPLICATION_CREDENTIALS"] = SA_KEY_PATH
else:
    # Fallback: Jeśli plik klucza nie istnieje, google-genai SDK spróbuje użyć 
    # Application Default Credentials (ADC) np. z lokalnego logowania `gcloud auth application-default login`
    print("💡 [GCP Auth] Brak lokalnego pliku klucza SA w domyślnej lokalizacji. Używam domyślnych poświadczeń systemu.")

def get_client():
    try:
        return genai.Client(
            vertexai=True,
            project="holistic-dashboard-dev",
            location="us-central1"
        )
    except Exception as e:
        print(f"\n❌ Błąd autoryzacji Google Cloud Platform: {e}")
        print("💡 Aby rozwiązać ten problem na stałe, uruchom skrypt:")
        print("   powershell -File \".\\auth_gcp_permanent.ps1\"\n")
        sys.exit(1)

def chat(prompt, model="gemini-2.5-flash", context_path=None):
    client = get_client()

    
    system_instruction = "Jesteś asystentem 'Holistic Architect'. Pomagasz w automatyzacji, marketingu i zarządzaniu wiedzą."
    
    context_text = ""
    if context_path:
        p = Path(context_path)
        if p.exists():
            context_text = f"\n\nKONTEKST Z PLIKU ({p.name}):\n{p.read_text(encoding='utf-8')}"
    
    full_prompt = f"{prompt}{context_text}"
    
    print(f"🤖 [Gemini {model}] Thinking...")
    
    try:
        response = client.models.generate_content(
            model=model,
            contents=full_prompt,
            config=types.GenerateContentConfig(
                system_instruction=system_instruction,
                temperature=0.7
            )
        )
        return response.text
    except Exception as e:
        return f"❌ Błąd: {str(e)}"

def main():
    parser = argparse.ArgumentParser(description="Holistic Gemini CLI")
    parser.add_argument("prompt", help="Twoje zapytanie do AI", nargs="?")
    parser.add_argument("--model", default="gemini-2.5-flash", help="Model (flash/pro)")
    parser.add_argument("--file", help="Ścieżka do pliku z kontekstem")
    parser.add_argument("--interactive", action="store_true", help="Tryb czatu")
    
    args = parser.parse_args()
    
    if args.interactive:
        print("进入 [Holistic Gemini Interactive Mode]. Napisz 'exit' aby wyjść.")
        while True:
            user_input = input("👤 Ty: ")
            if user_input.lower() in ["exit", "quit"]:
                break
            response = chat(user_input, args.model, args.file)
            print(f"\n{response}\n")
    elif args.prompt:
        response = chat(args.prompt, args.model, args.file)
        print(response)
    else:
        parser.print_help()

if __name__ == "__main__":
    main()
