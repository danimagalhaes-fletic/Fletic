#!/usr/bin/env python3
"""
Fletic Vision — Master parametric diagnostic report generator.
Cover: Ethel style (dark bg, circular deco, cover-info-items, score hero)
Internal pages: Ana Paula style (numbered sections, linear scale bar, pilar cards with critico/baixo, criteria table with score-avg, narrative with alerta-box + gap-list)
"""

import asyncio
from playwright.async_api import async_playwright

# ─── CLIENT DATA STRUCTURES ───────────────────────────────────────────────────

ANA_PAULA = {
    "nome": "Ana Paula Rodrigues",
    "clinica": "APR LTDA",
    "especialidade": "Cardiologia & Cuidados Paliativos",
    "cidade": "Rio de Janeiro – RJ",
    "faturamento_mensal": "até R$ 30.000",
    "mes_ano": "Junho 2026",
    "score_final": 0.76,
    "nivel": "Inicial",
    "nivel_desc": "Operação artesanal, sem estrutura digital relevante",
    "pilares": [
        {
            "num": "01", "nome": "Estratégia & Modelo Assistencial", "peso": "25%",
            "score": 0.67, "classe": "critico",
            "criterios": [
                ("Modelo assistencial híbrido definido", 0, "Só presencial, sem plano digital"),
                ("Segmentação de pacientes por perfil/risco", 1, "Sem segmentação formal"),
                ("Protocolos clínicos digitais estruturados", 1, "Tudo informal"),
                ("Integração entre digital e presencial", 0, "Operam isolados"),
                ("Governança clínica do digital", 0, "Inexistente"),
                ("Alinhamento estratégico institucional", 2, "Objetivo existe mas não operacionalizado"),
            ],
            "desc": "A clínica opera exclusivamente no modelo presencial, sem planejamento para integração digital. Ausência de protocolos formais e governança clínica compromete a escalabilidade."
        },
        {
            "num": "02", "nome": "Operação & Jornada", "peso": "20%",
            "score": 1.00, "classe": "critico",
            "criterios": [
                ("Fluxo de entrada digital estruturado", 1, "Agenda digital básica"),
                ("Integração da agenda (presencial + digital)", 1, "Mesma ferramenta, sem regras"),
                ("Programas de acompanhamento estruturados", 0, "Nenhum programa ativo"),
                ("Comunicação com paciente padronizada", 2, "Scripts informais via WhatsApp"),
                ("Experiência do paciente monitorada", 1, "Feedback informal ocasional"),
                ("Gestão de capacidade e demanda", 1, "Percebido mas não gerenciado"),
            ],
            "desc": "Operação reativa, com agendamento digital básico mas sem programas de acompanhamento. Comunicação não rastreável via WhatsApp."
        },
        {
            "num": "03", "nome": "Tecnologia & Integração", "peso": "15%",
            "score": 1.00, "classe": "critico",
            "criterios": [
                ("Prontuário eletrônico estruturado", 2, "Sistema básico subutilizado"),
                ("Integração entre sistemas", 1, "Integração manual/parcial"),
                ("Plataforma de telemedicina adequada", 0, "Ligação/WhatsApp informal"),
                ("Interoperabilidade de dados", 1, "Exportação manual possível"),
                ("Segurança da informação (LGPD)", 1, "Política básica não auditada"),
                ("Infraestrutura tecnológica", 1, "Funcional mas frágil"),
            ],
            "desc": "Stack tecnológico fragmentado. Prontuário subutilizado, sem telemedicina estruturada e dados presos em silos."
        },
        {
            "num": "04", "nome": "Dados & Inteligência", "peso": "20%",
            "score": 0.33, "classe": "critico",
            "criterios": [
                ("Coleta estruturada de dados", 1, "Coleta parcial e manual"),
                ("Indicadores clínicos definidos", 0, "Nenhum indicador formal"),
                ("Indicadores operacionais definidos", 1, "Visibilidade parcial"),
                ("Uso de dados na decisão", 0, "Decisão por percepção"),
                ("Dashboards gerenciais", 0, "Inexistente"),
                ("Analytics / predição", 0, "Nenhum uso preditivo"),
            ],
            "desc": "Gestão 100% por percepção. Sem indicadores clínicos ou operacionais formais. Decisões tomadas sem base em dados."
        },
        {
            "num": "05", "nome": "Modelo Econômico & Sustentabilidade", "peso": "20%",
            "score": 0.83, "classe": "critico",
            "criterios": [
                ("Precificação estruturada", 2, "Tabela existe mas não seguida"),
                ("Modelo de receita definido", 1, "Mix com pouca recorrência"),
                ("Previsibilidade financeira", 0, "Receita imprevisível"),
                ("ROI do digital medido", 0, "Nunca medido"),
                ("Alinhamento de incentivos", 1, "Parcialmente alinhados"),
                ("Controle de custos assistenciais", 1, "Controle financeiro geral"),
            ],
            "desc": "Modelo 100% transacional por consulta avulsa. Sem previsibilidade financeira ou mensuração do ROI digital."
        },
    ],
    "narrativa_paragrafos": [
        "A APR LTDA apresenta score de maturidade <strong>0,76 — nível Inicial</strong>, refletindo uma operação ainda artesanal e centrada exclusivamente no modelo presencial. A ausência de estrutura digital relevante limita o potencial de crescimento e expõe a clínica a riscos operacionais e financeiros significativos.",
        "O pilar mais crítico é <strong>Dados & Inteligência (0,33)</strong>: decisões são tomadas inteiramente por percepção, sem indicadores clínicos ou operacionais formais. Sem visibilidade de dados, é impossível identificar gargalos, medir resultados ou planejar expansão com segurança.",
        "Em <strong>Estratégia (0,67)</strong>, a clínica opera sem modelo híbrido definido, sem protocolos documentados e sem governança clínica do digital — o que significa que qualquer investimento em tecnologia feito hoje tende a ser subutilizado ou abandonado.",
        "No <strong>Modelo Econômico (0,83)</strong>, a receita é 100% transacional e imprevisível. A ausência de recorrência estruturada torna a clínica vulnerável a variações sazonais e impede projeções financeiras confiáveis.",
    ],
    "alertas": [
        "Dependência total de consultas avulsas — vulnerabilidade à sazonalidade",
        "Ausência de indicadores: impossível medir eficiência ou justificar investimentos",
        "Tecnologia fragmentada impede escala mesmo com aumento de demanda",
    ],
    "gaps_priorizados": [
        ("🔴", "Pilar 4 — Dados & Inteligência (0,33)", "Sem indicadores, a gestão é cega. Prioridade máxima."),
        ("🔴", "Pilar 1 — Estratégia & Modelo Assistencial (0,67)", "Sem direção clara, investimentos em tech não se sustentam."),
        ("🟠", "Pilar 5 — Modelo Econômico (0,83)", "Receita transacional 100% — risco de imprevisibilidade financeira."),
        ("🟠", "Pilares 2 e 3 — Operação & Tecnologia (1,00)", "Base operacional frágil — agendamento e prontuário subutilizados."),
    ],
    "receita_mensal": 30000,
    "incremento_pct": 15,
    "fase1_entrada": 8000,
    "fase1_conclusao": 16000,
    "fase1_semanas": 4,
    "fase2_entrada": 8000,
    "fase2_conclusao": 16000,
    "fase2_semanas": 8,
    "fase1_modulos": ["Módulo 01 — Arquitetura Assistencial", "Módulo 02 — Estrutura Operacional"],
    "fase2_modulos": ["Módulo 03 — Modelo Econômico & Receita Recorrente", "Módulo 04 — Arquitetura Tecnológica", "Módulo 05 — Gestão por Indicadores"],
    "output": "/tmp/relatorio_diagnostico_apr_ltda_v5.pdf",
}

