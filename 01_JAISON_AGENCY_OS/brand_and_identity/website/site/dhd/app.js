// ======================================================================
// 🧠 A(I)-DHD AUDIT APPLICATION LOGIC (v1.1)
// ======================================================================

const slides = [
    "slide0", 
    "slide1", "slide2", "slide3", "slide4", "slide5", 
    "slide6", "slide7", "slide8", "slide9", "slide10", 
    "slide11", "slide12", "slide13", "slide14", "slide15", 
    "slide15_email", 
    "slide16"
];

let currentSlideIndex = 0;
const answers = {};

function nextSlide() {
    const currentSlideId = slides[currentSlideIndex];
    const activeSlide = document.getElementById(currentSlideId);
    if (activeSlide) {
        activeSlide.classList.remove('active');
    }
    
    currentSlideIndex++;
    
    const nextSlideId = slides[currentSlideIndex];
    const nextSlideElem = document.getElementById(nextSlideId);
    if (nextSlideElem) {
        nextSlideElem.classList.add('active');
    }
    
    // Manage progress bar display (only during active questions 1 to 15)
    const progressContainer = document.getElementById('progressContainer');
    if (currentSlideIndex > 0 && currentSlideIndex <= 15) {
        progressContainer.style.display = 'block';
        updateProgressBar();
    } else {
        progressContainer.style.display = 'none';
    }
    
    // If we land on the final results page, calculate the outcomes
    if (nextSlideId === "slide16") {
        calculateResults();
    }
}

function updateProgressBar() {
    const progressBar = document.getElementById('progressBar');
    const percentage = ((currentSlideIndex - 1) / 15) * 100;
    progressBar.style.width = `${percentage}%`;
}

function selectAnswer(questionNum, points) {
    answers[questionNum] = points;
    
    // Dynamic micro-delay for smooth ADHD-friendly user flow
    setTimeout(() => {
        nextSlide();
    }, 200);
}

function submitLead() {
    const emailInput = document.getElementById('leadEmail');
    const email = emailInput.value.trim();
    
    if (!email || !email.includes('@')) {
        alert('Proszę podać poprawny adres e-mail, aby otrzymać darmowy e-book i raport!');
        emailInput.style.borderColor = '#ff85a1';
        emailInput.style.boxShadow = '0 0 10px rgba(255, 133, 161, 0.2)';
        return;
    }
    
    // Calculate final scores for the payload
    let totalScore = 0;
    let categoryScores = { chaos: 0, money: 0, focus: 0 };
    for (let i = 1; i <= 15; i++) {
        const val = answers[i] || 0;
        totalScore += val;
        if (i <= 5) categoryScores.chaos += val;
        else if (i <= 10) categoryScores.money += val;
        else categoryScores.focus += val;
    }
    
    let diagnosis = "";
    if (totalScore <= 10) diagnosis = "Holistic Operator";
    else if (totalScore <= 20) diagnosis = "Strefa Sredniakow";
    else diagnosis = "Rekodzielo i Chaos";    // Target n8n Webhook URL
    const functionUrl = "https://n8n.jaison.pl/webhook/jaison-audit";
    
    const payload = {
        email: email,
        score: totalScore,
        diagnosis: diagnosis,
        category_scores: categoryScores
    };
    
    // Non-blocking fetch submission for seamless UI transition
    fetch(functionUrl, {
        method: 'POST',
        headers: { 'Content-Type': 'application/json' },
        body: JSON.stringify(payload),
        mode: 'cors'
    })
    .then(response => response.json())
    .then(data => console.log('Dane zapisane w CRM Sheets:', data))
    .catch(err => console.log('Offline / Testy lokalne - dane zachowane w pamięci:', err));
    
    // Save email context globally
    answers['email'] = email;
    
    // Smooth transition: redirect to unified checkout with order bump page
    setTimeout(() => {
        window.location.href = `checkout.html?score=${totalScore}&email=${encodeURIComponent(email)}&chaos=${categoryScores.chaos}&money=${categoryScores.money}&focus=${categoryScores.focus}`;
    }, 600);
}

