<?php
header("Content-Type: application/json; charset=utf-8");
header("Access-Control-Allow-Origin: *");
header("Access-Control-Allow-Methods: POST, OPTIONS");
header("Access-Control-Allow-Headers: Content-Type");

if ($_SERVER['REQUEST_METHOD'] === 'OPTIONS') {
    exit(0);
}

if ($_SERVER['REQUEST_METHOD'] !== 'POST') {
    echo json_encode(["error" => "Method not allowed"]);
    exit;
}

$input = file_get_contents("php://input");
$data = json_decode($input, true);

if (!isset($data['message'])) {
    echo json_encode(["error" => "Brak wiadomości."]);
    exit;
}

// 1. Load API Key securely from same directory json file
$apiKey = null;
$configFile = __DIR__ . '/gemini_config.json';
if (file_exists($configFile)) {
    $config = json_decode(file_get_contents($configFile), true);
    if (isset($config['api_key'])) {
        $apiKey = $config['api_key'];
    }
}

if (!$apiKey || $apiKey === "YOUR_GEMINI_API_KEY_HERE" || $apiKey === "TWÓJ_KLUCZ_API") {
    // Return a safe friendly response on frontend if API key is missing. No public instructions shown!
    echo json_encode([
        "response" => "Cześć! Chwilowo odpoczywam. Wpisz 'menu', aby zobaczyć nasze pyszne dania lub 'kontakt' aby się z nami skontaktować! 🍗",
        "debug_error" => "Brak klucza API Gemini w gemini_config.json na serwerze. Dodaj klucz, aby aktywować sztuczną inteligencję."
    ]);
    exit;
}

$userMessage = $data['message'];
$history = isset($data['history']) ? $data['history'] : [];

// 2. Prepare contents
$contents = [];
foreach ($history as $msg) {
    if (isset($msg['role']) && isset($msg['text'])) {
        $contents[] = [
            "role" => $msg['role'] === 'user' ? 'user' : 'model',
            "parts" => [
                ["text" => $msg['text']]
            ]
        ];
    }
}
$contents[] = [
    "role" => "user",
    "parts" => [
        ["text" => $userMessage]
    ]
];

