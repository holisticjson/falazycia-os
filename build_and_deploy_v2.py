#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
MASTER BUILD SCRIPT v2.0 — kurczakujasia.pl
Naprawia WSZYSTKIE błędy z audytu i wdraża przez FTP.
"""
import os, re, shutil, ftplib

# === CONFIG ===
SRC_DIR   = "04_clients/kurczakujasia/kurczakujasia_html"
BUILD_DIR = "04_clients/kurczakujasia/kurczakujasia_html"
LOGO_SRC  = "04_clients/kurczakujasia/logo/Logo Bar Jaś.png"
LOGO_DEST = f"{BUILD_DIR}/assets/img/logo.png"

FTP_HOST  = "kurczakujasia.pl"
FTP_USER  = "deploy@kurczakujasia.pl"
FTP_PASS  = "Kosmos!!@@1234"
FTP_ROOT  = "public_html"

os.makedirs(f"{BUILD_DIR}/assets/css", exist_ok=True)
os.makedirs(f"{BUILD_DIR}/assets/js",  exist_ok=True)
os.makedirs(f"{BUILD_DIR}/assets/img", exist_ok=True)

# -------------------------------------------------------
# LOGO: kopiuj plik
# -------------------------------------------------------
shutil.copy2(LOGO_SRC, LOGO_DEST)
print(f"✅ Logo skopiowane -> {LOGO_DEST}")

# -------------------------------------------------------
# STYLE.CSS — poprawiony (sticky header, hover, brak !imp)
# -------------------------------------------------------
CSS = """
@import url('https://fonts.googleapis.com/css2?family=Fredoka:wght@600;700&family=Plus+Jakarta+Sans:wght@400;500;700;800&display=swap');

:root {
  --primary:    #FCC036;
  --primary-dk: #E0A51B;
  --red:        #D32F2F;
  --red-dk:     #A01828;
  --dark:       #2D1A1E;
  --cream:      #FAF6EE;
  --white:      #FFFFFF;
  --shadow:     4px 4px 0px var(--dark);
  --shadow-lg:  6px 6px 0px var(--dark);
  --radius:     1rem;
  --border:     3px solid var(--dark);
}

*, *::before, *::after { box-sizing: border-box; }

html, body {
  max-width: 100%;
  overflow-x: hidden;
  margin: 0; padding: 0;
}

body {
  font-family: 'Plus Jakarta Sans', sans-serif;
  background-color: var(--cream);
  color: var(--dark);
  line-height: 1.6;
}

h1, h2, h3, h4, h5, h6 {
  font-family: 'Fredoka', sans-serif;
  text-transform: uppercase;
  font-weight: 700;
  margin: 0;
}

img { max-width: 100%; height: auto; display: block; }

/* === HEADER (STICKY) === */
.site-header {
  background-color: var(--cream);
  border-bottom: 4px solid var(--dark);
  position: sticky;
  top: 0;
  z-index: 1000;
  display: flex;
  justify-content: space-between;
  align-items: center;
  padding: 8px 5%;
  gap: 20px;
}

.site-logo-link { text-decoration: none; display: flex; align-items: center; }
.site-logo-link img { height: 62px; width: auto; }

.main-navigation ul {
  list-style: none;
  display: flex;
  gap: 18px;
  margin: 0; padding: 0;
  align-items: center;
}

.main-navigation a {
  text-decoration: none;
  color: var(--dark);
  font-family: 'Fredoka', sans-serif;
  font-size: 1.05rem;
  text-transform: uppercase;
  letter-spacing: 0.5px;
  transition: color 0.2s;
}

.main-navigation a:hover,
.main-navigation a.active { color: var(--red); }

/* === BUTTONS === */
.jas-btn {
  font-family: 'Fredoka', sans-serif;
  border-radius: var(--radius);
  border: var(--border);
  box-shadow: var(--shadow);
  transition: all 0.2s ease;
  text-decoration: none;
  display: inline-flex;
  align-items: center;
  justify-content: center;
  gap: 8px;
  padding: 10px 22px;
  font-size: 1.05rem;
  cursor: pointer;
  text-transform: uppercase;
}

.jas-btn-primary {
  background-color: var(--primary);
  color: var(--dark);
}
.jas-btn-primary:hover {
  background-color: var(--primary-dk);
  transform: translate(-2px, -2px);
  box-shadow: var(--shadow-lg);
}

.jas-btn-secondary {
  background-color: var(--red);
  color: var(--white);
}
.jas-btn-secondary:hover {
  background-color: var(--red-dk);
  transform: translate(-2px, -2px);
  box-shadow: var(--shadow-lg);
}

.jas-btn-outline {
  background-color: transparent;
  color: var(--primary);
  border-color: var(--primary);
  box-shadow: 3px 3px 0px var(--primary);
}
.jas-btn-outline:hover {
  background-color: rgba(252,192,54,0.12);
  transform: translate(-2px, -2px);
  box-shadow: 5px 5px 0px var(--primary);
}

/* === FOOTER === */
.site-footer {
  background-color: var(--dark);
  color: var(--cream);
  border-top: 3px solid var(--primary);
  padding: 48px 5% 32px;
}
.footer-inner {
  max-width: 1100px;
  margin: 0 auto;
  display: grid;
  grid-template-columns: repeat(auto-fit, minmax(220px, 1fr));
  gap: 32px;
}
.footer-title {
  font-family: 'Fredoka', sans-serif;
  color: var(--primary);
  font-size: 1.5rem;
  text-transform: uppercase;
  margin-bottom: 16px;
  display: flex;
  align-items: center;
  gap: 10px;
}
.footer-title img { height: 40px; width: auto; }
.site-footer a { color: var(--primary); text-decoration: none; transition: color 0.2s; }
.site-footer a:hover { color: var(--red); }
.footer-bottom {
  text-align: center;
  margin-top: 32px;
  padding-top: 20px;
  border-top: 1px solid rgba(252,192,54,0.2);
  font-size: 0.85rem;
  opacity: 0.7;
}

/* === MOBILE NAV === */
.mobile-menu-toggle {
  display: none;
  background: var(--primary);
  border: var(--border);
  border-radius: 50%;
  width: 46px; height: 46px;
  cursor: pointer;
  box-shadow: 2px 2px 0px var(--dark);
  align-items: center;
  justify-content: center;
  flex-shrink: 0;
}

@media (max-width: 921px) {
  .mobile-menu-toggle { display: flex; }
  .main-navigation {
    display: none;
    position: absolute;
    top: 100%; left: 0; right: 0;
    background: var(--cream);
    border-bottom: 3px solid var(--dark);
    padding: 16px 5%;
    flex-direction: column;
    align-items: stretch;
  }
  .main-navigation.open { display: flex; }
  .main-navigation ul { flex-direction: column; width: 100%; gap: 0; }
  .main-navigation ul li {
    text-align: center;
    border-bottom: 1px solid rgba(45,26,30,0.1);
    padding: 12px 0;
  }
  .main-navigation ul li:last-child { border-bottom: none; }
}

/* === CONTENT CONTAINERS === */
.jas-home-container, .jas-about-container, .jas-menu-container, .jas-contact-container {
  max-width: 1200px;
  margin: 2rem auto;
  padding: 2rem 1.5rem;
  background-color: var(--cream);
  border-radius: 2rem;
  border: var(--border);
  box-shadow: var(--shadow);
}

@media (max-width: 768px) {
  .jas-home-container, .jas-about-container, .jas-menu-container, .jas-contact-container {
    margin: 1rem 0.75rem;
    padding: 1.2rem 1rem;
    border-radius: 1.5rem;
  }
}

/* === HERO === */
.jas-home-hero {
  text-align: center;
  padding: 5rem 1.5rem;
  background: linear-gradient(135deg, rgba(45,26,30,0.78) 0%, rgba(45,26,30,0.88) 100%),
              url('https://kurczakujasia.pl/wp-content/uploads/2023/11/Kurczak-z-rozna-Bar-Jas.png') center/cover;
  border-radius: 1.5rem;
  border: var(--border);
  box-shadow: var(--shadow);
  margin-bottom: 3rem;
}

.jas-home-hero h1 {
  font-family: 'Fredoka', sans-serif;
  font-size: clamp(2.2rem, 5vw, 3.8rem);
  color: var(--primary);
  text-shadow: 3px 3px 0px var(--red), 6px 6px 0px var(--dark);
  margin-bottom: 1.2rem;
  line-height: 1.1;
}

.jas-home-hero p {
  font-size: clamp(1rem, 2.5vw, 1.3rem);
  font-weight: 700;
  color: var(--cream);
  max-width: 720px;
  margin: 0 auto 2rem;
  text-shadow: 0 2px 8px rgba(0,0,0,0.6);
}

.jas-hero-cta-group {
  display: flex;
  justify-content: center;
  flex-wrap: wrap;
  gap: 1rem;
}

