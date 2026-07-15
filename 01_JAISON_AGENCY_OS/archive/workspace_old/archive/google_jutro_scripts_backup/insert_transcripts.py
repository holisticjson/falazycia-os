import json
import os

with open('scraped_transcripts.json', 'r', encoding='utf-8') as f:
    transcripts = json.load(f)

updated_count = 0

for file_path, transcript_text in transcripts.items():
    if transcript_text == "Brak transkrypcji (twórca jej nie dodał/włączył).":
        continue

    if os.path.exists(file_path):
        with open(file_path, 'r', encoding='utf-8') as md_file:
            content = md_file.read()
            
        if '## Transkrypcja' in content:
            parts = content.split('## Transkrypcja')
            new_content = parts[0] + "## Transkrypcja\n\n" + transcript_text + "\n"
            
            with open(file_path, 'w', encoding='utf-8') as md_file:
                md_file.write(new_content)
            updated_count += 1

print(f"Zaktualizowano {updated_count} plików wprowadzając surową transkrypcję z JSON.")
