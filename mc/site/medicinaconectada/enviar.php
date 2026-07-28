<?php
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

$email_fletic    = 'contato@fletic.com.br';
$email_remetente = 'contato@fletic.com.br';
$checklist_path  = __DIR__ . '/checklist_mc.pdf';
$checklist_nome  = 'Checklist_Elegibilidade_Telemedicina_MC.pdf';
$icone           = (strpos($interesse, 'vaga agora') !== false) ? 'ACESSO ANTECIPADO' : 'PRIORIDADE';
$primeiro_nome   = explode(' ', $nome)[0];

function enviar_email($para, $assunto, $html, $texto, $remetente, $anexo_path = null, $anexo_nome = null) {
    $boundary = '----MC_' . md5(uniqid(rand(), true));
    $alt      = '----MC_ALT_' . md5(uniqid(rand(), true));

    $headers  = "From: Medicina Conectada <$remetente>\r\n";
    $headers .= "Reply-To: $remetente\r\n";
    $headers .= "MIME-Version: 1.0\r\n";

    if ($anexo_path && file_exists($anexo_path)) {
        $headers .= "Content-Type: multipart/mixed; boundary=\"$boundary\"\r\n";

        $body  = "--$boundary\r\n";
        $body .= "Content-Type: multipart/alternative; boundary=\"$alt\"\r\n\r\n";
        $body .= "--$alt\r\n";
        $body .= "Content-Type: text/plain; charset=UTF-8\r\n";
        $body .= "Content-Transfer-Encoding: 8bit\r\n\r\n";
        $body .= $texto . "\r\n\r\n";
        $body .= "--$alt\r\n";
        $body .= "Content-Type: text/html; charset=UTF-8\r\n";
        $body .= "Content-Transfer-Encoding: 8bit\r\n\r\n";
        $body .= $html . "\r\n\r\n";
        $body .= "--$alt--\r\n\r\n";

        $pdf_base64 = chunk_split(base64_encode(file_get_contents($anexo_path)));
        $body .= "--$boundary\r\n";
        $body .= "Content-Type: application/pdf; name=\"$anexo_nome\"\r\n";
        $body .= "Content-Transfer-Encoding: base64\r\n";
        $body .= "Content-Disposition: attachment; filename=\"$anexo_nome\"\r\n\r\n";
        $body .= $pdf_base64 . "\r\n";
        $body .= "--$boundary--";
    } else {
        $headers .= "Content-Type: text/html; charset=UTF-8\r\n";
        $body = $html;
    }

    return mail($para, $assunto, $body, $headers);
}

// ── 1. E-mail para a FLETIC com dados do lead ─────────────
$html_fletic = "
<!DOCTYPE html>
<html lang='pt-BR'>
<head><meta charset='UTF-8'></head>
<body style='margin:0;padding:0;background:#f5f5f5;font-family:Arial,sans-serif;'>
  <table width='100%' cellpadding='0' cellspacing='0'>
    <tr><td align='center' style='padding:24px 16px;'>
      <table width='560' cellpadding='0' cellspacing='0' style='background:#ffffff;border:1px solid #ddd;'>
        <tr>
          <td style='background:#143D34;padding:20px 28px;'>
            <p style='margin:0;color:#C9A84C;font-size:17px;font-weight:bold;'>Nova inscrição — Medicina Conectada</p>
            <p style='margin:4px 0 0;color:#A8C8BF;font-size:12px;'>$icone &nbsp;|&nbsp; " . date('d/m/Y H:i') . "</p>
          </td>
        </tr>
        <tr>
          <td style='padding:28px;font-size:14px;color:#333;'>
            <table width='100%' cellpadding='6' cellspacing='0' style='border-collapse:collapse;'>
              <tr style='background:#EAF2EF;'>
                <td style='width:35%;font-weight:bold;color:#143D34;padding:8px 12px;'>Nome</td>
                <td style='padding:8px 12px;'>$nome</td>
              </tr>
              <tr>
                <td style='font-weight:bold;color:#143D34;padding:8px 12px;'>WhatsApp</td>
                <td style='padding:8px 12px;'>
                  <a href='https://wa.me/55" . preg_replace('/\D/', '', $whatsapp) . "' style='color:#143D34;font-weight:bold;'>$whatsapp</a>
                </td>
              </tr>
              <tr style='background:#EAF2EF;'>
                <td style='font-weight:bold;color:#143D34;padding:8px 12px;'>E-mail</td>
                <td style='padding:8px 12px;'>$email</td>
              </tr>
              <tr>
                <td style='font-weight:bold;color:#143D34;padding:8px 12px;'>Momento</td>
                <td style='padding:8px 12px;'>$momento</td>
              </tr>
              <tr style='background:#EAF2EF;'>
                <td style='font-weight:bold;color:#143D34;padding:8px 12px;'>Interesse</td>
                <td style='padding:8px 12px;font-weight:bold;color:#A67C2E;'>$icone</td>
              </tr>
            </table>
          </td>
        </tr>
        <tr>
          <td style='background:#143D34;padding:14px 28px;text-align:center;'>
            <p style='margin:0;color:#A8C8BF;font-size:11px;'>Medicina Conectada — Fletic Saúde Digital</p>
          </td>
        </tr>
      </table>
    </td></tr>
  </table>
