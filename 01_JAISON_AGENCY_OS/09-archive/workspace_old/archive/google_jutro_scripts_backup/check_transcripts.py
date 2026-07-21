import os
import json
from youtube_transcript_api import YouTubeTranscriptApi

IDS_TO_TEST = ['WctbtcsLANY', 'xlG3SRkIzRQ', 'JkLWdRyPQd0']
TRANSCRIPT_DIR = 'Transkrypcje'

for video_id in IDS_TO_TEST:
    print(f"\nTesting Video ID: {video_id}")
    
    # 1. Fetch from YT
    try:
        transcript_list = YouTubeTranscriptApi.get_transcript(video_id, languages=['pl', 'en'])
        fetched_text = " ".join([t['text'] for t in transcript_list])
        print(f"  [+] Fetched {len(fetched_text)} characters from YouTube.")
        fetched_sample = fetched_text[:200].replace('\n', ' ')
    except Exception as e:
        print(f"  [-] Failed to fetch from YouTube: {e}")
        fetched_sample = ""
        
    # 2. Read from local file
    local_file = os.path.join(TRANSCRIPT_DIR, f"{video_id}.txt")
    if os.path.exists(local_file):
        with open(local_file, 'r', encoding='utf-8') as f:
            local_text = f.read()
        print(f"  [+] Read {len(local_text)} characters from local file.")
        local_sample = local_text[:200].replace('\n', ' ')
    else:
        print(f"  [-] Local file not found: {local_file}")
        local_sample = ""
        
    # 3. Compare
    print(f"  Fetched Sample: {fetched_sample}")
    print(f"  Local Sample:   {local_sample}")
    
    if fetched_sample and local_sample:
        # Simple similarity check (could use difflib but visual is fine)
        if fetched_sample[:50] == local_sample[:50]:
            print("  [SUCCESS] Local transcript matches YouTube (No hallucination).")
        else:
            print("  [WARNING] Mismatch detected! Possibly hallucinated or different format.")
