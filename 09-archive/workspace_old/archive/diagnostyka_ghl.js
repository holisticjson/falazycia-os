/**
 * GHL Library-v2 Structure Diagnostic Tool
 * -----------------------------------------
 * Paste this simple script in the browser console of university.gohighlevel.com/library-v2
 * to dump the exact HTML structure of the course cards. 
 * This will show us why the standard links are not being detected!
 */

(function runDiagnostic() {
  console.clear();
  console.log("%c🔍 DIAGNOSTYKA STRUKTURY GHL LIBRARY-V2", "color: #ff007f; font-size: 16px; font-weight: bold;");

  const productList = document.querySelector('#product-list');
  if (!productList) {
    console.error("❌ Nie odnaleziono kontenera '#product-list' na tej stronie!");
    return;
  }

  const cards = productList.children;
  console.log(`✅ Odnaleziono '#product-list'. Liczba kart kursów: ${cards.length}`);

  if (cards.length > 0) {
    const firstCard = cards[0];
    console.log("%c\n1. HTML PIERWSZEJ KARTY KURSU:", "color: #38bdf8; font-weight: bold;");
    console.log(firstCard.outerHTML);

    console.log("%c\n2. LINKI <a> WEWNĄTRZ PIERWSZEJ KARTY:", "color: #38bdf8; font-weight: bold;");
    const firstCardLinks = Array.from(firstCard.querySelectorAll('a'));
    if (firstCardLinks.length === 0) {
      console.log("⚠️ Brak tagów <a> w pierwszej karcie! Prawdopodobnie kliknięcie jest obsługiwane przez JS na poziomie DIV.");
    } else {
      firstCardLinks.forEach((a, idx) => {
        console.log(`   [a #${idx + 1}] Text: "${a.innerText.trim()}", Href: "${a.href}", Classes: "${a.className}"`);
      });
    }

    console.log("%c\n3. INNE ELEMENTY KLIKALNE (button, div z click) W PIERWSZEJ KARTIE:", "color: #38bdf8; font-weight: bold;");
    const clickables = Array.from(firstCard.querySelectorAll('button, [onclick], [class*="btn"], [class*="button"]'));
    clickables.forEach((el, idx) => {
      console.log(`   [el #${idx + 1}] Tag: <${el.tagName.toLowerCase()}>, Text: "${el.innerText.trim()}", Attributes:`, Array.from(el.attributes).map(attr => `${attr.name}="${attr.value}"`));
    });
  }

  console.log("%c\n4. WSZYSTKIE LINKI <a> NA CAŁEJ STRONIE:", "color: #a855f7; font-weight: bold;");
  const allLinks = Array.from(document.querySelectorAll('a'));
  console.log(`Łączna liczba linków <a> na stronie: ${allLinks.length}`);
  allLinks.slice(0, 30).forEach((a, idx) => {
    console.log(`   [#${idx + 1}] Text: "${a.innerText.trim().substring(0,30)}", Href: "${a.href}"`);
  });

  console.log("%c\n-------------------------------------------------------------", "color: #ff007f;");
  console.log("%cSkopiuj powyższy log z konsoli i wklej go do czatu, a ja natychmiast dostosuję wtyczkę!", "color: #10b981; font-weight: bold;");
})();
