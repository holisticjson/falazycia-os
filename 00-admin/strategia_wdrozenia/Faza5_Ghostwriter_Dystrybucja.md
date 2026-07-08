# **Raport Techniczny: Faza 5 – Ghostwriter v2 i Dystrybucja Treści**

Jako Twój inżynier promptów i architekt automatyzacji, przeanalizowałem dostarczoną bazę wiedzy, w tym specyfikację GHOST v2 opartą na transkrypcjach Whisper Flow. Poniżej przedstawiam kompletny, rygorystyczny i zoptymalizowany pod kątem ADHD plan wdrożenia ostatniej warstwy Twojego systemu (Holistic Agentic OS).

---

### 1. GHOST v2: Filtr Stylizujący (Cyfrowy Bliźniak)

Filtr GHOST v2 jest ostatnim węzłem w procesie (tzw. post-processing hook). Jego zadaniem jest przechwycenie generycznego, surowego tekstu wygenerowanego przez innych dyrektorów (np. CMO AI) i bezwzględne sformatowanie go w autentyczny, mówiony styl Tomasza.

**Jak filtr analizuje i konwertuje tekst (Krok po Kroku):**
1. **Ekstrakcja rdzenia:** Filtr ignoruje sztuczne wstępy i zakończenia LLM. Wyciąga tylko twarde fakty i argumenty biznesowe.
2. **Eliminacja AI-isms:** Skanuje tekst pod kątem zakazanych słów (np. "kompleksowy", "w dzisiejszych czasach") i bezlitośnie je usuwa.
3. **Wstrzyknięcie markerów Tomasza:** Na początku dodaje typowe powitania ("Hej", "Słuchaj", "Dobra").
4. **Formatowanie ADHD-Optimal:** Dzieli blok tekstu na pojedyncze zdania. Maksymalnie 8-12 słów w zdaniu. Dodać punktory i dużo światła (przerw między liniami) dla łatwego skanowania wzrokiem.

#### Ostateczny Prompt Systemowy dla GHOST v2
Wklej ten prompt jako instrukcję systemową (System Prompt) do agenta lub węzła n8n odpowiedzialnego za finalną redakcję tekstu.

```text
ROLA: 
Jesteś filtrem stylizującym GHOST v2. Twoim zadaniem jest rygorystyczne przepisywanie surowych tekstów AI na autentyczny, mówiony język Tomasza – bezpośredniego, dynamicznego praktyka biznesu i automatyzacji.

ZASADY GŁÓWNE (ADHD-FRIENDLY & LOW-COST):
1. Bezpośredniość: Zwracaj się wprost do odbiorcy ("Ty", "Słuchaj", "Pokaż"). Bądź doradcą, nie korporacyjnym robotem.
2. Sktruktura wizualna: Pisz ekstremalnie krótko. Jedno zdanie to jedna myśl (max 8-12 słów). Zostawiaj dużo pustych linii (światła) między akapitami. Używaj wypunktowań.
3. Rytm mowy: Zaczynaj od obserwacji ("jak się temu przyglądam", "w mojej ocenie"). Zakończ twardo i zadaniowo ("Działaj", "Działajmy", "Koniec"). Brak owijania w bawełnę.

BEZWZGLĘDNA LISTA SŁÓW ZAKAZANYCH (USUNĄĆ NATYCHMIAST):
- "Wykorzystaj potencjał", "Transformacyjny wpływ", "Holistyczne podejście" (chyba że to nazwa własna Holistic Jason).
- "W dzisiejszych czasach", "Nie sposób przecenić", "Podsumowując", "Warto zauważyć, że...".
- "Innowacyjny", "Synergia", "Kompleksowy", "Droga do sukcesu".

TON ENERGETYCZNY:
- Jeśli tekst jest promocyjny/edukacyjny, wstrzyknij wysoką energię: "Naprawdę kozak, nie?", "Słuchajcie, o co tu chodzi...".
- Jeśli tekst jest upomnieniem lub twardą instrukcją B2B: "Weź się w garść", "Jak nie urok, to sraczka" (usuwając mocne wulgaryzmy, zachowując szorstką stanowczość).

INSTRUKCJA WYKONAWCZA:
Przepisz podany poniżej tekst wejściowy zgodnie z zasadami GHOST v2. Nie dodawaj komentarzy od siebie. Zwróć WYŁĄCZNIE czysty, gotowy do publikacji tekst.
```

