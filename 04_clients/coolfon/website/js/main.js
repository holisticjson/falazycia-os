/* ==========================================================================
   COOLFON.PL — JAVASCRIPT CONTROL SYSTEM
   ========================================================================== */

document.addEventListener("DOMContentLoaded", () => {
    initNavigation();
    initCookieBanner();
    initRepairCalculator();
    init3DTilt();
    initMouseGlow();
    initScrollReveal();
    initParticlesCanvas();
    initChatbot();
    initStatsCounters();
});

/* --- Navigation / Mobile Menu & Sticky Header --- */
function initNavigation() {
    const header = document.querySelector(".header");
    const menuBtn = document.querySelector(".menu-btn");
    const nav = document.querySelector(".nav");
    const navLinks = document.querySelectorAll(".nav-link");

    // Sticky Header Scroll effect
    window.addEventListener("scroll", () => {
        if (window.scrollY > 50) {
            header.classList.add("header-scrolled");
        } else {
            header.classList.remove("header-scrolled");
        }
    });

    // Mobile menu toggle
    if (menuBtn && nav) {
        menuBtn.addEventListener("click", () => {
            nav.classList.toggle("active");
            // Zmiana ikony hamburgera na X (używamy symboli tekstowych)
            if (nav.classList.contains("active")) {
                menuBtn.innerHTML = "✕";
            } else {
                menuBtn.innerHTML = "☰";
            }
        });
    }

    // Close menu when link is clicked
    navLinks.forEach(link => {
        link.addEventListener("click", () => {
            if (nav) nav.classList.remove("active");
            if (menuBtn) menuBtn.innerHTML = "☰";
        });
    });
}

/* --- Cookie Consent Banner (localStorage) --- */
function initCookieBanner() {
    const banner = document.getElementById("cookie-banner");
    const acceptBtn = document.getElementById("cookie-accept");
    const rejectBtn = document.getElementById("cookie-reject");

    if (!banner) return;

    // Sprawdź czy użytkownik dokonał wyboru w tej sesji/przeglądarce
    const consent = localStorage.getItem("coolfon_cookie_consent");

    if (!consent) {
        // Pokaż banner z opóźnieniem
        setTimeout(() => {
            banner.classList.add("show");
        }, 1000);
    }

    if (acceptBtn) {
        acceptBtn.addEventListener("click", () => {
            localStorage.setItem("coolfon_cookie_consent", "accepted");
            banner.classList.remove("show");
            // Tutaj można odpalić np. Google Analytics
            enableAnalytics();
        });
    }

    if (rejectBtn) {
        rejectBtn.addEventListener("click", () => {
            localStorage.setItem("coolfon_cookie_consent", "rejected");
            banner.classList.remove("show");
        });
    }
}

function enableAnalytics() {
    console.log("Analytics enabled based on user consent.");
    // Inicjalizacja skryptów śledzących po akceptacji marketingowych ciasteczek
}

