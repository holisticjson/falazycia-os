"""
📹 Vimeo & Universal Course Transcriber (Dashboard UI)
Masowe przetwarzanie lekcji z platformy kursowej w notatki Bazy Wiedzy.
"""
import streamlit as st
import sys
import json
import time
from pathlib import Path
import importlib

sys.path.append(str(Path(__file__).parent))

# Wymuszenie przeładowania modułu skills.vimeo_transcriber przy każdym przeładowaniu Streamlita
if "skills.vimeo_transcriber" in sys.modules:
    importlib.reload(sys.modules["skills.vimeo_transcriber"])

from skills.vimeo_transcriber import process_vimeo_lesson_to_md, find_free_alternatives, fast_inject_description_locally

def auto_detect_target_parent(course_name: str, fallback_parent: str) -> str:
    """Auto-detects target folder in Baza_Wiedzy based on course/module name keywords."""
    c_lower = course_name.lower()
    
    # Obsługa Google Umiejętności Jutra (zarówno z fallback_parent jak i autodetekcji)
    is_guj = "umiejętności jutra" in c_lower or "guj" in c_lower or fallback_parent == "Google Umiejętności Jutra"
    
    if is_guj:
        # Słowa kluczowe dla Tygodnia 1
        t1_keywords = [
            "wprowadzenie do tygodnia 1", "fundamenty pracy", "generatywną ai", "bielik.ai", "bielik",
            "deep research", "notebooklm", "strategie skutecznego", "pierwsi asystenci", "bezpieczeństwo i szersze", "produktywność osobista"
        ]
        # Słowa kluczowe dla Tygodnia 2
        t2_keywords = [
            "pisanie skutecznych", "tworzenie treści wizualnych", "od pomysłu do mvp", "ai w sprzedaży", 
            "ai w marketingu", "notebooklm w obsłudze", "tworzenie treści i rozwój"
        ]
        # Słowa kluczowe dla Tygodnia 3
        t3_keywords = [
            "wprowadzenie do agentów", "automatyzacja jako umiejętność", "budowa agentów", "n8n", 
            "elevenlabs", "głosowego agenta", "ekosystemie google", "praktyczne przykłady automatyzacji", "asystentami i agentami"
        ]
        
        if any(k in c_lower for k in t1_keywords):
            return r"Google Umiejętności Jutra\Tydzień 1 - Fundamenty AI i produktywność osobista"
        elif any(k in c_lower for k in t2_keywords):
            return r"Google Umiejętności Jutra\Tydzień 2 - Tworzenie treści i rozwój biznesu z AI"
        elif any(k in c_lower for k in t3_keywords):
            return r"Google Umiejętności Jutra\Tydzień 3 - Automatyzacja pracy z asystentami i agentami AI"
            
        return r"Google Umiejętności Jutra"

    if any(k in c_lower for k in ["szopa", "pdf masterclass", "zdalnej agencji", "zdalna agencja"]):
        return "Jan Szopa - Akademia Zdalnej Agencji Marketingowej"
    if any(k in c_lower for k in ["kilar", "ai magic", "ai master", "motion", "mowi kamera"]):
        return "Adrian Kilar Motion"
    if any(k in c_lower for k in ["automatyzacji", "akademia automatyzacji"]):
        return "Akademia Automatyzacji"
    return fallback_parent

