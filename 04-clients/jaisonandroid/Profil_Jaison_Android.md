# 🤖 Profil Projektu: Jaison Android (Hermes Mobile OS)

Karta kontrolna i mapa operacyjna dla mobilnego asystenta AI **Jaison Android** (obsługującego domenę **`android.jaison.pl`**).

---

## 📂 Spis Ścieżek i Namiarów

*   **Katalog Projektu (Stacjonarny & Laptop):**
    `C:\Aplikacje MVP\Android`
*   **Dedykowana Domena / Subdomena:**
    `android.jaison.pl` (lub pomocniczo `android.json.pl`)
*   **Lokalna Baza Danych:**
    `C:\Aplikacje MVP\Android\hermes.db` (SQLite)

---

## 📑 Cel i Opis Projektu

Aplikacja mobilna stanowiąca integralną część ekosystemu **Hermes Agentic OS**. Służy Tomaszowi jako kieszonkowy asystent AI i interfejs do sterowania procesami agencyjnymi bezpośrednio z telefonu z systemem Android.

### Architektura Kodu:
*   `client/` — Kod źródłowy aplikacji mobilnej (Android Native / Flutter / WebView Wrapper).
*   `server/` — Lokalny serwer pośredniczący (Backend API w Pythonie).
*   `web/` — Panel administratora i mobilny interfejs webowy.

---

## 🚀 Plan Wdrożeniowy (Deploy)

Wdrożenie aplikacji i synchronizacja jej zasobów graficznych:

### A. Kompilacja i Deploy Aplikacji Mobilnej:
W folderze znajduje się dedykowany skrypt PowerShell do automatycznej kompilacji pliku `.apk`, podpisywania go certyfikatem deweloperskim i wysyłania na serwer dystrybucyjny pod domenę `android.jaison.pl`:
```powershell
# Uruchomienie skryptu wdrożeniowego (z poziomu folderu C:\Aplikacje MVP\Android):
.\deploy.ps1
```

### B. Przetwarzanie Nowych Zasobów Graficznych (Ikony, Logotypy):
Aby ułatwić rebranding i podmieniać ikony aplikacji na nowe, przygotowano dedykowane skrypty automatycznie skalujące grafiki do standardów Androida (mipmap-xxxhdpi etc.):
```powershell
# Szybkie generowanie ikon aplikacji ze źródłowego pliku PNG:
python process_app_icon.py

# Skalowanie pozostałych zasobów graficznych:
python process_new_assets_v3.py
```

---

## 📝 Powiązane Dokumenty i Briefy
*   `android_agent_jaison_rebrand_brief.md` — Dokumentacja założeń rebrandingu wizualnego na standardy Jaison AI (ADHD-friendly, psychologiczne kotwice NLP).