---

### 2. Automatyczny Pipeline Wideo (Faceless Channels na GCP)

Aby Twój agent CCO AI (Dyrektor Kreatywny) produkował rolki na TikToka/Shorts całkowicie bez Twojego udziału, zaprojektowałem liniowy potok danych działający na Twojej maszynie `hermes-os` na GCP.

**Architektura Pipeline'u:**
1. **Skrypt (LLM + GHOST):** CCO AI generuje scenariusz, a GHOST v2 go stylizuje.
2. **Audio (TTS):** Moduł używa darmowej biblioteki (np. Edge-TTS) do wygenerowania głosu.
3. **B-Roll (Pexels API):** Skrypt uderza do darmowego API Pexels w poszukiwaniu pionowych klipów pasujących do słów kluczowych scenariusza.
4. **Montaż (MoviePy):** Python łączy audio z pobranym wideo, przycina długość i nakłada proste napisy, a następnie eksportuje plik `.mp4`.

#### Gotowy kod Python (Integracja na VM)
Poniższy kod można wdrożyć jako skrypt wywoływany przez Hermesa (terminal-execution) lub jako webhook FastAPI. Implementuje on zasadę Autoleczenia (try/catch).

```python
import os
import requests
import asyncio
import edge_tts
from moviepy.editor import VideoFileClip, AudioFileClip, TextClip, CompositeVideoClip
from moviepy.video.tools.subtitles import SubtitlesClip

# Konfiguracja API Pexels
PEXELS_API_KEY = os.getenv("PEXELS_API_KEY")

async def generate_tts(text: str, output_audio: str):
    """Generuje lektora TTS w stylu dynamicznym z użyciem darmowego Edge TTS."""
    communicate = edge_tts.Communicate(text, "pl-PL-MarekNeural", rate="+10%")
    await communicate.save(output_audio)

def fetch_pexels_broll(query: str, output_video: str):
    """Pobiera pionowy darmowy klip wideo z Pexels na bazie słowa kluczowego."""
    headers = {"Authorization": PEXELS_API_KEY}
    url = f"https://api.pexels.com/videos/search?query={query}&orientation=portrait&size=medium&per_page=1"
    
    try:
        response = requests.get(url, headers=headers)
        response.raise_for_status()
        video_data = response.json()
        
        if video_data.get("videos"):
            video_url = video_data["videos"][0]["video_files"][0]["link"]
            video_content = requests.get(video_url).content
            with open(output_video, "wb") as f:
                f.write(video_content)
            return True
        return False
    except Exception as e:
        print(f"Błąd Pexels API: {e}") # Logowanie błędu - Autoleczenie
        return False

def build_faceless_video(audio_path: str, video_path: str, output_path: str, hook_text: str):
    """Skleja audio, wideo B-Roll oraz nakłada tekst (Hook) za pomocą MoviePy."""
    try:
        # Ładowanie zasobów
        audio = AudioFileClip(audio_path)
        video = VideoFileClip(video_path)
        
        # Zapętlanie wideo, jeśli jest krótsze niż audio, i przycinanie do długości audio
        if video.duration < audio.duration:
            video = video.loop(duration=audio.duration)
        video = video.subclip(0, audio.duration)
        
        # Nakładanie audio na wideo
        video_with_audio = video.set_audio(audio)
        
        # Generowanie napisu (Hook w pierwszych 3 sekundach)
        txt_clip = TextClip(hook_text, fontsize=70, color='white', bg_color='rgba(0,0,0,0.5)', font='Arial-Bold', size=video.size, method='caption')
        txt_clip = txt_clip.set_position('center').set_duration(3) # Napis znika po 3 sek.
        
        # Składanie warstw
        final_video = CompositeVideoClip([video_with_audio, txt_clip])
        
        # Zapis z optymalizacją pod social media
        final_video.write_videofile(output_path, fps=30, codec="libx264", audio_codec="aac", threads=4)
        return True
    except Exception as e:
        print(f"Błąd montażu wideo: {e}")
        return False

# Przykładowy Workflow - wykonanie liniowe (Linear Swarm)
if __name__ == "__main__":
    script = "Znowu masz chaos w firmie? Weź się w garść. Zamiast testować setki apek, wdróż jednego agenta AI."
    search_keyword = "frustrated business man"
    
    asyncio.run(generate_tts(script, "voice.mp3"))
    if fetch_pexels_broll(search_keyword, "broll.mp4"):
        build_faceless_video("voice.mp3", "broll.mp4", "final_reel.mp4", "Chaos w firmie?")
        print("Wideo Faceless wygenerowane pomyślnie!")
```

