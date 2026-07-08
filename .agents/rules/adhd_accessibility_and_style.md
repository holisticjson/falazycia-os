# Zasady Dostępności i Stylu UI (ADHD) w Streamlit [Always On]

## Cel i Kontekst
Głównym użytkownikiem *Holistic CEO Dashboard* jest przedsiębiorca z ADHD i astygmatyzmem. Interfejs musi być dla niego bezpieczną przystanią (Sanctuary), a nie źródłem stresu poznawczego. Zbyt wiele bodźców, gęsty tekst i skomplikowane menu powodują zjawisko "Shiny Object Syndrome" (SOS) i paraliż decyzyjny.

## Żelazne Reguły Architektury UI:

1. **Minimalizm i Przestrzeń (White Space)**
   - Ukrywaj zaawansowane opcje za pomocą `st.expander` (np. "Zobacz Mapę Myśli & Plan Działania").
   - Unikaj "ścian tekstu" (Walls of Text). Komunikaty i raporty muszą być formatowane jako krótkie listy punktowane, checklisty i tabele.
   - Używaj kolumn (`st.columns`) do logicznego grupowania elementów na jednym poziomie.

2. **Stan i Tryby Pracy (Context Switching)**
   - Użytkownik przemieszcza się między zdefiniowanymi stanami: **Zen Mode** (metryki), **ADHD Flow** (głęboka praca), **Ingestion Hub** (szybki zrzut myśli), **SOS Sanctuary** (przebodźcowanie).
   - UI musi dostosowywać się do tych trybów. Wszystko, co nie jest w danej chwili potrzebne, znika z ekranu.

3. **Przejrzyste CTA (Call to Action)**
   - Przyciski kluczowych akcji muszą być duże i wyraźnie widoczne, najlepiej oparte na kolorach marki i gradientach (np. `st.button` stylizowane przez CSS).
   - Akcje zapisujące lub finalizujące (np. "Zapisz do Pamięci") powinny od razu dostarczać mechanizmów nagrody (Dopamine Boosts), takich jak `st.toast()`, konfetti (`st.balloons()`) czy aktualizacja punktacji (Dopamine Journal).

4. **Bezpieczeństwo Kognitywne & Floating Czacha**
   - Na wszystkich ekranach pracy zablokowanej musi być dostępny szybki zrzut myśli (tzw. "Braindump"). 
   - Wdrożony widget "Pływająca Czaszka" umożliwia zrzut myśli (dyktowanie głosowe Web Speech API) bez opuszczania bieżącego kontekstu.

5. **Wydajność i Asynchroniczność (Nie blokuj UI)**
   - Wykorzystuj `st.cache_data` oraz `st.cache_resource` do cachowania kosztownych obliczeń, ładowania słowników (np. `vocabulary.json`) i pobierania danych analitycznych.
   - Zapytania do API (LLM, n8n, GHL) powinny wykorzystywać wskaźnik postępu (`st.spinner`), aby użytkownik wiedział, że system "myśli".
   - Unikaj blokowania aplikacji – używaj asynchronicznego ładowania komponentów gdzie to tylko możliwe.

6. **Motyw Kolorystyczny i Kontrast (Astygmatyzm)**
   - Wspieraj dynamiczny przełącznik Dark Mode / Light Mode, dostosowując natywnie paletę Streamlit i wstrzyknięty CSS.
   - Unikaj jaskrawych, neonowych barw na dużych powierzchniach. Stosuj miękkie, zharmonizowane gradienty i ciemne, nieprzytłaczające tła (`rgba(11, 31, 51, 0.96)`). Wszelkie kluczowe teksty muszą mieć wysoki kontrast i łagodne czcionki (Outfit / Inter).

*Zasady te obowiązują każdego agenta pracującego przy kodzie Streamlit w tym projekcie.*
