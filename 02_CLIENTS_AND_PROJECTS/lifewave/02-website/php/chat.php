<?php
/**
 * Jaison AI Double-Chatbot Secure Proxy for GCP Vertex AI Search
 * Project ID: jaison-x2o-portal
 * Service Account: x2o-service@jaison-x2o-portal.iam.gserviceaccount.com
 */

header("Access-Control-Allow-Origin: *");
header("Access-Control-Allow-Headers: Content-Type");
header("Content-Type: application/json");

// Define secure paths and settings
define('SA_FILE_PATH', __DIR__ . '/key.json'); // User can drop their downloaded service account JSON here as key.json
define('PROJECT_ID', 'jaison-x2o-portal');
define('GCP_LOCATION', 'eu'); // Multi-region EU as per SOP

// Detect Chatbot Type (Marketing vs Technical)
$botType = isset($_GET['type']) ? trim($_GET['type']) : 'marketing';

// Assign Engine IDs based on type
if ($botType === 'technical') {
    $engineId = 'x2o-technical-search_1784202964185'; // Technical manual chatbot Data Store
} else {
    $engineId = 'x2o-marketing-search_1784201767565'; // Marketing & MLM chatbot Data Store
}

// Initialize session for Spam Shield
if (session_status() === PHP_SESSION_NONE) {
    ini_set('session.cookie_httponly', 1);
    ini_set('session.use_only_cookies', 1);
    session_start();
}

$input = json_decode(file_get_contents("php://input"), true);

// TARCZA 1: Honeypot (Anti-Bot)
if ($input) {
    if (!empty($input['email_confirm']) || !empty($input['phone_check'])) {
        echo json_encode(["status" => "success", "reply" => "Wiadomość wysłana pomyślnie! Nasz asystent skontaktuje się z Tobą. 🤝"]);
        exit;
    }
}

if ($_SERVER["REQUEST_METHOD"] !== "POST") {
    http_response_code(405);
    echo json_encode(["status" => "error", "message" => "Metoda niedozwolona."]);
    exit;
}

$userMessage = isset($input['message']) ? trim($input['message']) : '';
if (empty($userMessage)) {
    echo json_encode(["status" => "error", "message" => "Pusta wiadomość."]);
    exit;
}

// TARCZA 2: IP Rate Limiter (min. 3 sekundy przerwy między pytaniami)
if (isset($_SESSION['chat_last_query_time'])) {
    if (time() - $_SESSION['chat_last_query_time'] < 3) {
        echo json_encode(["status" => "success", "reply" => "Piszesz odrobinę za szybko! Odczekaj chwilę, aby dać wodzie i światłu czas na rezonans. ⏱️"]);
        exit;
    }
}
$_SESSION['chat_last_query_time'] = time();

// TARCZA 3: Dobowy limit sesyjny (max. 30 pytań na dobę na użytkownika)
if (!isset($_SESSION['chat_query_count'])) {
    $_SESSION['chat_query_count'] = 0;
    $_SESSION['chat_first_query_time'] = time();
}
if (time() - $_SESSION['chat_first_query_time'] > 86400) {
    $_SESSION['chat_query_count'] = 0;
    $_SESSION['chat_first_query_time'] = time();
}
if ($_SESSION['chat_query_count'] >= 30) {
    echo json_encode([
        "status" => "success",
        "reply" => "Przekroczyłeś dobowy limit 30 zapytań do bota. Skontaktuj się z nami bezpośrednio na <strong>Klubowym WhatsAppie</strong>, gdzie chętnie odpowiemy na wszystkie Twoje pytania osobiście! 👉 <a href='https://wa.me/48791636644' target='_blank' class='chat-link'>Otwórz WhatsApp</a>"
    ]);
    exit;
}
$_SESSION['chat_query_count']++;

