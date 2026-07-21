# 🎙️ Profil Produktu: Vojsik Speech-to-Text

Karta kontrolna, ścieżki i dokumentacja dla własnego silnika i aplikacji **Vojsik Speech-to-Text** (funkcjonującego jako darmowy lead magnet).

---

## 📂 Spis Ścieżek i Namiarów

*   **Katalog Główny (Stacjonarny & Laptop):**
    `C:\Aplikacje MVP\Vojsik AI`
*   **Katalog Kodów/Szybkich Testów:**
    `C:\Aplikacje MVP\Vojsik MVP`
*   **Dedykowany Adres Dystrybucji:**
    Darmowa aplikacja webowa **Speech-to-Text** dystrybuowana na **`app.jaison.pl`** jako potężny, darmowy lead magnet.

---

## 📑 Cel i Opis Produktu (Model Biznesowy)

**Vojsik Speech-to-Text** to wyspecjalizowany, autorski system transkrypcji mowy i notowania głosowego, zaprojektowany z myślą o maksymalnym skupieniu (eliminacja szumu kognitywnego dla ADHD).

### 💎 Strategia Produktowa (Free vs PRO):
1.  **Darmowa Aplikacja Webowa STT (Lead Magnet):**
    *   Uruchomiona jako darmowe narzędzie webowe pod adresem **`app.jaison.pl`** (np. `app.jaison.pl/speech-to-text`).
    *   Pozwala użytkownikom na błyskawiczne wgrywanie notatek głosowych lub nagrywanie na żywo w celu otrzymania natychmiastowej, krystalicznie czystej transkrypcji w zamian za zapis na newsletter.
2.  **Wersje Płatne / Aplikacja Desktopowa PRO (Premium SaaS):**
    *   **`Vojsik AI.exe`** — pełna wersja desktopowa zintegrowana z systemem Windows (globalne skróty klawiszowe, sterowanie głosowe komputerem, integracja z Word/Obsidian).
    *   Udostępniana jako produkt płatny (subskrypcyjny lub jednorazowa licencja High-Ticket) dla profesjonalistów i przedsiębiorców.

---

## 🚀 Plan Wdrożeniowy (Deploy & Paczkowanie)

Kompilacja i dystrybucja wersji desktopowej z poziomu katalogu `C:\Aplikacje MVP\Vojsik AI`:

### A. Kompilacja wersji Desktop (.exe):
```powershell
# Uruchomienie skryptu kompilującego PyInstaller ze wszystkimi ikonami i zależnościami:
python package_all.py
```

### B. Wdrożenie wersji Webowej STT (na Cloud Run):
Moduł webowy Speech-to-Text jest wdrożony jako część zunifikowanego panelu Streamlit pod domeną **`app.jaison.pl`** za pomocą naszego oficjalnego skryptu:
```powershell
python deploy_jaison.py
```

---

## ⚙️ Pliki Kluczowe
*   `config.json` — Konfiguracja portów, API i modeli transkrypcji.
*   `vocabulary.txt` — Dedykowany słownik ułatwiający poprawną transkrypcję pojęć biznesowych i NLP.
*   `instaluj_vojsik.bat` — Automatyczny instalator zależności systemowych na Windows.
