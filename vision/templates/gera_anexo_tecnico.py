#!/usr/bin/env python3
"""
Fletic Vision — Anexo Técnico (Estrutura do Projeto)
Layout: Medicina Vaccaro reference document.
4 pages: Cover/Objetivo/Metodologia/M01 | M02-M04 | M04-M05 | Cronograma/Critérios/Assinatura
"""

import asyncio
from playwright.async_api import async_playwright

# ── CLIENT DATA ────────────────────────────────────────────────────────────────

ANA_PAULA = {
    "nome":         "Ana Paula Rodrigues",
    "clinica":      "APR LTDA",
    "dra":          "Dra. Ana Paula Rodrigues",
    "especialidade":"Cardiologia & Cuidados Paliativos",
    "cidade":       "Rio de Janeiro – RJ",
    "mes_ano":      "Junho 2026",
    "objetivo": (
        "Desenvolver um modelo assistencial híbrido estruturado para a prática de cardiologia e "
        "cuidados paliativos da Dra. Ana Paula Rodrigues, transformando a operação presencial atual "
        "em um sistema recorrente, com dados e governança, visando:"
    ),
    "objetivos_bullets": [
        "Captura de receita recorrente via programas de acompanhamento de pacientes crônicos cardíacos",
        "Integração entre atendimento presencial e teleconsulta para follow-up longitudinal",
        "Criação de previsibilidade financeira com indicadores clínicos e operacionais formais",
        "Redução da dependência do modelo 100% transacional e do volume de consultas avulsas",
    ],
    "modulos": [
        {
            "num": "01", "titulo": "Arquitetura Assistencial",
            "objetivo": "Definir o modelo de cuidado",
            "entregaveis": [
                ("Mapeamento da jornada atual (AS-IS) da carteira de pacientes crônicos", []),
                ("Desenho da jornada ideal (TO-BE) com protocolos de acompanhamento e retorno", []),
                ("Segmentação da carteira por risco cardíaco e frequência de cuidado", []),
                ("Estruturação dos serviços assistenciais", ["Consulta presencial", "Teleconsulta de acompanhamento", "Cuidados paliativos", "Retorno estruturado"]),
                ("Critérios de elegibilidade para atendimento digital vs. presencial", []),
            ],
        },
        {
            "num": "02", "titulo": "Estrutura Operacional",
            "objetivo": "Transformar o modelo em operação",
            "entregaveis": [
                ("Protocolos assistenciais por etapa", ["Pré-consulta", "Consulta cardíaca", "Pós-consulta e follow-up"]),
                ("Scripts operacionais e fluxos por função", ["Recepção", "Médico"]),
                ("Organização da agenda", ["Blocos presenciais", "Blocos digitais", "Blocos de retorno programado"]),
                ("Regras de alocação de capacidade e gestão de lista de espera", []),
                ("Definição de responsabilidades — base para estruturação da equipe", []),
            ],
        },
        {
            "num": "03", "titulo": "Modelo Econômico",
            "objetivo": "Estruturar crescimento sustentável",
            "entregaveis": [
                ("Análise do modelo de receita atual — avulso vs. recorrente", []),
                ("Programas de acompanhamento cardíaco longitudinal", ["Contratos de cuidado", "Planos de retorno periódico"]),
                ("Estrutura de precificação por complexidade", ["Cardiologia geral", "Cuidados paliativos"]),
                ("Simulação de impacto financeiro e projeção de receita recorrente", []),
                ("Estratégia de retenção e aumento do LTV por paciente", []),
            ],
        },
        {
            "num": "04", "titulo": "Arquitetura Tecnológica",
            "objetivo": "Suportar o modelo com eficiência",
            "entregaveis": [
                ("Seleção de plataforma de telemedicina para acompanhamento cardíaco", []),
                ("Fluxos digitais estruturados", ["Pré-consulta automatizada", "Follow-up pós-consulta"]),
                ("Integração entre prontuário eletrônico e agenda digital", []),
                ("Padronização de uso das ferramentas pela equipe", []),
                ("Política de segurança da informação — LGPD", []),
            ],
        },
        {
            "num": "05", "titulo": "Gestão por Indicadores",
            "objetivo": "Garantir controle e evolução contínua",
            "entregaveis": [
                ("Definição de KPIs", ["Clínicos: adesão, retorno, estratificação de risco cardíaco", "Operacionais: ocupação, cancelamentos, tempo de espera", "Financeiros: receita por paciente, custo por serviço"]),
                ("Construção de dashboard gerencial", []),
                ("Rotina de acompanhamento", ["Semanal", "Mensal"]),
                ("Estrutura de tomada de decisão baseada em dados", []),
            ],
        },
    ],
    "criterios_sucesso": [
        "Jornada cardíaca e de cuidados paliativos estruturada e operante",
        "Protocolos implementados e utilizados pela equipe",
        "Programa de acompanhamento de crônicos cardíacos com pacientes ativos",
        "Modelo econômico ativo — serviços precificados e ofertados com recorrência",
        "Indicadores sendo acompanhados em rotina definida",
        "Dashboard funcional com decisões baseadas em dados",
    ],
    "output": "/tmp/anexo_tecnico_ana_paula.pdf",
}

