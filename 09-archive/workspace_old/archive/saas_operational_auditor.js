/**
 * Holistic SaaS Operational Architecture Auditor v2.0
 * ----------------------------------------------------
 * Narzędzie deweloperskie (F12 Console) stworzone specjalnie dla Holistic Jasona.
 * Służy do natychmiastowego prześwietlania platform funkcjonalnych (SaaS) takich jak:
 * deal.ai, Localo, Supercool, Systeme.io i innych.
 * 
 * Ekstrahuje:
 * 1. Strukturę nawigacji i moduły operacyjne (Sidebar/Menus)
 * 2. Silniki AI, Prompt-boxy i Selektory Modeli (GPT, Claude, Gemini, systemy promptów)
 * 3. Zintegrowane usługi zewnętrzne (Google Maps/GBP, Stripe, Webhooki, API)
 * 4. Logikę formularzy i narzędzi (inputy, konfiguratory, opcje wyboru)
 * 5. Limity i limity użycia (kredyty, tokeny, pakiety)
 * 
 * Wynikiem działania jest pobranie pliku .JSON i .MD z kompletną specyfikacją architektury SaaS.
 */

(async function runSaaSOperationalAudit() {
  console.clear();
  console.log("%c🧠 HOLISTIC SAAS OPERATIONAL AUDITOR v2.0", "color: #8b5cf6; font-size: 18px; font-weight: bold;");
  console.log("%cPrześwietlam architekturę, integracje, silniki AI oraz logikę interfejsu... Czekaj...", "color: #94a3b8; font-size: 12px;");

  const domain = window.location.hostname;
  const path = window.location.pathname;
  const pageTitle = document.title || "Panel SaaS";
  const scannedAt = new Date().toISOString();

  // Pomocnicze oczyszczanie tekstu
  function clean(str) {
    return (str || '').replace(/\s+/g, ' ').trim();
  }

  // Funkcja penetrująca Shadow DOM
  function querySelectorAllShadow(selector, root = document) {
    let elements = Array.from(root.querySelectorAll(selector));
    const findShadows = (node) => {
      if (node && node.shadowRoot) {
        elements = elements.concat(Array.from(node.shadowRoot.querySelectorAll(selector)));
        findShadows(node.shadowRoot);
      }
      if (node && node.childNodes) {
        node.childNodes.forEach(child => findShadows(child));
      }
    };
    findShadows(root);
    return elements;
  }

  // 1. SKANOWANIE STRUKTURY MENU I NAWIGACJI (Główne Moduły Operacyjne)
  console.log("%c📁 Skanowanie modułów nawigacji...", "color: #3b82f6; font-weight: bold;");
  const navigation = [];
  const seenUrls = new Set();

  const navElements = querySelectorAllShadow('nav a, aside a, [class*="sidebar"] a, [class*="menu"] a, header a, [role="menuitem"]');
  navElements.forEach(a => {
    const url = a.href || a.getAttribute('data-href') || '';
    const text = clean(a.innerText || a.title || a.getAttribute('aria-label') || '');
    if (!text || seenUrls.has(url || text)) return;
    
    const hasIcon = !!(a.querySelector('svg') || a.querySelector('img') || a.querySelector('i') || a.querySelector('[class*="icon"]'));
    seenUrls.add(url || text);
    navigation.push({ text, url, hasIcon });
  });

  // Fallback dla luźnych linków, które wyglądają jak punkty nawigacyjne
  if (navigation.length === 0) {
    querySelectorAllShadow('a').forEach(a => {
      const url = a.href || '';
      const text = clean(a.innerText || '');
      if (text.length > 0 && text.length < 40 && !seenUrls.has(url) && (url.includes(domain) || url.startsWith('/'))) {
        seenUrls.add(url);
        navigation.push({ text, url, hasIcon: false });
      }
    });
  }

  // 2. DETEKCJA SILNIKÓW AI I SELEKTORÓW MODELI
  console.log("%c🤖 Skanowanie elementów sztucznej inteligencji (AI)...", "color: #8b5cf6; font-weight: bold;");
  const aiElements = [];
  const aiKeywords = /gpt|claude|gemini|llama|openai|anthropic|prompt|temperature|tokens|creative|generate|tłumacz|pisz|asystent|ai\s*model|sztuczn/i;

  // Skanuj tagi select i dropdowny pod kątem nazw modeli
  querySelectorAllShadow('select, [class*="select"], [class*="dropdown"]').forEach(el => {
    const txt = clean(el.innerText || '');
    if (aiKeywords.test(txt)) {
      aiElements.push({
        type: "Model/Prompt Selector",
        text: txt.substring(0, 200),
        htmlTag: el.tagName.toLowerCase(),
        classes: el.className || ''
      });
    }
  });

  // Skanuj pola tekstowe (Prompt Boxes)
  querySelectorAllShadow('textarea, [contenteditable="true"]').forEach(el => {
    const placeholder = el.getAttribute('placeholder') || '';
    const label = el.getAttribute('aria-label') || '';
    if (aiKeywords.test(placeholder) || aiKeywords.test(label) || /prompt|opisz|wpisz|generuj/i.test(placeholder)) {
      aiElements.push({
        type: "AI Prompt Input Field",
        placeholder: placeholder,
        label: label,
        htmlTag: el.tagName.toLowerCase()
      });
    }
  });

  // Przycisk "Generuj" lub "Uruchom AI"
  querySelectorAllShadow('button, input[type="submit"], [class*="btn"], [class*="button"]').forEach(btn => {
    const txt = clean(btn.innerText || btn.value || '');
    if (aiKeywords.test(txt) || /generuj|generate|twórz|stwórz|write|pisz|run/i.test(txt)) {
      if (txt.length < 50) {
        aiElements.push({
          type: "AI Action Trigger Button",
          text: txt,
          htmlTag: btn.tagName.toLowerCase()
        });
      }
    }
  });

  // 3. DETEKCJA INTEGRACJI I USŁUG ZEWNĘTRZNYCH (GBP, Stripe, Webhooki, API)
  console.log("%c🔌 Skanowanie integracji API i usług zewnętrznych...", "color: #10b981; font-weight: bold;");
  const integrations = [];
  const integrationKeywords = /stripe|paypal|google\s*maps|google\s*business|gbp|zapier|make\.com|make|webhook|api\s*key|klucz\s*api|shopify|facebook|meta|instagram|linkedin|tiktok|mailchimp|activecampaign|connect|połącz|integracj/i;

  querySelectorAllShadow('*').forEach(el => {
    if (el.children.length > 3) return; // tylko końcowe liście DOM
    const text = clean(el.innerText || '');
    const title = el.getAttribute('title') || '';
    const src = el.getAttribute('src') || '';
    
    let matchedKeyword = '';
    if (integrationKeywords.test(text)) matchedKeyword = text.match(integrationKeywords)[0];
    else if (integrationKeywords.test(title)) matchedKeyword = title.match(integrationKeywords)[0];
    else if (integrationKeywords.test(src)) matchedKeyword = src.match(integrationKeywords)[0];

    if (matchedKeyword) {
      const type = src ? "Zewnętrzny Skrypt/Zasób" : "Tekst/Opcja w Panelu";
      const preview = text || title || src;
      if (preview.length < 150) {
        integrations.push({
          detectedService: matchedKeyword.toUpperCase(),
          type: type,
          preview: preview.substring(0, 100),
          classes: el.className || ''
        });
      }
    }
  });

  // Usunięcie duplikatów z integracji
  const uniqueIntegrations = Array.from(new Map(integrations.map(item => [item.preview + item.detectedService, item])).values());

  // 4. ANALIZA STRUKTURY FORMULARZY I NARZĘDZI (Konfiguratory, Filtry)
  console.log("%c⚡ Skanowanie interaktywnych konfiguratorów i pól formularzy...", "color: #eab308; font-weight: bold;");
  const forms = [];
  
  querySelectorAllShadow('form, [class*="form"], [class*="editor-container"], [class*="configurator"]').forEach((f, formIdx) => {
    const inputs = [];
    f.querySelectorAll('input, select, textarea').forEach(inp => {
      const type = inp.type || inp.tagName.toLowerCase();
      const placeholder = inp.placeholder || '';
      const name = inp.name || inp.id || '';
      
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

    const actions = [];
    f.querySelectorAll('button, input[type="submit"]').forEach(btn => {
      const btnText = clean(btn.innerText || btn.value || '');
      if (btnText && btnText.length < 40) actions.push(btnText);
    });

    if (inputs.length > 0) {
      forms.push({
        id: formIdx + 1,
        containerClass: f.className || '',
        inputs: inputs.slice(0, 15),
        actions: [...new Set(actions)]
      });
    }
  });

  // 5. LIMITY, PAKIETY I KREDYTY (Quota Watcher)
  console.log("%c📊 Skanowanie limitów konta i kredytów...", "color: #ec4899; font-weight: bold;");
  const quotas = [];
  const quotaKeywords = /credit|kredyt|token|limit|użycie|usage|quota|pakiet|plan|premium|upgrade|words|słów|subskrypcj/i;

  querySelectorAllShadow('*').forEach(el => {
    if (el.children.length > 2) return; // liście DOM
    const txt = clean(el.innerText || '');
    if (quotaKeywords.test(txt) && /\d+/.test(txt)) {
      if (txt.length < 120) {
        quotas.push(txt);
      }
    }
  });

  const uniqueQuotas = [...new Set(quotas)];

  // BUDOWANIE SPECYFIKACJI KOŃCOWEJ
  const spec = {
    metadata: {
      domain,
      path,
      pageTitle,
      scannedAt,
      engine: "Holistic SaaS Operational Auditor v2.0"
    },
    navigation,
    aiFeatures: aiElements,
    apiIntegrations: uniqueIntegrations,
    functionalTools: forms,
    quotaUsage: uniqueQuotas
  };

  // GENEROWANIE DOKUMENTACJI W MARKDOWN
  const mdContent = `# Specyfikacja Funkcjonalna SaaS: ${domain}
Automatyczny audyt techniczno-operacyjny panelu aplikacji funkcjonalnej.

## 📑 Metadane Skanu
- **Domena Panelu:** \`${domain}\`
- **Aktualna Ścieżka:** \`${path}\`
- **Tytuł Podstrony:** \`${pageTitle}\`
- **Data Audytu:** \`${scannedAt}\`
- **Skaner:** \`Holistic SaaS Operational Auditor v2.0\`

---

## 📁 1. Główne Moduły Operacyjne (Nawigacja i Sidebar)
Struktura podstron i klocków funkcjonalnych, z których składa się platforma:

| Moduł | Adres URL / Ścieżka | Typ Menu |
| :--- | :--- | :---: |
${spec.navigation.map(l => `| **${l.text}** | \`${l.url}\` | ${l.hasIcon ? '⭐ Główny moduł' : '🔗 Link pomocniczy'} |`).join('\n')}

---

## 🤖 2. Wykryte Moduły Sztucznej Inteligencji (AI & LLM Integration)
Sposób integracji sztucznej inteligencji, silników LLM i struktury promptowania w interfejsie użytkownika:

${spec.aiFeatures.length === 0 ? '*Nie wykryto bezpośrednich selektorów modeli ani prompt-boxów na tej stronie.*' : spec.aiFeatures.map(ai => `
### • Typ Elementu: **${ai.type}**
- **Identyfikacja tagu:** \`<${ai.htmlTag}>\`
- **Wartość / Tekst:** 
  > ${ai.text || ai.placeholder || ai.label || 'brak etykiety'}
- **Klasy CSS:** \`${ai.classes || 'brak'}\`
`).join('\n')}

---

## 🔌 3. Zintegrowane Usługi Zewnętrzne i API (GBP, Google, Payments, Automations)
Połączenia i mechanizmy synchronizacji danych z zewnętrznymi ekosystemami wykryte w kodzie i interfejsie:

${spec.apiIntegrations.length === 0 ? '*Brak wykrytych znaczników integracji (Stripe, Zapier, Webhooki, GBP) na tej podstronie.*' : spec.apiIntegrations.map(int => `
- **Wykryta Usługa:** **\`${int.detectedService}\`**
  - **Typ osadzenia:** ${int.type}
  - **Podgląd elementu:** \`${int.preview}\`
`).join('\n')}

---

## 📝 4. Interaktywne Formularze, Narzędzia i Konfiguratory
Główne panele, za pomocą których użytkownik wchodzi w interakcję z systemem (pola wejściowe, kreatory):

${spec.functionalTools.length === 0 ? '*Brak standardowych formularzy konfiguracyjnych na tej podstronie.*' : spec.functionalTools.map(f => `
### 🛠️ Panel Funkcjonalny #${f.id}
- **Klasa kontenera:** \`${f.containerClass}\`
- **Elementy wejściowe (Inputy/Ustawienia):**
${f.inputs.map(i => `  - **[${i.type.toUpperCase()}]** Etykieta: \`${i.label || 'brak'}\` | Nazwa: \`${i.name || 'brak'}\` | Podpowiedź: *"${i.placeholder}"*`).join('\n')}
- **Przyciski Wykonawcze / Akcje:** ${f.actions.map(a => `\`${a}\``).join(', ') || '*Brak dedykowanych przycisków*'}
`).join('\n')}

---

## 📊 5. Wykryte Limity, Kredyty i Informacje o Pakiecie (Quota Spec)
Aktualne ograniczenia taryfowe i dane o zużyciu zasobów (tokeny, kredyty, plany):

${spec.quotaUsage.length === 0 ? '*Brak danych o kredytach i limitach na tym widoku.*' : spec.quotaUsage.map(q => `- **Wykryty wskaźnik:** \`${q}\``).join('\n')}

---
*Dokumentacja techniczna wygenerowana przez Holistic Platform System Architect.*
`;

  // Pobieranie plików
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

  const filePrefix = `Holistic_SaaS_Architecture_${domain.replace(/[^a-z0-9]/gi, '_').toLowerCase()}`;
  downloadFile(mdContent, `${filePrefix}.md`, 'text/markdown');
  downloadFile(JSON.stringify(spec, null, 2), `${filePrefix}.json`, 'application/json');

  console.log(`\n%c🎉 AUDYT UKOŃCZONY POMYŚLNIE!`, "color: #10b981; font-weight: bold; font-size: 14px;");
  console.log(`Pobrano pliki:\n1. ${filePrefix}.md (Dla oka i dokumentacji)\n2. ${filePrefix}.json (Surowa struktura dla Agenta)`);
  console.log("%cMożesz teraz przeciągnąć pliki do naszego czatu, a ja natychmiast zsyntetyzuję układ dashboardu, logikę integracji i procesy biznesowe tej platformy dla Twojego Holistic CEO!", "color: #38bdf8; font-weight: bold;");
})();
