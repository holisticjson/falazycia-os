
(function() {
  const toggleBtn = document.getElementById('jasbot-toggle');
  const closeBtn  = document.getElementById('jasbot-close-btn');
  const windowEl  = document.getElementById('jasbot-window');
  const messages  = document.getElementById('jasbot-messages');
  const input     = document.getElementById('jasbot-input');
  const sendBtn   = document.getElementById('jasbot-send-btn');
  const badge     = document.getElementById('jasbot-badge');

  const WA_NUMBER  = '48663970016';
  const BLIK_PHONE = '663 970 016';
  let cart = [];
  let step = 'idle';
  let pendingOrderText = '';
  let pendingTotal = 0;

  const MENU_ITEMS = [
  {
    "id": 1,
    "name": "Zestaw Kurczak z Rożna (Cały)",
    "price": 52,
    "desc": "Cały soczysty kurczak z rożna (~900g) + duża porcja złocistych frytek (300g) lub opiekanych ziemniaczków + duży zestaw 3 świeżych domowych surówek (300g) + sos autorski czosnkowy i pikantny gratis!"
  },
  {
    "id": 2,
    "name": "Zestaw Kurczak z Rożna (Połówka)",
    "price": 34,
    "desc": "Połówka chrupiącego kurczaka (~450g) + złociste frytki (150g) lub opiekane ziemniaczki + zestaw 3 świeżych domowych surówek (150g) + sos autorski czosnkowy lub pikantny gratis!"
  },
  {
    "id": 3,
    "name": "Legendarny Kurczak z Rożna (Cały)",
    "price": 38,
    "desc": "Cały dorodny kurczak z polskiej hodowli (~900g), ręcznie marynowany w autorskiej kompozycji 12 ziół, pieczony na złocisty kolor (sama sztuka bez dodatków)"
  },
  {
    "id": 4,
    "name": "Kurczak z Rożna (Połówka)",
    "price": 20,
    "desc": "Sama połówka soczystego kurczaka (~450g) o chrupiącej, złotej skórce, świeżo pieczona na tradycyjnym rożnie obrotowym (sama sztuka, bez dodatków)"
  },
  {
    "id": 5,
    "name": "Zestaw Kebab z Frytkami i Surówkami",
    "price": 32,
    "desc": "Sycąca porcja dobrze przypieczonego mięsa kebab (~180g) + frytki (150g) + zestaw 3 świeżych surówek (150g) + sos autorski czosnkowy lub pikantny"
  },
  {
    "id": 6,
    "name": "Kebab w Bułce z Surówkami",
    "price": 22,
    "desc": "Opiekana rzemieślnicza bułka z dużą ilością mięsa kebab (~150g), świeżą kapustą, pomidorem, ogórkiem, cebulką i domowym sosem (czosnek/ostry/mieszany)"
  },
  {
    "id": 7,
    "name": "Hamburger z Filetem z Kurczaka",
    "price": 20,
    "desc": "Chrupiący, świeżo smażony panierowany filet z piersi kurczaka (~150g) w bułce sezamowej z pomidorem, ogórkiem, sałatą i wyrazistym sosem burgerowym"
  },
  {
    "id": 8,
    "name": "Smerf – Zestaw dla Dzieci",
    "price": 18,
    "desc": "Delikatne domowe kąski z piersi kurczaka (~100g) + frytki (100g) + łagodny ketchup + zimny soczek owocowy w kartoniku (200ml)"
  },
  {
    "id": 9,
    "name": "Domowa Zupa Dnia",
    "price": 10,
    "desc": "Pyszna, gorąca zupa (350ml) gotowana codziennie rano na świeżych warzywach i mięsie (np. pomidorowa, rosół z makaronem rzemieślniczym lub żurek — zapytaj nas o dzisiejszą!)"
  },
  {
    "id": 10,
    "name": "Złociste Frytki (Porcja 150g)",
    "price": 10,
    "desc": "Chrupiące na zewnątrz, miękkie i puszyste w środku złociste frytki, idealnie usmażone i posolone"
  },
  {
    "id": 11,
    "name": "Opiekane Ziemniaczki (Porcja 150g)",
    "price": 10,
    "desc": "Aromatyczne, złociste połówki ziemniaczków pieczone w ziołach, miękkie w środku i chrupiące z wierzchu"
  },
  {
    "id": 12,
    "name": "Zestaw Domowych Surówek",
    "price": 8,
    "desc": "Świeża, witaminowa porcja (150g) trzech domowych surówek (biała kapusta, czerwona kapusta, marchewka) przygotowywana codziennie na miejscu"
  },
  {
    "id": 13,
    "name": "Zimne Napoje (Pepsi / Mirinda 0.33l)",
    "price": 8,
    "desc": "Zimna, orzeźwiająca puszka Pepsi, Pepsi Zero, Mirinda lub 7Up (0.33l) prosto z lodówki"
  }
];

  function addMsg(text, type) {
    type = type || 'bot';
    var div = document.createElement('div');
    div.className = 'jasbot-msg ' + type;
    div.innerHTML = text;
    messages.appendChild(div);
    messages.scrollTop = messages.scrollHeight;
  }

  function showMenu() {
    var html = '<strong>🍗 Nasze MENU — kliknij pozycję, aby dodać do koszyka:</strong><br><br>';
    for (var i = 0; i < MENU_ITEMS.length; i++) {
      var item = MENU_ITEMS[i];
      html += '<div style="margin:8px 0;">'
            + '<button onclick="window.jasBotAdd(' + item.id + ')" '
            + 'style="background:#FCC036;border:2px solid #2D1A1E;border-radius:10px;padding:8px 12px;'
            + 'cursor:pointer;font-family:inherit;width:100%;text-align:left;box-shadow:2px 2px 0px #2D1A1E;'
            + 'transition:all 0.1s ease;display:block;">'
            + '<div style="display:flex;justify-content:space-between;align-items:center;margin-bottom:3px;gap:8px;">'
            + '<span style="font-weight:800;font-size:0.9rem;color:#2D1A1E;flex:1;">' + item.name + '</span>'
            + '<span style="font-weight:800;font-size:0.95rem;color:#D32F2F;background:#fff;padding:1px 6px;border-radius:6px;border:1px solid #2D1A1E;white-space:nowrap;">' + item.price + ' zł</span>'
            + '</div>'
            + '<div style="font-size:0.75rem;color:#555;line-height:1.3;font-weight:500;">' + item.desc + '</div>'
            + '</button></div>';
    }
    addMsg(html);
  }

  function updateBadge() {
    var total = cart.reduce(function(s,i){ return s+i.qty; }, 0);
    badge.textContent = total;
    badge.style.display = total > 0 ? 'flex' : 'none';
  }

  window.jasBotAdd = function(id) {
    var item = null;
    for (var i = 0; i < MENU_ITEMS.length; i++) { if (MENU_ITEMS[i].id === id) { item = MENU_ITEMS[i]; break; } }
    var existing = null;
    for (var i = 0; i < cart.length; i++) { if (cart[i].id === id) { existing = cart[i]; break; } }
    if (existing) { existing.qty++; } else { cart.push({id:item.id, name:item.name, price:item.price, qty:1}); }
    updateBadge();
    var count = cart.reduce(function(s,i){ return s+i.qty; }, 0);
    addMsg('Dodano: <strong>' + item.name + '</strong>. Koszyk: <strong>' + count + '</strong> pozycji.<br>'
         + '<button onclick="window.jasBotCheckout()" '
         + 'style="margin-top:8px;background:#D32F2F;color:#fff;border:2px solid #2D1A1E;'
         + 'border-radius:6px;padding:6px 14px;cursor:pointer;font-weight:700;">'
         + 'ZŁÓŻ ZAMÓWIENIE</button>&nbsp;lub dodaj kolejne danie.');
  };

  window.jasBotCheckout = function() {
    if (cart.length === 0) { addMsg('Koszyk jest pusty! Wybierz najpierw danie.'); return; }
    var orderLines = '';
    var total = 0;
    for (var i = 0; i < cart.length; i++) {
      var ci = cart[i];
      orderLines += ci.name + ' x' + ci.qty + ' = ' + (ci.price * ci.qty) + ' zł\n';
      total += ci.price * ci.qty;
    }
    pendingOrderText = orderLines;
    pendingTotal = total;
    cart = [];
    updateBadge();
    step = 'awaiting_blik_ref';
    addMsg('<strong>Podsumowanie zamówienia:</strong><br><br>'
         + pendingOrderText.replace(/\n/g,'<br>')
         + '<br><strong>RAZEM: ' + pendingTotal + ' zł</strong>'
         + '<hr style="border:1px dashed #2D1A1E;margin:12px 0;">'
         + '<strong>Zapłać teraz przez BLIK na telefon:</strong><br><br>'
         + '1. Otwórz aplikację bankową<br>'
         + '2. Wybierz <strong>Przelew na telefon BLIK</strong><br>'
         + '3. Numer: <strong style="color:#D32F2F;font-size:1.1rem;">' + BLIK_PHONE + '</strong><br>'
         + '4. Kwota: <strong>' + pendingTotal + ' zł</strong><br>'
         + '5. Tytuł przelewu: np. <em>Zamówienie JaśBot</em><br><br>'
         + '<strong>Gdy wyślesz przelew — wpisz poniżej jego tytuł (lub imię i nazwisko), abyśmy mogli szybko potwierdzić wpłatę.</strong>');
  };

  window.jasBotOpenWithCart = function(pageCart) {
    cart = [];
    for (var key in pageCart) {
      if (pageCart.hasOwnProperty(key)) {
        var pc = pageCart[key];
        var itemId = 1;
        for (var i = 0; i < MENU_ITEMS.length; i++) {
          if (MENU_ITEMS[i].name === pc.name) {
            itemId = MENU_ITEMS[i].id;
            break;
          }
        }
        cart.push({ id: itemId, name: pc.name, price: pc.price, qty: pc.qty });
      }
    }
    updateBadge();
    windowEl.classList.add('open');
    var labelEl = document.getElementById('jasbot-label');
    if (labelEl) labelEl.style.display = 'none';
    window.jasBotCheckout();
  };

  function handleBlikRef(text) {
    step = 'idle';
    var blikRef = text.trim();
    var waMsg = encodeURIComponent(
      'NOWE ZAMÓWIENIE - Bar Jaś JaśBot\n'
      + '----------------------------\n'
      + pendingOrderText
      + '\nRAZEM: ' + pendingTotal + ' zł\n'
      + '----------------------------\n'
      + 'BLIK WYŚLANY\n'
      + 'Tytuł przelewu: ' + blikRef + '\n'
      + '(Proszę sprawdzić w aplikacji bankowej)\n'
      + '----------------------------\n'
      + 'Odbiór: ul. Rokicińska 190/214, Łódź\n'
      + 'Czas realizacji: ok. 20 min'
    );
    addMsg('Zamówienie z potwierdzeniem BLIK gotowe!<br><br>'
         + 'Kliknij przycisk poniżej, aby przesłać zamówienie <strong>i potwierdzenie płatności</strong> bezpośrednio do Marysi na WhatsApp:<br><br>'
         + '<a href="https://wa.me/' + WA_NUMBER + '?text=' + waMsg + '" target="_blank" '
         + 'style="display:inline-block;background:#25D366;color:#fff;padding:10px 20px;'
         + 'border-radius:10px;border:2px solid #2D1A1E;text-decoration:none;font-weight:700;font-size:1rem;text-align:center;">'
         + 'Wyślij zamówienie na WhatsApp</a><br><br>'
         + '<small>Czas realizacji ~20 min. Bar potwierdzi zamówienie przez WhatsApp.</small>');
    pendingOrderText = '';
    pendingTotal = 0;
  }

  function sendMsg() {
    var text = input.value.trim();
    if (!text) return;
    addMsg(text, 'user');
    input.value = '';
    if (step === 'awaiting_blik_ref') { handleBlikRef(text); return; }
    setTimeout(function() {
      var lower = text.toLowerCase();
      if (lower.indexOf('menu') >= 0 || lower.indexOf('dania') >= 0 || lower.indexOf('cena') >= 0 || lower.indexOf('cennik') >= 0) {
        showMenu();
      } else if (lower.indexOf('godzin') >= 0 || lower.indexOf('kiedy') >= 0 || lower.indexOf('otwart') >= 0) {
        addMsg('Jesteśmy otwarci:<br><strong>Pon-Sob: 09:00-19:00</strong><br>Niedziela: nieczynne');
      } else if (lower.indexOf('adres') >= 0 || lower.indexOf('gdzie') >= 0 || lower.indexOf('dojazd') >= 0 || lower.indexOf('lokalizacj') >= 0) {
        addMsg('Znajdziesz nas pod adresem:<br><strong>ul. Rokicińska 190/214, Łódź</strong><br>(tuż obok Selgros, dzielnica Widzew)');
      } else if (lower.indexOf('blik') >= 0 || lower.indexOf('płat') >= 0 || lower.indexOf('platn') >= 0) {
        addMsg('Przyjmujemy płatność przez <strong>BLIK na numer telefonu</strong>: <strong>' + BLIK_PHONE + '</strong><br>Wybierz dania z menu, a JaśBot przeprowadzi Cie przez płatność krok po kroku!');
      } else if (lower.indexOf('zamów') >= 0 || lower.indexOf('zamow') >= 0 || lower.indexOf('koszyk') >= 0 || lower.indexOf('chcę') >= 0 || lower.indexOf('chce') >= 0) {
        showMenu();
      } else {
        addMsg('Jesteś w Barze Jaś! Wpisz:<br>'
             + '<strong>menu</strong> - cennik i dania<br>'
             + '<strong>godziny</strong> - kiedy jesteśmy otwarci<br>'
             + '<strong>adres</strong> - jak do nas trafić<br>'
             + '<strong>zamów</strong> - złóż szybkie zamówienie online');
      }
    }, 350);
  }

  toggleBtn.addEventListener('click', function() {
    windowEl.classList.toggle('open');
    var labelEl = document.getElementById('jasbot-label');
    if (windowEl.classList.contains('open')) {
      if (labelEl) labelEl.style.display = 'none';
      if (messages.children.length === 0) {
        addMsg('Cześć! Jestem <strong>JaśBot</strong> - wirtualny asystent Baru Jaś! 🍗<br><br>'
             + 'Oto nasze pełne, pyszne menu. Kliknij wybrane pozycje, aby dodać je do koszyka i szybko złożyć zamówienie:<br>'
             + 'Płatność wygodnie przez <strong>BLIK na telefon</strong>.');
        showMenu();
      }
    } else {
      if (labelEl && window.innerWidth > 768) {
        labelEl.style.display = 'block';
      }
    }
  });
  closeBtn.addEventListener('click', function() {
    windowEl.classList.remove('open');
    var labelEl = document.getElementById('jasbot-label');
    if (labelEl && window.innerWidth > 768) {
      labelEl.style.display = 'block';
    }
  });
  sendBtn.addEventListener('click', sendMsg);
  input.addEventListener('keypress', function(e) { if (e.key === 'Enter') sendMsg(); });
})();
