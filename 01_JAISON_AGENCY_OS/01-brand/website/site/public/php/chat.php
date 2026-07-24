<?php
header("Access-Control-Allow-Origin: *");
header("Access-Control-Allow-Headers: Content-Type");
header("Content-Type: application/json");

// Inicjalizacja sesji pod Spam Shields
if (session_status() === PHP_SESSION_NONE) {
    ini_set('session.cookie_httponly', 1);
    ini_set('session.use_only_cookies', 1);
    session_start();
}

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

// Konwersja Markdown -> HTML (Zasada 13 - Bezwyjątkowe usuwanie gwiazdek)
function cleanAndHumanizeMarkdown($text) {
    $text = preg_replace('/\*\*(.*?)\*\*/', '<strong>$1</strong>', $text);
    $text = preg_replace('/\*(.*?)\*/', '<em>$1</em>', $text);
    $text = str_replace('**', '', $text);
    $text = str_replace('*', '', $text);
    return nl2br($text);
}

// Pobranie klucza SA z serwera
$saJsonStr = getEnvVar('GCP_SERVICE_ACCOUNT_JSON');

// Jeśli brak klucza GCP w PHP, uderzamy awaryjnie do n8n webhooka (v1/jaison-audit)
function queryN8nFallback($userMessage) {
    $n8nUrl = "https://n8n.jaison.pl/webhook/v1/jaison-audit";
    $payload = json_encode([
        "message" => $userMessage,
        "name" => "Klient WWW",
        "email" => "kontakt-www@jaison.pl"
    ]);

    $ch = curl_init($n8nUrl);
    curl_setopt($ch, CURLOPT_RETURNTRANSFER, true);
    curl_setopt($ch, CURLOPT_POST, true);
    curl_setopt($ch, CURLOPT_POSTFIELDS, $payload);
    curl_setopt($ch, CURLOPT_HTTPHEADER, ["Content-Type: application/json"]);
    curl_setopt($ch, CURLOPT_TIMEOUT, 8);
    $response = curl_exec($ch);
    $code = curl_getinfo($ch, CURLINFO_HTTP_CODE);
    curl_close($ch);

    if ($code === 200 && !empty($response)) {
        $data = json_decode($response, true);
        if (isset($data['reply'])) return $data['reply'];
        if (isset($data['text'])) return $data['text'];
    }
    return null;
}

if (!$saJsonStr) {
    $n8nReply = queryN8nFallback($userMessage);
    if ($n8nReply) {
        echo json_encode(["status" => "success", "reply" => cleanAndHumanizeMarkdown($n8nReply)]);
        exit;
    }
    
    // Zapytanie o charakterze powitalnym / audytowym
    echo json_encode([
        "status" => "success",
        "reply" => "Cześć! Jestem <strong>Jasiek AI</strong> — wirtualny architekt systemów i prawa ręka Tomasza Dudy (jaison.pl). Pomagam przedsiębiorcom uwalniać czas i likwidować chaos w firmie. <br/><br/>W czym dziś ucieka Ci najwięcej energii? Oferujemy m.in.:<br/>- <strong>AI Quick Win (4 900 PLN)</strong><br/>- <strong>AI Operator OS (8 900 PLN)</strong><br/>- <strong>Architecture Sprint (6 900 PLN)</strong><br/>- <strong>AI Boardroom (od 15 000 PLN)</strong><br/><br/>Zostaw wiadomość lub napisz bezpośrednio do Tomasza na <strong>hello@jaison.pl</strong> lub WhatsApp: <strong>+48 791 636 644</strong>! 📞"
    ]);
    exit;
}

