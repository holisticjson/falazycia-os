# **Raport Techniczny: Faza 4 – Generator Landing Pages 3D i Integracja z Systeme.io**

Jako Twój główny programista frontend oraz inżynier integracji chmurowych, zaprojektowałem architekturę łączącą potężne możliwości generatywne Hermesa ze środowiskiem Streamlit oraz restrykcjami darmowego planu Systeme.io. 

Aby system był przyjazny dla mózgu z ADHD (Low-Friction), raport jest sformatowany w wysoce skondensowanych blokach z gotowym do użycia kodem.

---

### 1. Moduł Streamlit: Połączenie CMO AI i CTO AI (Generator 3D)

Aby uniknąć "halucynacji" i przeciążenia pamięci agentów, proces w Streamlicie musi działać kaskadowo (Linear Swarm). CMO AI nie dotyka kodu, a CTO AI nie wymyśla tekstów.

**Przepływ pracy (Workflow) w Streamlit:**
1. **Faza Koncepcyjna (CMO AI):** Agent ładuje checklisty copywriterskie (np. formułę AIDA - Uwaga, Zainteresowanie, Pożądanie, Akcja) oraz strukturę z pliku `client_context.json`. Generuje surowe teksty dla sekcji Hero, Social Proof i FAQ. Wynik zapisuje w `st.session_state`.
2. **Faza Kodowania (CTO AI):** Agent pobiera gotowy tekst od CMO i "obleka" go w nowoczesny kod HTML5/CSS z interaktywną sekcją 3D (biblioteka Three.js).
3. **Faza Optymalizacji:** CTO AI konsoliduje cały kod do postaci jednego pliku (inline CSS i wstrzyknięty JS), aby uniknąć problemów z ładowaniem zewnętrznych zasobów w edytorze Systeme.io.

#### Gotowy System Prompt dla CTO AI (Generator Kodu)
```text
Jesteś CTO AI. Twoim zadaniem jest zamiana dostarczonego tekstu marketingowego od CMO AI na wysoce konwertującą sekcję Hero Landing Page'a w jednym pliku HTML.

WYTYCZNE TECHNICZNE:
1. Skonsoliduj całość do jednego pliku (HTML + CSS w <style> + JS w <script> na końcu pliku).
2. Tło sekcji Hero ma zawierać nowoczesną, responsywną animację 3D wykorzystującą bibliotekę Three.js (np. wolno obracająca się, geometryczna siatka cząsteczek zintegrowana z ruchem kursora).
3. Nałóż na animację 3D nakładkę (overlay), na której wyśrodkujesz nagłówek, podtytuł i jaskrawy przycisk CTA.
4. Zadbaj o hierarchię wizualną i kontrast zgodnie z zasadami WCAG. Zwróć wyłącznie surowy kod HTML gotowy do skopiowania.
```

#### Przykładowy Szablon Wygenerowanego Kodu HTML/Three.js
```html
<div id="hero-3d-container" style="position: relative; width: 100%; height: 100vh; overflow: hidden; background-color: #0f172a;">
    <!-- Warstwa 3D -->
    <canvas id="three-canvas" style="position: absolute; top: 0; left: 0; width: 100%; height: 100%; z-index: 1;"></canvas>
    
    <!-- Warstwa Tekstu (CMO Copy) -->
    <div style="position: absolute; top: 50%; left: 50%; transform: translate(-50%, -50%); z-index: 2; text-align: center; color: white; width: 80%;">
        <h1 style="font-size: 3rem; font-family: sans-serif; font-weight: bold; margin-bottom: 20px;">Zautomatyzuj swój biznes AI</h1>
        <p style="font-size: 1.25rem; font-family: sans-serif; margin-bottom: 30px;">Oszczędź 20h tygodniowo dzięki inteligentnym lejkom.</p>
        <button style="background-color: #3b82f6; color: white; padding: 15px 30px; font-size: 1.1rem; border: none; border-radius: 8px; cursor: pointer; font-weight: bold;">Zacznij Teraz</button>
    </div>
</div>

<script src="https://cdnjs.cloudflare.com/ajax/libs/three.js/r128/three.min.js"></script>
<script>
    // Inicjalizacja prostej animacji 3D
    const scene = new THREE.Scene();
    const camera = new THREE.PerspectiveCamera(75, window.innerWidth / window.innerHeight, 0.1, 1000);
    const renderer = new THREE.WebGLRenderer({ canvas: document.getElementById('three-canvas'), alpha: true });
    renderer.setSize(window.innerWidth, window.innerHeight);

    const geometry = new THREE.IcosahedronGeometry(2, 0);
    const material = new THREE.MeshBasicMaterial({ color: 0x3b82f6, wireframe: true });
    const sphere = new THREE.Mesh(geometry, material);
    scene.add(sphere);

    camera.position.z = 5;

    function animate() {
        requestAnimationFrame(animate);
        sphere.rotation.x += 0.005;
        sphere.rotation.y += 0.005;
        renderer.render(scene, camera);
    }
    animate();
</script>
```

---