const calculatorData = {
    brands: {
        apple: {
            name: "Apple (iPhone)",
            models: {
                "iphone-15-pro-max": {
                    name: "iPhone 15 Pro Max",
                    prices: { screen: 990, battery: 320, usb: 290 }
                },
                "iphone-15-pro": {
                    name: "iPhone 15 Pro",
                    prices: { screen: 890, battery: 290, usb: 280 }
                },
                "iphone-15": {
                    name: "iPhone 15",
                    prices: { screen: 720, battery: 290, usb: 280 }
                },
                "iphone-14-pro-max": {
                    name: "iPhone 14 Pro Max",
                    prices: { screen: 990, battery: 240, usb: 240 }
                },
                "iphone-14-pro": {
                    name: "iPhone 14 Pro",
                    prices: { screen: 890, battery: 240, usb: 240 }
                },
                "iphone-14": {
                    name: "iPhone 14",
                    prices: { screen: 590, battery: 240, usb: 240 },
                    popular: true
                },
                "iphone-13-pro-max": {
                    name: "iPhone 13 Pro Max",
                    prices: { screen: 850, battery: 210, usb: 190 }
                },
                "iphone-13": {
                    name: "iPhone 13",
                    prices: { screen: 480, battery: 210, usb: 190 }
                },
                "iphone-12": {
                    name: "iPhone 12",
                    prices: { screen: 390, battery: 180, usb: 170 }
                },
                "iphone-11": {
                    name: "iPhone 11",
                    prices: { screen: 290, battery: 160, usb: 150 }
                }
            }
        },
        samsung: {
            name: "Samsung",
            models: {
                "galaxy-s24-ultra": {
                    name: "Galaxy S24 Ultra",
                    prices: { screen: 990, battery: 240, usb: 220 }
                },
                "galaxy-s24": {
                    name: "Galaxy S24",
                    prices: { screen: 790, battery: 220, usb: 200 }
                },
                "galaxy-s23-ultra": {
                    name: "Galaxy S23 Ultra",
                    prices: { screen: 890, battery: 210, usb: 190 }
                },
                "galaxy-s23": {
                    name: "Galaxy S23",
                    prices: { screen: 590, battery: 190, usb: 180 },
                    popular: true
                },
                "galaxy-s22-ultra": {
                    name: "Galaxy S22 Ultra",
                    prices: { screen: 790, battery: 190, usb: 180 }
                },
                "galaxy-s22": {
                    name: "Galaxy S22",
                    prices: { screen: 490, battery: 180, usb: 170 }
                },
                "galaxy-s21": {
                    name: "Galaxy S21",
                    prices: { screen: 440, battery: 170, usb: 160 }
                },
                "galaxy-a54": {
                    name: "Galaxy A54",
                    prices: { screen: 320, battery: 150, usb: 130 }
                },
                "galaxy-a35": {
                    name: "Galaxy A35",
                    prices: { screen: 290, battery: 140, usb: 120 }
                }
            }
        },
        xiaomi: {
            name: "Xiaomi / POCO",
            models: {
                "xiaomi-13": {
                    name: "Xiaomi 13",
                    prices: { screen: 380, battery: 170, usb: 140 }
                },
                "redmi-note-13": {
                    name: "Redmi Note 13",
                    prices: { screen: 260, battery: 130, usb: 110 }
                },
                "redmi-note-12": {
                    name: "Redmi Note 12",
                    prices: { screen: 240, battery: 120, usb: 100 },
                    popular: true
                },
                "poco-x6": {
                    name: "POCO X6",
                    prices: { screen: 290, battery: 140, usb: 110 }
                },
                "poco-x5": {
                    name: "POCO X5",
                    prices: { screen: 250, battery: 130, usb: 100 }
                }
            }
        }
    },
    issues: {
        screen: "Rozbity ekran / szybka",
        battery: "Słaba bateria (wymiana)",
        usb: "Uszkodzone gniazdo USB / ładowania",
        other: "Inna usterka (wymaga diagnozy)"
    }
};

