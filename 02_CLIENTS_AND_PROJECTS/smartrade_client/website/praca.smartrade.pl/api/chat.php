<?php
// PHP Squeeze Page Rekrutacja API - proxy pośredniczące z Gemini API

header('Content-Type: application/json; charset=utf-8');
header('Access-Control-Allow-Origin: *');
header('Access-Control-Allow-Methods: POST, OPTIONS');
header('Access-Control-Allow-Headers: Content-Type');

if ($_SERVER['REQUEST_METHOD'] === 'OPTIONS') {
    exit(0);
}

// 1. Load config
$configFile = __DIR__ . '/config.php';
if (!file_exists($configFile)) {
    echo json_encode([
        'reply' => 'Błąd serwera: brak pliku konfiguracyjnego. Skontaktuj się z administratorem.',
        'qualified' => false
    ]);
    exit();
}

$config = require $configFile;

if (empty($config['gemini_api_key'])) {
    echo json_encode([
        'reply' => 'Wystąpił błąd autoryzacji: brak klucza Google AI Studio w konfiguracji.',
        'qualified' => false
    ]);
    exit();
}

// 2. Read request body
$inputRaw = file_get_contents('php://input');
$input = json_decode($inputRaw, true);

if (empty($input['history']) || !is_array($input['history'])) {
    echo json_encode([
        'reply' => 'Hej, napisz mi coś więcej, żebym mógł lepiej Cię poznać!',
        'qualified' => false
    ]);
    exit();
}

// 3. Define System Prompt for rekrutacja (Strict VAK copy guidelines + anti-addiction guard)
$systemPrompt = "Jesteś Bot HR, rekruterem i asystentem Jurka, który organizuje pracę dla polskich i wschodnioeuropejskich fachowców w słonecznej Gandii w Hiszpanii. Twoim jedynym celem jest zakwalifikowanie lub odrzucenie kandydata na podstawie 4 głównych kryteriów i skierowanie go na WhatsApp do Jurka.

Kryteria kwalifikacji:
1. SPECJALIZACJA: Szukamy głównie glazurników (płytkarzy) i hydraulików do prac wykończeniowych w prywatnych apartamentach i kamienicach u klientów.
2. DOŚWIADCZENIE: Kandydat musi posiadać faktyczne umiejętności i doświadczenie w zawodzie (mieć wyrobioną rękę).
3. TRZEŹWOŚĆ / ALKOHOL: Warunek absolutnie krytyczny. Oczekujemy 100% rzetelności, sumienności i braku nałogów. Jeśli kandydat wspomni, że ma problem z alkoholem, bawi się hucznie lub nie potrafi nad tym zapanować - musisz go uprzejmie, ale stanowczo odrzucić. Nie tolerujemy pijaństwa w pracy.
4. GOTOWOŚĆ / STAN WOLNY: Praca jest w Hiszpanii (Gandia). Mile widziane osoby stanu wolnego lub bez silnych zobowiązań w Polsce, które lubią hiszpański ciepły klimat.

Twoje zachowanie i styl:
- Komunikuj się wyłącznie w języku polskim.
- Pisz krótko, energicznie, perswazyjnie. Używaj estetycznego języka zmysłów (VAK): wizualizuj słońce, ciepło, spokój, wysokie zarobki do 1200 zł dziennie.
- Prowadź wywiad krok po kroku. Nie zadawaj wszystkich pytań na raz! Zadawaj jedno pytanie, czekaj na odpowiedź i dopiero wtedy kontynuuj.
- Bądź przyjazny, ale czujny. Wyłapuj sygnały ostrzegawcze (brak szacunku, niechęć do pracy, krętactwo).

Kiedy uznać, że kandydat jest ZAKWALIFIKOWANY:
Gdy odpowie na Twoje pytania dotyczące doświadczenia, potwierdzi pełną trzeźwość i gotowość do wyjazdu, a Ty uznasz go za rzetelnego faceta.
Wtedy i TYLKO WTEDY musisz wygenerować odpowiedź, która w formacie JSON powiadomi aplikację, że kandydat przeszedł rekrutację.

