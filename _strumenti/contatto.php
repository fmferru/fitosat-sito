<?php
// Riceve il modulo "Programma pilota" del sito e lo inoltra a info@fitosat.it
header('Content-Type: application/json; charset=utf-8');
header('X-Content-Type-Options: nosniff');

if ($_SERVER['REQUEST_METHOD'] !== 'POST') {
    http_response_code(405);
    echo '{"ok":false}';
    exit;
}

// Campo trappola per i bot: se compilato, fingiamo successo e non inviamo nulla
if (!empty($_POST['sito'])) {
    echo '{"ok":true}';
    exit;
}

function campo($k, $max = 200) {
    $v = isset($_POST[$k]) ? (string) $_POST[$k] : '';
    $v = trim(str_replace(array("\r", "\n", "\0"), ' ', $v));
    return function_exists('mb_substr') ? mb_substr($v, 0, $max, 'UTF-8') : substr($v, 0, $max);
}

$nome    = campo('nome', 120);
$email   = campo('email', 160);
$azienda = campo('azienda', 160);
$coltura = campo('coltura', 60);
$ettari  = campo('ettari', 20);
$lingua  = campo('lingua', 5);
$msg     = isset($_POST['messaggio']) ? trim(str_replace("\0", '', (string) $_POST['messaggio'])) : '';
$msg     = function_exists('mb_substr') ? mb_substr($msg, 0, 3000, 'UTF-8') : substr($msg, 0, 3000);

if ($nome === '' || !filter_var($email, FILTER_VALIDATE_EMAIL)) {
    http_response_code(400);
    echo '{"ok":false}';
    exit;
}

$to      = 'info@fitosat.it';
$subject = '=?UTF-8?B?' . base64_encode('Programma pilota – ' . $nome) . '?=';
$body    = "Nuova richiesta dal sito fitosat.it\n\n"
         . "Nome: $nome\nEmail: $email\nAzienda: $azienda\nColtura: $coltura\nEttari: $ettari\nLingua: $lingua\n\n"
         . "Messaggio:\n$msg\n";
$headers = "From: Sito Fitosat <info@fitosat.it>\r\n"
         . "Reply-To: $email\r\n"
         . "MIME-Version: 1.0\r\n"
         . "Content-Type: text/plain; charset=UTF-8\r\n";

$ok = @mail($to, $subject, $body, $headers, '-finfo@fitosat.it');
echo json_encode(array('ok' => (bool) $ok));