function initRepairCalculator() {
    const brandSelect = document.getElementById("calc-brand");
    const modelSelect = document.getElementById("calc-model");
    const issueSelect = document.getElementById("calc-issue");
    const priceDisplay = document.getElementById("calc-price-value");
    const calcForm = document.getElementById("coolfon-calc-form");
    const calcSuccess = document.getElementById("calc-success-msg");

    if (!brandSelect || !modelSelect || !issueSelect) return;

    // 1. Wypełnij marki
    brandSelect.innerHTML = '<option value="">-- Wybierz markę --</option>';
    for (const [key, brand] of Object.entries(calculatorData.brands)) {
        brandSelect.innerHTML += `<option value="${key}">${brand.name}</option>`;
    }

    // 2. Obsługa wyboru marki -> załaduj modele
    brandSelect.addEventListener("change", (e) => {
        const brandKey = e.target.value;
        modelSelect.innerHTML = '<option value="">-- Wybierz model --</option>';
        modelSelect.disabled = !brandKey;
        issueSelect.disabled = true;
        
        if (brandKey && calculatorData.brands[brandKey]) {
            const models = calculatorData.brands[brandKey].models;
            for (const [mKey, model] of Object.entries(models)) {
                modelSelect.innerHTML += `<option value="${mKey}">${model.name}</option>`;
            }
            modelSelect.disabled = false;
        }
        updatePrice();
    });

    // 3. Obsługa wyboru modelu -> włącz usterki
    modelSelect.addEventListener("change", (e) => {
        const modelKey = e.target.value;
        issueSelect.disabled = !modelKey;
        updatePrice();
    });

    // 4. Obsługa wyboru usterki
    issueSelect.addEventListener("change", () => {
        updatePrice();
    });

    // Funkcja obliczająca i aktualizująca cenę
    function updatePrice() {
        const brandKey = brandSelect.value;
        const modelKey = modelSelect.value;
        const issueKey = issueSelect.value;

        if (!brandKey || !modelKey || !issueKey || !priceDisplay) {
            if (priceDisplay) priceDisplay.innerHTML = "0";
            return;
        }

        if (issueKey === "other") {
            priceDisplay.innerHTML = "Wycena indywidualna (diagnoza 0 zł)";
            return;
        }

        try {
            const price = calculatorData.brands[brandKey].models[modelKey].prices[issueKey];
            priceDisplay.innerHTML = `ok. ${price} zł`;
        } catch (err) {
            priceDisplay.innerHTML = "Błąd kalkulacji";
        }
    }

    // 5. Submit formularza -> wysyłka wyceny
    if (calcForm) {
        calcForm.addEventListener("submit", (e) => {
            e.preventDefault();
            
            const submitBtn = calcForm.querySelector("button[type='submit']");
            const phone = document.getElementById("calc-phone").value;
            const brand = brandSelect.options[brandSelect.selectedIndex].text;
            const model = modelSelect.options[modelSelect.selectedIndex].text;
            const issue = issueSelect.options[issueSelect.selectedIndex].text;
            const price = priceDisplay.textContent;

            if (submitBtn) {
                submitBtn.disabled = true;
                submitBtn.innerHTML = "Wysyłanie...";
            }

            // Integracja przez webhook n8n lub fallback PHP do wysyłki e-mail
            // Zbudujemy webhook n8n dedykowany dla Coolfon
            const webhookUrl = "https://n8n.holisticjson.pl/webhook/coolfon-wycena";

            const payload = {
                phone: phone,
                brand: brand,
                model: model,
                issue: issue,
                estimated_price: price,
                target_email: "info@coolfon.pl"
            };

            fetch(webhookUrl, {
                method: "POST",
                headers: { "Content-Type": "application/json" },
                body: JSON.stringify(payload)
            })
            .then(res => {
                calcForm.style.display = "none";
                if (calcSuccess) calcSuccess.style.display = "block";
            })
            .catch(err => {
                console.error("n8n Webhook error, trying PHP fallback...", err);
                // PHP Fallback
                fetch("/php/send_wycena.php", {
                    method: "POST",
                    headers: { "Content-Type": "application/json" },
                    body: JSON.stringify(payload)
                })
                .then(() => {
                    calcForm.style.display = "none";
                    if (calcSuccess) calcSuccess.style.display = "block";
                })
                .catch(phpErr => {
                    alert("Wystąpił błąd podczas wysyłania wyceny. Zadzoń do nas bezpośrednio: +48 532 840 877");
                    if (submitBtn) {
                        submitBtn.disabled = false;
                        submitBtn.innerHTML = "Spróbuj ponownie 🚀";
                    }
                });
            });
        });
    }
}

/* ==========================================================================
   INTERACTIVE 3D & "WOW" THEMATIC EFFECTS
   ========================================================================== */