### 2. Transfer Kodu do Systeme.io (Darmowy Plan)

Darmowy plan Systeme.io **nie udostępnia API do zautomatyzowanego tworzenia czy edytowania stron**. Bezpośrednia integracja backendowa dla kreatora lejków jest tu niemożliwa.

Zamiast walczyć z systemem, stosujemy architekturę hybrydową (Asynchroniczny eksport + schowek), która dla osoby z ADHD musi być banalnie prosta w egzekucji. W aplikacji Streamlit kod jest wyświetlany w komponencie `st.code()` wyposażonym w natywny przycisk kopiowania.

#### SOP: Wdrożenie kodu w 3 prostych krokach (Low-Friction)
1. **Generowanie i Kopiowanie:** W dashboardzie Streamlit, po wygenerowaniu kodu przez CTO AI, kliknij małą ikonę kopiowania (clipboard) w prawym gargu bloku kodu.
2. **Przeciągnięcie Widgetu:** Otwórz kreator swojej strony lądowania w Systeme.io. Z lewego menu elementów przeciągnij widget o nazwie **"Kod HTML"** (Custom HTML) w wybrane miejsce na stronie.
3. **Wklejenie i Publikacja:** Kliknij upuszczony widget, otwórz jego ustawienia po lewej stronie, wybierz opcję edycji kodu i użyj `Ctrl+V` (lub `Cmd+V`), aby wkleić zawartość schowka. Zapisz zmiany. Systeme.io automatycznie wyrenderuje interaktywną sekcję 3D!

---

### 3. Architektura FastAPI (`webhook_api.py`) w GCP

Gdy użytkownik wypełni formularz na Twoim pięknym Landing Page'u 3D, Systeme.io może wysłać ładunek danych (Webhook payload) typu `contact.optin.completed` na zewnętrzny adres.

Zagrożeniem integracyjnym w Systeme.io jest to, że zewnętrzne nadawanie tagów **wymaga unikalnego `Contact ID`, a nie adresu e-mail** (inaczej API zwraca błąd 404). Nasz webhook must odebrać ładunek, zapisać leada, wydobyć jego `contact_id` i natychmiast odesłać żądanie do API.

**Logika biznesowa:** Przypisanie tagu za pomocą wywołania `POST /contacts/{id}/tags` automatycznie aktywuje wewnętrzny "Workflow" w Systeme.io, który natychmiastowo dodaje klienta do kampanii mailingowej.

#### Kod backendu (FastAPI + httpx)
```python
from fastapi import FastAPI, Request, HTTPException
import httpx
import sqlite3 # Przykładowa baza lokalna / Mnemosyne

app = FastAPI()

# Konfiguracja API Systeme.io
SYSTEME_IO_API_KEY = "twój_prywatny_klucz_api"
SYSTEME_IO_BASE_URL = "https://api.systeme.io/api"
TARGET_TAG_ID = "twoj_id_tagu_z_systeme_io"

def save_lead_to_local_crm(email: str, contact_id: str):
    # Prosty zapis do lokalnej bazy (np. SQLite)
    conn = sqlite3.connect("local_crm.db")
    cursor = conn.cursor()
    cursor.execute("CREATE TABLE IF NOT EXISTS leads (id TEXT, email TEXT)")
    cursor.execute("INSERT INTO leads (id, email) VALUES (?, ?)", (contact_id, email))
    conn.commit()
    conn.close()

@app.post("/webhook/systeme-io")
async def receive_systeme_io_optin(request: Request):
    payload = await request.json()
    
    # 1. Sprawdzenie typu zdarzenia (zapis na listę)
    if payload.get("type") == "contact.optin.completed":
        data = payload.get("data", {})
        contact = data.get("contact", {})
        
        # 2. Wyciągnięcie rygorystycznie wymaganych Contact ID oraz e-maila
        contact_id = contact.get("id")
        email = contact.get("email")
        
        if not contact_id:
            raise HTTPException(status_code=400, detail="Brak Contact ID w ładunku")
            
        # 3. Zapis leada lokalnie w CRM (dla raportów CFO AI)
        save_lead_to_local_crm(email, str(contact_id))
        
        # 4. Wywołanie API Systeme.io w celu nadania tagu (wyzwala kampanię mailową)
        headers = {
            "X-API-Key": SYSTEME_IO_API_KEY,
            "Content-Type": "application/json"
        }
        
        # API wymaga Contact ID w URL, a nie adresu e-mail!
        tag_endpoint = f"{SYSTEME_IO_BASE_URL}/contacts/{contact_id}/tags"
        
        async with httpx.AsyncClient() as client:
            response = await client.post(
                tag_endpoint,
                headers=headers,
                json={"tagId": TARGET_TAG_ID} # lub "tag_id", zgodnie z nową specyfikacją
            )
            
            if response.status_code == 200:
                return {"status": "success", "message": f"Tag assigned to {contact_id}"}
            else:
                raise HTTPException(status_code=response.status_code, detail=response.text)

    return {"status": "ignored", "message": "Nieobsługiwany typ zdarzenia"}
```
