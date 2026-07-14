<?php
header("Access-Control-Allow-Origin: *");
header("Access-Control-Allow-Headers: Content-Type");
header("Content-Type: application/json");

// Inicjalizacja sesji pod Spam Shields i utrzymanie historii czatu
if (session_status() === PHP_SESSION_NONE) {
    ini_set('session.cookie_httponly', 1);
    ini_set('session.use_only_cookies', 1);
    session_start();
}

// Funkcja wczytywania zmiennych .env (obejście putenv na Hostido / Cloud Run)
function getEnvVar($name) {
    if (isset($_ENV[$name])) return $_ENV[$name];
    if (isset($_SERVER[$name])) return $_SERVER[$name];
    $val = getenv($name);
    return $val !== false ? $val : null;
}

$input = json_decode(file_get_contents("php://input"), true);

// TARCZA 1: Honeypot
if ($input) {
    if (!empty($input['email_confirm']) || !empty($input['phone_check'])) {
        echo json_encode(["status" => "success", "reply" => "Wiadomość wysłana! Serwisant skontaktuje się z Tobą. 🤝"]);
        exit;
    }
}

if ($_SERVER["REQUEST_METHOD"] !== "POST") {
    http_response_code(405);
    exit;
}

$userMessage = isset($input['message']) ? trim($input['message']) : '';
if (empty($userMessage)) {
    echo json_encode(["status" => "error", "message" => "Pusta wiadomość."]);
    exit;
}

// TARCZA 2: IP Rate Limiter (3 sekundy)
if (isset($_SESSION['chat_last_query_time'])) {
    if (time() - $_SESSION['chat_last_query_time'] < 3) {
        echo json_encode(["status" => "success", "reply" => "Piszesz trochę za szybko! Odczekaj chwilę przed zadaniem pytania. ⏱️"]);
        exit;
    }
}
$_SESSION['chat_last_query_time'] = time();

// TARCZA 3: Dobowy limit (30 zapytań)
if (!isset($_SESSION['chat_query_count'])) {
    $_SESSION['chat_query_count'] = 0;
    $_SESSION['chat_first_query_time'] = time();
}
if (time() - $_SESSION['chat_first_query_time'] > 86400) {
    $_SESSION['chat_query_count'] = 0;
    $_SESSION['chat_first_query_time'] = time();
}
if ($_SESSION['chat_query_count'] >= 30) {
    echo json_encode(["status" => "success", "reply" => "Przekroczyłeś dobowy limit 30 zapytań do bota. Skontaktuj się z nami bezpośrednio na <b>WhatsApp</b>: https://wa.me/48791636644 📞"]);
    exit;
}
$_SESSION['chat_query_count']++;

// Inicjalizacja i aktualizacja historii czatu w sesji (ostatnie 15 wiadomości dla oszczędności tokenów)
if (!isset($_SESSION['chat_history']) || !is_array($_SESSION['chat_history'])) {
    $_SESSION['chat_history'] = [];
}
$_SESSION['chat_history'][] = ["role" => "user", "text" => $userMessage];
if (count($_SESSION['chat_history']) > 15) {
    array_shift($_SESSION['chat_history']);
}

// Pomocnicze funkcje JWT
function base64UrlEncode($data) {
    return str_replace(['+', '/', '='], ['-', '_', ''], base64_encode($data));
}

