import os
import pandas as pd
import pdfplumber

ROOT_DIR = "c:/Aplikacje MVP/02_knowledge_base/raw/Google Umiejętności Jutra 3.0"
WEEK5_DIR = os.path.join(ROOT_DIR, "Obsidian_Knowledge_Base", "Tydzień 5 - Transformacja i zarządzanie projektami Ai w organizacji")

def convert_pdf_to_md(pdf_path, md_path):
    text_content = f"# Zawartość pliku PDF: {os.path.basename(pdf_path)}\n\n"
    try:
        with pdfplumber.open(pdf_path) as pdf:
            for i, page in enumerate(pdf.pages):
                page_text = page.extract_text()
                if page_text:
                    text_content += f"## Strona {i+1}\n{page_text}\n\n"
        with open(md_path, 'w', encoding='utf-8') as f:
            f.write(text_content)
        print(f"Converted PDF: {os.path.basename(pdf_path)}")
    except Exception as e:
        print(f"Error reading PDF {pdf_path}: {e}")

def convert_excel_to_md(excel_path, md_path):
    text_content = f"# Zawartość arkusza: {os.path.basename(excel_path)}\n\n"
    try:
        xls = pd.ExcelFile(excel_path)
        for sheet_name in xls.sheet_names:
            df = pd.read_excel(xls, sheet_name=sheet_name)
            text_content += f"## Arkusz: {sheet_name}\n\n"
            text_content += df.to_markdown(index=False)
            text_content += "\n\n"
        with open(md_path, 'w', encoding='utf-8') as f:
            f.write(text_content)
        print(f"Converted Excel: {os.path.basename(excel_path)}")
    except Exception as e:
        print(f"Error reading Excel {excel_path}: {e}")

def main():
    print(f"Scanning for PDF and Excel files in {WEEK5_DIR}...")
    for root, dirs, files in os.walk(WEEK5_DIR):
        for file in files:
            file_path = os.path.join(root, file)
            md_path = file_path + ".md"
            
            # Skip if MD already exists
            if os.path.exists(md_path):
                continue
                
            if file.endswith('.pdf'):
                convert_pdf_to_md(file_path, md_path)
            elif file.endswith(('.xlsx', '.xls')):
                convert_excel_to_md(file_path, md_path)
            elif file.endswith('.csv'):
                try:
                    df = pd.read_csv(file_path)
                    text_content = f"# Zawartość CSV: {file}\n\n" + df.to_markdown(index=False)
                    with open(md_path, 'w', encoding='utf-8') as f:
                        f.write(text_content)
                    print(f"Converted CSV: {file}")
                except Exception as e:
                    print(f"Error reading CSV {file_path}: {e}")

if __name__ == '__main__':
    main()
