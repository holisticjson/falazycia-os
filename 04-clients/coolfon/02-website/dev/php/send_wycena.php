<?php
/* ==========================================================================
   COOLFON.PL — CALCULATOR MAIL CONDUIT (PHP FALLBACK)
   ========================================================================== */

header("Access-Control-Allow-Origin: *");
header("Access-Control-Allow-Headers: Content-Type");
header("Content-Type: application/json");

if ($_SERVER["REQUEST_METHOD"] !== "POST") {
    http_response_code(405);
    echo json_encode(["status" => "error", "message" => "Method Not Allowed"]);
    exit;
}

$input = json_decode(file_get_contents("php://input"), true);
if (!$input) {
    $input = $_POST;
}

$phone = isset($input["phone"]) ? strip_tags(trim($input["phone"])) : "";
$brand = isset($input["brand"]) ? strip_tags(trim($input["brand"])) : "";
$model = isset($input["model"]) ? strip_tags(trim($input["model"])) : "";
$issue = isset($input["issue"]) ? strip_tags(trim($input["issue"])) : "";
$price = isset($input["estimated_price"]) ? strip_tags(trim($input["estimated_price"])) : "";

if (empty($phone) || empty($model) || empty($issue)) {
    http_response_code(400);
    echo json_encode(["status" => "error", "message" => "Brakujące dane wyceny."]);
    exit;
}

// Przygotowanie linku Click-to-Chat WhatsApp dla serwisanta
// Format: https://wa.me/48XXXXXXXXX?text=...
$clean_phone = preg_replace('/[^0-9]/', '', $phone);
// Jeśli telefon nie zaczyna się od kierunkowego Polski 48
if (strlen($clean_phone) === 9) {
    $wa_phone = "48" . $clean_phone;
} else {
    $wa_phone = $clean_phone;
}

$wa_text = rawurlencode("Cześć! Otrzymaliśmy Twoje zapytanie o wycenę naprawy. Urządzenie: $brand $model, usterka: $issue. Szacowany koszt to $price. Czy chcesz zarezerwować termin na dziś?");
$whatsapp_link = "https://wa.me/$wa_phone?text=$wa_text";

$to = "info@coolfon.pl";
$subject = "Nowe zapytanie o wycenę ze strony coolfon.pl";

$email_content = "
<html>
<head>
  <title>$subject</title>
</head>
<body style='font-family: Arial, sans-serif; line-height: 1.6; color: #333;'>
  <h2 style='color: #00C2FF;'>Nowa wycena online do przetworzenia</h2>
  <table style='width: 100%; border-collapse: collapse; margin-top: 20px;'>
    <tr style='background-color: #f8f8f8;'>
      <td style='padding: 10px; border: 1px solid #ddd; font-weight: bold;'>Telefon klienta:</td>
      <td style='padding: 10px; border: 1px solid #ddd;'>$phone</td>
    </tr>
    <tr>
      <td style='padding: 10px; border: 1px solid #ddd; font-weight: bold;'>Marka:</td>
      <td style='padding: 10px; border: 1px solid #ddd;'>$brand</td>
    </tr>
    <tr style='background-color: #f8f8f8;'>
      <td style='padding: 10px; border: 1px solid #ddd; font-weight: bold;'>Model:</td>
      <td style='padding: 10px; border: 1px solid #ddd;'>$model</td>
    </tr>
    <tr>
      <td style='padding: 10px; border: 1px solid #ddd; font-weight: bold;'>Usterka:</td>
      <td style='padding: 10px; border: 1px solid #ddd;'>$issue</td>
    </tr>
    <tr style='background-color: #e6f7ff;'>
      <td style='padding: 10px; border: 1px solid #ddd; font-weight: bold;'>Wstępna cena:</td>
      <td style='padding: 10px; border: 1px solid #ddd; font-weight: bold; color: #007bff;'>$price</td>
    </tr>
  </table>
  
  <div style='margin-top: 30px; padding: 20px; background-color: #e6ffed; border: 1px solid #b7eb8f; border-radius: 8px; text-align: center;'>
    <h3 style='margin-top: 0; color: #389e0d;'>Szybki kontakt z klientem</h3>
    <p>Kliknij poniższy przycisk, aby automatycznie otworzyć WhatsApp z gotową odpowiedzią do tego klienta:</p>
    <a href='$whatsapp_link' target='_blank' style='display: inline-block; padding: 12px 24px; background-color: #25D366; color: #FFFFFF; font-weight: bold; text-decoration: none; border-radius: 6px; margin-top: 10px; box-shadow: 0 4px 10px rgba(37,211,102,0.3);'>Napisz na WhatsApp 💬</a>
  </div>
  
  <p style='margin-top: 30px; font-size: 0.8rem; color: #666;'>Wiadomość wygenerowana automatycznie przez kalkulator na stronie coolfon.pl</p>
</body>
</html>
";

$headers = "MIME-Version: 1.0" . "\r\n";
$headers .= "Content-type:text/html;charset=UTF-8" . "\r\n";
$headers .= "From: Serwis Coolfon <info@coolfon.pl>" . "\r\n";

if (mail($to, $subject, $email_content, $headers)) {
    echo json_encode(["status" => "success", "message" => "Wycena przesłana."]);
} else {
    http_response_code(500);
    echo json_encode(["status" => "error", "message" => "Błąd wysyłania e-mail wyceny."]);
}
?>