// Pobieranie tokenu z Service Account
function getGoogleAccessToken($saJsonStr) {
    $sa = json_decode($saJsonStr, true);
    if (!$sa || !isset($sa['private_key']) || !isset($sa['client_email'])) {
        throw new Exception("Błędny format klucza Service Account JSON.");
    }
    $privateKey = str_replace('\n', "\n", $sa['private_key']);
    $clientEmail = $sa['client_email'];

    $header = json_encode(['alg' => 'RS256', 'typ' => 'JWT']);
    $now = time();
    $payload = json_encode([
        'iss' => $clientEmail,
        'scope' => 'https://www.googleapis.com/auth/cloud-platform',
        'aud' => 'https://oauth2.googleapis.com/token',
        'exp' => $now + 3600,
        'iat' => $now
    ]);

    $base64UrlHeader = base64UrlEncode($header);
    $base64UrlPayload = base64UrlEncode($payload);
    $signatureInput = $base64UrlHeader . "." . $base64UrlPayload;
    $signature = '';
    openssl_sign($signatureInput, $signature, $privateKey, 'SHA256');

    $jwt = $signatureInput . "." . base64UrlEncode($signature);

    $ch = curl_init("https://oauth2.googleapis.com/token");
    curl_setopt($ch, CURLOPT_RETURNTRANSFER, true);
    curl_setopt($ch, CURLOPT_POST, true);
    curl_setopt($ch, CURLOPT_POSTFIELDS, http_build_query([
        'grant_type' => 'urn:ietf:params:oauth:grant-type:jwt-bearer',
        'assertion' => $jwt
    ]));
    $res = curl_exec($ch);
    curl_close($ch);

    $data = json_decode($res, true);
    if (!isset($data['access_token'])) {
        throw new Exception("Nie udało się uzyskać Google Access Token: " . json_encode($data));
    }
    return $data['access_token'];
}

// Konwersja Markdown -> HTML (Zasada 13 - Bezwyjątkowe usuwanie gwiazdek)
function cleanAndHumanizeMarkdown($text) {
    // Zamiana pogrubień i kursyw na tagi HTML
    $text = preg_replace('/\*\*(.*?)\*\*/', '<strong>$1</strong>', $text);
    $text = preg_replace('/\*(.*?)\*/', '<em>$1</em>', $text);
    
    // Całkowite wyczyszczenie wszelkich pozostałych gwiazdek
    $text = str_replace('**', '', $text);
    $text = str_replace('*', '', $text);
    
    // Parsowanie list nienumerowanych
    $lines = explode("\n", $text);
    $inList = false;
    $htmlLines = [];
    foreach ($lines as $line) {
        $trimmed = trim($line);
        // Dopasowanie linii zaczynających się od myślnika lub kulki (bullet point)
        if (preg_match('/^[\-\x{2022}]\s+(.*)$/u', $trimmed, $matches)) {
            if (!$inList) {
                $htmlLines[] = '<ul>';
                $inList = true;
            }
            $htmlLines[] = '<li>' . $matches[1] . '</li>';
        } else {
            if ($inList) {
                $htmlLines[] = '</ul>';
                $inList = false;
            }
            $htmlLines[] = $line;
        }
    }
    if ($inList) {
        $htmlLines[] = '</ul>';
    }
    return nl2br(implode("\n", $htmlLines));
}

// Klasyfikator zapytań: czy to powitanie lub odpowiedź sterująca audytem?
function isCasualOrAudit($message) {
    // Usuń interpunkcję, by uniknąć problemów z 'Cześć!' itp.
    $clean = mb_strtolower(trim(preg_replace('/[^\p{L}\p{N}\s]/u', '', $message)));
    
    $greetings = [
        'cześć', 'czesc', 'hej', 'hejo', 'witaj', 'witajcie', 'dzień dobry', 'dzien dobry', 
        'dobry wieczór', 'dobry wieczor', 'hello', 'hi', 'siema', 'siemanko', 'elo', 'elówa',
        'dzięki', 'dzieki', 'dziękuje', 'dziekuje', 'dziękuję', 'super', 'fajnie', 'ekstra',
        'kim jesteś', 'kim jestes', 'co robisz', 'co potrafisz', 'jak się nazywasz', 'jak sie nazywasz'
    ];
    
    $auditAnswers = [
        'tak', 'nie', 'zgadzam się', 'zgadzam sie', 'pewnie', 'jasne', 'okej', 'ok', 'o k',
        'audyt', 'diagnostyka', 'zacznijmy', 'start', 'dalej', 'pomiń', 'pomin', 'chcę', 'chce',
        'gotowy', 'gotowa', '1', '2', '3', '4', '5', '0', 'a', 'b', 'c', 'd', 'e'
    ];
    
    if (in_array($clean, $greetings) || in_array($clean, $auditAnswers)) {
        return true;
    }
    
    // Jeśli to bardzo krótki zwrot i nie ma w nim znaku zapytania
    if (mb_strlen($clean) <= 15 && strpos($message, '?') === false) {
        return true;
    }
    
    return false;
}

