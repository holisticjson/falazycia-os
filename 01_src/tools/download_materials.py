import requests
import re
import sys
from pathlib import Path

# Ensure UTF-8 for Windows console
if sys.platform == "win32":
    import codecs
    sys.stdout = codecs.getwriter("utf-8")(sys.stdout.detach())

def download_all_storage_links():
    md_path = Path(r"c:\Aplikacje MVP\Holistic Jason\Baza_Wiedzy\Kursy_i_Szkolenia\Umiejętności_Jutra_3.0 - tydzień_2\TYDZIEŃ 2 — Pełna lista zasobów wideo i materiałów.md")
    output_dir = md_path.parent / "03_Materialy"
    output_dir.mkdir(exist_ok=True)
    
    with open(md_path, 'r', encoding='utf-8') as f:
        content = f.read()
    
    urls = re.findall(r'https://storage\.googleapis\.com/[\w\d./%?=-]+', content)
    
    print(f"Found {len(urls)} links.")
    
    for i, url in enumerate(urls, 1):
        # Extract a name or use a generic one
        name_match = re.search(r'assets%2F([\w\d-]+)', url) or re.search(r'assets/([\w\d-]+)', url)
        name = name_match.group(1) if name_match else f"material_{i}"
        out_path = output_dir / f"Promptbook_{name}.pdf"
        
        if out_path.exists():
            continue
            
        print(f"Downloading: {out_path.name}...")
        try:
            r = requests.get(url, allow_redirects=True, timeout=30)
            if r.status_code == 200:
                with open(out_path, 'wb') as f_pdf:
                    f_pdf.write(r.content)
                print("SUCCESS: Saved.")
            else:
                print(f"ERROR: HTTP {r.status_code}")
        except Exception as e:
            print(f"ERROR: {str(e)}")

if __name__ == "__main__":
    download_all_storage_links()
