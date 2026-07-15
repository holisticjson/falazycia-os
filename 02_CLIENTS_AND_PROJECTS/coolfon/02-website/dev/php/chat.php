<?php
/* ==========================================================================
   COOLFON.PL — SECURE CHATBOT BACKEND PROXY (PHP + VERTEX AI SEARCH + FALLBACK)
   ========================================================================== */

header("Access-Control-Allow-Origin: *");
header("Access-Control-Allow-Headers: Content-Type");
header("Content-Type: application/json");

// 1. Funkcja do bezpiecznego wczytywania zmiennych środowiskowych z pliku .env
function loadEnv($path) {
    if (!file_exists($path)) return;
    $lines = file($path, FILE_IGNORE_NEW_LINES | FILE_SKIP_EMPTY_LINES);
    foreach ($lines as $line) {
        if (strpos(trim($line), '#') === 0) continue;
        $parts = explode('=', $line, 2);
        if (count($parts) === 2) {
            $name = trim($parts[0]);
            $value = trim($parts[1]);
            // Zawsze zapisujemy bezpośrednio w $_ENV oraz $_SERVER (obejście blokady putenv)
            $_ENV[$name] = $value;
            $_SERVER[$name] = $value;
            @putenv("{$name}={$value}");
        }
    }
}

// Funkcja bezpiecznego pobierania zmiennych środowiskowych (sandbox-proof)
function getEnvVar($name) {
    if (isset($_ENV[$name])) {
        return $_ENV[$name];
    }
    if (isset($_SERVER[$name])) {
        return $_SERVER[$name];
    }
    $val = getenv($name);
    return $val !== false ? $val : null;
}

// Wczytaj plik .env znajdujący się poziom wyżej (w katalogu głównym)
loadEnv(__DIR__ . '/../.env');

// 2. Inicjalizacja sesji pod kątem potrójnej tarczy anty-spamowej
if (session_status() === PHP_SESSION_NONE) {
    ini_set('session.cookie_httponly', 1);
    ini_set('session.use_only_cookies', 1);
    session_start();
}

$input = json_decode(file_get_contents("php://input"), true);

// ==========================================================================
// TARCZA 1: Honeypot (Weryfikacja czy zapytania nie wysłał bot)
// ==========================================================================
if ($input) {
    $emailConfirm = isset($input['email_confirm']) ? trim($input['email_confirm']) : '';
    $phoneCheck = isset($input['phone_check']) ? trim($input['phone_check']) : '';
    
    if (!empty($emailConfirm) || !empty($phoneCheck)) {
        echo json_encode([
            "status" => "success",
            "reply" => "Dziękuję za wiadomość! Serwisant przeanalizuje Twoje zapytanie tak szybko, jak to możliwe. 🤝"
        ]);
        exit;
    }
}

if ($_SERVER["REQUEST_METHOD"] !== "POST") {
    http_response_code(405);
    echo json_encode(["status" => "error", "message" => "Method Not Allowed"]);
    exit;
}

if (!$input || !isset($input['message'])) {
    http_response_code(400);
    echo json_encode(["status" => "error", "message" => "Brak wymaganej wiadomości użytkownika."]);
    exit;
}

$userMessage = trim($input['message']);
$chatHistory = isset($input['history']) ? $input['history'] : [];

// ==========================================================================
// TARCZA 2: IP Rate Limiter (Zabezpieczenie przed seryjnymi zapytaniami)
// ==========================================================================
if (isset($_SESSION['chat_last_query_time'])) {
    $timeSinceLast = time() - $_SESSION['chat_last_query_time'];
    if ($timeSinceLast < 3) {
        echo json_encode([
            "status" => "success",
            "reply" => "Piszesz trochę za szybko! Odczekaj chwilę (co najmniej 3 sekundy) przed zadaniem kolejnego pytania. ⏱️"
        ]);
        exit;
    }
}
$_SESSION['chat_last_query_time'] = time();

// ==========================================================================
// TARCZA 3: Dobowy limit zapytań na użytkownika (Maksymalnie 30)
// ==========================================================================
if (!isset($_SESSION['chat_query_count'])) {
    $_SESSION['chat_query_count'] = 0;
    $_SESSION['chat_first_query_time'] = time();
}

