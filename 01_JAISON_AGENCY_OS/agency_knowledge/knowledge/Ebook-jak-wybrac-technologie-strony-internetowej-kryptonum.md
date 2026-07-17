### 1. Główne zasady / ramy logiczne (Frameworki)

#### Architektura JAMstack
*   JAMstack to podejście do architektury aplikacji internetowych (również stron www), które oddziela warstwę doświadczeń użytkownika od danych i logiki biznesowej.
*   **JAM** to akronim od:
    *   **J**avaScript: Ewoluujące przeglądarki i API JavaScriptu oferują niemal nieograniczone możliwości poprawy doświadczeń użytkownika (np. animacje, interaktywne infografiki).
    *   **A**PIs: Gotowe do wykorzystania oprogramowanie, infrastruktura, funkcje i platformy. Podstawą jest możliwość integracji z kodem najlepszych zespołów programistycznych świata (np. Sanity.io dla CMS, Algolia dla wyszukiwarki). Twórcy API dbają o poprawność integracji i bezpieczeństwo.
    *   **M**arkup: Treści to proste pliki markdown, zgodne ze standardami, które można budować i testować wszędzie. Eliminują problemy z instalacją pakietów serwerowych czy kompatybilnością.

#### Filary JAMstack
Architektura JAMstack opiera się na postępie w 4 kluczowych obszarach, aby tworzyć strony zorientowane na szybkość, bezpieczeństwo i łatwość zarządzania:
1.  **Headless CMS:** Przechowywanie treści niezależnie od wyglądu, co pozwala na łatwe dostosowanie treści do różnych kanałów (web, mobile, IoT, dokumenty, marketing).
2.  **Nowoczesne platformy hostingowe i narzędzia CI/CD:** Delegowanie zarządzania i skalowania infrastruktury serwerowej do specjalistycznych platform, co przyspiesza i automatyzuje proces budowania i hostowania.
3.  **Statyczne Generatory Stron (SSG):** Narzędzia, które zawczasu budują całą stronę, generując statyczne zasoby. Pobierają dane z CMS i API, kompresują je i dzielą, aby pliki strony były maksymalnie lekkie i ładowały tylko to, co konieczne.
4.  **Rozwijające się API:** Umożliwiające integrację z zaawansowanymi platformami (np. Stripe, Algolia, Shopify).

#### Korzyści z JAMstack
*   Ultra szybkie działanie.
*   Skalowalność (prawie) bez ograniczeń.
*   Łatwość edycji treści.
*   Wysoka niezawodność (średni uptime projektów Kryptonum to 100% w ciągu 5 lat).
*   Maksymalne bezpieczeństwo.
*   Optymalizacja kosztów: Płacisz tylko za funkcje, z których korzystasz.
*   Wysoka atrakcyjność dla developerów ("developer experience wymiata").

#### Znaczenie szybkości wczytywania strony dla biznesu
*   **Konwersja:** Przyspieszenie wczytywania o 0,1 sekundy zwiększa konwersję o 8% (Deloitte).
*   **Współczynnik odrzuceń:** 88,5% użytkowników opuszcza wolno ładującą się stronę (review42).
*   **Sprzedaż:** Wzrost czasu wczytywania o 1 sekundę powoduje spadek sprzedaży o 27% (sagipl).
*   **Oczekiwania użytkowników:** 47% użytkowników oczekuje wczytywania strony poniżej 2 sekund (curatti).
*   **SEO:** Niska ocena w Google Core Web Vitals negatywnie wpływa na organiczne wyniki wyszukiwania i doświadczenie użytkowników.

#### Decyzja o wyborze technologii
Aby podjąć świadomą decyzję o wyborze technologii, należy wziąć pod uwagę:
*   Znajomość głównych założeń JAMstack.
*   Uwzględnienie strategii biznesowej.
*   Określenie konkretnych celów strony.
*   Każdy biznes i projekt jest inny – kluczowe jest dobre rozpracowanie problemu i koncepcji rozwiązania.

