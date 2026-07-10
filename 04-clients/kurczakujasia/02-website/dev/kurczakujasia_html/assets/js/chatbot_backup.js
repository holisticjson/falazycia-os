
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
  let pendingPhone = '';
  let pendingName = '';
  let pendingOrderId = '';

  const MENU_ITEMS = [
  {
    "id": 1,
    "name": "Kurczak z rożna (1 sztuka)",
    "price": 40.0,
    "desc": "Legendarny, cały chrupiący kurczak z rożna obrotowego, ręcznie marynowany w kompozycji 12 ziół i powoli pieczony na złocisty kolor (sama sztuka)."
  },
  {
    "id": 2,
    "name": "Kurczak z rożna (1/2 sztuki)",
    "price": 20.0,
    "desc": "Soczysta połówka chrupiącego kurczaka, pieczona na tradycyjnym rożnie obrotowym (sama połówka)."
  },
  {
    "id": 3,
    "name": "Zestaw z połówką kurczaka (z frytkami i surówką)",
    "price": 36.0,
    "desc": "Sycący zestaw obiadowy: połówka soczystego kurczaka z rożna (20 zł) podawana ze złocistymi frytkami (150g — 9 zł) oraz świeżą, domową surówką (250g — 7 zł)."
  },
  {
    "id": 4,
    "name": "Zestaw z całym kurczakiem (z frytkami i surówką)",
    "price": 56.0,
    "desc": "Olbrzymi zestaw dla naprawdę głodnych lub dla dwojga: cały, legendarny kurczak z rożna (40 zł) podawany ze złocistymi frytkami (150g — 9 zł) oraz świeżą, domową surówką (250g — 7 zł)."
  },
  {
    "id": 5,
    "name": "Kurczak z rożna zestaw (ze świeżymi surówkami)",
    "price": 40.0,
    "desc": "Cały chrupiący kurczak z rożna (1 sztuka) serwowany w zestawie z naszym codziennie przygotowywanym, świeżym bukietem domowych surówek (250g)."
  },
  {
    "id": 6,
    "name": "Kebab zestaw (z frytkami lub ryżem)",
    "price": 35.0,
    "desc": "Sycąca porcja dobrze doprawionego, soczystego mięsa kebab podawana ze złocistymi frytkami lub sypkim ryżem oraz bukietem surówek i sosem."
  },
  {
    "id": 7,
    "name": "Kebab w bułce (z surówkami)",
    "price": 25.0,
    "desc": "Opiekana, chrupiąca rzemieślnicza bułka wypełniona soczystym mięsem kebab, świeżymi warzywami oraz autorskim sosem (czosnkowym lub pikantnym)."
  },
  {
    "id": 8,
    "name": "Kebab w tortilli",
    "price": 24.0,
    "desc": "Ciepła tortilla ściśle zawinięta z dużą ilością przypieczonego mięsa kebab, chrupiącymi surówkami i wyrazistymi sosami."
  },
  {
    "id": 9,
    "name": "Hamburger z filetem z kurczaka",
    "price": 20.0,
    "desc": "Chrupiący panierowany filet z piersi kurczaka w puszystej bułce sezamowej z pomidorem, ogórkiem, sałatą i wyrazistym sosem burgerowym."
  },
  {
    "id": 10,
    "name": "Hamburger",
    "price": 16.0,
    "desc": "Klasyczny, soczysty kotlet wołowy w bułce z sezamem, podawany z chrupiącym ogórkiem kiszonym, cebulką, ketchupem i musztardą."
  },
  {
    "id": 11,
    "name": "Hot-Dog",
    "price": 14.0,
    "desc": "Gorąca parówka w chrupiącej, podgrzanej bułce z ulubionymi sosami (ketchup, musztarda, duński) i prażoną cebulką."
  },
  {
    "id": 12,
    "name": "Kiełbasa z grilla (porcja 100g)",
    "price": 10.0,
    "desc": "Aromatyczna, doskonale przypieczona na grillu tradycyjna polska kiełbasa, podawana na gorąco z musztardą lub ketchupem (cena za porcję 100g)."
  },
  {
    "id": 13,
    "name": "Frytki (porcja 150g)",
    "price": 9.0,
    "desc": "Złociste, chrupiące frytki, idealnie usmażone i delikatnie posolone - doskonały dodatek do każdego zamówienia."
  },
  {
    "id": 14,
    "name": "Surówka (porcja 250g)",
    "price": 7.0,
    "desc": "Świeżo siekane, pełne witamin domowe surówki przygotowywane codziennie rano ze świeżych warzyw."
  },
  {
    "id": 15,
    "name": "Bułka Poznańska",
    "price": 2.5,
    "desc": "Świeża, chrupiąca rzemieślnicza Bułka Poznańska (przedzielana), doskonała jako tradycyjny dodatek do kurczaka z rożna."
  },
  {
    "id": 16,
    "name": "Bułka Kajzerka",
    "price": 1.0,
    "desc": "Klasyczna, świeża bułka kajzerka z chrupiącą złocistą skórką, idealny tradycyjny dodatek."
  },
  {
    "id": 17,
    "name": "Kawa",
    "price": 10.0,
    "desc": "Aromatyczna, gorąca kawa parzona, idealna na każdą porę dnia."
  },
  {
    "id": 18,
    "name": "Herbata",
    "price": 6.0,
    "desc": "Gorąca, rozgrzewająca herbata podawana z cytryną."
  },
  {
    "id": 19,
    "name": "Pepsi",
    "price": 8.0,
    "desc": "Mocno schłodzona, orzeźwiająca puszka Pepsi (lub inny zimny napój z oferty) prosto z lodówki."
  },
  {
    "id": 20,
    "name": "Opakowanie",
    "price": 1.0,
    "desc": "Opakowanie na wynos zapewniające bezpieczny i higieniczny transport posiłku oraz utrzymanie temperatury."
  },
  {
    "id": 21,
    "name": "Sztućce",
    "price": 0.5,
    "desc": "Komplet jednorazowych, ekologicznych sztućców drewnianych (widelec, nóż, serwetka) dla Twojej wygody."
  },
  {
    "id": 22,
    "name": "Kubek / Kaucja za butelkę",
    "price": 0.5,
    "desc": "Kaucja zwrotna za butelkę szklaną lub jednorazowy kubek do napojów na wynos."
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
    
    var cartListHtml = '<div style="margin:8px 0;padding:10px;background:#fff;border:2px solid #2D1A1E;border-radius:8px;box-shadow:2px 2px 0px #2D1A1E;font-size:0.85rem;color:#2D1A1E;">';
    cartListHtml += '<strong>Twój koszyk:</strong><br>';
    for (var i = 0; i < cart.length; i++) {
      var ci = cart[i];
      cartListHtml += '<div style="display:flex;justify-content:space-between;align-items:center;margin-top:6px;font-weight:500;">'
                   + '<span>' + ci.name + ' x' + ci.qty + ' (' + (ci.price * ci.qty) + ' zł)</span>'
                   + '<button onclick="window.jasBotRemove(' + ci.id + ')" '
                   + 'style="background:#D32F2F;color:#fff;border:1px solid #2D1A1E;border-radius:4px;padding:2px 6px;font-size:0.75rem;cursor:pointer;font-weight:bold;margin-left:8px;">'
                   + 'Usuń</button>'
                   + '</div>';
    }
    cartListHtml += '</div>';

    addMsg('Dodano: <strong>' + item.name + '</strong>.<br>'
         + cartListHtml
         + '<div style="margin-top:10px;display:flex;gap:8px;flex-wrap:wrap;">'
         + '<button onclick="window.jasBotCheckout()" '
         + 'style="background:#D32F2F;color:#fff;border:2px solid #2D1A1E;border-radius:6px;padding:6px 14px;cursor:pointer;font-weight:700;">'
         + 'ZŁÓŻ ZAMÓWIENIE ➔</button>'
         + '<button onclick="window.jasBotClearCart()" '
         + 'style="background:#fff;color:#555;border:2px solid #2D1A1E;border-radius:6px;padding:6px 14px;cursor:pointer;font-weight:700;">'
         + 'Wyczyść koszyk</button>'
         + '</div>'
         + '<small style="display:block;margin-top:6px;color:#555;">lub wybierz kolejne danie z MENU powyżej.</small>');
  };

  window.jasBotRemove = function(id) {
    for (var i = 0; i < cart.length; i++) {
      if (cart[i].id === id) {
        cart[i].qty--;
        if (cart[i].qty <= 0) {
          cart.splice(i, 1);
        }
        break;
      }
    }
    updateBadge();
    if (cart.length === 0) {
      addMsg('Twój koszyk jest teraz pusty. Wybierz potrawy z MENU powyżej!');
    } else {
      var cartListHtml = '<div style="margin:8px 0;padding:10px;background:#fff;border:2px solid #2D1A1E;border-radius:8px;box-shadow:2px 2px 0px #2D1A1E;font-size:0.85rem;color:#2D1A1E;">';
      cartListHtml += '<strong>Twój koszyk:</strong><br>';
      for (var i = 0; i < cart.length; i++) {
        var ci = cart[i];
        cartListHtml += '<div style="display:flex;justify-content:space-between;align-items:center;margin-top:6px;font-weight:500;">'
                     + '<span>' + ci.name + ' x' + ci.qty + ' (' + (ci.price * ci.qty) + ' zł)</span>'
                     + '<button onclick="window.jasBotRemove(' + ci.id + ')" '
                     + 'style="background:#D32F2F;color:#fff;border:1px solid #2D1A1E;border-radius:4px;padding:2px 6px;font-size:0.75rem;cursor:pointer;font-weight:bold;margin-left:8px;">'
                     + 'Usuń</button>'
                     + '</div>';
      }
      cartListHtml += '</div>';

      addMsg('Usunięto pozycję z koszyka.<br>'
           + cartListHtml
           + '<div style="margin-top:10px;display:flex;gap:8px;flex-wrap:wrap;">'
           + '<button onclick="window.jasBotCheckout()" '
           + 'style="background:#D32F2F;color:#fff;border:2px solid #2D1A1E;border-radius:6px;padding:6px 14px;cursor:pointer;font-weight:700;">'
           + 'ZŁÓŻ ZAMÓWIENIE ➔</button>'
           + '<button onclick="window.jasBotClearCart()" '
           + 'style="background:#fff;color:#555;border:2px solid #2D1A1E;border-radius:6px;padding:6px 14px;cursor:pointer;font-weight:700;">'
           + 'Wyczyść koszyk</button>'
           + '</div>'
           + '<small style="display:block;margin-top:6px;color:#555;">lub wybierz kolejne danie z MENU powyżej.</small>');
    }
  };

  window.jasBotClearCart = function() {
    cart = [];
    updateBadge();
    addMsg('Koszyk został wyczyszczony. Możesz wybrać potrawy na nowo z MENU powyżej! 🍗');
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
    pendingOrderId = 'JAS-' + Date.now().toString().slice(-6);
    step = 'awaiting_name';
    addMsg('<strong>Podsumowanie zamówienia:</strong><br><br>'
         + pendingOrderText.replace(/\n/g,'<br>')
         + '<br><strong>RAZEM: ' + pendingTotal + ' zł</strong>'
         + '<hr style="border:1px dashed #2D1A1E;margin:12px 0;">'
         + '<strong>Aby rozpocząć, proszę podać swoje Imię i Nazwisko:</strong>');
  };

  function handleName(text) {
    var rawName = text.trim();
    if (rawName.length < 2) {
      addMsg('Proszę podać prawidłowe imię i nazwisko (min. 2 znaki):');
      return;
    }
    pendingName = rawName;
    step = 'awaiting_phone';
    addMsg('Dziękujemy <strong>' + pendingName + '</strong>!<br><br>'
         + '<strong>Teraz proszę podać swój numer telefonu komórkowego:</strong><br><br>'
         + '<small>Użyjemy go do kontaktu w sprawie odbioru oraz automatycznej prośby o opinię.</small>');
  }

  function handlePhone(text) {
    var rawPhone = text.trim();
    if (!/^\+?[0-9\s-]{9,15}$/.test(rawPhone)) {
      addMsg('Wprowadzono niepoprawny numer telefonu. Podaj prawidłowy numer (np. 663970016):');
      return;
    }
    pendingPhone = rawPhone;
    step = 'awaiting_blik_ref';

    window.jasBotConfirmBlik = function() {
      handleBlikRef(pendingOrderId);
    };

    addMsg(`Dziękujemy! Twój numer telefonu to: <strong>` + pendingPhone + `</strong>.<br><br>
🎉 <strong>Twoje zamówienie zostało zarejestrowane pod unikalnym numerem: <span style="font-size:1.15rem;color:#D32F2F;font-weight:800;">` + pendingOrderId + `</span></strong><br><br>
Wpisz ten numer jako <strong>Tytuł przelewu BLIK</strong>, abyśmy mogli błyskawicznie połączyć wpłatę z Twoim zamówieniem!<br><br>
<strong>Teraz zapłać przez BLIK na telefon Marysi:</strong><br>
<div style="background:#FFF;border:3px solid #2D1A1E;border-radius:1rem;padding:15px;margin:12px 0;box-shadow:3px 3px 0px #2D1A1E;color:#2D1A1E;font-size:0.95rem;text-align:left;">
  <div style="margin-bottom:10px;display:flex;justify-content:space-between;align-items:center;flex-wrap:wrap;gap:8px;">
    <span>1. Numer telefonu BLIK:</span>
    <div style="display:flex;align-items:center;gap:6px;">
      <strong style="color:#D32F2F;font-size:1.1rem;letter-spacing:0.5px;">` + BLIK_PHONE + `</strong>
      <button onclick="var b = this; navigator.clipboard.writeText('663970016').then(function() { b.innerText = 'Skopiowano!'; setTimeout(function() { b.innerText = 'Skopiuj'; }, 2000); })"
              style="background:#FCC036;border:2px solid #2D1A1E;border-radius:6px;padding:3px 8px;font-size:0.75rem;font-weight:bold;cursor:pointer;font-family:inherit;box-shadow:1px 1px 0 #2D1A1E;">
        Skopiuj
      </button>
    </div>
  </div>
  <div style="margin-bottom:10px;display:flex;justify-content:space-between;align-items:center;flex-wrap:wrap;gap:8px;">
    <span>2. Kwota przelewu:</span>
    <strong style="font-size:1.1rem;color:#2D1A1E;">` + pendingTotal + ` zł</strong>
  </div>
  <div style="display:flex;justify-content:space-between;align-items:center;flex-wrap:wrap;gap:8px;">
    <span>3. Tytuł przelewu:</span>
    <div style="display:flex;align-items:center;gap:6px;">
      <strong style="color:#D32F2F;font-size:1.1rem;letter-spacing:0.5px;">` + pendingOrderId + `</strong>
      <button onclick="var b = this; navigator.clipboard.writeText('` + pendingOrderId + `').then(function() { b.innerText = 'Skopiowano!'; setTimeout(function() { b.innerText = 'Skopiuj'; }, 2000); })"
              style="background:#FCC036;border:2px solid #2D1A1E;border-radius:6px;padding:3px 8px;font-size:0.75rem;font-weight:bold;cursor:pointer;font-family:inherit;box-shadow:1px 1px 0 #2D1A1E;">
        Skopiuj
      </button>
    </div>
  </div>
</div>
<strong>Po wysłaniu przelewu w aplikacji bankowej kliknij przycisk poniżej, aby sfinalizować zamówienie:</strong>
<button onclick="window.jasBotConfirmBlik()"
        style="display:block;width:100%;margin-top:12px;background:#25D366;color:#fff;border:3px solid #2D1A1E;
        border-radius:10px;padding:12px;font-weight:800;font-size:1rem;font-family:inherit;cursor:pointer;
        box-shadow:3px 3px 0 #2D1A1E;transition:all 0.1s ease;text-transform:uppercase;">
  Potwierdzam wysłanie przelewu BLIK ➔
</button>
<div style="text-align:center;margin-top:8px;font-size:0.8rem;color:#666;">lub wpisz w czacie &quot;wysłane&quot;</div>`);
  }

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
    if (blikRef.toLowerCase() === 'wysłane' || blikRef.toLowerCase() === 'wyslane' || blikRef === '') {
      blikRef = pendingOrderId;
    }
    var orderId = pendingOrderId;

    // Trigger n8n Webhook
    var webhookUrl = 'https://n8n.jaison.pl/webhook/bar-jas-zamowienie';
    fetch(webhookUrl, {
      method: 'POST',
      headers: { 'Content-Type': 'application/json' },
      body: JSON.stringify({
        order_id: orderId,
        timestamp: new Date().toISOString(),
        client_name: pendingName,
        phone: pendingPhone,
        order_details: pendingOrderText,
        total_amount: pendingTotal
      })
    })
    .catch(function(e) { console.warn('[n8n Webhook Error]', e); });

    var waMsg = encodeURIComponent(
      'NOWE ZAMÓWIENIE (' + orderId + ') - Bar Jaś JaśBot\n'
      + '----------------------------\n'
      + pendingOrderText
      + '\nRAZEM: ' + pendingTotal + ' zł\n'
      + '----------------------------\n'
      + 'Blik Wysłany !\n'
      + 'Tytuł przelewu: ' + orderId + ' (Imię: ' + pendingName + ')\n'
      + 'Telefon klienta: ' + pendingPhone + '\n'
      + '(Proszę sprawdzić w aplikacji bankowej)\n'
      + '----------------------------\n'
      + 'Odbiór: ul. Rokicińska 190/214, Łódź (przy wejściu do Selgrosa)\n'
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
    pendingPhone = '';
    pendingName = '';
    pendingOrderId = '';
  }

  let chatHistory = [];
  try {
    var stored = localStorage.getItem('jasbot_history');
    if (stored) {
      chatHistory = JSON.parse(stored);
    }
  } catch (e) {
    console.warn('[JaśBot] LocalStorage load failed', e);
  }

  function saveHistory() {
    try {
      localStorage.setItem('jasbot_history', JSON.stringify(chatHistory));
    } catch (e) {
      console.warn('[JaśBot] LocalStorage save failed', e);
    }
  }

  function sendMsg() {
    var text = input.value.trim();
    if (!text) return;
    addMsg(text, 'user');
    input.value = '';
    if (step === 'awaiting_name') { handleName(text); return; }
    if (step === 'awaiting_phone') { handlePhone(text); return; }
    if (step === 'awaiting_blik_ref') { handleBlikRef(text); return; }
    
    // Quick local rule matching to remain responsive and save API quota
    var lower = text.toLowerCase();
    if (lower === 'menu' || lower === 'dania' || lower === 'cennik') {
      showMenu();
      chatHistory.push({role: 'user', text: text});
      chatHistory.push({role: 'model', text: '[Wyświetlono interaktywne menu]'});
      saveHistory();
      return;
    } else if (lower === 'godziny' || lower === 'otwarte' || lower === 'kiedy') {
      addMsg('Jesteśmy otwarci:<br><strong>Pon-Sob: 09:00-19:00</strong><br>Niedziela: nieczynne');
      chatHistory.push({role: 'user', text: text});
      chatHistory.push({role: 'model', text: 'Jesteśmy otwarci: Pon-Sob: 09:00-19:00, Niedziela: nieczynne'});
      saveHistory();
      return;
    } else if (lower === 'adres' || lower === 'dojazd' || lower === 'lokalizacja') {
      addMsg('Znajdziesz nas pod adresem:<br><strong>ul. Rokicińska 190/214, Łódź</strong><br>(na parkingu, tuż przy wejściu do Selgrosa)');
      chatHistory.push({role: 'user', text: text});
      chatHistory.push({role: 'model', text: 'Znajdziesz nas pod adresem: ul. Rokicińska 190/214, Łódź (na parkingu, tuż przy wejściu do Selgrosa)'});
      saveHistory();
      return;
    } else if (lower === 'blik' || lower === 'płatność') {
      addMsg('Przyjmujemy płatność przez <strong>BLIK na numer telefonu</strong>: <strong>' + BLIK_PHONE + '</strong><br>Wybierz dania z menu, a JaśBot przeprowadzi Cie przez płatność krok po kroku!');
      chatHistory.push({role: 'user', text: text});
      chatHistory.push({role: 'model', text: 'Przyjmujemy płatność przez BLIK na numer telefonu: ' + BLIK_PHONE});
      saveHistory();
      return;
    }

    // Call server PHP proxy for general conversation
    // 1. Create a thinking indicator div
    var thinkingDiv = document.createElement('div');
    thinkingDiv.className = 'jasbot-msg bot';
    thinkingDiv.innerHTML = '<span class="thinking-dot">.</span><span class="thinking-dot">.</span><span class="thinking-dot">.</span> 🍗';
    thinkingDiv.style.fontStyle = 'italic';
    thinkingDiv.style.color = '#777';
    messages.appendChild(thinkingDiv);
    messages.scrollTop = messages.scrollHeight;

    // 2. Prepare history (last 10 messages)
    if (chatHistory.length > 10) {
      chatHistory = chatHistory.slice(-10);
    }

    // 3. Make fetch request
    fetch('/gemini_proxy.php', {
      method: 'POST',
      headers: {
        'Content-Type': 'application/json'
      },
      body: JSON.stringify({
        message: text,
        history: chatHistory
      })
    })
    .then(function(res) { return res.json(); })
    .then(function(data) {
      // remove thinking indicator
      if (thinkingDiv && thinkingDiv.parentNode) {
        thinkingDiv.parentNode.removeChild(thinkingDiv);
      }
      
      var reply = data.response || 'Przepraszam, coś mnie rozproszyło. Możesz powtórzyć? 🍗';
      addMsg(reply);
      
      // Save to chat history
      chatHistory.push({role: 'user', text: text});
      // strip html for clean context history
      var cleanReply = reply.replace(/<[^>]*>/g, '');
      chatHistory.push({role: 'model', text: cleanReply});
      saveHistory();
      
      // Log hidden debug errors in console ONLY (for Tomasz / developers)
      if (data.debug_error) {
        console.warn('[JaśBot Debug]', data.debug_error);
      }
    })
    .catch(function(err) {
      if (thinkingDiv && thinkingDiv.parentNode) {
        thinkingDiv.parentNode.removeChild(thinkingDiv);
      }
      console.error('[JaśBot Connection Error]', err);
      addMsg('Przepraszam, chwilowo mam trudności z połączeniem. Wpisz <strong>menu</strong>, aby zobaczyć nasze dania!');
    });
  }

  toggleBtn.addEventListener('click', function() {
    windowEl.classList.toggle('open');
    var labelEl = document.getElementById('jasbot-label');
    if (windowEl.classList.contains('open')) {
      if (labelEl) labelEl.style.display = 'none';
      if (messages.children.length === 0) {
        if (chatHistory.length > 0) {
          addMsg('<em>Witamy ponownie! Poniżej znajduje się historia Twojej rozmowy z JaśBotem:</em> 🍗');
          for (var idx = 0; idx < chatHistory.length; idx++) {
            var msg = chatHistory[idx];
            if (msg.text !== '[Wyświetlono interaktywne menu]') {
              addMsg(msg.text, msg.role === 'user' ? 'user' : 'bot');
            } else {
              showMenu();
            }
          }
        } else {
          addMsg('Cześć! Jestem <strong>JaśBot</strong> - wirtualny asystent Baru Jaś! 🍗<br><br>'
               + 'Oto nasze pełne, pyszne menu. Kliknij wybrane pozycje, aby dodać je do koszyka i szybko złożyć zamówienie:<br>'
               + 'Płatność wygodnie przez <strong>BLIK na telefon</strong>.');
          showMenu();
        }
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