/* === REVIEWS SECTION === */
.jas-reviews-section {
  background: var(--dark);
  border-radius: 1.5rem;
  padding: 2.5rem 1.5rem;
  border: var(--border);
  box-shadow: var(--shadow);
  margin-top: 2rem;
}
.jas-reviews-section h2 {
  color: var(--primary);
  text-align: center;
  margin-bottom: 2rem;
}
.jas-reviews-grid {
  display: grid;
  grid-template-columns: repeat(auto-fit, minmax(260px, 1fr));
  gap: 1.2rem;
}
.jas-review-card {
  background: var(--white);
  border-radius: 1.2rem;
  border: 3px solid var(--dark);
  box-shadow: 4px 4px 0px var(--dark);
  padding: 1.2rem;
  color: var(--dark) !important;
}
.jas-review-card .stars {
  color: #FCC036;
  font-size: 1.2rem;
  margin-bottom: 0.5rem;
}
.jas-review-card p {
  color: var(--dark) !important;
  font-size: 0.95rem;
  line-height: 1.5;
  margin: 0.5rem 0;
}
.jas-review-card .reviewer {
  color: var(--dark) !important;
  font-weight: 700;
  font-size: 0.9rem;
  margin-top: 0.5rem;
}

/* FAQ */
.jas-faq-section { margin-top: 2rem; }
.jas-faq-section h2 { margin-bottom: 1.5rem; color: var(--dark); text-align: center; }
.jas-faq-item {
  background: var(--white);
  border: var(--border);
  border-radius: var(--radius);
  box-shadow: var(--shadow);
  margin-bottom: 1rem;
  overflow: hidden;
}
.jas-faq-item summary {
  padding: 1rem 1.5rem;
  cursor: pointer;
  font-family: 'Fredoka', sans-serif;
  font-size: 1.1rem;
  list-style: none;
  display: flex;
  justify-content: space-between;
  align-items: center;
  transition: background 0.2s;
}
.jas-faq-item summary:hover { background: rgba(252,192,54,0.1); }
.jas-faq-item[open] summary { background: rgba(252,192,54,0.15); }
.jas-faq-item p { padding: 0.5rem 1.5rem 1.2rem; margin: 0; }

/* JASBOT LABEL */
.jasbot-label {
  position: fixed;
  bottom: 2.8rem;
  right: 7rem;
  background: var(--dark);
  color: var(--cream);
  padding: 8px 14px;
  border-radius: 12px;
  font-size: 0.8rem;
  font-weight: 700;
  font-family: 'Plus Jakarta Sans', sans-serif;
  white-space: nowrap;
  z-index: 9999;
  pointer-events: none;
  border: 2px solid var(--primary);
  box-shadow: 3px 3px 0px var(--dark);
  animation: jasbot-label-pulse 3s ease-in-out infinite;
}
@keyframes jasbot-label-pulse {
  0%,100% { opacity: 0.95; transform: translateY(0); }
  50%      { opacity: 1;    transform: translateY(-3px); }
}
"""
with open(f"{BUILD_DIR}/assets/css/style.css", "w", encoding="utf-8") as f:
    f.write(CSS)
print("✅ style.css zapisany")

# -------------------------------------------------------
# MASTER_MENU — CENTRALNA BAZA DAŃ (13 pozycji)
# -------------------------------------------------------
import json

MASTER_MENU = [
    {
        "id": 1,
        "id_str": "set-chicken-whole",
        "name": "Zestaw Kurczak z Rożna (Cały)",
        "category": "sets",
        "price": 52,
        "desc": "Cały soczysty kurczak z rożna (~900g) + duża porcja złocistych frytek (300g) lub opiekanych ziemniaczków + duży zestaw 3 świeżych domowych surówek (300g) + sos autorski czosnkowy i pikantny gratis!",
        "badge": "DLA RODZINY 👨‍👩‍👧‍👦",
        "image": "https://kurczakujasia.pl/wp-content/uploads/2023/12/Kurczak-z-rozna_zestaw-z-surowkami_frytki-1.png"
    },
    {
        "id": 2,
        "id_str": "set-chicken-half",
        "name": "Zestaw Kurczak z Rożna (Połówka)",
        "category": "sets",
        "price": 34,
        "desc": "Połówka chrupiącego kurczaka (~450g) + złociste frytki (150g) lub opiekane ziemniaczki + zestaw 3 świeżych domowych surówek (150g) + sos autorski czosnkowy lub pikantny gratis!",
        "badge": "KULTOWE 🔥",
        "image": "https://kurczakujasia.pl/wp-content/uploads/2023/12/Kurczak-z-rozna_zestaw-z-surowkami_frytki-1.png"
    },
    {
        "id": 3,
        "id_str": "chicken-whole",
        "name": "Legendarny Kurczak z Rożna (Cały)",
        "category": "sets",
        "price": 38,
        "desc": "Cały dorodny kurczak z polskiej hodowli (~900g), ręcznie marynowany w autorskiej kompozycji 12 ziół, pieczony na złocisty kolor (sama sztuka bez dodatków)",
        "badge": "BESTSELLER 👑",
        "image": "https://kurczakujasia.pl/wp-content/uploads/2023/12/Kurczak-z-rozna_zestaw-z-surowkami_frytki-1.png"
    },
    {
        "id": 4,
        "id_str": "chicken-half",
        "name": "Kurczak z Rożna (Połówka)",
        "category": "sets",
        "price": 20,
        "desc": "Sama połówka soczystego kurczaka (~450g) o chrupiącej, złotej skórce, świeżo pieczona na tradycyjnym rożnie obrotowym (sama sztuka, bez dodatków)",
        "badge": None,
        "image": "https://kurczakujasia.pl/wp-content/uploads/2023/12/Kurczak-z-rozna_zestaw-z-surowkami_frytki-1.png"
    },
    {
        "id": 5,
        "id_str": "set-kebab",
        "name": "Zestaw Kebab z Frytkami i Surówkami",
        "category": "sets",
        "price": 32,
        "desc": "Sycąca porcja dobrze przypieczonego mięsa kebab (~180g) + frytki (150g) + zestaw 3 świeżych surówek (150g) + sos autorski czosnkowy lub pikantny",
        "badge": "HIT 👍",
        "image": "https://kurczakujasia.pl/wp-content/uploads/2026/07/kebab_z_frytkami.png"
    },
    {
        "id": 6,
        "id_str": "kebab-bun",
        "name": "Kebab w Bułce z Surówkami",
        "category": "kebab",
        "price": 22,
        "desc": "Opiekana rzemieślnicza bułka z dużą ilością mięsa kebab (~150g), świeżą kapustą, pomidorem, ogórkiem, cebulką i domowym sosem (czosnek/ostry/mieszany)",
        "badge": None,
        "image": "https://kurczakujasia.pl/wp-content/uploads/2026/07/kebab_w_bulce.png"
    },
    {
        "id": 7,
        "id_str": "burger-chicken",
        "name": "Hamburger z Filetem z Kurczaka",
        "category": "kebab",
        "price": 20,
        "desc": "Chrupiący, świeżo smażony panierowany filet z piersi kurczaka (~150g) w bułce sezamowej z pomidorem, ogórkiem, sałatą i wyrazistym sosem burgerowym",
        "badge": "DLA GŁODNYCH ⚡",
        "image": "https://kurczakujasia.pl/wp-content/uploads/2023/12/Hamburger-z-filetem-z-kurczaka-2-1.png"
    },
    {
        "id": 8,
        "id_str": "set-kids",
        "name": "Smerf – Zestaw dla Dzieci",
        "category": "sets",
        "price": 18,
        "desc": "Delikatne domowe kąski z piersi kurczaka (~100g) + frytki (100g) + łagodny ketchup + zimny soczek owocowy w kartoniku (200ml)",
        "badge": "DLA DZIECI 👦",
        "image": "https://kurczakujasia.pl/wp-content/uploads/2026/07/zestaw_dla_dzieci.png"
    },
    {
        "id": 9,
        "id_str": "soup-day",
        "name": "Domowa Zupa Dnia",
        "category": "sides",
        "price": 10,
        "desc": "Pyszna, gorąca zupa (350ml) gotowana codziennie rano na świeżych warzywach i mięsie (np. pomidorowa, rosół z makaronem rzemieślniczym lub żurek — zapytaj nas o dzisiejszą!)",
        "badge": "ŚWIEŻA 🍲",
        "image": "https://images.unsplash.com/photo-1547592180-85f173990554?auto=format&fit=crop&w=600&q=80"
    },
    {
        "id": 10,
        "id_str": "fries",
        "name": "Złociste Frytki (Porcja 150g)",
        "category": "sides",
        "price": 10,
        "desc": "Chrupiące na zewnątrz, miękkie i puszyste w środku złociste frytki, idealnie usmażone i posolone",
        "badge": None,
        "image": "https://images.unsplash.com/photo-1573080496219-bb080dd4f877?auto=format&fit=crop&w=600&q=80"
    },
    {
        "id": 11,
        "id_str": "potatoes",
        "name": "Opiekane Ziemniaczki (Porcja 150g)",
        "category": "sides",
        "price": 10,
        "desc": "Aromatyczne, złociste połówki ziemniaczków pieczone w ziołach, miękkie w środku i chrupiące z wierzchu",
        "badge": None,
        "image": "https://images.unsplash.com/photo-1573080496219-bb080dd4f877?auto=format&fit=crop&w=600&q=80"
    },
    {
        "id": 12,
        "id_str": "salads",
        "name": "Zestaw Domowych Surówek",
        "category": "sides",
        "price": 8,
        "desc": "Świeża, witaminowa porcja (150g) trzech domowych surówek (biała kapusta, czerwona kapusta, marchewka) przygotowywana codziennie na miejscu",
        "badge": "WITAMINY 🥗",
        "image": "https://images.unsplash.com/photo-1512621776951-a57141f2eefd?auto=format&fit=crop&w=600&q=80"
    },
    {
        "id": 13,
        "id_str": "drinks",
        "name": "Zimne Napoje (Pepsi / Mirinda 0.33l)",
        "category": "drinks",
        "price": 8,
        "desc": "Zimna, orzeźwiająca puszka Pepsi, Pepsi Zero, Mirinda lub 7Up (0.33l) prosto z lodówki",
        "badge": None,
        "image": "https://images.unsplash.com/photo-1622483767028-3f66f32aef97?auto=format&fit=crop&w=600&q=80"
    }
]

chatbot_items = []
menu_items = []

for item in MASTER_MENU:
    chatbot_items.append({
        "id": item["id"],
        "name": item["name"],
        "price": item["price"],
        "desc": item["desc"]
    })
    menu_items.append({
        "id": item["id_str"],
        "name": item["name"],
        "category": item["category"],
        "price": float(item["price"]),
        "description": item["desc"],
        "badge": item["badge"],
        "image": item["image"]
    })

chatbot_items_js = json.dumps(chatbot_items, ensure_ascii=False, indent=2)
menu_items_js = json.dumps(menu_items, ensure_ascii=False, indent=2)

# -------------------------------------------------------
# CHATBOT JS — z czytelnym tooltipem i labelką
# -------------------------------------------------------
CHATBOT_HTML = """
<div id="jasbot-widget">
  <div class="jasbot-label" id="jasbot-label">🍗 Złóż zamówienie u JaśBota!</div>
  <div class="jasbot-toggle" id="jasbot-toggle" aria-label="Otwórz chat JaśBot">
    <img src="assets/img/logo.png" alt="JaśBot" style="width:42px;height:42px;object-fit:contain;border-radius:50%;">
    <div class="jasbot-badge" id="jasbot-badge" style="display:none;">0</div>
  </div>
  <div class="jasbot-window" id="jasbot-window" role="dialog" aria-label="Chat z JaśBotem">
    <div class="jasbot-header">
      <div class="jasbot-header-info">
        <img src="assets/img/logo.png" alt="JaśBot Logo" class="jasbot-avatar-img" style="width:40px;height:40px;object-fit:contain;border-radius:50%;background:var(--cream);">
        <div class="jasbot-header-text">
          <h3>JaśBot</h3>
          <p>Złóż zamówienie online!</p>
        </div>
      </div>
      <button class="jasbot-close-btn" id="jasbot-close-btn" aria-label="Zamknij chat">&times;</button>
    </div>
    <div class="jasbot-body" id="jasbot-messages"></div>
    <div class="jasbot-input-area">
      <input type="text" class="jasbot-input" id="jasbot-input" placeholder="Wpisz wiadomość..." autocomplete="off">
      <button class="jasbot-send-btn" id="jasbot-send-btn" aria-label="Wyślij">
        <svg viewBox="0 0 24 24" width="20" height="20" fill="currentColor"><path d="M2.01 21L23 12 2.01 3 2 10l15 2-15 2z"/></svg>
      </button>
    </div>
  </div>