function calculateResults() {
    let totalScore = 0;
    let categoryScores = {
        chaos: 0,
        money: 0,
        focus: 0
    };

    for (let i = 1; i <= 15; i++) {
        const val = answers[i] || 0;
        totalScore += val;
        
        if (i <= 5) {
            categoryScores.chaos += val;
        } else if (i <= 10) {
            categoryScores.money += val;
        } else {
            categoryScores.focus += val;
        }
    }

    document.getElementById('finalScore').innerText = totalScore;
    
    const titleElem = document.getElementById('resultTitle');
    const descElem = document.getElementById('resultDesc');
    const recElem = document.getElementById('resultRec');
    
    const leadEmail = answers['email'] || "Twój e-mail";
    
    if (totalScore <= 10) {
        titleElem.innerText = "Diagnoza: Poziom 🟢 Holistic Operator";
        titleElem.style.color = "#a8e6cf";
        descElem.innerText = `Gratulacje! Twój wynik to ${totalScore}/30. Działasz w sposób wysoce zorganizowany. Nie cierpisz na chroniczny paraliż i potrafisz delegować zadania. AI-DHD posłuży Ci jako potężna dźwignia deweloperska.`;
        recElem.innerHTML = `<strong>Zalecany kolejny krok:</strong> Wysłaliśmy spersonalizowany e-book na adres <strong>${leadEmail}</strong>. Skonfiguruj zaawansowane agenty w tle (np. autonomicznego CSO do automatycznego odpisywania na maile), które zaczną pracować za Ciebie 24/7.`;
    } else if (totalScore <= 20) {
        titleElem.innerText = "Diagnoza: Poziom 🟡 Strefa Średniaków";
        titleElem.style.color = "#ffd166";
        descElem.innerText = `Twój wynik to ${totalScore}/30. Posiadasz pojedyncze narzędzia, ale brak Ci zintegrowanego Systemu. Często zmieniasz zdanie (SOS), tracąc fokus. Wyczerpanie kognitywne spowalnia Twoje codzienne przychody.`;
        recElem.innerHTML = `<strong>Zalecany kolejny krok:</strong> Twój raport i e-book zostały wysłane na adres <strong>${leadEmail}</strong>. Uprość swój stack technologiczny. Zamiast 10 narzędzi, stwórz jeden wirtualny zarząd z asystentami (CEO, Ghost, CSO, CTO) i naucz się pracować w jednym oknie czatu, w oparciu o sztywne pliki profilu.`;
    } else {
        titleElem.innerText = "Diagnoza: Poziom 🔴 Rękodzieło i Chaos";
        titleElem.style.color = "#ff85a1";
        descElem.innerText = `Twój wynik to ${totalScore}/30. Jesteś niewolnikiem własnej firmy i działasz w permanentnym paraliżu startowym. Wysokie ryzyko nagłego wypalenia ADHD. Bez Twojej obecności wszystko natychmiast leży.`;
        recElem.innerHTML = `<strong>Zalecany kolejny krok:</strong> Sprawdź skrzynkę <strong>${leadEmail}</strong> – wysłaliśmy tam natychmiastową instrukcję ratunkową. Wstrzymaj skomplikowane automatyzacje. Twoim priorytetem jest wdrożenie <strong>Procedury Wyciszenia Chaosu</strong>: 1. Uporządkowanie zadań do papierowego dziennika, 2. Stworzenie prostego Profilu Przedsiębiorcy, 3. Dopuszczenie AI jako asystenta do najprostszych spraw.`;
    }
    
    // Inject tailored neuro-advice if focus is the main bottleneck
    if (categoryScores.focus > categoryScores.chaos && categoryScores.focus > categoryScores.money && totalScore > 10) {
        recElem.innerHTML += `<br><br><strong>⚠️ Detektor ADHD:</strong> Twój największy wyciek leży w sferze <em>Skupienia i Paraliżu Zadaniowego</em>. Przed przystąpieniem do jakiejkolwiek pracy wdroż u siebie <strong>Zasadę 5 sekund</strong> oraz tryb <strong>Zen Mode</strong> – chowaj wszystkie rozpraszacze i pracuj tylko nad jednym nano-krokiem na raz.`;
    } else if (categoryScores.money > categoryScores.chaos && categoryScores.money > categoryScores.focus && totalScore > 10) {
        recElem.innerHTML += `<br><br><strong>⚠️ Detektor Pieniędzy:</strong> Twój największy wyciek to <em>Wyciek Pieniędzy w Sprzedaży</em>. Twoim kluczowym zadaniem jest natychmiastowe wdrożenie automatycznego kalendarza (np. Cal.com / Calendly) oraz prostego asystenta sprzedaży (CSO) do szybkiego generowania follow-upów.`;
    }
}

function restartAudit() {
    currentSlideIndex = 0;
    // Clear answers
    for (let key in answers) {
        delete answers[key];
    }
    
    // Reset DOM slide classes
    slides.forEach(slideId => {
        const slide = document.getElementById(slideId);
        if (slide) slide.classList.remove('active');
    });
    
    // Reset inputs
    const emailInput = document.getElementById('leadEmail');
    if (emailInput) {
        emailInput.value = "";
        emailInput.style.borderColor = 'rgba(255, 255, 255, 0.1)';
        emailInput.style.boxShadow = 'none';
    }
    
    // Activate slide 0
    document.getElementById(slides[0]).classList.add('active');
    document.getElementById('progressContainer').style.display = 'none';
}

// ======================================================================
// 🚀 GLOBAL WINDOW BINDINGS (Bridges scope gap for module onClick handlers)
// ======================================================================
window.nextSlide = nextSlide;
window.selectAnswer = selectAnswer;
window.submitLead = submitLead;
window.restartAudit = restartAudit;

