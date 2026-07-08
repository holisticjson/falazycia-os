/**
 * Holistic Universal Dashboard & Layout Analyzer v1.0
 * --------------------------------------------------
 * Paste this script directly into your browser console (F12) on any page
 * (GHL University, Deal.ai, Localo, Supercool, etc.) to immediately audit,
 * dissect, and extract its entire layout structure, menus, cards, forms, and features!
 * 
 * It will output a gorgeous hierarchy to the console and auto-download
 * a highly detailed Markdown and JSON specification.
 */

(async function runUniversalAudit() {
  console.clear();
  console.log("%c🚀 HOLISTIC DASHBOARD ANALYZER v1.0", "color: #3b82f6; font-size: 20px; font-weight: bold;");
  console.log("%cInicjalizacja skanowania struktury, logiki i funkcji... Czekaj na zakończenie...", "color: #a1a1aa; font-size: 13px;");

  const domain = window.location.hostname;
  const path = window.location.pathname;
  const pageTitle = document.title || "Dashboard";
  
  // 1. Pomocnicze funkcje ekstrakcji
  function clean(str) {
    return (str || '').replace(/\s+/g, ' ').trim();
  }

  function getElementXPath(element) {
    if (element.id) return `//*[@id="${element.id}"]`;
    if (element === document.body) return '/html/body';
    let ix = 0;
    let siblings = element.parentNode ? element.parentNode.childNodes : [];
    for (let i = 0; i < siblings.length; i++) {
      let sibling = siblings[i];
      if (sibling === element) return getElementXPath(element.parentNode) + '/' + element.tagName.toLowerCase() + '[' + (ix + 1) + ']';
      if (sibling.nodeType === 1 && sibling.tagName === element.tagName) ix++;
    }
    return '';
  }

  // 2. Skanowanie nawigacji (Sidebar / Menus)
  console.log("📁 %cSkanowanie elementów nawigacji i menu...", "color: #60a5fa; font-weight: bold;");
  const navLinks = [];
  const seenUrls = new Set();
  
  // Szukamy elementów typu nav, sidebar, menu lub wszystkich linków z ikonami/krótkim tekstem
  document.querySelectorAll('nav a, aside a, [class*="sidebar"] a, [class*="menu"] a, header a').forEach(a => {
    const url = a.href;
    const text = clean(a.innerText || a.title || a.getAttribute('aria-label') || '');
    if (!text || seenUrls.has(url)) return;
    
    // Sprawdź czy link ma ikonę (SVG lub img lub i)
    const hasIcon = !!(a.querySelector('svg') || a.querySelector('img') || a.querySelector('i') || a.querySelector('[class*="icon"]'));
    seenUrls.add(url);
    navLinks.push({ text, url, hasIcon });
  });

  // Jeśli powyższe nie dało wyników, zgarnij wszystkie linki z nagłówkiem/stopką
  if (navLinks.length === 0) {
    document.querySelectorAll('a').forEach(a => {
      const url = a.href;
      const text = clean(a.innerText || '');
      if (text.length > 0 && text.length < 50 && !seenUrls.has(url) && (url.includes(domain) || url.startsWith('/'))) {
        seenUrls.add(url);
        navLinks.push({ text, url, hasIcon: false });
      }
    });
  }

  // 3. Skanowanie modułów i kart (Dashboard Cards)
  console.log("📦 %cSkanowanie widżetów, statystyk i sekcji...", "color: #34d399; font-weight: bold;");
  const cards = [];
  document.querySelectorAll('[class*="card"], [class*="widget"], [class*="block"], [class*="panel"], [class*="box"], section, article').forEach((el, index) => {
    // Odfiltruj małe lub całe body
    if (el.clientWidth < 100 || el.clientHeight < 50 || el === document.body) return;
    
    // Tytuł karty
    const headerEl = el.querySelector('h1, h2, h3, h4, h5, h6, [class*="header"], [class*="title"]');
    const title = headerEl ? clean(headerEl.innerText) : '';
    
    // Teksty i wartości (np. "2,450 PLN", "+15%")
    const rawText = clean(el.innerText);
    if (!rawText || rawText.length < 5 || rawText.length > 1000) return;
    
    // Szukamy przycisków/akcji wewnątrz karty
    const buttons = [];
    el.querySelectorAll('button, a').forEach(btn => {
      const btnText = clean(btn.innerText || btn.title || btn.getAttribute('aria-label') || '');
      if (btnText) buttons.push(btnText);
    });

    cards.push({
      id: index + 1,
      title: title || `Karta ${index + 1}`,
      xpath: getElementXPath(el),
      textPreview: rawText.substring(0, 150) + (rawText.length > 150 ? '...' : ''),
      buttons: [...new Set(buttons)].slice(0, 5)
    });
  });

  // 4. Skanowanie formularzy, pól wejściowych i przycisków akcji
  console.log("⚡ %cSkanowanie interaktywnych formularzy i funkcji...", "color: #fbbf24; font-weight: bold;");
  const forms = [];
  document.querySelectorAll('form, [class*="form"]').forEach((f, formIdx) => {
    const inputs = [];
    f.querySelectorAll('input, select, textarea').forEach(inp => {
      const type = inp.type || inp.tagName.toLowerCase();
      const placeholder = inp.placeholder || '';
      const name = inp.name || inp.id || '';
      // Znajdź powiązaną etykietę (label)
      let labelText = '';
      if (inp.id) {
        const lbl = document.querySelector(`label[for="${inp.id}"]`);
        if (lbl) labelText = clean(lbl.innerText);
      }
      if (!labelText) {
        const parentLabel = inp.closest('label');
        if (parentLabel) labelText = clean(parentLabel.innerText);
      }
      inputs.push({ type, name, placeholder, label: labelText });
    });

    const submitBtns = [];
    f.querySelectorAll('button, input[type="submit"]').forEach(btn => {
      const btnText = clean(btn.innerText || btn.value || '');
      if (btnText) submitBtns.push(btnText);
    });

    if (inputs.length > 0) {
      forms.push({
        id: formIdx + 1,
        inputs,
        actions: submitBtns
      });
    }
  });

  // Zbieranie wszystkich luźnych przycisków na stronie (akcje globalne)
  const globalActions = [];
  document.querySelectorAll('button').forEach(btn => {
    const txt = clean(btn.innerText || btn.title || btn.getAttribute('aria-label') || '');
    if (txt && txt.length < 40 && !globalActions.includes(txt)) {
      globalActions.push(txt);
    }
  });

  // 5. Budowanie raportu końcowego
  const results = {
    metadata: {
      domain,
      path,
      pageTitle,
      scannedAt: new Date().toISOString(),
      userAgent: navigator.userAgent
    },
    navigation: navLinks,
    dashboardCards: cards.slice(0, 30), // limit do 30 dla czytelności
    interactiveForms: forms,
    globalButtons: globalActions.slice(0, 20)
  };

  // Generowanie ładnego widoku w konsoli
  console.log("%c\n📊 WYNIKI SKANOWANIA STRUKTURY:", "color: #10b981; font-size: 16px; font-weight: bold;");
  console.log(`🌐 Domena: ${domain}`);
  console.log(`📃 Tytuł: ${pageTitle}`);
  
  console.log(`\n%c📌 LINKI NAWIGACJI (${results.navigation.length}):`, "color: #60a5fa; font-weight: bold;");
  results.navigation.forEach(l => {
    console.log(`   [${l.hasIcon ? '⭐ Menu' : '🔗 Link'}] ${l.text} -> ${l.url}`);
  });

  console.log(`\n%c📌 KARTY/BLOKI DANYCH (${results.dashboardCards.length}):`, "color: #34d399; font-weight: bold;");
  results.dashboardCards.forEach(c => {
    console.log(`   📦 ${c.title} \n      Podgląd: "${c.textPreview}"\n      Akcje: ${c.buttons.join(', ') || 'brak'}`);
  });

  console.log(`\n%c📌 FORMULARZE & INPUTY (${results.interactiveForms.length}):`, "color: #fbbf24; font-weight: bold;");
  results.interactiveForms.forEach(f => {
    console.log(`   📝 Formularz #${f.id}:`);
    f.inputs.forEach(i => console.log(`      └─ [${i.type}] "${i.label}" (placeholder: "${i.placeholder}")`));
    console.log(`      └─ Akcje wysłania: ${f.actions.join(', ') || 'domyślny submit'}`);
  });

  // Pobieranie jako plik Markdown (.md)
  const mdContent = `# Analiza Struktury Dashboardu: ${domain}
Zeskanowano automatycznie przy użyciu **Holistic Dashboard Analyzer**.

## 📑 Informacje ogólne
- **Domena:** \`${domain}\`
- **Ścieżka:** \`${path}\`
- **Tytuł Strony:** \`${pageTitle}\`
- **Data skanowania:** \`${results.metadata.scannedAt}\`

---

## 🧭 Menu Nawigacyjne i Funkcje Panelu (${results.navigation.length})
Te linki definiują główne moduły funkcjonalne systemu:

| Moduł / Menu | Adres URL | Posiada ikonę? |
| :--- | :--- | :---: |
${results.navigation.map(l => `| **${l.text}** | \`${l.url}\` | ${l.hasIcon ? '✅ Tak' : '❌ Nie'} |`).join('\n')}

