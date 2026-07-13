<?php
header("Access-Control-Allow-Origin: *");
header("Access-Control-Allow-Headers: Content-Type");
header("Content-Type: application/json");

// Funkcja wczytywania zmiennych .env (obejście putenv na Hostido / Cloud Run)
function getEnvVar($name) {
    if (isset($_ENV[$name])) return $_ENV[$name];
    if (isset($_SERVER[$name])) return $_SERVER[$name];
    $val = getenv($name);
    return $val !== false ? $val : null;
}

// Inicjalizacja sesji pod Spam Shields
if (session_status() === PHP_SESSION_NONE) {
    ini_set('session.cookie_httponly', 1);
    ini_set('session.use_only_cookies', 1);
    session_start();
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

// Konwersja Markdown -> HTML (Zasada 13)
function cleanAndHumanizeMarkdown($text) {
    // Zamiana pogrubień i kursyw
    $text = preg_replace('/\*\*(.*?)\*\*/', '<strong>$1</strong>', $text);
    $text = preg_replace('/\*(.*?)\*/', '<em>$1</em>', $text);
    
    // Parsowanie list nienumerowanych
    $lines = explode("\n", $text);
    $inList = false;
    $htmlLines = [];
    foreach ($lines as $line) {
        $trimmed = trim($line);
        if (preg_match('/^[\*\-\x{2022}]\s+(.*)$/u', $trimmed, $matches)) {
            if (!$inList) { $htmlLines[] = '<ul>'; $inList = true; }
            $htmlLines[] = '<li>' . $matches[1] . '</li>';
        } else {
            if ($inList) { $htmlLines[] = '</ul>'; $inList = false; }
            $htmlLines[] = $line;
        }
    }
    if ($inList) $htmlLines[] = '</ul>';
    return nl2br(implode("\n", $htmlLines));
}

// Właściwe odpytanie Vertex AI Search (REST API)
$saJsonStr = getEnvVar('GCP_SERVICE_ACCOUNT_JSON');
if (!$saJsonStr) {
    echo json_encode(["status" => "success", "reply" => "Przepraszam, konfiguracja autoryzacji bota (GCP_SERVICE_ACCOUNT_JSON) jest tymczasowo niedostępna na serwerze."]);
    exit;
}

try {
    $accessToken = getGoogleAccessToken($saJsonStr);
    
    // Pobranie konfiguracji ze zmiennych środowiskowych
    $project_id = getEnvVar('GCP_PROJECT_AGENCY') ?? "holistic-dashboard-dev";
    $loc = "global";
    $host = ($loc === "global") ? "discoveryengine.googleapis.com" : "{$loc}-discoveryengine.googleapis.com";
    $engine_id = getEnvVar('VERTEX_ENGINE_AGENCY') ?? "holistic-search-app_1780143991783";
    
    $searchUrl = "https://{$host}/v1/projects/{$project_id}/locations/{$loc}/collections/default_collection/engines/{$engine_id}/servingConfigs/default_search:search";
    
    $payload = json_encode([
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
    curl_setopt($ch, CURLOPT_POSTFIELDS, $payload);
    curl_setopt($ch, CURLOPT_HTTPHEADER, [
        "Authorization: Bearer " . $accessToken,
        "Content-Type: application/json"
    ]);
    $response = curl_exec($ch);
    $httpCode = curl_getinfo($ch, CURLINFO_HTTP_CODE);
    curl_close($ch);

    if ($httpCode !== 200) {
        throw new Exception("Błąd API Google Discovery Engine! Kod HTTP: " . $httpCode . " Odpowiedź: " . $response);
    }

    $resData = json_decode($response, true);
    $reply = $resData['summary']['summaryText'] ?? "";
    
    if (empty($reply)) {
        $reply = "Nie znalazłem precyzyjnej odpowiedzi w mojej bazie wiedzy. Możesz skontaktować się ze mną bezpośrednio przez e-mail: hello@jaison.pl lub napisać do mnie na WhatsApp!";
    }

    echo json_encode([
        "status" => "success",
        "reply" => cleanAndHumanizeMarkdown($reply)
    ]);

} catch (Exception $e) {
    echo json_encode([
        "status" => "success",
        "reply" => "Przepraszam, wystąpił chwilowy błąd techniczny podczas łączenia z chmurą Google: " . $e->getMessage() . ". Skontaktuj się ze mną bezpośrednio pod adresem hello@jaison.pl! 📞"
    ]);
}
