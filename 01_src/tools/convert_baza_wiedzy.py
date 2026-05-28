import os
import glob
from pathlib import Path
import subprocess
import sys

def install_dependencies():
    packages = ["docx2txt", "pandas", "openpyxl"]
    subprocess.check_call([sys.executable, "-m", "pip", "install", *packages])

try:
    import docx2txt
    import pandas as pd
except ImportError:
    install_dependencies()
    import docx2txt
    import pandas as pd

def process_docx(file_path):
    try:
        text = docx2txt.process(file_path)
        md_path = file_path.with_suffix('.md')
        with open(md_path, 'w', encoding='utf-8') as f:
            f.write(text)
        print(f"Skonwertowano DOCX: {md_path.name}")
        return md_path
    except Exception as e:
        print(f"Blad DOCX {file_path.name}: {e}")
        return None

def process_xlsx(file_path):
    try:
        # Odczyt wszystkich arkuszy
        excel_file = pd.ExcelFile(file_path)
        md_path = file_path.with_suffix('.md')
        
        with open(md_path, 'w', encoding='utf-8') as f:
            f.write(f"# Wynik konwersji: {file_path.name}\n\n")
            for sheet_name in excel_file.sheet_names:
                df = pd.read_excel(file_path, sheet_name=sheet_name)
                f.write(f"## Arkusz: {sheet_name}\n\n")
                # Konwersja DataFrame do Markdown table
                f.write(df.to_markdown(index=False))
                f.write("\n\n")
                
        print(f"Skonwertowano XLSX: {md_path.name}")
        return md_path
    except Exception as e:
        print(f"Blad XLSX {file_path.name}: {e}")
        return None

def main():
    base_dir = Path(r"c:\Aplikacje MVP\Holistic Jason\Baza_Wiedzy")
    
    # Znajdź wszystkie pliki do konwersji
    docx_files = list(base_dir.rglob("*.docx"))
    xlsx_files = list(base_dir.rglob("*.xlsx"))
    
    print(f"Znaleziono {len(docx_files)} plików DOCX i {len(xlsx_files)} plików XLSX do konwersji.")
    
    for f in docx_files:
        process_docx(f)
        
    for f in xlsx_files:
        process_xlsx(f)

if __name__ == "__main__":
    main()