### 2. Gotowe schematy, prompty lub szablony

#### Legenda rekomendacji
*   **KryptoPolecanko:** Sprawdzone przez nas rozwiązania, z których sami regularnie korzystamy.
*   **KryptoCiekawe:** Technologie, które robią super wrażenie, niesamowicie się rozwijają, ale jeszcze nie były wykorzystywane w dużych, komercyjnych projektach.

#### Wybór Headless CMS na podstawie wielkości strony (unikalne podstrony)
| Liczba podstron         | S (Do 10) | M (11-30) | L (31-100) | XL (100+) |
| :---------------------- | :-------- | :-------- | :-------- | :-------- |
| DatoCMS                 | ✅        | ✅        | ✅        | ✅        |
| Prismic                 | ✅        | ✅        | ✅        | ✅        |
| Headless Wordpress      | ✅        | ✅        | ✅        | ✅        |
| Sanity                  | ✅        | ✅        | ✅        | ✅        |
| Contentful              | ✅        | ✅        | ✅        | ✅        |

*   **Rekomendacja:** DatoCMS i Prismic są polecane dla mniejszych projektów. Sanity jest polecane dla większych projektów (XL).

#### Wybór Headless CMS na podstawie liczby postów i kategorii bloga
| Posty i Kategorie bloga | Do 30 postów / 5 kat. | 30-100 postów / 10 kat. | 100-1000 postów / 20 kat. | 1000+ postów / 30+ kat. |
| :---------------------- | :--------------------- | :---------------------- | :------------------------ | :----------------------- |
| DatoCMS                 | ✅                     | ✅                      | ✅                        | ✅                       |
| Prismic                 | ✅                     | ✅                      | ✅                        | ✅                       |
| Headless Wordpress      | ✅                     | ✅                      | ✅                        | ✅                       |
| Sanity                  | ✅                     | ✅                      | ✅                        | ✅                       |
| Contentful              | ✅                     | ✅                      | ✅                        | ✅                       |

#### Wybór Headless CMS na podstawie liczby redaktorów
| Liczba redaktorów | 1 użytkownik | 2 użytkowników | 2-5 użytkowników | 5+ użytkowników |
| :---------------- | :----------- | :------------- | :--------------- | :-------------- |
| DatoCMS           | ✅           | ✅             | ✅               | ✅              |
| Prismic           | ✅           | ✅             | ✅               | ✅              |
| Headless Wordpress| ✅           | ✅             | ✅               | ✅              |
| Sanity            | ✅           | ✅             | ✅               | ✅              |
| Contentful        | ✅           | ✅             | ✅               | ✅              |

#### Wybór Headless CMS na podstawie wersji językowych
| Wersje językowe | 1 wersja | do 4 wersji | 4+ wersji |
| :-------------- | :------- | :---------- | :-------- |
| DatoCMS         | ✅       | ✅          | ✅        |
| Prismic         | ✅       | ✅          | ✅        |
| Headless Wordpress| ✅       | ✅          | ✅        |
| Sanity          | ✅       | ✅          | ✅        |
| Contentful      | ✅       | ✅          | ✅        |

#### Wybór Headless CMS na podstawie liczby użytkowników miesięcznie (e-commerce)
| Użytkownicy/miesiąc | Do 1000 | Powyżej 1000 | Powyżej 10000 |
| :------------------ | :------ | :----------- | :------------ |
| DatoCMS             | ✅      | ✅           | ✅            |
| Prismic             | ✅      | ✅           | ✅            |
| Headless Wordpress  | ✅      | ✅           | ✅            |
| Sanity              | ✅      | ✅           | ✅            |
| Contentful          | ✅      | ✅           | ✅            |

*   **Ostrzeżenie:** Dla fizycznych produktów z wysyłką, DatoCMS jest zdecydowanie odradzany.