// Pobranie klucza SA z serwera
$saJsonStr = getEnvVar('GCP_SERVICE_ACCOUNT_JSON');
if (!$saJsonStr) {
    echo json_encode(["status" => "success", "reply" => "Przepraszam, konfiguracja autoryzacji bota (GCP_SERVICE_ACCOUNT_JSON) jest tymczasowo niedostępna na serwerze."]);
    exit;
}

try {
    $accessToken = getGoogleAccessToken($saJsonStr);
    
    $project_id = getEnvVar('GCP_PROJECT_AGENCY') ?? "holistic-dashboard-dev";
    $loc = "global";
    $host = ($loc === "global") ? "discoveryengine.googleapis.com" : "{$loc}-discoveryengine.googleapis.com";
    $engine_id = getEnvVar('VERTEX_ENGINE_AGENCY') ?? "holistic-search-app_1780143991783";
    
    $retrievedSummary = "";
    
    // KROK 1: Odpytywanie Vertex AI Search (RAG) zostało TYMCZASOWO ODPIĘTE na życzenie użytkownika.
    // Zostawiamy czystego Agenta opartego o System Prompt (Ghost v2 + Audyt), aby uniknąć 
    // zbyt obszernych odpowiedzi bazujących na materiałach edukacyjnych.
    /*
    if (!isCasualOrAudit($userMessage)) {
        $searchUrl = "https://{$host}/v1/projects/{$project_id}/locations/{$loc}/collections/default_collection/engines/{$engine_id}/servingConfigs/default_search:search";
        
        $searchPayload = json_encode([
            "query" => $userMessage,
            "pageSize" => 1,
            "contentSearchSpec" => [
                "summarySpec" => [
                    "summaryResultCount" => 1,
                    "useSemanticChunks" => true,
                    "ignoreAdversarialQuery" => true
                ]
            ]
        ]);

        $ch = curl_init($searchUrl);
        curl_setopt($ch, CURLOPT_RETURNTRANSFER, true);
        curl_setopt($ch, CURLOPT_POST, true);
        curl_setopt($ch, CURLOPT_POSTFIELDS, $searchPayload);
        curl_setopt($ch, CURLOPT_HTTPHEADER, [
            "Authorization: Bearer " . $accessToken,
            "Content-Type: application/json"
        ]);
        $searchResponse = curl_exec($ch);
        $searchHttpCode = curl_getinfo($ch, CURLINFO_HTTP_CODE);
        curl_close($ch);

        if ($searchHttpCode === 200) {
            $searchData = json_decode($searchResponse, true);
            $retrievedSummary = $searchData['summary']['summaryText'] ?? "";
        }
    }
    */

    // KROK 2: Przygotowanie instrukcji systemowej dla Gemini
    $baseSystemInstruction = "Jesteś J(AI)SON AI — wirtualnym architektem systemów i prawą ręką Tomasza Dudy (założyciela agencji jaison.pl).
Twoim nadrzędnym zadaniem jest demaskowanie chaosu u użytkowników na stronie jaison.pl oraz oferowanie i przeprowadzanie z nimi **Interaktywnego Audytu Systemowego (21 Pytań Diagnostycznych)**, który uświadamia im wąskie gardła i wycieki zysków w ich biznesie.

**OFERTA I CENNIK:**
1. **AI Quick Win — od 4 900 PLN netto (do 7 dni roboczych):** Podstawowa automatyzacja (n8n/Make), mapowanie procesów, usunięcie powtarzalnych zadań. Najlepsze na start dla solopreneurów, twórców, biznesów lokalnych.
2. **AI Operator OS — od 8 900 PLN netto:** Zaawansowane agenty AI, pełna integracja z CRM, automatyzacje n8n i Systeme.io, odzyskanie do 80% czasu operacyjnego właściciela.
3. **AI Grant & Architecture Sprint — od 6 900 PLN netto:** Audyt gotowości, specyfikacja architektury pod GCP i dokumentacja niezbędna do pozyskania dotacji KPO / unijnych.
4. **AI Boardroom / Enterprise — od 15 000 PLN netto:** Pełny Wirtualny Zarząd AI (CEO, CMO, CFO, COO) na prywatnej maszynie GCP, SQL, SLA.

**INTERAKTYWNY AUDYT (21 PYTAŃ DIAGNOSTYCZNYCH):**
Jeśli użytkownik zapyta o audyt, automatyzacje, diagnostykę, chce poukładać biznes (niezależnie czy to lokalne usługi, e-commerce, MLM, twórca czy korporacja) lub po prostu wykaże ciekawość, **zaproponuj natychmiast rozpoczęcie szybkiego Audytu Jaisona (21 pytań)**.
- **Zasada interakcji:** Nie zarzucaj użytkownika ścianą tekstu. Zadawaj pytania **po jednym** lub w **bardzo krótkich seriach (maksymalnie 2-3 pytania na raz)**, aby utrzymać dynamikę i zaangażowanie (ADHD-friendly).
- **Punktacja:** Ustal prostą zasadę: za każdą odpowiedź 'Tak/Zgadzam się/Mam ten problem' użytkownik otrzymuje **1 punkt**. Za odpowiedź 'Nie/Mam to zautomatyzowane/Nie mam tego problemu' otrzymuje **0 punktów**. Prowadź w pamięci jego bilans.
- **Struktura Audytu (Uniwersalne Pytania):**
  - **Sekcja 1: Chaos i Czas** (ręczne przepisywanie danych, brak jednego źródła prawdy, onboarding powyżej 2 dni, uciekające leady z czatów, brak SOP).
  - **Sekcja 2: Lejki i Konwersja** (odpowiedź na leady powyżej 15 min, brak automatycznego dogrzewania leadów, brak analityki ruchu, brak follow-upów, ręczne umawianie spotkań).
  - **Sekcja 3: Skalowalność i AI** (brak bazy wiedzy dla AI, obawa przed załamaniem przy 10-krotnym wzroście, praca manualna zamiast automatyzacji, ręczna obsługa powtarzalnych pytań, brak automatycznego zbierania opinii).
  - **Sekcja 4: Wolność Biznesowa** (uczucie bycia niewolnikiem operacyjnym, praca po godzinach/weekendami, brak możliwości wyjazdu na 30 dni, gaszenie pożarów, pytanie kluczowe: gotowość na wdrożenie Niewidzialnego Pracownika AI).
- **Podsumowanie i Wyniki:**
  - **0-7 pkt: RĘKODZIEŁO.** Biznes w 100% zależy od nich. Ryzyko wypalenia.
  - **8-15 pkt: STREFA ŚREDNIAKÓW.** Chaos narzędziowy. Dane rozproszone.
  - **16-21 pkt: HOLISTIC OPERATOR.** Gotowość do wdrożenia Agentów AI, którzy przejmą rutynę 24/7.
- **CTA:** Po audycie (lub w trakcie, gdy widzisz głęboki problem), skieruj użytkownika na **umówienie rozmowy w widgecie Cal.com obok** lub napisanie bezpośrednio na **hello@jaison.pl**.

**STYL KOMUNIKACJI (Ghost v2 / NLP VAK / ADHD-Friendly):**
1. Mów zwięźle i konkretnie. Akapity max 2-3 zdania. Żadnego lania wody, korpo-bełkotu i ściemniania.
2. **NIGDY nie używaj formatowania Markdown (np. gwiazdek **). Formatuj całą odpowiedź WYŁĄCZNIE w czystym HTML**, używając tagów `<p>`, `<strong>`, `<ul>` i `<li>`. Obficie stosuj tag `<strong>` do pogrubiania kluczowych słów, aby ułatwić szybkie skanowanie wzrokiem (visual anchoring).
3. Pisz bezpośrednio i szczerze do odbiorcy ('Ty').
4. Używaj NLP VAK:
   - **Wzrok:** 'zobacz to', 'dostrzeż ten wyciek', 'spójrz na schemat'.
   - **Słuch:** 'posłuchaj tego', 'usłysz jak Twoja skrzynka milknie'.
   - 'poczuj ulgę', 'zdejmij ten ciężar', 'dotknij tej prostoty'.
5. Demaskuj naciąganie konkurencji na drogie abonamenty (my wdrażamy raz, bez stałych opłat licencyjnych, na własności klienta).

Odpowiadaj krótko, inteligentnie, z lekkim pazurem. Nie wymyślaj cen ani usług poza podanymi powyżej.";

    $dynamicSystemInstruction = $baseSystemInstruction;
    if (!empty($retrievedSummary)) {
        $dynamicSystemInstruction .= "

<ZASADY_KORZYSTANIA_Z_BAZY_WIEDZY>
Otrzymujesz poniżej dodatkowy kontekst z bazy wiedzy Jaison (np. transkrypcje wideo lub artykuły).
KATEGORYCZNE RESTRYKCJE:
1. NIE WOLNO Ci wchodzić w rolę prowadzącego webinar (np. nie używaj zwrotów 'Witajcie serdecznie', 'Dzisiaj będzie materiał').
2. NIE KOPIUJ tekstu z bazy słowo w słowo. Traktuj to wyłącznie jako encyklopedyczne suche fakty do rozwiązania problemu użytkownika.
3. Zachowaj 100% spójności ze swoim stylem (krótkie zdania, bezpośredni zwrot na 'Ty', HTML bez markdownu).
</ZASADY_KORZYSTANIA_Z_BAZY_WIEDZY>

<BAZA_WIEDZY>
" . $retrievedSummary . "
</BAZA_WIEDZY>";
    }

    // KROK 3: Wywołanie Vertex AI Gemini 2.5 Flash przez REST API
    $geminiUrl = "https://us-central1-aiplatform.googleapis.com/v1/projects/{$project_id}/locations/us-central1/publishers/google/models/gemini-2.5-flash:generateContent";
    
    $contentsPayload = [];
    foreach ($_SESSION['chat_history'] as $turn) {
        $contentsPayload[] = [
            "role" => ($turn['role'] === 'user') ? 'user' : 'model',
            "parts" => [
                ["text" => $turn['text']]
            ]
        ];
    }
    
    $geminiPayload = json_encode([
        "contents" => $contentsPayload,
        "systemInstruction" => [
            "parts" => [
                ["text" => $dynamicSystemInstruction]
            ]
        ],
        "generationConfig" => [
            "temperature" => 0.7,
            "maxOutputTokens" => 800
        ]
    ]);

    $ch = curl_init($geminiUrl);
    curl_setopt($ch, CURLOPT_RETURNTRANSFER, true);
    curl_setopt($ch, CURLOPT_POST, true);
    curl_setopt($ch, CURLOPT_POSTFIELDS, $geminiPayload);
    curl_setopt($ch, CURLOPT_HTTPHEADER, [
        "Authorization: Bearer " . $accessToken,
        "Content-Type: application/json"
    ]);
    $geminiResponse = curl_exec($ch);
    $geminiHttpCode = curl_getinfo($ch, CURLINFO_HTTP_CODE);
    curl_close($ch);

    $replyText = "";
    if ($geminiHttpCode === 200) {
        $geminiData = json_decode($geminiResponse, true);
        $replyText = $geminiData['candidates'][0]['content']['parts'][0]['text'] ?? "";
    } else {
        // Fallback: jeśli Gemini zwróci błąd, zaloguj go i użyj bezpośredniej odpowiedzi z wyszukiwarki lub standardowej wiadomości
        error_log("Błąd Vertex AI Gemini: Kod HTTP " . $geminiHttpCode . ", Odpowiedź: " . $geminiResponse);
    }

    // Dodatkowy fallback bezpieczeństwa
    if (empty($replyText)) {
        $replyText = !empty($retrievedSummary) ? $retrievedSummary : "Nie potrafię odpowiedzieć w tym momencie. Możesz skontaktować się bezpośrednio ze mną pisząc na <strong>hello@jaison.pl</strong>!";
    }

    // Oczyszczenie odpowiedzi z markdown i transformacja na HTML
    $cleanReply = cleanAndHumanizeMarkdown($replyText);

    // Aktualizacja historii czatu w sesji o odpowiedź bota
    $_SESSION['chat_history'][] = ["role" => "bot", "text" => $cleanReply];

    echo json_encode([
        "status" => "success",
        "reply" => $cleanReply
    ]);

} catch (Exception $e) {
    echo json_encode([
        "status" => "success",
        "reply" => "Przepraszam, wystąpił chwilowy błąd techniczny podczas łączenia z chmurą Google: " . $e->getMessage() . ". Skontaktuj się ze mną bezpośrednio pod adresem hello@jaison.pl! 📞"
    ]);
}
