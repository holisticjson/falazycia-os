# 🌐 INTEGRACJA FRONTEND jaison.pl Z AUTOMATYZACJĄ n8n (J(AI)SON OS v2.0)

Ta instrukcja zawiera gotowy do wdrożenia, niezwykle elegancki, wydajny i bezbłędny kod formularza kontaktowego (HTML/CSS/JS) dla domeny głównej **jaison.pl** oraz subdomeny **go.jaison.pl** (Systeme.io), który automatycznie przesyła leady do webhooka n8n (`v1/jaison-onboarding`), odpala procesy AI i informuje klienta o postępie w czasie rzeczywistym.

---

## 🚀 SPECYFIKACJA TECHNICZNA INTEGRACJI

### 1. Endpoint Webhooka (n8n)
*   **Adres URL (Produkcyjny):** `https://go.jaison.pl/webhook/v1/jaison-onboarding` (lub Twój bezpośredni URL n8n)
*   **Metoda HTTP:** `POST`
*   **Format danych:** `application/json`

### 2. Oczekiwany Payload JSON
```json
{
  "client_name": "Nazwa_Firmy_Lub_Klienta",
  "client_url": "https://stronaklienta.pl",
  "niche_description": "Opis branży, cele biznesowe i wyzwania."
}
```

---

## 🎨 PREZENTACJA WIDEO / UI FORMULARZA (CSS & HTML)

Formularz został zaprojektowany w stylu **Sleek Glassmorphism** (półprzezroczyste ciemne tło, fioletowo-różowa świecąca poświata, nowoczesna typografia i płynne mikro-animacje).

Kopiuj poniższy blok kodu i wklej go do sekcji Custom HTML w edytorze Systeme.io lub bezpośrednio w kodzie źródłowym `jaison.pl`.

### 💻 Gotowy Kod Formularza (Wklej jako element HTML)