def render_vimeo_transcriber():
    st.title("📹 Universal Course & Video Transcriber")
    st.markdown("""
    **Uniwersalne, inteligentne narzędzie do masowego nadrabiania i syntezy specjalistycznych kursów wideo.**  
    Generuj gęste notatki szkoleniowe oparte na wideo (Vimeo, BunnyCDN, Wistia, YouTube, HTML5), wzbogacone o opisy z platformy i darmowe alternatywy.
    """)

    baza_root = Path(r"c:\Aplikacje MVP\Holistic Jason\Baza_Wiedzy")
    
    # Skanowanie istniejących folderów w Bazie Wiedzy
    existing_dirs = []
    if baza_root.exists():
        existing_dirs = sorted([d.name for d in baza_root.iterdir() if d.is_dir()])
    
    # Wybór folderu docelowego w Bazie Wiedzy
    st.sidebar.subheader("📂 Konfiguracja Zapisów")
    
    default_index = existing_dirs.index("Adrian Kilar Motion") if "Adrian Kilar Motion" in existing_dirs else 0
    
    selected_parent = st.sidebar.selectbox(
        "Wybierz folder docelowy w Bazie Wiedzy",
        options=existing_dirs + ["➕ Utwórz nowy folder..."],
        index=default_index
    )
    
    if selected_parent == "➕ Utwórz nowy folder...":
        target_parent = st.sidebar.text_input("Wpisz nazwę nowego folderu", value="Nowy_Kurs_Wiedza")
    else:
        target_parent = selected_parent

    # Liczenie notatek w wybranym folderze
    target_dir_path = baza_root / target_parent
    existing_files = list(target_dir_path.glob("**/*.md")) if target_dir_path.exists() else []
    st.metric(f"📚 Łączna liczba notatek w '{target_parent}'", len(existing_files))

    tab_extractor, tab_single, tab_batch, tab_tools, tab_notes = st.tabs([
        "🔌 1. Głęboki Ekstraktor (JS)",
        "⚡ 2. Pojedyncza Lekcja",
        "📦 3. Masowy Import (JSON/Tekst)",
        "💡 4. Alternatywy Narzędzi AI",
        "📚 5. Gotowe Notatki"
    ])

    # === TAB 1: SCRAPER JS ===
    with tab_extractor:
        st.subheader("🔌 Uniwersalny Ekstraktor Lekcji (JS) - Sesje Zalogowane")
        st.markdown(f"""
        Ten skrypt działa w przeglądarce i **automatycznie wykrywa nazwę kursu oraz dowolne odtwarzacze wideo** (Vimeo, YouTube, Wistia, BunnyCDN, HTML5) osadzone na lekcjach!
        
        **Instrukcja:**
        1. Wejdź na **główną stronę kursu lub platformy szkoleniowej**.
        2. Otwórz Konsolę Deweloperską: kliknij prawym przyciskiem myszy -> **Zbadaj** (lub wciśnij **F12**), a następnie wybierz zakładkę **Console** (Konsola).
        3. Skopiuj poniższy kod, wklej go do konsoli i wciśnij **Enter**.
        4. Skrypt pobierze dane lekcji, **skopiuje JSON do schowka**.
        
        *Wskazówka: Gdyby schowek systemowy zablokował kopiowanie, po prostu wpisz w konsoli `copy(scrapedData)` i wciśnij Enter!*
        """)

        deep_js_code = r"""// Uniwersalny Skrypt Crawler'a - wklej na głównej stronie dowolnego kursu:
(async function() {
    console.log("🚀 Rozpoczynam automatyczne skanowanie całego kursu...");
    let courseData = [];
    
    // Auto-detekcja tytułu kursu z nagłówka H1
    let detectedCourseName = document.querySelector('h1')?.innerText.trim() || document.title || "Universal Course";
    console.log("Detected Course:", detectedCourseName);
    
    // Ustalamy bazowy URL kursu, aby wchodzić tylko w jego podstrony (dzieci)
    let courseBaseUrl = window.location.href.split('?')[0].split('#')[0];
    if (!courseBaseUrl.endsWith('/')) {
        courseBaseUrl += '/';
    }
    
    // Funkcja pancernego kopiowania
    function copyToClipboard(text) {
        try {
            let dummy = document.createElement("textarea");
            document.body.appendChild(dummy);
            dummy.value = text;
            dummy.select();
            document.execCommand("copy");
            document.body.removeChild(dummy);
            return true;
        } catch (e) {
            console.error("Błąd pancernego kopiowania:", e);
            return false;
        }
    }
    
    // 1. Znajdź wszystkie odnośniki na stronie głównej kursu
    let mainLinks = Array.from(document.querySelectorAll('a')).map(a => a.href.split('?')[0].split('#')[0]);
    let moduleUrls = [...new Set(mainLinks)].filter(href => {
        return href.startsWith(courseBaseUrl) && href.length > courseBaseUrl.length;
    });

    console.log(`Zidentyfikowano ${moduleUrls.length} precyzyjnych sekcji/lekcji do przeszukania. Rozpoczynam crawl...`);
    
    for (let uIdx = 0; uIdx < moduleUrls.length; uIdx++) {
        let mUrl = moduleUrls[uIdx];
        console.log(`[Crawl ${uIdx+1}/${moduleUrls.length}] Analiza: ${mUrl}`);
        
        try {
            let response = await fetch(mUrl);
            if (response.status !== 200) {
                console.warn(`   ⚠️ Pomijam (Status ${response.status}): ${mUrl}`);
                continue;
            }
            let htmlText = await response.text();
            let parser = new DOMParser();
            let doc = parser.parseFromString(htmlText, 'text/html');
            
            // Szukamy wideo
            let iframes = doc.querySelectorAll('iframe');
            let hasVideo = false;
            let videoUrl = "";
            
            iframes.forEach(iframe => {
                let src = iframe.src || iframe.getAttribute('data-src') || "";
                if (src.includes('vimeo.com') || src.includes('youtube.com') || src.includes('youtu.be') || src.includes('wistia') || src.includes('bunny') || src.includes('vzaar') || src.includes('player.')) {
                    hasVideo = true;
                    videoUrl = src;
                }
            });
            
            if (!hasVideo) {
                let videoTag = doc.querySelector('video');
                if (videoTag) {
                    let src = videoTag.src || videoTag.querySelector('source')?.src || "";
                    if (src) {
                        hasVideo = true;
                        videoUrl = src;
                    }
                }
            }
            
            // Pancerne pobieranie opisu
            let description = "";
            let descElement = doc.querySelector('.ld-tab-content, .learndash-wrapper, .ld-lesson-content, article, .entry-content, .post-content, #content, .main-content, .wp-block-post-content, .lesson-content, #lesson-description');
            if (descElement) {
                description = descElement.innerText.trim();
            } else {
                let mainElements = Array.from(doc.querySelectorAll('p, li, h2, h3, h4')).filter(el => {
                    let parentString = "";
                    let parent = el.parentElement;
                    while(parent) {
                        parentString += " " + (parent.className || "") + " " + (parent.id || "");
                        parent = parent.parentElement;
                    }
                    parentString = parentString.toLowerCase();
                    return !parentString.includes('menu') && 
                           !parentString.includes('nav') && 
                           !parentString.includes('footer') && 
                           !parentString.includes('sidebar') && 
                           !parentString.includes('header') &&
                           !parentString.includes('widget');
                });
                description = mainElements.map(el => el.innerText.trim()).filter(t => t.length > 5).join('\n');
            }

            // Szukanie linków zewnętrznych (materiały do pobrania, np. Google Drive, Dropbox, ChatGPT)
            let downloadLinks = [];
            if (descElement) {
                let hrefs = Array.from(descElement.querySelectorAll('a')).map(a => ({
                    text: a.innerText.trim() || a.href,
                    url: a.href
                }));
                downloadLinks = hrefs.filter(h => {
                    if (!h.url) return false;
                    let u = h.url.toLowerCase();
                    return !u.includes(window.location.hostname) && 
                           u.startsWith('http') && 
                           !u.includes('vimeo.com') && 
                           !u.includes('youtube.com') && 
                           !u.includes('youtu.be') && 
                           !u.includes('player.vimeo');
                });
            }

            if (downloadLinks.length > 0) {
                description += "\n\n📥 **Materiały do pobrania / Linki:**\n" + 
                               downloadLinks.map(dl => `- [${dl.text}](${dl.url})`).join('\n');
            }

            // Czy to jest lekcja? (ma wideo LUB ma opis > 30 znaków LUB ma linki do pobrania)
            let isLesson = hasVideo || (description.length > 30) || (downloadLinks.length > 0);

            if (isLesson) {
                let title = doc.querySelector('h1, h2, h3, .lesson-title, .title-lesson')?.innerText.trim() || doc.title || "Lekcja";
                
                courseData.push({
                    course: detectedCourseName,
                    title: title,
                    url: videoUrl,
                    description: description,
                    lesson_url: mUrl
                });
                console.log(`   ✅ Dodano lekcję: ${title} (${videoUrl || 'Brak wideo'})`);
            } else {
                // Spis treści sekcji - szukamy lekcji wewnątrz
                let subLinks = Array.from(doc.querySelectorAll('a')).map(a => a.href.split('?')[0].split('#')[0]);
                let lessonUrls = [...new Set(subLinks)].filter(href => {
                    return href.startsWith(courseBaseUrl) && href.length > courseBaseUrl.length && href !== mUrl;
                });
                
                console.log(`   -> Zlokalizowano ${lessonUrls.length} lekcji w tym module. Crawling...`);
                for (let lIdx = 0; lIdx < lessonUrls.length; lIdx++) {
                    let lUrl = lessonUrls[lIdx];
                    if (courseData.some(d => d.lesson_url === lUrl)) continue;
                    
                    try {
                        let lRes = await fetch(lUrl);
                        if (lRes.status !== 200) continue;
                        let lHtml = await lRes.text();
                        let lDoc = parser.parseFromString(lHtml, 'text/html');
                        
                        let lIframes = lDoc.querySelectorAll('iframe');
                        let lvUrl = "";
                        lIframes.forEach(iframe => {
                            let src = iframe.src || iframe.getAttribute('data-src') || "";
                            if (src.includes('vimeo.com') || src.includes('youtube.com') || src.includes('youtu.be') || src.includes('wistia') || src.includes('bunny') || src.includes('vzaar') || src.includes('player.')) {
                                lvUrl = src;
                            }
                        });
                        
                        if (!lvUrl) {
                            let lVideoTag = lDoc.querySelector('video');
                            if (lVideoTag) {
                                lvUrl = lVideoTag.src || lVideoTag.querySelector('source')?.src || "";
                            }
                        }
                        
                        let lDesc = "";
                        let lDescEl = lDoc.querySelector('.ld-tab-content, .learndash-wrapper, .ld-lesson-content, article, .entry-content, .post-content, #content, .main-content, .wp-block-post-content, .lesson-content, #lesson-description');
                        if (lDescEl) {
                            lDesc = lDescEl.innerText.trim();
                        } else {
                            let lMainElements = Array.from(lDoc.querySelectorAll('p, li, h2, h3, h4')).filter(el => {
                                let lParentString = "";
                                let lParent = el.parentElement;
                                while(lParent) {
                                    lParentString += " " + (lParent.className || "") + " " + (lParent.id || "");
                                    lParent = lParent.parentElement;
                                }
                                lParentString = lParentString.toLowerCase();
                                return !lParentString.includes('menu') && 
                                       !lParentString.includes('nav') && 
                                       !lParentString.includes('footer') && 
                                       !lParentString.includes('sidebar') && 
                                       !lParentString.includes('header') &&
                                       !lParentString.includes('widget');
                            });
                            lDesc = lMainElements.map(el => el.innerText.trim()).filter(t => t.length > 5).join('\n');
                        }

                        let lDownloadLinks = [];
                        if (lDescEl) {
                            let lHrefs = Array.from(lDescEl.querySelectorAll('a')).map(a => ({
                                text: a.innerText.trim() || a.href,
                                url: a.href
                            }));
                            lDownloadLinks = lHrefs.filter(h => {
                                if (!h.url) return false;
                                let u = h.url.toLowerCase();
                                return !u.includes(window.location.hostname) && 
                                       u.startsWith('http') && 
                                       !u.includes('vimeo.com') && 
                                       !u.includes('youtube.com') && 
                                       !u.includes('youtu.be') && 
                                       !u.includes('player.vimeo');
                            });
                        }

                        if (lDownloadLinks.length > 0) {
                            lDesc += "\n\n📥 **Materiały do pobrania / Linki:**\n" + 
                                     lDownloadLinks.map(dl => `- [${dl.text}](${dl.url})`).join('\n');
                        }

                        let lIsLesson = lvUrl || (lDesc.length > 30) || (lDownloadLinks.length > 0);
                        
                        if (lIsLesson) {
                            let lTitle = lDoc.querySelector('h1, h2, h3, .lesson-title, .title-lesson')?.innerText.trim() || lDoc.title || "Lekcja";
                            
                            courseData.push({
                                course: detectedCourseName,
                                title: lTitle,
                                url: lvUrl,
                                description: lDesc,
                                lesson_url: lUrl
                            });
                            console.log(`      ✅ [${lIdx+1}/${lessonUrls.length}] Zaimportowano lekcję: ${lTitle}`);
                        }
                    } catch (err) {
                        console.error(`Błąd pobierania lekcji ${lUrl}:`, err);
                    }
                }
            }
        } catch (err) {
            console.error(`Błąd pobierania modułu ${mUrl}:`, err);
        }
    }
    
    if (courseData.length > 0) {
        let outputJson = JSON.stringify(courseData, null, 2);
        console.log("%c🎉 UKOŃCZONO AUTOMATYCZNY SKAN CAŁEGO KURSU!", "color: green; font-size: 20px; font-weight: bold;");
        
        window.scrapedData = outputJson;
        console.log("Dane zapisano w zmiennej: scrapedData");
        
        let copied = copyToClipboard(outputJson);
        if (copied) {
            alert(`Sukces! Zeskanowano automatycznie ${courseData.length} lekcji z kursu "${detectedCourseName}" i skopiowano JSON do schowka!`);
        } else {
            console.log(outputJson);
            alert(`Zeskanowano ${courseData.length} lekcji. Przeglądarka zablokowała schowek. JSON został w konsoli lub wpisz: copy(scrapedData)`);
        }
    } else {
        alert("Nie udało się automatycznie wyciągnąć danych. Upewnij się, że jesteś na głównej stronie kursu.");
    }
})();"""

        st.code(deep_js_code, language="javascript")

    # === TAB 2: POJEDYNCZA LEKCJA ===
    with tab_single:
        st.subheader("⚡ Procesuj pojedynczą lekcję")
        st.markdown(f"Zapisywana do folderu: **`Baza_Wiedzy / {target_parent}`**")
        with st.form("vimeo_single_form"):
            vimeo_url = st.text_input("🔗 Link do wideo (Vimeo/BunnyCDN/YouTube/itp.)", placeholder="np. https://player.vimeo.com/video/123456789")
            lesson_title = st.text_input("📝 Tytuł Lekcji", placeholder="np. Nano Banana Pro - Gemini w akcji")
            lesson_desc = st.text_area("📄 Opis lekcji (opcjonalny, pod wideo)", placeholder="Wklej tekst lub notatki pod filmem z platformy...")
            module_name = st.text_input("📁 Nazwa Kursu / Modułu", value="Kurs")
            overwrite_single = st.checkbox("🔄 Nadpisz istniejącą notatkę", value=False)
            enrich_single = st.checkbox("🔄 Wzbogać istniejącą notatkę (Enrich Mode)", value=False)
            submit_single = st.form_submit_button("🚀 Generuj notatkę z wiedzą", type="primary", use_container_width=True)

        if submit_single and vimeo_url and lesson_title:
            with st.spinner("Pobieranie danych, analiza i synteza notatki..."):
                actual_parent = auto_detect_target_parent(module_name, target_parent)
                result = process_vimeo_lesson_to_md(vimeo_url, lesson_title, module_name, lesson_desc, overwrite=overwrite_single, target_parent=actual_parent, enrich_mode=enrich_single)
                if "✅" in result:
                    st.success(result)
                elif "⏭️" in result:
                    st.info(result)
                else:
                    st.error(result)

    # === TAB 3: BATCH PROCESSING ===
    with tab_batch:
        st.subheader("📦 Masowy Import / Uzdatnianie Lekcji")
        st.markdown(f"Wszystkie notatki zostaną zapisane lub wzbogacone w folderze: **`Baza_Wiedzy / {target_parent}`**")
        
        uploaded_files = st.file_uploader("📂 Przeslij jeden lub wiele plikow JSON (np. wygenerowanych przez wtyczke Holistic)", type=["json"], accept_multiple_files=True)
        
        batch_text = st.text_area("📄 LUB wklej dane do importu (JSON / lista URL wideo)", height=150, 
                                  placeholder='[\n  {\n    "course": "AI MAGIC VIDEO EDITOR",\n    "title": "Jak dziala SORA...",\n    "url": "https://player.vimeo.com/video/...",\n    "description": "Pelny opis..."\n  }\n]')
        
        batch_module = st.text_input("📁 Domyslna nazwa modulu (jesli brak w JSON)", value="Kurs")
        
        st.markdown("### ⚙️ Tryb Dzialania:")
        fast_local_enrich = st.checkbox("⚡ Szybki import opisu (Bez AI)", value=False,
                                        help="Zaznacz, aby blyskawicznie (w ulamku sekundy) wkleic opis z platformy do istniejacych plikow notatek jako wstep. Calkowicie BEZ odpytywania API Gemini!")
        
        enrich_batch = st.checkbox("🔄 Tryb Wzbogacania AI (Enrich Mode)", value=True, 
                                    disabled=fast_local_enrich,
                                    help="Zaznacz, aby dopisac nowe, dlugie opisy lekcji do juz istniejacych notatek na dysku przy uzyciu Gemini (syntetyzowanie transkrypcji i opisu).")
        
        overwrite_batch = st.checkbox("🔥 Nadpisz wszystko (Overwrite)", value=False, 
                                      disabled=fast_local_enrich,
                                      help="Zaznacz, aby wygenerowac notatki calkowicie od zera przy uzyciu Gemini, ignorujac istniejace checkpointy.")
        
        submit_batch = st.button("🚀 Rozpocznij masowy proces", type="primary", use_container_width=True)

        if submit_batch:
            if not uploaded_files and not batch_text.strip():
                st.error("Wybierz pliki JSON do przeslania LUB wklej kod do pola tekstowego.")
            else:
                lessons_to_process = []
                
                # 1. Przetwarzanie przesłanych plików JSON
                if uploaded_files:
                    for u_file in uploaded_files:
                        try:
                            file_content = u_file.read().decode("utf-8")
                            data = json.loads(file_content)
                            if isinstance(data, list):
                                for item in data:
                                    url = item.get("url") or item.get("vimeo_url") or ""
                                    title = item.get("title") or item.get("lesson_title") or "Lekcja"
                                    desc = item.get("description") or item.get("desc") or ""
                                    mod = item.get("course") or item.get("module") or batch_module
                                    if title:
                                        lessons_to_process.append({
                                            "url": url.strip(),
                                            "title": title.strip(),
                                            "description": desc.strip(),
                                            "module": mod.strip()
                                        })
                                st.info(f"📂 Zaladowano {len(data)} lekcji z pliku: `{u_file.name}`")
                            else:
                                st.warning(f"⚠️ Plik `{u_file.name}` nie zawiera listy JSON.")
                        except Exception as e:
                            st.error(f"❌ Blad odczytu pliku `{u_file.name}`: {e}")
                
                # 2. Przetwarzanie wklejonego tekstu
                if batch_text.strip():
                    try:
                        data = json.loads(batch_text.strip())
                        if isinstance(data, list):
                            for item in data:
                                url = item.get("url") or item.get("vimeo_url") or ""
                                title = item.get("title") or item.get("lesson_title") or "Lekcja"
                                desc = item.get("description") or item.get("desc") or ""
                                mod = item.get("course") or item.get("module") or batch_module
                                if title:
                                        lessons_to_process.append({
                                            "url": url.strip(),
                                            "title": title.strip(),
                                            "description": desc.strip(),
                                            "module": mod.strip()
                                        })
                            st.info(f"📝 Zaladowano lekcje z wklejonego tekstu JSON.")
                    except json.JSONDecodeError:
                        # Fallback do zwykłego tekstu linia po linii
                        lines = batch_text.split('\n')
                        text_lessons_count = 0
                        for i, line in enumerate(lines):
                            if "vimeo.com" in line or "youtube.com" in line or "youtu.be" in line or "bunny" in line or "wistia" in line or "http" in line:
                                title = "Lekcja bez tytulu"
                                for j in range(i-1, max(-1, i-4), -1):
                                    potential_title = lines[j].strip()
                                    if potential_title and "http" not in potential_title and len(potential_title) > 3:
                                        title = potential_title
                                        break
                                lessons_to_process.append({
                                    "url": line.strip(),
                                    "title": title.strip(),
                                    "description": "",
                                    "module": batch_module
                                })
                                text_lessons_count += 1
                        if text_lessons_count > 0:
                            st.info(f"📝 Zaladowano {text_lessons_count} odnosnikow wideo z listy tekstowej.")
                
                if not lessons_to_process:
                    st.error("Nie znaleziono zadnych poprawnych danych do zaimportowania.")
                else:
                    st.success(f"Znaleziono LACZNIE {len(lessons_to_process)} lekcji do przetworzenia!")
                progress_bar = st.progress(0.0)
                status_area = st.empty()
                
                for idx, item in enumerate(lessons_to_process):
                    title = item["title"]
                    url = item["url"]
                    desc = item["description"]
                    mod = item["module"]
                    
                    actual_parent = auto_detect_target_parent(mod, target_parent)
                    
                    status_area.markdown(f"⚙️ [{idx+1}/{len(lessons_to_process)}] Przetwarzanie: **{title}** (Folder: `{actual_parent}`)...")
                    
                    # Szybki bypass dla pustych nagłówków / sekcji bez wideo i bez opisu
                    v_url = (url or "").strip()
                    l_desc = (desc or "").strip()
                    if not v_url and not l_desc:
                        safe_course_folder = "".join([c if c.isalnum() or c in (" ", "_", "-") else "_" for c in mod]).strip().replace(" ", "_")
                        baza_dir = Path(r"c:\Aplikacje MVP\Holistic Jason\Baza_Wiedzy") / actual_parent / safe_course_folder
                        safe_title = "".join([c if c.isalnum() else "_" for c in title])[:80]
                        file_path = baza_dir / f"{safe_title}.md"
                        try:
                            baza_dir.mkdir(exist_ok=True, parents=True)
                            placeholder_content = (
                                f"# NOTATKA / SEKCJA: {title}\n\n"
                                f"**Kurs/Moduł:** {mod}\n"
                                f"**Status:** Sekcja organizacyjna / Brak materiałów\n\n"
                                f"---\n\n"
                                f"*Ta sekcja nie zawiera nagrania wideo ani opisu tekstowego na platformie.*"
                            )
                            with open(file_path, "w", encoding="utf-8") as f:
                                f.write(placeholder_content)
                            res = f"✅ Zapisano pusty szablon dla sekcji: {file_path.name}"
                        except Exception as e:
                            res = f"❌ Błąd zapisu szablonu sekcji: {e}"
                    elif fast_local_enrich:
                        res = fast_inject_description_locally(
                            title, mod, desc,
                            target_parent=actual_parent
                        )
                    else:
                        res = process_vimeo_lesson_to_md(
                            url, title, mod, desc, 
                            overwrite=overwrite_batch, 
                            target_parent=actual_parent, 
                            enrich_mode=enrich_batch
                        )
                    
                    if "⏭️" in res:
                        st.write(f"⏭️ Lekcja **{title}** już istnieje (pominięto).")
                    elif "Uzdatniono" in res or "błyskawicznie" in res:
                        st.write(f"🔄 Wzbogacono i uzdatniono: **{title}**")
                        time.sleep(3.0) # Cooldown to protect Gemini TPM/RPM limits
                    elif "✅" in res:
                        st.write(f"✅ Zsyntetyzowano od zera: **{title}**")
                        if "pusty szablon" not in res:
                            time.sleep(3.0) # Cooldown to protect Gemini TPM/RPM limits
                    else:
                        st.write(f"❌ Błąd lekcji **{title}**: {res}")
                        
                    progress_bar.progress((idx + 1) / len(lessons_to_process))
                
                status_area.empty()
                st.success("🎉 Zakończono masowy proces! Wszystkie lekcje zostały zaktualizowane!")

    # === TAB 4: ALTERNATYWY AI ===
    with tab_tools:
        st.subheader("💡 Research darmowych alternatyw dla narzędzi premium")
        st.write("Wpisz nazwę płatnego programu, aby AI znalazło darmowe i open-source opcje.")
        
        search_tool = st.text_input("Wpisz nazwę narzędzia (np. Magnific, ElevenLabs, Midjourney, HeyGen)", "Magnific AI")
        if st.button("🔍 Szukaj darmowych opcji"):
            with st.spinner("AI szuka darmowych alternatyw..."):
                alts = find_free_alternatives(search_tool)
                st.markdown(alts)

    # === TAB 5: LIST OF NOTES ===
    with tab_notes:
        st.subheader(f"📚 Gotowe Notatki w folderze '{target_parent}'")
        if target_dir_path.exists():
            # Znajdź podfoldery kursów
            course_folders = [d for d in target_dir_path.iterdir() if d.is_dir()]
            if course_folders:
                for c_folder in course_folders:
                    st.markdown(f"### 📁 Kurs: `{c_folder.name.replace('_', ' ')}`")
                    c_files = list(c_folder.glob("*.md"))
                    if c_files:
                        for f in sorted(c_files, key=lambda x: x.stat().st_mtime, reverse=True):
                            with st.expander(f"📄 {f.name} ({f.stat().st_size/1024:.1f} KB)"):
                                with open(f, "r", encoding="utf-8") as fh:
                                    st.markdown(fh.read()[:4000])
                    else:
                        st.info("Brak notatek w tym kursie.")
            else:
                # Brak podfolderów, może są luźne pliki w root?
                root_files = list(target_dir_path.glob("*.md"))
                if root_files:
                    for f in sorted(root_files, key=lambda x: x.stat().st_mtime, reverse=True):
                        with st.expander(f"📄 {f.name}"):
                            with open(f, "r", encoding="utf-8") as fh:
                                st.markdown(fh.read()[:4000])
                else:
                    st.info("Brak notatek. Wybierz inną bazę docelową lub przetwórz pierwszą lekcję powyżej! ☝️")
        else:
            st.info("Ten folder bazy docelowej nie ma jeszcze żadnych notatek.")