ETHEL = {
    "nome":         "Ethel Pinella",
    "clinica":      "Ethel Pinella Clínica",
    "dra":          "Dra. Ethel Pinella",
    "especialidade":"Endoscopia & Nutrologia",
    "cidade":       "Leblon, Rio de Janeiro – RJ",
    "mes_ano":      "Junho 2026",
    "objetivo": (
        "Estruturar o modelo operacional e econômico da prática de endoscopia e nutrologia da "
        "Dra. Ethel Pinella, transformando atendimentos avulsos em programas de acompanhamento "
        "longitudinal com integração digital e governança por dados, visando:"
    ),
    "objetivos_bullets": [
        "Receita recorrente via programas de acompanhamento nutrológico e pós-procedimento",
        "Integração da telemedicina com protocolo clínico definido para follow-up",
        "Criação de previsibilidade financeira com indicadores formais e dashboard gerencial",
        "Redução da dependência de volume e de captação constante de novos pacientes",
    ],
    "modulos": [
        {
            "num": "01", "titulo": "Arquitetura Assistencial",
            "objetivo": "Definir o modelo de cuidado",
            "entregaveis": [
                ("Mapeamento da jornada atual (AS-IS) da carteira de pacientes", []),
                ("Desenho da jornada ideal (TO-BE) com protocolos nutrológicos e pós-endoscopia", []),
                ("Segmentação da carteira por perfil de saúde e frequência de acompanhamento", []),
                ("Estruturação dos serviços assistenciais", ["Consulta nutrológica", "Follow-up pós-endoscopia", "Teleconsulta de acompanhamento", "Programas de longevidade"]),
                ("Critérios de elegibilidade para telemedicina vs. presencial", []),
            ],
        },
        {
            "num": "02", "titulo": "Estrutura Operacional",
            "objetivo": "Transformar o modelo em operação",
            "entregaveis": [
                ("Protocolos assistenciais por etapa", ["Pré-consulta", "Consulta nutrológica", "Pós-endoscopia e follow-up"]),
                ("Scripts operacionais e fluxos por função", ["Recepção", "Médico"]),
                ("Organização da agenda", ["Blocos presenciais", "Blocos digitais", "Blocos de retorno programado"]),
                ("Regras de alocação de capacidade e gestão de lista de espera", []),
                ("Definição de responsabilidades — base para contratação de equipe", []),
            ],
        },
        {
            "num": "03", "titulo": "Modelo Econômico",
            "objetivo": "Estruturar crescimento sustentável",
            "entregaveis": [
                ("Análise do modelo de receita atual — avulso vs. recorrente", []),
                ("Definição de novos produtos e programas", ["Programas de acompanhamento nutrológico mensal", "Pacotes pós-endoscopia", "Programas de longevidade e performance"]),
                ("Estrutura de precificação por complexidade", ["Nutrologia e longevidade", "Endoscopia e pós-procedimento"]),
                ("Simulação de impacto financeiro e projeção de receita recorrente", []),
                ("Estratégia de aumento de ticket médio por paciente", []),
            ],
        },
        {
            "num": "04", "titulo": "Arquitetura Tecnológica",
            "objetivo": "Suportar o modelo com eficiência",
            "entregaveis": [
                ("Seleção de plataforma de telemedicina dedicada para nutrologia e follow-up", []),
                ("Fluxos digitais estruturados", ["Pré-consulta automatizada", "Follow-up pós-consulta e pós-procedimento"]),
                ("Integração entre prontuário eletrônico e agenda digital", []),
                ("Padronização de uso das ferramentas pela equipe", []),
                ("Política de segurança da informação — LGPD", []),
            ],
        },
        {
            "num": "05", "titulo": "Gestão por Indicadores",
            "objetivo": "Garantir controle e evolução contínua",
            "entregaveis": [
                ("Definição de KPIs", ["Clínicos: adesão, retorno, estratificação de risco nutrológico", "Operacionais: ocupação, cancelamentos, tempo de espera", "Financeiros: receita por paciente, custo por serviço"]),
                ("Construção de dashboard gerencial", []),
                ("Rotina de acompanhamento", ["Semanal", "Mensal"]),
                ("Estrutura de tomada de decisão baseada em dados", []),
            ],
        },
    ],
    "criterios_sucesso": [
        "Jornada nutrológica e pós-endoscopia estruturada e operante",
        "Protocolos implementados e utilizados pela equipe",
        "Programas de acompanhamento nutrológico com pacientes recorrentes ativos",
        "Modelo econômico ativo — produtos precificados e ofertados com recorrência",
        "Indicadores sendo acompanhados em rotina definida",
        "Dashboard funcional com decisões baseadas em dados",
    ],
    "output": "/tmp/anexo_tecnico_ethel.pdf",
}

