<?php
header("Access-Control-Allow-Origin: *");
header("Access-Control-Allow-Headers: Content-Type");
header("Content-Type: application/json");

// Inicjalizacja sesji pod Spam Shields i utrzymanie historii sesji Dialogflow CX
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

// TARCZA 1: Honeypot (Antyspam)
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
    echo json_encode(["status" => "success", "reply" => "Przekroczyłeś dobowy limit zapytań do bota. Skontaktuj się z nami bezpośrednio na <b>WhatsApp</b>: https://wa.me/48791636644 📞"]);
    exit;
}
$_SESSION['chat_query_count']++;

// Generowanie unikalnego ID sesji pod Dialogflow CX
if (!isset($_SESSION['df_session_id'])) {
    $_SESSION['df_session_id'] = "session_" . bin2hex(random_bytes(8));
}
$sessionId = $_SESSION['df_session_id'];

// Funkcja czyszczenia Markdown -> HTML (Zasada 13 - Używanie <strong> zamiast **)
function cleanAndHumanizeMarkdown($text) {
    $text = preg_replace('/\*\*(.*?)\*\*/', '<strong>$1</strong>', $text);
    $text = preg_replace('/\*(.*?)\*/', '<em>$1</em>', $text);
    $text = str_replace('**', '', $text);
    $text = str_replace('*', '', $text);
    return nl2br($text);
}

// Awaryjne połączenie z produkcyjnym n8n webhookiem
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

// Identyfikatory Produkcyjne Agenta Dialogflow CX z GCP
$projectId = "jaison-chatbot-www-503310";
$locationId = "europe-west1";
$agentId = "e1c84bd4-5bad-4ebb-8b22-f5e9624d434d";

$saJsonStr = getEnvVar('GCP_SERVICE_ACCOUNT_JSON');

if (!$saJsonStr) {
    $n8nReply = queryN8nFallback($userMessage);
    if ($n8nReply) {
        echo json_encode(["status" => "success", "reply" => cleanAndHumanizeMarkdown($n8nReply)]);
        exit;
    }
    
    echo json_encode([
        "status" => "success",
        "reply" => "Cześć! Jestem <strong>Jasiek AI</strong> — wirtualny architekt systemów jaison.pl. Pomagam przedsiębiorcom uwalniać czas i likwidować chaos operacyjny.<br/><br/>Jakiego rozwiązania szukasz? W czym ucieka Ci dziś najwięcej energii?<br/>- <strong>AI Quick Win (4 900 PLN)</strong><br/>- <strong>AI Operator OS (8 900 PLN)</strong><br/>- <strong>Architecture Sprint (6 900 PLN)</strong><br/>- <strong>AI Boardroom (od 15 000 PLN)</strong><br/><br/>Napisz bezpośrednio do Tomasza na <strong>hello@jaison.pl</strong> lub WhatsApp: <strong>+48 791 636 644</strong>! 📞"
    ]);
    exit;
}

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
        throw new Exception("Brak access tokena.");
    }

    // Wywołanie produkcyjnego API Dialogflow CX (Playbook Jasiek Chatbot)
    $dfUrl = "https://{$locationId}-dialogflow.googleapis.com/v3/projects/{$projectId}/locations/{$locationId}/agents/{$agentId}/sessions/{$sessionId}:detectIntent";

    $dfPayload = json_encode([
        "queryInput" => [
            "text" => [
                "text" => $userMessage
            ],
            "languageCode" => "pl"
        ]
    ]);

    $ch2 = curl_init($dfUrl);
    curl_setopt($ch2, CURLOPT_RETURNTRANSFER, true);
    curl_setopt($ch2, CURLOPT_POST, true);
    curl_setopt($ch2, CURLOPT_POSTFIELDS, $dfPayload);
    curl_setopt($ch2, CURLOPT_HTTPHEADER, [
        "Authorization: Bearer " . $accessToken,
        "Content-Type: application/json"
    ]);
    $dfResponse = curl_exec($ch2);
    $httpCode = curl_getinfo($ch2, CURLINFO_HTTP_CODE);
    curl_close($ch2);

    if ($httpCode === 200) {
        $data = json_decode($dfResponse, true);
        $responseMessages = $data['queryResult']['responseMessages'] ?? [];
        $combinedReply = [];
        
        foreach ($responseMessages as $msgObj) {
            if (isset($msgObj['text']['text'])) {
                foreach ($msgObj['text']['text'] as $t) {
                    $combinedReply[] = $t;
                }
            }
        }

        if (!empty($combinedReply)) {
            $finalText = implode("<br/><br/>", $combinedReply);
            echo json_encode(["status" => "success", "reply" => cleanAndHumanizeMarkdown($finalText)]);
            exit;
        }
    }

    // Jeśli Dialogflow CX zwrócił pustą odpowiedź, próbujemy n8n fallback
    $n8nReply = queryN8nFallback($userMessage);
    if ($n8nReply) {
        echo json_encode(["status" => "success", "reply" => cleanAndHumanizeMarkdown($n8nReply)]);
        exit;
    }

    echo json_encode(["status" => "success", "reply" => "Cześć! Jestem <strong>Jasiek AI</strong>. W czym mogę Ci dzisiaj pomóc w kwestii automatyzacji? Skontaktuj się ze mną na <strong>hello@jaison.pl</strong>! 📞"]);

} catch (Exception $e) {
    $n8nReply = queryN8nFallback($userMessage);
    if ($n8nReply) {
        echo json_encode(["status" => "success", "reply" => cleanAndHumanizeMarkdown($n8nReply)]);
        exit;
    }
    echo json_encode(["status" => "success", "reply" => "Witaj! Jestem <strong>Jasiek AI</strong>. Skontaktuj się ze mną bezpośrednio na <strong>hello@jaison.pl</strong>! 📞"]);
}