</div>
"""

CHATBOT_CSS = """
#jasbot-widget { position:fixed; bottom:2rem; right:2rem; z-index:10000; font-family:'Plus Jakarta Sans',sans-serif; }
.jasbot-toggle { width:65px; height:65px; background:#D32F2F; border-radius:50%; display:flex; align-items:center; justify-content:center; cursor:pointer; box-shadow:0px 8px 24px rgba(211,47,47,0.4),3px 3px 0px #2D1A1E; border:3px solid #FCC036; transition:all 0.3s cubic-bezier(0.175,0.885,0.32,1.275); position:relative; }
.jasbot-toggle:hover { transform:scale(1.12) rotate(8deg); }
.jasbot-badge { position:absolute; top:-5px; right:-5px; background:#FCC036; color:#2D1A1E; font-weight:800; font-size:0.8rem; width:22px; height:22px; border-radius:50%; display:flex; align-items:center; justify-content:center; border:2px solid #fff; }
.jasbot-window { position:fixed; bottom:7.5rem; right:2rem; width:380px; height:520px; background:#FAF6EE; border:3px solid #2D1A1E; border-radius:1.5rem; box-shadow:0px 15px 40px rgba(0,0,0,0.15),6px 6px 0px #2D1A1E; display:flex; flex-direction:column; overflow:hidden; transform:scale(0.8) translateY(50px); opacity:0; pointer-events:none; transition:all 0.3s cubic-bezier(0.175,0.885,0.32,1.275); z-index:10001; }
.jasbot-window.open { transform:scale(1) translateY(0); opacity:1; pointer-events:all; }
.jasbot-header { background:#2D1A1E; padding:1rem 1.2rem; display:flex; align-items:center; justify-content:space-between; }
.jasbot-header-info { display:flex; align-items:center; gap:0.8rem; }
.jasbot-header-text h3 { font-family:'Fredoka',sans-serif; color:#FCC036; font-size:1.1rem; margin:0; }
.jasbot-header-text p { color:#FAF6EE; font-size:0.8rem; margin:0; opacity:0.8; }
.jasbot-close-btn { background:none; border:none; color:#FAF6EE; font-size:1.5rem; cursor:pointer; opacity:0.7; transition:opacity 0.2s; }
.jasbot-close-btn:hover { opacity:1; }
.jasbot-body { flex:1; overflow-y:auto; padding:1rem; display:flex; flex-direction:column; gap:0.8rem; }
.jasbot-msg { max-width:80%; padding:0.7rem 1rem; border-radius:1rem; font-size:0.9rem; line-height:1.4; }
.jasbot-msg.bot { background:#FCC036; color:#2D1A1E; border:2px solid #2D1A1E; border-radius:1rem 1rem 1rem 0; align-self:flex-start; }
.jasbot-msg.user { background:#2D1A1E; color:#FAF6EE; border-radius:1rem 1rem 0 1rem; align-self:flex-end; }
.jasbot-input-area { display:flex; padding:0.8rem; gap:0.5rem; border-top:2px solid #2D1A1E; background:#fff; }
.jasbot-input { flex:1; padding:0.6rem 1rem; border:2px solid #2D1A1E; border-radius:0.8rem; font-family:'Plus Jakarta Sans',sans-serif; font-size:0.9rem; background:#FAF6EE; }
.jasbot-input:focus { outline:none; border-color:#D32F2F; }
.jasbot-send-btn { background:#D32F2F; color:#fff; border:2px solid #2D1A1E; border-radius:0.8rem; padding:0.5rem 0.8rem; cursor:pointer; transition:background 0.2s; }
.jasbot-send-btn:hover { background:#A01828; }
.jasbot-cart-bar { display:none; position:fixed; bottom:0; left:0; right:0; background:#2D1A1E; color:#FAF6EE; padding:0.8rem 1.5rem; z-index:9998; align-items:center; justify-content:space-between; border-top:3px solid #FCC036; }
.jasbot-cart-bar.visible { display:flex; }
@media(max-width:768px) {
  .jasbot-window { left:1rem; right:1rem; width:auto; max-width:none; height:calc(100vh - 7rem); max-height:480px; bottom:5.5rem; border-radius:1.2rem; }
  #jasbot-widget { bottom:1rem; right:1rem; }
  .jasbot-toggle { width:55px; height:55px; }
  .jasbot-toggle img { width:34px !important; height:34px !important; }
  .jasbot-label { display:none !important; }
}
#jasbot-widget:has(.jasbot-window.open) .jasbot-label { display:none !important; }
"""

CHATBOT_JS = """
(function() {
  const toggleBtn = document.getElementById('jasbot-toggle');
  const closeBtn  = document.getElementById('jasbot-close-btn');
  const windowEl  = document.getElementById('jasbot-window');
  const messages  = document.getElementById('jasbot-messages');
  const input     = document.getElementById('jasbot-input');
  const sendBtn   = document.getElementById('jasbot-send-btn');
  const badge     = document.getElementById('jasbot-badge');

  const WA_NUMBER  = '48663970016';
  const BLIK_PHONE = '663 970 016';
  let cart = [];
  let step = 'idle';
  let pendingOrderText = '';
  let pendingTotal = 0;

  const MENU_ITEMS = <MENU_ITEMS_PLACEHOLDER>;

  function addMsg(text, type) {
    type = type || 'bot';
    var div = document.createElement('div');
    div.className = 'jasbot-msg ' + type;
    div.innerHTML = text;
    messages.appendChild(div);
    messages.scrollTop = messages.scrollHeight;
  }

  function showMenu() {
    var html = '<strong>🍗 Nasze MENU — kliknij pozycję, aby dodać do koszyka:</strong><br><br>';
    for (var i = 0; i < MENU_ITEMS.length; i++) {
      var item = MENU_ITEMS[i];
      html += '<div style="margin:8px 0;">'
            + '<button onclick="window.jasBotAdd(' + item.id + ')" '
            + 'style="background:#FCC036;border:2px solid #2D1A1E;border-radius:10px;padding:8px 12px;'
            + 'cursor:pointer;font-family:inherit;width:100%;text-align:left;box-shadow:2px 2px 0px #2D1A1E;'
            + 'transition:all 0.1s ease;display:block;">'
            + '<div style="display:flex;justify-content:space-between;align-items:center;margin-bottom:3px;gap:8px;">'
            + '<span style="font-weight:800;font-size:0.9rem;color:#2D1A1E;flex:1;">' + item.name + '</span>'
            + '<span style="font-weight:800;font-size:0.95rem;color:#D32F2F;background:#fff;padding:1px 6px;border-radius:6px;border:1px solid #2D1A1E;white-space:nowrap;">' + item.price + ' zł</span>'
            + '</div>'
            + '<div style="font-size:0.75rem;color:#555;line-height:1.3;font-weight:500;">' + item.desc + '</div>'
            + '</button></div>';
    }
    addMsg(html);
  }

  function updateBadge() {
    var total = cart.reduce(function(s,i){ return s+i.qty; }, 0);
    badge.textContent = total;
    badge.style.display = total > 0 ? 'flex' : 'none';
  }

  window.jasBotAdd = function(id) {
    var item = null;
    for (var i = 0; i < MENU_ITEMS.length; i++) { if (MENU_ITEMS[i].id === id) { item = MENU_ITEMS[i]; break; } }
    var existing = null;
    for (var i = 0; i < cart.length; i++) { if (cart[i].id === id) { existing = cart[i]; break; } }
    if (existing) { existing.qty++; } else { cart.push({id:item.id, name:item.name, price:item.price, qty:1}); }
    updateBadge();
    var count = cart.reduce(function(s,i){ return s+i.qty; }, 0);
    addMsg('Dodano: <strong>' + item.name + '</strong>. Koszyk: <strong>' + count + '</strong> pozycji.<br>'
         + '<button onclick="window.jasBotCheckout()" '
         + 'style="margin-top:8px;background:#D32F2F;color:#fff;border:2px solid #2D1A1E;'
         + 'border-radius:6px;padding:6px 14px;cursor:pointer;font-weight:700;">'
         + 'ZŁÓŻ ZAMÓWIENIE</button>&nbsp;lub dodaj kolejne danie.');
  };

  window.jasBotCheckout = function() {
    if (cart.length === 0) { addMsg('Koszyk jest pusty! Wybierz najpierw danie.'); return; }
    var orderLines = '';
    var total = 0;
    for (var i = 0; i < cart.length; i++) {
      var ci = cart[i];
      orderLines += ci.name + ' x' + ci.qty + ' = ' + (ci.price * ci.qty) + ' zł\\n';
      total += ci.price * ci.qty;
    }
    pendingOrderText = orderLines;
    pendingTotal = total;
    cart = [];
    updateBadge();
    step = 'awaiting_blik_ref';
    addMsg('<strong>Podsumowanie zamówienia:</strong><br><br>'
         + pendingOrderText.replace(/\\n/g,'<br>')
         + '<br><strong>RAZEM: ' + pendingTotal + ' zł</strong>'
         + '<hr style="border:1px dashed #2D1A1E;margin:12px 0;">'
         + '<strong>Zapłać teraz przez BLIK na telefon:</strong><br><br>'
         + '1. Otwórz aplikację bankową<br>'
         + '2. Wybierz <strong>Przelew na telefon BLIK</strong><br>'
         + '3. Numer: <strong style="color:#D32F2F;font-size:1.1rem;">' + BLIK_PHONE + '</strong><br>'
         + '4. Kwota: <strong>' + pendingTotal + ' zł</strong><br>'
         + '5. Tytuł przelewu: np. <em>Zamówienie JaśBot</em><br><br>'
         + '<strong>Gdy wyślesz przelew — wpisz poniżej jego tytuł (lub imię i nazwisko), abyśmy mogli szybko potwierdzić wpłatę.</strong>');
  };

  window.jasBotOpenWithCart = function(pageCart) {
    cart = [];
    for (var key in pageCart) {
      if (pageCart.hasOwnProperty(key)) {
        var pc = pageCart[key];
        var itemId = 1;
        for (var i = 0; i < MENU_ITEMS.length; i++) {
          if (MENU_ITEMS[i].name === pc.name) {
            itemId = MENU_ITEMS[i].id;
            break;
          }
        }
        cart.push({ id: itemId, name: pc.name, price: pc.price, qty: pc.qty });
      }
    }
    updateBadge();
    windowEl.classList.add('open');
    var labelEl = document.getElementById('jasbot-label');
    if (labelEl) labelEl.style.display = 'none';
    window.jasBotCheckout();
  };

  function handleBlikRef(text) {
    step = 'idle';
    var blikRef = text.trim();
    var waMsg = encodeURIComponent(
      'NOWE ZAMÓWIENIE - Bar Jaś JaśBot\\n'
      + '----------------------------\\n'
      + pendingOrderText
      + '\\nRAZEM: ' + pendingTotal + ' zł\\n'
      + '----------------------------\\n'
      + 'BLIK WYŚLANY\\n'
      + 'Tytuł przelewu: ' + blikRef + '\\n'
      + '(Proszę sprawdzić w aplikacji bankowej)\\n'
      + '----------------------------\\n'
      + 'Odbiór: ul. Rokicińska 190/214, Łódź\\n'
      + 'Czas realizacji: ok. 20 min'
    );
    addMsg('Zamówienie z potwierdzeniem BLIK gotowe!<br><br>'
         + 'Kliknij przycisk poniżej, aby przesłać zamówienie <strong>i potwierdzenie płatności</strong> bezpośrednio do Marysi na WhatsApp:<br><br>'
         + '<a href="https://wa.me/' + WA_NUMBER + '?text=' + waMsg + '" target="_blank" '
         + 'style="display:inline-block;background:#25D366;color:#fff;padding:10px 20px;'
         + 'border-radius:10px;border:2px solid #2D1A1E;text-decoration:none;font-weight:700;font-size:1rem;text-align:center;">'
         + 'Wyślij zamówienie na WhatsApp</a><br><br>'
         + '<small>Czas realizacji ~20 min. Bar potwierdzi zamówienie przez WhatsApp.</small>');
    pendingOrderText = '';
    pendingTotal = 0;
  }

  function sendMsg() {
    var text = input.value.trim();
    if (!text) return;
    addMsg(text, 'user');
    input.value = '';
    if (step === 'awaiting_blik_ref') { handleBlikRef(text); return; }
    setTimeout(function() {
      var lower = text.toLowerCase();
      if (lower.indexOf('menu') >= 0 || lower.indexOf('dania') >= 0 || lower.indexOf('cena') >= 0 || lower.indexOf('cennik') >= 0) {
        showMenu();
      } else if (lower.indexOf('godzin') >= 0 || lower.indexOf('kiedy') >= 0 || lower.indexOf('otwart') >= 0) {
        addMsg('Jesteśmy otwarci:<br><strong>Pon-Sob: 09:00-19:00</strong><br>Niedziela: nieczynne');
      } else if (lower.indexOf('adres') >= 0 || lower.indexOf('gdzie') >= 0 || lower.indexOf('dojazd') >= 0 || lower.indexOf('lokalizacj') >= 0) {
        addMsg('Znajdziesz nas pod adresem:<br><strong>ul. Rokicińska 190/214, Łódź</strong><br>(tuż obok Selgros, dzielnica Widzew)');
      } else if (lower.indexOf('blik') >= 0 || lower.indexOf('płat') >= 0 || lower.indexOf('platn') >= 0) {
        addMsg('Przyjmujemy płatność przez <strong>BLIK na numer telefonu</strong>: <strong>' + BLIK_PHONE + '</strong><br>Wybierz dania z menu, a JaśBot przeprowadzi Cie przez płatność krok po kroku!');
      } else if (lower.indexOf('zamów') >= 0 || lower.indexOf('zamow') >= 0 || lower.indexOf('koszyk') >= 0 || lower.indexOf('chcę') >= 0 || lower.indexOf('chce') >= 0) {
        showMenu();
      } else {
        addMsg('Jesteś w Barze Jaś! Wpisz:<br>'
             + '<strong>menu</strong> - cennik i dania<br>'
             + '<strong>godziny</strong> - kiedy jesteśmy otwarci<br>'
             + '<strong>adres</strong> - jak do nas trafić<br>'
             + '<strong>zamów</strong> - złóż szybkie zamówienie online');
      }
    }, 350);
  }

  toggleBtn.addEventListener('click', function() {
    windowEl.classList.toggle('open');
    var labelEl = document.getElementById('jasbot-label');
    if (windowEl.classList.contains('open')) {
      if (labelEl) labelEl.style.display = 'none';
      if (messages.children.length === 0) {
        addMsg('Cześć! Jestem <strong>JaśBot</strong> - wirtualny asystent Baru Jaś! 🍗<br><br>'
             + 'Oto nasze pełne, pyszne menu. Kliknij wybrane pozycje, aby dodać je do koszyka i szybko złożyć zamówienie:<br>'
             + 'Płatność wygodnie przez <strong>BLIK na telefon</strong>.');
        showMenu();
      }
    } else {
      if (labelEl && window.innerWidth > 768) {
        labelEl.style.display = 'block';
      }
    }
  });
  closeBtn.addEventListener('click', function() {
    windowEl.classList.remove('open');
    var labelEl = document.getElementById('jasbot-label');
    if (labelEl && window.innerWidth > 768) {
      labelEl.style.display = 'block';
    }
  });
  sendBtn.addEventListener('click', sendMsg);
  input.addEventListener('keypress', function(e) { if (e.key === 'Enter') sendMsg(); });
})();
"""

with open(f"{BUILD_DIR}/assets/js/chatbot.js", "w", encoding="utf-8") as f:
    f.write(CHATBOT_JS.replace("<MENU_ITEMS_PLACEHOLDER>", chatbot_items_js))
print("✅ chatbot.js zapisany")


# -------------------------------------------------------
# META TAGS PER PAGE
# -------------------------------------------------------
META = {
    "index.html": {
        "title": "Bar Jaś Łódź | Kurczak z Rożna od 2001 | Rokicińska 190",
        "description": "Najlepszy kurczak z rożna w Łodzi od ponad 20 lat. Rodzinna receptura, świeże polskie mięso. Zamów: 663 970 016. ul. Rokicińska 190 (obok Selgros), Widzew."
    },
    "menu.html": {
        "title": "Menu — Kurczak, Kebab, Burgery | Bar Jaś Łódź",
        "description": "Sprawdź menu Baru Jaś: zestawy z kurczakiem z rożna od 34 zł, kebab, burgery, frytki, surówki. Zamów przez WhatsApp lub telefon: 663 970 016."
    },
    "onas.html": {
        "title": "O Nas — 20+ Lat Tradycji | Bar Jaś Łódź",
        "description": "Poznaj historię rodzinnego Baru Jaś. Od 2001 roku serwujemy najlepszego kurczaka z rożna w Łodzi, Widzew. Sekretna receptura, świeże polskie składniki."
    },
    "kontakt.html": {
        "title": "Kontakt — Bar Jaś | Rokicińska 190, Łódź | Tel: 663 970 016",
        "description": "Skontaktuj się z Barem Jaś: ul. Rokicińska 190, 92-412 Łódź (obok Selgros). Tel: +48 663 970 016. Pn–Sob 09:00–19:00. Niedziela: nieczynne."
    },
    "polityka.html": {
        "title": "Polityka Prywatności i RODO | Bar Jaś",
        "description": "Polityka prywatności i informacje o ochronie danych osobowych (RODO) dla strony internetowej Baru Jaś, ul. Rokicińska 190, Łódź."
    }
}

SCHEMA_LD = """<script type="application/ld+json">
{
  "@context": "https://schema.org",
  "@type": "Restaurant",
  "name": "\u201eJA\u015a\u201d BAR MARIA DYNEL",
  "legalName": "\u201eJA\u015a\u201d BAR MARIA DYNEL",
  "image": "https://kurczakujasia.pl/assets/img/logo.png",
  "url": "https://kurczakujasia.pl",
  "telephone": "+48663970016",
  "email": "kontakt@kurczakujasia.pl",
  "address": {
    "@type": "PostalAddress",
    "streetAddress": "ul. Rokici\u0144ska 190/214",
    "addressLocality": "\u0141\u00f3d\u017a",
    "addressRegion": "\u0141\u00f3d\u017a",
    "postalCode": "92-412",
    "addressCountry": "PL"
  },
  "geo": {
    "@type": "GeoCoordinates",
    "latitude": 51.7264,
    "longitude": 19.5543
  },
  "openingHoursSpecification": [
    {
      "@type": "OpeningHoursSpecification",
      "dayOfWeek": ["Monday","Tuesday","Wednesday","Thursday","Friday","Saturday"],
      "opens": "09:00",
      "closes": "19:00"
    }
  ],
  "servesCuisine": ["Polish","Fast Food","Chicken"],
  "priceRange": "$$",
  "menu": "https://kurczakujasia.pl/menu.html",
  "hasMap": "https://maps.app.goo.gl/kurczakujasia",
  "description": "Najlepszy kurczak z rożna w Łodzi od ponad 20 lat. Rodzinna receptura, świeże polskie mięso, ul. Rokicińska 190 obok Selgros."
}
</script>
<script type="application/ld+json">
{
  "@context": "https://schema.org",
  "@type": "FAQPage",
  "mainEntity": [
    {"@type":"Question","name":"Do której godziny jest otwarty Bar Jaś?","acceptedAnswer":{"@type":"Answer","text":"Bar Jaś jest otwarty od poniedziałku do soboty w godzinach 9:00–19:00. W niedziele jesteśmy nieczynni."}},
    {"@type":"Question","name":"Ile kosztuje zestaw z kurczakiem z rożna?","acceptedAnswer":{"@type":"Answer","text":"Zestaw z połówką kurczaka z rożna (z frytkami i surówkami) kosztuje 34 zł. Cały kurczak to 38 zł."}},
    {"@type":"Question","name":"Gdzie znajduje się Bar Jaś w Łodzi?","acceptedAnswer":{"@type":"Answer","text":"Bar Jaś mieści się przy ul. Rokicińskiej 190, 92-412 Łódź, w dzielnicy Widzew, tuż obok Selgros."}},
    {"@type":"Question","name":"Czy Bar Jaś przyjmuje zamówienia online?","acceptedAnswer":{"@type":"Answer","text":"Tak! Zamówienia możesz złożyć przez naszego chatbota JaśBota na stronie, przez WhatsApp lub telefonicznie pod numerem +48 663 970 016."}},
    {"@type":"Question","name":"Czy Bar Jaś ma opcję dostawy do domu?","acceptedAnswer":{"@type":"Answer","text":"Obecnie oferujemy odbiór osobisty przy ul. Rokicińskiej 190. Zamówienie zgłoś przez JaśBota, WhatsApp lub telefon — będzie gotowe na Twoje przybycie!"}}
  ]
}
</script>"""

FAQ_HTML = """
<section class="jas-faq-section" id="faq">
  <h2>Najczęściej Zadawane Pytania</h2>
  <details class="jas-faq-item">
    <summary>Do której godziny jest otwarty Bar Jaś? <span>+</span></summary>
    <p>Jesteśmy otwarci od <strong>poniedziałku do soboty</strong> w godzinach <strong>9:00–19:00</strong>. W niedziele jesteśmy nieczynni.</p>
  </details>
  <details class="jas-faq-item">
    <summary>Ile kosztuje zestaw z kurczakiem z rożna? <span>+</span></summary>
    <p>Zestaw z <strong>połówką kurczaka</strong> z rożna (z frytkami i surówką) kosztuje <strong>34 zł</strong>. Cały kurczak to <strong>38 zł</strong>. Kebab w zestawie od 29 zł.</p>
  </details>
  <details class="jas-faq-item">
    <summary>Gdzie znajduje się Bar Jaś? <span>+</span></summary>
    <p>Znajdziesz nas przy <strong>ul. Rokicińskiej 190, 92-412 Łódź</strong>, w dzielnicy Widzew, tuż obok Selgros. Łatwy dojazd i parking.</p>
  </details>
  <details class="jas-faq-item">
    <summary>Czy można zamówić online lub przez WhatsApp? <span>+</span></summary>
    <p>Tak! Skorzystaj z naszego <strong>JaśBota</strong> w prawym dolnym rogu — wybierz dania i wyślij zamówienie przez WhatsApp bezpośrednio do nas. Możesz też zadzwonić: <strong>663 970 016</strong>.</p>
  </details>
  <details class="jas-faq-item">
    <summary>Czy Bar Jaś ma opcję dostawy do domu? <span>+</span></summary>
    <p>Obecnie oferujemy <strong>odbiór osobisty</strong> przy ul. Rokicińskiej 190. Zamówienie zgłoś przez JaśBota, WhatsApp lub telefon — będzie gotowe na Twoje przybycie!</p>
  </details>
</section>
"""

REVIEWS_HTML = """
<section class="jas-reviews-section" id="opinie">
  <h2>Co Mówią Nasi Goście?</h2>
  <div class="jas-reviews-grid">
    <div class="jas-review-card">
      <div class="stars">★★★★★</div>
      <p>"Najlepszy kurczak z rożna w całej Łodzi! Chrupka skórka, soczyste mięso i rewelacyjne surówki. Wracamy tu od lat i nigdy się nie zawiedliśmy."</p>
      <div class="reviewer">— Marek K., Google Reviews</div>
    </div>
    <div class="jas-review-card">
      <div class="stars">★★★★★</div>
      <p>"Obsługa błyskawiczna, ceny uczciwe, a jakość jedzenia na najwyższym poziomie. Kurczak świeży i gorący. Polecam wszystkim z okolicy Widzewa!"</p>
      <div class="reviewer">— Ania P., Google Reviews</div>
    </div>
    <div class="jas-review-card">
      <div class="stars">★★★★★</div>
      <p>"Bar Jaś to prawdziwa perełka! Sekretna receptura kurczaka jest coś! Niedaleko Selgros, zawsze zatrzymuję się tu po zakupach. Rodzinny klimat, super ceny."</p>
      <div class="reviewer">— Tomasz W., Google Reviews</div>
    </div>
  </div>
  <div style="text-align:center;margin-top:1.5rem;">
    <a href="https://g.page/r/barjas/review" target="_blank" rel="noopener noreferrer" class="jas-btn jas-btn-outline">
      <svg viewBox="0 0 24 24" width="18" height="18" fill="currentColor" style="margin-right:6px;"><path d="M12 2C8.13 2 5 5.13 5 9c0 5.25 7 13 7 13s7-7.75 7-13c0-3.87-3.13-7-7-7zm0 9.5c-1.38 0-2.5-1.12-2.5-2.5s1.12-2.5 2.5-2.5 2.5 1.12 2.5 2.5-1.12 2.5-2.5 2.5z"/></svg>
      Wystaw Opinię na Google
    </a>
  </div>
</section>
"""

MAIN_JS = """
document.addEventListener('DOMContentLoaded', () => {
  // Active nav link
  const page = window.location.pathname.split('/').pop() || 'index.html';
  document.querySelectorAll('.nav-link').forEach(a => {
    if (a.getAttribute('href') === page) a.classList.add('active');
  });

  // Mobile menu
  const toggle = document.getElementById('mobile-toggle');
  const nav    = document.getElementById('main-nav');
  if (toggle && nav) {
    toggle.addEventListener('click', () => nav.classList.toggle('open'));
    document.addEventListener('click', e => {
      if (!nav.contains(e.target) && !toggle.contains(e.target)) nav.classList.remove('open');
    });
  }
});
"""
with open(f"{BUILD_DIR}/assets/js/main.js", "w", encoding="utf-8") as f:
    f.write(MAIN_JS)
print("✅ main.js zapisany")

# -------------------------------------------------------
# FOOTER HTML
# -------------------------------------------------------
FOOTER_HTML = """
<footer class="site-footer">
  <div class="footer-inner">
    <div>
      <div class="footer-title">
        <img src="assets/img/logo.png" alt="Bar Jaś Logo">
        Bar Jaś
      </div>
      <p>Najlepszy kurczak z rożna w Łodzi od ponad 20 lat. Rodzinna receptura, świeże polskie składniki.</p>
    </div>
    <div>
      <h3 style="color:var(--primary);margin-bottom:12px;">Kontakt</h3>
      <p>
        <strong>Adres:</strong><br>
        ul. Rokicińska 190/214, 92-412 Łódź<br>
        (obok Selgros, dzielnica Widzew)
      </p>
      <p><strong>Telefon:</strong> <a href="tel:+48663970016">+48 663 970 016</a></p>
      <p><strong>E-mail:</strong> <a href="mailto:kontakt@kurczakujasia.pl">kontakt@kurczakujasia.pl</a></p>
      <p><strong>NIP:</strong> 7261001953</p>
    </div>
    <div>
      <h3 style="color:var(--primary);margin-bottom:12px;">Godziny Otwarcia</h3>
      <p><strong>Pon – Sob:</strong> 09:00 – 19:00</p>
      <p><strong>Niedziela:</strong> Nieczynne</p>
      <h3 style="color:var(--primary);margin-top:16px;margin-bottom:12px;">Nawigacja</h3>
      <p><a href="index.html">Strona Główna</a> · <a href="menu.html">Menu</a> · <a href="onas.html">O Nas</a> · <a href="kontakt.html">Kontakt</a></p>
      <p style="margin-top:8px;"><a href="polityka.html">Polityka Prywatności i RODO</a></p>
    </div>
  </div>
  <div class="footer-bottom">
    &copy; 2026 &bdquo;JAŚ&rdquo; BAR MARIA DYNEL · NIP: 7261001953 · ul. Rokicińska 190/214, 92-412 Łódź
  </div>
</footer>
"""

# -------------------------------------------------------
# HEADER HTML
# -------------------------------------------------------
def make_header(page_name, title, description, extra_head=""):
    return f"""<!DOCTYPE html>
<html lang="pl">
<head>
  <meta charset="UTF-8">
  <meta name="viewport" content="width=device-width, initial-scale=1.0">
  <title>{title}</title>
  <meta name="description" content="{description}">
  <meta name="robots" content="index, follow">
  <meta property="og:title" content="{title}">
  <meta property="og:description" content="{description}">
  <meta property="og:image" content="https://kurczakujasia.pl/assets/img/logo.png">
  <meta property="og:url" content="https://kurczakujasia.pl/{page_name}">
  <meta property="og:type" content="website">
  <meta property="og:locale" content="pl_PL">
  <link rel="canonical" href="https://kurczakujasia.pl/{page_name}">
  <link rel="stylesheet" href="assets/css/style.css">
  <style>{CHATBOT_CSS}</style>
  {extra_head}
</head>
<body>
<header class="site-header">
  <a href="index.html" class="site-logo-link" aria-label="Bar Jaś - Strona Główna">
    <img src="assets/img/logo.png" alt="Bar Jaś - Logo" width="62" height="62">
  </a>
  <nav class="main-navigation" id="main-nav" aria-label="Nawigacja główna">
    <ul>
      <li><a href="index.html" class="nav-link">Home</a></li>
      <li><a href="menu.html" class="nav-link">Menu</a></li>
      <li><a href="onas.html" class="nav-link">O Nas</a></li>
      <li><a href="kontakt.html" class="nav-link">Kontakt</a></li>
      <li>
        <a href="tel:+48663970016" class="jas-btn jas-btn-secondary" style="padding:8px 16px;font-size:0.95rem;border-radius:0.8rem;" aria-label="Zadzwoń i zamów">
          <svg viewBox="0 0 24 24" width="16" height="16" fill="currentColor" aria-hidden="true"><path d="M6.62 10.79c1.44 2.83 3.76 5.14 6.59 6.59l2.2-2.2c.27-.27.67-.36 1.02-.24 1.12.37 2.33.57 3.57.57.55 0 1 .45 1 1V20c0 .55-.45 1-1 1-9.39 0-17-7.61-17-17 0-.55.45-1 1-1h3.5c.55 0 1 .45 1 1 0 1.25.2 2.45.57 3.57.11.35.03.74-.25 1.02l-2.2 2.2z"/></svg>
          ZAMÓW TERAZ
        </a>
      </li>
    </ul>
  </nav>
  <button class="mobile-menu-toggle" id="mobile-toggle" aria-label="Otwórz menu mobilne" aria-expanded="false">
    <svg viewBox="0 0 24 24" width="24" height="24" fill="var(--dark)" aria-hidden="true"><path d="M3 18h18v-2H3v2zm0-5h18v-2H3v2zm0-7v2h18V6H3z"/></svg>
  </button>
</header>
"""

SCRIPTS_CLOSE = """
<script src="assets/js/main.js"></script>
<script src="assets/js/chatbot.js"></script>
</body>
</html>"""

# -------------------------------------------------------
# PAGES — read from source, fix all bugs, write clean UTF-8
# -------------------------------------------------------
def clean_encoding(text):
    """Repair double-encoding and corrupt characters (CP1250 artifacts from WP-origin templates)"""
    rep_map = {
        "JA\x9a": "JAŚ",
        "roşna": "rożna",
        "minut\x99": "minutę",
        "ZAM\x93WIENIA": "ZAMÓWIENIA",
        "ponişej": "poniżej",
        "Wy\x9blij": "Wyślij",
        "przej\x9b\x87": "przejść",
        "godzin\x99": "godzinę",
        "zap\x82a\x87": "zapłać",
        "si\x99": "się",
        "DA\x83": "DAŃ",
        "obs\x82ugi": "obsługi",
        "obs\x82ug\x99": "obsługę",
        "mog\x85": "mogą",
        "zawiera\x87": "zawierać",
        "zboşa": "zboża",
        "zawieraj\x85ce": "zawierające",
        "laktoz\x99": "laktozę",
        "gorczyc\x99": "gorczycę",
        "Szczegó\x82owy": "Szczegółowy",
        "kaşdego": "każdego",
        "dost\x99pny": "dostępny",
        "warto\x9bciami": "wartościami",
        "obróbk\x85": "obróbką",
        "termiczn\x85": "termiczną",
        "róşni\x87": "różnić",
        "zaleşno\x9bci": "zależności",
        "z\x82": "zł",
        "Po\x82ówka": "Połówka",
        "\x9bwieşym": "świeżym",
        "Syc\x85ca": "Sycąca",
        "mi\x99sa": "mięsa",
        "Ca\x82y": "Cały",
        "r\x99cznie": "ręcznie",
        "zió\x82": "ziół",
        "mi\x99kkie": "miękkie",
        "\x9brodku": "środku",
        "Bu\x82ce": "Bułce",
        "wype\x82niona": "wypełniona",
        "rzemie\x9blnicza": "rzemieślnicza",
        "\x82agodnym": "łagodnym",
        "sa\x82at\x85": "sałatą",
        "G\x81ODNYCH": "GŁODNYCH",
        "k\x85sków": "kąsków",
        "rado\x9b\x87": "radość",
        "najm\x82odszych": "najmłodszych",
        "poşywna": "pożywna",
        "gor\x85ca": "gorąca",
        "nasz\x85": "naszą",
        "dzisiejsz\x85": "dzisiejszą",
        "pozycj\x99": "pozycję",
        "\x9aWIEŝA": "ŚWIEŻA",
        "uzupe\x82nienie": "uzupełnienie",
        "bia\x82ej": "białej",
        "orzeźwiaj\x85ca": "orzeźwiająca",
        "posi\x82ku": "posiłku",
        "klikni\x99cia": "kliknięcia",
        "bezpo\x9brednio": "bezpośrednio",
        "Prosz\x99": "Proszę",
        "chwil\x99": "chwilę",
        "ş": "ż",
        "\x9a\xa0\x8f": "⚠️",
        "\x9f\x94": "🔥",
        "\x9e\x95": "➕",
        "\x9f\x8d\x97": "🍗",
        "\x9f\x9b\x92": "🛒",
        "Smerf \x80\x93": "Smerf –",
        "\x80\x93": "–",
    }
    for k, v in rep_map.items():
        text = text.replace(k, v)
    return text

def fix_links(text):
    """Fix broken WordPress-style links"""
    text = text.replace('href="/menu/"',    'href="menu.html"')
    text = text.replace('href="/onas/"',    'href="onas.html"')
    text = text.replace('href="/kontakt/"', 'href="kontakt.html"')
    text = text.replace('href="/menu"',     'href="menu.html"')
    text = text.replace('"hasMenu": "https://kurczakujasia.pl/menu/"', '"hasMenu": "https://kurczakujasia.pl/menu.html"')
    text = text.replace('[trustindex no-registration=google]', '')
    return text

def strip_shell(text):
    """Remove existing <head>, <header>, <footer>, chatbot from the page content"""
    # Remove everything in <head>
    text = re.sub(r'<!DOCTYPE.*?<body[^>]*>', '', text, flags=re.DOTALL|re.IGNORECASE)
    # Remove the header block
    text = re.sub(r'<header\b[^>]*>.*?</header>', '', text, flags=re.DOTALL|re.IGNORECASE)
    # Remove footers
    text = re.sub(r'<footer\b[^>]*>.*?</footer>', '', text, flags=re.DOTALL|re.IGNORECASE)
    # Remove jasbot-widget
    text = re.sub(r'<div[^>]+id=["\']jasbot-widget["\'].*?</div>\s*</div>', '', text, flags=re.DOTALL|re.IGNORECASE)
    # Remove jasbot-label
    text = re.sub(r'<div[^>]+class=["\']jasbot-label["\'][^>]*>.*?</div>', '', text, flags=re.DOTALL|re.IGNORECASE)
    # Remove closing body/html
    text = re.sub(r'</body>.*?</html>', '', text, flags=re.DOTALL|re.IGNORECASE)
    # Remove existing scripts
    text = re.sub(r'<script\b[^>]*src=["\']assets/js/[^"\']+["\'][^>]*/?>(\s*</script>)?', '', text, flags=re.DOTALL|re.IGNORECASE)
    return text.strip()

PAGES = {
    "index.html":   "scratch/previews/home_preview.html",
    "menu.html":    "scratch/previews/menu_new_preview.html",
    "onas.html":    "scratch/previews/onas_preview.html",
    "kontakt.html": "scratch/previews/kontakt_preview.html",
}

for out_name, src_path in PAGES.items():
    m = META[out_name]
    extra = SCHEMA_LD if out_name == "index.html" else ""
    header = make_header(out_name, m["title"], m["description"], extra)

    if os.path.exists(src_path):
        with open(src_path, "r", encoding="utf-8", errors="replace") as f:
            body = f.read()
        body = strip_shell(body)
    else:
        body = "<main><p>Treść w przygotowaniu.</p></main>"

    # Ensure we use Fredoka (supports Polish diacritics natively) instead of Lilita One or Titan One
    body = body.replace("Lilita One", "Fredoka").replace("Lilita+One", "Fredoka")
    body = body.replace("Titan One", "Fredoka").replace("Titan+One", "Fredoka")

    # Fix WP artifacts
    body = body.replace("<!-- wp:html -->", "").replace("<!-- /wp:html -->", "")
    body = fix_links(body)

    # Page-specific fixes
    if out_name == "index.html":
        # Fix phone number
        body = body.replace("+48 +48 +48 663 970 016", "+48 663 970 016")
        # Inject reviews & FAQ before closing of main container
        body += REVIEWS_HTML + FAQ_HTML

    if out_name == "menu.html":
        # Replace hardcoded JAS_MENU_ITEMS with dynamically serialized python master menu
        pattern = r'const\s+JAS_MENU_ITEMS\s*=\s*\[.*?\]\s*;'
        body = re.sub(pattern, lambda m: f'const JAS_MENU_ITEMS = {menu_items_js};', body, flags=re.DOTALL)

    if out_name == "kontakt.html":
        body = body.replace("ZAMÓWIENIA I ODBIÓR", "KONTAKT TELEFONICZNY")
        # Add Google Maps embed
        maps = """
<div style="margin-top:2rem;border-radius:1rem;overflow:hidden;border:3px solid var(--dark);box-shadow:var(--shadow);">
  <iframe
    src="https://www.google.com/maps/embed?pb=!1m18!1m12!1m3!1d2468.9!2d19.5543!3d51.7264!2m3!1f0!2f0!3f0!3m2!1i1024!2i768!4f13.1!3m3!1m2!1s0x471a344b7e0e4b57%3A0xbar_jas_lodz!2sBokicińska%20190%2C%20Łódź!5e0!3m2!1spl!2spl!4v1699000000000!5m2!1spl!2spl"
    width="100%" height="380" style="border:0;" allowfullscreen="" loading="lazy"
    referrerpolicy="no-referrer-when-downgrade" title="Mapa dojazdu do Bar Jaś Łódź">
  </iframe>
</div>
<div style="text-align:center;margin-top:1rem;">
  <a href="https://maps.app.goo.gl/barjas" target="_blank" rel="noopener noreferrer" class="jas-btn jas-btn-primary">
    <svg viewBox="0 0 24 24" width="18" height="18" fill="currentColor"><path d="M12 2C8.13 2 5 5.13 5 9c0 5.25 7 13 7 13s7-7.75 7-13c0-3.87-3.13-7-7-7zm0 9.5c-1.38 0-2.5-1.12-2.5-2.5s1.12-2.5 2.5-2.5 2.5 1.12 2.5 2.5-1.12 2.5-2.5 2.5z"/></svg>
    Otwórz w Google Maps
  </a>
</div>
"""
        body += maps

    final = header + "\n" + body + "\n" + CHATBOT_HTML + "\n" + FOOTER_HTML + "\n" + SCRIPTS_CLOSE
    final = clean_encoding(final)
    out_path = f"{BUILD_DIR}/{out_name}"
    with open(out_path, "w", encoding="utf-8") as f:
        f.write(final)
    print(f"✅ {out_name} zbudowany")

# -------------------------------------------------------
# POLITYKA PRYWATNOŚCI (RODO)
# -------------------------------------------------------
POLITYKA = make_header("polityka.html", META["polityka.html"]["title"], META["polityka.html"]["description"]) + """
<main style="max-width:900px;margin:3rem auto;padding:2rem;background:#fff;border-radius:2rem;border:3px solid var(--dark);box-shadow:var(--shadow);">
  <h1 style="margin-bottom:2rem;">Polityka Prywatności i RODO</h1>

  <h2>1. Administrator Danych Osobowych</h2>
  <p>Administratorem Twoich danych osobowych jest:<br>
  <strong>&bdquo;JAŚ&rdquo; BAR MARIA DYNEL</strong><br>
  ul. Rokicińska 190/214, 92-412 Łódź<br>
  NIP: <strong>7261001953</strong><br>
  Tel: <a href="tel:+48663970016">+48 663 970 016</a><br>
  E-mail: <a href="mailto:kontakt@kurczakujasia.pl">kontakt@kurczakujasia.pl</a></p>

  <h2>2. Cel i Podstawa Przetwarzania Danych</h2>
  <p>Twoje dane osobowe przetwarzamy w celu:</p>
  <ul>
    <li>Obsługi zapytań i zamówień składanych telefonicznie, przez WhatsApp lub formularz kontaktowy — podstawa prawna: art. 6 ust. 1 lit. b RODO (niezbędność do wykonania umowy)</li>
    <li>Kontaktu zwrotnego w odpowiedzi na przesłane zapytanie — podstawa prawna: art. 6 ust. 1 lit. f RODO (prawnie uzasadniony interes)</li>
  </ul>

  <h2>3. Jakie Dane Zbieramy?</h2>
  <p>Przy składaniu zamówienia lub kontakcie możemy zebrać: imię, numer telefonu, wiadomość (treść zamówienia). Strona internetowa nie korzysta z Google Analytics ani plików cookie śledzących.</p>

  <h2>4. Okres Przechowywania Danych</h2>
  <p>Dane związane z obsługą zamówień przechowujemy przez okres niezbędny do realizacji zamówienia, a następnie przez okres wynikający z przepisów podatkowych (5 lat).</p>

  <h2>5. Twoje Prawa</h2>
  <p>Przysługuje Ci prawo do:</p>
  <ul>
    <li>Dostępu do swoich danych</li>
    <li>Sprostowania nieprawidłowych danych</li>
    <li>Usunięcia danych (prawo do bycia zapomnianym)</li>
    <li>Ograniczenia przetwarzania</li>
    <li>Przenoszenia danych</li>
    <li>Wniesienia skargi do Prezesa Urzędu Ochrony Danych Osobowych (UODO), ul. Stawki 2, 00-193 Warszawa</li>
  </ul>

  <h2>6. Kontakt w Sprawie Danych</h2>
  <p>W sprawach związanych z ochroną danych osobowych skontaktuj się z nami mailowo: <a href="mailto:kontakt@kurczakujasia.pl">kontakt@kurczakujasia.pl</a> lub telefonicznie: <a href="tel:+48663970016">+48 663 970 016</a>.</p>

  <h2>7. Cookies i Śledzenie</h2>
  <p>Niniejsza strona internetowa nie używa plików cookies do celów reklamowych ani śledzenia. Chatbot JaśBot przechowuje stan koszyka wyłącznie w pamięci przeglądarki (nie na serwerze) i jest kasowany po zamknięciu zakładki.</p>

  <p style="margin-top:2rem;font-size:0.85rem;color:#888;">Ostatnia aktualizacja: 6 lipca 2026</p>
  <a href="index.html" class="jas-btn jas-btn-primary" style="margin-top:1rem;display:inline-flex;">← Wróć do strony głównej</a>
</main>
""" + CHATBOT_HTML + FOOTER_HTML + SCRIPTS_CLOSE

with open(f"{BUILD_DIR}/polityka.html", "w", encoding="utf-8") as f:
    f.write(clean_encoding(POLITYKA))
print("✅ polityka.html (RODO) zapisana")

# -------------------------------------------------------
# ROBOTS.TXT
# -------------------------------------------------------
ROBOTS = """User-agent: *
Allow: /
Disallow: /assets/

User-agent: GPTBot
Allow: /

User-agent: ChatGPT-User
Allow: /

User-agent: PerplexityBot
Allow: /

User-agent: ClaudeBot
Allow: /

User-agent: Google-Extended
Allow: /

Sitemap: https://kurczakujasia.pl/sitemap.xml
"""
with open(f"{BUILD_DIR}/robots.txt", "w", encoding="utf-8") as f:
    f.write(ROBOTS)
print("✅ robots.txt")

# -------------------------------------------------------
# SITEMAP.XML
# -------------------------------------------------------
SITEMAP = """<?xml version="1.0" encoding="UTF-8"?>
<urlset xmlns="http://www.sitemaps.org/schemas/sitemap/0.9">
  <url><loc>https://kurczakujasia.pl/</loc><priority>1.0</priority><changefreq>weekly</changefreq></url>
  <url><loc>https://kurczakujasia.pl/menu.html</loc><priority>0.9</priority><changefreq>weekly</changefreq></url>
  <url><loc>https://kurczakujasia.pl/kontakt.html</loc><priority>0.8</priority><changefreq>monthly</changefreq></url>
  <url><loc>https://kurczakujasia.pl/onas.html</loc><priority>0.7</priority><changefreq>monthly</changefreq></url>
  <url><loc>https://kurczakujasia.pl/polityka.html</loc><priority>0.3</priority><changefreq>yearly</changefreq></url>
</urlset>
"""
with open(f"{BUILD_DIR}/sitemap.xml", "w", encoding="utf-8") as f:
    f.write(SITEMAP)
print("✅ sitemap.xml")

# -------------------------------------------------------
# .HTACCESS (HTTPS redirect)
# -------------------------------------------------------
HTACCESS = """Options -Indexes
RewriteEngine On

# Force HTTPS
RewriteCond %{HTTPS} off
RewriteRule ^(.*)$ https://%{HTTP_HOST}%{REQUEST_URI} [L,R=301]

# www -> non-www
RewriteCond %{HTTP_HOST} ^www\\.(.*)$ [NC]
RewriteRule ^(.*)$ https://%1/$1 [R=301,L]

# Directory index
DirectoryIndex index.html

# Charset
AddDefaultCharset UTF-8
AddCharset UTF-8 .html .css .js .xml

# Security headers
Header always set X-Content-Type-Options nosniff
Header always set X-Frame-Options SAMEORIGIN
Header always set Referrer-Policy strict-origin-when-cross-origin
"""
with open(f"{BUILD_DIR}/.htaccess", "w", encoding="utf-8") as f:
    f.write(HTACCESS)
print("✅ .htaccess (HTTPS + charset)")

print("\n🚀 BUILD ZAKOŃCZONY. Uruchamiam FTP deploy...")

# -------------------------------------------------------
# FTP DEPLOY
# -------------------------------------------------------
def ftp_upload_dir(ftp, local_dir, remote_dir):
    try:
        ftp.cwd(remote_dir)
    except ftplib.error_perm:
        ftp.mkd(remote_dir)
        ftp.cwd(remote_dir)

    for item in sorted(os.listdir(local_dir)):
        local_path = os.path.join(local_dir, item)
        if os.path.isfile(local_path):
            with open(local_path, "rb") as f:
                ftp.storbinary(f"STOR {item}", f)
            print(f"  ⬆ {remote_dir}/{item}")
        elif os.path.isdir(local_path):
            ftp_upload_dir(ftp, local_path, item)
            ftp.cwd("..")

print(f"Łączę się z {FTP_HOST}...")
ftp = ftplib.FTP(FTP_HOST)
ftp.login(FTP_USER, FTP_PASS)
ftp.set_pasv(True)

# Rename WP index if still exists
ftp.cwd(FTP_ROOT)
try:
    files = ftp.nlst()
    if "index.php" in files:
        ftp.rename("index.php", "wp-index-backup.php")
        print("  ✅ index.php -> wp-index-backup.php")
    if ".htaccess" in files and ".htaccess-backup" not in files:
        ftp.rename(".htaccess", ".htaccess-old")
        print("  ✅ Stary .htaccess -> .htaccess-old")
except Exception as e:
    print(f"  ⚠ (WP backup skip): {e}")

ftp.cwd("/")
ftp_upload_dir(ftp, BUILD_DIR, FTP_ROOT)
ftp.quit()

print("\n✅✅✅ DEPLOY ZAKOŃCZONY! Strona jest na żywo: https://kurczakujasia.pl")
print("Sprawdź: https://kurczakujasia.pl/polityka.html | /menu.html | /sitemap.xml | /robots.txt")