// 3D Tilt Effect on cards and elements with interactive Specular Reflection (Sheen)
function init3DTilt() {
    const cards = document.querySelectorAll(".tilt-3d");
    cards.forEach(card => {
        card.addEventListener("mousemove", e => {
            const rect = card.getBoundingClientRect();
            const x = e.clientX - rect.left;
            const y = e.clientY - rect.top;
            
            const centerX = rect.width / 2;
            const centerY = rect.height / 2;
            
            // Maximum tilt angle of 8 degrees for smooth elegant response
            const rotateX = ((centerY - y) / centerY) * 8;
            const rotateY = ((x - centerX) / centerX) * -8; // Negative for correct physical follow
            
            card.style.transform = `perspective(1000px) rotateX(${rotateX}deg) rotateY(${rotateY}deg) scale3d(1.015, 1.015, 1.015)`;
            
            // Dynamic percentages for 3D Sheen specular reflection
            const percentX = (x / rect.width) * 100;
            const percentY = (y / rect.height) * 100;
            card.style.setProperty("--sheen-x", `${percentX}%`);
            card.style.setProperty("--sheen-y", `${percentY}%`);
        });
        
        card.addEventListener("mouseleave", () => {
            card.style.transform = "perspective(1000px) rotateX(0deg) rotateY(0deg) scale3d(1, 1, 1)";
            card.style.setProperty("--sheen-x", "50%");
            card.style.setProperty("--sheen-y", "50%");
        });
    });
}

// Mouse-Follow radial backlight glow grid
function initMouseGlow() {
    const glowContainers = document.querySelectorAll(".glow-container");
    glowContainers.forEach(container => {
        container.addEventListener("mousemove", e => {
            const rect = container.getBoundingClientRect();
            const x = e.clientX - rect.left;
            const y = e.clientY - rect.top;
            
            container.style.setProperty("--mouse-x", `${x}px`);
            container.style.setProperty("--mouse-y", `${y}px`);
        });
    });
}

// 3D Scroll Reveal on scroll
function initScrollReveal() {
    const observer = new IntersectionObserver((entries) => {
        entries.forEach(entry => {
            if (entry.isIntersecting) {
                entry.target.classList.add("revealed");
                observer.unobserve(entry.target);
            }
        });
    }, {
        threshold: 0.1,
        rootMargin: "0px 0px -40px 0px"
    });

    const revealElements = document.querySelectorAll(".reveal-3d");
    revealElements.forEach(el => observer.observe(el));
}

