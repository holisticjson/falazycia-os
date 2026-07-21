import os
import json

with open('missing_files_week5.json', 'r', encoding='utf-8') as f:
    files = json.load(f)

missing_rag = []
no_transcript = []
has_rag = []

for item in files:
    file_path = item['file']
    if not os.path.exists(file_path):
        print(f"Plik nie istnieje: {file_path}")
        continue
        
    with open(file_path, 'r', encoding='utf-8') as f:
        content = f.read()
        
    has_notes = "## Zoptymalizowane Notatki (RAG)" in content
    
    parts = content.split("## Transkrypcja\n\n")
    if len(parts) < 2:
        no_transcript.append(file_path)
        continue
        
    raw_transcript = parts[1].strip()
    if not raw_transcript or "Transkrypcja niedostępna" in raw_transcript:
        no_transcript.append(file_path)
    elif not has_notes:
        missing_rag.append({
            'file': file_path,
            'yt_id': item['yt_id']
        })
    else:
        has_rag.append(file_path)

print(f"Status Tygodnia 5:")
print(f" - Pliki z generowanymi notatkami RAG: {len(has_rag)}")
print(f" - Pliki bez notatek RAG (do przetworzenia): {len(missing_rag)}")
print(f" - Pliki bez transkrypcji (pomijane): {len(no_transcript)}")

print("\nPliki do przetworzenia:")
for item in missing_rag:
    print(f"  * {os.path.basename(item['file'])}")

with open('missing_rag_week5.json', 'w', encoding='utf-8') as f:
    json.dump(missing_rag, f, indent=2, ensure_ascii=False)
print("\nZapisano listę brakujących plików do 'missing_rag_week5.json'")