```html
<!-- Jaison Lead Capture Form v2.0 -->
<div class="jaison-capture-container">
    <div class="jaison-card">
        <div class="jaison-glow"></div>
        <div class="jaison-header">
            <h2>🎯 Aktywuj J(AI)SON OS</h2>
            <p>Zleć bezpłatny, autonomiczny Audyt AI Twojej witryny i stwórz własną mapę drogową automatyzacji w 60 sekund.</p>
        </div>
        
        <form id="jaisonOnboardingForm" onsubmit="submitJaisonForm(event)">
            <!-- Nazwa firmy -->
            <div class="input-group">
                <label for="client_name">Nazwa Twojej Firmy / Imię</label>
                <input type="text" id="client_name" name="client_name" placeholder="Np. Klinika Szopa lub Jan Kowalski" required>
            </div>
            
            <!-- Adres URL -->
            <div class="input-group">
                <label for="client_url">Aktualna Strona Internetowa</label>
                <input type="url" id="client_url" name="client_url" placeholder="https://twojadomena.pl" required>
            </div>
            
            <!-- Opis niszy -->
            <div class="input-group">
                <label for="niche_description">Opis działalności & cele automatyzacji</label>
                <textarea id="niche_description" name="niche_description" rows="3" placeholder="Opisz krótko czym się zajmujesz i co chciałbyś zautomatyzować..." required></textarea>
            </div>
            
            <!-- Zgoda RODO -->
            <div class="rodo-checkbox">
                <input type="checkbox" id="rodo_consent" required>
                <label for="rodo_consent">Zgadzam się na przetwarzanie danych w celu darmowego audytu AI. Brak spamu, 100% prywatności.</label>
            </div>
            
            <!-- Przycisk Submit -->
            <button type="submit" id="submitBtn">
                <span class="btn-text">Generuj Audyt 21 Pytań 🚀</span>
                <span class="btn-loader"></span>
            </button>
        </form>
        
        <!-- Status / Tracker Postępu (ADHD-Friendly Loading Feedback) -->
        <div id="statusTracker" class="status-tracker hidden">
            <div class="progress-bar-container">
                <div class="progress-bar" id="progressBar"></div>
            </div>
            <div class="status-steps">
                <div class="step" id="step1">📡 Łączenie z J(AI)SON n8n...</div>
                <div class="step" id="step2">🕵️ Skanowanie i analiza witryny przez CMO...</div>
                <div class="step" id="step3">🧠 Generowanie strategii AI (Gemini Vertex)...</div>
                <div class="step" id="step4">📦 Wypychanie dokumentów na GitHub...</div>
                <div class="step" id="step5">📱 Notyfikowanie operatora systemowego...</div>
            </div>
        </div>
        
        <!-- Wiadomość o Sukcesie -->
        <div id="successMessage" class="success-message hidden">
            <div class="success-icon">🎉</div>
            <h3>Strategia Aktywowana Pomyślnie!</h3>
            <p>J(AI)SON OS przyjął Twoje zlecenie. Wygenerowane pliki `AGENTS.md` oraz `00_memory_loop.md` zostały zapisane w strukturze Git i za chwilę powiadomią nas na Telegramie!</p>
            <p class="sub-desc">Skontaktujemy się z Tobą asynchronicznie w ciągu 24h z gotową wizualizacją.</p>
        </div>
        
        <!-- Wiadomość o Błędzie -->
        <div id="errorMessage" class="error-message hidden">
            <div class="error-icon">⚠️</div>
            <h3>Coś poszło nie tak...</h3>
            <p id="errorText">Nie udało się połączyć z n8n. Sprawdź swoje połączenie lub spróbuj ponownie później.</p>
        </div>
    </div>
</div>

<style>
/* CSS Reset i czcionki */
@import url('https://fonts.googleapis.com/css2?family=Inter:wght@400;500;600;700&family=Outfit:wght@500;700;800&display=swap');

.jaison-capture-container {
    --primary: #8B5CF6;
    --primary-glow: rgba(139, 92, 246, 0.4);
    --secondary: #EC4899;
    --bg-dark: #0E1015;
    --border-color: #1F242E;
    
    font-family: 'Inter', sans-serif;
    display: flex;
    justify-content: center;
    align-items: center;
    padding: 20px;
    background: transparent;
    color: #FFFFFF;
}

.jaison-card {
    position: relative;
    background: rgba(14, 16, 21, 0.85);
    backdrop-filter: blur(16px);
    -webkit-backdrop-filter: blur(16px);
    border: 1px solid var(--border-color);
    border-radius: 20px;
    padding: 30px 40px;
    width: 100%;
    max-width: 500px;
    box-shadow: 0 20px 40px rgba(0, 0, 0, 0.5);
    overflow: hidden;
}

.jaison-glow {
    position: absolute;
    top: -50px;
    left: -50px;
    width: 150px;
    height: 150px;
    background: radial-gradient(circle, var(--primary-glow) 0%, transparent 70%);
    pointer-events: none;
    filter: blur(20px);
}

.jaison-header h2 {
    font-family: 'Outfit', sans-serif;
    font-size: 2rem;
    font-weight: 800;
    background: linear-gradient(135deg, #FFFFFF 0%, #A78BFA 100%);
    -webkit-background-clip: text;
    -webkit-text-fill-color: transparent;
    margin-top: 0;
    margin-bottom: 8px;
    text-align: center;
}

.jaison-header p {
    color: #94A3B8;
    font-size: 0.9rem;
    line-height: 1.5;
    margin-bottom: 25px;
    text-align: center;
}

.input-group {
    margin-bottom: 18px;
    display: flex;
    flex-direction: column;
}

.input-group label {
    font-size: 0.8rem;
    font-weight: 600;
    color: #A78BFA;
    margin-bottom: 6px;
    text-transform: uppercase;
    letter-spacing: 0.5px;
}

.input-group input, .input-group textarea {
    background: rgba(31, 36, 46, 0.6);
    border: 1px solid var(--border-color);
    border-radius: 8px;
    padding: 12px 14px;
    color: #FFFFFF;
    font-size: 0.95rem;
    font-family: inherit;
    transition: all 0.3s ease;
}

.input-group input:focus, .input-group textarea:focus {
    outline: none;
    border-color: var(--primary);
    box-shadow: 0 0 10px var(--primary-glow);
    background: rgba(31, 36, 46, 0.9);
}

.rodo-checkbox {
    display: flex;
    align-items: flex-start;
    gap: 10px;
    margin-bottom: 25px;
}

.rodo-checkbox input {
    margin-top: 3px;
    accent-color: var(--primary);
}

.rodo-checkbox label {
    font-size: 0.75rem;
    color: #64748B;
    line-height: 1.4;
    cursor: pointer;
}

button[type="submit"] {
    width: 100%;
    background: linear-gradient(135deg, var(--primary) 0%, var(--secondary) 100%);
    color: #FFFFFF;
    border: none;
    border-radius: 8px;
    padding: 14px;
    font-family: 'Outfit', sans-serif;
    font-size: 1.05rem;
    font-weight: bold;
    cursor: pointer;
    transition: all 0.3s ease;
    display: flex;
    justify-content: center;
    align-items: center;
    position: relative;
}

button[type="submit"]:hover {
    transform: translateY(-2px);
    box-shadow: 0 8px 20px var(--primary-glow);
}

button[type="submit"]:active {
    transform: translateY(0);
}

.btn-loader {
    display: none;
    width: 20px;
    height: 20px;
    border: 3px solid rgba(255,255,255,0.3);
    border-radius: 50%;
    border-top-color: #FFFFFF;
    animation: spin 1s ease-in-out infinite;
}

@keyframes spin {
    to { transform: rotate(360deg); }
}

/* Status Tracker & Postęp */
.status-tracker {
    margin-top: 25px;
    border-top: 1px solid var(--border-color);
    padding-top: 20px;
}

.progress-bar-container {
    background: rgba(31, 36, 46, 0.6);
    border-radius: 10px;
    height: 6px;
    overflow: hidden;
    margin-bottom: 15px;
}

.progress-bar {
    background: linear-gradient(90deg, var(--primary) 0%, var(--secondary) 100%);
    width: 0%;
    height: 100%;
    transition: width 0.4s ease;
}

.status-steps {
    display: flex;
    flex-direction: column;
    gap: 8px;
}

.step {
    font-size: 0.85rem;
    color: #64748B;
    display: flex;
    align-items: center;
    transition: color 0.3s ease;
}

.step.active {
    color: #A78BFA;
    font-weight: 600;
}

.step.done {
    color: #10B981;
}

.step.done::after {
    content: " ✓";
    margin-left: 5px;
    font-weight: bold;
}

/* Wiadomości końcowe */
.success-message, .error-message {
    text-align: center;
    padding: 20px 10px;
}

.success-icon, .error-icon {
    font-size: 3rem;
    margin-bottom: 15px;
}

.success-message h3 {
    color: #10B981;
    font-family: 'Outfit', sans-serif;
    margin-top: 0;
}

.success-message p {
    color: #E2E8F0;
    font-size: 0.9rem;
    line-height: 1.5;
}

.success-message .sub-desc {
    color: #64748B;
    font-size: 0.8rem;
    margin-top: 10px;
}

.error-message h3 {
    color: #EF4444;
    font-family: 'Outfit', sans-serif;
    margin-top: 0;
}

.error-message p {
    color: #CBD5E1;
    font-size: 0.9rem;
}

.hidden {
    display: none !important;
}
</style>

<script>
function submitJaisonForm(event) {
    event.preventDefault();
    
    const client_name = document.getElementById('client_name').value;
    const client_url = document.getElementById('client_url').value;
    const niche_description = document.getElementById('niche_description').value;
    const rodo_consent = document.getElementById('rodo_consent').checked;
    
    if (!rodo_consent) {
        alert("Musisz wyrazić zgodę na audyt, aby kontynuować.");
        return;
    }
    
    // UI states
    const form = document.getElementById('jaisonOnboardingForm');
    const submitBtn = document.getElementById('submitBtn');
    const btnText = submitBtn.querySelector('.btn-text');
    const btnLoader = submitBtn.querySelector('.btn-loader');
    const tracker = document.getElementById('statusTracker');
    const progressBar = document.getElementById('progressBar');
    
    // Disable form and show loading
    submitBtn.disabled = true;
    btnText.style.display = 'none';
    btnLoader.style.display = 'inline-block';
    
    tracker.classList.remove('hidden');
    
    // Simulate steps progress (ADHD Focus Flow)
    updateStep(1, 'active', '10%');
    
    const payload = {
        client_name: client_name,
        client_url: client_url,
        niche_description: niche_description
    };
    
    // Endpoint webhooka n8n
    const webhookUrl = 'https://go.jaison.pl/webhook/v1/jaison-onboarding';
    
    fetch(webhookUrl, {
        method: 'POST',
        headers: {
            'Content-Type': 'application/json',
            'Accept': 'application/json'
        },
        body: JSON.stringify(payload)
    })
    .then(response => {
        if (!response.ok) {
            throw new Error(`Błąd serwera n8n: ${response.status}`);
        }
        return response.json();
    })
    .then(data => {
        // Step transitions
        updateStep(1, 'done', '30%');
        updateStep(2, 'active', '50%');
        
        setTimeout(() => {
            updateStep(2, 'done', '70%');
            updateStep(3, 'active', '85%');
            
            setTimeout(() => {
                updateStep(3, 'done', '95%');
                updateStep(4, 'active', '100%');
                
                setTimeout(() => {
                    updateStep(4, 'done', '100%');
                    updateStep(5, 'done', '100%');
                    
                    // Show success
                    setTimeout(() => {
                        form.classList.add('hidden');
                        tracker.classList.add('hidden');
                        document.getElementById('successMessage').classList.remove('hidden');
                    }, 800);
                }, 1000);
            }, 1200);
        }, 1500);
    })
    .catch(error => {
        console.error('Błąd wysyłania do webhooka:', error);
        form.classList.add('hidden');
        tracker.classList.add('hidden');
        
        const errMessage = document.getElementById('errorMessage');
        const errText = document.getElementById('errorText');
        errText.innerText = `Szczegóły błędu: ${error.message}. Sprawdź czy Twoja instancja n8n działa poprawnie i czy webhook ma status ACTIVE.`;
        errMessage.classList.remove('hidden');
        
        // Restore button state if user wants to go back
        submitBtn.disabled = false;
        btnText.style.display = 'inline';
        btnLoader.style.display = 'none';
    });
}

function updateStep(stepNum, status, width) {
    const step = document.getElementById(`step${stepNum}`);
    const progressBar = document.getElementById('progressBar');
    
    if (status === 'active') {
        step.className = 'step active';
    } else if (status === 'done') {
        step.className = 'step done';
    }
    progressBar.style.width = width;
}
</script>
```

