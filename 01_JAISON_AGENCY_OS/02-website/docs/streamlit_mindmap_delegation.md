# 🖥️ INSTALACJA I DELEGACJA: Dynamiczna Mapa Systemu w Streamlit

Ten dokument zawiera instrukcję techniczną dla Agenta deweloperskiego obsługującego **Dashboard Streamlit (`app.py`)**, opisującą jak w 4 linijkach kodu wdrożyć dynamiczną, automatycznie rysowaną interaktywną mapę sieciową Twojej agencji i wszystkich klientów!

---

### 🗺️ Jak to działa (Koncepcja "Żywej Mapy")

1.  W roocie projektu znajduje się folder `02_CLIENTS_AND_PROJECTS/`, gdzie lądują wszystkie foldery wdrożeniowe nowych klientów (zakładane automatycznie przez webhook n8n).
2.  Nowo utworzony moduł **`modules.dynamic_mindmap`**:
    - Skanuje ten folder przy każdym odświeżeniu dashboardu.
    - Sprawdza, czy w folderze klienta istnieje plik `.agents/AGENTS.md`. Jeśli tak, odczytuje jego stan (np. jako `live`).
    - Automatycznie generuje nowy obiekt węzła (Node) i strzałkę łączącą (Edge) z centralą (Jaison OS).
    - Wstrzykuje wygenerowane dane dynamicznie do bazowego silnika wizualizacyjnego **`mindmap_visualizer.html`** (Vis-network JS).

---

### 🛠️ KOD DO IMPLEMENTACJI W `app.py` (Dla Agenta Streamlit)

Aby wyświetlić interaktywną mapę jako nową zakładkę lub sekcję w głównym dashboardzie, należy dodać następujący blok kodu do pliku `app.py`:

```python
import streamlit as st
import streamlit.components.v1 as components
from modules.dynamic_mindmap import generate_dynamic_html

def render_system_mindmap():
    st.subheader("🌐 Dynamiczna Interaktywna Mapa Systemu v2.0")
    st.markdown(
        "Poniższa mapa systemu jest generowana **automatycznie w czasie rzeczywistym**. "
        "Skanuje ona strukturę katalogów `02_CLIENTS_AND_PROJECTS/` i wizualizuje połączone zasoby, "
        "agenty oraz aktywnych klientów agencji."
    )
    
    # 1. Wygeneruj dynamiczny kod HTML wstrzykujący aktualnych klientów
    try:
        html_content = generate_dynamic_html()
        
        # 2. Wyrenderuj komponent HTML wewnątrz Streamlita
        components.html(html_content, height=800, scrolling=True)
        
    except Exception as e:
        st.error(f"Nie udało się załadować mapy systemu: {str(e)}")
```

#### Gdzie to wpiąć?
Wystarczy wywołać funkcję `render_system_mindmap()` w miejscu dedykowanej zakładki (np. "Mapa Systemu" lub "Operacje agencji") w menu bocznym lub głównym kontenerze kart `st.tabs()`.

---

### 📈 Zalety tego wdrożenia:
- **Pełna automatyzacja:** Tomasz nie musi ręcznie aktualizować mapy systemu, gdy pozyskuje nowego klienta. Folder klienta pojawia się na mapie sam!
- **Kompatybilność:** Vis-network działa bezpośrednio w piaskownicy (sandbox) iframe Streamlita i reaguje błyskawicznie na dotyk oraz przeciąganie myszką.
- **Brak zależności zewnętrznych:** Kod działa w 100% lokalnie i nie wymaga żadnych płatnych API.