// TARCZA 4: Błyskawiczny lokalny interceptor zdefiniowanych tematów (wyklucza halucynacje i natychmiastowo odpowiada)
function getPredefinedReply($msg, $botType) {
    $msgLower = mb_strtolower($msg, 'UTF-8');
    
    if ($botType === 'technical') {
        if (strpos($msgLower, 'adapter') !== false || strpos($msgLower, 'usa') !== false || strpos($msgLower, 'wtycz') !== false) {
            return "Do podłączenia stacji X2O™ w Europie wymagany jest prosty adapter podróżny ze standardu USA (NEMA 1-15) na standard europejski (Europlug). Urządzenie fabrycznie dostarczane jest z uniwersalnym zasilaczem obsługującym napięcie 100-240V oraz częstotliwość 50/60Hz, dzięki czemu nie potrzebujesz żadnych transformatorów napięcia – wystarczy zwykła przejściówka mechaniczna za kilka złotych!";
        } elseif (strpos($msgLower, 'płuka') !== false || strpos($msgLower, 'flushing') !== false || strpos($msgLower, 'zawór') !== false) {
            return "Procedura płukania filtra (Flushing) jest kluczowa dla zachowania czystości membrany. Wykonaj ją w 3 prostych krokach:\n* Podłącz wężyk odpływowy do czarnego zaworu Flushing Valve z tyłu urządzenia.\n* Otwórz zawór (przekręć o 90 stopni) i pozwól wodzie swobodnie przepływać przez około 5-10 minut przed pierwszym użyciem lub po wymianie filtrów.\n* Zamknij zawór. Urządzenie jest teraz gotowe do pracy w trybie filtracji molekularnej!";
        } elseif (strpos($msgLower, 'błąd') !== false || strpos($msgLower, 'e2') !== false || strpos($msgLower, 'error') !== false) {
            return "Kod błędu <strong>E2</strong> na wyświetlaczu stacji X2O oznacza zbyt niskie ciśnienie wody wejściowej lub przerwany dopływ wody. Sprawdź, czy zawór przyłączeniowy jest całkowicie otwarty oraz czy wężyk doprowadzający nie jest zagięty. Po przywróceniu odpowiedniego ciśnienia błąd zniknie automatycznie.";
        } elseif (strpos($msgLower, 'czyszcz') !== false || strpos($msgLower, 'kamień') !== false || strpos($msgLower, 'kwasek') !== false) {
            return "Aby oczyścić komorę aktywatora z osadów wapiennych, rozpuść 2 łyżeczki kwasku cytrynowego w szklance ciepłej wody i wlej do zbiornika. Uruchom urządzenie na 1 krótki cykl, a następnie pozostaw roztwór w komorze na 30 minut. Na koniec przepłucz zbiornik dwukrotnie czystą wodą. Zalecamy powtarzanie tego procesu raz w miesiącu.";
        }
    } else {
        if (strpos($msgLower, 'patent') !== false || strpos($msgLower, 'schmidt') !== false || strpos($msgLower, 'dowod') !== false || strpos($msgLower, 'naukow') !== false || strpos($msgLower, 'badani') !== false) {
            return "Technologia X2O™ oraz plastrów fototerapeutycznych LifeWave opiera się na przełomowych odkryciach Davida Schmidta, chronionych ponad 100 patentami na całym świecie. Kluczowy patent **US 12,312,256** szczegółowo opisuje naświetlanie wody i chromoforów wieloma długościami fal świetlnych w celu nadania jej struktury bio-przewodnej. Z kolei patent **US 8,734,316** dotyczy nanostrukturalnej technologii noszonych aparatów biomolekularnych. Więcej o badaniach przeczytasz na oficjalnej stronie <a href='https://lifewave.com/tomaszduda/home/light-into-water' target='_blank' class='chat-link'>LiveWave Light into Water</a> oraz w inspirującym dokumencie <a href='https://elevatinglight.com/' target='_blank' class='chat-link'>Elevating Light</a>.";
        } elseif (strpos($msgLower, 'mlm') !== false || strpos($msgLower, 'biznes') !== false || strpos($msgLower, 'zarob') !== false || strpos($msgLower, 'partner') !== false || strpos($msgLower, 'pieniądz') !== false || strpos($msgLower, 'zarabia') !== false) {
            return "Biznes LifeWave to unikalna szansa w branży MLM (Direct Selling). Firma zanotowała gigantyczny skok przychodów z **20 milionów USD do ponad 500-580 milionów USD** rocznie, zdobywając nagrodę **DSN Bravo Growth Award** oraz prestiżowy rating **AAA+** na Business For Home. Dzięki naszemu autorskiemu systemowi automatyzacji i duplikacji LifeWave4Life, budowanie struktur rekrutacyjnych staje się niezwykle proste, asynchroniczne i profesjonalne. Dołącz do naszej elitarnej grupy partnerskiej na WhatsApp i buduj stabilny rurociąg finansowy! Chcesz poznać szczegóły? Dołącz bezpośrednio do grupy: <a href='https://chat.whatsapp.com/H4KTNar9YQTCF9bCTC6TFe' target='_blank' class='chat-link'>Dołącz do grupy Biznes & Duplikacja</a>";
        } elseif (strpos($msgLower, 'degustacj') !== false || strpos($msgLower, 'gabinet') !== false || strpos($msgLower, 'łodz') !== false || strpos($msgLower, 'nawrot') !== false || strpos($msgLower, 'gabine') !== false) {
            return "Zapraszamy Cię serdecznie na bezpłatną degustację wody biofotonowej X2O™ do naszego fizycznego **Gabinetu Świątynia Harmonii** w Łodzi przy ul. Nawrot (zabytkowy Księży Młyn). Spotkanie prowadzą nasze wspaniałe terapeutki i Brand Partnerki:\n" .
                   "* 💧 **Monika**: [+48 535 200 879](https://wa.me/48535200879) (Director, Doradczyni ds. hydratacji biofotonowej X2O™ oraz regeneracji organizmu)\n" .
                   "* 🧬 **Ania**: [+48 501 401 704](https://wa.me/48501401704) (Specjalistka ds. fotobiomodulacji i naturalnego zdrowia komórkowego)\n" .
                   "Doświadczysz u nich na własnej skórze synergii hydratacji molekularnej oraz fototerapii komórkowej. Aby zarezerwować termin i odebrać darmową szklankę wody, wypełnij formularz na naszej stronie lub kliknij w jeden z powyższych kontaktów, aby umówić się bezpośrednio na WhatsApp!";
        } elseif (strpos($msgLower, 'x39') !== false || strpos($msgLower, 'plaster') !== false || strpos($msgLower, 'plastry') !== false || strpos($msgLower, 'komórk') !== false || strpos($msgLower, 'macierzyst') !== false) {
            return "Plastry fototerapeutyczne **LifeWave X39** to absolutny przełom w dziedzinie nieinwazyjnej fotobiomodulacji i regeneracji komórkowej. \n\n" .
                   "**Jak to działa?**\n" .
                   "Plaster X39 to zaawansowany nanotechnologiczny aparat biomolekularny, który po naklejeniu na ciało pod wpływem ciepła (promieniowania podczerwonego) odbija precyzyjnie określone, biofotonowe pasmo światła z powrotem do wnętrza organizmu. Proces ten stymuluje naturalną produkcję **peptydu miedzi GHK-Cu**, który ma udowodnione naukowo właściwości resetowania ponad 4000 genów do ich młodszego, zdrowszego stanu. \n\n" .
                   "**Kluczowe efekty X39:**\n" .
                   "* 🧬 **Aktywacja komórek macierzystych** – Twój organizm zaczyna naturalnie produkować nowe, w pełni sprawne komórki macierzyste do regeneracji tkanek i narządów.\n" .
                   "* ⚡ **Błyskawiczna ulga w bólu i stanach zapalnych** – Silne, naturalne wsparcie bez obciążania wątroby chemią.\n" .
                   "* 🔋 **Zwiększenie energii i witalności komórkowej** – Lepsza praca mitochondriów, szybsza regeneracja po wysiłku i głęboki, regenerujący sen.\n" .
                   "* 🩹 **Przyspieszone gojenie ran** i odnowa skóry (efekt anti-aging).\n\n" .
                   "Wspólnie ze stacją **X2O™** (która dba o idealne, heksagonalne nawodnienie komórek i bio-przewodnictwo), plastry X39 tworzą najpotężniejszą na świecie, domową synergię biohackingową! \n\n" .
                   "Chcesz dowiedzieć się więcej i poznać tysiące opinii o efektach fototerapii? Dołącz do naszej dedykowanej grupy: " .
                   "<a href='https://chat.whatsapp.com/FPtH1JW21PD3KgwmeCgEcs' target='_blank' class='chat-link'>Grupa Fototerapia & Plastry X39 na WhatsApp</a> " .
                   "lub skontaktuj się bezpośrednio z naszą specjalistką ds. fotobiomodulacji, **Anią**: [+48 501 401 704](https://wa.me/48501401704).";
        } elseif (strpos($msgLower, 'jak działa') !== false || strpos($msgLower, 'foton') !== false || strpos($msgLower, 'aktyw') !== false || strpos($msgLower, 'biofoton') !== false || strpos($msgLower, 'technolog') !== false || strpos($msgLower, 'woda') !== false || strpos($msgLower, 'nawadnia') !== false || strpos($msgLower, 'nawandnia') !== false) {
            return "Stacja X2O™ poddaje wodę zaawansowanej filtracji wodorowej (nasycaniu aktywnym wodorem), a następnie aktywuje ją specjalnym widmem światła o częstotliwościach biofotonowych, zgodnie z patentami Davida Schmidta. Taka woda uzyskuje strukturę heksagonalną (ciekłokrystaliczną) – identyczną jak woda wewnątrzkomórkowa w zdrowych, młodych organizmach. Dzięki temu woda błyskawicznie nawadnia mitochondria komórkowe, dodając czystej energii fizycznej, ułatwiając detoksykację i idealnie współgrając z fototerapią komórkową LifeWave X39. Chcesz wejść głębiej? Wejdź do naszej grupy: <a href='https://chat.whatsapp.com/EKGnb8Znu5fBlcIZHV80HR' target='_blank' class='chat-link'>Dołącz do Klubu X2O</a>";
        } elseif (strpos($msgLower, 'kontakt') !== false || strpos($msgLower, 'whatsapp') !== false || strpos($msgLower, 'grupa') !== false || strpos($msgLower, 'grupy') !== false || strpos($msgLower, 'społecznoś') !== false) {
            return "Nasza społeczność LifeWave4Life to tętniący życiem ekosystem. Możesz dołączyć do naszych dedykowanych kanałów i grup:\n" .
                   "* 📢 <a href='https://whatsapp.com/channel/0029Vb6R9OaBfxoA1QUX9n3y' target='_blank' class='chat-link'>Kanał Nadawczy LifeWave 4 Polska</a> (Prywatne, ogólne aktualności)\n" .
                   "* 💧 <a href='https://chat.whatsapp.com/EKGnb8Znu5fBlcIZHV80HR' target='_blank' class='chat-link'>Klub Wody Komórkowej X2O</a> (Grupa otwarta, opinie o wodzie i X2O)\n" .
                   "* 🧬 <a href='https://chat.whatsapp.com/FPtH1JW21PD3KgwmeCgEcs' target='_blank' class='chat-link'>Fototerapia & Plastry X39</a> (Dyskusje o plastrach i komórkach macierzystych)\n" .
                   "* 🚀 <a href='https://chat.whatsapp.com/H4KTNar9YQTCF9bCTC6TFe' target='_blank' class='chat-link'>Biznes & Duplikacja LifeWave4Life</a> (Zamknięta grupa partnerska MLM)\n\n" .
                   "Możesz też skontaktować się bezpośrednio z nami:\n" .
                   "* **Monika (Zdrowie, Degustacje Łódź)**: [+48 535 200 879](https://wa.me/48535200879)\n" .
                   "* **Ania (Zdrowie, Fototerapia)**: [+48 501 401 704](https://wa.me/48501401704)\n" .
                   "* **Tomasz (Biznes, Automatyzacja, Nowi Partnerzy)**: [+48 791 636 644](https://wa.me/48791636644)";
        }
    }
    return null;
}

