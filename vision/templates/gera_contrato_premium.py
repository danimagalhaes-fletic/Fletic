#!/usr/bin/env python3
"""
Contrato Fletic Vision — replica exatamente o layout do PDF aprovado,
com assinaturas em página dedicada (sem sobreposição).
"""
import asyncio
from playwright.async_api import async_playwright

HTML = """<!DOCTYPE html>
<html lang="pt-BR">
<head>
<meta charset="UTF-8"/>
<style>
@page { size: A4; margin: 0; }
* { box-sizing: border-box; margin: 0; padding: 0; }

body {
  font-family: 'Georgia', 'Times New Roman', serif;
  font-size: 10.3pt;
  color: #1a1a1a;
  background: #fff;
  -webkit-print-color-adjust: exact;
}

/* ═══════════════════════════════
   CAPA (branca, layout centralizado)
═══════════════════════════════ */
.cover {
  width: 210mm;
  height: 297mm;
  display: flex;
  flex-direction: column;
  page-break-after: always;
  background: #fff;
  position: relative;
}

/* Faixa teal fina no topo */
.cover-top-line {
  height: 3px;
  background: #0F7173;
  flex-shrink: 0;
}

/* Área principal da capa */
.cover-main {
  flex: 1;
  display: flex;
  flex-direction: column;
  align-items: center;
  padding: 0 22mm;
  padding-top: 28mm;
}

.cover-eyebrow {
  font-size: 6.8pt;
  font-weight: 400;
  color: #1B3A5C;
  letter-spacing: 4.5px;
  text-transform: uppercase;
  text-align: center;
  margin-bottom: 7mm;
}

.cover-rule {
  width: 38px;
  height: 2px;
  background: #1B3A5C;
  margin-bottom: 7mm;
}

.cover-title {
  font-size: 28pt;
  font-weight: 400;
  color: #1B3A5C;
  line-height: 1.2;
  text-align: center;
  letter-spacing: 0.2px;
  margin-bottom: 5mm;
}

.cover-subtitle {
  font-size: 11pt;
  font-weight: 400;
  color: #4a5568;
  font-style: italic;
  text-align: center;
  margin-bottom: 0;
}

/* Bloco de partes */
.cover-parties-wrap {
  width: 100%;
  margin-top: auto;
  margin-bottom: 9mm;
}

.cover-parties {
  display: flex;
  border-top: 1px solid #e2e8f0;
  border-bottom: 1px solid #e2e8f0;
  padding: 7mm 0;
  gap: 0;
}

.cover-party {
  flex: 1;
  padding-right: 12mm;
}
.cover-party:last-child {
  padding-right: 0;
  padding-left: 12mm;
  border-left: 1px solid #e2e8f0;
}

.cover-party-label {
  font-size: 6pt;
  font-weight: 700;
  color: #0F7173;
  letter-spacing: 3.5px;
  text-transform: uppercase;
  margin-bottom: 3.5mm;
}

.cover-party-name {
  font-size: 10.5pt;
  font-weight: 700;
  color: #1B3A5C;
  line-height: 1.35;
  margin-bottom: 2mm;
}

.cover-party-detail {
  font-size: 8.5pt;
  color: #718096;
  line-height: 1.65;
}

/* Meta row */
.cover-meta {
  display: flex;
  gap: 0;
  width: 100%;
  justify-content: center;
  padding-bottom: 0;
}

.cover-meta-item {
  flex: 1;
  text-align: center;
  padding: 0 4mm;
  border-right: 1px solid #e2e8f0;
}
.cover-meta-item:last-child { border-right: none; }

.cover-meta-label {
  font-size: 5.5pt;
  color: #a0aec0;
  text-transform: uppercase;
  letter-spacing: 2.5px;
  margin-bottom: 2.5mm;
}

.cover-meta-value {
  font-size: 10pt;
  font-weight: 700;
  color: #1B3A5C;
}

/* Rodapé da capa */
.cover-footer {
  flex-shrink: 0;
  height: 13mm;
  background: #f7f9fc;
  border-top: 1px solid #e2e8f0;
  display: flex;
  align-items: center;
  justify-content: space-between;
  padding: 0 22mm;
}

.cover-footer-brand {
  font-size: 7pt;
  font-weight: 700;
  color: #1B3A5C;
  letter-spacing: 2px;
  text-transform: uppercase;
}

.cover-footer-contact {
  font-size: 7pt;
  color: #a0aec0;
}

/* ═══════════════════════════════
   PÁGINAS INTERNAS
═══════════════════════════════ */
.page {
  width: 210mm;
  min-height: 297mm;
  padding: 14mm 22mm 14mm 22mm;
  page-break-after: always;
  display: flex;
  flex-direction: column;
}
.page:last-child { page-break-after: avoid; }

/* Cabeçalho corrente */
.ph {
  display: flex;
  justify-content: space-between;
  align-items: center;
  padding-bottom: 3mm;
  margin-bottom: 7mm;
  border-bottom: 1px solid #e2e8f0;
  flex-shrink: 0;
}

.ph-left {
  font-size: 6.5pt;
  color: #1B3A5C;
  letter-spacing: 0.5px;
}
.ph-left strong {
  font-weight: 700;
  letter-spacing: 1.5px;
}
.ph-dot {
  display: inline-block;
  width: 5px; height: 5px;
  border-radius: 50%;
  background: #0F7173;
  margin: 0 5px;
  vertical-align: middle;
}
.ph-right {
  font-size: 6.5pt;
  color: #0F7173;
  font-style: italic;
}

/* Área de conteúdo */
.ct { flex: 1; }

/* Preâmbulo */
.pre {
  font-size: 10.3pt;
  color: #1a1a1a;
  line-height: 1.8;
  margin-bottom: 4.5mm;
  text-align: justify;
}
.pre strong { color: #1a1a1a; }

/* Título de cláusula */
.ct-title {
  font-size: 7pt;
  font-weight: 700;
  color: #1B3A5C;
  letter-spacing: 2px;
  text-transform: uppercase;
  margin: 7mm 0 0 0;
  padding-bottom: 2mm;
  border-bottom: 1px solid #e2e8f0;
  margin-bottom: 4mm;
}
.ct-title:first-child { margin-top: 0; }

/* Item numerado — exatamente como no PDF: número bold + tab + texto justificado */
.ci {
  display: flex;
  gap: 0;
  margin-bottom: 3.5mm;
  padding-left: 0;
}
.ci-num {
  font-size: 10.3pt;
  font-weight: 700;
  color: #1B3A5C;
  min-width: 30px;
  flex-shrink: 0;
  line-height: 1.8;
  padding-right: 4mm;
}
.ci-text {
  font-size: 10.3pt;
  color: #1a1a1a;
  line-height: 1.8;
  text-align: justify;
}
.ci-text strong { color: #1a1a1a; }

/* Lista bullet com — teal */
.bl {
  list-style: none;
  margin: 1mm 0 3mm 4mm;
  padding: 0;
}
.bl li {
  font-size: 10.3pt;
  color: #1a1a1a;
  line-height: 1.75;
  padding-left: 6mm;
  position: relative;
  margin-bottom: 1mm;
  text-align: justify;
}
.bl li::before {
  content: "—";
  position: absolute;
  left: 0;
  color: #0F7173;
  font-weight: 700;
}

/* Rodapé corrente */
.pf {
  flex-shrink: 0;
  padding-top: 4mm;
  border-top: 1px solid #e2e8f0;
  display: flex;
  justify-content: space-between;
  margin-top: auto;
  padding-top: 4mm;
}
.pf-left { font-size: 6.5pt; color: #a0aec0; }
.pf-right { font-size: 6.5pt; color: #a0aec0; }

/* ═══════════════════════════════
   PÁGINA DE ASSINATURAS (dedicada)
═══════════════════════════════ */
.sig-page {
  width: 210mm;
  height: 297mm;
  padding: 14mm 22mm 14mm 22mm;
  page-break-before: always;
  display: flex;
  flex-direction: column;
}

.sig-place {
  font-size: 10.3pt;
  color: #1a1a1a;
  margin-bottom: 14mm;
  margin-top: 2mm;
}

/* Label de seção de assinatura */
.sig-section {
  font-size: 6pt;
  font-weight: 700;
  color: #0F7173;
  letter-spacing: 3.5px;
  text-transform: uppercase;
  margin-bottom: 14mm;
}

/* Grid de assinatura */
.sig-row {
  display: flex;
  gap: 12mm;
  margin-bottom: 0;
}

.sig-block { flex: 1; }

.sig-line {
  width: 80%;
  height: 1px;
  background: #1B3A5C;
  margin-bottom: 3mm;
}

.sig-name {
  font-size: 10.3pt;
  font-weight: 700;
  color: #1B3A5C;
  margin-bottom: 1px;
}

.sig-role {
  font-size: 8.5pt;
  color: #0F7173;
  margin-bottom: 1px;
}

.sig-detail {
  font-size: 8pt;
  color: #718096;
  line-height: 1.55;
}

.sig-divider {
  height: 1px;
  background: #e2e8f0;
  margin: 12mm 0;
}

.confidential {
  margin-top: auto;
  border: 1px solid #e2e8f0;
  padding: 4mm 8mm;
  background: #f7f9fc;
}

.confidential p {
  font-size: 7.5pt;
  color: #a0aec0;
  font-style: italic;
  text-align: center;
  line-height: 1.65;
}

</style>
</head>
<body>

<!-- ══════════════════ CAPA ══════════════════ -->
<div class="cover">
  <div class="cover-top-line"></div>

  <div class="cover-main">
    <div class="cover-eyebrow">Instrumento Particular de Prestação de Serviços</div>
    <div class="cover-rule"></div>
    <div class="cover-title">Contrato de Consultoria<br>Estratégica em Saúde Digital</div>
    <div class="cover-subtitle">Fletic Vision</div>

    <div class="cover-parties-wrap">
      <div class="cover-parties">
        <div class="cover-party">
          <div class="cover-party-label">Contratada</div>
          <div class="cover-party-name">Fletic Gestão Estratégica<br>de Inovação em Saúde Ltda.</div>
          <div class="cover-party-detail">CNPJ 57.625.870/0001-73<br>Petrópolis – RJ</div>
        </div>
        <div class="cover-party">
          <div class="cover-party-label">Contratante</div>
          <div class="cover-party-name">Ana Paula Carneiro Monteiro</div>
          <div class="cover-party-detail">CPF 083.584.837-08<br>Médica · Cardiologia &amp; Cuidados Paliativos</div>
        </div>
      </div>

      <div style="height:8mm"></div>

      <div class="cover-meta">
        <div class="cover-meta-item">
          <div class="cover-meta-label">Valor Total</div>
          <div class="cover-meta-value">R$ 24.000,00</div>
        </div>
        <div class="cover-meta-item">
          <div class="cover-meta-label">Prazo</div>
          <div class="cover-meta-value">12 Semanas</div>
        </div>
        <div class="cover-meta-item">
          <div class="cover-meta-label">Vigência</div>
          <div class="cover-meta-value">Julho – Setembro 2026</div>
        </div>
        <div class="cover-meta-item">
          <div class="cover-meta-label">Data</div>
          <div class="cover-meta-value">Julho de 2026</div>
        </div>
      </div>
    </div>
  </div>

  <div class="cover-footer">
    <div class="cover-footer-brand">Fletic Vision</div>
    <div class="cover-footer-contact">dani.magalhaes@fletic.com.br · simone.farah@fletic.com.br · fletic.com.br</div>
  </div>
</div>


<!-- ══════════════════ PÁG 2: Preâmbulo + Cláusulas 1–2 ══════════════════ -->
<div class="page">
  <div class="ph">
    <div class="ph-left"><strong>FLETIC VISION</strong><span class="ph-dot"></span>CONTRATO DE CONSULTORIA ESTRATÉGICA</div>
    <div class="ph-right">Confidencial</div>
  </div>
  <div class="ct">

    <div class="pre">Pelo presente instrumento particular, celebrado de forma eletrônica, de um lado:</div>

    <div class="pre"><strong>CONTRATADA:</strong> FLETIC — Gestão Estratégica de Inovação em Saúde Ltda., inscrita no CNPJ sob nº 57.625.870/0001-73, com sede na Rua Trinta e Um de Março, nº 18, Itaipava, Petrópolis – RJ, CEP 25.740-140, neste ato representada por suas sócias-fundadoras <strong>Danielle Gonzaga Morais Magalhães</strong> (CEO · Co-Fundadora) e <strong>Simone Farah</strong> (CMO · Fundadora), doravante denominada <strong>CONTRATADA</strong>;</div>

    <div class="pre"><strong>CONTRATANTE:</strong> <strong>Ana Paula Carneiro Monteiro</strong>, médica, pessoa física inscrita no CPF sob nº 083.584.837-08, e-mail: apcmonteiro55@hotmail.com, telefone: (21) 98221-1848, doravante denominada <strong>CONTRATANTE</strong>;</div>

    <div class="pre">As partes resolvem celebrar o presente <strong>Contrato de Prestação de Serviços de Consultoria Estratégica — Fletic Vision</strong>, que se regerá pelas cláusulas e condições abaixo:</div>

    <div class="ct-title">Cláusula Primeira — Do Objeto</div>

    <div class="ci">
      <span class="ci-num">1.1.</span>
      <span class="ci-text">O presente contrato tem como objeto a prestação de serviços de <strong>consultoria estratégica em saúde digital</strong>, no âmbito do programa <strong>Fletic Vision</strong>, voltado à estruturação do modelo assistencial, operacional, econômico e tecnológico da prática médica da CONTRATANTE, especializada em Cardiologia e Cuidados Paliativos.</span>
    </div>

    <div class="ci">
      <span class="ci-num">1.2.</span>
      <span class="ci-text">O projeto será conduzido em <strong>5 módulos sequenciais e integrados</strong>, ao longo de <strong>12 semanas (3 meses)</strong>, com entregas definidas ao final de cada etapa:</span>
    </div>

    <ul class="bl">
      <li><strong>Módulo 01 — Arquitetura Assistencial:</strong> Mapeamento da jornada atual e desenho do modelo híbrido de atendimento;</li>
      <li><strong>Módulo 02 — Estrutura Operacional:</strong> Protocolos, fluxos internos e organização da agenda;</li>
      <li><strong>Módulo 03 — Modelo Econômico:</strong> Estrutura de produtos, precificação e projeção de receita recorrente;</li>
      <li><strong>Módulo 04 — Arquitetura Tecnológica:</strong> Definição de ferramentas, telemedicina e política LGPD;</li>
      <li><strong>Módulo 05 — Gestão por Indicadores:</strong> KPIs, dashboard gerencial e rotina de acompanhamento.</li>
    </ul>

    <div class="ci">
      <span class="ci-num">1.3.</span>
      <span class="ci-text">A metodologia empregada integra fundamentos de gestão em saúde, telemedicina, value-based health care, transformação digital, estratégia comercial e governança por dados.</span>
    </div>

    <div class="ci">
      <span class="ci-num">1.4.</span>
      <span class="ci-text">Os encontros serão realizados de forma <strong>100% online e ao vivo</strong>, com encontros presenciais possíveis em caráter excepcional, mediante acordo prévio entre as partes.</span>
    </div>

    <div class="ct-title">Cláusula Segunda — Do Investimento e Forma de Pagamento</div>

    <div class="ci">
      <span class="ci-num">2.1.</span>
      <span class="ci-text">Pelos serviços descritos na Cláusula Primeira, a CONTRATANTE pagará à CONTRATADA o valor total de <strong>R$ 24.000,00 (vinte e quatro mil reais)</strong>, estruturado em duas fases:</span>
    </div>

    <ul class="bl">
      <li><strong>Fase 1 (Módulos 01 e 02):</strong> R$ 8.000,00 (oito mil reais);</li>
      <li><strong>Fase 2 (Módulos 03, 04 e 05):</strong> R$ 16.000,00 (dezesseis mil reais).</li>
    </ul>

    <div class="ci">
      <span class="ci-num">2.2.</span>
      <span class="ci-text">A CONTRATANTE optou pelo pagamento parcelado em <strong>3 (três) parcelas de R$ 8.000,00 (oito mil reais)</strong> cada, com vencimentos nos dias <strong>05 de julho, 05 de agosto e 05 de setembro de 2026</strong>, realizadas via transferência PIX para chave a ser informada pela CONTRATADA.</span>
    </div>

    <div class="ci">
      <span class="ci-num">2.3.</span>
      <span class="ci-text">A confirmação do pagamento da primeira parcela constitui aceite pleno, irrevogável e irretratável deste contrato e autoriza o início dos serviços.</span>
    </div>

    <div class="ci">
      <span class="ci-num">2.4.</span>
      <span class="ci-text">O atraso no pagamento de qualquer parcela por mais de <strong>5 (cinco) dias úteis</strong> poderá ensejar a suspensão temporária dos serviços, sem prejuízo da cobrança dos valores em aberto, acrescidos de multa de 2% e juros de 1% ao mês sobre o valor da parcela em atraso.</span>
    </div>

  </div>
  <div class="pf">
    <span class="pf-left">Fletic Vision · Contrato de Consultoria Estratégica · Confidencial</span>
    <span class="pf-right">Página 2</span>
  </div>
</div>


<!-- ══════════════════ PÁG 3: Cláusulas 3–5 ══════════════════ -->
<div class="page">
  <div class="ph">
    <div class="ph-left"><strong>FLETIC VISION</strong><span class="ph-dot"></span>CONTRATO DE CONSULTORIA ESTRATÉGICA</div>
    <div class="ph-right">Confidencial</div>
  </div>
  <div class="ct">

    <div class="ct-title">Cláusula Terceira — Das Obrigações da Contratada</div>
    <div class="ci"><span class="ci-num">3.1.</span><span class="ci-text">Constituem obrigações da CONTRATADA:</span></div>
    <ul class="bl">
      <li>Conduzir os módulos e entregas previstos no programa Fletic Vision com padrão técnico, confidencialidade e rigor metodológico;</li>
      <li>Disponibilizar materiais estratégicos, ferramentas e suporte nos canais definidos durante o período contratado;</li>
      <li>Garantir a qualidade das entregas e o cumprimento do cronograma de 12 semanas;</li>
      <li>Atuar com ética, profissionalismo e alinhamento às necessidades da CONTRATANTE;</li>
      <li>Cumprir as disposições da Lei nº 13.709/2018 (LGPD) no tratamento de dados.</li>
    </ul>

    <div class="ct-title">Cláusula Quarta — Das Obrigações da Contratante</div>
    <div class="ci"><span class="ci-num">4.1.</span><span class="ci-text">Constituem obrigações da CONTRATANTE:</span></div>
    <ul class="bl">
      <li>Realizar os pagamentos nos prazos e formas estabelecidos na Cláusula Segunda;</li>
      <li>Participar ativamente dos encontros e etapas previstas, fornecendo as informações necessárias para o desenvolvimento do projeto;</li>
      <li>Respeitar o cronograma acordado e comunicar com antecedência mínima de 48 horas qualquer necessidade de reagendamento;</li>
      <li>Não compartilhar materiais, metodologias e ferramentas exclusivas da CONTRATADA com terceiros, sem autorização prévia por escrito.</li>
    </ul>

    <div class="ct-title">Cláusula Quinta — Da Confidencialidade</div>
    <div class="ci"><span class="ci-num">5.1.</span><span class="ci-text">As partes se comprometem a manter em sigilo absoluto todas as informações confidenciais trocadas no âmbito deste contrato, incluindo dados clínicos, financeiros, estratégicos e operacionais.</span></div>
    <div class="ci"><span class="ci-num">5.2.</span><span class="ci-text">A obrigação de confidencialidade é perene e permanece vigente por prazo indeterminado, mesmo após o encerramento do contrato.</span></div>

    <div class="ct-title">Cláusula Sexta — Do Uso de Imagem e Dados para Fins de Marketing</div>
    <div class="ci"><span class="ci-num">6.1.</span><span class="ci-text">A CONTRATANTE autoriza expressamente a CONTRATADA a utilizar, para fins de divulgação institucional e marketing digital:</span></div>
    <ul class="bl">
      <li>Dados de crescimento e resultados obtidos ao longo do projeto (de forma anonimizada ou nominal, conforme preferência da CONTRATANTE);</li>
      <li>Depoimentos e relatos de experiência, mediante aprovação prévia da CONTRATANTE;</li>
      <li>Nome, especialidade e informações profissionais da CONTRATANTE, para composição de cases de sucesso;</li>
      <li>Imagens e fotos da CONTRATANTE, desde que previamente autorizadas por escrito em cada uso específico.</li>
    </ul>
    <div class="ci"><span class="ci-num">6.2.</span><span class="ci-text">A CONTRATANTE poderá revogar esta autorização a qualquer momento, por comunicação escrita à CONTRATADA, sem que isso implique rescisão do presente contrato.</span></div>
    <div class="ci"><span class="ci-num">6.3.</span><span class="ci-text">É vedada a divulgação de informações sensíveis, dados pessoais de pacientes ou qualquer conteúdo que viole a privacidade da CONTRATANTE ou de terceiros, nos termos da LGPD.</span></div>

    <div class="ct-title">Cláusula Sétima — Da Propriedade Intelectual</div>
    <div class="ci"><span class="ci-num">7.1.</span><span class="ci-text">Todos os materiais, metodologias, ferramentas, frameworks e conteúdos desenvolvidos e disponibilizados pela CONTRATADA são de sua propriedade exclusiva, sendo vedada à CONTRATANTE sua reprodução, distribuição ou comercialização sem autorização prévia e por escrito.</span></div>
    <div class="ci"><span class="ci-num">7.2.</span><span class="ci-text">Os entregáveis personalizados produzidos especificamente para a CONTRATANTE (diagnósticos, planos, protocolos, dashboards) são de uso exclusivo da CONTRATANTE para sua prática profissional.</span></div>

  </div>
  <div class="pf">
    <span class="pf-left">Fletic Vision · Contrato de Consultoria Estratégica · Confidencial</span>
    <span class="pf-right">Página 3</span>
  </div>
</div>


<!-- ══════════════════ PÁG 4: Cláusulas 8–12 ══════════════════ -->
<div class="page">
  <div class="ph">
    <div class="ph-left"><strong>FLETIC VISION</strong><span class="ph-dot"></span>CONTRATO DE CONSULTORIA ESTRATÉGICA</div>
    <div class="ph-right">Confidencial</div>
  </div>
  <div class="ct">

    <div class="ct-title">Cláusula Oitava — Da Rescisão</div>
    <div class="ci"><span class="ci-num">8.1.</span><span class="ci-text">O presente contrato poderá ser rescindido por qualquer das partes mediante comunicação escrita com antecedência mínima de <strong>15 (quinze) dias</strong>.</span></div>
    <div class="ci"><span class="ci-num">8.2.</span><span class="ci-text">Em caso de rescisão por iniciativa da CONTRATANTE após o início dos serviços, serão devidos os valores proporcionais às etapas já realizadas, sem direito a restituição das parcelas pagas.</span></div>
    <div class="ci"><span class="ci-num">8.3.</span><span class="ci-text">Em caso de rescisão por inadimplemento da CONTRATANTE, todos os valores em aberto tornam-se imediatamente exigíveis.</span></div>
    <div class="ci"><span class="ci-num">8.4.</span><span class="ci-text">Em caso de rescisão por iniciativa ou inadimplemento da CONTRATADA, será devida a restituição proporcional dos valores pagos relativos às etapas não executadas.</span></div>

    <div class="ct-title">Cláusula Nona — Da Proteção de Dados (LGPD)</div>
    <div class="ci"><span class="ci-num">9.1.</span><span class="ci-text">As partes se comprometem a tratar os dados pessoais compartilhados no âmbito deste contrato em conformidade com a Lei nº 13.709/2018 (LGPD), garantindo sua segurança, confidencialidade e uso exclusivo para as finalidades aqui previstas.</span></div>
    <div class="ci"><span class="ci-num">9.2.</span><span class="ci-text">A CONTRATADA não compartilhará dados pessoais da CONTRATANTE ou de seus pacientes com terceiros, salvo mediante autorização expressa ou obrigação legal.</span></div>

    <div class="ct-title">Cláusula Décima — Do Prazo</div>
    <div class="ci"><span class="ci-num">10.1.</span><span class="ci-text">O presente contrato tem vigência de <strong>12 (doze) semanas</strong>, contadas a partir da data de confirmação do primeiro pagamento, podendo ser prorrogado por acordo mútuo entre as partes.</span></div>

    <div class="ct-title">Cláusula Décima Primeira — Do Foro</div>
    <div class="ci"><span class="ci-num">11.1.</span><span class="ci-text">As partes elegem o foro da Comarca de <strong>Petrópolis – RJ</strong> para dirimir quaisquer dúvidas ou litígios oriundos do presente contrato, renunciando a qualquer outro, por mais privilegiado que seja.</span></div>

    <div class="ct-title">Cláusula Décima Segunda — Das Disposições Gerais</div>
    <div class="ci"><span class="ci-num">12.1.</span><span class="ci-text">A confirmação eletrônica do pagamento ou assinatura digital deste instrumento constitui aceite integral de todos os termos e condições aqui estabelecidos.</span></div>
    <div class="ci"><span class="ci-num">12.2.</span><span class="ci-text">Eventuais alterações neste contrato somente serão válidas se formalizadas por escrito e assinadas por ambas as partes.</span></div>
    <div class="ci"><span class="ci-num">12.3.</span><span class="ci-text">A tolerância de qualquer das partes em relação ao descumprimento de cláusulas não implica novação ou renúncia de direitos.</span></div>

  </div>
  <div class="pf">
    <span class="pf-left">Fletic Vision · Contrato de Consultoria Estratégica · Confidencial</span>
    <span class="pf-right">Página 4</span>
  </div>
</div>


<!-- ══════════════════ PÁG 5: ASSINATURAS (página dedicada) ══════════════════ -->
<div class="sig-page">
  <div class="ph">
    <div class="ph-left"><strong>FLETIC VISION</strong><span class="ph-dot"></span>CONTRATO DE CONSULTORIA ESTRATÉGICA</div>
    <div class="ph-right">Confidencial</div>
  </div>

  <div class="ct">
    <div class="sig-place">Petrópolis – RJ, _____ de julho de 2026.</div>

    <!-- Contratadas -->
    <div class="sig-section">Contratada</div>

    <div class="sig-row">
      <div class="sig-block">
        <div class="sig-line"></div>
        <div class="sig-name">Danielle Gonzaga Morais Magalhães</div>
        <div class="sig-role">CEO · Co-Fundadora</div>
        <div class="sig-detail">Fletic Gestão Estratégica de Inovação em Saúde Ltda.<br>CNPJ: 57.625.870/0001-73</div>
      </div>
      <div class="sig-block">
        <div class="sig-line"></div>
        <div class="sig-name">Simone Farah</div>
        <div class="sig-role">CMO · Fundadora</div>
        <div class="sig-detail">Fletic Gestão Estratégica de Inovação em Saúde Ltda.<br>CNPJ: 57.625.870/0001-73</div>
      </div>
    </div>

    <div class="sig-divider"></div>

    <!-- Contratante -->
    <div class="sig-section">Contratante</div>

    <div class="sig-row">
      <div class="sig-block" style="max-width: 50%">
        <div class="sig-line"></div>
        <div class="sig-name">Ana Paula Carneiro Monteiro</div>
        <div class="sig-role">Médica</div>
        <div class="sig-detail">CPF: 083.584.837-08</div>
      </div>
      <div class="sig-block"></div>
    </div>

    <div class="confidential">
      <p>Este instrumento é de natureza confidencial e destinado exclusivamente às partes signatárias.<br>
      Sua reprodução, distribuição ou divulgação a terceiros é expressamente vedada sem autorização prévia e por escrito da CONTRATADA.</p>
    </div>
  </div>

  <div class="pf">
    <span class="pf-left">Fletic Vision · Contrato de Consultoria Estratégica · Confidencial</span>
    <span class="pf-right">Página 5</span>
  </div>
</div>

</body>
</html>"""

async def main():
    async with async_playwright() as p:
        browser = await p.chromium.launch(
            executable_path="/opt/pw-browsers/chromium-1194/chrome-linux/chrome"
        )
        page = await browser.new_page()
        await page.set_content(HTML, wait_until="networkidle")
        await page.pdf(
            path="/tmp/contrato_vision_ana_paula_monteiro.pdf",
            format="A4",
            print_background=True,
            margin={"top": "0", "right": "0", "bottom": "0", "left": "0"},
        )
        await browser.close()
    print("Gerado: /tmp/contrato_vision_ana_paula_monteiro.pdf")

asyncio.run(main())