// Lightweight Interactive AI Particles Background Matrix
function initParticlesCanvas() {
    const canvas = document.getElementById("particles-canvas");
    if (!canvas) return;

    const ctx = canvas.getContext("2d");
    let particlesArray = [];
    const numberOfParticles = 40; // Low count for maximum performance (PageSpeed optimized)

    function resize() {
        const parent = canvas.parentElement;
        if (!parent) return;
        canvas.width = parent.clientWidth;
        canvas.height = parent.clientHeight;
    }
    resize();
    window.addEventListener("resize", resize);

    const mouse = {
        x: null,
        y: null,
        radius: 130
    };

    const parent = canvas.parentElement;
    parent.addEventListener("mousemove", (e) => {
        const rect = parent.getBoundingClientRect();
        mouse.x = e.clientX - rect.left;
        mouse.y = e.clientY - rect.top;
    });

    parent.addEventListener("mouseleave", () => {
        mouse.x = null;
        mouse.y = null;
    });

    class Particle {
        constructor() {
            this.x = Math.random() * canvas.width;
            this.y = Math.random() * canvas.height;
            this.size = Math.random() * 1.5 + 1;
            this.speedX = Math.random() * 0.3 - 0.15;
            this.speedY = Math.random() * 0.3 - 0.15;
        }

        update() {
            this.x += this.speedX;
            this.y += this.speedY;

            if (this.x < 0 || this.x > canvas.width) this.speedX = -this.speedX;
            if (this.y < 0 || this.y > canvas.height) this.speedY = -this.speedY;

            // Mouse interactive repulsion force
            if (mouse.x !== null && mouse.y !== null) {
                const dx = this.x - mouse.x;
                const dy = this.y - mouse.y;
                const dist = Math.sqrt(dx * dx + dy * dy);
                if (dist < mouse.radius) {
                    const force = (mouse.radius - dist) / mouse.radius;
                    const directionX = (dx / dist) * force * 1.8;
                    const directionY = (dy / dist) * force * 1.8;
                    this.x += directionX;
                    this.y += directionY;
                }
            }
        }

        draw() {
            ctx.fillStyle = "rgba(0, 155, 172, 0.4)";
            ctx.beginPath();
            ctx.arc(this.x, this.y, this.size, 0, Math.PI * 2);
            ctx.closePath();
            ctx.fill();
        }
    }

    function init() {
        particlesArray = [];
        for (let i = 0; i < numberOfParticles; i++) {
            particlesArray.push(new Particle());
        }
    }

    function animate() {
        ctx.clearRect(0, 0, canvas.width, canvas.height);
        
        for (let i = 0; i < particlesArray.length; i++) {
            particlesArray[i].update();
            particlesArray[i].draw();
        }
        connect();
        requestAnimationFrame(animate);
    }

    function connect() {
        for (let a = 0; a < particlesArray.length; a++) {
            for (let b = a + 1; b < particlesArray.length; b++) {
                const dx = particlesArray[a].x - particlesArray[b].x;
                const dy = particlesArray[a].y - particlesArray[b].y;
                const dist = Math.sqrt(dx * dx + dy * dy);

                if (dist < 100) {
                    const opacity = (1 - dist / 100) * 0.15;
                    ctx.strokeStyle = `rgba(0, 155, 172, ${opacity})`;
                    ctx.lineWidth = 0.8;
                    ctx.beginPath();
                    ctx.moveTo(particlesArray[a].x, particlesArray[a].y);
                    ctx.lineTo(particlesArray[b].x, particlesArray[b].y);
                    ctx.stroke();
                }
            }
        }
    }

    init();
    animate();
}

/* ==========================================================================
   PREMIUM GLASSMORPHISM CHATBOT ENGINE (100% FREE & CLIENT-SIDE)
   ========================================================================== */