// Resetowanie limitu po upływie 24 godzin
if (time() - $_SESSION['chat_first_query_time'] > 86400) {
    $_SESSION['chat_query_count'] = 0;
    $_SESSION['chat_first_query_time'] = time();
}

if ($_SESSION['chat_query_count'] >= 30) {
    echo json_encode([
        "status" => "success",
        "reply" => "Przekroczyłeś dobowy limit 30 zapytań do naszego asystenta AI. Aby otrzymać natychmiastową pomoc, napisz bezpośrednio do naszego serwisanta na <b>WhatsApp</b> lub zadzwoń pod numer: <b>+48 532 840 877</b>! 📞"
    ]);
    exit;
}

// ==========================================================================
// FUNKCJE POMOCNICZE (AUTORYZACJA GOOGLE I CZYSZCZENIE MARKDOWNU)
// ==========================================================================

function base64UrlEncode($data) {
    return str_replace(['+', '/', '='], ['-', '_', ''], base64_encode($data));
}

// Generowanie tokenu Google OAuth2 z klucza konta usługowego
function getGoogleAccessToken($saJsonStr) {
    $sa = json_decode($saJsonStr, true);
    if (!$sa || !isset($sa['private_key']) || !isset($sa['client_email'])) {
        throw new Exception("Nieprawidłowa struktura klucza konta usługowego!");
    }

    $privateKey = $sa['private_key'];
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
    
    if (!openssl_sign($signatureInput, $signature, $privateKey, 'SHA256')) {
        throw new Exception("Błąd OpenSSL podczas podpisywania tokenu JWT.");
    }

    $base64UrlSignature = base64UrlEncode($signature);
    $jwt = $signatureInput . "." . $base64UrlSignature;

    $ch = curl_init("https://oauth2.googleapis.com/token");
    curl_setopt($ch, CURLOPT_RETURNTRANSFER, true);
    curl_setopt($ch, CURLOPT_POST, true);
    curl_setopt($ch, CURLOPT_POSTFIELDS, http_build_query([
        'grant_type' => 'urn:ietf:params:oauth:grant-type:jwt-bearer',
        'assertion' => $jwt
    ]));
    curl_setopt($ch, CURLOPT_HTTPHEADER, [
        'Content-Type: application/x-www-form-urlencoded'
    ]);
    curl_setopt($ch, CURLOPT_TIMEOUT, 10);
    
    $response = curl_exec($ch);
    $httpCode = curl_getinfo($ch, CURLINFO_HTTP_CODE);
    curl_close($ch);

    if ($httpCode !== 200) {
        throw new Exception("Błąd pobierania access tokenu (HTTP $httpCode): " . $response);
    }

    $data = json_decode($response, true);
    if (!isset($data['access_token'])) {
        throw new Exception("Brak access_token w odpowiedzi Google.");
    }

    return $data['access_token'];
}

