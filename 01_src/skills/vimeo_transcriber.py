"""
📹 Vimeo & Course Transcriber for Adrian Kilar's Courses
Generuje gęste notatki szkoleniowe z filmów Vimeo osadzonych na platformie.
Wyciąga realne napisy (transkrypcje) z Vimeo bez użycia API keys!
Wykorzystuje Gemini 2.5 Flash / Pro + wyszukiwanie darmowych alternatyw do narzędzi.
"""
import os
import re
import sys
import time
import requests
import json
from pathlib import Path
from google import genai
from google.genai import types
from google.genai.errors import APIError

# Konfiguracja Google Auth
SA_KEY_PATH = r"c:\Aplikacje MVP\Holistic Jason\holistic-dashboard-dev-dea2c872139e.json"
SA_KEY_PATH_FALLBACK = r"c:\Aplikacje MVP\Holistic Jason\01_src\config\holistic-dashboard-dev-dea2c872139e.json"

if os.path.exists(SA_KEY_PATH):
    os.environ["GOOGLE_APPLICATION_CREDENTIALS"] = SA_KEY_PATH
elif os.path.exists(SA_KEY_PATH_FALLBACK):
    os.environ["GOOGLE_APPLICATION_CREDENTIALS"] = SA_KEY_PATH_FALLBACK

def _get_client():
    return genai.Client(
        vertexai=True, 
        project="holistic-dashboard-dev", 
        location="us-central1",
        http_options=types.HttpOptions(timeout=60000)
    )

def get_vimeo_transcript(vimeo_url: str) -> str:
    """
    Pobiera napisy (transkrypcję) bezpośrednio z pliku WebVTT z Vimeo,
    odpytując publiczny endpoint playera.
    """
    if "vimeo.com" not in vimeo_url:
        return "" # Tylko Vimeo obsługuje pobieranie napisów bez API
        
    video_id_match = re.search(r"video/(\d+)", vimeo_url)
    if not video_id_match:
        video_id_match = re.search(r"(\d+)", vimeo_url)
    
    if not video_id_match:
        return ""
        
    video_id = video_id_match.group(1)
    config_url = f"https://player.vimeo.com/video/{video_id}/config"
    
    try:
        headers = {
            "User-Agent": "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/120.0.0.0 Safari/537.36"
        }
        res = requests.get(config_url, headers=headers, timeout=10)
        if res.status_code != 200:
            return ""
            
        data = res.json()
        text_tracks = data.get("request", {}).get("text_tracks", [])
        if not text_tracks:
            return ""
            
        # Szukamy napisów po polsku, potem po angielsku, lub bierzemy pierwsze lepsze
        track_url = ""
        for track in text_tracks:
            lang = track.get("lang", "").lower()
            if lang == "pl":
                track_url = track.get("url")
                break
        
        if not track_url:
            for track in text_tracks:
                lang = track.get("lang", "").lower()
                if lang == "en":
                    track_url = track.get("url")
                    break
                    
        if not track_url:
            track_url = text_tracks[0].get("url")
            
        if not track_url:
            return ""
            
        # Pobieranie pliku WebVTT
        vtt_res = requests.get(track_url, headers=headers, timeout=10)
        if vtt_res.status_code != 200:
            return ""
            
        vtt_text = vtt_res.text
        lines = vtt_text.split('\n')
        clean_lines = []
        for line in lines:
            line = line.strip()
            if not line:
                continue
            if line.startswith("WEBVTT") or line.startswith("STYLE") or line.startswith("NOTE"):
                continue
            if "-->" in line:
                continue
            # Usuwanie tagów HTML/WebVTT (np. <c>...)
            line = re.sub(r"<[^>]+>", "", line)
            if line.isdigit():
                continue
            clean_lines.append(line)
            
        # De-duplikacja sąsiednich linii
        final_lines = []
        for l in clean_lines:
            if not final_lines or final_lines[-1] != l:
                final_lines.append(l)
                
        return " ".join(final_lines)
    except Exception as e:
        print(f"[TRANSCRIPT ERROR] Błąd pobierania napisów dla Vimeo {video_id}: {e}")
        return ""