</body>
</html>";

$texto_fletic = "Nova inscricao — Medicina Conectada\n\nInteresse: $icone\nNome: $nome\nWhatsApp: $whatsapp\nE-mail: $email\nMomento: $momento\nData: " . date('d/m/Y H:i');

enviar_email($email_fletic, "[MC] Nova inscricao — $nome ($icone)", $html_fletic, $texto_fletic, $email_remetente);

// ── 2. E-mail para o LEAD com checklist em anexo ─────────
$html_lead = "
<!DOCTYPE html>
<html lang='pt-BR'>
<head><meta charset='UTF-8'></head>
<body style='margin:0;padding:0;background:#FAFAF5;font-family:Arial,sans-serif;'>
  <table width='100%' cellpadding='0' cellspacing='0' style='background:#FAFAF5;'>
    <tr><td align='center' style='padding:32px 16px;'>
      <table width='600' cellpadding='0' cellspacing='0' style='background:#ffffff;border:1px solid #e0e0e0;'>
        <tr>
          <td style='background:#143D34;padding:28px 32px;'>
            <p style='margin:0;color:#C9A84C;font-size:20px;font-weight:bold;'>Medicina Conectada</p>
            <p style='margin:6px 0 0;color:#D4C080;font-size:13px;'>Domine a Telemedicina e Telessaúde. Transforme sua prática.</p>
          </td>
        </tr>
        <tr>
          <td style='padding:32px;color:#333333;font-size:15px;line-height:1.8;'>
            <p>Olá, <strong>$primeiro_nome</strong>!</p>
            <p>Sua prioridade está garantida no <strong>Medicina Conectada</strong>.</p>
            <p>Em anexo você encontra o seu primeiro entregável:</p>
            <p style='background:#EAF2EF;border-left:4px solid #143D34;padding:14px 18px;margin:16px 0;'>
              <strong style='color:#143D34;'>Checklist de Elegibilidade para Telemedicina e Telessaúde</strong><br>
              <span style='font-size:13px;color:#555;'>Com base na Resolução CFM 2.314/2022. Use antes de qualquer teleconsulta.</span>
            </p>
            <p>Ou acesse pelo link direto:<br>
              <a href='https://fletic.com.br/medicinaconectada/checklist_mc.pdf' style='color:#143D34;font-weight:bold;'>
                fletic.com.br/medicinaconectada/checklist_mc.pdf
              </a>
            </p>
            <p>Em breve você receberá todas as informações do lançamento.</p>
            <p>Qualquer dúvida, nos chame no WhatsApp: <strong>(11) 94543-6336</strong></p>
          </td>
        </tr>
        <tr>
          <td style='background:#143D34;padding:20px 32px;text-align:center;'>
            <p style='margin:0;color:#C9A84C;font-size:13px;font-weight:bold;'>Dra. Simone Farah &nbsp;|&nbsp; Dra. Danielle Magalhães</p>
            <p style='margin:4px 0 0;color:#A8C8BF;font-size:12px;'>Medicina Conectada — Fletic Saúde Digital</p>
          </td>
        </tr>
      </table>
    </td></tr>
  </table>
</body>
</html>";

$texto_lead = "Ola, $primeiro_nome!\n\nSua prioridade esta garantida no Medicina Conectada.\n\nEm anexo: Checklist de Elegibilidade para Telemedicina e Telessaude.\nCom base na Resolucao CFM 2.314/2022.\n\nLink direto: https://fletic.com.br/medicinaconectada/checklist_mc.pdf\n\nEm breve voce recebera as informacoes do lancamento.\n\nDuvidas? WhatsApp: (11) 94543-6336\n\nDra. Simone Farah | Dra. Danielle Magalhaes\nMedicina Conectada - Fletic";

enviar_email($email, 'Sua prioridade esta garantida — Medicina Conectada', $html_lead, $texto_lead, $email_remetente, $checklist_path, $checklist_nome);

http_response_code(200);
echo 'ok';
?>
