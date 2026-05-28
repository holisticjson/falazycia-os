"""
🎬 Faceless Video Pipeline — Holistic Jason
Pipeline: Skrypt → TTS (Kokoro/ElevenLabs) → B-Roll (Pexels) → Montaż (FFmpeg) → Upload
"""
import os
import json
import requests
from pathlib import Path
from datetime import datetime

# ============================================================
# KONFIGURACJA
# ============================================================
PEXELS_API_KEY = os.getenv("PEXELS_API_KEY", "")  # Darmowe API
ELEVENLABS_API_KEY = os.getenv("ELEVENLABS_API_KEY", "")  # Premium TTS
OUTPUT_DIR = Path(r"c:\Aplikacje MVP\Holistic Jason\generated_media\faceless")
OUTPUT_DIR.mkdir(exist_ok=True, parents=True)

# ============================================================
# 1. PEXELS — Darmowe B-Roll (Stock Footage)
# ============================================================
def search_pexels_videos(query: str, per_page: int = 5, orientation: str = "portrait"):
    """Szuka darmowych wideo na Pexels do wykorzystania jako B-Roll."""
    if not PEXELS_API_KEY:
        return {"error": "Brak PEXELS_API_KEY. Zarejestruj się na pexels.com/api"}
    
    url = "https://api.pexels.com/videos/search"
    headers = {"Authorization": PEXELS_API_KEY}
    params = {
        "query": query,
        "per_page": per_page,
        "orientation": orientation,  # portrait = 9:16 (Shorts/Reels)
        "size": "medium"
    }
    
    response = requests.get(url, headers=headers, params=params)
    if response.status_code == 200:
        videos = response.json().get("videos", [])
        results = []
        for v in videos:
            # Wybierz najlepszą jakość w formacie pionowym
            best_file = None
            for vf in v.get("video_files", []):
                if vf.get("height", 0) >= 720:
                    best_file = vf
                    break
            if not best_file and v.get("video_files"):
                best_file = v["video_files"][0]
            
            results.append({
                "id": v["id"],
                "duration": v.get("duration"),
                "preview": v.get("image"),
                "download_url": best_file["link"] if best_file else None,
                "width": best_file.get("width") if best_file else None,
                "height": best_file.get("height") if best_file else None,
            })
        return results
    else:
        return {"error": response.status_code, "detail": response.text}


def download_pexels_video(video_url: str, filename: str) -> str:
    """Pobiera wideo z Pexels na dysk."""
    output_path = OUTPUT_DIR / filename
    response = requests.get(video_url, stream=True)
    if response.status_code == 200:
        with open(output_path, "wb") as f:
            for chunk in response.iter_content(chunk_size=8192):
                f.write(chunk)
        return str(output_path)
    return ""


# ============================================================
# 2. ELEVENLABS — Premium Text-to-Speech
# ============================================================
def generate_voiceover_elevenlabs(text: str, voice_id: str = "21m00Tcm4TlvDq8ikWAM", 
                                   output_filename: str = "voiceover.mp3") -> str:
    """Generuje voiceover przez ElevenLabs API."""
    if not ELEVENLABS_API_KEY:
        return "BRAK_KLUCZA_ELEVENLABS"
    
    url = f"https://api.elevenlabs.io/v1/text-to-speech/{voice_id}"
    headers = {
        "Accept": "audio/mpeg",
        "Content-Type": "application/json",
        "xi-api-key": ELEVENLABS_API_KEY
    }
    data = {
        "text": text,
        "model_id": "eleven_multilingual_v2",  # Obsługuje polski!
        "voice_settings": {
            "stability": 0.5,
            "similarity_boost": 0.75
        }
    }
    
    response = requests.post(url, json=data, headers=headers)
    if response.status_code == 200:
        output_path = OUTPUT_DIR / output_filename
        with open(output_path, "wb") as f:
            f.write(response.content)
        return str(output_path)
    else:
        return f"ERROR: {response.status_code} - {response.text[:200]}"


