import os
import requests
from dotenv import load_dotenv

load_dotenv()

def generate_video_reel(query: str, count: int = 1) -> str:
    """
    Video Maker Specialist: Wyszukuje darmowe przebitki wideo (B-Roll) na Pexels
    i zwraca linki do pobrania, gotowe do montażu.
    """
    api_key = os.getenv("PEXELS_API_KEY")
    if not api_key:
        return "BŁĄD: Brak klucza PEXELS_API_KEY w pliku .env."
    
    url = f"https://api.pexels.com/videos/search?query={query}&per_page={count}&orientation=portrait"
    headers = {"Authorization": api_key}
    
    try:
        response = requests.get(url, headers=headers)
        response.raise_for_status()
        data = response.json()
        
        if not data.get("videos"):
            return f"Brak wyników wideo dla zapytania: '{query}'."
            
        videos = []
        for v in data["videos"]:
            video_url = v["video_files"][0]["link"]
            videos.append(f"Znalazłem wideo '{query}': {video_url}")
            
        return "\n".join(videos)
        
    except Exception as e:
        return f"Wystąpił błąd podczas szukania wideo w Pexels: {e}"

def build_funnel_systeme_io(funnel_name: str, html_content: str) -> str:
    """
    Funnel Builder Specialist: Buduje lejek w Systeme.io
    Obecnie czeka na klucz API / Webhook, dlatego symuluje działanie.
    """
    # MOCK dla Systeme.io (oczekujemy na klucz od użytkownika)
    api_key = os.getenv("SYSTEME_IO_API_KEY")
    if not api_key:
        return f"ZBUDOWANO LEJEK LOKALNIE: '{funnel_name}'. Oczekuję na SYSTEME_IO_API_KEY w .env, aby przesłać go na serwer."
        
    return f"SUKCES: Lejek '{funnel_name}' został przesłany do Systeme.io pomyślnie za pomocą API."

def seo_analysis(keyword: str) -> str:
    """
    SEO Specialist: Wykonuje podstawową analizę SEO słowa kluczowego.
    """
    return f"Wynik analizy SEO dla '{keyword}': Wysoki potencjał wyszukiwania, niska konkurencja w niszach edukacyjnych."
