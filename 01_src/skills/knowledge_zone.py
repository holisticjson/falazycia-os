"""
🧠 CENTRUM WIEDZY — Moduł Strefa Głębokiej Wiedzy
Mapy myśli + Drzewo lekcji z notatkami per Tydzień kursu
"""
import streamlit as st
import streamlit.components.v1 as components
import os
import json
from pathlib import Path

# ─── ŚCIEŻKI ───────────────────────────────────────────────────────────────
BAZA_ROOT = Path(r"c:\Aplikacje MVP\Holistic Jason\02_knowledge_base\raw")
UJ_ROOT   = BAZA_ROOT / "Google Umiejętności Jutra 3.0"
MINDMAP_DIR = UJ_ROOT  # HTML mapy myśli leżą tam


# ─── HELPERS ───────────────────────────────────────────────────────────────
def _read_md(path: Path) -> str:
    try:
        return path.read_text(encoding="utf-8")
    except Exception as e:
        return f"⚠️ Błąd odczytu: {e}"


def _module_icon(name: str) -> str:
    mapping = {
        "fundamenty": "🔰", "notebook": "📓", "strategi": "🎯",
        "pierwsi": "🤖", "deep": "🔬", "bielik": "🇵🇱",
        "bezpiecze": "🛡️", "wprowadzenie": "📘", "pisanie": "✍️",
        "tworzenie": "🎨", "pomysłu": "🛠️", "mvp": "🛠️",
        "sprzeda": "💼", "marketin": "📊", "notebooklm": "🎙️",
    }
    lower = name.lower()
    for key, icon in mapping.items():
        if key in lower:
            return icon
    return "📁"


# ─── DRZEWO LEKCJI ─────────────────────────────────────────────────────────
def _render_week_tree(week_path: Path):
    """Renderuje moduły i lekcje danego tygodnia jako rozwijalne karty."""
    modules = sorted([d for d in week_path.iterdir() if d.is_dir()])
    if not modules:
        st.info("Brak modułów w tym tygodniu.")
        return

    for mod in modules:
        icon = _module_icon(mod.name)
        desc_path = mod / "1.1_Opis kursu.md"
        desc = _read_md(desc_path) if desc_path.exists() else ""
        # Oczyść opis
        desc_clean = desc.replace("Opis kursu:", "").replace("Opis kursu", "").strip()

        with st.expander(f"{icon} **{mod.name}**", expanded=False):
            if desc_clean:
                st.markdown(
                    f"<div style='background:rgba(74,144,226,0.07);border-left:4px solid #4A90E2;"
                    f"padding:10px 14px;border-radius:8px;margin-bottom:12px;"
                    f"font-size:0.88rem;color:#1e293b'>{desc_clean}</div>",
                    unsafe_allow_html=True
                )

            # Pliki lekcji (md, poza 1.1_Opis kursu.md)
            lesson_files = sorted([
                f for f in mod.iterdir()
                if f.suffix == ".md" and f.name != "1.1_Opis kursu.md"
            ])
            pdf_files = sorted([f for f in mod.iterdir() if f.suffix == ".pdf"])

            if not lesson_files and not pdf_files:
                st.caption("Brak lekcji w tym module.")

            for lf in lesson_files:
                clean_title = lf.stem.replace("_", " ").strip()
                with st.expander(f"   📄 {clean_title}", expanded=False):
                    content = _read_md(lf)
                    st.markdown(content)
                    st.markdown(
                        f"<p style='font-size:.75rem;color:#94a3b8'>📁 {lf.name}</p>",
                        unsafe_allow_html=True
                    )

            for pf in pdf_files:
                st.markdown(
                    f"<div style='padding:6px 0;font-size:.82rem;color:#10b981'>📄 {pf.name}</div>",
                    unsafe_allow_html=True
                )


# ─── MAPA MYŚLI HTML ───────────────────────────────────────────────────────
def _render_mindmap(week_num: int):
    html_path = MINDMAP_DIR / f"mindmap_tydzien{week_num}.html"
    if not html_path.exists():
        st.info(f"Mapa myśli dla Tygodnia {week_num} jeszcze nie istnieje.")
        st.caption(f"Oczekiwana lokalizacja: `{html_path}`")
        return
    html_content = html_path.read_text(encoding="utf-8")
    components.html(html_content, height=820, scrolling=True)


