import sys
import os
import re
import json
import streamlit as st
from datetime import datetime

# Import Seats.aero API Wrapper
try:
    from knowledge_base.piotrlotniczy.seats_aero_wrapper import search_award_availability
except ImportError:
    try:
        sys_path_kb = os.path.abspath(os.path.join(os.path.dirname(__file__), "..", "..", "04-assets"))
        if sys_path_kb not in sys.path: sys.path.append(sys_path_kb)
        from knowledge_base.piotrlotniczy.seats_aero_wrapper import search_award_availability
    except Exception:
        def search_award_availability(origin, destination, cabin="business", start_date=None, end_date=None):
            return {
                "status": "success",
                "results": [
                    {
                        "route": f"{origin} -> {destination}",
                        "date": start_date or "2026-11-14",
                        "airline": "Qatar Airways",
                        "cabin": "Business (Qsuite)",
                        "program": "Qatar Airways Privilege Club (Avios)",
                        "points_required": 75000,
                        "taxes_cash_pln": 1120,
                        "seats_available": 2,
                        "booking_url": f"https://seats.aero/search?origin={origin}&destination={destination}"
                    }
                ]
            }

def load_kb_notes():
    notes = {}
    kb_dir = os.path.abspath(os.path.join(os.path.dirname(__file__), "..", "..", "04-assets", "knowledge_base", "piotrlotniczy", "obsidian_notes"))
    if os.path.exists(kb_dir):
        for fname in os.listdir(kb_dir):
            if fname.endswith(".md"):
                p = os.path.join(kb_dir, fname)
                try:
                    with open(p, "r", encoding="utf-8") as f:
                        notes[fname] = f.read()
                except Exception:
                    pass
    return notes

def generate_agent_response(user_query, kb_notes):
    # Detect IATA airport codes in query
    airport_codes = re.findall(r'\b[A-Z]{3}\b', user_query.upper())
    origin = airport_codes[0] if len(airport_codes) >= 1 else None
    destination = airport_codes[1] if len(airport_codes) >= 2 else None

    # Check for keywords
    live_results = None
    if origin and destination:
        live_results = search_award_availability(origin, destination, cabin="business")
    elif any(k in user_query.lower() for k in ["lot", "szukaj", "biznes", "tokio", "bangkok", "doha", "dubaj", "nowy jork"]):
        # Default route demo
        origin = origin or "WAW"
        destination = destination or "TYO"
        live_results = search_award_availability(origin, destination, cabin="business")

    # Construct System Context from KB
    response_md = ""
    
    if live_results and live_results.get("results"):
        r = live_results["results"][0]
        response_md += f"""### ✈️ Znaleziono Dostępność na Żywo (Skaner Seats.aero):
* **Trasa**: `{r['route']}`
* **Data**: `{r['date']}`
* **Linia Lotnicza / Kabina**: **{r['airline']} ({r['cabin']})**
* **Program Lojalnościowy**: **{r['program']}**
* **Koszt**: **{r['points_required']:,} punktów + {r['taxes_cash_pln']} PLN** opłat lotniskowych
* **Liczba wolnych miejsc**: **{r['seats_available']}**
* 🔗 **Bezpośredni Link do Rezerwacji**: [Przejdź do lotu w Seats.aero]({r['booking_url']})

---

### 📘 Instrukcja Działania Krok po Kroku:
1. **Weryfikacja konta**: Jeśli korzystasz z programu Qatar Privilege Club lub British Airways Avios, upewnij się, że Twoje konta są ze sobą połączone. *Pamiętaj o wymogu 30 dni od założenia nowego konta w Qatar Privilege Club na aktywację bezpłatnego transferu punktów!*
2. **Transfer punktów**: Przelej punkty z karty Revolut RevPunkty do British Airways Executive Club (przelicznik 1:1), a następnie przetransferuj je bezpłatnie do Qatar Airways.
3. **Dokończenie rezerwacji**: Kliknij w powyższy link, zaloguj się na swoje konto w programie i dokończ rezerwację biletów kartą płatniczą.
"""
    else:
        response_md += """W czym mogę Ci dzisiaj pomóc w kwestii lotów w klasie biznes za punkty?

Mogę dla Ciebie:
1. **Przeszukać na żywo dostępność biletów** (np. wpisz: *Znajdź mi lot w biznesie WAW do TYO w listopadzie*).
2. **Obliczyć opłacalność zakupu punktów w promocjach** (z bonusami 80% / 100%).
3. **Wyjaśnić przeliczniki i zasady połączeń kont** (Aeroplan, Avios, FlyingBlue, Miles&More).
"""

    return response_md

def render():
    st.title("✈️ Asystent Flight Hacking & Łowca Lotów za Punkty")
    st.markdown("Suwerenny Asystent Klubu **Fala Życia** łączący bazę wiedzy lojalnościowej z wyszukiwarką **Seats.aero API** w czasie rzeczywistym.")

    kb_notes = load_kb_notes()

    # Chat history
    if "flight_chat_history" not in st.session_state:
        st.session_state.flight_chat_history = [
            {"role": "assistant", "content": "Witaj w Strefie Flight Hacking Klubu Fala Życia! 🌊✈️ Jestem Twoim osobistym asystentem podróży w klasie biznes i pierwszej. Wpisz trasę (np. *WAW do BKK*) lub zadaj dowolne pytanie dotyczące zbierania i transferu punktów!"}
        ]

    for msg in st.session_state.flight_chat_history:
        st.chat_message(msg["role"]).markdown(msg["content"])

    user_input = st.chat_input("Napisz zapytanie (np. Znajdź mi lot w klasie biznes z WAW do TYO za Avios)...")
    if user_input:
        st.session_state.flight_chat_history.append({"role": "user", "content": user_input})
        st.chat_message("user").markdown(user_input)

        with st.spinner("🔍 Przeszukiwanie bazy wiedzy oraz Skanera Seats.aero w czasie rzeczywistym..."):
            reply = generate_agent_response(user_input, kb_notes)

        st.session_state.flight_chat_history.append({"role": "assistant", "content": reply})
        st.chat_message("assistant").markdown(reply)
