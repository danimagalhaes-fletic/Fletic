/**
 * MAP FLETIC — Backend do diagnóstico público (fletic.com.br/diagnostico)
 *
 * O que faz: recebe a resposta do formulário via POST, grava uma linha na planilha
 * a que este script está vinculado e envia um email de notificação para contato@fletic.com.br.
 *
 * COMO IMPLANTAR:
 * 1. Crie uma Planilha Google nova (ex: "MAP FLETIC — Diagnóstico (Respostas)").
 * 2. Extensões > Apps Script. Apague o conteúdo padrão e cole este arquivo inteiro.
 * 3. Implantar > Nova implantação > tipo "App da Web".
 *    - Executar como: Eu (sua conta)
 *    - Quem pode acessar: Qualquer pessoa
 * 4. Autorize o script quando solicitado (só na primeira vez).
 * 5. Copie a URL do Web App gerada e cole na constante GAS_ENDPOINT em vision/diagnostico.html.
 */

const SHEET_NAME = 'Respostas';
const NOTIFY_EMAIL = 'contato@fletic.com.br';

function doPost(e) {
  try {
    const data = JSON.parse(e.postData.contents);
    registrarResposta_(data);
    enviarNotificacao_(data);
    return ContentService.createTextOutput(JSON.stringify({ ok: true }))
      .setMimeType(ContentService.MimeType.JSON);
  } catch (err) {
    return ContentService.createTextOutput(JSON.stringify({ ok: false, error: String(err) }))
      .setMimeType(ContentService.MimeType.JSON);
  }
}

function registrarResposta_(data) {
  const sheet = getSheet_();
  const respostas = data.respostas || [];
  sheet.appendRow([
    new Date(),
    data.nome || '',
    data.whatsapp || '',
    data.origem || 'Site - /diagnostico',
    respostas[0] || '', respostas[1] || '', respostas[2] || '', respostas[3] || '',
    respostas[4] || '', respostas[5] || '', respostas[6] || '',
    'N' + data.nivel,
    'Novo',
    '', '', ''
  ]);
}

function getSheet_() {
  const ss = SpreadsheetApp.getActiveSpreadsheet();
  let sheet = ss.getSheetByName(SHEET_NAME);
  if (!sheet) {
    sheet = ss.insertSheet(SHEET_NAME);
    sheet.appendRow([
      'Data', 'Nome', 'WhatsApp', 'Origem',
      'P1', 'P2', 'P3', 'P4', 'P5', 'P6', 'P7',
      'Nível', 'Status do lead', 'Prioridade', 'Último contato', 'Próxima ação'
    ]);
  }
  return sheet;
}

function enviarNotificacao_(data) {
  const nivelNomes = { 1: 'N1 — Operacional', 2: 'N2 — Desorganizado', 3: 'N3 — Estruturando', 4: 'N4 — Escalável' };
  const nomeNivel = nivelNomes[data.nivel] || ('N' + data.nivel);
  const assunto = `Novo diagnóstico MAP FLETIC — ${data.nome} (${nomeNivel})`;
  const corpo = [
    'Novo lead respondeu o diagnóstico em fletic.com.br/diagnostico',
    '',
    `Nome: ${data.nome}`,
    `WhatsApp: ${data.whatsapp}`,
    `Nível: ${nomeNivel}`,
    '',
    `Respostas (P1-P7): ${(data.respostas || []).join(', ')}`,
    '',
    `Data: ${new Date().toLocaleString('pt-BR')}`
  ].join('\n');

  MailApp.sendEmail(NOTIFY_EMAIL, assunto, corpo);
}