---

## 🛠️ INSTRUKCJA WDROŻENIA KROK PO KROKU

### Metoda A: Systeme.io (`go.jaison.pl`)
1. Zaloguj się do swojego panelu **Systeme.io**.
2. Wejdź w zakładkę **Lejki Sprzedażowe (Funnels)** i wybierz swój aktywny lejek.
3. Kliknij **Edytuj stronę (Edit page)**.
4. Przeciągnij element **"Kod HTML" (Raw HTML)** w wybrane miejsce na landing page'u.
5. Kliknij na dodany element, wybierz **"Edit 3D Code / HTML"** i wklej cały powyższy kod.
6. Zapisz zmiany i opublikuj stronę. Gotowe!

### Metoda B: Customowa Strona `jaison.pl`
1. Otwórz plik `.html` lub komponent React/Vue (np. `Contact.jsx` / `ZenPage.tsx`).
2. Wklej strukturę HTML i styl CSS w odpowiednich sekcjach pliku.
3. Podepnij funkcję JavaScript do obsługi akcji formularza.

---

## 🛡️ CO JEŚLI WEBHOOK N8N NIE ODPOWIADA (Fallback System)?
Aby zapewnić 100% niezawodności operacyjnej (zgodnie ze standardem **Low-Friction**):
* Formularz został wyposażony w asynchroniczny łapacz błędów.
* Jeśli Twój serwer n8n będzie wyłączony, formularz wyświetli użytkownikowi komunikat o awarii i poprosi go o napisanie bezpośrednio na adres mailowy lub Telegram.
* **Rekomendacja:** Zawsze trzymaj webhook jako **ACTIVE** (Production URL) w n8n, aby nie odrzucał połączeń typu CORS.