function initChatbot() {
    // 1. Dynamic Injection of Chatbot HTML structure
    const chatbotHTML = `
        <button class="chatbot-toggle" id="chat-toggle" aria-label="Otwórz czat">
            <svg viewBox="0 0 24 24">
                <path d="M20 2H4c-1.1 0-2 .9-2 2v18l4-4h14c1.1 0 2-.9 2-2V4c0-1.1-.9-2-2-2zm0 14H6l-3 3V4h17v12z"/>
            </svg>
        </button>
        <div class="chatbot-widget" id="chat-widget">
            <div class="chatbot-header">
                <div class="chatbot-header-info">
                    <div class="chatbot-avatar">🤖</div>
                    <div>
                        <div class="chatbot-title">Asystent Coolfon</div>
                        <div class="chatbot-status">Online</div>
                    </div>
                </div>
                <button class="chatbot-close" id="chat-close" aria-label="Zamknij czat">✕</button>
            </div>
            <div class="chatbot-messages" id="chat-messages"></div>
            <div class="chat-suggestions" id="chat-suggestions"></div>
            <div class="chatbot-input-area">
                <input type="text" class="chatbot-input" id="chat-input" placeholder="Zadaj pytanie..." autocomplete="off">
                <button class="chatbot-send" id="chat-send" aria-label="Wyślij wiadomość">
                    <svg viewBox="0 0 24 24">
                        <path d="M2.01 21L23 12 2.01 3 2 10l15 2-15 2z"/>
                    </svg>
                </button>
            </div>
        </div>
    `;
    
    const container = document.createElement("div");
    container.id = "coolfon-chatbot-container";
    container.innerHTML = chatbotHTML;
    document.body.appendChild(container);
    
    const chatToggle = document.getElementById("chat-toggle");
    const chatWidget = document.getElementById("chat-widget");
    const chatClose = document.getElementById("chat-close");
    const chatMessages = document.getElementById("chat-messages");
    const chatSuggestions = document.getElementById("chat-suggestions");
    const chatInput = document.getElementById("chat-input");
    const chatSend = document.getElementById("chat-send");
    
    if (!chatToggle || !chatWidget || !chatClose || !chatMessages || !chatSuggestions || !chatInput || !chatSend) return;
    
    // Toggle widget active state
    chatToggle.addEventListener("click", () => {
        chatWidget.classList.toggle("active");
        if (chatWidget.classList.contains("active")) {
            chatInput.focus();
            if (chatMessages.children.length === 0) {
                showWelcomeMessage();
            }
        }
    });
    
    chatClose.addEventListener("click", () => {
        chatWidget.classList.remove("active");
    });
    
    // Close on click outside (mobile friendly)
    document.addEventListener("click", (e) => {
        if (!chatWidget.contains(e.target) && !chatToggle.contains(e.target) && chatWidget.classList.contains("active")) {
            chatWidget.classList.remove("active");
        }
    });
    
    // Keypress enter on input
    chatInput.addEventListener("keypress", (e) => {
        if (e.key === "Enter") {
            handleSendMessage();
        }
    });
    
    chatSend.addEventListener("click", handleSendMessage);
    
    // Welcome sequence
    function showWelcomeMessage() {
        appendBotMessage("Cześć! Jestem inteligentnym asystentem Coolfon GSM. 📱 Chętnie odpowiem na Twoje pytania o nasz serwis, cennik, lokalizację czy folie hydrożelowe na wymiar. O co chciałbyś zapytać?");
        showSuggestions([
            { text: "💰 Cennik i diagnoza", handler: () => triggerIntent("prices") },
            { text: "📍 Gdzie jesteście?", handler: () => triggerIntent("location") },
            { text: "✂️ Folia na wymiar", handler: () => triggerIntent("foil") },
            { text: "💬 Kontakt / WhatsApp", handler: () => triggerIntent("contact") }
        ]);
    }
    
    function appendBotMessage(text) {
        const bubble = document.createElement("div");
        bubble.className = "chat-bubble chat-bubble-bot";
        bubble.innerHTML = text;
        chatMessages.appendChild(bubble);
        scrollToBottom();
    }
    
    function appendUserMessage(text) {
        const bubble = document.createElement("div");
        bubble.className = "chat-bubble chat-bubble-user";
        bubble.textContent = text;
        chatMessages.appendChild(bubble);
        scrollToBottom();
    }
    
    function showSuggestions(options) {
        chatSuggestions.innerHTML = "";
        options.forEach(opt => {
            const btn = document.createElement("button");
            btn.className = "chat-suggest-btn";
            btn.textContent = opt.text;
            btn.addEventListener("click", () => {
                appendUserMessage(opt.text);
                setTimeout(opt.handler, 300);
            });
            chatSuggestions.appendChild(btn);
        });
    }
    
    function scrollToBottom() {
        chatMessages.scrollTop = chatMessages.scrollHeight;
    }
    
    function handleSendMessage() {
        const text = chatInput.value.trim();
        if (!text) return;
        
        appendUserMessage(text);
        chatInput.value = "";
        
        showTypingIndicator();
        
        setTimeout(() => {
            removeTypingIndicator();
            processUserText(text);
        }, 700);
    }
    
    let typingIndicator = null;
    
    function showTypingIndicator() {
        typingIndicator = document.createElement("div");
        typingIndicator.className = "chat-bubble chat-bubble-bot";
        typingIndicator.style.display = "flex";
        typingIndicator.style.alignItems = "center";
        typingIndicator.style.gap = "4px";
        typingIndicator.innerHTML = '<span style="opacity: 0.6; font-style: italic; font-size: 0.85rem;">Asystent pisze...</span>';
        chatMessages.appendChild(typingIndicator);
        scrollToBottom();
    }
    
    function removeTypingIndicator() {
        if (typingIndicator && typingIndicator.parentElement) {
            typingIndicator.remove();
        }
    }
    
    // Intent processing logic
    function triggerIntent(intent) {
        showTypingIndicator();
        setTimeout(() => {
            removeTypingIndicator();
            respondToIntent(intent);
        }, 500);
    }
    
    function processUserText(text) {
        const normalized = text.toLowerCase().normalize("NFD").replace(/[\u0300-\u036f]/g, ""); // remove Polish diacritics
        
        if (normalized.match(/(cena|cennik|koszt|ile|plat|plac|diagnoz|wycena)/)) {
            respondToIntent("prices");
        } else if (normalized.match(/(gdzie|adres|lokalizacj|dojazd|dojechac|opolczyk|lodz|olechow|dzielnic)/)) {
            respondToIntent("location");
        } else if (normalized.match(/(godzin|kiedy|otwart|zamkniet|sobota|poniedzialek|piatek)/)) {
            respondToIntent("hours");
        } else if (normalized.match(/(foli|hydrozel|zabezpiecz|ploter|wymiar|ekran|szyb|hybryd)/)) {
            respondToIntent("foil");
        } else if (normalized.match(/(kontakt|telefon|whatsapp|rozmow|czlowiek|serwisant|rezerwacj|umow)/)) {
            respondToIntent("contact");
        } else {
            respondToIntent("default");
        }
    }
    
    function respondToIntent(intent) {
        let reply = "";
        let chips = [];
        
        switch(intent) {
            case "prices":
                reply = "Ceny naszych usług zależą od marki, modelu oraz stopnia uszkodzenia urządzenia. **Oferujemy w 100% darmową diagnozę techniczną 0 zł**, na podstawie której przygotujemy dla Ciebie indywidualną wycenę przed naprawą (jeśli zrezygnujesz, nie płacisz nic!).<br><br>Orientacyjne ceny najpopularniejszych modeli możesz sprawdzić w naszym [Kalkulatorze Wyceny](#kalkulator) na stronie głównej lub w dziale [Cennik](/cennik/). Czy chcesz omówić swój problem bezpośrednio z serwisantem?";
                chips = [
                    { text: "💬 Czat na WhatsApp", handler: () => triggerIntent("contact") },
                    { text: "📍 Adres i godziny", handler: () => triggerIntent("location") },
                    { text: "✂️ Folia ochronna", handler: () => triggerIntent("foil") }
                ];
                break;
            case "location":
                reply = "Nasz serwis stacjonarny znajduje się w Łodzi (dzielnica Olechów):<br><br>📍 **ul. Księcia Władysława Opolczyka 17 lok. C6** (92-417 Łódź)<br><br>🚗 Przed samym lokalem czeka na Ciebie **wygodny, darmowy parking**! Możesz też zerknąć na interaktywną mapę na dole naszej strony.";
                chips = [
                    { text: "🕒 Godziny otwarcia", handler: () => triggerIntent("hours") },
                    { text: "💰 Cennik / Diagnoza", handler: () => triggerIntent("prices") },
                    { text: "💬 Napisz na WhatsApp", handler: () => triggerIntent("contact") }
                ];
                break;
            case "hours":
                reply = "Zapraszamy stacjonarnie bez wcześniejszych zapisów! Jesteśmy otwarci w godzinach:<br><br>• **Poniedziałek – Piątek:** 10:00 – 19:00<br>• **Sobota:** 09:00 – 15:00<br>• **Niedziela:** Zamknięte.<br><br>Większość napraw i diagnoz staramy się realizować sprawnie na miejscu, dopasowując czas naprawy do dostępności części po indywidualnej ocenie technicznej.";
                chips = [
                    { text: "📍 Gdzie jesteście?", handler: () => triggerIntent("location") },
                    { text: "💰 Wstępna wycena", handler: () => triggerIntent("prices") },
                    { text: "💬 Napisz na WhatsApp", handler: () => triggerIntent("contact") }
                ];
                break;
            case "foil":
                reply = "✂️ *Precyzyjne zabezpieczanie ekranów na wymiar!*<br><br>W naszym salonie docinamy profesjonalnym ploterem najwyższej klasy **folie hydrożelowe i hybrydowe** dopasowane idealnie pod Twoje urządzenie:<br>• Smartfony i zegarki (smartwatche)<br>• Tablety i czytniki e-booków<br>• Ekrany nawigacji i kokpity w samochodach (GPS)<br><br>Montaż wykonujemy na miejscu! Folia chroni przed pęknięciami, rysami i amortyzuje uderzenia.";
                chips = [
                    { text: "💬 Zapytaj o cenę folii", handler: () => triggerIntent("contact") },
                    { text: "💰 Koszt naprawy tel.", handler: () => triggerIntent("prices") },
                    { text: "📍 Lokalizacja serwisu", handler: () => triggerIntent("location") }
                ];
                break;
            case "contact":
                reply = "Jasne! Przekierowuję Cię do bezpośredniego kontaktu z naszym serwisem. Kliknij poniższy przycisk, aby rozpocząć czat na WhatsApp, lub zadzwoń pod numer **+48 532 840 877**.<br><br><a href='https://wa.me/48532840877?text=Hej!%20Pisze%20ze%20strony%20coolfon.pl%20w%20sprawie%20naprawy%20mojego%20urzadzenia...' target='_blank' class='btn btn-primary' style='display:inline-flex; align-items:center; justify-content:center; gap:8px; margin-top:12px; width:100%; text-decoration:none; background:#25D366; border-color:#25D366; color:#FFF; box-shadow:0 4px 15px rgba(37, 211, 102, 0.4); font-weight:600;'>Rozpocznij czat na WhatsApp 💬</a>";
                chips = [
                    { text: "🕒 Godziny pracy", handler: () => triggerIntent("hours") },
                    { text: "📍 Gdzie jesteście?", handler: () => triggerIntent("location") },
                    { text: "💰 Darmowa diagnoza", handler: () => triggerIntent("prices") }
                ];
                break;
            default:
                reply = "Dziękuję za wiadomość! Jestem automatycznym asystentem i odpowiadam na najczęstsze pytania stacjonarne. Jeśli chcesz poznać dokładną wycenę dla rzadkiego modelu lub porozmawiać o niestandardowej usterce, połączę Cię bezpośrednio z naszym serwisem na WhatsApp! 💬";
                chips = [
                    { text: "💬 Połącz z WhatsApp", handler: () => triggerIntent("contact") },
                    { text: "💰 Cennik i diagnoza", handler: () => triggerIntent("prices") },
                    { text: "📍 Adres i dojazd", handler: () => triggerIntent("location") }
                ];
                break;
        }
        
        appendBotMessage(reply);
        showSuggestions(chips);
    }
}

// Dynamic Social Proof Counter Animation (Intersection Observer)
function initStatsCounters() {
    const counters = document.querySelectorAll('.counter');
    const speed = 100; // Szybkość animacji (im mniej, tym szybciej)

    const animate = (counter) => {
        const target = +counter.getAttribute('data-target');
        const decimals = +counter.getAttribute('data-decimals') || 0;
        let count = 0;
        const step = target / speed;

        const updateCount = () => {
            count += step;
            if (count < target) {
                counter.innerText = (decimals > 0) ? count.toFixed(decimals) : Math.floor(count);
                setTimeout(updateCount, 12);
            } else {
                counter.innerText = (decimals > 0) ? target.toFixed(decimals) : target;
            }
        };
        updateCount();
    };

    const observer = new IntersectionObserver((entries, observer) => {
        entries.forEach(entry => {
            if (entry.isIntersecting) {
                animate(entry.target);
                observer.unobserve(entry.target);
            }
        });
    }, { threshold: 0.2 });

    counters.forEach(counter => observer.observe(counter));
}
