<?php
/* ==========================================================================
   COOLFON.PL — FORM MAIL CONDUIT (PHP)
   ========================================================================== */

header("Access-Control-Allow-Origin: *");
header("Access-Control-Allow-Headers: Content-Type");
header("Content-Type: application/json");

if ($_SERVER["REQUEST_METHOD"] !== "POST") {
    http_response_code(405);
    echo json_encode(["status" => "error", "message" => "Method Not Allowed"]);
    exit;
}

// Odczytaj dane z formularza (JSON lub POST)
$input = json_decode(file_get_contents("php://input"), true);
if (!$input) {
    $input = $_POST;
}

$name = isset($input["name"]) ? strip_tags(trim($input["name"])) : "";
$phone = isset($input["phone"]) ? strip_tags(trim($input["phone"])) : "";
$email = isset($input["email"]) ? filter_var(trim($input["email"]), FILTER_SANITIZE_EMAIL) : "";
$device = isset($input["device"]) ? strip_tags(trim($input["device"])) : "";
$message = isset($input["message"]) ? strip_tags(trim($input["message"])) : "";

// Walidacja pól wymaganych
if (empty($name) || empty($phone)) {
    http_response_code(400);
    echo json_encode(["status" => "error", "message" => "Imię oraz telefon są wymagane."]);
    exit;
}

// Konfiguracja odbiorcy
$to = "info@coolfon.pl";
$subject = "Nowe zgłoszenie serwisowe ze strony coolfon.pl";

// Konstrukcja wiadomości HTML
$email_content = "
<html>
<head>
  <title>$subject</title>
</head>
<body style='font-family: Arial, sans-serif; line-height: 1.6; color: #333;'>
  <h2 style='color: #00A8E8;'>Nowy lead ze strony kontaktowej</h2>
  <table style='width: 100%; border-collapse: collapse; margin-top: 20px;'>
    <tr style='background-color: #f8f8f8;'>
      <td style='padding: 10px; border: 1px solid #ddd; font-weight: bold;'>Imię i Nazwisko:</td>
      <td style='padding: 10px; border: 1px solid #ddd;'>$name</td>
    </tr>
    <tr>
      <td style='padding: 10px; border: 1px solid #ddd; font-weight: bold;'>Telefon:</td>
      <td style='padding: 10px; border: 1px solid #ddd;'>$phone</td>
    </tr>
    <tr style='background-color: #f8f8f8;'>
      <td style='padding: 10px; border: 1px solid #ddd; font-weight: bold;'>E-mail:</td>
      <td style='padding: 10px; border: 1px solid #ddd;'>$email</td>
    </tr>
    <tr>
      <td style='padding: 10px; border: 1px solid #ddd; font-weight: bold;'>Urządzenie / Model:</td>
      <td style='padding: 10px; border: 1px solid #ddd;'>$device</td>
    </tr>
    <tr style='background-color: #f8f8f8;'>
      <td style='padding: 10px; border: 1px solid #ddd; font-weight: bold;'>Opis problemu:</td>
      <td style='padding: 10px; border: 1px solid #ddd;'>".nl2br($message)."</td>
    </tr>
  </table>
  <p style='margin-top: 30px; font-size: 0.8rem; color: #666;'>Wiadomość wygenerowana automatycznie przez formularz na stronie coolfon.pl</p>
</body>
</html>
";

// Nagłówki e-mail
$headers = "MIME-Version: 1.0" . "\r\n";
$headers .= "Content-type:text/html;charset=UTF-8" . "\r\n";
$headers .= "From: Serwis Coolfon <info@coolfon.pl>" . "\r\n";
$headers .= "Reply-To: $email" . "\r\n";

if (mail($to, $subject, $email_content, $headers)) {
    echo json_encode(["status" => "success", "message" => "Wiadomość wysłana pomyślnie."]);
} else {
    http_response_code(500);
    echo json_encode(["status" => "error", "message" => "Błąd krytyczny podczas wysyłania e-mail."]);
}
?>