---

### 3. Dystrybucja Organiczna i Pętla Zwrotna (Feedback Loop)

Aby system ewoluował i sam uczył się, co działa, musimy połączyć publikację z twardą analityką finansowo-reklamową. Zastosujemy metodę Client Financed Acquisition i rygorystyczne śledzenie metryk.

#### System Dystrybucji Organicznej
Wykorzystujemy n8n na Twoim VPS połączone z natywnym skillem Hermesa `social-media`. Agent wypluwa gotowy plik, a n8n przez webhooki automatycznie dystrybuuje plik `.mp4` i opisy (skonstruowane przez GHOST v2) do API LinkedIn, YouTube Shorts oraz Instagrama. Wszelkie linki publikowane w postach muszą posiadać ścisłe tagowanie UTM (np. `?utm_source=tiktok&utm_campaign=faceless_adhd_01`).

#### Implementacja Pętli Zwrotnej (Silos CMO)
Aby zamknąć obieg informacji, agenci muszą mieć dostęp do wyników sprzedażowych wygenerowanych przez Systeme.io, w celu oceny, które "haczyki" (hooks) przyniosły rzeczywistą gotówkę (a nie tylko próżne metryki - vanity metrics).

1. **Krok 1: Zbieranie danych (FastAPI Webhook):** Twój plik `webhook_api.py` wystawia punkt końcowy (endpoint) nasłuchujący zdarzeń z Systeme.io. Gdy nastąpi zakup (zdarzenie `customer.sale.completed` lub `contact.optin.completed`), webhook przechwytuje surowy ładunek (Payload) z informacją o UTM (z jakiego wideo przyszedł klient) oraz o kwocie.
2. **Krok 2: Formatowanie RAG (Automatyczny zapis do GCS):** Zamiast wrzucać to do relacyjnej bazy danych (której Vertex AI Search bezpośrednio nie odczyta), FastAPI transformuje ten wynik w krótki plik raportu w formacie Markdown i asynchronicznie ładuje go do katalogu `gs://holistic_kubelek/silos-cmo/raporty/` (wykorzystując uprawnienia konta usługi na maszynie VM).

*Przykład raportu w `silos-cmo/raporty/`:*
```markdown
# Raport Konwersji: Wideo "Chaos w firmie"
- Kampania: faceless_adhd_01
- Platforma: TikTok
- Akcja: Opt-in (Lead) - `contact.optin.completed`
- Wygenerowany przychód (Cash Collected): 0 PLN
- Wniosek systemowy: Hook agresywny ("Weź się w garść") skutecznie generuje leady w środowisku TikTok. 
```

3. **Krok 3: Analiza przez CMO AI (Vertex AI Search):** Podczas planowania kolejnego kalendarza treści, wywołujesz CMO AI w Streamlicie. Dzięki ustawionej logice Dynamicznego RAG, agent CMO odpytuje dedykowany Data Store powiązany z `silos-cmo/`. Agent analizuje wygenerowane raporty `.md` i stosuje zasadę proporcji 70-20-10 Hormoziego:
   * Przeznacza 70% zasobów na klonowanie najskuteczniejszego formatu, który fizycznie dowiózł leady.
   * Eliminuje tworzenie formatów, które miały dużo wyświetleń, ale zerowe konwersje z Systeme.io.

Dzięki takiej architekturze opartej na GCP, Twój ekosystem Holistic Agentic OS eliminuje w całości Twój udział w ręcznym analizowaniu wyników – staje się "samouczącą" się maszyną do optymalizacji LTV:CAC, a Ty skupiasz się wyłącznie na nadzorze dyrektorów.