ETHEL = {
    "nome": "Ethel Pinella",
    "clinica": "Ethel Pinella Clínica",
    "especialidade": "Endoscopia & Nutrologia",
    "cidade": "Leblon, Rio de Janeiro – RJ",
    "faturamento_mensal": "até R$ 30.000",
    "mes_ano": "Junho 2026",
    "score_final": 1.29,
    "nivel": "Inicial",
    "nivel_desc": "Operação artesanal, sem estrutura digital relevante",
    "pilares": [
        {
            "num": "01", "nome": "Estratégia & Modelo Assistencial", "peso": "25%",
            "score": 1.58, "classe": "baixo",
            "criterios": [
                ("Modelo assistencial híbrido definido", 2, "Digital existe mas não é estratégico"),
                ("Segmentação de pacientes por perfil/risco", 1.5, "Programas existem sem critério formal"),
                ("Protocolos clínicos digitais estruturados", 1, "Tudo informal"),
                ("Integração entre digital e presencial", 2, "Conectados via WhatsApp/agenda manual"),
                ("Governança clínica do digital", 1.5, "Responsabilidade difusa"),
                ("Alinhamento estratégico institucional", 1.5, "Objetivo existe mas não operacionalizado"),
            ],
            "desc": "Há iniciativas digitais em andamento, mas sem formalização estratégica. A integração digital-presencial acontece via WhatsApp — funcional, mas não escalável."
        },
        {
            "num": "02", "nome": "Operação & Jornada", "peso": "20%",
            "score": 1.33, "classe": "baixo",
            "criterios": [
                ("Fluxo de entrada digital estruturado", 1.5, "Agenda digital básica"),
                ("Integração da agenda (presencial + digital)", 1.5, "Mesma ferramenta, sem regras"),
                ("Programas de acompanhamento estruturados", 1.5, "1–2 programas informais"),
                ("Comunicação com paciente padronizada", 1, "Scripts informais via WhatsApp"),
                ("Experiência do paciente monitorada", 1, "Feedback informal ocasional"),
                ("Gestão de capacidade e demanda", 1.5, "Percebido mas não gerenciado"),
            ],
            "desc": "Operação com alguma digitalização básica. Programas de acompanhamento existem informalmente. Comunicação não padronizada limita a escalabilidade."
        },
        {
            "num": "03", "nome": "Tecnologia & Integração", "peso": "15%",
            "score": 1.17, "classe": "critico",
            "criterios": [
                ("Prontuário eletrônico estruturado", 1, "Sistema básico subutilizado"),
                ("Integração entre sistemas", 1, "Integração manual/parcial"),
                ("Plataforma de telemedicina adequada", 2, "Plataforma genérica em uso"),
                ("Interoperabilidade de dados", 1, "Exportação manual possível"),
                ("Segurança da informação (LGPD)", 1, "Política básica não auditada"),
                ("Infraestrutura tecnológica", 1, "Funcional mas frágil"),
            ],
            "desc": "Plataforma de telemedicina genérica em uso, mas sistemas não integrados. Dados em silos, prontuário subutilizado e LGPD sem auditoria."
        },
        {
            "num": "04", "nome": "Dados & Inteligência", "peso": "20%",
            "score": 1.00, "classe": "critico",
            "criterios": [
                ("Coleta estruturada de dados", 1, "Coleta parcial e manual"),
                ("Indicadores clínicos definidos", 1, "Indicadores informais conhecidos"),
                ("Indicadores operacionais definidos", 1, "Visibilidade parcial"),
                ("Uso de dados na decisão", 1, "Dados consultados às vezes"),
                ("Dashboards gerenciais", 1, "Planilha manual"),
                ("Analytics / predição", 1, "Análise descritiva básica"),
            ],
            "desc": "Algum uso de dados existe, mas tudo manual e informal. Sem dashboards automatizados ou KPIs formalizados para apoiar decisões clínicas e operacionais."
        },
        {
            "num": "05", "nome": "Modelo Econômico & Sustentabilidade", "peso": "20%",
            "score": 1.25, "classe": "baixo",
            "criterios": [
                ("Precificação estruturada", 1.5, "Tabela existe mas não seguida"),
                ("Modelo de receita definido", 1, "Mix com pouca recorrência"),
                ("Previsibilidade financeira", 1, "Previsão aproximada possível"),
                ("ROI do digital medido", 1, "Estimativa informal"),
                ("Alinhamento de incentivos", 2, "Parcialmente alinhados"),
                ("Controle de custos assistenciais", 1, "Controle financeiro geral"),
            ],
            "desc": "Modelo predominantemente transacional com alguma recorrência informal. Previsibilidade financeira baixa, sem mensuração formal do ROI digital."
        },
    ],
    "narrativa_paragrafos": [
        "A Ethel Pinella Clínica apresenta score de maturidade <strong>1,29 — nível Inicial</strong>, indicando uma operação que possui iniciativas digitais pontuais, mas ainda sem estrutura, governança ou integração que permita escala.",
        "O gap mais crítico está em <strong>Dados & Inteligência (1,00)</strong>: apesar de haver algum uso informal de dados, não há indicadores clínicos ou operacionais formalizados, nem dashboards que suportem decisões gerenciais com base em evidências.",
        "Em <strong>Tecnologia & Integração (1,17)</strong>, os sistemas existentes — prontuário e plataforma de telemedicina — operam de forma desintegrada e subutilizada. A ausência de interoperabilidade impede que os dados gerados se tornem inteligência acionável.",
        "No <strong>Modelo Econômico (1,25)</strong>, a receita ainda é predominantemente transacional. A clínica possui potencial para estruturar receita recorrente — especialmente em Nutrologia — mas ainda não captura esse valor de forma sistemática.",
    ],
    "alertas": [
        "Sistemas desintegrados: dados gerados não se transformam em inteligência",
        "Receita transacional dominante — vulnerabilidade a variações de demanda",
        "Governança digital difusa — sem responsável formal pelo digital",
    ],
    "gaps_priorizados": [
        ("🔴", "Pilar 4 — Dados & Inteligência (1,00)", "Sem KPIs formais, a clínica não consegue medir seu próprio progresso."),
        ("🔴", "Pilar 3 — Tecnologia & Integração (1,17)", "Sistemas desintegrados bloqueiam a extração de valor do digital."),
        ("🟠", "Pilar 5 — Modelo Econômico (1,25)", "Potencial de recorrência em Nutrologia não capturado."),
        ("🟠", "Pilares 1 e 2 — Estratégia & Operação (1,33–1,58)", "Iniciativas existem mas sem formalização ou protocolo."),
    ],
    "receita_mensal": 30000,
    "incremento_pct": 15,
    "fase1_entrada": 8000,
    "fase1_conclusao": 16000,
    "fase1_semanas": 4,
    "fase2_entrada": 8000,
    "fase2_conclusao": 16000,
    "fase2_semanas": 8,
    "fase1_modulos": ["Módulo 01 — Arquitetura Assistencial", "Módulo 02 — Estrutura Operacional"],
    "fase2_modulos": ["Módulo 03 — Modelo Econômico & Receita Recorrente", "Módulo 04 — Arquitetura Tecnológica", "Módulo 05 — Gestão por Indicadores"],
    "output": "/tmp/relatorio_diagnostico_ethel_pinella_v2.pdf",
}