#### Wybór Headless CMS na podstawie przechowywania plików (storage)
| Storage size       | Do 200 MB | Powyżej 200 MB | Powyżej 10 GB |
| :----------------- | :-------- | :------------- | :------------ |
| DatoCMS            | ✅        | ✅             | ✅            |
| Prismic            | ✅        | ✅             | ✅            |
| Headless Wordpress | ✅        | ✅             | ✅            |
| Sanity             | ✅        | ✅             | ✅            |
| Contentful         | ✅        | ✅             | ✅            |

#### Wybór Headless CMS na podstawie częstości zmian na stronie
| Częstość zmian na stronie | 2 nowe treści/miesiąc | 2-8 nowych treści/miesiąc | 8-20 nowych treści/miesiąc | 20+ treści/miesiąc |
| :------------------------ | :-------------------- | :------------------------- | :-------------------------- | :----------------- |
| DatoCMS                   | ✅                    | ✅                         | ✅                          | ✅                 |
| Prismic                   | ✅                    | ✅                         | ✅                          | ✅                 |
| Headless Wordpress        | ✅                    | ✅                         | ✅                          | ✅                 |
| Sanity                    | ✅                    | ✅                         | ✅                          | ✅                 |
| Contentful                | ✅                    | ✅                         | ✅                          | ✅                 |

#### Typowe narzędzia / platformy JAMstack
*   **Headless CMS:**
    *   **KryptoPolecanko:** Strapi, Prismic, Sanity, Headless WordPress, DatoCMS, Contentful
    *   **KryptoCiekawe:** GraphCMS, TinaCMS, Statamic, Kontent
*   **E-commerce:**
    *   **KryptoPolecanko:** Shopify, WooCommerce, easycart, SnipCart
    *   **KryptoCiekawe:** CommerceTools, BigCommerce, Hydrogen, Swell
*   **Backend & Logika Biznesowa (BaaS, Bazy Danych):**
    *   **KryptoPolecanko:** Firebase, Fauna, Airtable
    *   **KryptoCiekawe:** Backendless, MongoDB, Atlas
*   **Wyszukiwarka:**
    *   **KryptoPolecanko:** Algolia, Elastic search
    *   **KryptoCiekawe:** Swiftype, Lunr
*   **Komentowanie / Opinie:**
    *   **KryptoPolecanko:** Własna implementacja w CMS, Disqus
    *   **KryptoCiekawe:** ReplyBox, GraphComment
*   **Wysyłka formularzy:**
    *   **KryptoPolecanko:** Tally, SendGrid, Netlify Forms
    *   **KryptoCiekawe:** Kwes Forms, getform, Formspree, FormKeep, mailgun
*   **Automatyzacje marketingowe:**
    *   **KryptoPolecanko:** MailerLite, MailChimp, ActiveCampaign
    *   **KryptoCiekawe:** Campaign Monitor, ConvertKit, Brevo, MailJet
*   **Repozytorium kodu:**
    *   **KryptoPolecanko:** GitHub, GitLab (dla projektów), CodePen, StackBlitz (dla eksperymentów)
    *   **KryptoCiekawe:** Bitbucket
*   **Analityka:**
    *   **KryptoPolecanko:** Fathom analytics, Plausible
    *   **KryptoCiekawe:** statsy, Piwik PRO
*   **Automatyzacje biznesowe (Integracje API):**
    *   **KryptoPolecanko:** make, Zapier, Notion automations
    *   **KryptoCiekawe:** IFTTT
*   **CRM:**
    *   **KryptoPolecanko:** Livespace, Clickup
    *   **KryptoCiekawe:** pipedrive, HubSpot

#### Wybór Statycznego Generatora Stron (SSG)
*   **Dla stron ciężkich (wiele wideo, grafik) priorytetyzujących budowanie strony:** Hugo, Astro.js, Next.js.
    *   **Rekomendowane:** Astro.js i Next.js.