---

## 📊 Elementy Wizualne, Karty i Statystyki (${results.dashboardCards.length})
Układy graficzne, podsumowania i moduły informacyjne wykryte na stronie głównej:

${results.dashboardCards.map(c => `
### 📦 ${c.title}
- **XPath:** \`${c.xpath}\`
- **Zawartość tekstowa:** 
  > ${c.textPreview}
- **Akcje/Przyciski wewnątrz karty:** ${c.buttons.map(b => `\`${b}\``).join(', ') || '*Brak wykrytych przycisków*'}
`).join('\n')}

---

## 📝 Formularze i Pola Wprowadzania Danych (${results.interactiveForms.length})
Wykryte panele konfiguracyjne, kreatory i formularze ustawień:

${results.interactiveForms.map(f => `
### 📝 Formularz #${f.id}
- **Pola wejściowe:**
${f.inputs.map(i => `  - **[${i.type.toUpperCase()}]** Etykieta: \`${i.label || 'brak'}\` | Nazwa: \`${i.name || 'brak'}\` | Podpowiedź: *"${i.placeholder}"*`).join('\n')}
- **Wykryte przyciski wykonawcze:** ${f.actions.map(a => `\`${a}\``).join(', ') || '*Brak dedykowanych przycisków*'}
`).join('\n')}

---

## ⚡ Globalne Przyciski Akcji na Stronie
Wszystkie luźne interakcje sterujące panelem:
${results.globalButtons.map(b => `- \`${b}\``).join('\n')}