// 3. System Instruction with full menu wstrzykniętym przy kompilacji
$systemInstruction = "Jesteś JaśBot – wirtualny asystent Baru Jaś (ul. Rokicińska 190/214, Łódź, Widzew). Twój styl komunikacji jest niezwykle przyjazny, ciepły, z poczuciem humoru i retro-modernistycznym zacięciem. Używaj emotek (np. 🍗, 🍟, 🥤, 👑) w naturalny sposób.\n\n"
    . "Informacje o firmie:\n"
    . "- Adres: ul. Rokicińska 190/214, 92-412 Łódź (tuż obok Selgros, Widzew).\n"
    . "- Godziny otwarcia: Poniedziałek - Sobota: 09:00 - 19:00, Niedziela: nieczynne.\n"
    . "- Telefon: 663 970 016 (Marysia).\n"
    . "- Metody płatności: Gotówka, Karta, oraz BLIK na telefon (numer: 663 970 016). Zachęcaj do składania zamówień przez interaktywne menu.\n"
    . "- Czas realizacji zamówienia: około 20 minut, odbiór osobisty na miejscu.\n\n"
    . "Oto aktualne MENU Baru Jaś:\n- Kurczak z rożna (1 sztuka) (BESTSELLER 👑) — 40.0 zł: Legendarny, cały chrupiący kurczak z rożna obrotowego, ręcznie marynowany w kompozycji 12 ziół i powoli pieczony na złocisty kolor (sama sztuka).\n- Kurczak z rożna (1/2 sztuki) (KULTOWE 🔥) — 20.0 zł: Soczysta połówka chrupiącego kurczaka, pieczona na tradycyjnym rożnie obrotowym (sama połówka).\n- Zestaw z połówką kurczaka (z frytkami i surówką) (POLECAMY ⭐) — 36.0 zł: Sycący zestaw obiadowy: połówka soczystego kurczaka z rożna (20 zł) podawana ze złocistymi frytkami (150g — 9 zł) oraz świeżą, domową surówką (250g — 7 zł).\n- Zestaw z całym kurczakiem (z frytkami i surówką) (GIGANT 👑) — 56.0 zł: Olbrzymi zestaw dla naprawdę głodnych lub dla dwojga: cały, legendarny kurczak z rożna (40 zł) podawany ze złocistymi frytkami (150g — 9 zł) oraz świeżą, domową surówką (250g — 7 zł).\n- Kurczak z rożna zestaw (ze świeżymi surówkami) (Z SURÓWKAMI 🥗) — 40.0 zł: Cały chrupiący kurczak z rożna (1 sztuka) serwowany w zestawie z naszym codziennie przygotowywanym, świeżym bukietem domowych surówek (250g).\n- Kebab zestaw (z frytkami lub ryżem) (SYCĄCY 🔥) — 35.0 zł: Sycąca porcja dobrze doprawionego, soczystego mięsa kebab podawana ze złocistymi frytkami lub sypkim ryżem oraz bukietem surówek i sosem.\n- Kebab w bułce (z surówkami) (HIT 👍) — 25.0 zł: Opiekana, chrupiąca rzemieślnicza bułka wypełniona soczystym mięsem kebab, świeżymi warzywami oraz autorskim sosem (czosnkowym lub pikantnym).\n- Kebab w tortilli (KLASYK 🌯) — 24.0 zł: Ciepła tortilla ściśle zawinięta z dużą ilością przypieczonego mięsa kebab, chrupiącymi surówkami i wyrazistymi sosami.\n- Hamburger z filetem z kurczaka (CHRUPIĄCY 🍗) — 20.0 zł: Chrupiący panierowany filet z piersi kurczaka w puszystej bułce sezamowej z pomidorem, ogórkiem, sałatą i wyrazistym sosem burgerowym.\n- Hamburger (KLASYK 🍔) — 16.0 zł: Klasyczny, soczysty kotlet wołowy w bułce z sezamem, podawany z chrupiącym ogórkiem kiszonym, cebulką, ketchupem i musztardą.\n- Hot-Dog (SZYBKA PRZEKĄSKA 🌭) — 14.0 zł: Gorąca parówka w chrupiącej, podgrzanej bułce z ulubionymi sosami (ketchup, musztarda, duński) i prażoną cebulką.\n- Kiełbasa z grilla (porcja 100g) (Z GRILLA 🪵) — 10.0 zł: Aromatyczna, doskonale przypieczona na grillu tradycyjna polska kiełbasa, podawana na gorąco z musztardą lub ketchupem (cena za porcję 100g).\n- Frytki (porcja 150g) (KULTOWE 🍟) — 9.0 zł: Złociste, chrupiące frytki, idealnie usmażone i delikatnie posolone - doskonały dodatek do każdego zamówienia.\n- Surówka (porcja 250g) (ZDROWY WYBÓR 🥗) — 7.0 zł: Świeżo siekane, pełne witamin domowe surówki przygotowywane codziennie rano ze świeżych warzyw.\n- Bułka Poznańska (ŚWIEŻA 🥖) — 2.5 zł: Świeża, chrupiąca rzemieślnicza Bułka Poznańska (przedzielana), doskonała jako tradycyjny dodatek do kurczaka z rożna.\n- Bułka Kajzerka — 1.0 zł: Klasyczna, świeża bułka kajzerka z chrupiącą złocistą skórką, idealny tradycyjny dodatek.\n- Kawa (GORĄCA ☕) — 10.0 zł: Aromatyczna, gorąca kawa parzona, idealna na każdą porę dnia.\n- Herbata — 6.0 zł: Gorąca, rozgrzewająca herbata podawana z cytryną.\n- Pepsi (PROMO 🥤) — 8.0 zł: Mocno schłodzona, orzeźwiająca puszka Pepsi (lub inny zimny napój z oferty) prosto z lodówki.\n- Opakowanie (OPŁATA 📦) — 1.0 zł: Opakowanie na wynos zapewniające bezpieczny i higieniczny transport posiłku oraz utrzymanie temperatury.\n- Sztućce — 0.5 zł: Komplet jednorazowych, ekologicznych sztućców drewnianych (widelec, nóż, serwetka) dla Twojej wygody.\n- Kubek / Kaucja za butelkę — 0.5 zł: Kaucja zwrotna za butelkę szklaną lub jednorazowy kubek do napojów na wynos.\n\n"
    . "Instrukcje postępowania (metody NLP):\n"
    . "1. Odpowiadaj krótko, treściwie i zachęcająco (ADHD-friendly!). Unikaj długich bloków tekstu.\n"
    . "2. Używaj sensoryki VAK (Visual, Auditory, Kinesthetic) w opisach dań. Opisuj jedzenie tak, by pobudzić wyobraźnię (np. 'złocista, chrupiąca skórka', 'soczyste, delikatne mięso', 'aromatyczne zioła', 'usłysz chrupanie świeżo usmażonych frytek').\n"
    . "3. Stosuj presupozycje i Milton Model (np. 'Gdy spróbujesz naszego legendarnego kurczaka, poczujesz prawdziwy, tradycyjny smak...', 'Wyobraź sobie ciepły, sycący kebab, który czeka na Ciebie już za 20 minut...').\n"
    . "4. Odpowiadaj wyłącznie w języku polskim.\n"
    . "5. Jeśli użytkownik chce złożyć zamówienie, powiedz mu, że może kliknąć żółte przyciski 'Dodaj do zamówienia' przy daniach w menu na stronie lub w oknie czatu, aby skompletować koszyk, a następnie wysłać gotowe zamówienie jednym kliknięciem na WhatsApp.\n"
    . "6. Jeśli użytkownik pyta o rzeczy niezwiązane z Barem Jaś, uprzejmie i żartobliwie skieruj rozmowę z powrotem na kurczaka z rożna i kebaby.\n"
    . "7. PROSZENIE O OPINIĘ (Wiatr w skrzydła!): Jeśli klient chwali jedzenie, obsługę, stronę lub wyraża duże zadowolenie, poproś go o wystawienie nam opinii. Zrób to w bardzo serdeczny, a zarazem lekko zabawny sposób, nawiązując tematycznie do kurczaka i piór: powiedz mu żartobliwie, że jego 5 gwiazdek 'daje nam niesamowity wiatr w piórka... to znaczy w skrzydła! 🌬️🍗👑'. Podaj mu bezpośrednie linki:\n"
    . "   - Aby wystawić nam 5 gwiazdek w Google: https://g.page/r/CWKq0_yDruxCEBM/review\n"
    . "   - Aby zostawić nam rekomendację na Facebooku: https://www.facebook.com/kurczakujasia/reviews";

