#!/usr/bin/env python3
"""
Fletic Vision — Anexo Técnico (Estrutura do Projeto)
Layout: Medicina Vaccaro reference. 4 pages A4.
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
                ("Scripts operacionais da equipe", []),
                ("Fluxos internos por função", ["Recepção", "Médico"]),
                ("Organização da agenda", ["Blocos presenciais", "Blocos digitais", "Blocos de retorno programado"]),
                ("Definição de responsabilidades por função", []),
            ],
        },
        {
            "num": "03", "titulo": "Modelo Econômico",
            "objetivo": "Estruturar crescimento sustentável",
            "entregaveis": [
                ("Análise do modelo de receita atual — avulso vs. recorrente", []),
                ("Definição de novos produtos e programas", ["Programas de acompanhamento cardíaco longitudinal", "Contratos de cuidado recorrente"]),
                ("Estrutura de precificação", ["Ticket por serviço", "Ticket por programa"]),
                ("Simulação de impacto financeiro e projeção de receita recorrente", []),
                ("Estratégia de aumento de ticket médio e LTV por paciente", []),
            ],
        },
        {
            "num": "04", "titulo": "Arquitetura Tecnológica",
            "objetivo": "Suportar o modelo com eficiência",
            "entregaveis": [
                ("Definição da arquitetura tecnológica", ["Prontuário eletrônico", "Plataforma de telemedicina", "Comunicação (WhatsApp / automatizado)"]),
                ("Desenho de fluxos digitais", ["Pré-consulta automatizada", "Follow-up pós-consulta"]),
                ("Definição de integrações necessárias", []),
                ("Padronização de uso das ferramentas", []),
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
        "Modelo econômico ativo — serviços e programas precificados e ofertados",
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
                ("Scripts operacionais da equipe", []),
                ("Fluxos internos por função", ["Recepção", "Médico"]),
                ("Organização da agenda", ["Blocos presenciais", "Blocos digitais", "Blocos de retorno programado"]),
                ("Definição de responsabilidades por função", []),
            ],
        },
        {
            "num": "03", "titulo": "Modelo Econômico",
            "objetivo": "Estruturar crescimento sustentável",
            "entregaveis": [
                ("Análise do modelo de receita atual — avulso vs. recorrente", []),
                ("Definição de novos produtos e programas", ["Programas de acompanhamento nutrológico mensal", "Pacotes pós-endoscopia", "Programas de longevidade e performance"]),
                ("Estrutura de precificação", ["Ticket por serviço", "Ticket por programa"]),
                ("Simulação de impacto financeiro e projeção de receita recorrente", []),
                ("Estratégia de aumento de ticket médio por paciente", []),
            ],
        },
        {
            "num": "04", "titulo": "Arquitetura Tecnológica",
            "objetivo": "Suportar o modelo com eficiência",
            "entregaveis": [
                ("Definição da arquitetura tecnológica", ["Prontuário eletrônico", "Plataforma de telemedicina para nutrologia", "Comunicação (WhatsApp / automatizado)"]),
                ("Desenho de fluxos digitais", ["Pré-consulta automatizada", "Follow-up pós-consulta e pós-procedimento"]),
                ("Definição de integrações necessárias", []),
                ("Padronização de uso das ferramentas", []),
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
                ("Segmentação da carteira de pacientes", ["Crônicos cardíacos", "Pacientes pós-procedimento", "Novos encaminhamentos"]),
                ("Estruturação dos serviços por tipo e frequência de retorno esperada", []),
                ("Critérios de elegibilidade para telemedicina vs. presencial", []),
            ],
        },
        {
            "num": "02", "titulo": "Estrutura Operacional",
            "objetivo": "Transformar o modelo em operação",
            "entregaveis": [
                ("Protocolos de retorno pós-exame", ["Eco e Doppler", "Holter e MAPA", "Consulta de acompanhamento"]),
                ("Scripts de comunicação com pacientes", []),
                ("Organização das 3 salas / 11 turnos disponíveis", ["Regras de alocação por tipo de atendimento", "Priorização de crônicos e retornos", "Lista de espera ativa"]),
                ("Gestão de capacidade — eliminação da ociosidade", []),
                ("Definição de fluxos operacionais independentes da Dra. Daniela", []),
            ],
        },
        {
            "num": "03", "titulo": "Modelo Econômico",
            "objetivo": "Estruturar crescimento sustentável",
            "entregaveis": [
                ("Análise do modelo de receita atual — avulso vs. recorrente", []),
                ("Definição de programas de acompanhamento cardíaco recorrente", ["Contratos de cuidado para crônicos", "Pacotes pós-exame com retorno programado"]),
                ("Estrutura de precificação", ["Ticket por serviço", "Ticket por programa"]),
                ("Simulação de impacto financeiro e estratégia de equilíbrio das dívidas", []),
                ("Estratégia de aumento de ticket e receita sem ampliar captação", []),
            ],
        },
        {
            "num": "04", "titulo": "Arquitetura Tecnológica",
            "objetivo": "Suportar o modelo com eficiência",
            "entregaveis": [
                ("Definição da arquitetura tecnológica", ["Prontuário eletrônico e resultados de exames", "Plataforma de telemedicina cardiológica", "Comunicação (WhatsApp / automatizado)"]),
                ("Desenho de fluxos digitais", ["Pré-consulta automatizada", "Entrega de resultados de exames", "Follow-up pós-consulta"]),
                ("Definição de integrações necessárias", []),
                ("Padronização de uso das ferramentas", []),
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
        "Taxa de retorno de pacientes acima de 70% e ocupação das 3 salas acima de 90%",
        "Modelo econômico ativo — programas de acompanhamento precificados e ativos",
        "Indicadores sendo acompanhados em rotina definida",
        "Dashboard funcional com decisões baseadas em dados",
    ],
    "output": "/tmp/anexo_tecnico_imagecor.pdf",
}


# ── HTML builder helpers ───────────────────────────────────────────────────────

def ent_html(entregaveis):
    parts = []
    for i, (main, subs) in enumerate(entregaveis):
        sep = '<div class="sep"></div>' if i > 0 else ''
        sub_block = ""
        if subs:
            items = "".join(f"<li>{s}</li>" for s in subs)
            sub_block = f"<ul class='sub'>{items}</ul>"
        parts.append(f"{sep}<div class='ei'><span class='di'>◆</span><span class='et'>{main}</span>{sub_block}</div>")
    return "\n".join(parts)


def mod_html(m):
    return f"""<div class="mod">
  <div class="mh">
    <div class="mn">{m["num"]}</div>
    <div class="mi">
      <div class="mt">{m["titulo"].upper()}</div>
      <div class="mo">Objetivo: {m["objetivo"]}</div>
    </div>
  </div>
  <div class="es">
    <div class="el">ENTREGÁVEIS</div>
    <div class="eb">{ent_html(m["entregaveis"])}</div>
  </div>