def fetch_google_doc_content(url: str) -> str:
    """
    Pobiera treść dokumentu z Google Docs lub Google Drive bez API key.
    Obsługuje:
    - Google Docs:  /document/d/ID/  → export?format=txt
    - Google Slides: /presentation/d/ID/ → export?format=txt
    - Google Sheets: /spreadsheets/d/ID/ → export?format=csv
    - Google Drive: /file/d/ID/  → uc?export=download&id=ID
    """
    try:
        import re as _re
        headers = {
            "User-Agent": "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36"
        }
        export_url = None
        content_type = "text"
        
        # Google Docs - dokumenty tekstowe
        doc_match = _re.search(r'docs\.google\.com/document/d/([a-zA-Z0-9_-]+)', url)
        if doc_match:
            doc_id = doc_match.group(1)
            export_url = f"https://docs.google.com/document/d/{doc_id}/export?format=txt"
        
        # Google Slides - prezentacje
        slides_match = _re.search(r'docs\.google\.com/presentation/d/([a-zA-Z0-9_-]+)', url)
        if not export_url and slides_match:
            doc_id = slides_match.group(1)
            export_url = f"https://docs.google.com/presentation/d/{doc_id}/export?format=txt"
        
        # Google Sheets - arkusze
        sheets_match = _re.search(r'docs\.google\.com/spreadsheets/d/([a-zA-Z0-9_-]+)', url)
        if not export_url and sheets_match:
            doc_id = sheets_match.group(1)
            export_url = f"https://docs.google.com/spreadsheets/d/{doc_id}/export?format=csv"
            content_type = "csv"
        
        # Google Drive - pliki generyczne (PDF, DOCX itp.)
        drive_match = _re.search(r'drive\.google\.com/file/d/([a-zA-Z0-9_-]+)', url)
        if not export_url and drive_match:
            file_id = drive_match.group(1)
            # Próba pobrania metadanych pliku (sprawdzenie czy to dokument)
            meta_url = f"https://drive.google.com/uc?export=download&id={file_id}"
            export_url = meta_url
            content_type = "binary"
        
        if not export_url:
            return ""
        
        res = requests.get(export_url, headers=headers, timeout=15, allow_redirects=True)
        
        if res.status_code != 200:
            return ""
        
        # Dla binarnych plików (PDF, DOCX) - nie możemy czytać treści bez bibliotek
        if content_type == "binary":
            content_disp = res.headers.get('Content-Disposition', '')
            content_mime = res.headers.get('Content-Type', '')
            if 'pdf' in content_mime or 'pdf' in content_disp.lower():
                return f"[Plik PDF dostępny pod linkiem: {url}]\n(Treść PDF wymaga ręcznego otwarcia lub biblioteki PyMuPDF)"
            elif 'text' in content_mime:
                return res.text[:8000]
            else:
                return f"[Plik do pobrania: {url}]"
        
        text = res.text[:10000]  # Limit 10k znaków
        
        # Czyszczenie zbędnych białych znaków
        lines = [l.strip() for l in text.split('\n') if l.strip()]
        return '\n'.join(lines)
        
    except Exception as e:
        print(f"[GDOC WARN] Nie udało się pobrać treści z {url}: {e}")
        return ""


def find_free_alternatives(tool_name: str) -> str:
    """
    Wyszukuje darmowe lub open-source alternatywy dla podanego płatnego narzędzia.
    """
    client = _get_client()
    prompt = f"""Jesteś architektem systemów AI i ekspertem ds. oprogramowania open-source.
Znajdź najlepsze, darmowe lub open-source alternatywy dla płatnego narzędzia kreatywnego: "{tool_name}".

Zwróć:
1. **Darmową alternatywę 1** (nazwa, krótki opis, dlaczego warto, link lub sposób instalacji).
2. **Darmową alternatywę 2** (np. rozwiązanie webowe lub lokalne).
3. **Porównanie Premium vs Free**: W czym wersja płatna {tool_name} wygrywa, a gdzie darmowa jest wystarczająca.

Pisz po polsku, krótko i konkretnie.
"""
    try:
        response = client.models.generate_content(
            model='gemini-2.5-flash',
            contents=prompt,
            config=types.GenerateContentConfig(temperature=0.2)
        )
        return response.text
    except Exception as e:
        return f"Nie udało się pobrać alternatyw dla {tool_name}: {e}"

