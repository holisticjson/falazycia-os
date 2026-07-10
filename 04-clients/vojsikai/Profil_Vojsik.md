# 🎙️ Profil Projektu: Vojsik AI (Voice Assistant MVP)

Karta kontrolna i mapa operacyjna dla inteligentnego asystenta głosowego **Vojsik AI**.

---

## 📂 Spis Ścieżek i Namiarów

*   **Katalog Główny (Stacjonarny & Laptop):**
    `C:\Aplikacje MVP\Vojsik AI`
*   **Katalog MVP:**
    `C:\Aplikacje MVP\Vojsik MVP`
*   **Dedykowany Klucz Service Account GCP:**
    `C:\Aplikacje MVP\Vojsik AI\holistic-operator-ai-6534bc5016f3.json`

---

## 📑 Cel i Opis Projektu

**Vojsik AI** to zaawansowany asystent głosowy (Voice-to-Text / Text-to-Voice) zaprojektowany do bezdotykowej obsługi komputera, notowania myśli, sterowania systemami domowymi oraz asystowania osobom z ADHD.

### Główne Komponenty Technologiczne:
1.  **Aplikacja Desktopowa:** Napisana w Pythonie, skompilowana do pliku wykonywalnego **`Vojsik AI.exe`** za pomocą PyInstaller.
2.  **Silnik Audio:** Integracja z szybkim przetwarzaniem mowy Whisper (m.in. przez lokalne serwery / API NVIDIA) oraz syntezą mowy Google Cloud Text-to-Speech (GCP TTS).
3.  **Baza Wiedzy i Historia:** Lokalne zapisywanie konwersacji w formacie JSON (`history.json`) oraz konfiguracja w `config.json`.

---

## 🚀 Plan Wdrożeniowy (Deploy) i Paczkowanie

Wszystkie operacje paczkowania i instalacji są zautomatyzowane lokalnie:

### A. Budowanie i Paczkowanie Aplikacji (.exe):
W roocie projektu znajduje się skrypt automatycznie kompilujący i pakujący wszystkie zasoby (ikony, biblioteki) do paczki dystrybucyjnej:
```powershell
# Uruchomienie skryptu pakującego:
python package_all.py
```

### B. Instalacja na nowym urządzeniu użytkownika:
Dla ułatwienia instalacji przygotowany jest skrypt wsadowy Windows (Batch), który instaluje wymagane zależności i rejestruje asystenta w systemie:
```powershell
# Uruchom jako Administrator na nowym komputerze:
.\instaluj_vojsik.bat
```

---

## ⚙️ Kluczowe Pliki Konfiguracyjne

*   `config.json` — Konfiguracja portów, API, czułości mikrofonu i parametrów LLM.
*   `vocabulary.txt` — Słownik niestandardowych pojęć i skrótów (sensoryka NLP) poprawiający jakość rozpoznawania mowy.
*   `instrukcja_instalacji.md` — Pełny podręcznik użytkownika końcowego.