// Konwersja formatowania Markdown na przyjazny HTML (Zasada 13)
function cleanAndHumanizeMarkdown($text) {
    // 1. Zamiana podwójnych gwiazdek **tekst** na <b>tekst</b>
    $text = preg_replace('/\*\*(.*?)\*\//', '<b>$1</b>', $text); // Wait: correction preg_replace below
    $text = preg_replace('/\*\*(.*?)\*\*/', '<b>$1</b>', $text);
    
    // 2. Zamiana pojedynczych gwiazdek *tekst* na <i>tekst</i>
    $text = preg_replace('/\*(.*?)\*/', '<i>$1</i>', $text);
    
    // 3. Konwersja wypunktowań na semantyczne listy <ul>/<li>
    $lines = explode("\n", $text);
    $inList = false;
    $htmlLines = [];
    
    foreach ($lines as $line) {
        $trimmed = trim($line);
        if (preg_match('/^[\*\-\x{2022}]\s+(.*)$/u', $trimmed, $matches)) {
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
    
    $text = implode("\n", $htmlLines);
    
    // 4. Bezpieczna zamiana końców linii na <br> (nl2br)
    $text = nl2br($text);
    
    $text = str_replace(["<ul><br />", "</ul><br />", "<li><br />", "</li><br />"], ["<ul>", "</ul>", "<li>", "</li>"], $text);
    $text = str_replace(["<ul><br>", "</ul><br>", "<li><br>", "</li><br>"], ["<ul>", "</ul>", "<li>", "</li>"], $text);
    
    return trim($text);
}

// ==========================================================================
// WYKONANIE ZAPYTANIA: VERTEX AI SEARCH (GŁÓWNY SILNIK RAG)
// ==========================================================================

$botReply = "";
$usingFallback = false;
$saJsonStr = getEnvVar('GCP_SERVICE_ACCOUNT_JSON');

if ($saJsonStr) {
    try {
        $accessToken = getGoogleAccessToken($saJsonStr);
        
        $project_id = "coolfon-project";
        $loc = "eu";
        $engine_id = "coolfon-serwis-bot_1783862426006";
        
        $searchUrl = "https://{$loc}-discoveryengine.googleapis.com/v1/projects/{$project_id}/locations/{$loc}/collections/default_collection/engines/{$engine_id}/servingConfigs/default_search:search";
        
        $preamble = "Jesteś inteligentnym, niezwykle uprzejmym i profesjonalnym asystentem AI lokalnego serwisu GSM Coolfon w Łodzi (ul. Opolczyka 17 lok. C6). "
                  . "Twoim zadaniem jest precyzyjne odpowiadanie na pytania klientów na podstawie udostępnionych dokumentów i cenników. "
                  . "ZŁOTE ZASADY KOMUNIKACJI (TRZYMAJ SIĘ ICH BEZWZGLĘDNIE):\n"
                  . "1. NIGDY nie obiecuj naprawy w 1 godzinę ani w 30 minut. Każda naprawa wymaga indywidualnej diagnozy technicznej.\n"
                  . "2. ZAWSZE podkreślaj, że diagnoza usterki w Coolfon jest w 100% darmowa (0 zł) przy wykonaniu naprawy u nas. W przypadku rezygnacji po wycenie pobierana jest niewielka opłata za czas pracy technika (od 49 zł).\n"
                  . "3. Jeśli klient pyta o nietypową naprawę, rezerwację terminu lub kontakt z człowiekiem, zaproponuj przejście na WhatsApp i powiedz, że klikając przycisk pod czatem lub pisząc na numer +48 532 840 877 połączy się bezpośrednio z technicznym serwisantem.\n"
                  . "4. Pisz zwięźle, strukturalnie, używając emotek dopasowanych do kontekstu (📱, 🛠️, 💰, 📍, ✂️). Pisz wyłącznie po polsku.";

        $payload = [
            "query" => $userMessage,
            "pageSize" => 3,
            "contentSearchSpec" => [
                "summarySpec" => [
                    "summaryResultCount" => 3,
                    "includeCitations" => true,
                    "modelPromptSpec" => [
                        "preamble" => $preamble
                    ]
                ]
            ]
        ];

        $ch = curl_init($searchUrl);
        curl_setopt($ch, CURLOPT_RETURNTRANSFER, true);
        curl_setopt($ch, CURLOPT_POST, true);
        curl_setopt($ch, CURLOPT_POSTFIELDS, json_encode($payload));
        curl_setopt($ch, CURLOPT_HTTPHEADER, [
            "Authorization: Bearer " . $accessToken,
            "Content-Type: application/json"
        ]);
        curl_setopt($ch, CURLOPT_TIMEOUT, 12);
        
        $response = curl_exec($ch);
        $httpCode = curl_getinfo($ch, CURLINFO_HTTP_CODE);
        curl_close($ch);
        
        if ($httpCode === 200) {
            $responseData = json_decode($response, true);
            if (isset($responseData['summary']['summaryText'])) {
                $botReply = $responseData['summary']['summaryText'];
                
                // Oczyszczamy z ewentualnych znaczników cytatów typu [1], [2, 3] dla maksymalnej estetyki UI
                $botReply = preg_replace('/\[\d+(,\s*\d+)*\]/', '', $botReply);
                $botReply = str_replace('  ', ' ', $botReply);
            }
        } else {
            error_log("Vertex Search API error (HTTP $httpCode): " . $response);
        }
        
    } catch (Exception $e) {
        error_log("Exception during Vertex Search execution: " . $e->getMessage());
    }
}

// ==========================================================================
// SYSTEM AWARYJNY (FALLBACK): BEZPOŚREDNIE API GEMINI (AI STUDIO)
// ==========================================================================

if (empty($botReply)) {
    $usingFallback = true;
    $apiKey = getEnvVar('GEMINI_API_KEY');
    
    if ($apiKey) {
        $systemInstruction = "Jesteś inteligentnym, niezwykle uprzejmym i profesjonalnym asystentem AI lokalnego serwisu GSM Coolfon w Łodzi (ul. Opolczyka 17 lok. C6). "
                           . "Twoim celem jest edukowanie klientów, odpowiadanie na pytania dotyczące oferty, cen, dojazdu oraz sprawne przekierowanie na czat WhatsApp serwisu. "
                           . "ZŁOTE ZASADY KOMUNIKACJI:\n"
                           . "1. NIGDY nie obiecuj naprawy w 1 godzinę ani w 30 minut.\n"
                           . "2. ZAWSZE podkreślaj, że diagnoza usterki w Coolfon jest w 100% darmowa (0 zł) przy wykonaniu naprawy u nas. Jeśli klient rezygnuje po wycenie, pobierana jest opłata od 49 zł.\n"
                           . "3. Kiedy klient pyta o ceny konkretnych napraw, podaj orientacyjny zakres cen (np. wymiana ekranu iPhone 13 to ok. 350-450 zł), ale zawsze dodaj, że diagnoza jest darmowa przy naprawie.\n"
                           . "4. Zachęcaj do kliknięcia kontaktu z człowiekiem na WhatsApp pod numerem +48 532 840 877.\n"
                           . "5. Pisz zwięźle, używaj list punktowanych, pogrubień oraz emotek (📱, 🛠️, 💰, 📍, ✂️).";

        $contents = [];
        foreach ($chatHistory as $turn) {
            $role = ($turn['role'] === 'user') ? 'user' : 'model';
            $contents[] = [
                "role" => $role,
                "parts" => [["text" => $turn['text']]]
            ];
        }
        $contents[] = [
            "role" => "user",
            "parts" => [["text" => $userMessage]]
        ];

        $requestData = [
            "contents" => $contents,
            "systemInstruction" => [
                "parts" => [["text" => $systemInstruction]]
            ],
            "generationConfig" => [
                "temperature" => 0.4,
                "maxOutputTokens" => 500,
                "topP" => 0.95
            ]
        ];

        $url = "https://generativelanguage.googleapis.com/v1beta/models/gemini-1.5-flash:generateContent?key=" . $apiKey;

        $ch = curl_init($url);
        curl_setopt($ch, CURLOPT_RETURNTRANSFER, true);
        curl_setopt($ch, CURLOPT_POST, true);
        curl_setopt($ch, CURLOPT_POSTFIELDS, json_encode($requestData));
        curl_setopt($ch, CURLOPT_HTTPHEADER, ["Content-Type: application/json"]);
        curl_setopt($ch, CURLOPT_TIMEOUT, 12);
        
        $response = curl_exec($ch);
        $httpCode = curl_getinfo($ch, CURLINFO_HTTP_CODE);
        curl_close($ch);

        if ($httpCode === 200) {
            $responseData = json_decode($response, true);
            if (isset($responseData['candidates'][0]['content']['parts'][0]['text'])) {
                $botReply = $responseData['candidates'][0]['content']['parts'][0]['text'];
            }
        }
    }
}

// ==========================================================================
// REAKCJA NA BRAK JAKIEJKOLWIEK ODPOWIEDZI (ZASADA PROAKTYWNEJ WERYFIKACJI)
// ==========================================================================

if (empty($botReply)) {
    echo json_encode([
        "status" => "error",
        "reply" => "Przepraszam, chwilowo mam trudności techniczne z dostępem do mojego cyfrowego mózgu. 🧠 Skontaktuj się z nami bezpośrednio przez WhatsApp lub zadzwoń pod numer <b>+48 532 840 877</b> – chętnie pomożemy Ci od ręki! 📞"
    ]);
    exit;
}

// ==========================================================================
// FORMATOWANIE I ZWRÓCENIE ODPOWIEDZI
// ==========================================================================

$_SESSION['chat_query_count']++;
$cleanReply = cleanAndHumanizeMarkdown($botReply);

echo json_encode([
    "status" => "success",
    "using_fallback" => $usingFallback,
    "reply" => $cleanReply
]);
?>