$predefinedReply = getPredefinedReply($userMessage, $botType);
if ($predefinedReply !== null) {
    echo json_encode([
        "status" => "success",
        "reply" => cleanAndHumanizeMarkdown($predefinedReply)
    ]);
    exit;
}

// Helper function to encode URL-safe Base64
function base64UrlEncode($data) {
    return str_replace(['+', '/', '='], ['-', '_', ''], base64_encode($data));
}

// Helper function to get access token from Google Cloud Service Account
function getGoogleAccessToken($saJsonStr) {
    $sa = json_decode($saJsonStr, true);
    if (!isset($sa['private_key']) || !isset($sa['client_email'])) {
        throw new Exception("Nieprawidłowy format pliku klucza Service Account.");
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
        throw new Exception("Błąd podpisywania JWT openssl.");
    }

    $jwt = $signatureInput . "." . base64UrlEncode($signature);

    $ch = curl_init("https://oauth2.googleapis.com/token");
    curl_setopt($ch, CURLOPT_RETURNTRANSFER, true);
    curl_setopt($ch, CURLOPT_POST, true);
    curl_setopt($ch, CURLOPT_POSTFIELDS, http_build_query([
        'grant_type' => 'urn:ietf:params:oauth:grant-type:jwt-bearer',
        'assertion' => $jwt
    ]));
    $res = curl_exec($ch);
    $httpCode = curl_getinfo($ch, CURLINFO_HTTP_CODE);
    curl_close($ch);

    if ($httpCode !== 200) {
        throw new Exception("Błąd pobierania tokenu OAuth2: " . $res);
    }

    $data = json_decode($res, true);
    return $data['access_token'];
}