DANIELA_BORGES = {
    "nome": "Daniela Borges",
    "clinica": "Imagecor",
    "especialidade": "Cardiologia",
    "cidade": "Catete, Rio de Janeiro – RJ",
    "faturamento_mensal": "até R$ 30.000",
    "mes_ano": "Junho 2026",
    "score_final": 0.58,
    "nivel": "Inicial",
    "nivel_desc": "Operação artesanal, sem estrutura digital relevante",
    "pilares": [
        {
            "num": "01", "nome": "Estratégia & Modelo Assistencial", "peso": "25%",
            "score": 0.50, "classe": "critico",
            "criterios": [
                ("Modelo assistencial híbrido definido", 1, "Somente presencial — sem telemedicina ou plano digital"),
                ("Segmentação de pacientes por perfil/risco", 1, "Perfil de crônicos identificado informalmente, sem critério formal"),
                ("Protocolos clínicos digitais estruturados", 0, "'Nenhum desses' — sem protocolos documentados"),
                ("Integração entre digital e presencial", 0, "'Nenhum desses' — operam completamente isolados"),
                ("Governança clínica do digital", 0, "Decisões 'na pessoa' — responsabilidade difusa, sem processo formal"),
                ("Alinhamento estratégico institucional", 1, "Objetivo declarado (novas receitas), mas sem operacionalização"),
            ],
            "desc": "Clínica 100% presencial, sem qualquer planejamento ou estrutura digital. Decisões centralizadas na gestora sem processos formais. Foco em exames cardiológicos (Eco/Doppler) é diferencial não explorado estrategicamente."
        },
        {
            "num": "02", "nome": "Operação & Jornada", "peso": "20%",
            "score": 0.50, "classe": "critico",
            "criterios": [
                ("Fluxo de entrada digital estruturado", 1, "Apenas WhatsApp e agenda — sem fluxo multicanal"),
                ("Integração da agenda (presencial + digital)", 1, "Agenda manual via WhatsApp; 3 salas com 8 de 11 turnos preenchidos"),
                ("Programas de acompanhamento estruturados", 0, "Nenhum programa ativo — crônicos sem follow-up estruturado"),
                ("Comunicação com paciente padronizada", 1, "Só WhatsApp — sem padrão, sem rastreabilidade"),
                ("Experiência do paciente monitorada", 0, "Sem NPS ou pesquisa de satisfação"),
                ("Gestão de capacidade e demanda", 0, "Ocupação baixa, 3 salas / 8 turnos de 11 — sem gestão ativa"),
            ],
            "desc": "Operação reativa e subutilizada — 3 salas com apenas 8 dos 11 turnos possíveis preenchidos e taxa de retorno abaixo de 50%. Pacientes crônicos sem programa de acompanhamento representam receita recorrente não capturada."
        },
        {
            "num": "03", "nome": "Tecnologia & Integração", "peso": "15%",
            "score": 1.00, "classe": "critico",
            "criterios": [
                ("Prontuário eletrônico estruturado", 2, "Possui PEP, nota 6/10 — presente mas subutilizado"),
                ("Integração entre sistemas", 1, "Agenda e prontuário não integrados, WhatsApp paralelo"),
                ("Plataforma de telemedicina adequada", 0, "Não usa telemedicina"),
                ("Interoperabilidade de dados", 1, "Dados em silos — exportação manual possível"),
                ("Segurança da informação (LGPD)", 1, "Sem menção a política formal — inferência conservadora"),
                ("Infraestrutura tecnológica", 1, "Improvisada — WhatsApp/agenda como base operacional"),
            ],
            "desc": "Prontuário eletrônico existe (nota 6) mas é subutilizado. Infraestrutura improvisada via WhatsApp. Exames de imagem (Eco, Doppler, Holter) geram dados clínicos valiosos que não se transformam em inteligência de gestão."
        },
        {
            "num": "04", "nome": "Dados & Inteligência", "peso": "20%",
            "score": 0.33, "classe": "critico",
            "criterios": [
                ("Coleta estruturada de dados", 1, "Coleta parcial via prontuário — nota 4 para gestão de dados"),
                ("Indicadores clínicos definidos", 0, "Sem indicadores clínicos formais"),
                ("Indicadores operacionais definidos", 1, "Ticket médio acompanhado, mas visibilidade parcial"),
                ("Uso de dados na decisão", 0, "Decisões 'na pessoa' — gestão por percepção"),
                ("Dashboards gerenciais", 0, "Inexistente — sem painel de controle"),
                ("Analytics / predição", 0, "Nenhum uso preditivo ou analítico"),
            ],
            "desc": "Gestão 100% intuitiva. Apesar de monitorar ticket médio, não há indicadores clínicos, operacionais ou dashboard. A frase 'muito trabalho, pouco controle financeiro' sintetiza a ausência de dados na decisão."
        },
        {
            "num": "05", "nome": "Modelo Econômico & Sustentabilidade", "peso": "20%",
            "score": 0.67, "classe": "critico",
            "criterios": [
                ("Precificação estruturada", 1, "Ticket R$78-80 conhecido, mas nota financeiro = 1"),
                ("Modelo de receita definido", 1, "Misto 50-50 (plano/particular) com recorrência variável"),
                ("Previsibilidade financeira", 0, "Dívidas e dificuldade de captação — receita imprevisível"),
                ("ROI do digital medido", 0, "Nota marketing = 1 — sem mensuração de retorno digital"),
                ("Alinhamento de incentivos", 1, "Percentual por atendimento — pode desincentivar qualidade"),
                ("Controle de custos assistenciais", 1, "Controle financeiro 'Sim' mas nota 1 — superficial"),
            ],
            "desc": "Modelo econômico frágil com dívidas declaradas. Receita mista (plano/particular) mas imprevisível. Taxa de retorno <50% e 70% de pacientes novos indicam dependência de captação constante — modelo insustentável no médio prazo."
        },
    ],
    "narrativa_paragrafos": [
        "A Imagecor apresenta score de maturidade <strong>0,58 — nível Inicial</strong>, com uma operação artesanal que concentra todos os riscos na gestora e depende de captação constante de novos pacientes para se sustentar. A frase da própria Daniela resume o diagnóstico: <em>\"muito trabalho, pouco controle financeiro\"</em>.",
        "O desafio mais urgente é a <strong>ausência de dados na decisão (Pilar 4: 0,33)</strong>: sem indicadores, dashboard ou visibilidade financeira real, é impossível identificar onde estão as perdas, o que está funcionando ou como priorizar os investimentos. A nota 1 para controle financeiro confirma que o problema não é falta de esforço — é falta de sistema.",
        "Em <strong>Operações (Pilar 2: 0,50)</strong>, a clínica possui 3 salas com apenas 8 dos 11 turnos possíveis preenchidos e taxa de retorno abaixo de 50%. Isso significa que mais da metade dos pacientes cardiológicos — crônicos que deveriam voltar regularmente — não retorna. Esse é o maior vazamento de receita da Imagecor.",
        "O <strong>Modelo Econômico (Pilar 5: 0,67)</strong> é igualmente crítico: com 70% de pacientes novos, a clínica precisa captar continuamente apenas para manter o faturamento atual. Sem recorrência estruturada e com dívidas declaradas, o crescimento orgânico está bloqueado. A boa notícia: exames de Eco e Doppler + perfil de crônicos são ativos ideais para construir receita recorrente.",
    ],
    "alertas": [
        "Dívidas declaradas + receita imprevisível = risco de ruptura financeira no curto prazo",
        "Taxa de retorno <50% em cardiologia crônica: o maior vazamento de receita identificado",
        "3 salas, 8/11 turnos preenchidos: capacidade ociosa gerando custo fixo sem retorno",
        "70% pacientes novos: modelo insustentável — captação constante como única alavanca",
    ],
    "gaps_priorizados": [
        ("🔴", "Pilares 1, 2 e 4 (0,50)", "Ausência de sistema de gestão — operação por percepção, sem dados, sem processos."),
        ("🔴", "Retenção de pacientes crônicos (<50% retorno)", "Cardiologia crônica tem natureza recorrente — a não-retenção é receita desperdiçada."),
        ("🟠", "Pilar 5 — Modelo Econômico (0,67)", "Dívidas + dependência de novos pacientes tornam o crescimento insustentável."),
        ("🟠", "Capacidade ociosa (8/11 turnos)", "Receita potencial já existe — o problema é gestão, não demanda."),
    ],
    "receita_mensal": 30000,
    "incremento_pct": 15,
    "fase1_entrada": 8000,
    "fase1_conclusao": 16000,
    "fase1_semanas": 4,
    "fase2_entrada": 8000,
    "fase2_conclusao": 16000,
    "fase2_semanas": 8,
    "fase1_modulos": ["Módulo 01 — Arquitetura Assistencial", "Módulo 02 — Estrutura Operacional & Retenção"],
    "fase2_modulos": ["Módulo 03 — Modelo Econômico & Receita Recorrente", "Módulo 04 — Arquitetura Tecnológica", "Módulo 05 — Gestão por Indicadores"],
    "output": "/tmp/relatorio_diagnostico_imagecor.pdf",
}

# ─── HTML GENERATION ──────────────────────────────────────────────────────────

def score_to_bar_pct(score):
    return round(score / 5.0 * 100, 1)

def score_color(score):
    if score < 1.6:
        return "#C0392B"
    elif score < 2.6:
        return "#E67E22"
    elif score < 3.6:
        return "#F1C40F"
    elif score < 4.6:
        return "#27AE60"
    else:
        return "#0F7173"

def pilar_card_html(p, c):
    cls = p["classe"]
    score = p["score"]
    col = score_color(score)
    criterios_rows = ""
    for nome, nota, just in p["criterios"]:
        nota_fmt = f"{nota:.1f}"
        criterios_rows += f"""
        <tr>
          <td class="crit-nome">{nome}</td>
          <td class="crit-just">{just}</td>
          <td class="crit-nota">{nota_fmt}</td>
        </tr>"""
    return f"""
    <div class="pilar-card {cls}">
      <div class="pilar-score-row">
        <div class="pilar-score-num" style="color:{col}">{score:.2f}</div>
        <div>
          <div class="pilar-nome">{p['nome']}</div>
          <div class="pilar-peso">Peso: {p['peso']}</div>
        </div>
      </div>
      <div class="pilar-desc">{p['desc']}</div>
    </div>"""