Kiedy uznać, że kandydat jest ODRZUCONY:
Jeśli przyzna się do nałogów, nie szanuje warunku trzeźwości lub nie ma żadnego doświadczenia budowlanego.

PROCEUDRA ZWROTU JSON:
Na końcu każdej swojej odpowiedzi musisz dodać unikalny znacznik sterujący w formacie JSON w nowej linii, który pomoże silnikowi PHP określić status kandydata.
Format znacznika (dołącz go na samym końcu odpowiedzi, bez znaczników kodu markdown, np. ```json):
[STATUS_DATA: {\"qualified\": true/false, \"summary\": \"Krótkie streszczenie kandydata np: Jan Kowalski, Glazurnik 5 lat exp, bez nałogów, gotowy od zaraz.\"}]";

// 4. Format history for Gemini Developer API (Google AI Studio REST endpoint)
$contents = [];
foreach ($input['history'] as $msg) {
    // Gemini roles: user, model
    $role = $msg['role'] === 'user' ? 'user' : 'model';
    $contents[] = [
        'role' => $role,
        'parts' => [
            ['text' => $msg['content']]
        ]
    ];
}

// Prepare payload (using system_instruction payload standard for Gemini API)
$payload = [
    'contents' => $contents,
    'systemInstruction' => [
        'parts' => [
            ['text' => $systemPrompt]
        ]
    ],
    'generationConfig' => [
        'temperature' => 0.7,
        'maxOutputTokens' => 800,
    ]
];

// 5. Send cURL request to Google AI Studio
$apiKey = $config['gemini_api_key'];
$url = "https://generativelanguage.googleapis.com/v1beta/models/gemini-2.5-flash:generateContent?key=" . $apiKey;

$ch = curl_init($url);
curl_setopt($ch, CURLOPT_RETURNTRANSFER, true);
curl_setopt($ch, CURLOPT_POST, true);
curl_setopt($ch, CURLOPT_POSTFIELDS, json_encode($payload));
curl_setopt($ch, CURLOPT_HTTPHEADER, [
    'Content-Type: application/json'
]);

$responseRaw = curl_exec($ch);
$httpCode = curl_getinfo($ch, CURLINFO_HTTP_CODE);
$curlError = curl_error($ch);
curl_close($ch);

if ($httpCode !== 200) {
    echo json_encode([
        'reply' => 'Przepraszamy, połączenie z systemem rekrutacji zostało przerwane. Spróbuj ponownie za chwilę lub napisz bezpośrednio do Jurka na WhatsApp.',
        'qualified' => false,
        'debug_error' => 'HTTP Code: ' . $httpCode . ' | Response: ' . $responseRaw . ' | cURL Error: ' . $curlError
    ]);
    exit();
}

$responseArr = json_decode($responseRaw, true);
$botReply = "";

if (!empty($responseArr['candidates'][0]['content']['parts'][0]['text'])) {
    $botReply = $responseArr['candidates'][0]['content']['parts'][0]['text'];
} else {
    $botReply = "Przepraszam, nie zrozumiałem. Możesz powtórzyć?";
}

// 6. Parse status from response text (extracting [STATUS_DATA: ...])
$qualified = false;
$summary = "";

if (preg_match('/\[STATUS_DATA:\s*({.*?})\]/s', $botReply, $matches)) {
    $statusJson = json_decode($matches[1], true);
    if ($statusJson) {
        $qualified = isset($statusJson['qualified']) ? (bool)$statusJson['qualified'] : false;
        $summary = isset($statusJson['summary']) ? $statusJson['summary'] : "";
    }
    // Clean up the JSON block from user facing reply
    $botReply = preg_replace('/\[STATUS_DATA:\s*({.*?})\]/s', '', $botReply);
}

// Return clean response
echo json_encode([
    'reply' => trim($botReply),
    'qualified' => $qualified,
    'summary' => $summary
]);
