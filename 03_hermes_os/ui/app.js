/**
 * Hermes OS - Backend for Frontend Logic
 * Obsługuje komunikację z wtyczkami Hermesa oraz zarządza widokami.
 */

document.addEventListener('DOMContentLoaded', () => {
    
    // --- Nawigacja (Views routing) ---
    // Logika została przeniesiona do globalnej funkcji switchView, wywoływanej w HTML.

    // --- Czat i Komunikacja (Mockup dla podłączenia pod backend) ---
    const chatInput = document.getElementById('chat-input');
    const sendBtn = document.getElementById('send-btn');
    const chatHistory = document.getElementById('chat-history');

    function addMessage(text, sender) {
        const msgDiv = document.createElement('div');
        msgDiv.classList.add('message', sender);
        
        if(sender === 'agent') {
            msgDiv.innerHTML = `<strong>Hermes:</strong> ${text}`;
        } else if (sender === 'user') {
            msgDiv.innerHTML = text;
        }
        
        chatHistory.appendChild(msgDiv);
        chatHistory.scrollTop = chatHistory.scrollHeight;
    }

    function handleSend() {
        const text = chatInput.value.trim();
        if(!text) return;

        addMessage(text, 'user');
        chatInput.value = '';

        // Symulacja wywołania API Hermesa
        setTimeout(() => {
            if(text.toLowerCase().includes('reddit') || text.toLowerCase().includes('lead')) {
                addMessage('Uruchamiam wtyczkę `holistic_reddit_scanner`... Przeszukuję subreddity pod kątem osób zmagających się z planowaniem. Wyniki wkrótce trafią na Twoją tablicę Kanban.', 'agent');
            } else {
                addMessage('Zrozumiałem. Analizuję cel i sprawdzam naszą pamięć Mnemosyne.', 'agent');
            }
        }, 800);
    }

    sendBtn.addEventListener('click', handleSend);
    chatInput.addEventListener('keypress', (e) => {
        if(e.key === 'Enter') handleSend();
    });

    // --- Dopamine Tracker (Nagrody dla ADHD) ---
    // Prosta symulacja
    let score = 450;
    function addWin(points) {
        score += points;
        document.querySelector('.dopamine-score').innerText = `${score} pkt`;
        
        // Pasek max 1000
        const percentage = Math.min((score / 1000) * 100, 100);
        document.getElementById('dopamine-progress').style.width = `${percentage}%`;
    }

    // Dodanie eventów dla kart kanbana (kliknięcie = wykonane zadanie)
    const kanbanCards = document.querySelectorAll('.kanban-card');
    kanbanCards.forEach(card => {
        card.addEventListener('dblclick', function() {
            if(this.parentNode.id !== 'col-done') {
                document.getElementById('col-done').appendChild(this);
                addWin(30); // Nagroda dopaminowa!
            }
        });
    });
});

// Drag and Drop Logic dla Tablicy Kanban
function allowDrop(ev) {
    ev.preventDefault();
}

function drag(ev) {
    ev.dataTransfer.setData("text", ev.target.id);
}

function drop(ev) {
    ev.preventDefault();
    var data = ev.dataTransfer.getData("text");
    var target = ev.target;
    // Jeśli rzucono na inną kartę, znajdź kolumnę
    while (!target.classList.contains('kanban-column')) {
        target = target.parentNode;
    }
    target.querySelector('.kanban-cards').appendChild(document.getElementById(data));
    
    // Jeśli rzucono do Done, dodaj punkty
    if(target.id === 'col-done') {
        const scoreElem = document.querySelector('.dopamine-score');
        let score = parseInt(scoreElem.innerText);
        score += 30;
        scoreElem.innerText = `${score} pkt`;
        const percentage = Math.min((score / 1000) * 100, 100);
        document.getElementById('dopamine-progress').style.width = `${percentage}%`;
    }
}

// Global View Switcher
function switchView(viewId, element) {
    const navLinks = document.querySelectorAll('.nav-links li');
    navLinks.forEach(l => l.classList.remove('active'));
    if(element) element.classList.add('active');

    const views = document.querySelectorAll('.view-container');
    views.forEach(v => v.classList.add('hidden'));
    
    const targetView = document.getElementById(viewId);
    if(targetView) targetView.classList.remove('hidden');
}