DANIELA_BORGES = {
    "nome":         "Daniela Borges",
    "clinica":      "Imagecor",
    "dra":          "Dra. Daniela Borges",
    "especialidade":"Cardiologia",
    "cidade":       "Catete, Rio de Janeiro – RJ",
    "mes_ano":      "Junho 2026",
    "objetivo": (
        "Transformar a operação da Imagecor — com capacidade subutilizada e taxa de retorno "
        "abaixo de 50% — em um modelo cardiológico recorrente, previsível e financeiramente "
        "sustentável, visando:"
    ),
    "objetivos_bullets": [
        "Aumento da taxa de retorno dos pacientes cardíacos crônicos pós-exame (Eco, Doppler, Holter)",
        "Ocupação plena das 3 salas com gestão ativa de capacidade e demanda",
        "Criação de previsibilidade financeira com dashboard e indicadores gerenciais formais",
        "Redução da dependência de captação constante — receita recorrente como base do modelo",
    ],
    "modulos": [
        {
            "num": "01", "titulo": "Arquitetura Assistencial",
            "objetivo": "Definir o modelo de cuidado",
            "entregaveis": [
                ("Mapeamento da jornada atual (AS-IS) dos pacientes cardíacos e pós-exame", []),
                ("Desenho da jornada ideal (TO-BE) com protocolo de retorno pós-Eco e Holter", []),
                ("Segmentação da carteira", ["Crônicos cardíacos", "Pacientes pós-procedimento", "Novos encaminhamentos"]),
                ("Estruturação dos serviços por tipo e frequência esperada de retorno", []),
                ("Critérios de elegibilidade para telemedicina vs. presencial", []),
            ],
        },
        {
            "num": "02", "titulo": "Estrutura Operacional",
            "objetivo": "Transformar o modelo em operação",
            "entregaveis": [
                ("Protocolos de retorno pós-exame", ["Eco e Doppler", "Holter e MAPA", "Consulta de acompanhamento"]),
                ("Scripts de comunicação com pacientes via agenda e WhatsApp", []),
                ("Organização das 3 salas / 11 turnos disponíveis", ["Regras de alocação por tipo de atendimento", "Priorização de crônicos e retornos", "Criação de lista de espera ativa"]),
                ("Gestão de capacidade — eliminação da ociosidade", []),
                ("Definição de fluxos independentes da Dra. Daniela", []),
            ],
        },
        {
            "num": "03", "titulo": "Modelo Econômico",
            "objetivo": "Estruturar crescimento sustentável",
            "entregaveis": [
                ("Análise do modelo de receita atual — avulso vs. recorrente", []),
                ("Programas de acompanhamento cardíaco recorrente", ["Contratos de cuidado para crônicos", "Pacotes pós-exame com retorno programado"]),
                ("Estrutura de precificação por complexidade e valor percebido", []),
                ("Simulação de impacto financeiro e estratégia de equilíbrio das dívidas", []),
                ("Estratégia de aumento de ticket e receita sem ampliar captação", []),
            ],
        },
        {
            "num": "04", "titulo": "Arquitetura Tecnológica",
            "objetivo": "Suportar o modelo com eficiência",
            "entregaveis": [
                ("Integração do prontuário eletrônico com agenda e resultados de exames", []),
                ("Plataforma de telemedicina para follow-up cardiológico", []),
                ("Fluxos digitais estruturados", ["Pré-consulta automatizada", "Entrega de resultados de exames", "Follow-up pós-consulta"]),
                ("Padronização de uso das ferramentas pela equipe", []),
                ("Política de segurança da informação — LGPD", []),
            ],
        },
        {
            "num": "05", "titulo": "Gestão por Indicadores",
            "objetivo": "Garantir controle e evolução contínua",
            "entregaveis": [
                ("Definição de KPIs", ["Clínicos: taxa de retorno, adesão, risco cardíaco", "Operacionais: ocupação de salas, cancelamentos, tempo de espera", "Financeiros: receita por paciente, custo por turno de sala"]),
                ("Construção de dashboard gerencial", []),
                ("Rotina de acompanhamento", ["Semanal", "Mensal"]),
                ("Estrutura de tomada de decisão baseada em dados", []),
            ],
        },
    ],
    "criterios_sucesso": [
        "Jornada cardiológica e pós-exame estruturada e operante",
        "Protocolos implementados e utilizados pela equipe",
        "Taxa de retorno de pacientes cardíacos acima de 70% e ocupação das 3 salas acima de 90%",
        "Modelo econômico ativo — programas de acompanhamento precificados e ativos",
        "Indicadores sendo acompanhados em rotina definida",
        "Dashboard funcional com decisões baseadas em dados",
    ],
    "output": "/tmp/anexo_tecnico_imagecor.pdf",
}