# ─── GŁÓWNA FUNKCJA ────────────────────────────────────────────────────────
def render_knowledge_zone():
    st.markdown(
        "<div class='adhd-header-card' style='padding:20px;border-radius:15px'>"
        "<h1>🧠 Centrum Wiedzy — Google Umiejętności Jutra 3.0</h1>"
        "<p>Mapy Myśli · Notatki z lekcji · Materiały dodatkowe</p>"
        "</div>",
        unsafe_allow_html=True
    )
    st.write("")

    # ── Wykryj dostępne tygodnie dynamicznie ──────────────────────────────
    if not UJ_ROOT.exists():
        st.error(f"❌ Folder bazy wiedzy nie istnieje:\n`{UJ_ROOT}`")
        return

    week_dirs = sorted([
        d for d in UJ_ROOT.iterdir()
        if d.is_dir() and "Tydzień" in d.name
    ])

    if not week_dirs:
        st.warning("Brak tygodni kursów w bazie wiedzy.")
        return

    # ── Zakładki: Tydzień 1 | Tydzień 2 | ... ────────────────────────────
    tab_labels = [f"📅 {d.name}" for d in week_dirs]
    tabs = st.tabs(tab_labels)

    for i, (tab, week_dir) in enumerate(zip(tabs, week_dirs), start=1):
        with tab:
            week_num = i

            # Sub-zakładki: Mapa Myśli | Drzewo Lekcji
            sub_mapa, sub_drzewo = st.tabs(["🗺️ Mapa Myśli", "📚 Drzewo Lekcji"])

            with sub_mapa:
                st.markdown(
                    f"<p style='color:#6b7280;font-size:.85rem;margin-bottom:8px'>"
                    f"Interaktywna mapa modułów i lekcji. Kliknij moduł aby rozwinąć lekcje i przejść do filmów YouTube.</p>",
                    unsafe_allow_html=True
                )
                _render_mindmap(week_num)

                # Przycisk otwarcia w pełnym oknie
                html_path = MINDMAP_DIR / f"mindmap_tydzien{week_num}.html"
                if html_path.exists():
                    with open(html_path, "rb") as f:
                        st.download_button(
                            label="⬇️ Pobierz mapę jako HTML",
                            data=f.read(),
                            file_name=f"mindmap_tydzien{week_num}.html",
                            mime="text/html",
                            key=f"dl_map_{week_num}"
                        )

            with sub_drzewo:
                st.markdown(
                    f"<p style='color:#6b7280;font-size:.85rem;margin-bottom:12px'>"
                    f"Rozwiń moduł → lekcję → aby przeczytać notatki Gemini z danej lekcji.</p>",
                    unsafe_allow_html=True
                )

                # Statystyki tygodnia
                all_md = list(week_dir.rglob("*.md"))
                lesson_md = [f for f in all_md if f.name != "1.1_Opis kursu.md"]
                all_pdf = list(week_dir.rglob("*.pdf"))
                mod_count = len([d for d in week_dir.iterdir() if d.is_dir()])

                c1, c2, c3 = st.columns(3)
                c1.metric("📁 Modułów", mod_count)
                c2.metric("📄 Lekcji (.md)", len(lesson_md))
                c3.metric("📋 PDF", len(all_pdf))
                st.write("")

                _render_week_tree(week_dir)

    # ── Sekcja: inne zasoby bazy wiedzy ───────────────────────────────────
    st.divider()
    with st.expander("📂 Pozostałe zasoby bazy wiedzy", expanded=False):
        if BAZA_ROOT.exists():
            other_dirs = [
                d for d in BAZA_ROOT.iterdir()
                if d.is_dir() and "Umiejętności Jutra" not in d.name
            ]
            if other_dirs:
                for d in sorted(other_dirs):
                    st.markdown(f"**📁 {d.name}**")
                    md_files = list(d.rglob("*.md"))
                    for mf in md_files[:5]:
                        st.caption(f"   · {mf.relative_to(d)}")
                    if len(md_files) > 5:
                        st.caption(f"   ... i {len(md_files)-5} więcej")
            else:
                st.info("Brak innych zasobów.")


# Eksportuj też pills (legacy) ─────────────────────────────────────────────
def render_pills():
    pills_path = BAZA_ROOT.parent / "pills" / "pills.json"
    if not pills_path.exists():
        return
    pills = json.loads(pills_path.read_text(encoding="utf-8"))
    for pill in pills:
        with st.expander(f"💡 {pill.get('title', 'Brak tytułu')}"):
            for b in pill.get("bullets", []):
                st.markdown(f"- {b}")