def process_vimeo_lesson_to_md(vimeo_url: str, title: str, module_name: str = "AI MAGIC VIDEO EDITOR", lesson_description: str = "", overwrite: bool = False, target_parent: str = "Adrian Kilar Motion", enrich_mode: bool = False) -> str:
    """
    Tworzy notatkę na podstawie tytułu lekcji, linku wideo, transkrypcji oraz opisu.
    Jeśli plik istnieje, a enrich_mode jest włączony, łączy istniejącą notatkę z nowym opisem!
    """
    safe_course_folder = "".join([c if c.isalnum() or c in (" ", "_", "-") else "_" for c in module_name]).strip().replace(" ", "_")
    baza_dir = Path(r"c:\Aplikacje MVP\Holistic Jason\02_knowledge_base\raw") / target_parent / safe_course_folder
    
    # Tworzenie bezpiecznego tytułu
    safe_title = "".join([c if c.isalnum() else "_" for c in title])[:80]
    file_path = baza_dir / f"{safe_title}.md"
    
    # === CHECKPOINT / ENRICHMENT SYSTEM ===
    is_existing = file_path.exists()
    
    if is_existing and not overwrite and not enrich_mode:
        return f"⏭️ Pominięto (notatka już istnieje pod ścieżką: Baza_Wiedzy/{target_parent}/{safe_course_folder}/{file_path.name})"
        
    # === PUSTY NAGŁÓWEK / PUSTA LEKCJA BYPASS ===
    # Zapobiega zawieszaniu się i odpytywaniu Gemini o puste opisy dla sekcji/modułów organizacyjnych
    v_url = (vimeo_url or "").strip()
    l_desc = (lesson_description or "").strip()
    if not v_url and not l_desc:
        try:
            baza_dir.mkdir(exist_ok=True, parents=True)
            placeholder_content = (
                f"# NOTATKA / SEKCJA: {title}\n\n"
                f"**Kurs/Moduł:** {module_name}\n"
                f"**Status:** Sekcja organizacyjna / Brak materiałów\n\n"
                f"---\n\n"
                f"*Ta sekcja nie zawiera nagrania wideo ani opisu tekstowego na platformie.*"
            )
            with open(file_path, "w", encoding="utf-8") as f:
                f.write(placeholder_content)
            return f"✅ Zapisano pusty szablon dla sekcji: {file_path.name}"
        except Exception as e:
            return f"❌ Błąd zapisu szablonu sekcji: {e}"
            
    client = _get_client()
    
    # Tryb 1: Uzdatnienie / Wzbogacenie istniejącej notatki o pełny opis
    if is_existing and enrich_mode and not overwrite:
        try:
            with open(file_path, "r", encoding="utf-8") as f:
                existing_content = f.read()
        except Exception as e:
            return f"❌ Błąd odczytu istniejącej notatki: {e}"
            
        prompt = f"""Jesteś wiodącym analitykiem wiedzy.
Wklejam Ci istniejącą notatkę z lekcji (która została wcześniej wygenerowana na bazie wideo/transkrypcji) oraz kompletny opis tej lekcji z platformy kursowej (który zawiera szczegółowe kroki, linki, prompty i pro-tipy).

Twoim zadaniem jest WZBOGACIĆ istniejącą notatkę o te nowe szczegóły z opisu.
- Zachowaj wszystkie szczegóły z istniejącej notatki (szczególnie sekcje transkrypcji, streszczenia, wnioski).
- Uzupełnij workflow o dokładne instrukcje krok po kroku, prompty, linki i pro-tipy z pełnego opisu.
- Zaktualizuj i połącz tabele narzędzi premium oraz darmowych alternatyw.
- Zwróć gotowy, zaktualizowany Markdown o identycznym tytule.

ISTNIEJĄCA NOTATKA:
\"\"\"{existing_content}\"\"\"

PEŁNY OPIS Z PLATFORMY:
\"\"\"{lesson_description}\"\"\"

Pisz wyłącznie PO POLSKU. Zwróć gotowy, profesjonalny Markdown. Dołącz oryginalny link do filmu na początku.
"""
    # Tryb 2: Generowanie nowej notatki od zera
    else:
        # Wyciąganie transkrypcji
        transcript_text = get_vimeo_transcript(vimeo_url)
        
        # === GOOGLE DOCS/DRIVE: Ekstrakcja i pobieranie treści materiałów dodatkowych ===
        gdoc_content_blocks = []
        if lesson_description:
            gdoc_pattern = re.compile(
                r'https?://(?:docs\.google\.com/(?:document|presentation|spreadsheets)/d/|drive\.google\.com/file/d/)[a-zA-Z0-9_/-]+'
            )
            gdoc_links = gdoc_pattern.findall(lesson_description)
            # Deduplikacja zachowując kolejność
            seen_links = set()
            unique_gdoc_links = []
            for lnk in gdoc_links:
                base = lnk.split('/view')[0].split('?')[0]
                if base not in seen_links:
                    seen_links.add(base)
                    unique_gdoc_links.append(lnk)
            
            for gdoc_url in unique_gdoc_links[:5]:  # Max 5 dokumentów per lekcja
                print(f"  [GDOC] Pobieram: {gdoc_url[:80]}...")
                content = fetch_google_doc_content(gdoc_url)
                if content and len(content) > 50 and not content.startswith('[Plik'):
                    gdoc_content_blocks.append(f"### Dokument: {gdoc_url}\n\n{content}")
                elif content:
                    gdoc_content_blocks.append(f"### Link do materiału: {gdoc_url}\n\n{content}")
        
        gdoc_section = "\n\n---\n\n".join(gdoc_content_blocks) if gdoc_content_blocks else ""
        # ============================================================
        
        # Wczytujemy istniejący przewodnik Kilar jako dodatkowy kontekst
        context_guide = ""
        if "Kilar" in target_parent or "Kilar" in module_name:
            guide_path = Path(r"c:\Aplikacje MVP\Holistic Jason\02_knowledge_base\raw\Adrian Kilar Motion\PDF___MAPA___PRZEWODNIK.md")
            if guide_path.exists():
                with open(guide_path, "r", encoding="utf-8") as f:
                    context_guide = f.read()[:4000]

        prompt = f"""Jesteś wiodącym analitykiem wiedzy i ekspertem ds. wideo AI i e-learningu.
Przetrawiasz lekcję z kursu e-learningowego:
- Folder Docelowy: {target_parent}
- Kurs/Moduł: {module_name}
- Tytuł Lekcji: {title}
- Link Wideo: {vimeo_url}

OPIS LEKCJI Z PLATFORMY (POD FILMEM):
\"\"\"{lesson_description}\"\"\"

POBRANA TRANSKRYPCJA Z FILMU (JEŚLI DOSTĘPNA):
\"\"\"{transcript_text if transcript_text else "Brak bezpośredniej transkrypcji (wygeneruj notatkę na bazie opisu i tytułu)"}\"\"\"

{f"KONTEKST Z PRZEWODNIKA KURSU:\\n{context_guide}" if context_guide else ""}

{f"POBRANE MATERIAŁY DODATKOWE (Promptbooki / Dokumenty / Arkusze z Google Drive/Docs):\n\"\"\"{gdoc_section}\"\"\"" if gdoc_section else ""}

ZADANIE:
Na podstawie tytułu lekcji, opisu pod filmem, ewentualnej transkrypcji, kontekstu oraz pobranych materiałów dodatkowych zredaguj niezwykle szczegółową i gęstą notatkę szkoleniową.
1. **Nagłówek H1**: Tytuł Lekcji.
2. **Kluczowy Cel Ujęcia / Temat Lekcji**: Co chcemy osiągnąć w tej lekcji (filozofia, efekt).
3. **Streszczenie Transkrypcji / Wiedzy**: Streść najważniejsze wskazówki, techniki i wypowiedzi autora.
4. **Workflow Krok po Kroku**: Dokładna instrukcja wykonania omawianego zadania lub techniki.
5. **Narzędzia Premium & Darmowe Alternatywy**:
   - Wymień użyte narzędzia.
   - Zaproponuj DARMOWE lub open-source alternatywy.
6. **Materiały Dodatkowe (z Dokumentów)**:
   - Jeśli powyżej dołączono treść materiałów (Promptbook, Arkusz, itp.), wyciągnij z nich kluczowe prompty, instrukcje, szablony i osadź je w notatce jako gotowe do użycia zasoby.
   - Każdy kluczowy prompt/szablon umieść w bloku kodu ```.
7. **Złota Zasada Lekcji**: Jedno, kluczowe zdanie podsumowujące.

Pisz wyłącznie PO POLSKU. Zwróć gotowy, profesjonalny Markdown.
"""

    # === RESILIENT API CALL LOOP (EXPONENTIAL BACKOFF) ===
    md_content = ""
    max_retries = 7
    backoff = 5
    
    for attempt in range(max_retries):
        try:
            response = client.models.generate_content(
                model='gemini-2.5-flash',
                contents=prompt,
                config=types.GenerateContentConfig(temperature=0.3)
            )
            md_content = response.text
            break # Success!
        except Exception as e:
            # Określenie czy błąd kwalifikuje się do ponowienia (błędy sieciowe lub limit kwotowy)
            is_quota_or_network = False
            error_str = str(e).lower()
            
            if isinstance(e, APIError):
                # Kod 429 lub limit kwotowy
                if e.code == 429 or "quota" in error_str or "limit" in error_str:
                    is_quota_or_network = True
            else:
                # Każdy inny błąd sieciowy (RemoteDisconnected, Connection aborted, timeout, itp.)
                is_quota_or_network = True
                
            if is_quota_or_network and attempt < max_retries - 1:
                print(f"[API WARN] Próba {attempt+1}/{max_retries} nieudana z powodu sieci/limitu. Szczegóły: {e}. Czekam {backoff}s...")
                time.sleep(backoff)
                backoff *= 2
            else:
                return f"❌ Krytyczny błąd Gemini dla '{title}': {e}"
            
    if not md_content:
        # Ten warunek w teorii nie powinien się zdarzyć bo rzucilibyśmy błąd powyżej, ale dla bezpieczeństwa:
        return f"❌ Błąd: Przekroczono limit prób pobierania dla '{title}'."

    # Zapis w bazie wiedzy
    baza_dir.mkdir(exist_ok=True, parents=True)
    with open(file_path, "w", encoding="utf-8") as f:
        if enrich_mode and is_existing and not overwrite:
            f.write(md_content) # Tryb uzdatniania zwraca już pełny połączony md
        else:
            video_link_str = vimeo_url if vimeo_url else "Brak (Lekcja tekstowa / Materiały do pobrania)"
            f.write(f"# NOTATKA Z LEKCJI: {title}\n\n**Kurs/Moduł:** {module_name}\n**Oryginalny Link Wideo:** {video_link_str}\n\n---\n\n" + md_content)
        
    time.sleep(1.5)
    
    status_word = "Uzdatniono i wzbogacono" if (enrich_mode and is_existing) else "Zapisano"
    return f"✅ {status_word} notatkę w Bazie Wiedzy: {target_parent}/{safe_course_folder}/{file_path.name}"

