import os
import glob

base_dir = "Obsidian_Knowledge_Base/Tydzień 5 - Transformacja i zarządzanie projektami Ai w organizacji"
files = glob.glob(os.path.join(base_dir, "**/*.md"), recursive=True)

print(f"Znaleziono {len(files)} plików markdown w Tygodniu 5:")
no_rag = []
has_rag = []
no_transcript = []

for file_path in files:
    with open(file_path, 'r', encoding='utf-8') as f:
        content = f.read()
    
    basename = os.path.basename(file_path)
    
    if "## Zoptymalizowane Notatki (RAG)" in content:
        has_rag.append(basename)
    else:
        # Sprawdzamy czy ma jakikolwiek raw transcript
        if "## Transkrypcja" in content or "<details>" in content:
            no_rag.append(file_path)
        else:
            no_transcript.append(file_path)

print(f"\nPliki z RAG ({len(has_rag)}):")
for f in sorted(has_rag):
    print(f"  [x] {f}")

print(f"\nPliki bez RAG, ale posiadające transkrypcję (DO WYGENEROWANIA) ({len(no_rag)}):")
for f in sorted(no_rag):
    print(f"  [ ] {os.path.basename(f)}")

print(f"\nPliki inne / pdf / pomocnicze (bez transkrypcji i bez RAG) ({len(no_transcript)}):")
for f in sorted(no_transcript):
    print(f"  [-] {os.path.basename(f)}")

# Zapiszmy te do wygenerowania do pliku JSON
to_generate = []
for f in no_rag:
    to_generate.append({"file": f, "yt_id": ""}) # yt_id opcjonalne, w skrypcie i tak uzywany jest file_path

import json
with open('actual_missing_rag_week5.json', 'w', encoding='utf-8') as f:
    json.dump(to_generate, f, indent=2, ensure_ascii=False)
print(f"\nZapisano {len(to_generate)} plików do wygenerowania do 'actual_missing_rag_week5.json'")