# ============================================================
# 3. KOKORO TTS — Darmowy Text-to-Speech (lokalne/Docker)
# ============================================================
def generate_voiceover_kokoro(text: str, output_filename: str = "voiceover.wav") -> str:
    """Generuje voiceover przez Kokoro TTS (lokalne API Docker)."""
    # Kokoro działa na localhost:8880 gdy uruchomiony przez Docker
    url = "http://localhost:8880/v1/audio/speech"
    data = {
        "model": "kokoro",
        "input": text,
        "voice": "af_heart",  # lub bf_emma, am_adam, etc.
        "response_format": "wav",
        "speed": 1.0
    }
    
    try:
        response = requests.post(url, json=data, timeout=60)
        if response.status_code == 200:
            output_path = OUTPUT_DIR / output_filename
            with open(output_path, "wb") as f:
                f.write(response.content)
            return str(output_path)
        else:
            return f"ERROR: {response.status_code}"
    except requests.exceptions.ConnectionError:
        return "KOKORO_OFFLINE — Uruchom: docker run -p 8880:8880 ghcr.io/remsky/kokoro-fastapi-cpu"


# ============================================================
# 4. FFMPEG — Montaż wideo (B-Roll + Audio + Napisy)
# ============================================================
def create_faceless_video(audio_path: str, video_clips: list, 
                          output_name: str = "final_video.mp4",
                          add_subtitles: bool = True) -> str:
    """
    Łączy audio (voiceover) z klipami wideo (B-Roll) w gotowe wideo.
    Wymaga zainstalowanego FFmpeg.
    """
    import subprocess
    
    # Absolute path to FFmpeg found on this system
    ffmpeg_path = r"C:\Users\tomas_yq1b9su\AppData\Local\Microsoft\WinGet\Packages\Gyan.FFmpeg_Microsoft.Winget.Source_8wekyb3d8bbwe\ffmpeg-8.1.1-full_build\bin\ffmpeg.exe"
    
    output_path = OUTPUT_DIR / output_name
    
    if not video_clips:
        return "BRAK_KLIPOW_WIDEO"
    
    # Krok 1: Połącz klipy wideo w jeden plik
    concat_file = OUTPUT_DIR / "concat_list.txt"
    with open(concat_file, "w") as f:
        for clip in video_clips:
            f.write(f"file '{clip}'\n")
    
    merged_video = OUTPUT_DIR / "merged_broll.mp4"
    
    # Połącz klipy
    cmd_concat = [
        ffmpeg_path, "-y",
        "-f", "concat", "-safe", "0",
        "-i", str(concat_file),
        "-c", "copy",
        str(merged_video)
    ]
    
    # Krok 2: Nałóż audio na wideo
    cmd_final = [
        ffmpeg_path, "-y",
        "-i", str(merged_video),
        "-i", audio_path,
        "-c:v", "libx264",
        "-c:a", "aac",
        "-shortest",  # Kończy gdy krótszy stream się skończy
        "-map", "0:v:0",
        "-map", "1:a:0",
        str(output_path)
    ]
    
    try:
        subprocess.run(cmd_concat, check=True, capture_output=True)
        subprocess.run(cmd_final, check=True, capture_output=True)
        
        # Cleanup
        merged_video.unlink(missing_ok=True)
        concat_file.unlink(missing_ok=True)
        
        return str(output_path)
    except subprocess.CalledProcessError as e:
        return f"FFMPEG_ERROR: {e.stderr.decode()[:300]}"
    except FileNotFoundError:
        return "FFMPEG_NOT_FOUND — Zainstaluj FFmpeg: winget install FFmpeg"