# ── HTML generator ─────────────────────────────────────────────────────────────

def build_entregaveis_html(entregaveis):
    rows = []
    for i, (main, subs) in enumerate(entregaveis):
        sep = '<div class="ent-sep"></div>' if i > 0 else ''
        sub_html = ""
        if subs:
            sub_html = "<ul class='sub-list'>" + "".join(f"<li>{s}</li>" for s in subs) + "</ul>"
        rows.append(f"{sep}<div class='ent-item'><span class='diamond'>◆</span><span class='ent-main'>{main}</span>{sub_html}</div>")
    return "\n".join(rows)


def build_modulo_html(m):
    ent_html = build_entregaveis_html(m["entregaveis"])
    return f"""
<div class="modulo-block">
  <div class="modulo-header">
    <div class="modulo-num">{m["num"]}</div>
    <div class="modulo-info">
      <div class="modulo-title">{m["titulo"].upper()}</div>
      <div class="modulo-obj">Objetivo: {m["objetivo"]}</div>
    </div>
  </div>
  <div class="ent-section">
    <div class="ent-label">ENTREGÁVEIS</div>
    <div class="ent-list">
      {ent_html}
    </div>
  </div>
</div>
"""


CRONOGRAMA_ROWS = [
    ("Sem. 1–2",  "DIAGNÓSTICO PROFUNDO",
     ["Entrevistas com equipe e liderança", "Análise da operação atual", "Coleta de dados financeiros e operacionais", "Mapeamento AS-IS"],
     ["Relatório de diagnóstico detalhado", "Principais gaps estruturados"]),
    ("Sem. 3–4",  "ARQUITETURA ASSISTENCIAL",
     ["Desenho da jornada TO-BE", "Definição de serviços assistenciais", "Estruturação do modelo híbrido"],
     ["Jornada completa documentada", "Modelo assistencial definido"]),
    ("Sem. 5–6",  "ESTRUTURA OPERACIONAL",
     ["Criação de protocolos por etapa", "Definição de fluxos internos", "Organização da agenda"],
     ["Protocolos prontos", "Fluxos operacionais definidos"]),
    ("Sem. 7–8",  "MODELO ECONÔMICO",
     ["Definição de programas de acompanhamento", "Estrutura de precificação", "Simulação financeira"],
     ["Modelo de receita estruturado", "Estratégia de monetização"]),
    ("Sem. 9–10", "TECNOLOGIA & INTEGRAÇÃO",
     ["Definição da arquitetura tecnológica", "Estruturação de fluxos digitais", "Alinhamento de ferramentas"],
     ["Arquitetura tecnológica definida", "Fluxos digitais estruturados"]),
    ("Sem. 11–12","INDICADORES & IMPLEMENTAÇÃO",
     ["Definição de KPIs por dimensão", "Construção do dashboard", "Ajuste final do modelo e entrega"],
     ["Dashboard funcional", "Rotina de gestão definida"]),
]


