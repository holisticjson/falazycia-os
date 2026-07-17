# 🛠️ Specyfikacja Agenta Streamlit: Social Media & Visual Factory Dashboard

Ta specyfikacja definiuje strukturę, zmienne wejściowe, logikę biznesową oraz silniki generowania grafik dla asystenta/programisty tworzącego lub modyfikującego dashboard Streamlit. 

Cel aplikacji to automatyczna generacja spójnych opisów profilowych (Bio) oraz wysokiej jakości materiałów graficznych (Awatary i Banery w odpowiednich proporcjach) dla 6 kluczowych platform społecznościowych.

---

## 🏗️ 1. Architektura Wejść (Zmienne Globalne)
W lewym panelu bocznym (Sidebar) lub w sekcji konfiguracji marki użytkownik podaje następujące parametry:

| Nazwa Zmiennej | Typ Pola | Opis / Przykład |
| :--- | :--- | :--- |
| `brand_name` | Tekstowe (krótkie) | Nazwa marki / Imię i Nazwisko (np. `J(AI)SON`) |
| `website_url` | Tekstowe (krótkie) | URL strony głównej (np. `https://jaison.pl`) |
| `app_url` | Tekstowe (krótkie) | URL aplikacji SaaS (np. `https://app.jaison.pl`) |
| `niche` | Tekstowe (krótkie) | Branża / Specjalizacja (np. `Projektowanie systemów agentowych AI i automatyzacja B2B`) |
| `target_audience`| Tekstowe (długie) | Grupa docelowa (np. `neuroatypowi founderzy, mali i średni przedsiębiorcy B2B`) |
| `tone_of_voice` | Wybór (Selectbox) | Styl komunikacji (np. `Ghost v2: bezpośredni, ADHD-friendly, zero lania wody`) |
| `motto` | Tekstowe (długie) | Unikalne motto (np. `Automatyzuj powtarzalne. Twórz unikalne. Zyskaj.`) |
| `cta` | Tekstowe (krótkie) | Wezwanie do działania (np. `Zacznij automatyzować, żyj lepiej.`) |

---

## 📑 2. Zakładka 1: Brand Strategy & Profile BIOS (Generowanie Opisów)

Po kliknięciu przycisku **"Generuj Profile i BIOS"**, system powinien uruchomić prompt do LLM (np. Gemini 1.5 Pro) i wygenerować spójne opisy dostosowane do sztywnych limitów znakowych poszczególnych platform:

### 1. LinkedIn Profile:
*   **Nagłówek (Headline):** Max 220 znaków. Format: `Rola | Obietnica wartości + Kluczowe słowa kluczowe | Nazwa Marki`.
*   **O mnie (About):** Max 2600 znaków. Układ: Haczyk (problem), rozwiązanie (metoda), filary oferty, dlaczego my, call to action.
*   **Opis usług (Services Description):** **Rygorystyczny limit 500 znaków!** Skondensowana pigułka oferty.

### 2. Instagram Bio:
*   **Tekst Bio:** **Max 150 znaków ze spacjami!** Musi zawierać emotikony, wezwanie do działania i skrócony link.

### 3. Facebook Page About:
*   **Krótki opis (Short Bio):** Max 255 znaków.
*   **Długi opis (Long Description):** Bez limitu – pełna historia marki i misja.

### 5. TikTok Bio:
*   **Tekst Bio:** **Max 80 znaków ze spacjami!** Maksymalnie skondensowane, jednozdaniowe uderzenie z CTA.

### 5. Twitter / X Bio:
*   **Tekst Bio:** Max 160 znaków. Pozycjonowanie eksperckie, dynamiczne, tech-friendly.

### 6. Threads Bio:
*   **Tekst Bio:** Max 150 znaków. Bardziej luźny, osobisty charakter.

---

## 🎨 3. Zakładka 2: Avatar Generator (Spójne Zdjęcia Profilowe)

Moduł Streamlit pozwalający wygenerować spójne zdjęcie profilowe użytkownika przy użyciu wybranego stylu wizualnego.

