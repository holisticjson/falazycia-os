# 📱 Profil Produktu: Komunikator Bezpieczny J(AI)SON

Karta kontrolna, ścieżki i dokumentacja dla własnej aplikacji mobilnej **Komunikator Bezpieczny J(AI)SON** (funkcjonującej jako darmowy lead magnet).

---

## 📂 Spis Ścieżek i Namiarów

*   **Katalog Projektu (Stacjonarny & Laptop):**
    `C:\Aplikacje MVP\Android`
*   **Dedykowany Adres Dystrybucji:**
    Darmowy lead magnet dystrybuowany za pośrednictwem platformy **`app.jaison.pl`** (oraz dedykowanej subdomeny `android.jaison.pl`).
*   **Baza Danych (SQLite):**
    `C:\Aplikacje MVP\Android\hermes.db`

---

## 📑 Cel i Opis Produktu (Model Biznesowy)

**Komunikator Bezpieczny J(AI)SON** to własna, flagowa aplikacja mobilna agencji Jaison, która służy jako **główny lead magnet** do pozyskiwania kontaktów i budowania bazy marketingowej (w duchu ADHD-friendly).

### 💎 Strategia Produktowa (Free vs PRO):
1.  **Wersja Darmowa (Lead Magnet):** 
    *   Udostępniana bezpłatnie na **`app.jaison.pl`** w celu pobrania w zamian za zapis na listę mailingową w Systeme.io.
    *   Oferuje bezpieczną, szyfrowaną lokalnie wymianę wiadomości i asynchroniczne przesyłanie notatek głosowych/tekstowych do uproszczonego bazy wiedzy.
2.  **Wersje Płatne i Warianty PRO (SaaS / Premium):**
    *   W przyszłości na platformie **`app.jaison.pl`** pojawią się płatne subskrypcje i wersje premium (PRO) Komunikatora.
    *   Wersja PRO zaoferuje pełną integrację dwukierunkową z Hermes Agentic OS, dostęp do zaawansowanych agentów (CEO, CMO, CFO) oraz Vertex AI Search.

---

## 🚀 Plan Wdrożeniowy (Deploy / Kompilacja)

Wdrożenie kodu mobilnego i serwerowego z poziomu folderu `C:\Aplikacje MVP\Android`:

### A. Kompilacja i Deploy APK:
```powershell
# Uruchomienie oficjalnego skryptu kompilacji i wysłania na serwer android.jaison.pl:
.\deploy.ps1
```

### B. Automatyzacja Grafik i Ikon:
Służy do szybkiej regeneracji ikon aplikacji przy zmianie identyfikacji wizualnej:
```powershell
# Przetwarzanie ikony głównej:
python process_app_icon.py

# Przetwarzanie i skalowanie dodatkowych zasobów graficznych:
python process_new_assets_v3.py
```