def gerar_html(c):
    score = c["score_final"]
    score_pct = score_to_bar_pct(score)
    score_col = score_color(score)

    # Cover info items
    info_items = f"""
    <div class="cover-info-item">
      <div class="cover-info-label">Especialidade</div>
      <div class="cover-info-value">{c['especialidade']}</div>
    </div>
    <div class="cover-info-item">
      <div class="cover-info-label">Faturamento mensal</div>
      <div class="cover-info-value">{c['faturamento_mensal']}</div>
    </div>
    <div class="cover-info-item">
      <div class="cover-info-label">Localização</div>
      <div class="cover-info-value">{c['cidade']}</div>
    </div>
    <div class="cover-info-item">
      <div class="cover-info-label">Data</div>
      <div class="cover-info-value">{c['mes_ano']}</div>
    </div>"""

    # Pilar cards for overview page
    cards_html = ""
    for p in c["pilares"]:
        cards_html += pilar_card_html(p, c)

    # Section 2: criteria tables per pilar
    criterios_sections = ""
    for p in c["pilares"]:
        rows = ""
        for nome, nota, just in p["criterios"]:
            nota_fmt = f"{nota:.1f}"
            rows += f"""
            <tr>
              <td class="crit-nome">{nome}</td>
              <td class="crit-just">{just}</td>
              <td class="crit-nota">{nota_fmt}</td>
            </tr>"""
        col = score_color(p["score"])
        criterios_sections += f"""
        <div class="criterios-pilar">
          <div class="criterios-pilar-header">
            <span class="criterios-pilar-num">{p['num']}</span>
            <span class="criterios-pilar-nome">{p['nome']}</span>
            <span class="score-avg" style="color:{col}">Média: {p['score']:.2f}</span>
          </div>
          <table class="criterios-table">
            <thead><tr><th>Critério</th><th>Evidência / Racional</th><th>Nota</th></tr></thead>
            <tbody>{rows}</tbody>
          </table>
        </div>"""

    # Narrative
    paras = "".join(f"<p>{p}</p>" for p in c["narrativa_paragrafos"])
    alertas = "".join(f"<li>{a}</li>" for a in c["alertas"])
    gaps = ""
    for icon, titulo, desc in c["gaps_priorizados"]:
        gaps += f"""
        <li class="gap-item">
          <span class="gap-icon">{icon}</span>
          <div><strong>{titulo}</strong><br>{desc}</div>
        </li>"""

    # ROI calc
    rec = c["receita_mensal"]
    inc_pct = c["incremento_pct"]
    incremento_anual = rec * 12 * (inc_pct / 100)
    investimento_total = c["fase1_entrada"] + c["fase1_conclusao"] + c["fase2_entrada"] + c["fase2_conclusao"]
    roi = incremento_anual / investimento_total
    payback = round(investimento_total / (incremento_anual / 12), 1)

    fase1_mods = "".join(f"<li>✔ {m}</li>" for m in c["fase1_modulos"])
    fase2_mods = "".join(f"<li>✔ {m}</li>" for m in c["fase2_modulos"])

    html = f"""<!DOCTYPE html>
<html lang="pt-BR">
<head>
<meta charset="UTF-8">
<style>
  @import url('https://fonts.googleapis.com/css2?family=Inter:wght@400;600;700;800&display=swap');
  :root {{
    --teal: #0F7173;
    --teal-dark: #095052;
    --teal-light: #1A9496;
    --navy: #1B3A5C;
    --dark: #0D1B2A;
    --gray-light: #F7F8FA;
    --gray-mid: #E2E8F0;
    --red: #C0392B;
    --orange: #E67E22;
    --text: #1A1A2E;
    --text-mid: #4A5568;
    --text-light: #718096;
  }}
  * {{ margin:0; padding:0; box-sizing:border-box; }}
  body {{ font-family:'Inter',sans-serif; color:var(--text); font-size:10pt; line-height:1.5; }}

  /* ── PAGE SETUP ── */
  .page {{ width:210mm; min-height:297mm; padding:0; page-break-after:always; position:relative; overflow:hidden; }}
  .page:last-child {{ page-break-after:auto; }}

  /* ── COVER (Ethel style) ── */
  .cover {{
    background:var(--dark);
    display:flex; flex-direction:column; justify-content:space-between;
    padding:60px 64px; height:297mm;
  }}
  .cover::before {{
    content:''; position:absolute; top:-80px; right:-80px;
    width:360px; height:360px; border-radius:50%;
    background:var(--teal); opacity:0.12;
  }}
  .cover::after {{
    content:''; position:absolute; bottom:60px; left:-100px;
    width:300px; height:300px; border-radius:50%;
    background:var(--teal-light); opacity:0.07;
  }}
  .cover-top {{ position:relative; z-index:1; }}
  .cover-tag {{
    display:inline-block; background:rgba(15,113,115,0.2);
    border:1px solid rgba(15,113,115,0.4); color:var(--teal-light);
    font-size:8pt; font-weight:600; letter-spacing:1.5px; text-transform:uppercase;
    padding:4px 12px; border-radius:3px; margin-bottom:32px;
  }}
  .cover-title {{ color:#FFFFFF; font-size:28pt; font-weight:800; line-height:1.15; margin-bottom:8px; }}
  .cover-title span {{ color:var(--teal-light); }}
  .cover-subtitle {{ color:rgba(255,255,255,0.55); font-size:12pt; font-weight:400; margin-bottom:40px; }}
  .cover-info {{ display:flex; gap:32px; flex-wrap:wrap; }}
  .cover-info-item {{ border-left:2px solid var(--teal); padding-left:12px; }}
  .cover-info-label {{ color:rgba(255,255,255,0.45); font-size:7.5pt; font-weight:600; text-transform:uppercase; letter-spacing:0.8px; margin-bottom:3px; }}
  .cover-info-value {{ color:#FFFFFF; font-size:10pt; font-weight:600; }}

  .cover-bottom {{ position:relative; z-index:1; display:flex; justify-content:space-between; align-items:flex-end; }}
  .cover-score-hero {{ text-align:right; }}
  .cover-score-label {{ color:rgba(255,255,255,0.5); font-size:8pt; font-weight:600; text-transform:uppercase; letter-spacing:1px; margin-bottom:4px; }}
  .cover-score-num {{ font-size:52pt; font-weight:800; color:var(--teal-light); line-height:1; }}
  .cover-score-max {{ color:rgba(255,255,255,0.35); font-size:14pt; font-weight:400; }}
  .cover-score-badge {{
    display:inline-block; margin-top:8px;
    background:rgba(192,57,43,0.18); border:1px solid rgba(192,57,43,0.4);
    color:#ff9999; font-size:9pt; font-weight:700; padding:4px 14px; border-radius:3px;
  }}
  .cover-fletic {{ color:rgba(255,255,255,0.35); font-size:8pt; font-weight:600; letter-spacing:1px; text-transform:uppercase; }}

  /* ── INTERNAL PAGES (Ana Paula style) ── */
  .inner-page {{ padding:40px 48px; height:297mm; display:flex; flex-direction:column; }}
  .inner-header {{
    display:flex; justify-content:space-between; align-items:center;
    border-bottom:2px solid var(--teal); padding-bottom:10px; margin-bottom:28px;
  }}
  .inner-header-title {{ font-size:8pt; font-weight:700; color:var(--teal); letter-spacing:1.5px; text-transform:uppercase; }}
  .inner-header-client {{ font-size:8pt; color:var(--text-mid); }}

  .section-header {{ display:flex; align-items:flex-start; gap:16px; margin-bottom:20px; }}
  .section-num {{ font-size:40pt; font-weight:800; color:var(--teal-light); opacity:0.3; min-width:60px; line-height:1; }}
  .section-title {{ font-size:16pt; font-weight:800; color:var(--text); padding-top:8px; }}
  .section-sub {{ font-size:9pt; color:var(--text-mid); margin-top:2px; }}

  /* Score hero */
  .score-hero {{
    display:flex; align-items:center; gap:32px;
    background:var(--gray-light); border-radius:8px;
    border-left:4px solid var(--teal); padding:20px 28px; margin-bottom:24px;
  }}
  .score-number {{ font-size:50pt; font-weight:800; color:var(--teal); line-height:1; }}
  .score-info {{ flex:1; }}
  .score-nivel-name {{ font-size:18pt; font-weight:800; color:var(--text); }}
  .score-nivel-desc {{ font-size:9pt; color:var(--text-mid); margin-top:4px; }}

  /* Linear scale bar */
  .scale-wrap {{ margin-top:12px; }}
  .scale-label-row {{ display:flex; justify-content:space-between; font-size:7.5pt; color:var(--text-light); margin-bottom:4px; }}
  .scale-track {{ background:linear-gradient(to right,#C0392B 0%,#E67E22 32%,#F1C40F 52%,#27AE60 72%,#0F7173 100%); border-radius:4px; height:10px; position:relative; }}
  .scale-marker {{ width:14px; height:14px; border-radius:50%; background:#fff; border:3px solid #1A1A2E; position:absolute; top:-2px; transform:translateX(-50%); box-shadow:0 1px 4px rgba(0,0,0,0.35); }}
  .scale-ticks {{ display:flex; justify-content:space-between; font-size:7pt; color:var(--text-light); margin-top:5px; }}
  .scale-levels {{ display:flex; justify-content:space-between; font-size:6.5pt; color:var(--text-light); margin-top:2px; }}

  /* Pilar cards */
  .pilares-grid {{ display:grid; grid-template-columns:1fr 1fr; gap:12px; margin-bottom:16px; }}
  .pilar-card {{
    background:var(--gray-light); border-radius:6px;
    border-left:3px solid var(--teal); padding:12px 14px;
  }}
  .pilar-card.critico {{ border-left-color:var(--red); }}
  .pilar-card.baixo {{ border-left-color:var(--orange); }}
  .pilar-score-row {{ display:flex; align-items:center; gap:10px; margin-bottom:6px; }}
  .pilar-score-num {{ font-size:20pt; font-weight:800; line-height:1; }}
  .pilar-nome {{ font-size:9pt; font-weight:700; color:var(--text); }}
  .pilar-peso {{ font-size:7.5pt; color:var(--text-light); }}
  .pilar-desc {{ font-size:8pt; color:var(--text-mid); line-height:1.4; border-top:1px solid var(--gray-mid); padding-top:6px; margin-top:4px; }}

  /* Criteria tables */
  .criterios-pilar {{ margin-bottom:18px; }}
  .criterios-pilar-header {{ display:flex; align-items:center; gap:10px; margin-bottom:6px; background:var(--gray-light); padding:6px 10px; border-radius:4px; }}
  .criterios-pilar-num {{ font-size:13pt; font-weight:800; color:var(--teal-light); opacity:0.6; min-width:28px; }}
  .criterios-pilar-nome {{ font-size:9pt; font-weight:700; color:var(--text); flex:1; }}
  .score-avg {{ font-weight:800; font-size:9pt; }}
  .criterios-table {{ width:100%; border-collapse:collapse; font-size:8pt; }}
  .criterios-table th {{ text-align:left; padding:5px 8px; background:var(--navy); color:#fff; font-size:7.5pt; font-weight:700; }}
  .criterios-table td {{ padding:5px 8px; border-bottom:1px solid var(--gray-mid); vertical-align:top; }}
  .criterios-table tr:nth-child(even) td {{ background:var(--gray-light); }}
  .crit-nome {{ width:38%; font-weight:600; }}
  .crit-just {{ width:50%; color:var(--text-mid); }}
  .crit-nota {{ width:12%; text-align:center; font-weight:800; color:var(--teal); }}

  .calc-box {{
    background:#E8F4F4; border:1px solid rgba(15,113,115,0.25);
    border-radius:6px; padding:12px 16px; margin-top:16px; font-size:8pt;
  }}
  .calc-box-title {{ font-weight:800; color:var(--teal-dark); margin-bottom:6px; font-size:9pt; }}
  .calc-row {{ display:flex; justify-content:space-between; margin-bottom:3px; }}
  .calc-label {{ color:var(--text-mid); }}
  .calc-val {{ font-weight:700; color:var(--text); }}

  /* Narrative */
  .narrativa-block {{
    background:var(--gray-light); border-left:3px solid var(--teal);
    border-radius:0 6px 6px 0; padding:14px 18px; margin-bottom:14px;
  }}
  .narrativa-block p {{ margin-bottom:8px; font-size:9pt; line-height:1.6; color:var(--text); }}
  .narrativa-block p:last-child {{ margin-bottom:0; }}
  .alerta-box {{
    background:#fff8f6; border:1px solid rgba(192,57,43,0.2);
    border-radius:6px; padding:12px 16px; margin-bottom:14px;
  }}
  .alerta-box-title {{ font-weight:800; color:var(--red); font-size:9pt; margin-bottom:8px; }}
  .alerta-box ul {{ list-style:none; padding:0; }}
  .alerta-box li {{ font-size:8.5pt; color:var(--text); padding:3px 0; padding-left:18px; position:relative; }}
  .alerta-box li::before {{ content:'⚠'; position:absolute; left:0; color:var(--orange); }}
  .gap-list {{ list-style:none; padding:0; }}
  .gap-item {{ display:flex; gap:12px; padding:8px 0; border-bottom:1px solid var(--gray-mid); font-size:8.5pt; }}
  .gap-item:last-child {{ border-bottom:none; }}
  .gap-icon {{ font-size:13pt; flex-shrink:0; }}

  /* Footer */
  .footer {{
    margin-top:auto; padding-top:12px;
    border-top:1px solid var(--gray-mid);
    display:flex; justify-content:space-between; align-items:center;
    font-size:7pt; color:var(--text-light);
  }}
  .footer-logo {{ font-weight:800; color:var(--teal); font-size:8pt; }}

  /* ROI / investment */
  .roi-section {{ display:flex; gap:16px; margin-top:20px; }}
  .roi-box {{
    flex:1; background:var(--gray-light); border-radius:6px;
    border:1px solid var(--gray-mid); padding:14px 16px;
  }}
  .roi-box-title {{ font-size:8pt; font-weight:700; color:var(--text-mid); text-transform:uppercase; letter-spacing:0.5px; margin-bottom:8px; }}
  .roi-number {{ font-size:22pt; font-weight:800; color:var(--teal); line-height:1; }}
  .roi-label {{ font-size:7.5pt; color:var(--text-light); margin-top:3px; }}

  .fase-block {{
    background:var(--gray-light); border-radius:6px; padding:14px 18px; margin-bottom:14px;
    border-left:3px solid var(--teal);
  }}
  .fase-title {{ font-size:11pt; font-weight:800; color:var(--text); margin-bottom:4px; }}
  .fase-sub {{ font-size:8pt; color:var(--text-mid); margin-bottom:10px; }}
  .fase-mods {{ list-style:none; padding:0; }}
  .fase-mods li {{ font-size:8.5pt; padding:2px 0; color:var(--text); }}
  .fase-payment {{ display:flex; gap:10px; margin-top:10px; flex-wrap:wrap; }}
  .payment-chip {{
    background:#E8F4F4; border:1px solid rgba(15,113,115,0.3);
    border-radius:4px; padding:4px 10px; font-size:8pt; font-weight:700; color:var(--teal-dark);
  }}

  @media print {{
    body {{ -webkit-print-color-adjust:exact; print-color-adjust:exact; }}
    .page {{ page-break-after:always; }}
  }}
</style>
</head>
<body>

<!-- ════ PAGE 1: COVER ════ -->
<div class="page cover">
  <div class="cover-top">
    <div class="cover-tag">Diagnóstico de Maturidade Digital · Confidencial</div>
    <div class="cover-title">Diagnóstico<br><span>{c['nome']}</span></div>
    <div class="cover-subtitle">Relatório Executivo de Maturidade Digital em Saúde</div>
    <div class="cover-info">
      {info_items}
    </div>
  </div>
  <div class="cover-bottom">
    <div class="cover-fletic">Fletic Vision · Saúde Digital · {c['mes_ano']}</div>
    <div class="cover-score-hero">
      <div class="cover-score-label">Índice de Maturidade</div>
      <div class="cover-score-num">{c['score_final']:.2f}<span class="cover-score-max">/5,00</span></div>
      <div class="cover-score-badge">{c['nivel']} — {c['nivel_desc'][:32]}…</div>
    </div>
  </div>
</div>

<!-- ════ PAGE 2: VISÃO GERAL ════ -->
<div class="page inner-page">
  <div class="inner-header">
    <div class="inner-header-title">Fletic Vision · Diagnóstico de Maturidade</div>
    <div class="inner-header-client">{c['nome']} · {c['clinica']}</div>
  </div>

  <div class="section-header">
    <div class="section-num">01</div>
    <div>
      <div class="section-title">Resultado Global</div>
      <div class="section-sub">Score ponderado pelos 5 pilares de maturidade digital</div>
    </div>
  </div>

  <div class="score-hero">
    <div class="score-number">{c['score_final']:.2f}</div>
    <div class="score-info">
      <div class="score-nivel-name">{c['nivel']}</div>
      <div class="score-nivel-desc">{c['nivel_desc']}</div>
      <div class="scale-wrap">
        <div class="scale-label-row"><span>0,00</span><span>5,00</span></div>
        <div class="scale-track">
          <div class="scale-marker" style="left:{score_pct}%"></div>
        </div>
        <div class="scale-ticks"><span>0</span><span>1</span><span>2</span><span>3</span><span>4</span><span>5</span></div>
        <div class="scale-levels"><span>Inicial</span><span>Estruturando</span><span>Em Evolução</span><span>Avançado</span><span>Referência</span></div>
      </div>
    </div>
  </div>

  <div class="pilares-grid">
    {"".join(pilar_card_html(p, c) for p in c["pilares"])}
  </div>

  <div class="footer">
    <div class="footer-logo">FleticVision</div>
    <div>Diagnóstico de Maturidade · {c['clinica']} · Confidencial · {c['mes_ano']}</div>
    <div>Pág. 2</div>
  </div>
</div>

<!-- ════ PAGE 3: CRITÉRIOS DETALHADOS (pilares 1-3) ════ -->
<div class="page inner-page">
  <div class="inner-header">
    <div class="inner-header-title">Fletic Vision · Critérios Detalhados</div>
    <div class="inner-header-client">{c['nome']} · {c['clinica']}</div>
  </div>

  <div class="section-header">
    <div class="section-num">02</div>
    <div>
      <div class="section-title">Avaliação por Critério</div>
      <div class="section-sub">30 critérios distribuídos em 5 pilares — escala 0 a 5</div>
    </div>
  </div>

  {criterios_sections[:len(criterios_sections)//2 + criterios_sections[:len(criterios_sections)//2].rfind("</div>") + 6]}

  <div class="footer">
    <div class="footer-logo">FleticVision</div>
    <div>Diagnóstico de Maturidade · {c['clinica']} · Confidencial · {c['mes_ano']}</div>
    <div>Pág. 3</div>
  </div>
</div>

<!-- ════ PAGE 4: CRITÉRIOS (pilares 4-5 + calc) ════ -->
<div class="page inner-page">
  <div class="inner-header">
    <div class="inner-header-title">Fletic Vision · Critérios Detalhados</div>
    <div class="inner-header-client">{c['nome']} · {c['clinica']}</div>
  </div>

  {criterios_sections[len(criterios_sections)//2 + criterios_sections[:len(criterios_sections)//2].rfind("</div>") + 6:]}

  <div class="calc-box">
    <div class="calc-box-title">Cálculo do Score Final Ponderado</div>
    {"".join(f'<div class="calc-row"><span class="calc-label">{p["num"]}. {p["nome"]} ({p["peso"]})</span><span class="calc-val">{p["score"]:.2f}</span></div>' for p in c["pilares"])}
    <div class="calc-row" style="border-top:1px solid rgba(15,113,115,0.3);margin-top:6px;padding-top:6px;">
      <span class="calc-label" style="font-weight:800;color:var(--teal-dark)">Score Final Ponderado</span>
      <span class="calc-val" style="color:var(--teal);font-size:11pt">{c['score_final']:.2f}</span>
    </div>
  </div>

  <div class="footer">
    <div class="footer-logo">FleticVision</div>
    <div>Diagnóstico de Maturidade · {c['clinica']} · Confidencial · {c['mes_ano']}</div>
    <div>Pág. 4</div>
  </div>
</div>

<!-- ════ PAGE 5: NARRATIVA & GAPS ════ -->
<div class="page inner-page">
  <div class="inner-header">
    <div class="inner-header-title">Fletic Vision · Diagnóstico Narrativo</div>
    <div class="inner-header-client">{c['nome']} · {c['clinica']}</div>
  </div>

  <div class="section-header">
    <div class="section-num">03</div>
    <div>
      <div class="section-title">Diagnóstico Narrativo</div>
      <div class="section-sub">Leitura executiva dos resultados — gaps e oportunidades prioritárias</div>
    </div>
  </div>

  <div class="narrativa-block">
    {paras}
  </div>

  <div class="alerta-box">
    <div class="alerta-box-title">Alertas Prioritários</div>
    <ul>{alertas}</ul>
  </div>

  <div style="margin-top:14px;">
    <div style="font-size:9pt;font-weight:800;color:var(--text);margin-bottom:8px;">Gaps por Ordem de Prioridade</div>
    <ul class="gap-list">{gaps}</ul>
  </div>

  <div class="footer">
    <div class="footer-logo">FleticVision</div>
    <div>Diagnóstico de Maturidade · {c['clinica']} · Confidencial · {c['mes_ano']}</div>
    <div>Pág. 5</div>
  </div>
</div>

<!-- ════ PAGE 6: PROPOSTA COMERCIAL ════ -->
<div class="page inner-page">
  <div class="inner-header">
    <div class="inner-header-title">Fletic Vision · Proposta de Intervenção</div>
    <div class="inner-header-client">{c['nome']} · {c['clinica']}</div>
  </div>

  <div class="section-header">
    <div class="section-num">04</div>
    <div>
      <div class="section-title">Plano de Intervenção</div>
      <div class="section-sub">Estruturado em 2 fases — cada módulo derivado de um gap identificado</div>
    </div>
  </div>

  <div class="fase-block">
    <div class="fase-title">Fase 1 — Fundação Operacional · {c['fase1_semanas']} semanas</div>
    <div class="fase-sub">Menor risco, menor ticket, gera confiança para a Fase 2</div>
    <ul class="fase-mods">{fase1_mods}</ul>
    <div class="fase-payment">
      <div class="payment-chip">Entrada: R$ {c['fase1_entrada']:,.0f}</div>
      <div class="payment-chip">Conclusão: R$ {c['fase1_conclusao']:,.0f}</div>
      <div class="payment-chip">Total Fase 1: R$ {c['fase1_entrada']+c['fase1_conclusao']:,.0f}</div>
    </div>
  </div>

  <div class="fase-block">
    <div class="fase-title">Fase 2 — Crescimento Sustentável · {c['fase2_semanas']} semanas adicionais</div>
    <div class="fase-sub">Onde o ROI real se materializa — tecnologia, dados e modelo econômico</div>
    <ul class="fase-mods">{fase2_mods}</ul>
    <div class="fase-payment">
      <div class="payment-chip">Entrada: R$ {c['fase2_entrada']:,.0f}</div>
      <div class="payment-chip">Conclusão: R$ {c['fase2_conclusao']:,.0f}</div>
      <div class="payment-chip">Total Fase 2: R$ {c['fase2_entrada']+c['fase2_conclusao']:,.0f}</div>
    </div>
  </div>

  <div class="roi-section">
    <div class="roi-box">
      <div class="roi-box-title">Investimento Total</div>
      <div class="roi-number">R$ {investimento_total:,.0f}</div>
      <div class="roi-label">5 módulos · 12 semanas · Fixo</div>
    </div>
    <div class="roi-box">
      <div class="roi-box-title">Incremento Anual Projetado</div>
      <div class="roi-number">R$ {incremento_anual:,.0f}</div>
      <div class="roi-label">+{inc_pct}% s/ faturamento atual (conservador)</div>
    </div>
    <div class="roi-box">
      <div class="roi-box-title">ROI Estimado</div>
      <div class="roi-number">{roi:.1f}×</div>
      <div class="roi-label">Payback em ~{payback:.0f} meses</div>
    </div>
  </div>

  <div style="margin-top:16px;background:#E8F4F4;border-radius:6px;padding:12px 16px;font-size:8pt;color:var(--text-mid);">
    <strong style="color:var(--teal-dark)">Modelo Comercial:</strong> Fixo — pagamento em 4 parcelas (entrada + conclusão por fase).
    Premissas de crescimento declaradas como conservadoras. Valores reais dependem da implementação.
  </div>

  <div class="footer">
    <div class="footer-logo">FleticVision</div>
    <div>Diagnóstico de Maturidade · {c['clinica']} · Confidencial · {c['mes_ano']}</div>
    <div>Pág. 6</div>
  </div>
</div>

</body>
</html>"""
    return html

