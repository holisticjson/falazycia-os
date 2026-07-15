
(function() {
  const toggleBtn  = document.getElementById('jasbot-toggle');
  const closeBtn   = document.getElementById('jasbot-close-btn');
  const windowEl   = document.getElementById('jasbot-window');
  const messages   = document.getElementById('jasbot-messages');
  const input      = document.getElementById('jasbot-input');
  const sendBtn    = document.getElementById('jasbot-send-btn');
  const badge      = document.getElementById('jasbot-badge');

  const WA_NUMBER  = '48663970016';
  let cart         = [];
  let step         = 'menu';

  const MENU_ITEMS = [
    { id:1, name:'Zestaw Kurczak z Rożna (1/2 kurczaka)', price:34,  emoji:'🍗' },
    { id:2, name:'Cały Kurczak z Rożna',                  price:38,  emoji:'🍗' },
    { id:3, name:'Kebab w bułce',                          price:22,  emoji:'🥙' },
    { id:4, name:'Zestaw Kebab z frytkami',               price:29,  emoji:'🥙' },
    { id:5, name:'Hamburger z kurczakiem',                 price:24,  emoji:'🍔' },
    { id:6, name:'Frytki duże',                           price:9,   emoji:'🍟' },
    { id:7, name:'Surówka colesław',                      price:6,   emoji:'🥗' },
  ];

  function addMsg(text, type='bot') {
    const div = document.createElement('div');
    div.className = 'jasbot-msg ' + type;
    div.innerHTML = text;
    messages.appendChild(div);
    messages.scrollTop = messages.scrollHeight;
  }

  function showMenu() {
    let html = '<strong>Oto nasze dania:</strong><br><br>';
    MENU_ITEMS.forEach(item => {
      html += '<div style="margin:4px 0;"><button onclick="window.jasBotAdd(' + item.id + ')" style="background:#FCC036;border:2px solid #2D1A1E;border-radius:8px;padding:6px 10px;cursor:pointer;font-family:inherit;width:100%;text-align:left;font-size:0.85rem;"><strong>' + item.emoji + ' ' + item.name + '</strong> — ' + item.price + ' zł  [+]</button></div>';
    });
    addMsg(html);
  }

  function updateBadge() {
    const total = cart.reduce((s, i) => s + i.qty, 0);
    badge.textContent = total;
    badge.style.display = total > 0 ? 'flex' : 'none';
  }

  window.jasBotAdd = function(id) {
    const item = MENU_ITEMS.find(i => i.id === id);
    const existing = cart.find(i => i.id === id);
    if (existing) { existing.qty++; }
    else { cart.push({ ...item, qty: 1 }); }
    updateBadge();
    addMsg('✅ Dodano: <strong>' + item.name + '</strong>. Masz już <strong>' + cart.reduce((s,i)=>s+i.qty,0) + '</strong> pozycji w koszyku. Chcesz coś dodać, czy <button onclick="window.jasBotCheckout()" style="background:#D32F2F;color:#fff;border:2px solid #2D1A1E;border-radius:6px;padding:4px 10px;cursor:pointer;font-family:inherit;">ZŁÓŻ ZAMÓWIENIE</button>?');
  };

  window.jasBotCheckout = function() {
    if (cart.length === 0) { addMsg('🛒 Koszyk jest pusty! Wybierz najpierw danie.'); return; }
    let msg = '🧾 Podsumowanie zamówienia:\n';
    let total = 0;
    cart.forEach(i => { msg += i.emoji + ' ' + i.name + ' x' + i.qty + ' = ' + (i.price * i.qty) + ' zł\n'; total += i.price * i.qty; });
    msg += '\n💰 RAZEM: ' + total + ' zł\n\nOdbiór osobisty: ul. Rokicińska 190, Łódź\nCzas: ~20 min';
    const waMsg = encodeURIComponent(msg);
    addMsg('✅ Za chwilę otworzymy WhatsApp z Twoim zamówieniem. Zapłacisz przy odbiorze gotówką lub kartą. <a href="https://wa.me/' + WA_NUMBER + '?text=' + waMsg + '" target="_blank" style="display:inline-block;margin-top:10px;background:#25D366;color:#fff;padding:8px 16px;border-radius:8px;border:2px solid #2D1A1E;text-decoration:none;font-weight:700;">📱 Wyślij przez WhatsApp</a>');
    cart = [];
    updateBadge();
  };

  function sendMsg() {
    const text = input.value.trim();
    if (!text) return;
    addMsg(text, 'user');
    input.value = '';
    setTimeout(() => {
      const lower = text.toLowerCase();
      if (lower.includes('menu') || lower.includes('dania') || lower.includes('cena')) { showMenu(); }
      else if (lower.includes('godzin') || lower.includes('kiedy') || lower.includes('otwart')) { addMsg('🕐 Jesteśmy otwarci:<br><strong>Pon–Sob: 09:00–19:00</strong><br>Niedziela: nieczynne'); }
      else if (lower.includes('adres') || lower.includes('gdzie') || lower.includes('dojazd')) { addMsg('📍 Znajdziesz nas pod adresem:<br><strong>ul. Rokicińska 190, Łódź</strong><br>(tuż obok Selgros, dzielnica Widzew)'); }
      else if (lower.includes('zamówi') || lower.includes('koszyk') || lower.includes('zamow')) { showMenu(); addMsg('Wybierz dania które chcesz, a potem kliknij "ZŁÓŻ ZAMÓWIENIE" aby przesłać je do nas przez WhatsApp!'); }
      else { addMsg('Hej! Jestem JaśBot 🍗 Wpisz:<br>• <strong>menu</strong> — zobaczysz nasze dania<br>• <strong>godziny</strong> — sprawdzisz kiedy jesteśmy otwarci<br>• <strong>adres</strong> — dowiesz się gdzie nas znaleźć'); }
    }, 400);
  }

  toggleBtn.addEventListener('click', () => {
    windowEl.classList.toggle('open');
    if (windowEl.classList.contains('open') && messages.children.length === 0) {
      addMsg('Cześć! 👋 Jestem <strong>JaśBot</strong>, Twój asystent w Barze Jaś!<br><br>Wpisz <strong>menu</strong> aby zobaczyć nasze dania i złożyć zamówienie online — wyślę je bezpośrednio do nas przez WhatsApp!');
    }
  });
  closeBtn.addEventListener('click',  () => windowEl.classList.remove('open'));
  sendBtn.addEventListener('click',   sendMsg);
  input.addEventListener('keypress',  e => { if (e.key === 'Enter') sendMsg(); });
})();