# ============================================================
# 5. VIRAL FACELESS CHANNEL RESEARCH
# ============================================================
VIRAL_FACELESS_NICHES = {
    "AI & Tech Tips": {
        "channels": ["AI Revolution", "Matt Wolfe", "Futurepedia"],
        "format": "Screen recording + voiceover + tekst na ekranie",
        "hooks": [
            "This AI tool replaced my entire team...",
            "Stop using ChatGPT wrong. Here's how.",
            "I automated my entire business in 24 hours",
        ],
        "monetization": ["Affiliate links", "Kursy", "Sponsorzy"],
    },
    "Business & Productivity": {
        "channels": ["Ali Abdaal (faceless clips)", "Thomas Frank"],
        "format": "Animacje + B-Roll + silny voiceover",
        "hooks": [
            "5 narzędzi, które zarabiają za mnie",
            "Przestań pracować 12h dziennie. Zrób TO.",
            "Ta jedna zmiana podwoiła moje przychody",
        ],
        "monetization": ["Produkty cyfrowe", "Coaching", "Narzędzia SaaS"],
    },
    "Finance & Side Hustles": {
        "channels": ["Mark Tilbury", "Proactive Thinker"],
        "format": "Animacja whiteboard + dane + storytelling",
        "hooks": [
            "Jak zarabiać 5000 PLN miesięcznie pasywnie",
            "Nikt Ci tego nie powie o prowadzeniu firmy",
            "3 biznesy, które możesz zacząć JUTRO za 0 PLN",
        ],
        "monetization": ["Ebooki", "Kursy", "Mentoring"],
    },
}


# ============================================================
# 6. PEŁNY PIPELINE (Orkiestracja)
# ============================================================
def run_faceless_pipeline(script: str, broll_queries: list, 
                          voice_provider: str = "kokoro",
                          voice_id: str = None,
                          output_name: str = None) -> dict:
    """
    Uruchamia pełny pipeline produkcji Faceless Video:
    1. Generuje voiceover z tekstu
    2. Pobiera B-Roll z Pexels
    3. Montuje finalne wideo
    """
    timestamp = datetime.now().strftime("%Y%m%d_%H%M%S")
    if not output_name:
        output_name = f"faceless_{timestamp}.mp4"
    
    result = {"steps": [], "final_video": None}
    
    # Step 1: Voiceover
    if voice_provider == "elevenlabs":
        v_id = voice_id if voice_id else "21m00Tcm4TlvDq8ikWAM"
        audio_path = generate_voiceover_elevenlabs(script, voice_id=v_id, output_filename=f"vo_{timestamp}.mp3")
    else:
        audio_path = generate_voiceover_kokoro(script, output_filename=f"vo_{timestamp}.wav")
    
    result["steps"].append({"step": "voiceover", "result": audio_path})
    
    if "ERROR" in str(audio_path) or "BRAK" in str(audio_path) or "OFFLINE" in str(audio_path):
        result["error"] = f"Voiceover failed: {audio_path}"
        return result
    
    # Step 2: B-Roll
    downloaded_clips = []
    for i, query in enumerate(broll_queries):
        videos = search_pexels_videos(query, per_page=2)
        if isinstance(videos, list):
            for j, v in enumerate(videos):
                if v.get("download_url"):
                    clip_path = download_pexels_video(
                        v["download_url"], 
                        f"broll_{timestamp}_{i}_{j}.mp4"
                    )
                    if clip_path:
                        downloaded_clips.append(clip_path)
    
    result["steps"].append({"step": "broll", "clips": len(downloaded_clips)})
    
    if not downloaded_clips:
        result["error"] = "No B-Roll clips downloaded"
        return result
    
    # Step 3: Montaż
    final_path = create_faceless_video(audio_path, downloaded_clips, output_name)
    result["steps"].append({"step": "montage", "result": final_path})
    result["final_video"] = final_path
    
    return result


if __name__ == "__main__":
    print("=== Faceless Video Pipeline ===")
    print(f"Output dir: {OUTPUT_DIR}")
    print(f"Pexels API: {'OK' if PEXELS_API_KEY else 'BRAK (ustaw PEXELS_API_KEY)'}")
    print(f"ElevenLabs: {'OK' if ELEVENLABS_API_KEY else 'BRAK (ustaw ELEVENLABS_API_KEY)'}")
    print("\nViral Niches:")
    for niche, data in VIRAL_FACELESS_NICHES.items():
        print(f"  {niche}: {', '.join(data['hooks'][:2])}")