### ⚙️ Konfiguracja interfejsu (UI):
1.  **Wybór silnika (Engine):** `Google Imagen 3.0` vs `Flux.1 (z LoRA)`.
2.  **Opis postaci (Character Description):** Tekst podpowiadający (np. `confident bald man in late 30s, rectangular glasses, thin matte black frames, warm genuine smile`).
3.  **Wybór Stylu Wizualnego (Style Selector):** (Dodano 5 rozbudowanych, strategicznych stylów marki J(AI)SON).

---

### 🔮 System Prompts & Prompt Blueprints dla stylów Awatara (Kwadrat 1:1)

Poniższe szablony promptów są automatycznie uzupełniane w tle przez aplikację Streamlit i wysyłane do silnika generowania grafik. Zmienna `{{CHARACTER}}` wstrzykuje opis postaci (np. `bald athletic man in late 30s, with glasses, warm smile...`).

#### 🌌 Styl A: Cybernetic Hub (AI systems & Neural Networks)
*   **Kontekst marki:** Pozycjonowanie jako architekt zaawansowanych systemów AI, n8n i systemów agentowych.
*   **Zbudowany prompt systemowy:**
    > `"A high-end, clean close-up portrait of {{CHARACTER}} facing the camera. The background is a sophisticated and futuristic dark tech command center: glowing translucent glass screens displaying holographic cyan and electric purple data charts, mathematical equations, and delicate network connection lines. Studio key lighting creates sharp masculine features, strong jawline, and natural skin textures. No distortions, highly professional, 8k resolution, cinematic atmosphere, f/1.8."`

#### 🌿 Styl B: Cozy Server Sanctuary (Biohacking, Nature & Tech)
*   **Kontekst marki:** Pozycjonowanie na balans energetyczny, biohacking, ekologię oraz stabilną architekturę (Low-Cost / High-ROI).
*   **Zbudowany prompt systemowy:**
    > `"A professional cinematic portrait of {{CHARACTER}} with a natural and calm expression. The setting is a cozy, warm minimalist server room where technology meets nature: modern matte-charcoal server racks are softly illuminated by warm amber LED lights and gentle green power indicators. Delicate leafy organic plants like monsters and small bonsai trees grow harmoniously around the technical equipment. Soft morning sunlight streams from a side window, highlighting natural skin fullness, realistic textures, and sharp details. High-end, premium, photorealistic, 8k."`

#### 🌃 Styl C: Deep Focus Night Studio (Hyperfocus & High-Performance)
*   **Kontekst marki:** Praca asynchroniczna, wysoka wydajność, maksymalne skupienie, ucieczka od rozpraszaczy (ADHD).
*   **Zbudowany prompt systemowy:**
    > `"A high-contrast, moody close-up portrait of {{CHARACTER}} looking confident and focused. He is in a premium, quiet soundproof coding room at night. The background features dark acoustic hexagonal panels with glowing neon cyan linear lights running between them. To the side, there is a softly glowing vertical monitor showing clean coding structures. Warm, dramatic key lighting creates clear masculine facial lines, natural facial fullness, and reflections in his corrective glasses. Cinematic depth of field, photorealistic, premium feel, 8k."`

#### 🌅 Styl D: Biotech Garden / Freedom (Operational Freedom & Silence)
*   **Kontekst marki:** Święty spokój, asynchroniczność, automatyzacja "żyj lepiej", redukcja stresu.
*   **Zbudowany prompt systemowy:**
    > `"An ultra-minimalist, airy cinematic portrait of {{CHARACTER}} looking completely relaxed and happy, with a genuine smile. He is standing near a giant floor-to-ceiling clean panoramic glass window of a modern architectural estate. Outside, a pristine biotech garden with clean green plants is bathed in warm, golden sunset light. The atmosphere is quiet, bright, and completely silent. Key soft lighting showcases healthy skin tones, clear masculine structures, and authentic facial fullness. High-end editorial style, premium design, depth of field, 8k."`

#### 🕴️ Styl E: Executive Cyber-Casual (Founder Authority & B2B Trust)
*   **Kontekst marki:** Klasyczne zaufanie korporacyjne B2B, luksusowy minimalizm, "High-Ticket" consulting.
*   **Zbudowany prompt systemowy:**
    > `"An elegant and luxurious portrait of {{CHARACTER}} dressed in a tailor-made deep navy blue blazer over a premium charcoal grey turtleneck. On the collar of the turtleneck, a very small and clean matte grey embroidered text 'J(AI)SON' is subtly visible. He is standing inside a highly professional, dark-themed executive lounge. The background is a clean matte-black luxury wall with subtle recessed accent lighting. The lighting is soft, dramatic, and prestigious, highlighting natural masculine jawline, authentic facial fullness, and premium fabrics. Perfect corporate identity, photorealistic, 8k."`

