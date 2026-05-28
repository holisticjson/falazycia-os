import os
import sys
import re
from youtube_transcript_api import YouTubeTranscriptApi
import google.generativeai as genai
from datetime import datetime

# KONFIGURACJA API - TUTAJ MUSISZ WPISAC SWOJ KLUCZ GEMINI API!
GEMINI_API_KEY = "WPISZ_TUTAJ_SWOJ_KLUCZ_API"

# Upewnij sie, ze folder istnieje
OUTPUT_DIR = r"c:\Aplikacje MVP\Holistic Jason\Baza_Wiedzy\Kurs_Google"
os.makedirs(OUTPUT_DIR, exist_ok=True)

def get_video_id(url):
    """Wyciaga ID filmu z linku YouTube"""
    patterns = [
        r'(?:https?:\/\/)?(?:www\.)?youtube\.com\/watch\?v=([^&]+)',
        r'(?:https?:\/\/)?youtu\.be\/([^?]+)',
        r'(?:https?:\/\/)?(?:www\.)?youtube\.com\/embed\/([^?]+)'
    ]
    for pattern in patterns:
        match = re.search(pattern, url)
        if match:
            return match.group(1)
    return None

def get_transcript(video_id):
    """Pobiera transkrypcje z YT w jezyku polskim"""
    print("⏳ Pobieranie transkrypcji z YouTube...")
    try:
        # Pobiera polska transkrypcje
        transcript_list = YouTubeTranscriptApi.get_transcript(video_id, languages=['pl'])
        text = " ".join([t['text'] for t in transcript_list])
        print("✅ Transkrypcja pobrana pomyślnie!")
        return text
    except Exception as e:
        print(f"❌ Błąd pobierania transkrypcji: {e}")
        print("Upewnij się, że film posiada napisy (nawet wygenerowane automatycznie).")
        return None

def generate_content(transcript):
    """Wysyła transkrypcje do Gemini i generuje raport"""
    print("⏳ Analiza przez Gemini 1.5 Pro (tworzenie notatki, bloga i social media)...")
    genai.configure(api_key=GEMINI_API_KEY)
    
    # Używamy modelu 1.5 Pro, ktory swietnie radzi sobie z duzym tekstem
    model = genai.GenerativeModel('gemini-1.5-pro')
    
    prompt = f"""
Jesteś moim Głównym Architektem Systemów (Holistic Jason). Przeanalizuj poniższą transkrypcję wideo i wygeneruj dla mnie potrójny raport biznesowy w języku polskim.

Wyjście musi składać się dokładnie z tych 3 sekcji:

### CZĘŚĆ 1: MOJA NOTATKA BIZNESOWA (Baza Wiedzy)
Wypunktuj esencję materiału:
- Główne pojęcie / Narzędzie (co to jest?)
- Jaki problem rozwiązuje w firmie?
- Konkretne biznesowe zastosowanie (krok po kroku).
- Ograniczenia / na co uważać.

### CZĘŚĆ 2: ARTYKUŁ SEO NA BLOGA
Napisz krótki, ekspercki wpis na mojego bloga (Holistic Jason). 
- Zastosuj ton Architekta Systemów (zwracaj się do przedsiębiorców, którym "system przecieka", ton mentorski, techniczny ale ludzki).
- Użyj formatowania Markdown (nagłówki H2, H3, pogrubienia).
- Dodaj krótkie wezwanie do działania (CTA) na koniec – zachęta do audytu automatyzacji.

### CZĘŚĆ 3: KONTENT NA SOCIAL MEDIA
Przerób tę wiedzę na formaty SM:
1. POST NA LINKEDIN: Twardy, ekspercki format. Zacznij od mocnego faktu, wylistuj 3 korzyści, zakończ pytaniem otwartym.
2. SKRYPT NA ROLKĘ (TikTok/IG Reels):
   - Hook (Sekunda 0-3): [Mocne zdanie przykuwające uwagę]
   - Treść (Sekunda 3-30): Szybkie wyjaśnienie jak to działa.
   - Call to Action: [Co mają kliknąć/zrobić].

--- TRANSKRYPCJA WIDEO ---
{transcript}
"""
    try:
        response = model.generate_content(prompt)
        print("✅ Analiza zakończona sukcesem!")
        return response.text
    except Exception as e:
        print(f"❌ Błąd podczas generowania przez API: {e}")
        return None

def save_to_file(content, video_id):
    """Zapisuje raport na dysk"""
    timestamp = datetime.now().strftime("%Y%m%d_%H%M%S")
    filename = f"Raport_YT_{video_id}_{timestamp}.md"
    filepath = os.path.join(OUTPUT_DIR, filename)
    
    with open(filepath, 'w', encoding='utf-8') as f:
        f.write(content)
        
    print(f"🎉 GOTOWE! Plik zapisany pomyślnie w:")
    print(f"📂 {filepath}")

def main():
    print("="*50)
    print("🤖 HOLISTIC YOUTUBE PROCESSOR")
    print("="*50)
    
    if GEMINI_API_KEY == "WPISZ_TUTAJ_SWOJ_KLUCZ_API":
        print("❌ ZATRZYMANO: Musisz podać swój klucz Gemini API w pliku yt_processor.py w linii 8!")
        return

    url = input("\n🔗 Wklej link do filmu na YouTube: ")
    
    video_id = get_video_id(url)
    if not video_id:
        print("❌ Nieprawidłowy link YouTube.")
        return
        
    transcript = get_transcript(video_id)
    if transcript:
        content = generate_content(transcript)
        if content:
            save_to_file(content, video_id)

if __name__ == "__main__":
    main()
