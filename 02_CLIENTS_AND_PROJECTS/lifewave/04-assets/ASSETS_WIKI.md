# 🗂️ WIKI Zasobów (Assets) Klubu Fala Życia

Ten plik służy jako rejestr zasobów graficznych, wideo i dokumentów, aby utrzymać porządek w projekcie i zapobiec duplikacji.

## 📌 Konwencja Nazewnictwa (Tagowanie)
Proszę stosować następujące prefiksy dla nowo dodawanych plików:
* `IMG_` - Dla obrazów statycznych, grafik i logotypów (np. `IMG_portal_hero.jpg`, `IMG_logo_fala_zycia.png`).
* `VIDEO_` - Dla plików wideo i animacji (np. `VIDEO_do_tlumaczenia.mp4`, `VIDEO_instrukcja_x2o.mp4`).
* `DOC_` - Dla dokumentów PDF, Word, skryptów tekstowych (np. `DOC_mlm_skrypt_rozmowy.pdf`, `DOC_badania_kliniczne_x39.pdf`).

## 🗑️ Czyszczenie Śmieci
Zastosowano skrypt czyszczący, który automatycznie ignoruje i usuwa pliki z prefiksem `extracted_*` (powstające często przy błędach rozpakowywania PDF przez agentów RAG). Reguła ta została zapisana w `.gitignore`.

## 📁 Główne Katalogi Zasobów
1. **`knowledge_base/`** - Pliki `.md` z przetworzoną wiedzą dla agentów AI (np. Flight Hacking, X39, X2O, MLM Duplication).
2. **`images/`** - Skondensowane grafiki wykorzystywane bezpośrednio na portalu `fala-zycia.pl` oraz w aplikacji Streamlit (Dashboard).

---
*Aktualizacja: Lipiec 2026*
