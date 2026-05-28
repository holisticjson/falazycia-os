"""
🧠 Kombajn Wiedzy (Knowledge Extractor Dashboard)
Połączony moduł do ekstrakcji wiedzy z platform szkoleniowych (Holistic Collector) oraz pojedynczych filmów (YouTube/Vimeo).
"""
import streamlit as st
import sys
import json
import time
from pathlib import Path
import importlib

sys.path.append(str(Path(__file__).parent))

# Dynamic reload to ensure freshness
if "skills.vimeo_transcriber" in sys.modules:
    importlib.reload(sys.modules["skills.vimeo_transcriber"])
if "skills.youtube_transcriber" in sys.modules:
    importlib.reload(sys.modules["skills.youtube_transcriber"])

from skills.vimeo_transcriber import process_vimeo_lesson_to_md, find_free_alternatives, fast_inject_description_locally
from skills.youtube_transcriber import process_course_video_to_md, batch_process_text, parse_youtube_batch_text
from skills.knowledge_zone import render_knowledge_zone

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
    if any(k in c_lower for k in ["ghl", "gohighlevel", "high level", "highlevel", "level university"]):
        return "GHL_University"
    return fallback_parent

def render_knowledge_extractor():
    st.title("🎓 Centrum Wiedzy (Ekstrakcja & Mapy Myśli)")
    st.markdown("""
    **Scentralizowany hub do pozyskiwania i eksploracji wiedzy edukacyjnej z całego Internetu.**  
    Przeglądaj wygenerowane drzewa wiedzy, lub użyj wtyczki **Holistic Collector** do zgrania całych platform 
    szkoleniowych. Dane zostaną automatycznie ustrukturyzowane jako głębokie protokoły dla agentów.
    """)

    baza_root = Path(r"c:\Aplikacje MVP\Holistic Jason\02_knowledge_base\raw")
    
    # Skanowanie istniejących folderów w Bazie Wiedzy
    existing_dirs = []
    if baza_root.exists():
        existing_dirs = sorted([d.name for d in baza_root.iterdir() if d.is_dir()])
    
    st.sidebar.subheader("📂 Konfiguracja Bazy")
    default_index = existing_dirs.index("Adrian Kilar Motion") if "Adrian Kilar Motion" in existing_dirs else 0
    selected_parent = st.sidebar.selectbox(
        "Katalog docelowy",
        options=existing_dirs + ["➕ Utwórz nowy folder..."],
        index=default_index
    )
    
    if selected_parent == "➕ Utwórz nowy folder...":
        target_parent = st.sidebar.text_input("Nazwa nowego folderu", value="Nowa_Wiedza")
    else:
        target_parent = selected_parent

    tab_platforms, tab_yt, tab_extractor, tab_tools = st.tabs([
        "🎓 Platformy Szkoleniowe (Import JSON)", 
        "▶️ Filmy i Social Media", 
        "🔌 Kod Wtyczki (JS)",
        "💡 Szukaj Alternatyw AI"
    ])

    # === ZAKŁADKA 1: PLATFORMY SZKOLENIOWE ===
    with tab_platforms:
        st.subheader("📦 Masowy Import Lekcji z Platform Kursowych")
        st.markdown(f"Importujesz do katalogu: **`02_knowledge_base/raw / {target_parent}`**")
        
        uploaded_files = st.file_uploader("📂 Prześlij wygenerowane pliki JSON", type=["json"], accept_multiple_files=True)
        batch_text = st.text_area("📄 LUB wklej skopiowany kod z wtyczki JS (JSON)", height=150)
        batch_module = st.text_input("📁 Domyślna nazwa modułu kursu", value="Ogólne")
        
        col1, col2 = st.columns(2)
        with col1:
            fast_local_enrich = st.checkbox("⚡ Szybki import opisu (Bez AI)", value=False)
        with col2:
            enrich_batch = st.checkbox("🔄 Tryb Wzbogacania (Enrich Mode)", value=True, disabled=fast_local_enrich)
            
        submit_batch = st.button("🚀 Uruchom Destylator Wiedzy", type="primary", use_container_width=True)

        if submit_batch:
            if not uploaded_files and not batch_text.strip():
                st.error("Wybierz pliki JSON lub wklej kod do pola tekstowego.")
            else:
                lessons_to_process = []
                if uploaded_files:
                    for u_file in uploaded_files:
                        try:
                            data = json.loads(u_file.read().decode("utf-8"))
                            if isinstance(data, list):
                                for item in data:
                                    lessons_to_process.append({
                                        "url": (item.get("url") or item.get("vimeo_url") or "").strip(),
                                        "title": (item.get("title") or item.get("lesson_title") or "Lekcja").strip(),
                                        "description": (item.get("description") or item.get("desc") or "").strip(),
                                        "module": (item.get("course") or item.get("module") or batch_module).strip()
                                    })
                        except Exception as e:
                            st.error(f"❌ Błąd: {e}")
                
                if batch_text.strip():
                    try:
                        data = json.loads(batch_text.strip())
                        if isinstance(data, list):
                            for item in data:
                                lessons_to_process.append({
                                    "url": (item.get("url") or item.get("vimeo_url") or "").strip(),
                                    "title": (item.get("title") or item.get("lesson_title") or "Lekcja").strip(),
                                    "description": (item.get("description") or item.get("desc") or "").strip(),
                                    "module": (item.get("course") or item.get("module") or batch_module).strip()
                                })
                    except json.JSONDecodeError:
                        st.error("Wklejony tekst nie jest poprawnym formatem JSON.")

                if lessons_to_process:
                    st.success(f"Znaleziono {len(lessons_to_process)} lekcji.")
                    progress_bar = st.progress(0.0)
                    status_area = st.empty()
                    
                    for idx, item in enumerate(lessons_to_process):
                        title = item["title"]
                        actual_parent = auto_detect_target_parent(item["module"], target_parent)
                        status_area.markdown(f"⚙️ Przetwarzanie [{idx+1}/{len(lessons_to_process)}]: **{title}**...")
                        
                        if fast_local_enrich:
                            res = fast_inject_description_locally(title, item["module"], item["description"], target_parent=actual_parent)
                        else:
                            res = process_vimeo_lesson_to_md(item["url"], title, item["module"], item["description"], overwrite=False, target_parent=actual_parent, enrich_mode=enrich_batch)
                        
                        st.write(res)
                        progress_bar.progress((idx + 1) / len(lessons_to_process))
                    
                    status_area.empty()
                    st.success("🎉 Zakończono masowy proces importu.")

    # === ZAKŁADKA 2: YOUTUBE I POJEDYNCZE LINKI ===
    with tab_yt:
        st.subheader("▶️ Pobieranie z YouTube i Social Mediów")
        with st.form("yt_single"):
            video_url = st.text_input("🔗 Link do filmu (YouTube, Vimeo, Shorts)")
            video_title = st.text_input("📝 Tytuł filmu/lekcji")
            submitted = st.form_submit_button("🚀 Procesuj Film", type="primary", use_container_width=True)

        if submitted and video_url and video_title:
            with st.spinner("Gemini 2.5 Flash / Pro analizuje treść..."):
                if "youtube" in video_url or "youtu.be" in video_url:
                    result = process_course_video_to_md(video_url, video_title)
                else:
                    # Traktuj jako link Vimeo (brak masowego JSON)
                    actual_parent = auto_detect_target_parent(batch_module, target_parent)
                    result = process_vimeo_lesson_to_md(video_url, video_title, batch_module, "", overwrite=False, target_parent=actual_parent)
                
                st.write(result)
                
        st.divider()
        st.markdown("**Masowy import YouTube z logów (Comet)**")
        yt_batch_text = st.text_area("Wklej listę linków z tytułami", height=150)
        if st.button("🚀 Masowo (YouTube)"):
            if yt_batch_text:
                results = parse_youtube_batch_text(yt_batch_text)
                if not results:
                    st.error("Nie znaleziono żadnych linków YouTube w tekście.")
                else:
                    st.success(f"Znaleziono {len(results)} linków wideo do przetworzenia.")
                    progress_bar = st.progress(0.0)
                    status_area = st.empty()
                    
                    for idx, item in enumerate(results):
                        url = item["url"]
                        title = item["title"]
                        
                        status_area.markdown(f"⚙️ Przetwarzanie [{idx+1}/{len(results)}]: **{title}**...")
                        res = process_course_video_to_md(url, title)
                        st.write(res)
                        
                        progress_bar.progress((idx + 1) / len(results))
                        
                    status_area.empty()
                    st.success("🎉 Zakończono masowy proces produkcji wiedzy z YouTube!")

    with tab_extractor:
        st.info("Poniższy skrypt radzi sobie z nowoczesnymi platformami (SPA, React) tworząc niewidoczną przeglądarkę (iframe) do odczytu wyrenderowanej treści.")
        deep_js_code = r"""// Skaner SPA (Umiejętności Jutra / React / Vue) - Wklej w konsoli na liście modułów
(async function() {
    console.log("🚀 Skaner SPA rozpoczął pracę...");
    let courseData = [];
    let courseBaseUrl = window.location.origin;
    let detectedCourseName = document.title || "Kurs SPA";
    
    // Zbieranie wszystkich unikalnych linków do lekcji z obecnej strony
    let allLinks = Array.from(document.querySelectorAll('a')).map(a => {
        let href = a.href.split('#')[0];
        // Naprawa błędu programistów platformy (React router łapiący zewnętrzne linki)
        if (href.includes('/http')) href = href.substring(href.indexOf('http'));
        return href;
    });
    
    // Zaawansowany filtr: wyrzucamy śmieciowe strony z platform
    let junkKeywords = ['/dashboard', '/faq', '/kontakt', '/webinars', '/spolecznosc', '/cookie', '/policy', '/study-schedules', '/login', '/cart', '/checkout', '/my-account', '/profil', '/ustawienia'];
    
    let lessonUrls = [...new Set(allLinks)].filter(href => {
        let u = href.toLowerCase();
        if (!u.startsWith(courseBaseUrl)) return false;
        if (u === window.location.href.toLowerCase().split('#')[0]) return false; // omijamy obecną stronę
        if (u.includes('/http')) return false;
        for (let j of junkKeywords) {
            if (u.includes(j)) return false;
        }
        // Zabezpieczenie przed pobieraniem stron-matek, interesują nas tylko linki głębsze
        return u.length > courseBaseUrl.length + 5;
    });
    
    // Pozostałe zewnętrzne linki od razu klasyfikujemy jako materiały ogólne (jeśli są)
    let globalDownloadLinks = [...new Set(allLinks)].filter(href => !href.startsWith(courseBaseUrl) && href.startsWith('http'));
    
    console.log(`Znaleziono ${lessonUrls.length} potencjalnych lekcji oraz ${globalDownloadLinks.length} zewnętrznych linków.`);
    
    // Tworzenie ukrytego iframe do renderowania stron
    let iframe = document.createElement('iframe');
    iframe.style.display = 'none';
    document.body.appendChild(iframe);
    
    const wait = ms => new Promise(r => setTimeout(r, ms));

    for (let i = 0; i < lessonUrls.length; i++) {
        let url = lessonUrls[i];
        console.log(`⏳ Skanowanie [${i+1}/${lessonUrls.length}]: ${url}`);
        
        iframe.src = url;
        await wait(5000); 
        
        try {
            let doc = iframe.contentDocument || iframe.contentWindow.document;
            
            // Wymuszamy przewinięcie na dół, żeby odpalić lazy-loading (np. dla ukrytych plików z Dysku)
            iframe.contentWindow.scrollTo(0, 9999);
            await wait(1000);
            
            // Wideo
            let iframes = doc.querySelectorAll('iframe');
            let videoUrl = "";
            iframes.forEach(ifr => {
                let src = ifr.src || ifr.getAttribute('data-src') || "";
                if (src.includes('vimeo') || src.includes('youtube') || src.includes('youtu.be') || src.includes('bunny') || src.includes('wistia')) videoUrl = src;
            });
            if (!videoUrl) {
                let videoTag = doc.querySelector('video');
                if (videoTag) videoUrl = videoTag.src || videoTag.querySelector('source')?.src || "";
            }
            
            // Opis
            let descSelectors = '.course-lesson-body, .lesson-body, .lesson-content, .post-content, .post-body, .html-content, .ld-tab-content, .learndash-wrapper, article, .entry-content, .lesson-description, main, [class*="content"]';
            let descElement = doc.querySelector(descSelectors);
            let description = descElement ? descElement.innerText.trim() : "";
            
            // Wyciąganie linków do pobrania (Dysku Google, PDF, narzędzia) z danej lekcji
            let downloadLinks = [];
            if (descElement) {
                let hrefs = Array.from(descElement.querySelectorAll('a')).map(a => {
                    let h = a.href;
                    if (h.includes('/http')) h = h.substring(h.indexOf('http'));
                    return { text: a.innerText.trim() || h, url: h };
                });
                
                downloadLinks = hrefs.filter(h => {
                    if (!h.url) return false;
                    let u = h.url.toLowerCase();
                    return !u.includes(window.location.hostname) && 
                           u.startsWith('http') && 
                           !u.includes('vimeo.com') && 
                           !u.includes('youtube.com');
                });
            }

            if (downloadLinks.length > 0) {
                description += "\n\n📥 **Materiały do pobrania / Narzędzia:**\n" + 
                               downloadLinks.map(dl => `- [${dl.text}](${dl.url})`).join('\n');
            }
            
            let titleEl = doc.querySelector('.lesson-title') || doc.querySelector('.post-title') || doc.querySelector('h1') || doc.querySelector('h2') || doc.querySelector('.lesson-header');
            let title = titleEl ? titleEl.innerText.trim() : doc.title;
            
            if (videoUrl || description.length > 50 || downloadLinks.length > 0) {
                courseData.push({
                    course: detectedCourseName, 
                    title: title, 
                    url: videoUrl, 
                    description: description.substring(0, 5000)
                });
                console.log(`✅ Zapisano: ${title}`);
            }
        } catch (err) {
            console.error(`❌ Błąd dostępu do iframe dla ${url}:`, err);
        }
    }
    
    document.body.removeChild(iframe);
    
    if (courseData.length > 0) {
        let outputJson = JSON.stringify(courseData, null, 2);
        try {
            let dummy = document.createElement("textarea");
            document.body.appendChild(dummy);
            dummy.value = outputJson;
            dummy.select();
            document.execCommand("copy");
            document.body.removeChild(dummy);
            alert(`Sukces! Zeskanowano ${courseData.length} lekcji. Kod JSON znajduje się w schowku.`);
        } catch (e) {
            window.scrapedData = outputJson;
            console.log(outputJson);
            alert("Nie można skopiować (blokada). Wpisz w konsoli 'copy(scrapedData)'.");
        }
    } else {
        alert("Nie znaleziono materiałów. Upewnij się, że uruchamiasz skrypt na odpowiedniej podstronie.");
    }
})();"""
        st.code(deep_js_code, language="javascript")

    # === ZAKŁADKA 4: ALTERNATYWY ===
    with tab_tools:
        st.subheader("💡 Darmowe Alternatywy Narzędzi AI")
        search_tool = st.text_input("Nazwa płatnego programu (np. ElevenLabs, HeyGen)")
        if st.button("🔍 Szukaj"):
            st.markdown(find_free_alternatives(search_tool))

