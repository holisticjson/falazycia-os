import os
import re
import sys
from pathlib import Path
from youtube_transcript_api import YouTubeTranscriptApi

# Ensure UTF-8 for Windows console
if sys.platform == "win32":
    import codecs
    if hasattr(sys.stdout, 'detach'):
        sys.stdout = codecs.getwriter("utf-8")(sys.stdout.detach())

def extract_yt_id(url):
    match = re.search(r"v=([a-zA-Z0-9_-]+)", url)
    return match.group(1) if match else None

def mass_transcribe():
    md_path = Path(r"c:\Aplikacje MVP\Holistic Jason\Baza_Wiedzy\Kursy_i_Szkolenia\Umiejętności_Jutra_3.0 - tydzień_2\TYDZIEŃ 2 — Pełna lista zasobów wideo i materiałów.md")
    output_dir = md_path.parent / "02_Transkrypcje"
    output_dir.mkdir(exist_ok=True)
    
    with open(md_path, 'r', encoding='utf-8') as f:
        content = f.read()
    
    matches = re.findall(r"\| (\d+) \| (.*?) \| (https://www\.youtube\.com/watch\?v=[\w-]+) \|", content)
    
    print(f"Found {len(matches)} videos.")
    
    api = YouTubeTranscriptApi()
    
    for num, title, url in matches:
        video_id = extract_yt_id(url)
        # Remove emojis for console safety
        clean_title = title.strip().replace("\ud83c\udfa5 ", "").replace("\u23f3 ", "")
        safe_title = re.sub(r'[\\/*?:"<>|]', "", clean_title).strip()
        out_file = output_dir / f"{num}_{safe_title}.md"
        
        if out_file.exists():
            continue
            
        print(f"Transcribing: {safe_title}...")
        try:
            transcript_data = api.fetch(video_id, languages=['pl', 'en'])
            text = "\n".join([f"[{snippet.start:.1f}s] {snippet.text}" for snippet in transcript_data])
            
            with open(out_file, 'w', encoding='utf-8') as f_out:
                f_out.write(f"# {clean_title}\n\n**Source:** {url}\n\n---\n\n{text}")
            print(f"DONE: {safe_title}")
        except Exception as e:
            print(f"ERROR for {safe_title}: {str(e)}")

if __name__ == "__main__":
    mass_transcribe()
