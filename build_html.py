import os
import re

def fix_encoding(text):
    # Fix the double encoding artifacts for Polish characters found in menu
    replacements = {
        "Krà¶lewski": "Królewski",
        "roľna": "rożna",
        "zamÃw": "zamów",
        "minutÄ™": "minutę",
        "mogÄ…": "mogą",
        "zawieraÄ‡": "zawierać",
        "Ð Ä": "", # Garbage in category
        "Zestaw dla Dzieci 🍗 Ä": "Zestaw dla Dzieci",
        "OBIADOWE ZESTAWY 🍗 Ä": "OBIADOWE ZESTAWY",
    }
    for k, v in replacements.items():
        text = text.replace(k, v)
    return text

def build():
    base_dir = "kurczakujasia_html"
    
    # CHATBOT extraction and processing
    with open("scratch/jas_chatbot_widget.html", "r", encoding="utf-8") as f:
        chatbot_full = f.read()

    # Split CSS, HTML and JS
    chatbot_css = re.search(r"<style>(.*?)</style>", chatbot_full, re.DOTALL).group(1)
    chatbot_html = re.search(r"(<div id=\"jasbot-widget\".*?</div>\n</div>)", chatbot_full, re.DOTALL).group(1)
    chatbot_js = re.search(r"<script>(.*?)</script>", chatbot_full, re.DOTALL).group(1)

    # Fix emojis in chatbot
    chicken_svg = '<svg viewBox="0 0 24 24" width="24" height="24" fill="currentColor"><path d="M19.3 4.71c-1.38-1.38-3.41-1.63-5.04-.68L8.6 9.68C8.16 10.12 8 10.74 8.1 11.35L5.7 13.76c-.39.39-1.02.39-1.41 0-.39-.39-.39-1.02 0-1.41l1.41-1.41-1.41-1.41c-1.17 1.17-1.17 3.07 0 4.24L7.12 16.6l-4.83 4.83c-.39.39-.39 1.02 0 1.41.39.39 1.02.39 1.41 0l4.83-4.83 2.83 2.83c1.17 1.17 3.07 1.17 4.24 0l-1.41-1.41-1.41 1.41c-.39.39-1.02.39-1.41 0-.39-.39-.39-1.02 0-1.41l2.41-2.41c.61.1 1.23-.06 1.67-.5l5.65-5.65c.95-1.63.7-3.66-.68-5.04zm-1.41 3.53l-5.65 5.65c-.15.15-.36.21-.57.17l-1.28-1.28c-.04-.21.02-.42.17-.57l5.65-5.65c.98-.98 2.61-.92 3.54.14.93.93.98 2.56 0 3.54z"/></svg>'
    chatbot_html = chatbot_html.replace("🍗", chicken_svg)
    chatbot_html = chatbot_html.replace("Zamów przez WhatsApp!", "Otwórz JaśBot")
    chatbot_js = chatbot_js.replace("🍗", "")
    
    with open(f"{base_dir}/assets/js/chatbot.js", "w", encoding="utf-8") as f:
        f.write(chatbot_js)

    # Common HTML Shell
    header_html = f"""<!DOCTYPE html>
<html lang="pl">
<head>
    <meta charset="UTF-8">
    <meta name="viewport" content="width=device-width, initial-scale=1.0">
    <title>Bar Jaś - Kurczak z rożna w Łodzi</title>
    <link rel="stylesheet" href="assets/css/style.css">
    <style>{chatbot_css}</style>
</head>
<body>

<header class="site-header">
    <div class="site-logo">
        <a href="index.html" style="text-decoration:none;">
            <h1 class="retro-title" style="color:var(--dark-brown); margin:0;">BAR JAŚ</h1>
        </a>
    </div>
    <nav class="main-navigation" id="main-nav">
        <ul>
            <li><a href="index.html" class="nav-link">Home</a></li>
            <li><a href="menu.html" class="nav-link">Menu</a></li>
            <li><a href="onas.html" class="nav-link">O Nas</a></li>
            <li><a href="kontakt.html" class="nav-link">Kontakt</a></li>
            <li>
                <a href="tel:+48663970016" class="jas-btn jas-btn-secondary" style="padding:8px 16px; font-size:1rem; border-radius:0.8rem;">
                    <svg class="jas-icon" viewBox="0 0 24 24" style="width:16px;height:16px;margin-right:6px;"><path d="M6.62 10.79c1.44 2.83 3.76 5.14 6.59 6.59l2.2-2.2c.27-.27.67-.36 1.02-.24 1.12.37 2.33.57 3.57.57.55 0 1 .45 1 1V20c0 .55-.45 1-1 1-9.39 0-17-7.61-17-17 0-.55.45-1 1-1h3.5c.55 0 1 .45 1 1 0 1.25.2 2.45.57 3.57.11.35.03.74-.25 1.02l-2.2 2.2z"/></svg>
                    ZAMÓW TERAZ
                </a>
            </li>
        </ul>
    </nav>
    <div class="mobile-menu-toggle" id="mobile-toggle">
        <svg viewBox="0 0 24 24" width="24" height="24" fill="var(--cream-bg)"><path d="M3 18h18v-2H3v2zm0-5h18v-2H3v2zm0-7v2h18V6H3z"/></svg>
    </div>
</header>
"""

    footer_html = f"""
{chatbot_html}
<footer class="site-footer">
    <div style="max-width: 1200px; margin: 0 auto; display: flex; flex-direction: column; gap: 20px; align-items: center;">
        <h2 class="retro-title" style="color:var(--primary-color);">BAR JAŚ</h2>
        <p>Najlepszy kurczak z rożna w Łodzi od ponad 20 lat.</p>
        <p><strong>Poniedziałek – Sobota:</strong> 09:00 – 19:00<br><strong>Niedziela:</strong> Zamknięte</p>
        <div style="display:flex; gap: 20px; margin-top:10px;">
            <a href="kontakt.html">Kontakt</a>
            <a href="polityka.html">Polityka Prywatności i RODO</a>
        </div>
        <p style="margin-top:20px; font-size:0.9rem; opacity:0.8;">&copy; 2026 Bar Jaś. Wszelkie prawa zastrzeżone.</p>
    </div>
</footer>

<script src="assets/js/main.js"></script>
<script src="assets/js/chatbot.js"></script>
</body>
</html>
"""

    # MAIN JS
    js_content = """
document.addEventListener("DOMContentLoaded", () => {
    // Highlight active link
    const path = window.location.pathname;
    const page = path.split("/").pop() || "index.html";
    document.querySelectorAll('.nav-link').forEach(link => {
        if (link.getAttribute('href') === page || (page==="" && link.getAttribute('href')==="index.html")) {
            link.classList.add('active');
        }
    });

    // Mobile menu toggle
    const toggle = document.getElementById("mobile-toggle");
    const nav = document.getElementById("main-nav");
    if(toggle && nav) {
        toggle.addEventListener("click", () => {
            nav.classList.toggle("open");
        });
    }
});
"""
    with open(f"{base_dir}/assets/js/main.js", "w", encoding="utf-8") as f:
        f.write(js_content)

    # PROCESS PAGES
    pages = {
        "index.html": "scratch/previews/home_preview.html",
        "onas.html": "scratch/previews/onas_preview.html",
        "kontakt.html": "scratch/previews/kontakt_preview.html",
        "menu.html": "scratch/previews/menu_new_preview.html"
    }

    for out_name, in_path in pages.items():
        if os.path.exists(in_path):
            with open(in_path, "r", encoding="utf-8") as f:
                content = f.read()

            # Clean WP artifacts
            content = content.replace("<!-- wp:html -->", "").replace("<!-- /wp:html -->", "")
            
            # Apply bug fixes
            content = fix_encoding(content)
            
            # Home fixes
            if out_name == "index.html":
                # Fix phone number bug
                content = content.replace("Zadzwoń: +48 +48 +48 663 970 016", "Zadzwoń: +48 663 970 016")
                
                # Fix TrustIndex text color
                content += "\n<style>.ti-widget .ti-review-item .ti-review-content { color: #2D1A1E !important; }</style>\n"
                
                # Add SVGs to Hero buttons
                content = content.replace('Sprawdź Nasze Menu', '<svg class="jas-icon" viewBox="0 0 24 24" style="margin-right:8px;"><path d="M4 6H2v14c0 1.1.9 2 2 2h14v-2H4V6zm16-4H8c-1.1 0-2 .9-2 2v12c0 1.1.9 2 2 2h12c1.1 0 2-.9 2-2V4c0-1.1-.9-2-2-2zm0 14H8V4h12v12z"/></svg> Sprawdź Nasze Menu')
                content = content.replace('Zadzwoń: +48 663 970 016', '<svg class="jas-icon" viewBox="0 0 24 24" style="margin-right:8px;"><path d="M6.62 10.79c1.44 2.83 3.76 5.14 6.59 6.59l2.2-2.2c.27-.27.67-.36 1.02-.24 1.12.37 2.33.57 3.57.57.55 0 1 .45 1 1V20c0 .55-.45 1-1 1-9.39 0-17-7.61-17-17 0-.55.45-1 1-1h3.5c.55 0 1 .45 1 1 0 1.25.2 2.45.57 3.57.11.35.03.74-.25 1.02l-2.2 2.2z"/></svg> Zadzwoń: +48 663 970 016')

            if out_name == "kontakt.html":
                content = content.replace("ZAMÓWIENIA I ODBIÓR", "KONTAKT TELEFONICZNY")
                content = re.sub(r"Pon - Pt.*?18:00", "Poniedziałek – Sobota: 09:00 – 19:00", content, flags=re.DOTALL)
                content = re.sub(r"Sobota.*?14:00", "Niedziela: Zamknięte", content, flags=re.DOTALL)

            # Write full file
            with open(f"{base_dir}/{out_name}", "w", encoding="utf-8") as f:
                f.write(header_html + "\n" + content + "\n" + footer_html)
                
            print(f"Built {out_name}")

if __name__ == "__main__":
    build()