// Helper function to clean and humanize Markdown into clean HTML (Zasada 13)
function cleanAndHumanizeMarkdown($text) {
    // Replace markdown bold **text** with standard HTML <strong>text</strong>
    $text = preg_replace('/\*\*(.*?)\*\*/', '<strong>$1</strong>', $text);
    // Replace markdown italic *text* with standard HTML <em>text</em>
    $text = preg_replace('/\*(.*?)\*/', '<em>$1</em>', $text);
    
    // Replace markdown links [text](url) with HTML links with target="_blank"
    $text = preg_replace('/\[(.*?)\]\((.*?)\)/', '<a href="$2" target="_blank" class="chat-link">$1</a>', $text);
    
    // Handle bullet points lists
    $lines = explode("\n", $text);
    $inList = false;
    $htmlLines = [];
    foreach ($lines as $line) {
        $trimmed = trim($line);
        if (preg_match('/^[\*\-\x{2022}]\s+(.*)$/u', $trimmed, $matches)) {
            if (!$inList) {
                $htmlLines[] = '<ul class="chat-bullet-list">';
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

// Universal High-Fidelity Smart Fallback Reply Engine (Scrubbed of Jaison Agency references)
function getSmartFallbackReply($msg, $botType) {
    $msgLower = mb_strtolower($msg, 'UTF-8');
    
    if ($botType === 'technical') {
        if (strpos($msgLower, 'adapter') !== false || strpos($msgLower, 'usa') !== false || strpos($msgLower, 'wtycz') !== false) {
            return "Do podłączenia stacji X2O™ w Europie wymagany jest prosty adapter podróżny ze standardu USA (NEMA 1-15) na standard europejski (Europlug). Urządzenie fabrycznie dostarczane jest z uniwersalnym zasilaczem obsługującym napięcie 100-240V oraz częstotliwość 50/60Hz, dzięki czemu nie potrzebujesz żadnych transformatorów napięcia – wystarczy zwykła przejściówka mechaniczna za kilka złotych!";
        } elseif (strpos($msgLower, 'płuka') !== false || strpos($msgLower, 'flushing') !== false || strpos($msgLower, 'zawór') !== false) {
            return "Procedura płukania filtra (Flushing) jest kluczowa dla zachowania czystości membrany. Wykonaj ją w 3 prostych krokach:\n* Podłącz wężyk odpływowy do czarnego zaworu Flushing Valve z tyłu urządzenia.\n* Otwórz zawór (przekręć o 90 stopni) i pozwól wodzie swobodnie przepływać przez około 5-10 minut przed pierwszym użyciem lub po wymianie filtrów.\n* Zamknij zawór. Urządzenie jest teraz gotowe do pracy w trybie filtracji molekularnej!";
        } elseif (strpos($msgLower, 'błąd') !== false || strpos($msgLower, 'e2') !== false || strpos($msgLower, 'error') !== false) {
            return "Kod błędu <strong>E2</strong> na wyświetlaczu stacji X2O oznacza zbyt niskie ciśnienie wody wejściowej lub przerwany dopływ wody. Sprawdź, czy zawór przyłączeniowy jest całkowicie otwarty oraz czy wężyk doprowadzający nie jest zagięty. Po przywróceniu odpowiedniego ciśnienia błąd zniknie automatycznie.";
        } elseif (strpos($msgLower, 'czyszcz') !== false || strpos($msgLower, 'kamień') !== false || strpos($msgLower, 'kwasek') !== false) {
            return "Aby oczyścić komorę aktywatora z osadów wapiennych, rozpuść 2 łyżeczki kwasku cytrynowego w szklance ciepłej wody i wlej do zbiornika. Uruchom urządzenie na 1 krótki cykl, a następnie pozostaw roztwór w komorze na 30 minut. Na koniec przepłucz zbiornik dwukrotnie czystą wodą. Zalecamy powtarzanie tego procesu raz w miesiącu.";
        } else {
            return "Witaj! Jestem Twoim Asystentem Technicznym X2O. Chętnie pomogę Ci w kwestiach takich jak:\n* Podłączenie wtyczki USA i parametry zasilacza (100-240V)\n* Procedura płukania filtra przez zawór Flushing Valve\n* Usuwanie kamienia kwaskiem cytrynowym\n* Rozszyfrowanie kodów błędów (np. błędu E2)\nCo dokładnie chciałbyś dziś skonfigurować?";
        }
    } else {
        if (strpos($msgLower, 'patent') !== false || strpos($msgLower, 'schmidt') !== false || strpos($msgLower, 'dowod') !== false || strpos($msgLower, 'naukow') !== false || strpos($msgLower, 'badani') !== false) {
            return "Technologia X2O™ oraz plastrów fototerapeutycznych LifeWave opiera się na przełomowych odkryciach Davida Schmidta, chronionych ponad 100 patentami na całym świecie. Kluczowy patent **US 12,312,256** szczegółowo opisuje naświetlanie wody i chromoforów wieloma długościami fal świetlnych w celu nadania jej struktury bio-przewodnej. Z kolei patent **US 8,734,316** dotyczy nanostrukturalnej technologii noszonych aparatów biomolekularnych. Więcej o badaniach przeczytasz na oficjalnej stronie <a href='https://lifewave.com/tomaszduda/home/light-into-water' target='_blank' class='chat-link'>LiveWave Light into Water</a> oraz w inspirującym dokumencie <a href='https://elevatinglight.com/' target='_blank' class='chat-link'>Elevating Light</a>.";
        } elseif (strpos($msgLower, 'mlm') !== false || strpos($msgLower, 'biznes') !== false || strpos($msgLower, 'zarob') !== false || strpos($msgLower, 'partner') !== false || strpos($msgLower, 'pieniądz') !== false || strpos($msgLower, 'zarabia') !== false) {
            return "Biznes LifeWave to unikalna szansa w branży MLM (Direct Selling). Firma zanotowała gigantyczny skok przychodów z **20 milionów USD do ponad 500-580 milionów USD** rocznie, zdobywając nagrodę **DSN Bravo Growth Award** oraz prestiżowy rating **AAA+** na Business For Home. Dzięki naszemu autorskiemu systemowi automatyzacji i duplikacji LifeWave4Life, budowanie struktur rekrutacyjnych staje się niezwykle proste, asynchroniczne i profesjonalne. Dołącz do naszej elitarnej grupy partnerskiej na WhatsApp i buduj stabilny rurociąg finansowy! Chcesz poznać szczegóły? Dołącz bezpośrednio do grupy: <a href='https://chat.whatsapp.com/H4KTNar9YQTCF9bCTC6TFe' target='_blank' class='chat-link'>Dołącz do grupy Biznes & Duplikacja</a>";
        } elseif (strpos($msgLower, 'degustacj') !== false || strpos($msgLower, 'gabinet') !== false || strpos($msgLower, 'łodz') !== false || strpos($msgLower, 'nawrot') !== false || strpos($msgLower, 'gabine') !== false) {
            return "Zapraszamy Cię serdecznie na bezpłatną degustację wody biofotonowej X2O™ do naszego fizycznego **Gabinetu Świątynia Harmonii** w Łodzi przy ul. Nawrot (zabytkowy Księży Młyn). Spotkanie prowadzą nasze wspaniałe terapeutki i Brand Partnerki:\n" .
                   "* 💧 **Monika**: [+48 535 200 879](https://wa.me/48535200879) (Director, Doradczyni ds. hydratacji biofotonowej X2O™ oraz regeneracji organizmu)\n" .
                   "* 🧬 **Ania**: [+48 501 401 704](https://wa.me/48501401704) (Specjalistka ds. fotobiomodulacji i naturalnego zdrowia komórkowego)\n" .
                   "Doświadczysz u nich na własnej skórze synergii hydratacji molekularnej oraz fototerapii komórkowej. Aby zarezerwować termin i odebrać darmową szklankę wody, wypełnij formularz na naszej stronie lub kliknij w jeden z powyższych kontaktów, aby umówić się bezpośrednio na WhatsApp!";
        } elseif (strpos($msgLower, 'x39') !== false || strpos($msgLower, 'plaster') !== false || strpos($msgLower, 'plastry') !== false || strpos($msgLower, 'komórk') !== false || strpos($msgLower, 'macierzyst') !== false) {
            return "Plastry fototerapeutyczne **LifeWave X39** to absolutny przełom w dziedzinie nieinwazyjnej fotobiomodulacji i regeneracji komórkowej. \n\n" .
                   "**Jak to działa?**\n" .
                   "Plaster X39 to zaawansowany nanotechnologiczny aparat biomolekularny, który po naklejeniu na ciało pod wpływem ciepła (promieniowania podczerwonego) odbija precyzyjnie określone, biofotonowe pasmo światła z powrotem do wnętrza organizmu. Proces ten stymuluje naturalną produkcję **peptydu miedzi GHK-Cu**, który ma udowodnione naukowo właściwości resetowania ponad 4000 genów do ich młodszego, zdrowszego stanu. \n\n" .
                   "**Kluczowe efekty X39:**\n" .
                   "* 🧬 **Aktywacja komórek macierzystych** – Twój organizm zaczyna naturalnie produkować nowe, w pełni sprawne komórki macierzyste do regeneracji tkanek i narządów.\n" .
                   "* ⚡ **Błyskawiczna ulga w bólu i stanach zapalnych** – Silne, naturalne wsparcie bez obciążania wątroby chemią.\n" .
                   "* 🔋 **Zwiększenie energii i witalności komórkowej** – Lepsza praca mitochondriów, szybsza regeneracja po wysiłku i głęboki, regenerujący sen.\n" .
                   "* 🩹 **Przyspieszone gojenie ran** i odnowa skóry (efekt anti-aging).\n\n" .
                   "Wspólnie ze stacją **X2O™** (która dba o idealne, heksagonalne nawodnienie komórek i bio-przewodnictwo), plastry X39 tworzą najpotężniejszą na świecie, domową synergię biohackingową! \n\n" .
                   "Chcesz dowiedzieć się więcej i poznać tysiące opinii o efektach fototerapii? Dołącz do naszej dedykowanej grupy: " .
                   "<a href='https://chat.whatsapp.com/FPtH1JW21PD3KgwmeCgEcs' target='_blank' class='chat-link'>Grupa Fototerapia & Plastry X39 na WhatsApp</a> " .
                   "lub skontaktuj się bezpośrednio z naszą specjalistką ds. fotobiomodulacji, **Anią**: [+48 501 401 704](https://wa.me/48501401704).";
        } elseif (strpos($msgLower, 'jak działa') !== false || strpos($msgLower, 'foton') !== false || strpos($msgLower, 'aktyw') !== false || strpos($msgLower, 'biofoton') !== false || strpos($msgLower, 'technolog') !== false || strpos($msgLower, 'woda') !== false || strpos($msgLower, 'nawadnia') !== false) {
            return "Stacja X2O™ poddaje wodę zaawansowanej filtracji wodorowej (nasycaniu aktywnym wodorem), a następnie aktywuje ją specjalnym widmem światła o częstotliwościach biofotonowych, zgodnie z patentami Davida Schmidta. Taka woda uzyskuje strukturę heksagonalną (ciekłokrystaliczną) – identyczną jak woda wewnątrzkomórkowa w zdrowych, młodych organizmach. Dzięki temu woda błyskawicznie nawadnia mitochondria komórkowe, dodając czystej energii fizycznej, ułatwiając detoksykację i idealnie współgrając z fototerapią komórkową LifeWave X39. Chcesz wejść głębiej? Wejdź do naszej grupy: <a href='https://chat.whatsapp.com/EKGnb8Znu5fBlcIZHV80HR' target='_blank' class='chat-link'>Dołącz do Klubu X2O</a>";
        } elseif (strpos($msgLower, 'kontakt') !== false || strpos($msgLower, 'whatsapp') !== false || strpos($msgLower, 'grupa') !== false || strpos($msgLower, 'grupy') !== false || strpos($msgLower, 'społecznoś') !== false) {
            return "Nasza społeczność LifeWave4Life to tętniący życiem ekosystem. Możesz dołączyć do naszych dedykowanych kanałów i grup:\n" .
                   "* 📢 <a href='https://whatsapp.com/channel/0029Vb6R9OaBfxoA1QUX9n3y' target='_blank' class='chat-link'>Kanał Nadawczy LifeWave 4 Polska</a> (Prywatne, ogólne aktualności)\n" .
                   "* 💧 <a href='https://chat.whatsapp.com/EKGnb8Znu5fBlcIZHV80HR' target='_blank' class='chat-link'>Klub Wody Komórkowej X2O</a> (Grupa otwarta, opinie o wodzie i X2O)\n" .
                   "* 🧬 <a href='https://chat.whatsapp.com/FPtH1JW21PD3KgwmeCgEcs' target='_blank' class='chat-link'>Fototerapia & Regeneracja X39</a> (Dyskusje o plastrach i komórkach macierzystych)\n" .
                   "* 🚀 <a href='https://chat.whatsapp.com/H4KTNar9YQTCF9bCTC6TFe' target='_blank' class='chat-link'>Biznes & Duplikacja LifeWave4Life</a> (Zamknięta grupa partnerska MLM)\n\n" .
                   "Możesz też skontaktować się bezpośrednio z nami:\n" .
                   "* **Monika (Zdrowie, Degustacje Łódź)**: [+48 535 200 879](https://wa.me/48535200879)\n" .
                   "* **Ania (Zdrowie, Fototerapia)**: [+48 501 401 704](https://wa.me/48501401704)\n" .
                   "* **Tomasz (Biznes, Automatyzacja, Nowi Partnerzy)**: [+48 791 636 644](https://wa.me/48791636644)";
        } else {
            return "Witaj! Jestem wirtualnym asystentem marki LifeWave4Life. Chętnie opowiem Ci o przełomie w biohackingowym nawodnieniu komórkowym komórek macierzystych oraz o biznesie przyszłości w direct-sellingu. Wybierz jeden z tematów:\n* **Jak działa technologia biofotonów X2O™?**\n* **Naukowe patenty Davida Schmidta i dowody kliniczne fototerapii**\n* **Darmowa degustacja wody w naszym gabinecie w Łodzi (ul. Nawrot)**\n* **Możliwości biznesowe MLM i automatyczna duplikacja w LifeWave4Life**\n* **Nasze grupy i społeczności na WhatsApp**\nO co chciałbyś zapytać?";
        }
    }
}

// Attempt to read Service Account credentials from environment or local JSON file
$saJsonStr = null;
if (file_exists(SA_FILE_PATH)) {
    $saJsonStr = file_get_contents(SA_FILE_PATH);
} elseif (getenv('GCP_SERVICE_ACCOUNT_JSON')) {
    $saJsonStr = getenv('GCP_SERVICE_ACCOUNT_JSON');
}

// If no credentials found, run in High-Fidelity Smart Local Fallback mode to ensure client-side usability before credentials upload
if (!$saJsonStr) {
    $reply = getSmartFallbackReply($userMessage, $botType);
    echo json_encode([
        "status" => "success",
        "reply" => cleanAndHumanizeMarkdown($reply)
    ]);
    exit;
}

// Full Enterprise Production Integration with GCP Vertex AI Search REST API
try {
    $accessToken = getGoogleAccessToken($saJsonStr);
    
    // API endpoint construction for Vertex AI Search
    $searchUrl = "https://" . GCP_LOCATION . "-discoveryengine.googleapis.com/v1/projects/" . PROJECT_ID . "/locations/" . GCP_LOCATION . "/collections/default_collection/engines/" . $engineId . "/servingConfigs/default_search:search";
    
    // Prepare enterprise payload for search with summary settings
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
        throw new Exception("Vertex AI Search API returned non-200 code: " . $httpCode . " Response: " . $response);
    }

    $resData = json_decode($response, true);
    $reply = "";
    
    if (isset($resData['summary']['summaryText']) && !empty($resData['summary']['summaryText'])) {
        $reply = $resData['summary']['summaryText'];
        
        // Clean up dry academic robotic search engine prefixes
        $prefixesToStrip = [
            "/^oto odpowiedź na twoje zapytanie, oparta na dostarczonych źródłach:\s*/ui",
            "/^oto odpowiedź na twoje zapytanie oparta na dostarczonych źródłach:\s*/ui",
            "/^na podstawie dostarczonych źródeł,\s*/ui",
            "/^na podstawie dostarczonych źródeł:\s*/ui",
            "/^opierając się na dostarczonych źródłach,\s*/ui",
            "/^opierając się na dostarczonych źródłach:\s*/ui",
            "/^zgodnie z dostarczonymi źródłami,\s*/ui",
            "/^zgodnie z dostarczonymi źródłami:\s*/ui",
            "/^na podstawie dostępnych informacji,\s*/ui",
            "/^na podstawie dostępnych informacji:\s*/ui"
        ];
        foreach ($prefixesToStrip as $pattern) {
            $reply = preg_replace($pattern, '', $reply);
        }
        $reply = trim($reply);
        
        // Smart Hybrid Interceptor for Grounding Rejections & Off-Brand content (Case-insensitive)
        $rejectionKeywords = [
            'nie zawiera',
            'nie jestem w stanie',
            'nie udało mi się',
            'nie znaleziono',
            'nie opisano',
            'brak informacji',
            'nie mam informacji',
            'nie mogę znaleźć',
            'nie mogę odpowiedzieć',
            'nie ma wzmianki',
            'nie podano',
            'nie dostarczono',
            'rejection',
            'nie posiada',
            'błąd wyszukiwania',
            'brak danych',
            'tekst źródłowy',
            'tekstu źródłowego',
            'dostarczonym źródle',
            'nie wspomina',
            'nie ma mowy',
            'nie wyszczególniono',
            'nie jest opisana',
            'krzysztof markowski',
            'krzysztofa markowskiego',
            'markowski',
            'markowskiego',
            'kondratiew',
            'kondratiewa'
        ];
        
        $isRejection = false;
        foreach ($rejectionKeywords as $kw) {
            if (stripos($reply, $kw) !== false) {
                $isRejection = true;
                break;
            }
        }
        
        if ($isRejection) {
            // Trigger Smart Local Fallback
            $reply = getSmartFallbackReply($userMessage, $botType);
        }
    } else {
        $reply = getSmartFallbackReply($userMessage, $botType);
    }

    echo json_encode([
        "status" => "success",
        "reply" => cleanAndHumanizeMarkdown($reply)
    ]);

} catch (Exception $e) {
    // Elegant system fallback to high-fidelity local engine in case of GCP service disruptions
    $reply = getSmartFallbackReply($userMessage, $botType);
    echo json_encode([
        "status" => "success",
        "reply" => cleanAndHumanizeMarkdown($reply)
    ]);
}
