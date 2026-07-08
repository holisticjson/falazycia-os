/**
 * GHL Library-v2 Course Card Extractor v2.1
 * ----------------------------------------
 * Specifically designed to parse the GoHighLevel membership catalog.
 * Uses 6-level advanced fallback mechanisms (including React Fiber auditing and UUID sniffing)
 * to extract course URLs even if they are dynamically rendered clickable DIVs without <a> tags!
 * 
 * Extracts: Course Title, Progress, Author, Status, and URL!
 * Downloads a complete structured JSON file.
 */

(function runGHLExtractor() {
  console.clear();
  console.log("%c🎓 GHL LIBRARY COURSE EXTRACTOR v2.1 (PRO)", "color: #10b981; font-size: 16px; font-weight: bold;");

  const productList = document.querySelector('#product-list');
  if (!productList) {
    console.error("❌ Błąd: Nie znaleziono kontenera '#product-list' na tej stronie! Upewnij się, że jesteś zalogowany pod adresem university.gohighlevel.com/library-v2");
    return;
  }

  const cards = Array.from(productList.children);
  const courses = [];
  const uuidRegex = /[0-9a-f]{8}-[0-9a-f]{4}-[0-9a-f]{4}-[0-9a-f]{4}-[0-9a-f]{12}/i;

  function findGhlProductUrl(card) {
    // Metoda 1: Szukaj standardowego <a> wewnątrz karty zawierającego produkty/courses
    let a = card.querySelector('a[href*="/products/"], a[href*="/courses/"], a[href*="/library-v2/"]');
    if (a && a.href && !a.href.endsWith('/library-v2')) return a.href;

    // Metoda 2: Sprawdź czy sama karta jest tagiem <a>
    if (card.tagName.toLowerCase() === 'a' && card.href) return card.href;

    // Metoda 3: Przeszukaj wszystkie atrybuty karty w poszukiwaniu UUID
    for (let attr of card.attributes) {
      if (uuidRegex.test(attr.value)) {
        const match = attr.value.match(uuidRegex);
        return `https://university.gohighlevel.com/products/${match[0]}?source=courses`;
      }
    }

    // Metoda 4: Przeszukaj atrybuty wszystkich elementów podrzędnych w poszukiwaniu UUID
    let allElements = card.querySelectorAll('*');
    for (let el of allElements) {
      for (let attr of el.attributes) {
        if (uuidRegex.test(attr.value)) {
          const match = attr.value.match(uuidRegex);
          return `https://university.gohighlevel.com/products/${match[0]}?source=courses`;
        }
      }
    }

    // Metoda 5: Zaawansowane przeszukiwanie właściwości React Fiber (Props/State w pamięci DOM)
    try {
      const reactKey = Object.keys(card).find(k => k.startsWith('__reactFiber') || k.startsWith('__reactProps'));
      if (reactKey) {
        const fiber = card[reactKey];
        let foundUuid = null;
        function searchObj(obj, depth = 0) {
          if (!obj || depth > 10 || foundUuid) return;
          if (typeof obj === 'string' && uuidRegex.test(obj)) {
            const match = obj.match(uuidRegex);
            foundUuid = match[0];
            return;
          }
          if (typeof obj === 'object') {
            for (let k in obj) {
              if (k === 'id' || k === 'productId' || k === 'uuid' || k === 'product') {
                if (typeof obj[k] === 'string' && uuidRegex.test(obj[k])) {
                  foundUuid = obj[k].match(uuidRegex)[0];
                  return;
                }
              }
              try {
                searchObj(obj[k], depth + 1);
              } catch(e) {}
            }
          }
        }
        searchObj(fiber);
        if (foundUuid) {
          return `https://university.gohighlevel.com/products/${foundUuid}?source=courses`;
        }
      }
    } catch(e) {}

    // Metoda 6: Sprawdź czy w tekście całej karty nie ma jakiegoś linku
    const textLinks = Array.from(card.querySelectorAll('a')).map(el => el.href).filter(Boolean);
    if (textLinks.length > 0) return textLinks[0];

    return "";
  }

  cards.forEach((card, idx) => {
    // 1. Wyciąganie tytułu
    const titleEl = card.querySelector('h1, h2, h3, h4, [class*="title"], [class*="name"]');
    let title = titleEl ? titleEl.innerText.trim() : "";
    if (!title) {
      const textNodes = card.innerText.split('\n').map(t => t.trim()).filter(Boolean);
      title = textNodes[0] || `Kurs #${idx + 1}`;
    }

    // 2. Wyciąganie linku (URL) za pomocą zaawansowanych metod
    let url = findGhlProductUrl(card);

    // 3. Wyciąganie postępu (%)
    const cardText = card.innerText || "";
    const progressMatch = cardText.match(/(\d+)%/);
    const progress = progressMatch ? progressMatch[0] : "0%";

    // 4. Wyciąganie autora
    let author = "Nieznany";
    const authorCandidates = cardText.split('\n')
      .map(t => t.trim())
      .filter(t => t.length > 2 && !t.includes('%') && t !== "In Library" && t !== "Default" && t !== title);
    if (authorCandidates.length > 0) {
      author = authorCandidates[authorCandidates.length - 1];
    }

    courses.push({
      id: idx + 1,
      title,
      url,
      progress,
      author,
      rawText: cardText.replace(/\s+/g, ' ').trim()
    });
  });

  console.log(`\n%c📊 ZESKANOWANO KURSÓW: ${courses.length}`, "color: #10b981; font-weight: bold;");
  console.table(courses.map(c => ({ Tytuł: c.title, Link: c.url || "❌ NIE WYKRYTO", Postęp: c.progress, Autor: c.author })));

  // Pobierz plik JSON
  const json = JSON.stringify(courses, null, 2);
  const blob = new Blob([json], { type: 'application/json' });
  const downloadUrl = URL.createObjectURL(blob);
  const a = document.createElement('a');
  a.href = downloadUrl;
  a.download = `Holistic_HighLevel_Courses.json`;
  document.body.appendChild(a);
  a.click();
  document.body.removeChild(a);
  URL.revokeObjectURL(downloadUrl);

  console.log("%c✅ Plik 'Holistic_HighLevel_Courses.json' został pomyślnie pobrany!", "color: #10b981; font-weight: bold;");
})();