*   **Dla skomplikowanych stron z funkcjami aplikacji (zaawansowane funkcje client-side, bogate ekosystemy pluginów):** Next.js, Gatsby.js, SvelteKit.
    *   **Rekomendowane:** Next.js.
*   **Dla bardzo szybkich statycznych stron (większe strony budują się dłużej):** Hugo, Astro.js, Eleventy (uwaga: są uboższe w funkcje niż Next.js).
    *   **Rekomendowane jako domyślny SSG:** Next.js.
*   **Rekomendacja ogólna 2023:** Astro.js i Next.js.
    *   **Astro.js:** Dobry wybór dla stron bogatych w treści, które nie mają zaawansowanych interakcji.
    *   **Next.js:** Sprawdzi się dla skomplikowanych platform z wieloma funkcjami i interakcjami, które mają cechy aplikacji.

#### Wybór platformy hostingowej (dla budowania i hostingu)
*   **Rekomendowane dla bezpieczeństwa, wydajności i wygody developerów:** Vercel, Netlify.
*   **KryptoCiekawe dla wygody developerów:** CloudFlare, Fastly.
*   **KryptoCiekawe dla bezpieczeństwa:** Edgio, Heroku.
*   **Ostrzeżenie:** Dla dużych projektów i zespołów deweloperskich, koszty na Vercel i Netlify mogą szybko rosnąć – należy oszacować skalę projektu, aby estymować budżet.

#### Przykładowe zestawy technologii ("KryptoJAM")

**1. Wizerunkowa strona internetowa dla eksperta**
*   **Główny cel:** Pozyskiwanie leadów.
*   **Wielkość strony:** 5-6 podstron.
*   **Funkcje:** Formularz kontaktowy, autoresponder, budowa bazy mailowej, w przyszłości blog.
*   **KryptoJAM:**
    *   Headless CMS: Sanity
    *   Statyczny generator: Astro
    *   Hosting: Netlify
    *   Formularz: SendGrid
    *   Autoresponder i baza mailingowa: MailerLite

**2. E-commerce dla twórcy z produktami cyfrowymi**
*   **Główny cel:** Sprzedaż produktów.
*   **Wielkość strony:** 11-13 podstron.
*   **Funkcje:** E-commerce (3 produkty na uruchomienie), formularz kontaktowy, budowa bazy mailowej, newsletter, blog (9 artykułów zoptymalizowanych pod SEO na uruchomienie).
*   **KryptoJAM:**
    *   Headless CMS: Sanity
    *   Statyczny generator: Next.js
    *   E-commerce: easycart
    *   Formularz: SendGrid
    *   Baza i newsletter: MailerLite
    *   Hosting: Vercel
    *   Blog: Sanity

**3. Wielojęzyczna witryna korporacyjna**
*   **Główny cel:** Wsparcie marketingu i sprzedaży.
*   **Wielkość strony:** 250 podstron i 500 artykułów dla każdej wersji językowej.
*   **Funkcje:** 4 wersje językowe, blog, strony lądowania zintegrowane z webinarami, lejki marketingowe, integracja z Pipedrive i wewnętrznym systemem działu obsługi klienta.
*   **KryptoJAM:**
    *   Headless CMS: Sanity
    *   Statyczny generator: Next.js
    *   E-commerce: easycart
    *   Formularz: SendGrid
    *   Baza i newsletter: MailChimp
    *   Blog: Sanity
    *   4 wersje językowe - localization: Sanity + Next.js
    *   Strony lądowania zintegrowane z webinarami: Sanity + Zoom Enterprise
    *   Integracja z Pipedrive: make + dedykowane integracje
    *   Integracja z wewnętrznym systemem działu obsługi klienta: make + dedykowane integracje
    *   Lejki marketingowe: fathom analytics + systemy reklamowe LinkedIn, Google i Meta
    *   Hosting: Vercel

