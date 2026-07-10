import os
import re
import sys
from PIL import Image, ImageDraw, ImageFont

def get_font(font_name="Arial", size=40):
    """Próbuje wczytać czcionkę z systemu Windows lub zwraca domyślną."""
    # Lista typowych ścieżek do czcionek w systemie Windows
    system_fonts_dirs = [
        r"C:\Windows\Fonts",
        r"C:\Users\tomas_yq1b9su\AppData\Local\Microsoft\Windows\Fonts"
    ]
    
    font_files = {
        "Montserrat-Bold": "Montserrat-Bold.ttf",
        "Montserrat-Regular": "Montserrat.ttf",
        "Arial-Bold": "arialbd.ttf",
        "Arial": "arial.ttf",
        "SegoeUI-Bold": "segoeuib.ttf",
        "SegoeUI": "segoeui.ttf"
    }

    # Wybór pliku dla danej nazwy czcionki
    target_file = font_files.get(font_name, "arial.ttf")
    
    for fonts_dir in system_fonts_dirs:
        full_path = os.path.join(fonts_dir, target_file)
        if os.path.exists(full_path):
            try:
                return ImageFont.truetype(full_path, size)
            except Exception:
                continue
                
    # Fallback do standardowych czcionek systemowych
    try:
        return ImageFont.truetype("arial.ttf", size)
    except Exception:
        return ImageFont.load_default()

def wrap_text(text, font, max_width, draw):
    """Dzieli tekst na linie, które zmieszczą się w max_width."""
    words = text.split()
    lines = []
    current_line = []
    
    for word in words:
        test_line = ' '.join(current_line + [word])
        # textlength liczy szerokość w pikselach
        if draw.textlength(test_line, font=font) <= max_width:
            current_line.append(word)
        else:
            if current_line:
                lines.append(' '.join(current_line))
            current_line = [word]
            
    if current_line:
        lines.append(' '.join(current_line))
        
    return lines

def generate_carousel(text_content, output_dir="output_carousel"):
    """
    Generuje zestaw slajdów PNG (1080x1080) na podstawie tekstu podzielonego za pomocą '---'.
    """
    os.makedirs(output_dir, exist_ok=True)
    
    # Podział na slajdy z obsługą spacji wokół separatorów
    slides_raw = re.split(r'\n\s*---\s*\n|\n\s*---\s*|\n\s*===\s*', text_content)
    slides = [s.strip() for s in slides_raw if s.strip()]

    total_slides = len(slides)
    
    # Kolory motywu Jaison (ciemny niebieski/navy, biel, akcent niebieski)
    bg_color = (15, 23, 42)      # #0f172a (Slate 900)
    text_color = (255, 255, 255)  # #ffffff (White)
    accent_color = (56, 189, 248) # #38bdf8 (Sky 400)
    muted_color = (148, 163, 184) # #94a3b8 (Slate 400)
    
    # Wymiary slajdu
    width, height = 1080, 1080
    margin = 100
    max_text_width = width - (2 * margin)
    
    for i, slide_text in enumerate(slides):
        img = Image.new('RGB', (width, height), color=bg_color)
        draw = ImageDraw.Draw(img)
        
        # Pobieranie czcionek
        title_font = get_font("SegoeUI-Bold", 55)
        body_font = get_font("SegoeUI", 38)
        meta_font = get_font("SegoeUI-Bold", 32)
        
        lines = slide_text.split('\n')
        # Oddziel nagłówek (pierwsza linia, jeśli zaczyna się od #)
        title = ""
        body_start_idx = 0
        if lines and lines[0].startswith('#'):
            title = lines[0].lstrip('#').strip()
            body_start_idx = 1
            
        body_text = '\n'.join(lines[body_start_idx:]).strip()
        
        y_offset = 180
        
        # Rysowanie tytułu
        if title:
            wrapped_title = wrap_text(title, title_font, max_text_width, draw)
            for line in wrapped_title:
                draw.text((margin, y_offset), line, font=title_font, fill=accent_color)
                y_offset += 75
            y_offset += 40  # Dodatkowy odstęp po tytule
            
        # Rysowanie treści
        if body_text:
            # Rozbij na akapity i zawijaj
            paragraphs = body_text.split('\n\n')
            for p in paragraphs:
                p_lines = wrap_text(p, body_font, max_text_width, draw)
                for line in p_lines:
                    draw.text((margin, y_offset), line, font=body_font, fill=text_color)
                    y_offset += 55
                y_offset += 30  # Odstęp między akapitami
                
        # Rysowanie brandingowego nagłówka i stopki (ADHD-friendly Visual Anchors)
        # Stopka: Jaison.pl (lewy dół)
        draw.text((margin, height - 90), "jaison.pl", font=meta_font, fill=accent_color)
        
        # Stopka: Numeracja slajdów (prawy dół)
        slide_num_str = f"{i + 1} / {total_slides}"
        slide_num_w = draw.textlength(slide_num_str, font=meta_font)
        draw.text((width - margin - slide_num_w, height - 90), slide_num_str, font=meta_font, fill=muted_color)
        
        # Zapis slajdu
        slide_file = os.path.join(output_dir, f"slide_{i+1:02d}.png")
        img.save(slide_file, "PNG")
        print(f"Generated slide: {slide_file}")
        
    print(f"=== SUCCESSFULLY GENERATED {total_slides} SLIDES IN {output_dir} ===")

if __name__ == "__main__":
    test_text = """
    # Jak zbudować lejek w Systeme.io
    Dowiedz się, jak założyć darmowe konto, podpiąć webhooki n8n oraz zachować pełne bezpieczeństwo danych.
    ---
    # Krok 1: Wybór Domeny
    Zawsze wybieraj domenę biznesową. Rejestrując się na GCP wybierz typ konta 'Business' zamiast 'Individual', aby poprawnie odliczać koszty.
    ---
    # Krok 2: Klonowanie Głosu
    Używaj modelu VoxCPM2 do lokalnego klonowania głosu. Daje to studyjną jakość 48kHz bez żadnych opłat abonamentowych.
    """
    generate_carousel(test_text)
