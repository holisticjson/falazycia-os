<img src="https://r2cdn.perplexity.ai/pplx-full-logo-primary-dark%402x.png" style="height:64px;margin-right:32px"/>

## Raport PageSpeed Insights — jaison.pl (12.07.2026)


***

### Wyniki ogólne

| Metryka | 📱 Mobile | 🖥️ Desktop |
| :-- | :-- | :-- |
| **Wydajność** | 🟠 **63** | 🟢 **90** |
| **Ułatwienia dostępu** | 🟠 **84** | 🟠 **79** |
| **Sprawdzone metody** | 🟢 **96** | 🟢 **96** |
| **SEO** | 🟢 **100** | 🟢 **100** |
| **Przeglądanie agentowe** | 🔴 **0/2** | 🟡 **1/2** |

SEO 100/100 to bardzo dobry wynik — poprzednie zalecenia agenta zostały najwyraźniej dobrze wdrożone.[^1][^2]

***

### Core Web Vitals — szczegóły

| Metryka | Mobile | Desktop | Cel Google |
| :-- | :-- | :-- | :-- |
| **FCP** (First Contentful Paint) | 🟠 3,3 s | 🟢 0,9 s | < 1,8 s |
| **LCP** (Largest Contentful Paint) | 🔴 **10,8 s** | 🟢 1,9 s | < 2,5 s |
| **TBT** (Total Blocking Time) | 🟢 10 ms | 🟢 0 ms | < 200 ms |
| **CLS** (Layout Shift) | 🟠 0.132 | 🟢 0.006 | < 0.1 |
| **Speed Index** | 🟠 3,3 s | 🟢 0,9 s | < 3,4 s |

Desktop jest w świetnym stanie. **Problem leży wyłącznie na mobile** — głównie przez obrazy i zasoby blokujące renderowanie.[^2]

***

### Krytyczne problemy do naprawy

#### 🔴 1. LCP na mobile: 10,8 s — katastrofalny

To najpoważniejszy problem. LCP powyżej 4 s Google traktuje jako „słabe" — 10,8 s to wynik, który może powodować **aktywne obniżenie pozycji w mobile search**. Przyczyna: prawdopodobnie hero image lub wideo tła ładowane bez lazy load / preload.

**Naprawa:**

```html
<!-- Dodaj do hero image: -->
>
<img src="hero.webp" fetchpriority="high" loading="eager">
```


#### 🔴 2. Obrazy — 3 405 KiB do zaoszczędzenia

Strona waży **5 423 KiB łącznie** — to ogromnie dużo dla landing page'a. Obrazy nie są skompresowane ani nie mają podanych atrybutów `width`/`height` (powoduje CLS).[^1]

**Naprawa:**

- Konwersja wszystkich obrazów do formatu **WebP** (oszczędność 60–80% rozmiaru)
- Dodanie `width` i `height` do każdego `<img>` — zapobiega layout shift
- Narzędzie: Squoosh.app lub automatycznie przez Cloudflare Image Optimization


#### 🟠 3. CLS na mobile: 0.132 (próg: 0.1)

Elementy przesuwają się podczas ładowania — prawdopodobnie obrazy bez wymiarów i font loading. Bezpośrednio powiązane z brakiem `width`/`height` na obrazach.[^1]

#### 🟠 4. Zasoby blokujące renderowanie — 2 320 ms opóźnienia (mobile)

Skrypty JS lub CSS ładowane synchronicznie w `<head>` blokują wyświetlenie strony.

**Naprawa:**

```html
<!-- Skrypty JS przenieść na koniec lub dodać defer/async: -->
<script src="skrypt.js" defer></script>
<!-- CSS non-critical ładować asynchronicznie -->
```


#### 🟠 5. Cache — 3 459 KiB bez cache policy

Zasoby statyczne (obrazy, JS, CSS) nie mają ustawionego nagłówka `Cache-Control`. Każdy powracający użytkownik pobiera wszystko od nowa.

**Naprawa w Cloudflare** (masz już Cloudflare na domenie — widać w robots.txt): włącz **Browser Cache TTL** na min. 1 rok dla zasobów statycznych.

***

### 🤖 Przeglądanie agentowe — 1/2 (Desktop) i 0/2 (Mobile)

To nowy audyt Google oceniający czy agenty AI mogą poprawnie nawigować po stronie.[^3]

**Znaleziony błąd:**

```
Buttons must have discernible text
Element: <button id="jaison-chat-send" onclick="sendJaisonInput()">
```

Przycisk wysyłania w czacie (`#jaison-chat-send`) nie ma żadnego tekstu ani atrybutu `aria-label` — agent AI (i screen reader) nie wie co to jest.[^3]

**Naprawa — jedna linia:**

```html
<!-- Przed: -->
<button id="jaison-chat-send" onclick="sendJaisonInput()">
  <!-- sama ikona -->
</button>

<!-- Po: -->
<button id="jaison-chat-send" onclick="sendJaisonInput()" aria-label="Wyślij wiadomość">
  <!-- ikona -->
</button>
```

To jest poprawka na **dosłownie 30 sekund** w edytorze kodu, a podniesie wynik „Przeglądanie agentowe" do 2/2 — co jest ważne, bo Google oficjalnie mówi, że ta kategoria będzie zyskiwała na znaczeniu w kontekście AI search.

***

### Plan naprawy — priorytety

| Priorytet | Zadanie | Trudność | Wpływ |
| :-- | :-- | :-- | :-- |
| 🔴 1 | `aria-label` na przycisku czatu (`jaison-chat-send`) | ⚡ 5 min | Agentowe 0→2/2 |
| 🔴 2 | Konwersja obrazów na WebP + kompresja | ⏱️ 2-3h | LCP, rozmiar strony |
| 🔴 3 | `width` + `height` na wszystkich `<img>` | ⏱️ 1h | CLS 0.132→<0.1 |
| 🟠 4 | `fetchpriority="high"` na hero image | ⚡ 10 min | LCP mobile |
| 🟠 5 | `defer` na skryptach JS | ⏱️ 30 min | FCP mobile |
| 🟠 6 | Cache-Control przez Cloudflare | ⚡ 15 min | Powracający użytkownicy |

Najszybsza wygrana: **aria-label na przycisku** — 5 minut roboty, wynik agentowy skacze z 0/2 na 2/2, a strona już ma SEO 100/100, więc to domknięcie pełnej zieleni w każdej kategorii poza wydajnością mobile.[^2]

<div align="center">⁂</div>

[^1]: https://pagespeed.web.dev/analysis/https-jaison-pl/4yifj1kkvr?form_factor=mobile

[^2]: https://pagespeed.web.dev/analysis/https-jaison-pl/4yifj1kkvr?form_factor=desktop

[^3]: https://pagespeed.web.dev/analysis/https-jaison-pl/4yifj1kkvr?form_factor=desktop

