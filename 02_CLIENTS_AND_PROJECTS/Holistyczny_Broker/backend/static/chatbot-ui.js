/**
 * Holistyczny Broker - AI Concierge & Vertex AI Search Widget Integration
 * Estetyka: Quiet Luxury (Onyx Black, Emerald Green, Signature Gold)
 * Standard: Dual-Mode (Real Vertex RAG Widget / Intelligent Luxury Mockup) + WhatsApp Handoff
 */

// --- KONFIGURACJA VERTEX AI SEARCH ---
// Gdy wyklikasz aplikację w Google Cloud Console na koncie brokerholistic@gmail.com,
// uzupełnij poniższe dwie wartości. Widget Google zostanie automatycznie zainicjowany.
const VERTEX_AI_WIDGET_ID = ""; // np. "12345-abcde"
const VERTEX_AI_CONFIG_ID = ""; // np. "67890-fghij"
const WHATSAPP_CONTACT_LINK = "https://wa.me/48730882961";

document.addEventListener('DOMContentLoaded', () => {
    // Sprawdzamy czy Vertex AI Search jest skonfigurowany
    const isVertexConfigured = VERTEX_AI_WIDGET_ID && VERTEX_AI_CONFIG_ID;

    // Tworzenie głównego kontenera widgetu
    const widget = document.createElement('div');
    widget.id = 'hb-chat-widget';
    
    if (isVertexConfigured) {
        // --- TRYB REALNY: INICJALIZACJA WIDGETU GOOGLE VERTEX AI SEARCH ---
        // Ładowanie oficjalnego skryptu bootstrap z Google Cloud
        const script = document.createElement('script');
        script.src = `https://cloud.google.com/ai/search/widget/v1b/bootstrap.js?id=${VERTEX_AI_WIDGET_ID}`;
        script.async = true;
        document.head.appendChild(script);

        // Wstrzykiwanie widgetu bezpośrednio w strukturę strony
        widget.innerHTML = `
            <div id="hb-chat-window" class="vertex-mode">
                <div id="hb-chat-header">
                    <div class="hb-header-title">
                        <span class="hb-status-dot"></span>
                        <h3>AI Concierge</h3>
                        <span class="hb-badge">Vertex AI</span>
                    </div>
                    <div class="hb-header-actions">
                        <a href="${WHATSAPP_CONTACT_LINK}" target="_blank" class="hb-wa-handoff-btn" title="Połącz z Partnerem (WhatsApp)">
                            <svg width="18" height="18" fill="currentColor" viewBox="0 0 24 24"><path d="M.057 24l1.687-6.163c-1.041-1.804-1.588-3.849-1.587-5.946C.06 5.348 5.397.01 12.008.01c3.202.001 6.212 1.246 8.477 3.514 2.266 2.268 3.507 5.28 3.505 8.484-.004 6.657-5.34 11.997-11.953 11.997-2.005-.001-3.973-.502-5.739-1.45L0 24zm6.59-4.846c1.6.95 3.188 1.449 4.825 1.451 5.436 0 9.86-4.37 9.864-9.799.002-2.63-1.023-5.101-2.885-6.965C16.528 1.977 14.07 .951 11.453.951 6.019.951 1.593 5.323 1.589 10.751c-.001 1.724.463 3.41 1.345 4.9l-.315 1.15-.314 1.144 1.233-.317 1.11-.285c1.468.802 3.09 1.22 4.749 1.22zM17.5 14.316c-.302-.15-1.785-.882-2.062-.982-.277-.1-.478-.15-.68.15-.202.3-.782.982-.96 1.183-.176.2-.352.226-.654.076-.301-.15-1.274-.47-2.426-1.498-.897-.8-1.502-1.79-1.678-2.09-.176-.3-.019-.462.132-.612.135-.135.302-.35.453-.526.15-.175.202-.3.302-.5.1-.2.05-.376-.025-.526-.075-.15-.68-1.633-.932-2.24-.246-.594-.495-.513-.68-.523-.176-.01-.377-.01-.578-.01-.202 0-.528.075-.805.376-.277.301-1.057 1.028-1.057 2.508 0 1.48 1.082 2.909 1.232 3.11.15.2 2.13 3.25 5.16 4.561.72.311 1.28.497 1.719.637.724.23 1.38.197 1.9.115.58-.093 1.784-.73 2.035-1.432.25-.703.25-1.305.176-1.43-.075-.127-.277-.202-.58-.352z"/></svg>
                        </a>
                        <button id="hb-chat-close">
                            <svg width="20" height="20" fill="none" stroke="currentColor" viewBox="0 0 24 24"><path stroke-linecap="round" stroke-linejoin="round" stroke-width="2" d="M6 18L18 6M6 6l12 12"></path></svg>
                        </button>
                    </div>
                </div>
                <div id="hb-vertex-container">
                    <gcs-search-widget
                      data-config-id="${VERTEX_AI_CONFIG_ID}"
                      data-placeholder="Zapytaj asystenta o działki i ROI..."
                      data-max-results="5">
                    </gcs-search-widget>
                </div>
            </div>
            <div id="hb-chat-fab">
                <svg fill="none" stroke="currentColor" viewBox="0 0 24 24"><path stroke-linecap="round" stroke-linejoin="round" stroke-width="2" d="M8 10h.01M12 10h.01M16 10h.01M9 16H5a2 2 0 01-2-2V6a2 2 0 012-2h14a2 2 0 012 2v8a2 2 0 01-2 2h-5l-5 5v-5z"></path></svg>
            </div>
        `;
    } else {
        // --- TRYB PREZENTACYJNY: INTELIGENTNA MAKIETA MOCKUP ---
        widget.innerHTML = `
            <div id="hb-chat-window" class="mock-mode">
                <div id="hb-chat-header">
                    <div class="hb-header-title">
                        <span class="hb-status-dot pulse"></span>
                        <h3>AI Concierge</h3>
                        <span class="hb-badge">OFF-MARKET DEMO</span>
                    </div>
                    <button id="hb-chat-close">
                        <svg width="20" height="20" fill="none" stroke="currentColor" viewBox="0 0 24 24"><path stroke-linecap="round" stroke-linejoin="round" stroke-width="2" d="M6 18L18 6M6 6l12 12"></path></svg>
                    </button>
                </div>
                <div id="hb-chat-messages">
                    <div class="hb-msg bot">
                        Dzień dobry. Jestem wirtualnym asystentem <strong>Holistycznego Brokera</strong>. 
                        <br><br>
                        Specjalizuję się w dyskretnym wyszukiwaniu gruntów, analizie planistycznej MPZP oraz kojarzeniu inwestorów w segmencie <strong>Quiet Luxury</strong>. 
                        <br><br>
                        W czym mogę dzisiaj Państwu pomóc?
                    </div>
                </div>
                
                <div id="hb-chat-quick-actions">
                    <button class="hb-quick-btn" data-query="Jakie macie grunty off-market?">📂 Oferty Off-Market</button>
                    <button class="hb-quick-btn" data-query="Jakie ROI oferują Wasze projekty?">📈 Rentowność (ROI)</button>
                    <button class="hb-quick-btn" data-query="Jak działa Wasz skaner nieruchomości?">🔍 Skaner Deal Sourcing</button>
                </div>

                <div id="hb-chat-input-area">
                    <input type="text" id="hb-chat-input" placeholder="Wpisz zapytanie (np. MPZP, ROI, Grunty)..." autocomplete="off">
                    <button id="hb-chat-send">
                        <svg width="24" height="24" fill="none" stroke="currentColor" viewBox="0 0 24 24"><path stroke-linecap="round" stroke-linejoin="round" stroke-width="2" d="M12 19l9 2-9-18-9 18 9-2zm0 0v-8"></path></svg>
                    </button>
                </div>
                
                <div id="hb-chat-footer">
                    <span>Obsługiwane przez Vertex AI Search RAG</span>
                </div>
            </div>
            <div id="hb-chat-fab" class="pulse-glow">
                <svg fill="none" stroke="currentColor" viewBox="0 0 24 24"><path stroke-linecap="round" stroke-linejoin="round" stroke-width="2" d="M8 10h.01M12 10h.01M16 10h.01M9 16H5a2 2 0 01-2-2V6a2 2 0 012-2h14a2 2 0 012 2v8a2 2 0 01-2 2h-5l-5 5v-5z"></path></svg>
            </div>
        `;
    }

    document.body.appendChild(widget);

    // Selektory elementów sterujących UI
    const fab = document.getElementById('hb-chat-fab');
    const win = document.getElementById('hb-chat-window');
    const closeBtn = document.getElementById('hb-chat-close');
    
    let isOpen = false;

    // Funkcja otwierania i zamykania okna czatu
    function toggleChat() {
        isOpen = !isOpen;
        if (isOpen) {
            win.style.display = 'flex';
            setTimeout(() => win.classList.add('open'), 10);
            if (!isVertexConfigured) {
                document.getElementById('hb-chat-input').focus();
            }
        } else {
            win.classList.remove('open');
            setTimeout(() => win.style.display = 'none', 300);
        }
    }

    fab.addEventListener('click', toggleChat);
    closeBtn.addEventListener('click', toggleChat);

    // Jeśli jesteśmy w trybie symulacji, wdrażamy inteligentną pętlę odpowiedzi
    if (!isVertexConfigured) {
        const input = document.getElementById('hb-chat-input');
        const sendBtn = document.getElementById('hb-chat-send');
        const msgs = document.getElementById('hb-chat-messages');
        const quickBtns = document.querySelectorAll('.hb-quick-btn');

        // Baza inteligentnych odpowiedzi Quiet Luxury
        const mockResponses = [
            {
                keywords: ["grunt", "działka", "działki", "ziemia", "grunty", "teren", "tereny"],
                reply: `W portfolio <strong>Holistycznego Brokera</strong> posiadamy starannie wyselekcjonowane grunty off-market (Łódź, Warszawa, pasy logistyczne) o wysokim potencjale PUM/PUM. 
                <br><br>
                Z uwagi na rygorystyczne standardy poufności, precyzyjne lokalizacje oraz parametry chłonności udostępniamy <strong>wyłącznie zweryfikowanym inwestorom po podpisaniu umowy NDA</strong>.
                <br><br>
                <div class="hb-msg-action">
                    <a href="${WHATSAPP_CONTACT_LINK}" target="_blank" class="hb-msg-action-btn wa-btn">
                        💬 Połącz z WhatsApp Concierge (Pomiń NDA)
                    </a>
                </div>`
            },
            {
                keywords: ["roi", "irr", "yield", "rentowność", "stopa", "zysk", "koszt"],
                reply: `Nasze aktywa inwestycyjne są poddawane rygorystycznemu filtrowaniu finansowemu:
                <br>
                • <strong>Nieruchomości komercyjne:</strong> Yield (rentowność) na poziomie <strong>7.5% - 8.8% NOI</strong> rocznie.
                <br>
                • <strong>Grunty deweloperskie:</strong> Projekty celują w stopę <strong>IRR przekraczającą 20%</strong>.
                <br><br>
                Udostępniamy dynamiczne modele finansowe DCF (Discounted Cash Flow) w Google Sheets. Czy chciałbyś, by nasz doradca omówił z Tobą te wskaźniki?`
            },
            {
                keywords: ["skaner", "realestate", "rwdz", "gunb", "geoportal", "uldk", "baza", "technologia"],
                reply: `Wykorzystujemy autorski silnik <strong>AI Due Diligence (Deal Sourcing Core)</strong>, który co godzinę przeszukuje rządowy rejestr pozwoleń budowlanych (<strong>GUNB RWDZ</strong>) oraz łączy je z danymi katastralnymi <strong>ULDK Geoportalu</strong>.
                <br><br>
                Dzięki temu natychmiast wychwytujemy okazje zanim trafią na rynek i odrzucamy działki z wadami prawnymi. 
                <br><br>
                Możemy przeprowadzić dla Ciebie darmowe skanowanie wskazanej działki. Podaj jej numer, bądź kliknij poniżej, aby połączyć się bezpośrednio.`
            },
            {
                keywords: ["kontakt", "telefon", "rozmowa", "spotkanie", "wa", "whatsapp", "strateg"],
                reply: `Najszybszym sposobem na poufną dyskusję o wolnym kapilale lub przejrzenie memorandum informacyjnego jest bezpośrednie połączenie z naszym Partnerem Zarządzającym na WhatsApp:
                <br><br>
                <div class="hb-msg-action">
                    <a href="${WHATSAPP_CONTACT_LINK}" target="_blank" class="hb-msg-action-btn wa-btn">
                        📱 Otwórz WhatsApp (+48 730 882 961)
                    </a>
                </div>`
            },
            {
                keywords: ["prowizja", "prowizje", "success", "wynagrodzenie", "opłata"],
                reply: `Działamy w 100% w oparciu o model <strong>Success Fee (prowizja od sukcesu)</strong>. Płacą Państwo wyłącznie za sfinalizowaną, bezpieczną i w pełni zwalidowaną prawnie transakcję. Zero ukrytych kosztów na start.`
            }
        ];

        async function handleUserMessage(text) {
            if (!text.trim()) return;

            // Dodanie wiadomości użytkownika
            const userMsg = document.createElement('div');
            userMsg.className = 'hb-msg user';
            userMsg.innerText = text;
            msgs.appendChild(userMsg);
            input.value = '';
            msgs.scrollTop = msgs.scrollHeight;

            // Ukrycie szybkich akcji po pierwszej interakcji
            document.getElementById('hb-chat-quick-actions').style.opacity = '0.3';

            // Efekt "pisania" bot-a
            const typingMsg = document.createElement('div');
            typingMsg.className = 'hb-msg bot hb-typing';
            typingMsg.innerHTML = '<span class="hb-typing-dots"><span>.</span><span>.</span><span>.</span></span> Analizuję rejestr RAG...';
            msgs.appendChild(typingMsg);
            msgs.scrollTop = msgs.scrollHeight;

            // Symulacja opóźnienia sieciowego (premium feel)
            setTimeout(() => {
                msgs.removeChild(typingMsg);

                const lowerText = text.toLowerCase();
                let matchedResponse = null;

                // Szukanie dopasowania po słowach kluczowych
                for (const response of mockResponses) {
                    if (response.keywords.some(kw => lowerText.includes(lowerText.includes(kw) ? kw : ""))) {
                        // Dodatkowy warunek na dokładniejsze dopasowanie słów kluczowych
                        const hasKeyword = response.keywords.some(kw => {
                            const regex = new RegExp(`\\b${kw}\\b`, 'i');
                            return regex.test(lowerText);
                        });
                        if (hasKeyword) {
                            matchedResponse = response.reply;
                            break;
                        }
                    }
                }

                // Fallback na wypadek braku słów kluczowych
                if (!matchedResponse) {
                    matchedResponse = `Dziękuję za wiadomość. Państwa zapytanie dotyczy wrażliwych informacji handlowych. 
                    <br><br>
                    Jako <strong>AI Concierge</strong> dbam o całkowite bezpieczeństwo operacyjne (Zero-Data-Leakage). Aby zachować pełną dyskrecję i precyzję, rekomenduję poufne przekazanie sprawy do naszego Starszego Architekta Transakcji:
                    <br><br>
                    <div class="hb-msg-action">
                        <a href="${VERTEX_AI_WIDGET_ID ? '#' : WHATSAPP_CONTACT_LINK}" target="_blank" class="hb-msg-action-btn wa-btn">
                            💬 Połącz bezpośrednio (WhatsApp)
                        </a>
                    </div>`;
                }

                const botMsg = document.createElement('div');
                botMsg.className = 'hb-msg bot';
                botMsg.innerHTML = matchedResponse;
                msgs.appendChild(botMsg);
                msgs.scrollTop = msgs.scrollHeight;
            }, 1000);
        }

        // Obsługa kliknięć w szybkie akcje
        quickBtns.forEach(btn => {
            btn.addEventListener('click', () => {
                const query = btn.getAttribute('data-query');
                handleUserMessage(query);
            });
        });

        sendBtn.addEventListener('click', () => handleUserMessage(input.value));
        input.addEventListener('keypress', (e) => {
            if (e.key === 'Enter') handleUserMessage(input.value);
        });
    }
});