def fast_inject_description_locally(title: str, module_name: str, lesson_description: str, target_parent: str = "Adrian Kilar Motion") -> str:
    """
    Szybko wstrzykuje opis do istniejącego pliku MD bez użycia AI API (100% lokalnie).
    """
    safe_course_folder = "".join([c if c.isalnum() or c in (" ", "_", "-") else "_" for c in module_name]).strip().replace(" ", "_")
    baza_dir = Path(r"c:\Aplikacje MVP\Holistic Jason\02_knowledge_base\raw") / target_parent / safe_course_folder
    
    # Tworzenie bezpiecznego tytułu
    safe_title = "".join([c if c.isalnum() else "_" for c in title])[:80]
    file_path = baza_dir / f"{safe_title}.md"
    
    if not file_path.exists():
        # Jeśli plik nie istnieje, tworzymy go w minimalistycznej formie
        baza_dir.mkdir(exist_ok=True, parents=True)
        content = f"# NOTATKA Z LEKCJI: {title}\n\n**Kurs/Moduł:** {module_name}\n\n## 📝 Opis z Platformy (Wstęp)\n\n{lesson_description}\n\n---\n\n*(Notatka wygenerowana z opisu - brak transkrypcji)*\n"
        try:
            with open(file_path, "w", encoding="utf-8") as f:
                f.write(content)
            return f"✅ Stworzono nową notatkę z opisu: {file_path.name}"
        except Exception as e:
            return f"❌ Błąd zapisu nowej notatki: {e}"
        
    try:
        with open(file_path, "r", encoding="utf-8") as f:
            content = f.read()
    except Exception as e:
        return f"❌ Błąd odczytu pliku: {e}"
        
    # Sprawdzenie czy opis już tam jest
    if "## 📝 Opis z Platformy" in content or "Opis z platformy" in content or "OPIS LEKCJI Z PLATFORMY" in content:
        return f"⏭️ Lekcja już zawiera opis: {file_path.name}"
        
    # Wstrzyknięcie
    injection = f"\n\n## 📝 Opis z Platformy (Wstęp)\n\n{lesson_description}\n\n---\n"
    
    if "---" in content:
        parts = content.split("---", 1)
        new_content = parts[0] + "---" + injection + parts[1]
    else:
        # Fallback
        lines = content.split("\n")
        inserted = False
        for i, line in enumerate(lines):
            if line.startswith("# ") or "NOTATKA" in line:
                lines.insert(i + 1, injection)
                inserted = True
                break
        if inserted:
            new_content = "\n".join(lines)
        else:
            new_content = injection + "\n" + content
            
    try:
        with open(file_path, "w", encoding="utf-8") as f:
            f.write(new_content)
        return f"⚡ Uzdatniono błyskawicznie (dodano opis): {file_path.name}"
    except Exception as e:
        return f"❌ Błąd zapisu: {e}"

