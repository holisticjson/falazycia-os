import yt_dlp
import os

IDS_TO_TEST = ['WctbtcsLANY', 'xlG3SRkIzRQ', 'JkLWdRyPQd0']
TRANSCRIPT_DIR = 'Transkrypcje'

ydl_opts = {
    'skip_download': True,
    'writesubtitles': True,
    'writeautomaticsub': True,
    'subtitleslangs': ['pl'],
    'outtmpl': '%(id)s.%(ext)s',
    'quiet': True,
    'nocheckcertificate': True
}

for video_id in IDS_TO_TEST:
    print(f"\n--- Testing Video ID: {video_id} ---")
    url = f"https://www.youtube.com/watch?v={video_id}"
    try:
        with yt_dlp.YoutubeDL(ydl_opts) as ydl:
            ydl.download([url])
        
        # Check if downloaded
        vtt_file = f"{video_id}.pl.vtt"
        if os.path.exists(vtt_file):
            with open(vtt_file, 'r', encoding='utf-8') as f:
                fetched_content = f.read(500).replace('\n', ' ')
            print(f"FETCHED (first 500 chars):\n{fetched_content}\n")
            os.remove(vtt_file) # cleanup
        else:
            print("Failed to download subtitles (no file produced).")
            fetched_content = ""
            
    except Exception as e:
        print(f"Error fetching from YouTube: {e}")
        fetched_content = ""

    local_file = os.path.join(TRANSCRIPT_DIR, f"{video_id}.txt")
    if os.path.exists(local_file):
        with open(local_file, 'r', encoding='utf-8') as f:
            local_text = f.read(500).replace('\n', ' ')
        print(f"LOCAL TXT (first 500 chars):\n{local_text}\n")
    else:
        print(f"Local file {local_file} not found!")
        
    local_vtt = os.path.join(TRANSCRIPT_DIR, f"{video_id}.pl.vtt")
    if os.path.exists(local_vtt):
        with open(local_vtt, 'r', encoding='utf-8') as f:
            local_vtt_text = f.read(500).replace('\n', ' ')
        print(f"LOCAL VTT (first 500 chars):\n{local_vtt_text}\n")
    else:
        print(f"Local file {local_vtt} not found!")

print("\nDONE.")
