import os
from pathlib import Path
import shutil
import docx2txt
import pandas as pd
import pdfplumber

def get_existing_md_names(baza_dir: Path):
    names = set()
    for f in baza_dir.rglob("*.md"):
        names.add(f.stem.lower())
    return names

def process_docx(file_path, dest_dir):
    try:
        text = docx2txt.process(file_path)
        md_path = dest_dir / (file_path.stem + '.md')
        with open(md_path, 'w', encoding='utf-8') as f:
            f.write(text)
        safe_name = file_path.name.encode('ascii', 'ignore').decode('ascii')
        print(f"Skonwertowano DOCX: {safe_name}")
    except Exception as e:
        safe_name = file_path.name.encode('ascii', 'ignore').decode('ascii')
        print(f"Blad DOCX {safe_name}: {e}")

def process_xlsx(file_path, dest_dir):
    try:
        excel_file = pd.ExcelFile(file_path)
        md_path = dest_dir / (file_path.stem + '.md')
        with open(md_path, 'w', encoding='utf-8') as f:
            f.write(f"# Wynik konwersji: {file_path.name}\n\n")
            for sheet_name in excel_file.sheet_names:
                df = pd.read_excel(file_path, sheet_name=sheet_name)
                f.write(f"## Arkusz: {sheet_name}\n\n")
                f.write(df.to_markdown(index=False))
                f.write("\n\n")
        safe_name = file_path.name.encode('ascii', 'ignore').decode('ascii')
        print(f"Skonwertowano XLSX: {safe_name}")
    except Exception as e:
        safe_name = file_path.name.encode('ascii', 'ignore').decode('ascii')
        print(f"Blad XLSX {safe_name}: {e}")

def process_pdf(file_path, dest_dir):
    try:
        text = ""
        with pdfplumber.open(file_path) as pdf:
            for page in pdf.pages:
                page_text = page.extract_text()
                if page_text:
                    text += page_text + "\n\n"
        
        md_path = dest_dir / (file_path.stem + '.md')
        with open(md_path, 'w', encoding='utf-8') as f:
            f.write(text)
        safe_name = file_path.name.encode('ascii', 'ignore').decode('ascii')
        print(f"Skonwertowano PDF: {safe_name}")
    except Exception as e:
        safe_name = file_path.name.encode('ascii', 'ignore').decode('ascii')
        print(f"Blad PDF {safe_name}: {e}")

def main():
    baza_dir = Path(r"c:\Aplikacje MVP\Holistic Jason\Baza_Wiedzy")
    dest_dir = baza_dir / "Z_Dysku_Google"
    dest_dir.mkdir(exist_ok=True)
    
    existing_stems = get_existing_md_names(baza_dir)
    
    source_dirs = [
        Path(r"G:\Mój dysk\HOLISTIC_KNOWLEDGE_BASE"),
        Path(r"G:\Mój dysk\Kursy Szkolenia Marketing WWW A.I. APLIKACJE")
    ]
    
    processed_count = 0
    skipped_count = 0
    
    for sdir in source_dirs:
        if not sdir.exists():
            continue
            
        for file_path in sdir.rglob("*.*"):
            if file_path.is_dir() or file_path.suffix.lower() not in ['.md', '.docx', '.xlsx', '.pdf']:
                continue
                
            stem_lower = file_path.stem.lower()
            if stem_lower in existing_stems:
                skipped_count += 1
                continue
                
            safe_name = file_path.name.encode('ascii', 'ignore').decode('ascii')
            print(f"Przetwarzanie nowego pliku: {safe_name}")
            
            ext = file_path.suffix.lower()
            if ext == '.md':
                shutil.copy2(file_path, dest_dir / file_path.name)
                print(f"Skopiowano MD: {safe_name}")
            elif ext == '.docx':
                process_docx(file_path, dest_dir)
            elif ext == '.xlsx':
                process_xlsx(file_path, dest_dir)
            elif ext == '.pdf':
                process_pdf(file_path, dest_dir)
                
            existing_stems.add(stem_lower)
            processed_count += 1
            
    print(f"Zakonczono! Przetworzono nowych: {processed_count}, pominieto istniejacych: {skipped_count}")

if __name__ == "__main__":
    main()