### 3. Konkretne instrukcje "Krok po Kroku"

#### Co brać pod uwagę przy wyborze Headless CMS (KryptoTip)
*   Szacując skalę i potrzeby, weź pod uwagę strategię biznesową na najbliższe 3 lata, rozwój strony, nowe funkcje i inne inicjatywy powiązane z celami strony WWW.
*   Przy szacowaniu wielkości strony (liczbę unikalnych podstron) warto wziąć pod uwagę jej rozwój w ciągu 2-3 lat, np. dodanie silnika e-commerce czy stron lądowania dla automatyzacji marketingowych.

#### Optymalizacja obrazów i wideo dla stron JAMstack
*   Do kompresji zdjęć i grafik: Squoosh
*   Do optymalizacji wideo: FFmpeg

#### Wybór rozwiązań e-commerce (KryptoTip)
*   Polecamy korzystać z dedykowanych rozwiązań e-commerce, zintegrować je z CMS i ukryć dane poszczególnym redaktorom, żeby widzieli tylko to, co jest w zakresie ich obowiązków.
*   Sanity integruje się z Shopify, pozwalając na podgląd produktów zarówno z panelu Sanity, jak i panelu administracyjnego Shopify.

#### Jak wybrać Statyczny Generator Stron (SSG) – Kryteria długoterminowe i skalowalności
*   **Wiek:** Minimum 2 lata na rynku w wersji produkcyjnej.
*   **Zaawansowanie i integracje:** Kompatybilność z bibliotekami (np. Tailwind, Framer Motion, gsap, Locomotive scroll), CMSami (Sanity, Prismic, Contentful), SaaSami (Shopify, WooCommerce, BigCommerce, Swell).
*   **Wsparcie:** Bogaty system bibliotek dla Gatsby.js i Next.js.
*   **Tempo rozwoju:** Regularnie przeglądaj liczbę commitów, plan rozwoju i pracę zespołu. Brak postępu przez 2 miesiące to sygnał ostrzegawczy.
*   **Trendy:** Śledź trendy i statystyki technologii (np. State of JS i State of CSS).

#### Kiedy nie używać JAMstacka (i jak oszczędzić pieniądze na Landing Page)
*   Jeśli jest to szybka akcja i początkowy etap biznesu, liczy się czas i podejście Pareto (minimalny nakład finansowy).
*   **6 kroków do walidacji pomysłu biznesowego za pomocą landing page bez kodowania:**
    1.  Wykorzystaj narzędzia low-code, np. Webflow.
    2.  Poświęć kilka dni na naukę Webflow (np. Webflow University).
    3.  Stwórz darmowe konto MailerLite (wystarczy dla podstawowych landingów).
    4.  Zepnij MailerLite, przetestuj double opt-in i wysyłkę freebie.
    5.  Podepnij Google Tag Manager i wszystkie kody śledzące systemów reklamowych.
    6.  Sprawdź, czy konwersje na landingu są poprawnie spięte, czy wszystko śmiga na różnych przeglądarkach i odpalaj reklamy.
*   **Ważne wskazówki dla landing page:**
    *   Nie bój się długich landing page – generują średnio 220% więcej leadów niż krótkie.
    *   Średnia liczba pól formularza to 11. Redukcja liczby z 11 do 4 powoduje 120% wzrost konwersji landing page.
*   Kiedy biznes się rozhula i potrzebujesz solidnej strategii, brandingu i miejsca w sieci, aby zbudować "imperium online", rozważ współpracę z agencją. Samodzielne zarządzanie jest bardzo trudne.

#### Zasoby do obserwacji rynku
*   Ankiety developerów całego świata.
*   Nowe funkcje przeglądarek.
*   Blog Google'a.
*   Konta na Twitterze (X) i strony twórców: Cassidy Williams, Una Kravets, Cassie Evans, Adam Argyle, Josh W Comeau, Sara Soueidan.
*   State of JS, State of CSS.