# ─── SPLIT CRITERIA SECTIONS PROPERLY ────────────────────────────────────────

def gerar_html_v2(c):
    """Generate HTML with proper page splitting of criteria sections."""
    score = c["score_final"]
    score_pct = score_to_bar_pct(score)
    score_col = score_color(score)

    info_items = f"""
    <div class="cover-info-item">
      <div class="cover-info-label">Especialidade</div>
      <div class="cover-info-value">{c['especialidade']}</div>
    </div>
    <div class="cover-info-item">
      <div class="cover-info-label">Faturamento mensal</div>
      <div class="cover-info-value">{c['faturamento_mensal']}</div>
    </div>
    <div class="cover-info-item">
      <div class="cover-info-label">Localização</div>
      <div class="cover-info-value">{c['cidade']}</div>
    </div>
    <div class="cover-info-item">
      <div class="cover-info-label">Data</div>
      <div class="cover-info-value">{c['mes_ano']}</div>
    </div>"""

    # Build individual criteria section HTMLs
    crit_sections = []
    for p in c["pilares"]:
        rows = ""
        for nome, nota, just in p["criterios"]:
            nota_fmt = f"{nota:.1f}"
            rows += f"""
            <tr>
              <td class="crit-nome">{nome}</td>
              <td class="crit-just">{just}</td>
              <td class="crit-nota">{nota_fmt}</td>
            </tr>"""
        col = score_color(p["score"])
        crit_sections.append(f"""
        <div class="criterios-pilar">
          <div class="criterios-pilar-header">
            <span class="criterios-pilar-num">{p['num']}</span>
            <span class="criterios-pilar-nome">{p['nome']}</span>
            <span class="score-avg" style="color:{col}">Média: {p['score']:.2f}</span>
          </div>
          <table class="criterios-table">
            <thead><tr><th>Critério</th><th>Evidência / Racional</th><th>Nota</th></tr></thead>
            <tbody>{rows}</tbody>
          </table>
        </div>""")

    # First 3 pilares on page 3, last 2 + calc on page 4
    criterios_p3 = "".join(crit_sections[:3])
    criterios_p4 = "".join(crit_sections[3:])

    # Narrative
    paras = "".join(f"<p>{p}</p>" for p in c["narrativa_paragrafos"])
    alertas = "".join(f"<li>{a}</li>" for a in c["alertas"])
    gaps = ""
    for icon, titulo, desc in c["gaps_priorizados"]:
        gaps += f"""
        <li class="gap-item">
          <span class="gap-icon">{icon}</span>
          <div><strong>{titulo}</strong><br>{desc}</div>
        </li>"""

    calc_rows = "".join(
        f'<div class="calc-row"><span class="calc-label">{p["num"]}. {p["nome"]} ({p["peso"]})</span><span class="calc-val">{p["score"]:.2f}</span></div>'
        for p in c["pilares"]
    )

    # Pilar cards
    cards = "".join(pilar_card_html(p, c) for p in c["pilares"])

    html = f"""<!DOCTYPE html>
<html lang="pt-BR">
<head>
<meta charset="UTF-8">
<style>
  @import url('https://fonts.googleapis.com/css2?family=Inter:wght@400;600;700;800&display=swap');
  :root {{
    --teal: #0F7173;
    --teal-dark: #095052;
    --teal-light: #1A9496;
    --navy: #1B3A5C;
    --dark: #0D1B2A;
    --gray-light: #F7F8FA;
    --gray-mid: #E2E8F0;
    --red: #C0392B;
    --orange: #E67E22;
    --text: #1A1A2E;
    --text-mid: #4A5568;
    --text-light: #718096;
  }}
  * {{ margin:0; padding:0; box-sizing:border-box; }}
  body {{ font-family:'Inter',sans-serif; color:var(--text); font-size:10pt; line-height:1.5; }}

  .page {{ width:210mm; min-height:297mm; padding:0; page-break-after:always; position:relative; overflow:hidden; }}
  .page:last-child {{ page-break-after:auto; }}

  /* COVER */
  .cover {{ background:var(--dark); display:flex; flex-direction:column; justify-content:space-between; padding:60px 64px; height:297mm; }}
  .cover::before {{ content:''; position:absolute; top:-80px; right:-80px; width:360px; height:360px; border-radius:50%; background:var(--teal); opacity:0.12; }}
  .cover::after {{ content:''; position:absolute; bottom:60px; left:-100px; width:300px; height:300px; border-radius:50%; background:var(--teal-light); opacity:0.07; }}
  .cover-top {{ position:relative; z-index:1; }}
  .cover-tag {{ display:inline-block; background:rgba(15,113,115,0.2); border:1px solid rgba(15,113,115,0.4); color:var(--teal-light); font-size:8pt; font-weight:600; letter-spacing:1.5px; text-transform:uppercase; padding:4px 12px; border-radius:3px; margin-bottom:32px; }}
  .cover-title {{ color:#FFFFFF; font-size:28pt; font-weight:800; line-height:1.15; margin-bottom:8px; }}
  .cover-title span {{ color:var(--teal-light); }}
  .cover-subtitle {{ color:rgba(255,255,255,0.55); font-size:12pt; font-weight:400; margin-bottom:40px; }}
  .cover-info {{ display:flex; gap:32px; flex-wrap:wrap; }}
  .cover-info-item {{ border-left:2px solid var(--teal); padding-left:12px; }}
  .cover-info-label {{ color:rgba(255,255,255,0.45); font-size:7.5pt; font-weight:600; text-transform:uppercase; letter-spacing:0.8px; margin-bottom:3px; }}
  .cover-info-value {{ color:#FFFFFF; font-size:10pt; font-weight:600; }}
  .cover-bottom {{ position:relative; z-index:1; display:flex; justify-content:space-between; align-items:flex-end; }}
  .cover-score-hero {{ text-align:right; }}
  .cover-score-label {{ color:rgba(255,255,255,0.5); font-size:8pt; font-weight:600; text-transform:uppercase; letter-spacing:1px; margin-bottom:4px; }}
  .cover-score-num {{ font-size:52pt; font-weight:800; color:var(--teal-light); line-height:1; }}
  .cover-score-max {{ color:rgba(255,255,255,0.35); font-size:14pt; font-weight:400; }}
  .cover-score-badge {{ display:inline-block; margin-top:8px; background:rgba(192,57,43,0.18); border:1px solid rgba(192,57,43,0.4); color:#ff9999; font-size:9pt; font-weight:700; padding:4px 14px; border-radius:3px; }}
  .cover-fletic {{ color:rgba(255,255,255,0.35); font-size:8pt; font-weight:600; letter-spacing:1px; text-transform:uppercase; }}

  /* INNER PAGES */
  .inner-page {{ padding:40px 48px; height:297mm; display:flex; flex-direction:column; }}
  .inner-header {{ display:flex; justify-content:space-between; align-items:center; border-bottom:2px solid var(--teal); padding-bottom:10px; margin-bottom:28px; }}
  .inner-header-title {{ font-size:8pt; font-weight:700; color:var(--teal); letter-spacing:1.5px; text-transform:uppercase; }}
  .inner-header-client {{ font-size:8pt; color:var(--text-mid); }}
  .section-header {{ display:flex; align-items:flex-start; gap:16px; margin-bottom:20px; }}
  .section-num {{ font-size:40pt; font-weight:800; color:var(--teal-light); opacity:0.3; min-width:60px; line-height:1; }}
  .section-title {{ font-size:16pt; font-weight:800; color:var(--text); padding-top:8px; }}
  .section-sub {{ font-size:9pt; color:var(--text-mid); margin-top:2px; }}

  .score-hero {{ display:flex; align-items:center; gap:32px; background:var(--gray-light); border-radius:8px; border-left:4px solid var(--teal); padding:20px 28px; margin-bottom:24px; }}
  .score-number {{ font-size:50pt; font-weight:800; color:var(--teal); line-height:1; }}
  .score-info {{ flex:1; }}
  .score-nivel-name {{ font-size:18pt; font-weight:800; color:var(--text); }}
  .score-nivel-desc {{ font-size:9pt; color:var(--text-mid); margin-top:4px; }}
  .scale-wrap {{ margin-top:12px; }}
  .scale-label-row {{ display:flex; justify-content:space-between; font-size:7.5pt; color:var(--text-light); margin-bottom:4px; }}
  .scale-track {{ background:linear-gradient(to right,#C0392B 0%,#E67E22 32%,#F1C40F 52%,#27AE60 72%,#0F7173 100%); border-radius:4px; height:10px; position:relative; }}
  .scale-marker {{ width:14px; height:14px; border-radius:50%; background:#fff; border:3px solid #1A1A2E; position:absolute; top:-2px; transform:translateX(-50%); box-shadow:0 1px 4px rgba(0,0,0,0.35); }}
  .scale-ticks {{ display:flex; justify-content:space-between; font-size:7pt; color:var(--text-light); margin-top:5px; }}
  .scale-levels {{ display:flex; justify-content:space-between; font-size:6.5pt; color:var(--text-light); margin-top:2px; }}

  .pilares-grid {{ display:grid; grid-template-columns:1fr 1fr; gap:12px; margin-bottom:16px; }}
  .pilar-card {{ background:var(--gray-light); border-radius:6px; border-left:3px solid var(--teal); padding:12px 14px; }}
  .pilar-card.critico {{ border-left-color:var(--red); }}
  .pilar-card.baixo {{ border-left-color:var(--orange); }}
  .pilar-score-row {{ display:flex; align-items:center; gap:10px; margin-bottom:6px; }}
  .pilar-score-num {{ font-size:20pt; font-weight:800; line-height:1; }}
  .pilar-nome {{ font-size:9pt; font-weight:700; color:var(--text); }}
  .pilar-peso {{ font-size:7.5pt; color:var(--text-light); }}
  .pilar-desc {{ font-size:8pt; color:var(--text-mid); line-height:1.4; border-top:1px solid var(--gray-mid); padding-top:6px; margin-top:4px; }}

  .criterios-pilar {{ margin-bottom:16px; }}
  .criterios-pilar-header {{ display:flex; align-items:center; gap:10px; margin-bottom:6px; background:var(--gray-light); padding:6px 10px; border-radius:4px; }}
  .criterios-pilar-num {{ font-size:13pt; font-weight:800; color:var(--teal-light); opacity:0.6; min-width:28px; }}
  .criterios-pilar-nome {{ font-size:9pt; font-weight:700; color:var(--text); flex:1; }}
  .score-avg {{ font-weight:800; font-size:9pt; }}
  .criterios-table {{ width:100%; border-collapse:collapse; font-size:8pt; }}
  .criterios-table th {{ text-align:left; padding:5px 8px; background:var(--navy); color:#fff; font-size:7.5pt; font-weight:700; }}
  .criterios-table td {{ padding:5px 8px; border-bottom:1px solid var(--gray-mid); vertical-align:top; }}
  .criterios-table tr:nth-child(even) td {{ background:var(--gray-light); }}
  .crit-nome {{ width:38%; font-weight:600; }}
  .crit-just {{ width:50%; color:var(--text-mid); }}
  .crit-nota {{ width:12%; text-align:center; font-weight:800; color:var(--teal); }}

  .calc-box {{ background:#E8F4F4; border:1px solid rgba(15,113,115,0.25); border-radius:6px; padding:12px 16px; margin-top:16px; font-size:8pt; }}
  .calc-box-title {{ font-weight:800; color:var(--teal-dark); margin-bottom:6px; font-size:9pt; }}
  .calc-row {{ display:flex; justify-content:space-between; margin-bottom:3px; }}
  .calc-label {{ color:var(--text-mid); }}
  .calc-val {{ font-weight:700; color:var(--text); }}

  .narrativa-block {{ background:var(--gray-light); border-left:3px solid var(--teal); border-radius:0 6px 6px 0; padding:14px 18px; margin-bottom:14px; }}
  .narrativa-block p {{ margin-bottom:8px; font-size:9pt; line-height:1.6; color:var(--text); }}
  .narrativa-block p:last-child {{ margin-bottom:0; }}
  .alerta-box {{ background:#fff8f6; border:1px solid rgba(192,57,43,0.2); border-radius:6px; padding:12px 16px; margin-bottom:14px; }}
  .alerta-box-title {{ font-weight:800; color:var(--red); font-size:9pt; margin-bottom:8px; }}
  .alerta-box ul {{ list-style:none; padding:0; }}
  .alerta-box li {{ font-size:8.5pt; color:var(--text); padding:3px 0; padding-left:18px; position:relative; }}
  .alerta-box li::before {{ content:'⚠'; position:absolute; left:0; color:var(--orange); }}
  .gap-list {{ list-style:none; padding:0; }}
  .gap-item {{ display:flex; gap:12px; padding:8px 0; border-bottom:1px solid var(--gray-mid); font-size:8.5pt; }}
  .gap-item:last-child {{ border-bottom:none; }}
  .gap-icon {{ font-size:13pt; flex-shrink:0; }}

  .footer {{ margin-top:auto; padding-top:12px; border-top:1px solid var(--gray-mid); display:flex; justify-content:space-between; align-items:center; font-size:7pt; color:var(--text-light); }}
  .footer-logo {{ font-weight:800; color:var(--teal); font-size:8pt; }}

  .roi-section {{ display:flex; gap:16px; margin-top:20px; }}
  .roi-box {{ flex:1; background:var(--gray-light); border-radius:6px; border:1px solid var(--gray-mid); padding:14px 16px; }}
  .roi-box-title {{ font-size:8pt; font-weight:700; color:var(--text-mid); text-transform:uppercase; letter-spacing:0.5px; margin-bottom:8px; }}
  .roi-number {{ font-size:22pt; font-weight:800; color:var(--teal); line-height:1; }}
  .roi-label {{ font-size:7.5pt; color:var(--text-light); margin-top:3px; }}
  .fase-block {{ background:var(--gray-light); border-radius:6px; padding:14px 18px; margin-bottom:14px; border-left:3px solid var(--teal); }}
  .fase-title {{ font-size:11pt; font-weight:800; color:var(--text); margin-bottom:4px; }}
  .fase-sub {{ font-size:8pt; color:var(--text-mid); margin-bottom:10px; }}
  .fase-mods {{ list-style:none; padding:0; }}
  .fase-mods li {{ font-size:8.5pt; padding:2px 0; color:var(--text); }}
  .fase-payment {{ display:flex; gap:10px; margin-top:10px; flex-wrap:wrap; }}
  .payment-chip {{ background:#E8F4F4; border:1px solid rgba(15,113,115,0.3); border-radius:4px; padding:4px 10px; font-size:8pt; font-weight:700; color:var(--teal-dark); }}

  @media print {{
    body {{ -webkit-print-color-adjust:exact; print-color-adjust:exact; }}
    .page {{ page-break-after:always; }}
  }}
</style>
</head>
<body>

<!-- PAGE 1: COVER -->
<div class="page cover">
  <div class="cover-top">
    <div class="cover-tag">Diagnóstico de Maturidade Digital · Confidencial</div>
    <div class="cover-title">Diagnóstico<br><span>{c['nome']}</span></div>
    <div class="cover-subtitle">Relatório Executivo de Maturidade Digital em Saúde</div>
    <div class="cover-info">{info_items}</div>
  </div>
  <div class="cover-bottom">
    <div class="cover-fletic">Fletic Vision · Saúde Digital · {c['mes_ano']}</div>
    <div class="cover-score-hero">
      <div class="cover-score-label">Índice de Maturidade</div>
      <div class="cover-score-num">{c['score_final']:.2f}<span class="cover-score-max">/5,00</span></div>
      <div class="cover-score-badge">{c['nivel']} — {c['nivel_desc']}</div>
    </div>
  </div>
</div>

<!-- PAGE 2: OVERVIEW -->
<div class="page inner-page">
  <div class="inner-header">
    <div class="inner-header-title">Fletic Vision · Diagnóstico de Maturidade</div>
    <div class="inner-header-client">{c['nome']} · {c['clinica']}</div>
  </div>
  <div class="section-header">
    <div class="section-num">01</div>
    <div>
      <div class="section-title">Resultado Global</div>
      <div class="section-sub">Score ponderado pelos 5 pilares de maturidade digital</div>
    </div>
  </div>
  <div class="score-hero">
    <div class="score-number">{c['score_final']:.2f}</div>
    <div class="score-info">
      <div class="score-nivel-name">{c['nivel']}</div>
      <div class="score-nivel-desc">{c['nivel_desc']}</div>
      <div class="scale-wrap">
        <div class="scale-label-row"><span>0,00</span><span>5,00</span></div>
        <div class="scale-track">
          <div class="scale-marker" style="left:{score_pct}%"></div>
        </div>
        <div class="scale-ticks"><span>0</span><span>1</span><span>2</span><span>3</span><span>4</span><span>5</span></div>
        <div class="scale-levels"><span>Inicial</span><span>Estruturando</span><span>Em Evolução</span><span>Avançado</span><span>Referência</span></div>
      </div>
    </div>
  </div>
  <div class="pilares-grid">{cards}</div>
  <div class="footer">
    <div class="footer-logo">FleticVision</div>
    <div>Diagnóstico de Maturidade · {c['clinica']} · Confidencial · {c['mes_ano']}</div>
    <div>Pág. 2</div>
  </div>
</div>

<!-- PAGE 3: CRITÉRIOS 1-3 -->
<div class="page inner-page">
  <div class="inner-header">
    <div class="inner-header-title">Fletic Vision · Avaliação por Critério</div>
    <div class="inner-header-client">{c['nome']} · {c['clinica']}</div>
  </div>
  <div class="section-header">
    <div class="section-num">02</div>
    <div>
      <div class="section-title">Avaliação por Critério</div>
      <div class="section-sub">30 critérios distribuídos em 5 pilares — escala 0 a 5</div>
    </div>
  </div>
  {criterios_p3}
  <div class="footer">
    <div class="footer-logo">FleticVision</div>
    <div>Diagnóstico de Maturidade · {c['clinica']} · Confidencial · {c['mes_ano']}</div>
    <div>Pág. 3</div>
  </div>
</div>

<!-- PAGE 4: CRITÉRIOS 4-5 + CALC -->
<div class="page inner-page">
  <div class="inner-header">
    <div class="inner-header-title">Fletic Vision · Avaliação por Critério</div>
    <div class="inner-header-client">{c['nome']} · {c['clinica']}</div>
  </div>
  {criterios_p4}
  <div class="calc-box">
    <div class="calc-box-title">Cálculo do Score Final Ponderado</div>
    {calc_rows}
    <div class="calc-row" style="border-top:1px solid rgba(15,113,115,0.3);margin-top:6px;padding-top:6px;">
      <span class="calc-label" style="font-weight:800;color:var(--teal-dark)">Score Final Ponderado</span>
      <span class="calc-val" style="color:var(--teal);font-size:11pt">{c['score_final']:.2f}</span>
    </div>
  </div>
  <div class="footer">
    <div class="footer-logo">FleticVision</div>
    <div>Diagnóstico de Maturidade · {c['clinica']} · Confidencial · {c['mes_ano']}</div>
    <div>Pág. 4</div>
  </div>
</div>

<!-- PAGE 5: NARRATIVA -->
<div class="page inner-page">
  <div class="inner-header">
    <div class="inner-header-title">Fletic Vision · Diagnóstico Narrativo</div>
    <div class="inner-header-client">{c['nome']} · {c['clinica']}</div>
  </div>
  <div class="section-header">
    <div class="section-num">03</div>
    <div>
      <div class="section-title">Diagnóstico Narrativo</div>
      <div class="section-sub">Leitura executiva dos resultados — gaps e oportunidades prioritárias</div>
    </div>
  </div>
  <div class="narrativa-block">{paras}</div>
  <div class="alerta-box">
    <div class="alerta-box-title">Alertas Prioritários</div>
    <ul>{alertas}</ul>
  </div>
  <div style="margin-top:14px;">
    <div style="font-size:9pt;font-weight:800;color:var(--text);margin-bottom:8px;">Gaps por Ordem de Prioridade</div>
    <ul class="gap-list">{gaps}</ul>
  </div>
  <div class="footer">
    <div class="footer-logo">FleticVision</div>
    <div>Diagnóstico de Maturidade · {c['clinica']} · Confidencial · {c['mes_ano']}</div>
    <div>Pág. 5</div>
  </div>
</div>

<!-- PAGE 6: ASSINATURA -->
<div class="page" style="background:#fff;display:flex;flex-direction:column;justify-content:space-between;">

  <!-- topo com barra navy -->
  <div style="background:var(--navy);padding:28px 36px 24px;display:flex;align-items:center;justify-content:space-between;">
    <div>
      <div style="font-size:8pt;font-weight:700;color:var(--teal);letter-spacing:2px;text-transform:uppercase;margin-bottom:6px;">FleticVision</div>
      <div style="font-size:18pt;font-weight:800;color:#fff;line-height:1.2;">Responsabilidade Técnica</div>
      <div style="font-size:9pt;color:rgba(255,255,255,0.6);margin-top:4px;">Este relatório foi elaborado pela equipe Fletic e reflete análise independente baseada nas respostas fornecidas.</div>
    </div>
    <div style="text-align:right;">
      <div style="font-size:8pt;color:rgba(255,255,255,0.5);">{c['mes_ano']}</div>
      <div style="font-size:8pt;color:rgba(255,255,255,0.5);">Confidencial</div>
    </div>
  </div>

  <!-- corpo central -->
  <div style="flex:1;padding:32px 36px;display:flex;flex-direction:column;gap:22px;">

    <!-- declaração -->
    <div style="background:#F7F8FA;border-left:4px solid var(--teal);padding:16px 20px;border-radius:0 6px 6px 0;">
      <div style="font-size:9pt;color:var(--text);line-height:1.6;">
        O diagnóstico de maturidade digital <strong>{c['clinica']}</strong> foi conduzido pela Fletic Saúde Digital
        com base em metodologia proprietária de 30 critérios distribuídos em 5 pilares estratégicos.
        As análises, pontuações e recomendações apresentadas são de responsabilidade exclusiva das profissionais
        signatárias e destinam-se ao uso interno da instituição avaliada.
      </div>
    </div>

    <!-- assinaturas -->
    <div style="display:flex;gap:32px;margin-top:8px;">

      <!-- Dani -->
      <div style="flex:1;border:1px solid #E2E8F0;border-radius:8px;padding:24px 22px;display:flex;flex-direction:column;align-items:center;text-align:center;">
        <div style="width:64px;height:64px;border-radius:50%;background:var(--teal-bg);border:2px solid var(--teal);display:flex;align-items:center;justify-content:center;margin-bottom:14px;">
          <span style="font-size:22pt;font-weight:800;color:var(--teal);">D</span>
        </div>
        <div style="font-size:12pt;font-weight:800;color:var(--navy);margin-bottom:2px;">Danielle Magalhães</div>
        <div style="font-size:8.5pt;color:var(--teal);font-weight:600;margin-bottom:4px;">CEO · Co-fundadora</div>
        <div style="font-size:8pt;color:#64748B;">Fletic Saúde Digital</div>
        <div style="width:100%;height:1px;background:#E2E8F0;margin:16px 0;"></div>
        <div style="font-size:7.5pt;color:#94A3B8;">dani.magalhaes@fletic.com.br</div>
      </div>

      <!-- Simone -->
      <div style="flex:1;border:1px solid #E2E8F0;border-radius:8px;padding:24px 22px;display:flex;flex-direction:column;align-items:center;text-align:center;">
        <div style="width:64px;height:64px;border-radius:50%;background:var(--teal-bg);border:2px solid var(--teal);display:flex;align-items:center;justify-content:center;margin-bottom:14px;">
          <span style="font-size:22pt;font-weight:800;color:var(--teal);">S</span>
        </div>
        <div style="font-size:12pt;font-weight:800;color:var(--navy);margin-bottom:2px;">Simone Farah</div>
        <div style="font-size:8.5pt;color:var(--teal);font-weight:600;margin-bottom:4px;">CMO · Co-fundadora</div>
        <div style="font-size:8pt;color:#64748B;">Fletic Saúde Digital</div>
        <div style="width:100%;height:1px;background:#E2E8F0;margin:16px 0;"></div>
        <div style="font-size:7.5pt;color:#94A3B8;">simone.farah@fletic.com.br</div>
      </div>

    </div>

    <!-- lgpd note -->
    <div style="background:#FFF8F0;border:1px solid #FDDCB0;border-radius:6px;padding:12px 16px;">
      <div style="font-size:7.5pt;color:#92400E;line-height:1.5;">
        <strong>Confidencialidade e LGPD:</strong> Este documento contém informações estratégicas e operacionais da
        {c['clinica']}. Sua reprodução, distribuição ou uso fora do contexto da relação entre as partes é
        vedada sem autorização prévia. Os dados foram tratados em conformidade com a Lei Geral de Proteção de Dados (LGPD — Lei 13.709/2018).
      </div>
    </div>

  </div>

  <!-- rodapé final -->
  <div class="footer" style="border-top:2px solid var(--navy);">
    <div class="footer-logo">FleticVision</div>
    <div>Diagnóstico de Maturidade · {c['clinica']} · Confidencial · {c['mes_ano']}</div>
    <div>Pág. 6</div>
  </div>

</div>

</body>
</html>"""
    return html


async def gerar_pdf(c):
    html = gerar_html_v2(c)
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
    print(f"PDF gerado: {c['output']}")


async def main():
    await gerar_pdf(ANA_PAULA)
    await gerar_pdf(ETHEL)
    await gerar_pdf(DANIELA_BORGES)

if __name__ == "__main__":
    asyncio.run(main())