// Jeśli GCP SA istnieje, kontynuujemy z bezpośrednim API Vertex AI Gemini 2.5 Flash
try {
    $sa = json_decode($saJsonStr, true);
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

    $signatureInput = str_replace(['+', '/', '='], ['-', '_', ''], base64_encode($header)) . "." . str_replace(['+', '/', '='], ['-', '_', ''], base64_encode($payload));
    $signature = '';
    openssl_sign($signatureInput, $signature, $privateKey, 'SHA256');
    $jwt = $signatureInput . "." . str_replace(['+', '/', '='], ['-', '_', ''], base64_encode($signature));

    $ch = curl_init("https://oauth2.googleapis.com/token");
    curl_setopt($ch, CURLOPT_RETURNTRANSFER, true);
    curl_setopt($ch, CURLOPT_POST, true);
    curl_setopt($ch, CURLOPT_POSTFIELDS, http_build_query([
        'grant_type' => 'urn:ietf:params:oauth:grant-type:jwt-bearer',
        'assertion' => $jwt
    ]));
    $res = curl_exec($ch);
    curl_close($ch);
    $tokenData = json_decode($res, true);
    $accessToken = $tokenData['access_token'] ?? null;

    if (!$accessToken) {
        throw new Exception("Nie udało się uzyskać access tokena.");
    }

    $project_id = getEnvVar('GCP_PROJECT_AGENCY') ?? "holistic-dashboard-dev";
    $geminiUrl = "https://us-central1-aiplatform.googleapis.com/v1/projects/{$project_id}/locations/us-central1/publishers/google/models/gemini-2.5-flash:generateContent";

    $systemInstruction = "Jesteś Jasiek AI — wirtualny architekt systemów w agencji jaison.pl. Rozmawiasz z przedsiębiorcami krótko, bezpośrednio, bez bełkotu korporacyjnego. Stosujesz NLP VAK. Używasz tagów <strong> zamiast gwiazdek. Oferujesz pakiety: AI Quick Win (4900 PLN), AI Operator OS (8900 PLN), Architecture Sprint (6900 PLN), AI Boardroom (od 15000 PLN). Zachęcasz do konsultacji z Tomaszem: hello@jaison.pl / +48 791 636 644.";

    $geminiPayload = json_encode([
        "contents" => [
            ["role" => "user", "parts" => [["text" => $userMessage]]]
        ],
        "systemInstruction" => [
            "parts" => [["text" => $systemInstruction]]
        ],
        "generationConfig" => [
            "temperature" => 0.7,
            "maxOutputTokens" => 500
        ]
    ]);

    $ch2 = curl_init($geminiUrl);
    curl_setopt($ch2, CURLOPT_RETURNTRANSFER, true);
    curl_setopt($ch2, CURLOPT_POST, true);
    curl_setopt($ch2, CURLOPT_POSTFIELDS, $geminiPayload);
    curl_setopt($ch2, CURLOPT_HTTPHEADER, [
        "Authorization: Bearer " . $accessToken,
        "Content-Type: application/json"
    ]);
    $geminiResponse = curl_exec($ch2);
    $httpCode = curl_getinfo($ch2, CURLINFO_HTTP_CODE);
    curl_close($ch2);

    if ($httpCode === 200) {
        $data = json_decode($geminiResponse, true);
        $reply = $data['candidates'][0]['content']['parts'][0]['text'] ?? null;
        if ($reply) {
            echo json_encode(["status" => "success", "reply" => cleanAndHumanizeMarkdown($reply)]);
            exit;
        }
    }

    $n8nReply = queryN8nFallback($userMessage);
    if ($n8nReply) {
        echo json_encode(["status" => "success", "reply" => cleanAndHumanizeMarkdown($n8nReply)]);
        exit;
    }

    echo json_encode(["status" => "success", "reply" => "Cześć! Jestem <strong>Jasiek AI</strong>. W czym mogę Ci dzisiaj pomóc w kwestii automatyzacji i wdrożeń AI? Skontaktuj się bezpośrednio z Tomaszem pod adresem <strong>hello@jaison.pl</strong>! 📞"]);

} catch (Exception $e) {
    $n8nReply = queryN8nFallback($userMessage);
    if ($n8nReply) {
        echo json_encode(["status" => "success", "reply" => cleanAndHumanizeMarkdown($n8nReply)]);
        exit;
    }
    echo json_encode(["status" => "success", "reply" => "Witaj! Jestem <strong>Jasiek AI</strong>. Przepraszam za chwilową przerwę. Skontaktuj się ze mną bezpośrednio na <strong>hello@jaison.pl</strong>! 📞"]);
}