---

## 🖼️ 4. Zakładka 3: Tailored Banners Generator (Zdjęcia w tle)

Moduł generujący spójne, profesjonalne banery z wkomponowanym sloganem i wezwaniem do działania.

### ⚙️ Parametry wejściowe w UI:
1.  **Wybór platformy docelowej (Rozmiar baneru):**
    *   `LinkedIn Banner` -> `1584 x 396` (Proporcje ok. 4:1)
    *   `Facebook Cover` -> `851 x 315`
    *   `Twitter/X Banner` -> `1500 x 500` (Proporcje 3:1)
    *   `YouTube Banner` -> `2048 x 1152` (Proporcje 16:9)
2.  **Styl tła graficznego:** (Identyczny jak style awatarów powyżej, aby zachować spójność wizualną).
3.  **Slogan na banerze:** Pobierany automatycznie ze zmiennej `motto` (np. *Automatyzuj powtarzalne. Twórz unikalne. Zyskaj.*).
4.  **CTA na banerze:** Wyświetlane pod sloganem ze zmiennej `cta` (np. *➔ Zacznij automatyzować, żyj lepiej.*).

---

### ⚠️ Krytyczna zasada kompozycji graficznej (UX Safety Rule):
Na wszystkich platformach społecznościowych zdjęcie profilowe użytkownika (okrągły awatar) jest nakładane po **lewej stronie** baneru. 
Aby uniknąć zasłonięcia tekstu, agent Streamlit **Musi wydać silnikowi graficznemu instrukcję**:
> *"Place all text, slogans, and branding elements strictly on the RIGHT side of the image, keeping the left and center areas clean, minimalist, and containing only background graphics."*

---

### 🔮 System Prompts & Prompt Blueprints dla BAXERÓW (Szerokokątne)

Podczas generowania banerów dla wybranego stylu, system wstrzykuje slogan i CTA w prawą część obrazu. Prompty wysyłane do silnika (np. Flux) muszą wyglądać tak:

#### 🌌 Baner Styl A (Cybernetic Hub):
> `"A premium panoramic cinematic wide shot of a futuristic dark control center. On the left and center, glowing glass analytics screens display abstract neural connection lines, cyan and purple networks, and subtle data charts. On the RIGHT side of the image, there is a clean, dark charcoal space featuring the glowing, elegant text: 'Automatyzuj powtarzalne. Twórz unikalne. Zyskaj.' with a smaller subtitle '➔ Zacznij automatyzować, żyj lepiej.' underneath. Sharp lighting, ultra-high resolution, minimalist layout, text is perfectly readable, 8k."`

#### 🌿 Baner Styl B (Cozy Server Sanctuary):
> `"A premium panoramic wide-angle shot of a warm minimalist server room. On the left and center, modern server racks with glowing soft amber and soft green lights are mixed with lush green potted plants and small bonsais. On the RIGHT side, on a clean, dark matte-wood wall, the following text is beautifully engraved: 'Automatyzuj powtarzalne. Twórz unikalne. Zyskaj.' with a subtitle '➔ Zacznij automatyzować, żyj lepiej.' below. Warm morning side lighting, quiet, cozy, photorealistic, 8k."`

#### 🌅 Baner Styl D (Biotech Garden / Freedom):
> `"An ultra-clean, minimalist wide-angle panoramic shot of a modern glass-clad workspace. On the left and center, a beautiful view of a quiet green biotech garden bathed in golden sunset light through huge clean windows. On the RIGHT side, on a pristine, dark anthracite concrete wall, the text: 'Automatyzuj powtarzalne. Twórz unikalne. Zyskaj.' and subtitle '➔ Zacznij automatyzować, żyj lepiej.' is subtly embossed in matte metallic letters. Sunset lighting, airy atmosphere, quiet operational freedom, 8k."`
