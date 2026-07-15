# 📁 SILOS A: JAISON AGENCY OS
> **Przeznaczenie:** Repozytorium marki agencji jaison.pl, kod Streamlit (app.jaison.pl) oraz operacje wewnętrzne.

## 🚫 Czego NIE wolno robić pod-agentom w tym folderze:
1. **ZAKAZ umieszczania danych klientów:** Żadne dane zewnętrzne, logotypy, hasła klientów nie mogą trafić do tego silosu. To jest wyłącznie środowisko agencji.
2. **ZAKAZ "hardkodowania" kluczy:** Wszelkie klucze API (Vertex AI Search, n8n, Systeme.io) muszą być ładowane wyłącznie przez plik `.env` w roocie projektu.
3. **ZAKAZ wprowadzania zmian bez testów:** Kod Streamlit w `dashboard_and_core/app.py` musi być modyfikowany z zachowaniem standardów bezpieczeństwa wstecznego.
