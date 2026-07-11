<?php
/* ==========================================================================
   COOLFON.PL — SECURE CHATBOT BACKEND PROXY (PHP + GEMINI API)
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
            if (!array_key_exists($name, $_SERVER) && !array_key_exists($name, $_ENV)) {
                putenv("{$name}={$value}");
                $_ENV[$name] = $value;
                $_SERVER[$name] = $value;
            }
        }
    }
}

// Wczytaj plik .env znajdujący się poziom wyżej (w katalogu głównym)
loadEnv(__DIR__ . '/../.env');

$apiKey = getenv('GEMINI_API_KEY');

if (!$apiKey) {
    // Jeśli brak klucza API, przekaż czytelny błąd i instrukcję dla programisty / użytkownika
    http_response_code(500);
    echo json_encode([
        "status" => "error", 
        "message" => "Brak klucza API Gemini w pliku .env! Skonfiguruj GEMINI_API_KEY w głównym folderze.",
        "reply" => "Przepraszam, chwilowo mam trudności z połączeniem z moim cyfrowym mózgiem. Poinformuj obsługę o braku konfiguracji klucza API!"
    ]);
    exit;
}

if ($_SERVER["REQUEST_METHOD"] !== "POST") {
    http_response_code(405);
    echo json_encode(["status" => "error", "message" => "Method Not Allowed"]);
    exit;
}

// 2. Pobranie danych wejściowych (obecna wiadomość i historia konwersacji)
$input = json_decode(file_get_contents("php://input"), true);
if (!$input || !isset($input['message'])) {
    http_response_code(400);
    echo json_encode(["status" => "error", "message" => "Brak wymaganej wiadomości użytkownika."]);
    exit;
}

$userMessage = trim($input['message']);
$chatHistory = isset($input['history']) ? $input['history'] : [];

// 3. Budowanie System Promptu (Bazy Wiedzy Asystenta Coolfon GSM)
$systemInstruction = "Jesteś inteligentnym, niezwykle uprzejmym i profesjonalnym asystentem AI lokalnego serwisu GSM Coolfon w Łodzi (ul. Opolczyka 17 lok. C6). 
Twoim celem jest edukowanie klientów, odpowiadanie na pytania dotyczące oferty, cen, dojazdu oraz sprawne i naturalne przekierowanie klienta na czat WhatsApp serwisu, gdy o to poprosi lub gdy sprawa wymaga indywidualnej wyceny.

ZŁOTE ZASADY KOMUNIKACJI (TRZYMAJ SIĘ ICH BEZWZGLĘDNIE):
1. NIGDY nie obiecuj naprawy w 1 godzinę ani w 30 minut. Każda naprawa jest kwestią indywidualnej diagnozy technicznej.
2. ZAWSZE podkreślaj, że diagnoza usterki w Coolfon jest w 100% darmowa (0 zł) przy wykonaniu naprawy u nas. Jeśli klient po wycenie zrezygnuje z naprawy, pobierana jest niewielka opłata za czas pracy technika (od 49 zł).
3. Kiedy klient pyta o ceny konkretnych napraw, podaj orientacyjny zakres cen (np. wymiana ekranu iPhone 13 to ok. 350-450 zł, iPhone 14 to ok. 500-600 zł), ale zawsze dodaj, że diagnoza jest w 100% darmowa przy naprawie. Możesz też polecić skorzystanie z kalkulatora na naszej stronie głównej lub podstrony /cennik/.
4. Gdy klient poprosi o kontakt z człowiekiem, serwisantem, rezerwację terminu lub zapyta o nietypową naprawę, zaproponuj przejście na WhatsApp i powiedz, że klikając przycisk pod czatem lub pisząc na numer +48 532 840 877 połączy się bezpośrednio z technicznym serwisantem.
5. Pisz zwięźle, strukturalnie (używaj list punktowanych, pogrubień dla kluczowych słów) i dbaj o to, by tekst był przejrzysty (ADHD-friendly). Używaj emotek pasujących do kontekstu (📱, 🛠️, 💰, 📍, ✂️).

DANE O SERWISIE COOLFON GSM SP. Z O.O.:
- Adres: ul. Księcia Władysława Opolczyka 17 lok. C6, 92-417 Łódź (Park Handlowy Olechów). Przed wejściem jest duży, darmowy parking.
- Godziny pracy: Poniedziałek – Piątek: 10:00 – 19:00, Sobota: 09:00 – 15:00, Niedziela: Zamknięte.
- Telefon / WhatsApp: +48 532 840 877 (Link: https://wa.me/48532840877).
- Główna oferta: 
  * Kompleksowa naprawa telefonów, tabletów, smartwatchy (wymiana szybki, ekranu LCD, baterii, gniazda ładowania USB-C, naprawa po zalaniu) wszystkich marek: Apple (iPhone, iPad, Apple Watch), Samsung (Galaxy S, A, Z), Xiaomi (Redmi, POCO), Motorola, Huawei, Realme itd.
  * Usługa ULTRA bezpiecznego zabezpieczania ekranów foliami na wymiar: Docinamy profesjonalnym ploterem na miejscu folie hydrożelowe i hybrydowe na ekrany telefonów, tabletów, smartwatchy, a także ekrany samochodowe (GPS), konsole i inne nietypowe wyświetlacze. Montaż na miejscu w cenie folii!
  * Sklep stacjonarny: Akcesoria GSM, ładowarki, kable, etui/case ochronne, szkła hartowane, uchwyty samochodowe.

Formatuj odpowiedzi w czystym HTML (używaj <br> do nowych linii, <b></b> do pogrubień, wypunktowań <ul><li></li></ul>), ponieważ ten tekst będzie bezpośrednio wstrzykiwany do okna czatu.";

// 4. Konstruowanie struktury żądania zgodnego z oficjalną dokumentacją Gemini API v1beta
$contents = [];

// Dodanie historii czatu w formacie Gemini (user -> model -> user)
foreach ($chatHistory as $turn) {
    $role = ($turn['role'] === 'user') ? 'user' : 'model';
    $contents[] = [
        "role" => $role,
        "parts" => [
            ["text" => $turn['text']]
        ]
    ];
}

// Dodanie najnowszej wiadomości użytkownika na koniec historii
$contents[] = [
    "role" => "user",
    "parts" => [
        ["text" => $userMessage]
    ]
];

// Przygotowanie całego payloadu
$requestData = [
    "contents" => $contents,
    "systemInstruction" => [
        "parts" => [
            ["text" => $systemInstruction]
        ]
    ],
    "generationConfig" => [
        "temperature" => 0.4,
        "maxOutputTokens" => 500,
        "topP" => 0.95
    ]
];

// 5. Wysłanie zapytania cURL do Gemini API (używamy stabilnego modelu gemini-1.5-flash)
$url = "https://generativelanguage.googleapis.com/v1beta/models/gemini-1.5-flash:generateContent?key=" . $apiKey;

$ch = curl_init($url);
curl_setopt($ch, CURLOPT_RETURNTRANSFER, true);
curl_setopt($ch, CURLOPT_POST, true);
curl_setopt($ch, CURLOPT_POSTFIELDS, json_encode($requestData));
curl_setopt($ch, CURLOPT_HTTPHEADER, [
    "Content-Type: application/json"
]);

// Obsługa ewentualnego timeoutu (limit do 15 sekund na szybką reakcję)
curl_setopt($ch, CURLOPT_TIMEOUT, 15);

$response = curl_exec($ch);
$httpCode = curl_getinfo($ch, CURLINFO_HTTP_CODE);

if (curl_errno($ch)) {
    $errorMsg = curl_error($ch);
    curl_close($ch);
    http_response_code(500);
    echo json_encode([
        "status" => "error",
        "message" => "Błąd połączenia cURL: " . $errorMsg,
        "reply" => "Przepraszam, mam mały problem techniczny z połączeniem. Możesz skontaktować się z nami bezpośrednio przez telefon lub WhatsApp pod numerem <b>+48 532 840 877</b>! 📞"
    ]);
    exit;
}

curl_close($ch);

// 6. Parsowanie odpowiedzi i wyłuskanie tekstu bota
$responseData = json_decode($response, true);

if ($httpCode !== 200 || !isset($responseData['candidates'][0]['content']['parts'][0]['text'])) {
    http_response_code($httpCode ?: 500);
    
    // Logowanie błędów API dla administratora w odpowiedzi JSON (szczególnie przydatne przy złym kluczu API)
    $apiError = isset($responseData['error']['message']) ? $responseData['error']['message'] : "Unknown API Error";
    
    echo json_encode([
        "status" => "error",
        "http_code" => $httpCode,
        "api_error" => $apiError,
        "reply" => "Przepraszam, mój silnik AI zgłosił błąd autoryzacji lub limitu zapytań. Zachęcam do kontaktu bezpośrednio na nasz numer: <b>+48 532 840 877</b> 📞 lub przez WhatsApp!"
    ]);
    exit;
}

$botReply = $responseData['candidates'][0]['content']['parts'][0]['text'];

// Zwrócenie oczyszczonej, profesjonalnej odpowiedzi
echo json_encode([
    "status" => "success",
    "reply" => trim($botReply)
]);
?>