---
*Wygenerowano za pomocą Holistic Platform System Architect.*
`;

  // Funkcja download
  function downloadFile(content, filename, type) {
    const blob = new Blob([content], { type: type });
    const url = URL.createObjectURL(blob);
    const a = document.createElement('a');
    a.href = url;
    a.download = filename;
    document.body.appendChild(a);
    a.click();
    document.body.removeChild(a);
    URL.revokeObjectURL(url);
  }

  // Pobierz oba pliki: Markdown dla oka i JSON dla LLM
  const filePrefix = `Holistic_Structure_${domain.replace(/[^a-z0-9]/gi, '_').toLowerCase()}`;
  downloadFile(mdContent, `${filePrefix}.md`, 'text/markdown');
  downloadFile(JSON.stringify(results, null, 2), `${filePrefix}.json`, 'application/json');

  console.log(`\n%c🎉 GOTOOWE! Pliki struktury ${filePrefix}.md oraz .json zostały pobrane na Twój dysk!`, "color: #10b981; font-size: 14px; font-weight: bold;");
  console.log("%cMożesz teraz przeciągnąć plik .json do naszego czatu, a ja natychmiast zsyntetyzuję logikę działania i funkcje tego dashboardu!", "color: #38bdf8; font-size: 12px;");
})();