def gerar_html(c):
    modulos_html = "\n".join(build_modulo_html(m) for m in c["modulos"])

    objetivos_html = "\n".join(
        f'<li><strong>{b}</strong></li>' for b in c["objetivos_bullets"]
    )

    cron_rows_html = ""
    for per, fase, ativ, entregas in CRONOGRAMA_ROWS:
        ativ_html  = "".join(f"<div class='cron-item'>— {a}</div>" for a in ativ)
        entre_html = "".join(f"<div class='cron-check'>✔ {e}</div>" for e in entregas)
        cron_rows_html += f"""
<tr>
  <td class="cron-per">{per}</td>
  <td class="cron-fase">{fase}</td>
  <td>{ativ_html}</td>
  <td>{entre_html}</td>
</tr>"""

    criterios_html = "\n".join(
        f'<div class="criterio"><span class="check-icon">✔</span> {cr}</div>'
        for cr in c["criterios_sucesso"]
    )

    return f"""<!DOCTYPE html>
<html lang="pt-BR">
<head>
<meta charset="UTF-8"/>
<style>
  @page {{ size: A4; margin: 0; }}
  * {{ box-sizing: border-box; margin: 0; padding: 0; }}

  body {{
    font-family: 'Helvetica Neue', Arial, sans-serif;
    font-size: 9.5pt;
    color: #1a1a2e;
    background: #fff;
  }}

  /* ── PAGE WRAPPER ── */
  .page {{
    width: 210mm;
    min-height: 297mm;
    padding: 0 0 12mm 0;
    page-break-after: always;
    position: relative;
  }}
  .page:last-child {{ page-break-after: avoid; }}

  /* ── PAGE HEADER (top bar) ── */
  .page-header {{
    display: flex;
    justify-content: space-between;
    align-items: center;
    padding: 6mm 14mm 4mm;
    border-bottom: 1px solid #E2E8F0;
    margin-bottom: 7mm;
  }}
  .page-header-left {{ font-size: 7.5pt; color: #1B3A5C; font-weight: 600; }}
  .page-header-right {{ font-size: 7.5pt; color: #64748B; }}

  /* ── PAGE FOOTER ── */
  .page-footer {{
    position: absolute;
    bottom: 0; left: 0; right: 0;
    border-top: 1px solid #E2E8F0;
    padding: 3mm 14mm;
    display: flex;
    justify-content: space-between;
    font-size: 7pt;
    color: #94A3B8;
  }}

  /* ── CONTENT AREA ── */
  .content {{ padding: 0 14mm; }}

  /* ── TITLE BLOCK (page 1) ── */
  .tag-label {{
    font-size: 7.5pt;
    font-weight: 700;
    color: #0F7173;
    letter-spacing: 1.5px;
    text-transform: uppercase;
    margin-bottom: 4px;
  }}
  .doc-title {{
    font-size: 22pt;
    font-weight: 800;
    color: #1B3A5C;
    line-height: 1.1;
    margin-bottom: 2px;
  }}
  .doc-subtitle {{
    font-size: 10pt;
    color: #64748B;
    font-style: italic;
    margin-bottom: 8mm;
  }}

  /* ── META TABLE ── */
  .meta-table {{
    display: flex;
    border: 1px solid #E2E8F0;
    border-radius: 4px;
    overflow: hidden;
    margin-bottom: 8mm;
  }}
  .meta-cell {{
    flex: 1;
    padding: 8px 14px;
    border-right: 1px solid #E2E8F0;
  }}
  .meta-cell:last-child {{ border-right: none; }}
  .meta-label {{
    font-size: 7pt;
    font-weight: 700;
    color: #64748B;
    text-transform: uppercase;
    letter-spacing: 0.8px;
    margin-bottom: 3px;
  }}
  .meta-value {{ font-size: 10pt; font-weight: 700; color: #1B3A5C; }}

  /* ── SECTION HEADER ── */
  .section-hdr {{
    background: #1B3A5C;
    color: #fff;
    font-size: 8.5pt;
    font-weight: 700;
    letter-spacing: 0.5px;
    padding: 7px 12px;
    margin-bottom: 6mm;
    border-radius: 2px;
  }}

  /* ── OBJETIVO ── */
  .objetivo-block {{
    border-left: 3px solid #0F7173;
    padding: 8px 12px;
    background: #F7F8FA;
    margin-bottom: 8mm;
    border-radius: 0 4px 4px 0;
  }}
  .objetivo-texto {{ font-size: 9.5pt; color: #1a1a2e; line-height: 1.55; margin-bottom: 8px; }}
  .objetivo-block ul {{
    list-style: none;
    padding: 0; margin: 0;
  }}
  .objetivo-block ul li {{
    font-size: 9.5pt;
    color: #1B3A5C;
    padding: 3px 0 3px 16px;
    position: relative;
  }}
  .objetivo-block ul li::before {{
    content: "▸";
    position: absolute;
    left: 0;
    color: #0F7173;
    font-weight: 700;
  }}

  /* ── METODOLOGIA ── */
  .met-intro {{ font-size: 9.5pt; color: #1a1a2e; margin-bottom: 5mm; line-height: 1.5; }}
  .met-flow {{
    display: flex;
    gap: 0;
    margin-bottom: 8mm;
  }}
  .met-box {{
    flex: 1;
    border: 1px solid #E2E8F0;
    border-right: none;
    text-align: center;
    padding: 8px 4px;
  }}
  .met-box:last-child {{ border-right: 1px solid #E2E8F0; }}
  .met-num {{ font-size: 14pt; font-weight: 800; color: #1B3A5C; }}
  .met-name {{ font-size: 7pt; color: #64748B; margin-top: 3px; line-height: 1.3; }}

  /* ── MÓDULO BLOCK ── */
  .modulo-block {{ margin-bottom: 7mm; break-inside: avoid; }}
  .modulo-header {{
    display: flex;
    align-items: flex-start;
    background: #F0F4F8;
    border-left: 5px solid #1B3A5C;
    padding: 8px 12px;
    margin-bottom: 0;
    gap: 12px;
  }}
  .modulo-num {{
    background: #1B3A5C;
    color: #fff;
    font-size: 14pt;
    font-weight: 800;
    min-width: 36px;
    height: 36px;
    display: flex;
    align-items: center;
    justify-content: center;
    border-radius: 3px;
    flex-shrink: 0;
  }}
  .modulo-info {{ padding-top: 2px; }}
  .modulo-title {{ font-size: 10pt; font-weight: 800; color: #1B3A5C; }}
  .modulo-obj {{ font-size: 8.5pt; color: #64748B; font-style: italic; margin-top: 2px; }}

  /* ── ENTREGÁVEIS ── */
  .ent-section {{ border: 1px solid #E2E8F0; border-top: none; }}
  .ent-label {{
    background: #1B3A5C;
    color: #fff;
    font-size: 7.5pt;
    font-weight: 700;
    letter-spacing: 0.5px;
    padding: 5px 12px;
  }}
  .ent-list {{ padding: 4px 0; }}
  .ent-sep {{ height: 1px; background: #E2E8F0; margin: 0 12px; }}
  .ent-item {{ padding: 6px 12px; display: flex; align-items: flex-start; gap: 8px; }}
  .diamond {{ color: #0F7173; font-size: 10pt; flex-shrink: 0; margin-top: 1px; }}
  .ent-main {{ font-size: 9pt; font-weight: 700; color: #1a1a2e; line-height: 1.4; }}
  .sub-list {{
    list-style: none;
    margin: 4px 0 0 0;
    padding: 0;
  }}
  .sub-list li {{
    font-size: 8.5pt;
    color: #64748B;
    padding: 1px 0 1px 14px;
    position: relative;
  }}
  .sub-list li::before {{
    content: "—";
    position: absolute;
    left: 0;
    color: #94A3B8;
  }}

  /* ── CRONOGRAMA ── */
  .cron-table {{
    width: 100%;
    border-collapse: collapse;
    font-size: 8.5pt;
    margin-bottom: 8mm;
  }}
  .cron-table thead tr {{
    background: #1B3A5C;
    color: #fff;
  }}
  .cron-table thead th {{
    padding: 7px 10px;
    text-align: left;
    font-size: 7.5pt;
    font-weight: 700;
    letter-spacing: 0.3px;
  }}
  .cron-table tbody tr {{ border-bottom: 1px solid #E2E8F0; }}
  .cron-table tbody tr:nth-child(even) {{ background: #F7F8FA; }}
  .cron-table td {{ padding: 8px 10px; vertical-align: top; }}
  .cron-per {{ font-weight: 700; color: #1B3A5C; white-space: nowrap; }}
  .cron-fase {{ font-weight: 700; color: #1B3A5C; font-size: 8pt; }}
  .cron-item {{ color: #64748B; padding: 1px 0; font-size: 8pt; }}
  .cron-check {{ color: #1B3A5C; padding: 2px 0; font-size: 8pt; }}
  .cron-check::first-letter {{ color: #0F7173; font-weight: 700; }}

  /* ── CRITÉRIOS ── */
  .criterios-intro {{
    font-size: 9pt;
    color: #64748B;
    font-style: italic;
    margin-bottom: 5mm;
    line-height: 1.5;
    border-left: 3px solid #0F7173;
    padding: 6px 12px;
    background: #F7F8FA;
    border-radius: 0 4px 4px 0;
  }}
  .criterio {{
    font-size: 9.5pt;
    color: #1a1a2e;
    padding: 6px 12px 6px 0;
    border-bottom: 1px solid #E2E8F0;
    display: flex;
    align-items: flex-start;
    gap: 8px;
  }}
  .criterio:last-child {{ border-bottom: none; }}
  .check-icon {{ color: #0F7173; font-weight: 700; flex-shrink: 0; }}

  /* ── NOTA FINAL ── */
  .nota-final {{
    font-size: 8pt;
    color: #64748B;
    font-style: italic;
    line-height: 1.6;
    margin-top: 7mm;
    padding-top: 5mm;
    border-top: 1px solid #E2E8F0;
  }}

  /* ── ASSINATURA ── */
  .assinatura-block {{
    display: flex;
    gap: 20mm;
    margin-top: 10mm;
    padding-top: 8mm;
    border-top: 2px solid #1B3A5C;
  }}
  .assinatura-pessoa {{ flex: 1; }}
  .assin-line {{
    height: 1px;
    background: #1B3A5C;
    margin-bottom: 6px;
    width: 80%;
  }}
  .assin-nome {{ font-size: 10pt; font-weight: 800; color: #1B3A5C; margin-bottom: 2px; }}
  .assin-cargo {{ font-size: 8.5pt; color: #0F7173; font-weight: 600; margin-bottom: 2px; }}
  .assin-empresa {{ font-size: 8pt; color: #64748B; }}
  .assin-email {{ font-size: 7.5pt; color: #94A3B8; margin-top: 3px; }}

  /* ── DOC FOOTER LINE ── */
  .doc-footer-line {{
    text-align: center;
    margin-top: 9mm;
    font-size: 8pt;
    color: #64748B;
    padding-top: 5mm;
    border-top: 1px solid #E2E8F0;
  }}
</style>
</head>
<body>

<!-- ══════════════════════════════════════════════════════════════
     PÁGINA 1: Capa, Objetivo, Metodologia, Módulo 01
════════════════════════════════════════════════════════════════ -->
<div class="page">
  <div class="page-header">
    <div class="page-header-left">FLETIC VISION · Estrutura do Projeto {c["clinica"]} · Confidencial</div>
    <div class="page-header-right">{c["clinica"]} · Confidencial</div>
  </div>

  <div class="content">

    <!-- Title block -->
    <div class="tag-label">ANEXO TÉCNICO</div>
    <div class="doc-title">Estrutura do Projeto</div>
    <div class="doc-subtitle">Fletic Vision · {c["clinica"]}</div>

    <!-- Meta -->
    <div class="meta-table">
      <div class="meta-cell">
        <div class="meta-label">Cliente</div>
        <div class="meta-value">{c["clinica"]}</div>
      </div>
      <div class="meta-cell">
        <div class="meta-label">Duração</div>
        <div class="meta-value">12 semanas</div>
      </div>
      <div class="meta-cell">
        <div class="meta-label">Modalidade</div>
        <div class="meta-value">Consultoria estruturada</div>
      </div>
      <div class="meta-cell">
        <div class="meta-label">Especialidade</div>
        <div class="meta-value">{c["especialidade"]}</div>
      </div>
    </div>

    <!-- Objetivo -->
    <div class="section-hdr">OBJETIVO DO PROJETO</div>
    <div class="objetivo-block" style="margin-bottom:8mm;">
      <div class="objetivo-texto">{c["objetivo"]}</div>
      <ul>{objetivos_html}</ul>
    </div>

    <!-- Metodologia -->
    <div class="section-hdr">METODOLOGIA</div>
    <div class="met-intro">
      O projeto é conduzido em 5 módulos sequenciais e integrados.
      Cada módulo possui entregáveis definidos, validados com a clínica ao final de cada etapa.
    </div>
    <div class="met-flow">
      <div class="met-box"><div class="met-num">01</div><div class="met-name">Arquitetura<br>Assistencial</div></div>
      <div class="met-box"><div class="met-num">02</div><div class="met-name">Estrutura<br>Operacional</div></div>
      <div class="met-box"><div class="met-num">03</div><div class="met-name">Modelo<br>Econômico</div></div>
      <div class="met-box"><div class="met-num">04</div><div class="met-name">Arquitetura<br>Tecnológica</div></div>
      <div class="met-box"><div class="met-num">05</div><div class="met-name">Gestão por<br>Indicadores</div></div>
    </div>

    <!-- Escopo header -->
    <div class="section-hdr">ESCOPO DETALHADO</div>

    <!-- Módulo 01 -->
    {build_modulo_html(c["modulos"][0])}

  </div>

  <div class="page-footer">
    <span>Framework Fletic — Versão 1.0 · fletic.com.br</span>
    <span>Página 1 de 4</span>
  </div>
</div>

<!-- ══════════════════════════════════════════════════════════════
     PÁGINA 2: Módulos 02, 03 e 04
════════════════════════════════════════════════════════════════ -->
<div class="page">
  <div class="page-header">
    <div class="page-header-left">FLETIC VISION · Estrutura do Projeto {c["clinica"]} · Confidencial</div>
    <div class="page-header-right">{c["clinica"]} · Confidencial</div>
  </div>

  <div class="content">
    {build_modulo_html(c["modulos"][1])}
    {build_modulo_html(c["modulos"][2])}
    {build_modulo_html(c["modulos"][3])}
  </div>

  <div class="page-footer">
    <span>Framework Fletic — Versão 1.0 · fletic.com.br</span>
    <span>Página 2 de 4</span>
  </div>
</div>

<!-- ══════════════════════════════════════════════════════════════
     PÁGINA 3: Módulo 05
════════════════════════════════════════════════════════════════ -->
<div class="page">
  <div class="page-header">
    <div class="page-header-left">FLETIC VISION · Estrutura do Projeto {c["clinica"]} · Confidencial</div>
    <div class="page-header-right">{c["clinica"]} · Confidencial</div>
  </div>

  <div class="content">
    {build_modulo_html(c["modulos"][4])}
  </div>

  <div class="page-footer">
    <span>Framework Fletic — Versão 1.0 · fletic.com.br</span>
    <span>Página 3 de 4</span>
  </div>
</div>

<!-- ══════════════════════════════════════════════════════════════
     PÁGINA 4: Cronograma, Critérios de Sucesso, Assinaturas
════════════════════════════════════════════════════════════════ -->
<div class="page">
  <div class="page-header">
    <div class="page-header-left">FLETIC VISION · Estrutura do Projeto {c["clinica"]} · Confidencial</div>
    <div class="page-header-right">{c["clinica"]} · Confidencial</div>
  </div>

  <div class="content">

    <!-- Cronograma -->
    <div class="section-hdr">CRONOGRAMA — SEMANA A SEMANA</div>
    <table class="cron-table">
      <thead>
        <tr>
          <th>PERÍODO</th>
          <th>FASE</th>
          <th>ATIVIDADES</th>
          <th>ENTREGAS</th>
        </tr>
      </thead>
      <tbody>{cron_rows_html}</tbody>
    </table>

    <!-- Critérios -->
    <div class="section-hdr">CRITÉRIOS DE SUCESSO</div>
    <div class="criterios-intro">
      O projeto será considerado bem-sucedido quando todos os critérios abaixo estiverem operantes:
    </div>
    <div style="margin-bottom:8mm;">
      {criterios_html}
    </div>

    <!-- Nota final -->
    <div class="nota-final">
      Este documento é parte integrante da proposta Fletic Vision e tem caráter técnico-operacional.
      As informações aqui descritas refletem o escopo padrão do projeto, podendo ser ajustadas em função
      do diagnóstico inicial da clínica e das prioridades identificadas na reunião de alinhamento.
    </div>

    <!-- Assinaturas -->
    <div class="assinatura-block">
      <div class="assinatura-pessoa">
        <div class="assin-line"></div>
        <div class="assin-nome">Danielle Magalhães</div>
        <div class="assin-cargo">CEO · Co-Fundadora</div>
        <div class="assin-empresa">Fletic Saúde Digital</div>
        <div class="assin-email">dani.magalhaes@fletic.com.br</div>
      </div>
      <div class="assinatura-pessoa">
        <div class="assin-line"></div>
        <div class="assin-nome">Simone Farah</div>
        <div class="assin-cargo">CMO · Fundadora</div>
        <div class="assin-empresa">Fletic Saúde Digital</div>
        <div class="assin-email">simone.farah@fletic.com.br</div>
      </div>
    </div>

    <!-- Doc footer line -->
    <div class="doc-footer-line">
      Fletic Vision · fletic.com.br · Versão 1.0 · {c["mes_ano"]}
    </div>

  </div>

  <div class="page-footer">
    <span>Framework Fletic — Versão 1.0 · fletic.com.br</span>
    <span>Página 4 de 4</span>
  </div>
</div>

</body>
</html>"""


async def gerar_pdf(c):
    html = gerar_html(c)
    html_path = c["output"].replace(".pdf", ".html")
    with open(html_path, "w", encoding="utf-8") as f:
        f.write(html)
    async with async_playwright() as p:
        browser = await p.chromium.launch(
            executable_path="/opt/pw-browsers/chromium-1194/chrome-linux/chrome"
        )
        page = await browser.new_page()
        await page.goto(f"file://{html_path}", wait_until="networkidle")
        await page.pdf(
            path=c["output"],
            format="A4",
            print_background=True,
            margin={"top": "0", "right": "0", "bottom": "0", "left": "0"},
        )
        await browser.close()
    print(f"Anexo Técnico gerado: {c['output']}")


async def main():
    await gerar_pdf(ANA_PAULA)
    await gerar_pdf(ETHEL)
    await gerar_pdf(DANIELA_BORGES)

if __name__ == "__main__":
    asyncio.run(main())
