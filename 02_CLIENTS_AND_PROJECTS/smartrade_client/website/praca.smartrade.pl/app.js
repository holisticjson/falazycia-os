document.addEventListener('DOMContentLoaded', () => {
    const consentCheck = document.getElementById('consent-check');
    const btnStartChat = document.getElementById('btn-start-chat');
    const chatWelcome = document.getElementById('chat-welcome');
    const chatContainer = document.getElementById('chat-container');
    const chatMessages = document.getElementById('chat-messages');
    const chatInput = document.getElementById('chat-input');
    const btnSendMessage = document.getElementById('btn-send-message');

    // Floating widget elements
    const chatToggle = document.getElementById('chat-toggle');
    const chatWindow = document.getElementById('chat-window');
    const chatCloseBtn = document.getElementById('chat-close-btn');
    const chatIcon = chatToggle.querySelector('.chat-icon');
    const closeIcon = chatToggle.querySelector('.close-icon');

    // Page CTA buttons
    const btnHeroCta = document.getElementById('btn-hero-cta');
    const btnFinalCta = document.getElementById('btn-final-cta');

    let chatHistory = [];
    let isWaitingForBot = false;

    // Toggle widget logic
    function openChatWidget() {
        chatWindow.classList.remove('hidden');
        chatToggle.classList.add('hidden'); // Hide toggle button entirely on open
        // Auto-focus chat input if active
        if (!chatContainer.classList.contains('hidden')) {
            chatInput.focus();
        }
    }

    function closeChatWidget() {
        chatWindow.classList.add('hidden');
        chatToggle.classList.remove('hidden'); // Show toggle button on close
    }

    function toggleChatWidget() {
        if (chatWindow.classList.contains('hidden')) {
            openChatWidget();
        } else {
            closeChatWidget();
        }
    }

    // Toggle listeners
    chatToggle.addEventListener('click', toggleChatWidget);
    chatCloseBtn.addEventListener('click', closeChatWidget);

    // CTA links
    if (btnHeroCta) {
        btnHeroCta.addEventListener('click', (e) => {
            e.preventDefault();
            openChatWidget();
        });
    }

    if (btnFinalCta) {
        btnFinalCta.addEventListener('click', (e) => {
            e.preventDefault();
            openChatWidget();
        });
    }

    // Consent check activation
    consentCheck.addEventListener('change', () => {
        btnStartChat.disabled = !consentCheck.checked;
    });

    // Start Chat
    btnStartChat.addEventListener('click', () => {
        chatWelcome.classList.add('hidden');
        chatContainer.classList.remove('hidden');
        initChat();
        setTimeout(() => {
            chatInput.focus();
        }, 100);
    });

    // Send message triggers
    btnSendMessage.addEventListener('click', handleUserSend);
    chatInput.addEventListener('keypress', (e) => {
        if (e.key === 'Enter') handleUserSend();
    });

    // Initialize conversation
    function initChat() {
        appendMessage('bot', 'Cześć! Bardzo się cieszę, że zainteresowała Cię praca w Hiszpanii. Nazywam się Bot HR i pomogę Ci przejść wstępną kwalifikację. 🌴');
        setTimeout(() => {
            appendMessage('bot', 'Zanim połączę Cię bezpośrednio z Jurkiem na WhatsAppie, muszę zadać Ci kilka ważnych pytań. Na początek: jak masz na imię i jakie masz doświadczenie? Jesteś glazurnikiem, hydraulikiem, czy kimś innym?');
        }, 1200);
    }

    // Handle user input sending
    async function handleUserSend() {
        const text = chatInput.value.trim();
        if (!text || isWaitingForBot) return;

        chatInput.value = '';
        appendMessage('user', text);
        
        // Save to internal history
        chatHistory.push({ role: 'user', content: text });

        // Show typing animation
        const typingId = showTypingIndicator();

        try {
            isWaitingForBot = true;
            const botResponse = await callGeminiProxy(chatHistory);
            removeTypingIndicator(typingId);

            appendMessage('bot', botResponse.reply);
            chatHistory.push({ role: 'model', content: botResponse.reply });

            // Check if user is fully qualified or rejected to end conversation and redirect
            if (botResponse.qualified) {
                appendRedirectButton(botResponse.summary);
            }
        } catch (error) {
            console.error('Błąd komunikacji z botem:', error);
            removeTypingIndicator(typingId);
            appendMessage('bot', 'Przepraszam, wystąpił mały problem techniczny po mojej stronie. Spróbuj napisać jeszcze raz za chwilę.');
        } finally {
            isWaitingForBot = false;
        }
    }

    // Render messages in UI
    function appendMessage(sender, text) {
        const msgDiv = document.createElement('div');
        msgDiv.className = `msg msg-${sender}`;
        msgDiv.textContent = text;
        chatMessages.appendChild(msgDiv);
        scrollChatToBottom();
    }

    // Redirect to WhatsApp button
    function appendRedirectButton(summary) {
        // Disable inputs
        chatInput.disabled = true;
        btnSendMessage.disabled = true;
        chatInput.placeholder = 'Kwalifikacja zakończona!';

        const redirectDiv = document.createElement('div');
        redirectDiv.style.textAlign = 'center';
        redirectDiv.style.marginTop = '20px';

        const link = document.createElement('a');
        link.className = 'btn btn-redirect';
        link.id = 'btn-whatsapp-redirect';
        
        // Base64 or plain text message
        const waText = encodeURIComponent(`Cześć Jurek! Przesyłam moje podsumowanie rekrutacyjne z praca.smartrade.pl:\n\n${summary}\n\nChcę porozmawiać o szczegółach wyjazdu!`);
        link.href = `https://wa.me/34631626065?text=${waText}`;
        link.target = '_blank';
        link.innerHTML = '💬 Przejdź do rozmowy z Jurkiem na WhatsApp';

        redirectDiv.appendChild(link);
        chatMessages.appendChild(redirectDiv);
        scrollChatToBottom();
    }

    // Typing Indicators
    function showTypingIndicator() {
        const id = 'typing-' + Date.now();
        const indicator = document.createElement('div');
        indicator.className = 'typing-indicator';
        indicator.id = id;
        indicator.innerHTML = `
            <div class="typing-dot"></div>
            <div class="typing-dot"></div>
            <div class="typing-dot"></div>
        `;
        chatMessages.appendChild(indicator);
        scrollChatToBottom();
        return id;
    }

    function removeTypingIndicator(id) {
        const el = document.getElementById(id);
        if (el) el.remove();
    }

    function scrollChatToBottom() {
        chatMessages.scrollTop = chatMessages.scrollHeight;
    }

    // API cURL PHP Proxy client
    async function callGeminiProxy(history) {
        const response = await fetch('api/chat.php', {
            method: 'POST',
            headers: {
                'Content-Type': 'application/json'
            },
            body: JSON.stringify({ history: history })
        });

        if (!response.ok) {
            throw new Error('API server returned error status ' + response.status);
        }

        return await response.json();
    }
});