</div>"""


CRON = [
    ("Sem. 1–2",  "DIAGNÓSTICO PROFUNDO",
     ["Entrevistas com equipe e liderança", "Análise da operação atual",
      "Coleta de dados financeiros e operacionais", "Mapeamento AS-IS"],
     ["Relatório de diagnóstico detalhado", "Principais gaps estruturados"]),
    ("Sem. 3–4",  "ARQUITETURA ASSISTENCIAL",
     ["Desenho da jornada TO-BE", "Definição de serviços assistenciais",
      "Estruturação do modelo híbrido"],
     ["Jornada completa documentada", "Modelo assistencial definido"]),
    ("Sem. 5–6",  "ESTRUTURA OPERACIONAL",
     ["Criação de protocolos por etapa", "Definição de fluxos internos",
      "Organização da agenda"],
     ["Protocolos prontos", "Fluxos operacionais definidos"]),
    ("Sem. 7–8",  "MODELO ECONÔMICO",
     ["Definição de programas de acompanhamento", "Estrutura de precificação",
      "Simulação financeira"],
     ["Modelo de receita estruturado", "Estratégia de monetização"]),
    ("Sem. 9–10", "TECNOLOGIA & INTEGRAÇÃO",
     ["Definição da arquitetura tecnológica", "Estruturação de fluxos digitais",
      "Alinhamento de ferramentas"],
     ["Arquitetura tecnológica definida", "Fluxos digitais estruturados"]),
    ("Sem. 11–12","INDICADORES & IMPLEMENTAÇÃO",
     ["Definição de KPIs por dimensão", "Construção do dashboard",
      "Ajuste final do modelo e entrega"],
     ["Dashboard funcional", "Rotina de gestão definida"]),
]


# ── Main HTML ──────────────────────────────────────────────────────────────────

def gerar_html(c):
    obj_bullets = "\n".join(f"<li><strong>{b}</strong></li>" for b in c["objetivos_bullets"])

    cron_rows = ""
    for per, fase, ativ, entregas in CRON:
        av = "".join(f"<div class='ca'>— {a}</div>" for a in ativ)
        ev = "".join(f"<div class='ce'>✔ {e}</div>" for e in entregas)
        cron_rows += f"<tr><td class='cp'>{per}</td><td class='cf'>{fase}</td><td>{av}</td><td>{ev}</td></tr>"

    crit_html = "\n".join(
        f'<div class="cr"><span class="ck">✔</span> {x}</div>'
        for x in c["criterios_sucesso"]
    )

    ph_left  = f"FLETIC VISION · Estrutura do Projeto {c['clinica']} · Confidencial"
    ph_right = f"{c['clinica']} · Confidencial"

    def ph(pg):
        return f"""<div class="ph">
      <span class="phl">{ph_left}</span>
      <span class="phr">{ph_right}</span>
    </div>"""

    def pf(n, total=4):
        return f"""<div class="pf">
      <span>Framework Fletic — Versão 1.0 · fletic.com.br</span>
      <span>Página {n} de {total}</span>
    </div>"""

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
  color: #2d3748;
  background: #fff;
  -webkit-print-color-adjust: exact;
}}

/* PAGE */
.page {{
  width: 210mm;
  min-height: 297mm;
  padding-bottom: 14mm;
  page-break-after: always;
  position: relative;
  display: flex;
  flex-direction: column;
}}
.page:last-child {{ page-break-after: avoid; }}

/* PAGE HEADER */
.ph {{
  display: flex;
  justify-content: space-between;
  padding: 5mm 15mm 3.5mm;
  border-bottom: 1px solid #cbd5e0;
  margin-bottom: 7mm;
  flex-shrink: 0;
}}
.phl {{ font-size: 7pt; font-weight: 600; color: #2d3748; }}
.phr {{ font-size: 7pt; color: #718096; }}

/* CONTENT */
.ct {{ flex: 1; padding: 0 15mm; }}

/* PAGE FOOTER */
.pf {{
  position: absolute;
  bottom: 0; left: 0; right: 0;
  border-top: 1px solid #cbd5e0;
  padding: 2.5mm 15mm;
  display: flex;
  justify-content: space-between;
  font-size: 7pt;
  color: #a0aec0;
}}

/* ── TITLE BLOCK ── */
.tag {{ font-size: 7.5pt; font-weight: 700; color: #0F7173; letter-spacing: 1.5px; text-transform: uppercase; margin-bottom: 5px; }}
.title {{ font-size: 24pt; font-weight: 800; color: #1B3A5C; line-height: 1.1; margin-bottom: 3px; }}
.sub {{ font-size: 10.5pt; color: #718096; font-style: italic; margin-bottom: 7mm; }}

/* ── META TABLE ── */
.meta {{
  display: flex;
  border: 1px solid #e2e8f0;
  margin-bottom: 8mm;
}}
.mc {{ flex: 1; padding: 9px 14px; border-right: 1px solid #e2e8f0; }}
.mc:last-child {{ border-right: none; }}
.ml {{ font-size: 6.5pt; font-weight: 700; color: #718096; text-transform: uppercase; letter-spacing: 0.8px; margin-bottom: 4px; }}
.mv {{ font-size: 10pt; font-weight: 700; color: #1B3A5C; }}

/* ── SECTION HEADER ── */
.sh {{
  background: #1B3A5C;
  color: #fff;
  font-size: 8pt;
  font-weight: 700;
  letter-spacing: 0.8px;
  padding: 7px 12px;
  margin-bottom: 5mm;
}}

/* ── OBJETIVO ── */
.obj {{
  border-left: 3px solid #0F7173;
  background: #f7fafc;
  padding: 10px 14px;
  margin-bottom: 8mm;
  border-radius: 0 3px 3px 0;
}}
.obj p {{ font-size: 9.5pt; color: #2d3748; line-height: 1.6; margin-bottom: 8px; }}
.obj ul {{ list-style: none; padding: 0; }}
.obj ul li {{
  font-size: 9.5pt; color: #1B3A5C;
  padding: 3px 0 3px 18px;
  position: relative; line-height: 1.5;
}}
.obj ul li::before {{ content: "▸"; position: absolute; left: 0; color: #0F7173; font-weight: 700; }}

/* ── METODOLOGIA ── */
.met-p {{ font-size: 9.5pt; color: #2d3748; line-height: 1.6; margin-bottom: 5mm; }}
.mf {{ display: flex; margin-bottom: 8mm; border: 1px solid #e2e8f0; }}
.mb {{ flex: 1; text-align: center; padding: 9px 6px; border-right: 1px solid #e2e8f0; }}
.mb:last-child {{ border-right: none; }}
.mbn {{ font-size: 15pt; font-weight: 800; color: #1B3A5C; }}
.mbt {{ font-size: 7pt; color: #718096; margin-top: 3px; line-height: 1.35; }}

/* ── MODULE ── */
.mod {{ margin-bottom: 7mm; }}
.mh {{
  display: flex; align-items: center; gap: 12px;
  background: #edf2f7;
  padding: 9px 12px;
  border-left: none;
}}
.mn {{
  background: #0F7173;
  color: #fff;
  font-size: 15pt; font-weight: 800;
  min-width: 40px; height: 40px;
  display: flex; align-items: center; justify-content: center;
  flex-shrink: 0;
}}
.mi {{ }}
.mt {{ font-size: 10pt; font-weight: 800; color: #1B3A5C; }}
.mo {{ font-size: 8.5pt; color: #718096; font-style: italic; margin-top: 2px; }}

/* ENTREGAVEIS */
.es {{ border: 1px solid #e2e8f0; border-top: none; }}
.el {{ background: #1B3A5C; color: #fff; font-size: 7.5pt; font-weight: 700; letter-spacing: 0.5px; padding: 5px 12px; }}
.eb {{ padding: 2px 0; }}
.sep {{ height: 1px; background: #e2e8f0; margin: 0 12px; }}
.ei {{ padding: 7px 12px; display: flex; align-items: flex-start; gap: 9px; }}
.di {{ color: #0F7173; font-size: 10pt; flex-shrink: 0; margin-top: 1px; }}
.et {{ font-size: 9pt; font-weight: 700; color: #2d3748; line-height: 1.45; }}
.sub {{ list-style: none; margin: 5px 0 0 0; padding: 0; }}
.sub li {{ font-size: 8.5pt; color: #718096; padding: 2px 0 2px 16px; position: relative; line-height: 1.4; }}
.sub li::before {{ content: "—"; position: absolute; left: 0; color: #a0aec0; }}

/* ── CRONOGRAMA ── */
.ct-table {{ width: 100%; border-collapse: collapse; font-size: 8.5pt; margin-bottom: 8mm; }}
.ct-table thead tr {{ background: #1B3A5C; color: #fff; }}
.ct-table thead th {{ padding: 7px 10px; text-align: left; font-size: 7.5pt; font-weight: 700; letter-spacing: 0.3px; }}
.ct-table tbody tr {{ border-bottom: 1px solid #e2e8f0; }}
.ct-table tbody tr:nth-child(even) {{ background: #f7fafc; }}
.ct-table td {{ padding: 8px 10px; vertical-align: top; }}
.cp {{ font-weight: 700; color: #1B3A5C; white-space: nowrap; font-size: 8.5pt; }}
.cf {{ font-weight: 700; color: #1B3A5C; font-size: 8pt; }}
.ca {{ color: #718096; padding: 1.5px 0; font-size: 8pt; }}
.ce {{ color: #2d3748; padding: 2px 0; font-size: 8pt; }}

/* ── CRITÉRIOS ── */
.cri {{ font-size: 9pt; color: #718096; font-style: italic; line-height: 1.6;
       border-left: 3px solid #0F7173; background: #f7fafc;
       padding: 7px 12px; margin-bottom: 5mm; border-radius: 0 3px 3px 0; }}
.cr {{ font-size: 9.5pt; color: #2d3748; padding: 7px 0; border-bottom: 1px solid #e2e8f0;
      display: flex; align-items: flex-start; gap: 9px; }}
.cr:last-child {{ border-bottom: none; }}
.ck {{ color: #0F7173; font-weight: 700; flex-shrink: 0; }}

/* ── NOTA ── */
.nota {{
  font-size: 8pt; color: #718096; font-style: italic; line-height: 1.65;
  margin-top: 6mm; padding-top: 5mm; border-top: 1px solid #e2e8f0;
}}

/* ── ASSINATURAS ── */
.assin {{
  display: flex; gap: 24mm;
  margin-top: 9mm; padding-top: 7mm;
  border-top: 2px solid #1B3A5C;
}}
.ap {{ flex: 1; }}
.al {{ height: 1px; background: #1B3A5C; width: 75%; margin-bottom: 7px; }}
.an {{ font-size: 10pt; font-weight: 800; color: #1B3A5C; margin-bottom: 2px; }}
.ac {{ font-size: 8.5pt; color: #0F7173; font-weight: 600; margin-bottom: 2px; }}
.ae {{ font-size: 8pt; color: #718096; }}
.aemail {{ font-size: 7.5pt; color: #a0aec0; margin-top: 3px; }}

/* ── DOC CLOSING ── */
.dc {{ text-align: center; margin-top: 8mm; font-size: 8pt; color: #718096; padding-top: 5mm; border-top: 1px solid #e2e8f0; }}
</style>
</head>
<body>

<!-- ═══════════ PAGE 1: título · objetivo · metodologia · M01 ═══════════ -->
<div class="page">
  {ph(1)}
  <div class="ct">
    <div class="tag">ANEXO TÉCNICO</div>
    <div class="title">Estrutura do Projeto</div>
    <div class="sub">Fletic Vision · {c["clinica"]}</div>

    <div class="meta">
      <div class="mc"><div class="ml">Cliente</div><div class="mv">{c["clinica"]}</div></div>
      <div class="mc"><div class="ml">Duração</div><div class="mv">12 semanas</div></div>
      <div class="mc"><div class="ml">Modalidade</div><div class="mv">Consultoria estruturada</div></div>
    </div>

    <div class="sh">OBJETIVO DO PROJETO</div>
    <div class="obj">
      <p>{c["objetivo"]}</p>
      <ul>{obj_bullets}</ul>
    </div>

    <div class="sh">METODOLOGIA</div>
    <div class="met-p">
      O projeto é conduzido em 5 módulos sequenciais e integrados.
      Cada módulo possui entregáveis definidos, validados com a clínica ao final de cada etapa.
    </div>
    <div class="mf">
      <div class="mb"><div class="mbn">01</div><div class="mbt">Arquitetura<br>Assistencial</div></div>
      <div class="mb"><div class="mbn">02</div><div class="mbt">Estrutura<br>Operacional</div></div>
      <div class="mb"><div class="mbn">03</div><div class="mbt">Modelo<br>Econômico</div></div>
      <div class="mb"><div class="mbn">04</div><div class="mbt">Arquitetura<br>Tecnológica</div></div>
      <div class="mb"><div class="mbn">05</div><div class="mbt">Gestão por<br>Indicadores</div></div>
    </div>

    <div class="sh">ESCOPO DETALHADO</div>
    {mod_html(c["modulos"][0])}
  </div>
  {pf(1)}
</div>

<!-- ═══════════ PAGE 2: M02 · M03 ═══════════ -->
<div class="page">
  {ph(2)}
  <div class="ct">
    {mod_html(c["modulos"][1])}
    {mod_html(c["modulos"][2])}
  </div>
  {pf(2)}
</div>

<!-- ═══════════ PAGE 3: M04 · M05 ═══════════ -->
<div class="page">
  {ph(3)}
  <div class="ct">
    {mod_html(c["modulos"][3])}
    {mod_html(c["modulos"][4])}
  </div>
  {pf(3)}
</div>

<!-- ═══════════ PAGE 4: cronograma · critérios · assinaturas ═══════════ -->
<div class="page">
  {ph(4)}
  <div class="ct">
    <div class="sh">CRONOGRAMA — SEMANA A SEMANA</div>
    <table class="ct-table">
      <thead><tr><th>PERÍODO</th><th>FASE</th><th>ATIVIDADES</th><th>ENTREGAS</th></tr></thead>
      <tbody>{cron_rows}</tbody>
    </table>

    <div class="sh">CRITÉRIOS DE SUCESSO</div>
    <div class="cri">O projeto será considerado bem-sucedido quando todos os critérios abaixo estiverem operantes:</div>
    <div style="margin-bottom:7mm">{crit_html}</div>

    <div class="nota">
      Este documento é parte integrante da proposta Fletic Vision e tem caráter técnico-operacional.
      As informações aqui descritas refletem o escopo padrão do projeto, podendo ser ajustadas em função
      do diagnóstico inicial da clínica e das prioridades identificadas na reunião de alinhamento.
    </div>

    <div class="assin">
      <div class="ap">
        <div class="al"></div>
        <div class="an">Danielle Magalhães</div>
        <div class="ac">CEO · Co-Fundadora</div>
        <div class="ae">Fletic Saúde Digital</div>
        <div class="aemail">dani.magalhaes@fletic.com.br</div>
      </div>
      <div class="ap">
        <div class="al"></div>
        <div class="an">Simone Farah</div>
        <div class="ac">CMO · Fundadora</div>
        <div class="ae">Fletic Saúde Digital</div>
        <div class="aemail">simone.farah@fletic.com.br</div>
      </div>
    </div>

    <div class="dc">Fletic Vision · fletic.com.br · Versão 1.0 · {c["mes_ano"]}</div>
  </div>
  {pf(4)}
</div>

</body>
</html>"""


async def gerar_pdf(c):
    html = gerar_html(c)
    hp = c["output"].replace(".pdf", ".html")
    with open(hp, "w", encoding="utf-8") as f:
        f.write(html)
    async with async_playwright() as p:
        browser = await p.chromium.launch(
            executable_path="/opt/pw-browsers/chromium-1194/chrome-linux/chrome"
        )
        page = await browser.new_page()
        await page.goto(f"file://{hp}", wait_until="networkidle")
        await page.pdf(
            path=c["output"], format="A4", print_background=True,
            margin={"top": "0", "right": "0", "bottom": "0", "left": "0"},
        )
        await browser.close()
    print(f"Gerado: {c['output']}")


async def main():
    await gerar_pdf(ANA_PAULA)
    await gerar_pdf(ETHEL)
    await gerar_pdf(DANIELA_BORGES)

if __name__ == "__main__":
    asyncio.run(main())
