<?php
use PHPMailer\PHPMailer\PHPMailer;
use PHPMailer\PHPMailer\Exception;

require 'vendor/autoload.php';

if ($_SERVER['REQUEST_METHOD'] !== 'POST') {
    http_response_code(405);
    exit;
}

function limpar_cabecalho($valor) {
    return str_replace(["\r", "\n"], '', $valor);
}

$nome      = limpar_cabecalho(htmlspecialchars(trim($_POST['nome'] ?? '')));
$whatsapp  = limpar_cabecalho(htmlspecialchars(trim($_POST['whatsapp'] ?? '')));
$email     = trim($_POST['email'] ?? '');
$momento   = limpar_cabecalho(htmlspecialchars(trim($_POST['momento'] ?? '')));
$interesse = limpar_cabecalho(htmlspecialchars(trim($_POST['interesse'] ?? '')));

if (!$nome || !$email || !$whatsapp || !filter_var($email, FILTER_VALIDATE_EMAIL)) {
    http_response_code(400);
    exit;
}

$email = htmlspecialchars($email);

$icone         = (strpos($interesse, 'vaga agora') !== false) ? 'CHECKLIST DE ELEGIBILIDADE' : 'PRIORIDADE';
$primeiro_nome = explode(' ', $nome)[0];
$checklist     = __DIR__ . '/checklist_mc.pdf';
$comunidade    = 'https://chat.whatsapp.com/Lo1alaMU2Qq99KMzezvQPX?mode=gi_t';

$smtp = require __DIR__ . '/smtp_config.php';

function criarMailer($smtp) {
    $mail = new PHPMailer(true);
    $mail->isSMTP();
    $mail->Host       = $smtp['host'];
    $mail->SMTPAuth   = true;
    $mail->Username   = $smtp['username'];
    $mail->Password   = $smtp['password'];
    $mail->SMTPSecure = $smtp['secure'];
    $mail->Port       = $smtp['port'];
    $mail->CharSet    = 'UTF-8';
    $mail->Encoding   = 'base64';
    $mail->setFrom('contato@fletic.com.br', 'Medicina Conectada');
    return $mail;
}

// E-mail para a Fletic com dados do lead
try {
    $mail = criarMailer($smtp);
    $mail->addAddress('contato@fletic.com.br', 'Fletic');
    $mail->Subject = "[MC] Nova inscricao - $nome ($icone)";
    $mail->isHTML(true);
    $mail->Body = "
    <div style='font-family:Arial,sans-serif;max-width:600px;margin:0 auto'>
    <div style='background:#143D34;padding:20px 28px'>
      <p style='margin:0;color:#C9A84C;font-size:17px;font-weight:bold'>Nova inscri&ccedil;&atilde;o &mdash; Medicina Conectada</p>
      <p style='margin:4px 0 0;color:#A8C8BF;font-size:12px'>$icone &nbsp;|&nbsp; " . date('d/m/Y H:i') . "</p>
    </div>
    <div style='padding:28px'>
    <table width='100%' cellpadding='8' cellspacing='0' style='border-collapse:collapse;font-size:14px'>
      <tr style='background:#EAF2EF'><td style='font-weight:bold;color:#143D34;width:35%'>Nome</td><td>$nome</td></tr>
      <tr><td style='font-weight:bold;color:#143D34'>WhatsApp</td><td><a href='https://wa.me/55" . preg_replace('/\D/','',$whatsapp) . "' style='color:#143D34;font-weight:bold'>$whatsapp</a></td></tr>
      <tr style='background:#EAF2EF'><td style='font-weight:bold;color:#143D34'>E-mail</td><td>$email</td></tr>
      <tr><td style='font-weight:bold;color:#143D34'>Momento</td><td>$momento</td></tr>
      <tr style='background:#EAF2EF'><td style='font-weight:bold;color:#143D34'>Interesse</td><td style='font-weight:bold;color:#A67C2E'>$icone</td></tr>
    </table>
    </div>
    <div style='background:#143D34;padding:14px 28px;text-align:center'>
      <p style='margin:0;color:#A8C8BF;font-size:11px'>Medicina Conectada &mdash; Fletic Sa&uacute;de Digital</p>
    </div>
    </div>";
    $mail->send();
} catch (Exception $e) { error_log($e->getMessage()); }

// E-mail para o aluno com checklist
try {
    $mail = criarMailer($smtp);
    $mail->addAddress($email, $nome);
    $mail->Subject = 'Sua prioridade esta garantida - Medicina Conectada';
    $mail->isHTML(true);
    $mail->Body = "
    <div style='font-family:Arial,sans-serif;max-width:600px;margin:0 auto'>
    <div style='background:#143D34;padding:28px 32px'>
      <p style='margin:0;color:#C9A84C;font-size:20px;font-weight:bold'>Medicina Conectada</p>
      <p style='margin:6px 0 0;color:#D4C080;font-size:13px'>Domine a Telemedicina e Teless&aacute;ude. Transforme sua pr&aacute;tica.</p>
    </div>
    <div style='padding:32px;color:#333;font-size:15px;line-height:1.8'>
      <p>Ol&aacute;, <strong>$primeiro_nome</strong>!</p>
      <p>Sua prioridade est&aacute; garantida no <strong>Medicina Conectada</strong>.</p>
      <p>Em anexo voc&ecirc; encontra o seu primeiro entreg&aacute;vel:</p>
      <div style='background:#EAF2EF;border-left:4px solid #143D34;padding:14px 18px;margin:16px 0'>
        <strong style='color:#143D34'>Checklist de Elegibilidade para Telemedicina e Teless&aacute;ude</strong><br>
        <span style='font-size:13px;color:#555'>Com base na Resolu&ccedil;&atilde;o CFM 2.314/2022. Use antes de qualquer teleconsulta.</span>
      </div>
      <p>Ou acesse pelo link direto:<br>
        <a href='https://fletic.com.br/medicinaconectada/checklist_mc.pdf' style='color:#143D34;font-weight:bold'>
          fletic.com.br/medicinaconectada/checklist_mc.pdf
        </a>
      </p>
      <div style='background:#EAF2EF;border-left:4px solid #C9A84C;padding:14px 18px;margin:16px 0'>
        <strong style='color:#143D34'>Entre na Comunidade Medicina Conectada</strong><br>
        <span style='font-size:13px;color:#555'>Grupo exclusivo no WhatsApp para tirar d&uacute;vidas, receber novidades e trocar com outros m&eacute;dicos.</span><br><br>
        <a href='$comunidade' style='color:#143D34;font-weight:bold'>Entrar na comunidade agora</a>
      </div>
      <p>D&uacute;vidas? Nos chame no WhatsApp: <strong>(11) 94543-6336</strong></p>
    </div>
    <div style='background:#143D34;padding:20px 32px;text-align:center'>
      <p style='margin:0;color:#C9A84C;font-size:13px;font-weight:bold'>Dra. Simone Farah &nbsp;|&nbsp; Dra. Danielle Magalh&atilde;es</p>
      <p style='margin:4px 0 0;color:#A8C8BF;font-size:12px'>Medicina Conectada &mdash; Fletic Sa&uacute;de Digital</p>
    </div>
    </div>";
    if (file_exists($checklist)) {
        $mail->addAttachment($checklist, 'Checklist_Elegibilidade_Telemedicina_MC.pdf');
    }
    $mail->send();
} catch (Exception $e) { error_log($e->getMessage()); }

http_response_code(200);
echo 'ok';