$payload = [
    "contents" => $contents,
    "systemInstruction" => [
        "parts" => [
            ["text" => $systemInstruction]
        ]
    ],
    "generationConfig" => [
        "temperature" => 0.7,
        "maxOutputTokens" => 300
    ]
];

$url = "https://generativelanguage.googleapis.com/v1beta/models/gemini-1.5-flash:generateContent?key=" . $apiKey;

$ch = curl_init($url);
curl_setopt($ch, CURLOPT_RETURNTRANSFER, true);
curl_setopt($ch, CURLOPT_POST, true);
curl_setopt($ch, CURLOPT_POSTFIELDS, json_encode($payload));
curl_setopt($ch, CURLOPT_HTTPHEADER, [
    "Content-Type: application/json"
]);

$response = curl_exec($ch);
$httpCode = curl_getinfo($ch, CURLINFO_HTTP_CODE);
curl_close($ch);

if ($httpCode !== 200) {
    echo json_encode([
        "response" => "Cześć! Chwilowo mam małą przerwę techniczną. Wpisz 'menu', aby zobaczyć nasze pyszne dania lub zadzwoń bezpośrednio: 663 970 016! 🍗",
        "debug_error" => "Błąd API Gemini (HTTP " . $httpCode . "): " . $response
    ]);
    exit;
}

$resData = json_decode($response, true);
if (isset($resData['candidates'][0]['content']['parts'][0]['text'])) {
    $botReply = $resData['candidates'][0]['content']['parts'][0]['text'];
    echo json_encode(["response" => $botReply]);
} else {
    echo json_encode([
        "response" => "Cześć! Coś mnie na chwilę rozproszyło. Sprawdź nasze menu wpisując 'menu' lub kliknij, aby dodać swoje ulubione dania do koszyka! 🍟",
        "debug_error" => "Błędny format odpowiedzi z API Gemini: " . $response
    ]);
}
