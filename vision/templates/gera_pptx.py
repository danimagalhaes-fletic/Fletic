#!/usr/bin/env python3
"""
Fletic Vision — Master parametric PPT proposal generator.
Usage: python3 gera_pptx.py
Generates one PPTX per client defined at the bottom.
Financial standard: 15% growth / R$24k investment / ROI 2.25x / ~5 months payback.
"""

from pptx import Presentation
from pptx.util import Inches, Pt
from pptx.dml.color import RGBColor
from pptx.enum.text import PP_ALIGN
import matplotlib
matplotlib.use('Agg')
import matplotlib.pyplot as plt
import matplotlib.patches as mpatches
import numpy as np

# ── Palette ──────────────────────────────────────────────────────────────────
TEAL      = RGBColor(0x0F, 0x71, 0x73)
TEAL_DARK = RGBColor(0x09, 0x50, 0x52)
NAVY      = RGBColor(0x1B, 0x3A, 0x5C)
TEAL_BG   = RGBColor(0xE8, 0xF4, 0xF4)
WHITE     = RGBColor(0xFF, 0xFF, 0xFF)
GRAY      = RGBColor(0x64, 0x74, 0x8B)
GRAY_BG   = RGBColor(0xF7, 0xF8, 0xFA)
GRAY_LINE = RGBColor(0xE2, 0xE8, 0xF0)
DARK      = RGBColor(0x1A, 0x1A, 0x2E)
RED       = RGBColor(0xC0, 0x39, 0x2B)
ORANGE    = RGBColor(0xD3, 0x54, 0x00)
GREEN     = RGBColor(0x1E, 0x84, 0x49)

W = Inches(10)
H = Inches(5.625)

PILAR_NAMES  = ["Estratégia & Modelo Assistencial","Operação & Jornada",
                "Tecnologia & Integração","Dados & Inteligência",
                "Modelo Econômico & Sustentabilidade"]
PILAR_LABELS = ["Estratégia &\nModelo Assistencial","Operação &\nJornada",
                "Tecnologia &\nIntegração","Dados &\nInteligência",
                "Modelo Econômico\n& Sustentabilidade"]
PILAR_PESOS  = ["25%","20%","15%","20%","20%"]
PILAR_CODES  = ["P1","P2","P3","P4","P5"]


# ── Helpers ───────────────────────────────────────────────────────────────────

def pcol(s):
    if s < 1.6:  return RED
    if s < 2.6:  return ORANGE
    if s < 3.6:  return RGBColor(0xCA, 0xA8, 0x00)
    if s < 4.6:  return GREEN
    return TEAL

def ann_col(s):
    if s < 1.6:  return '#C0392B'
    if s < 2.6:  return '#D35400'
    return '#1B3A5C'

def score_fmt(s):
    return f"{s:.2f}".replace('.', ',')

def make_prs():
    prs = Presentation()
    prs.slide_width  = W
    prs.slide_height = H
    return prs

def ns(prs):
    return prs.slides.add_slide(prs.slide_layouts[6])

def box(sl, l, t, w, h, fill=None, line=None, lw=Pt(0.75)):
    sp = sl.shapes.add_shape(1, l, t, w, h)
    sp.line.fill.background()
    if fill:
        sp.fill.solid()
        sp.fill.fore_color.rgb = fill
    else:
        sp.fill.background()
    if line:
        sp.line.color.rgb = line
        sp.line.width = lw
    return sp

def txt(sl, text, l, top, w, h, size=10, bold=False, color=None,
        align=PP_ALIGN.LEFT, italic=False):
    tb = sl.shapes.add_textbox(l, top, w, h)
    tf = tb.text_frame
    tf.word_wrap = True
    p = tf.paragraphs[0]
    p.alignment = align
    run = p.add_run()
    run.text = text
    run.font.size = Pt(size)
    run.font.bold = bold
    run.font.italic = italic
    run.font.color.rgb = color or DARK
    return tb

def rule(sl, top, l=Inches(0.3), w=None):
    box(sl, l, top, w or (W - l*2), Inches(0.018), fill=GRAY_LINE)

def footer(sl, pg, c):
    box(sl, 0, H-Inches(0.28), W, Inches(0.28), fill=GRAY_BG)
    rule(sl, H-Inches(0.28), l=0, w=W)
    txt(sl, f"FleticVision  ·  {c['clinica']}  ·  {c['especialidade']}  ·  {c['cidade']}  ·  Confidencial  ·  {c['mes_ano']}",
        Inches(0.3), H-Inches(0.25), Inches(8), Inches(0.22), size=7, color=GRAY)
    txt(sl, f"fletic.com.br  ·  {pg}",
        W-Inches(1.5), H-Inches(0.25), Inches(1.4), Inches(0.22),
        size=7, color=GRAY, align=PP_ALIGN.RIGHT)

def slide_header(sl, tag, title, subtitle=None):
    txt(sl, tag, Inches(0.3), Inches(0.18), Inches(6), Inches(0.24),
        size=8, bold=True, color=TEAL)
    box(sl, Inches(0.3), Inches(0.44), Inches(9.4), Inches(0.03), fill=TEAL)
    txt(sl, title, Inches(0.3), Inches(0.52), Inches(9.2), Inches(0.58),
        size=22, bold=True, color=NAVY)
    if subtitle:
        txt(sl, subtitle, Inches(0.3), Inches(1.1), Inches(9.2), Inches(0.28),
            size=9, color=GRAY)


# ── Spider chart ──────────────────────────────────────────────────────────────

def gerar_spider(c, path):
    scores = c["scores"]
    N = 5
    angles = [n / float(N) * 2 * np.pi for n in range(N)]
    angles += angles[:1]
    sv = scores + scores[:1]

    fig, ax = plt.subplots(figsize=(5.8, 5.8), subplot_kw=dict(polar=True))
    fig.patch.set_facecolor('white')
    ax.set_facecolor('#F7F8FA')
    ax.set_ylim(0, 5)
    ax.set_yticks([1, 2, 3, 4, 5])
    ax.set_yticklabels(['1','2','3','4','5'], fontsize=7, color='#64748B')
    ax.grid(color='#CBD5E1', linewidth=0.8, linestyle='--')

    ax.plot(angles, [5]*N+[5], color='#0F7173', linewidth=0.5, linestyle=':', alpha=0.3)
    ax.plot(angles, [2.5]*N+[2.5], color='#94A3B8', linewidth=1, linestyle='--', alpha=0.6)

    ax.fill(angles, sv, color='#0F7173', alpha=0.25)
    ax.plot(angles, sv, color='#0F7173', linewidth=2.5, marker='o',
            markersize=8, markerfacecolor='white', markeredgecolor='#0F7173', markeredgewidth=2)

    for angle, score in zip(angles[:-1], scores):
        ax.annotate(score_fmt(score), xy=(angle, score),
                    xytext=(angle, score + 0.65),
                    textcoords='data', ha='center', va='center',
                    fontsize=11, fontweight='bold', color=ann_col(score))

    ax.set_xticks(angles[:-1])
    ax.set_xticklabels(PILAR_LABELS, fontsize=8.5, color='#1B3A5C', fontweight='bold')
    ax.tick_params(pad=14)
    ax.set_title(f"Diagnóstico de Maturidade  ·  {c['clinica']}", pad=22,
                 fontsize=11, fontweight='bold', color='#1B3A5C')

    p1 = mpatches.Patch(color='#0F7173', alpha=0.4, label=c['clinica'])
    p2 = mpatches.Patch(color='#94A3B8', alpha=0.6, label='Referência de mercado (2,5)')
    ax.legend(handles=[p1, p2], loc='lower center', bbox_to_anchor=(0.5, -0.18),
              ncol=2, fontsize=8, facecolor='white', edgecolor='#E2E8F0', labelcolor='#64748B')

    ax.text(0, 0, score_fmt(c["score_final"]), ha='center', va='center',
            fontsize=16, fontweight='bold', color='#0F7173', transform=ax.transData)

    plt.tight_layout()
    plt.savefig(path, dpi=180, bbox_inches='tight', facecolor='white', edgecolor='none')
    plt.close()


# ── Main generator ────────────────────────────────────────────────────────────

def gerar_pptx(c):
    spider_path = f"/tmp/spider_{c['key']}.png"
    gerar_spider(c, spider_path)

    prs = make_prs()

    # Financial calc (15% growth, R$24k investment)
    rec    = c["receita_mensal"]
    incr   = rec * 12 * 0.15
    inv    = 24000
    roi    = incr / inv
    pb     = inv / (incr / 12)
    sf     = c["score_final"]
    sfmt   = score_fmt(sf)
    scores = c["scores"]

    # Pilar table sorted by score ascending
    pilar_sorted = sorted(enumerate(scores), key=lambda x: x[1])

    # ── SLIDE 1 — CAPA (split layout: navy left / white right) ──────────────
    s = ns(prs)
    pc_idx = c["pilar_critico_idx"]

    # Left panel — navy background (~38% width)
    lp_w = Inches(3.8)
    box(s, 0, 0, lp_w, H, fill=NAVY)
    # Teal top accent strip on left panel
    box(s, 0, 0, lp_w, Inches(0.08), fill=TEAL)
    # Teal decorative circle (bottom-right of left panel, half-visible)
    from pptx.util import Emu
    circ_size = Inches(2.2)
    box(s, lp_w - circ_size*0.55, H - circ_size*0.55, circ_size, circ_size,
        fill=RGBColor(0x09, 0x50, 0x52))  # teal_dark, no line — decorative

    # Brand tag
    txt(s, "FLETICVISION", Inches(0.28), Inches(0.24), lp_w - Inches(0.36),
        Inches(0.28), size=8, bold=True, color=TEAL)
    txt(s, "PROPOSTA COMERCIAL", Inches(0.28), Inches(0.50), lp_w - Inches(0.36),
        Inches(0.22), size=7.5, color=RGBColor(0x94, 0xA3, 0xB8))

    # Divider line
    box(s, Inches(0.28), Inches(0.80), lp_w - Inches(0.56), Inches(0.025),
        fill=RGBColor(0x2E, 0x5A, 0x8A))

    # Main title — big white
    txt(s, c["titulo_capa"], Inches(0.28), Inches(0.98), lp_w - Inches(0.36),
        Inches(2.0), size=20, bold=True, color=WHITE)

    # Client details
    txt(s, c["dra"], Inches(0.28), Inches(3.16), lp_w - Inches(0.36),
        Inches(0.32), size=9.5, bold=True, color=WHITE)
    txt(s, c["especialidade"], Inches(0.28), Inches(3.50), lp_w - Inches(0.36),
        Inches(0.26), size=8, color=RGBColor(0x94, 0xA3, 0xB8))
    txt(s, c["cidade"], Inches(0.28), Inches(3.76), lp_w - Inches(0.36),
        Inches(0.26), size=8, color=RGBColor(0x94, 0xA3, 0xB8))

    # Month/year + validity at bottom-left
    txt(s, c["mes_ano"], Inches(0.28), Inches(4.78), lp_w - Inches(0.36),
        Inches(0.22), size=8, color=RGBColor(0x64, 0x74, 0x8B))
    txt(s, "Proposta válida por 30 dias", Inches(0.28), Inches(4.99), lp_w - Inches(0.36),
        Inches(0.22), size=7.5, italic=True, color=RGBColor(0x94, 0xA3, 0xB8))

    # Right panel — white, clean (no data on cover)
    rp_l = lp_w
    rp_w = W - lp_w
    box(s, rp_l, 0, rp_w, H, fill=WHITE)
    box(s, rp_l, 0, Inches(0.04), H, fill=TEAL)

    # Tagline / positioning statement centrado
    txt(s, "Diagnóstico de Maturidade Digital", rp_l + Inches(0.32),
        Inches(0.56), rp_w - Inches(0.44), Inches(0.32), size=9, color=GRAY)
    box(s, rp_l + Inches(0.32), Inches(0.94), rp_w - Inches(0.64), Inches(0.02),
        fill=GRAY_LINE)

    # Visual statement — large centered text
    txt(s, "Transformação digital estruturada.\nResultados mensuráveis.",
        rp_l + Inches(0.32), Inches(1.18), rp_w - Inches(0.44), Inches(1.44),
        size=18, bold=True, color=NAVY)

    # Feature pillars (clean icon-less list)
    features = [
        "5 módulos  ·  2 Fases  ·  12 semanas",
        "Escopo fechado  ·  sem custo variável",
        "Entregáveis práticos desde a semana 1",
    ]
    for fi, feat in enumerate(features):
        ft = Inches(2.82) + fi * Inches(0.44)
        box(s, rp_l + Inches(0.32), ft + Inches(0.1), Inches(0.04), Inches(0.24), fill=TEAL)
        txt(s, feat, rp_l + Inches(0.48), ft + Inches(0.04), rp_w - Inches(0.6),
            Inches(0.34), size=9, color=DARK)

    box(s, rp_l + Inches(0.32), Inches(4.26), rp_w - Inches(0.64), Inches(0.02),
        fill=GRAY_LINE)

    # Signature block at bottom
    txt(s, "Danielle Magalhães  ·  Simone Farah",
        rp_l + Inches(0.32), Inches(4.38), rp_w - Inches(0.44), Inches(0.28),
        size=9, bold=True, color=NAVY)
    txt(s, "Fletic Saúde Digital  ·  contato@fletic.com.br",
        rp_l + Inches(0.32), Inches(4.66), rp_w - Inches(0.44), Inches(0.24),
        size=8, color=GRAY)

    footer(s, "1", c)

    # ── SLIDE 2 — SNAPSHOT (dados que saíram da capa) ────────────────────────
    s = ns(prs)
    box(s, 0, 0, W, H, fill=WHITE)
    slide_header(s, "VISÃO GERAL", "Resumo do Diagnóstico",
                 f"Onde {c['a_clinica']} está hoje e o que esta proposta endereça")

    # 4 metrics em faixa horizontal
    mets = [
        ("Score de Maturidade",  f"{sfmt} / 5,0",  "Nível Inicial",               TEAL),
        ("Pilar Crítico",        PILAR_CODES[pc_idx] + " — " + PILAR_NAMES[pc_idx].split(" &")[0],
         f"Score {score_fmt(scores[pc_idx])}",                                     RED),
        ("Faturamento mensal",   f"até R$ {rec:,}".replace(",","."), "referência", TEAL),
        ("Payback projetado",    f"~{pb:.0f} meses", "estimativa conservadora",    TEAL),
    ]
    mw4 = (W - Inches(0.6) - Inches(0.36)) / 4
    mh4 = Inches(1.36)
    for i, (lab, val, sub, col) in enumerate(mets):
        ml4 = Inches(0.3) + i * (mw4 + Inches(0.12))
        mt4 = Inches(1.38)
        box(s, ml4, mt4, mw4, mh4, fill=GRAY_BG)
        box(s, ml4, mt4, Inches(0.04), mh4, fill=col)
        txt(s, lab, ml4+Inches(0.14), mt4+Inches(0.1),  mw4-Inches(0.18), Inches(0.26), size=7.5, color=GRAY)
        txt(s, val, ml4+Inches(0.14), mt4+Inches(0.38), mw4-Inches(0.18), Inches(0.56), size=14, bold=True, color=col)
        txt(s, sub, ml4+Inches(0.14), mt4+Inches(0.98), mw4-Inches(0.18), Inches(0.24), size=7.5, color=GRAY)

    rule(s, Inches(2.92))

    # Teaser block
    box(s, Inches(0.3), Inches(3.04), Inches(9.4), Inches(1.1), fill=TEAL_BG)
    box(s, Inches(0.3), Inches(3.04), Inches(0.04), Inches(1.1), fill=TEAL)
    txt(s, c["teaser_text"], Inches(0.44), Inches(3.14), Inches(9.1), Inches(0.9),
        size=9, color=NAVY)

    # Estrutura resumo
    txt(s, "Estrutura da proposta:", Inches(0.3), Inches(4.26),
        Inches(2.2), Inches(0.26), size=8, bold=True, color=NAVY)
    txt(s, "Fase 1 (4 semanas)  ·  Fase 2 (8 semanas)  ·  5 módulos  ·  Investimento total R$ 24.000",
        Inches(0.3), Inches(4.54), Inches(9.4), Inches(0.24), size=8.5, color=GRAY)

    footer(s, "2", c)

    # ── SLIDE 3 — DIAGNÓSTICO ────────────────────────────────────────────────
    s = ns(prs)
    box(s, 0, 0, W, H, fill=WHITE)
    slide_header(s, "DIAGNÓSTICO", "Diagnóstico Atual",
                 f"Onde {c['a_clinica']} está hoje — pontos de atenção estrutural")

    cw = Inches(4.5)
    for i, (num, titulo, desc, cor) in enumerate(c["gaps"]):
        col = i % 2; row = i // 2
        gl = Inches(0.3) + col * (cw + Inches(0.2))
        gt = Inches(1.45) + row * Inches(1.68)
        box(s, gl, gt, cw, Inches(1.55), fill=GRAY_BG)
        box(s, gl, gt, Inches(0.06), Inches(1.55), fill=cor)
        txt(s, num,    gl+Inches(0.18), gt+Inches(0.1),  Inches(0.4), Inches(0.32), size=13, bold=True, color=cor)
        txt(s, titulo, gl+Inches(0.18), gt+Inches(0.44), cw-Inches(0.28), Inches(0.34), size=10, bold=True, color=NAVY)
        txt(s, desc,   gl+Inches(0.18), gt+Inches(0.82), cw-Inches(0.28), Inches(0.62), size=8.5, color=GRAY)

    box(s, Inches(0.3), H-Inches(0.74), Inches(9.4), Inches(0.44), fill=TEAL_BG)
    box(s, Inches(0.3), H-Inches(0.74), Inches(0.04), Inches(0.44), fill=TEAL)
    txt(s, "Score de Maturidade Digital: ", Inches(0.44), H-Inches(0.7), Inches(2.2), Inches(0.3), size=8, color=GRAY)
    txt(s, f"{sfmt} / 5,0  ·  Nível INICIAL", Inches(2.4), H-Inches(0.72), Inches(3), Inches(0.32),
        size=10, bold=True, color=TEAL)
    txt(s, f"Pilar mais crítico: {PILAR_NAMES[pc_idx]}  {score_fmt(scores[pc_idx])}/5",
        Inches(5.8), H-Inches(0.72), Inches(3.8), Inches(0.3),
        size=8.5, bold=True, color=RED, align=PP_ALIGN.RIGHT)
    footer(s, "3", c)

    # ── SLIDE 4 — SPIDER ─────────────────────────────────────────────────────
    s = ns(prs)
    box(s, 0, 0, W, H, fill=WHITE)
    slide_header(s, "MATURIDADE", "Score de Maturidade por Pilar",
                 f"{c['clinica']}  ·  Score final ponderado {sfmt} / 5,0  ·  Nível INICIAL")

    s.shapes.add_picture(spider_path, Inches(0.2), Inches(1.1), Inches(5.0), Inches(4.1))

    tl = Inches(5.4); tt = Inches(1.22); rh = Inches(0.54); tw = Inches(4.28)
    box(s, tl, tt, tw, Inches(0.36), fill=NAVY)
    txt(s, "Pilar",      tl+Inches(0.1), tt+Inches(0.07), Inches(2.0), Inches(0.22), size=8, bold=True, color=WHITE)
    txt(s, "Peso",       tl+Inches(2.2), tt+Inches(0.07), Inches(0.6), Inches(0.22), size=8, bold=True, color=WHITE, align=PP_ALIGN.CENTER)
    txt(s, "Score / 5,0",tl+Inches(2.9), tt+Inches(0.07), Inches(1.2), Inches(0.22), size=8, bold=True, color=WHITE, align=PP_ALIGN.CENTER)

    for row_i, (pi, sc) in enumerate(pilar_sorted):
        rt  = tt + Inches(0.36) + row_i * rh
        bg  = WHITE if row_i % 2 == 0 else GRAY_BG
        cor = pcol(sc)
        box(s, tl, rt, tw, rh-Inches(0.04), fill=bg, line=GRAY_LINE, lw=Pt(0.5))
        bw = tw * (sc / 5.0)
        box(s, tl, rt+rh-Inches(0.1), bw, Inches(0.06), fill=cor)
        txt(s, PILAR_CODES[pi],  tl+Inches(0.1),  rt+Inches(0.08), Inches(0.32), Inches(0.28), size=8, bold=True, color=cor)
        txt(s, PILAR_NAMES[pi],  tl+Inches(0.44), rt+Inches(0.06), Inches(1.72), Inches(0.38), size=8, color=NAVY)
        txt(s, PILAR_PESOS[pi],  tl+Inches(2.2),  rt+Inches(0.12), Inches(0.6),  Inches(0.28), size=8, color=GRAY, align=PP_ALIGN.CENTER)
        txt(s, score_fmt(sc),    tl+Inches(2.9),  rt+Inches(0.06), Inches(1.2),  Inches(0.36), size=16, bold=True, color=cor, align=PP_ALIGN.CENTER)

    box(s, tl, tt+Inches(3.06), tw, Inches(0.46), fill=TEAL)
    txt(s, "SCORE FINAL PONDERADO", tl+Inches(0.1), tt+Inches(3.12), Inches(2.2), Inches(0.28), size=8, bold=True, color=WHITE)
    txt(s, f"{sfmt} / 5,0", tl+Inches(2.5), tt+Inches(3.08), Inches(1.6), Inches(0.36), size=16, bold=True, color=WHITE, align=PP_ALIGN.RIGHT)
    box(s, tl, tt+Inches(3.58), tw, Inches(0.34), fill=TEAL_BG)
    txt(s, "Nível INICIAL — Operação artesanal, sem estrutura digital relevante",
        tl+Inches(0.1), tt+Inches(3.62), tw-Inches(0.15), Inches(0.26), size=8, color=NAVY)
    footer(s, "4", c)

    # ── SLIDE 5 — MODELO ATUAL vs ESTRUTURADO ────────────────────────────────
    s = ns(prs)
    box(s, 0, 0, W, H, fill=WHITE)
    slide_header(s, "VISÃO", "Modelo Atual vs. Modelo Estruturado",
                 "A mudança de lógica que a Fletic Vision viabiliza")

    cw2 = Inches(4.3); ct = Inches(1.45); ch2 = Inches(3.76)
    box(s, Inches(0.3), ct, cw2, ch2, fill=WHITE, line=GRAY_LINE, lw=Pt(1))
    box(s, Inches(0.3), ct, cw2, Inches(0.04), fill=RED)
    txt(s, "MODELO ATUAL", Inches(0.44), ct+Inches(0.12), cw2-Inches(0.18), Inches(0.26), size=8, bold=True, color=RED)
    for j, item in enumerate(c["modelo_atual"]):
        jt = ct + Inches(0.5) + j*Inches(0.5)
        txt(s, "✗", Inches(0.44), jt, Inches(0.28), Inches(0.38), size=10, bold=True, color=RED)
        txt(s, item, Inches(0.74), jt, cw2-Inches(0.56), Inches(0.36), size=9, color=DARK)

    box(s, Inches(4.78), Inches(2.9), Inches(0.8), Inches(0.5), fill=TEAL)
    txt(s, "Fletic\nVision", Inches(4.78), Inches(2.92), Inches(0.8), Inches(0.46),
        size=7, bold=True, color=WHITE, align=PP_ALIGN.CENTER)

    rl = Inches(5.7)
    box(s, rl, ct, cw2, ch2, fill=TEAL_BG, line=TEAL, lw=Pt(1))
    box(s, rl, ct, cw2, Inches(0.04), fill=TEAL)
    txt(s, "MODELO ESTRUTURADO", rl+Inches(0.14), ct+Inches(0.12), cw2-Inches(0.18), Inches(0.26), size=8, bold=True, color=TEAL)
    for j, item in enumerate(c["modelo_estruturado"]):
        jt = ct + Inches(0.5) + j*Inches(0.5)
        txt(s, "✔", rl+Inches(0.14), jt, Inches(0.28), Inches(0.38), size=10, bold=True, color=TEAL)
        txt(s, item, rl+Inches(0.44), jt, cw2-Inches(0.56), Inches(0.36), size=9, color=NAVY)

    box(s, Inches(0.3), H-Inches(0.62), Inches(9.4), Inches(0.3), fill=TEAL_BG)
    txt(s, c["resultado_line"], Inches(0.44), H-Inches(0.6), Inches(9.1), Inches(0.26), size=8, color=NAVY)
    footer(s, "5", c)

    # ── SLIDE 5 — O QUE SERÁ CONSTRUÍDO ──────────────────────────────────────
    s = ns(prs)
    box(s, 0, 0, W, H, fill=WHITE)
    slide_header(s, "ENTREGA", "O Que Será Construído",
                 "Cinco dimensões de transformação — entregáveis concretos e mensuráveis")

    mw3 = Inches(1.84)
    modulos_resumo = [
        ("FASE 1","01","Arquitetura\nAssistencial", c["m01_resumo"], TEAL),
        ("FASE 1","02","Estrutura\nOperacional",    c["m02_resumo"], TEAL),
        ("FASE 2","03","Modelo\nEconômico",         c["m03_resumo"], NAVY),
        ("FASE 2","04","Arquitetura\nTecnológica",  c["m04_resumo"], NAVY),
        ("FASE 2","05","Gestão por\nIndicadores",   c["m05_resumo"], NAVY),
    ]
    for i, (fase, num, titulo, itens, cor) in enumerate(modulos_resumo):
        ml = Inches(0.18) + i*(mw3+Inches(0.075))
        mt = Inches(1.32); mh = Inches(3.86)
        box(s, ml, mt, mw3, mh, fill=GRAY_BG, line=GRAY_LINE, lw=Pt(0.5))
        box(s, ml, mt, mw3, Inches(0.22), fill=cor)
        txt(s, fase,   ml+Inches(0.1), mt+Inches(0.03), mw3, Inches(0.16), size=7, bold=True, color=WHITE)
        txt(s, num,    ml+Inches(0.1), mt+Inches(0.28), mw3, Inches(0.44), size=14, bold=True, color=cor)
        txt(s, titulo, ml+Inches(0.1), mt+Inches(0.72), mw3-Inches(0.12), Inches(0.52), size=10, bold=True, color=NAVY)
        box(s, ml+Inches(0.1), mt+Inches(1.3), mw3-Inches(0.2), Inches(0.02), fill=GRAY_LINE)
        for j, item in enumerate(itens):
            it = mt+Inches(1.42)+j*Inches(0.54)
            txt(s, "▸", ml+Inches(0.1), it, Inches(0.22), Inches(0.4), size=8, bold=True, color=cor)
            txt(s, item, ml+Inches(0.3), it, mw3-Inches(0.4), Inches(0.4), size=8, color=GRAY)
    footer(s, "6", c)

    # ── SLIDE 6 — CRONOGRAMA ─────────────────────────────────────────────────
    s = ns(prs)
    box(s, 0, 0, W, H, fill=WHITE)
    slide_header(s, "CRONOGRAMA", "Cronograma — 12 Semanas (Fases 1 e 2)",
                 "Fase 1 começa imediatamente após assinatura  ·  Fase 2 inicia na semana 5")

    gl = Inches(0.2); mcolw = Inches(2.35); gt = Inches(1.38)
    nsem = 12
    sw = (W - gl - mcolw - Inches(0.15)) / nsem
    rh2 = Inches(0.52)

    box(s, gl, gt, mcolw, Inches(0.4), fill=NAVY)
    txt(s, "Módulo", gl+Inches(0.1), gt+Inches(0.1), mcolw, Inches(0.24), size=8, bold=True, color=WHITE)
    box(s, gl+mcolw, gt, sw*4, Inches(0.4), fill=TEAL)
    txt(s, "FASE 1  ·  Sem. 1–4", gl+mcolw+Inches(0.1), gt+Inches(0.1), sw*4, Inches(0.24), size=8, bold=True, color=WHITE)
    box(s, gl+mcolw+sw*4, gt, sw*8, Inches(0.4), fill=NAVY)
    txt(s, "FASE 2  ·  Sem. 5–12", gl+mcolw+sw*4+Inches(0.1), gt+Inches(0.1), sw*8, Inches(0.24), size=8, bold=True, color=WHITE)

    for k in range(nsem):
        sl2 = gl+mcolw+k*sw
        bg = TEAL_BG if k < 4 else GRAY_BG
        box(s, sl2, gt+Inches(0.4), sw, Inches(0.26), fill=bg)
        txt(s, f"S{k+1}", sl2, gt+Inches(0.42), sw, Inches(0.22), size=7,
            bold=(k<4), color=TEAL if k<4 else NAVY, align=PP_ALIGN.CENTER)

    gantt = [
        ("01 — Arquitetura Assistencial", 0, 2),
        ("02 — Estrutura Operacional",    2, 4),
        ("03 — Modelo Econômico",         4, 6),
        ("04 — Arquitetura Tecnológica",  6, 10),
        ("05 — Gestão por Indicadores",   10, 12),
    ]
    for j, (nome, s1, s2) in enumerate(gantt):
        rt  = gt + Inches(0.66) + j*rh2
        bg  = WHITE if j % 2 == 0 else GRAY_BG
        box(s, gl, rt, mcolw, rh2-Inches(0.04), fill=bg, line=GRAY_LINE, lw=Pt(0.5))
        txt(s, nome, gl+Inches(0.1), rt+Inches(0.12), mcolw-Inches(0.12), Inches(0.28), size=8.5, color=NAVY)
        for k in range(nsem):
            sl2 = gl+mcolw+k*sw
            cbg = GRAY_BG if bg == WHITE else WHITE
            box(s, sl2, rt, sw, rh2-Inches(0.04), fill=cbg, line=GRAY_LINE, lw=Pt(0.3))
        bcol = TEAL if s2 <= 4 else NAVY
        bl   = gl+mcolw+s1*sw+Inches(0.05)
        bw2  = (s2-s1)*sw-Inches(0.1)
        box(s, bl, rt+Inches(0.12), bw2, Inches(0.26), fill=bcol)
        txt(s, f"Sem {s1+1}–{s2}", bl+Inches(0.06), rt+Inches(0.14), bw2, Inches(0.22),
            size=7.5, bold=True, color=WHITE)

    box(s, gl, H-Inches(0.66), W-gl*2, Inches(0.28), fill=TEAL_BG)
    txt(s, "▸  Programa de Acompanhamento & Escala: conversa que acontece ao final da Fase 2 — para clínicas que queiram continuar evoluindo.",
        gl+Inches(0.1), H-Inches(0.64), W-gl*2-Inches(0.15), Inches(0.26), size=8, color=TEAL)
    footer(s, "7", c)

    # ── SLIDE 7 — FASE 1 DETALHE ─────────────────────────────────────────────
    s = ns(prs)
    box(s, 0, 0, W, H, fill=WHITE)
    slide_header(s, "FASE 1", "FASE 1 — Fundação Operacional",
                 "Módulos 01 e 02  ·  4 semanas  ·  Base operacional com qualidade e previsibilidade")

    cw3 = Inches(4.55); ct3 = Inches(1.46); ch3 = Inches(3.6)
    for i, (num, titulo, subtitulo, itens) in enumerate([
        ("01", "Arquitetura Assistencial", "Definir o modelo de cuidado", c["m01_items"]),
        ("02", "Estrutura Operacional",    "Transformar o modelo em operação real", c["m02_items"]),
    ]):
        ml = Inches(0.3) + i*(cw3+Inches(0.2))
        box(s, ml, ct3, cw3, ch3, fill=GRAY_BG, line=GRAY_LINE, lw=Pt(0.5))
        box(s, ml, ct3, cw3, Inches(0.04), fill=TEAL)
        txt(s, num,       ml+Inches(0.15), ct3+Inches(0.1),  cw3,         Inches(0.44), size=14, bold=True, color=TEAL)
        txt(s, titulo,    ml+Inches(0.15), ct3+Inches(0.54), cw3-Inches(0.2), Inches(0.34), size=13, bold=True, color=NAVY)
        txt(s, subtitulo, ml+Inches(0.15), ct3+Inches(0.9),  cw3-Inches(0.2), Inches(0.24), size=8, italic=True, color=GRAY)
        box(s, ml+Inches(0.15), ct3+Inches(1.2), cw3-Inches(0.3), Inches(0.02), fill=GRAY_LINE)
        for j, item in enumerate(itens):
            jt = ct3+Inches(1.32)+j*Inches(0.44)
            txt(s, "▸", ml+Inches(0.15), jt, Inches(0.22), Inches(0.38), size=9, bold=True, color=TEAL)
            txt(s, item, ml+Inches(0.38), jt, cw3-Inches(0.48), Inches(0.38), size=8.5, color=DARK)
    footer(s, "8", c)

    # ── SLIDE 8 — FASE 2 DETALHE ─────────────────────────────────────────────
    s = ns(prs)
    box(s, 0, 0, W, H, fill=WHITE)
    slide_header(s, "FASE 2", "FASE 2 — Crescimento Sustentável",
                 "Módulos 03, 04 e 05  ·  8 semanas adicionais  ·  Monetização, tecnologia e inteligência de gestão")

    mw4 = Inches(3.0)
    for i, (num, titulo, subtitulo, itens) in enumerate([
        ("03", "Modelo Econômico",      "Estruturar crescimento sustentável",      c["m03_items"]),
        ("04", "Arquitetura Tecnológica","Suportar o modelo com eficiência",       c["m04_items"]),
        ("05", "Gestão por Indicadores","Garantir controle e evolução contínua",   c["m05_items"]),
    ]):
        ml = Inches(0.2) + i*(mw4+Inches(0.12))
        mt4 = Inches(1.46); mh4 = Inches(3.72)
        box(s, ml, mt4, mw4, mh4, fill=GRAY_BG, line=GRAY_LINE, lw=Pt(0.5))
        box(s, ml, mt4, mw4, Inches(0.04), fill=NAVY)
        txt(s, num,       ml+Inches(0.15), mt4+Inches(0.1),  mw4,         Inches(0.44), size=13, bold=True, color=NAVY)
        txt(s, titulo,    ml+Inches(0.15), mt4+Inches(0.54), mw4-Inches(0.2), Inches(0.34), size=12, bold=True, color=NAVY)
        txt(s, subtitulo, ml+Inches(0.15), mt4+Inches(0.9),  mw4-Inches(0.2), Inches(0.24), size=8, italic=True, color=GRAY)
        box(s, ml+Inches(0.15), mt4+Inches(1.2), mw4-Inches(0.3), Inches(0.02), fill=GRAY_LINE)
        for j, item in enumerate(itens):
            jt = mt4+Inches(1.32)+j*Inches(0.46)
            txt(s, "▸", ml+Inches(0.15), jt, Inches(0.22), Inches(0.4), size=9, bold=True, color=NAVY)
            txt(s, item, ml+Inches(0.38), jt, mw4-Inches(0.48), Inches(0.4), size=8.5, color=DARK)
    footer(s, "9", c)

    # ── SLIDE 9 — ESTRUTURA GERAL ────────────────────────────────────────────
    s = ns(prs)
    box(s, 0, 0, W, H, fill=WHITE)
    slide_header(s, "ESTRUTURA", "Duas Fases. Uma Transformação.",
                 "Modelo Fixo — escopo e custo totalmente definidos desde o início  ·  12 semanas")

    fw = Inches(4.55)
    fases_data = [
        ("FASE 1","Fundação\nOperacional","4 semanas","Módulos 01 e 02",
         ["Arquitetura Assistencial","Estrutura Operacional",
          "Jornada do paciente documentada","Protocolos e comunicação padronizados"],
         "R$ 8.000","pagamento no início da Fase 1", TEAL),
        ("FASE 2","Crescimento\nSustentável","8 semanas","Módulos 03, 04 e 05",
         ["Modelo Econômico & recorrência","Arquitetura Tecnológica",
          "Gestão por Indicadores","ROI do digital calculado"],
         "R$ 16.000","pagamento na conclusão da Fase 2", NAVY),
    ]
    for i, (fase, titulo3, prazo, mods2, itens2, valor, nota, cor) in enumerate(fases_data):
        fl = Inches(0.3)+i*(fw+Inches(0.1))
        ft = Inches(1.38); fh = Inches(3.88)
        box(s, fl, ft, fw, fh, fill=GRAY_BG, line=GRAY_LINE, lw=Pt(0.5))
        box(s, fl, ft, fw, Inches(0.28), fill=cor)
        txt(s, fase,   fl+Inches(0.14), ft+Inches(0.04), fw, Inches(0.2), size=7.5, bold=True, color=WHITE)
        txt(s, titulo3,fl+Inches(0.14), ft+Inches(0.36), fw-Inches(0.18), Inches(0.52), size=16, bold=True, color=NAVY)
        txt(s, f"⏱  {prazo}  ·  {mods2}", fl+Inches(0.14), ft+Inches(0.94), fw-Inches(0.18), Inches(0.24), size=8, color=GRAY)
        box(s, fl+Inches(0.14), ft+Inches(1.24), fw-Inches(0.28), Inches(0.02), fill=GRAY_LINE)
        for j, item in enumerate(itens2):
            jt = ft+Inches(1.36)+j*Inches(0.36)
            txt(s, "▸", fl+Inches(0.14), jt, Inches(0.22), Inches(0.3), size=8, bold=True, color=cor)
            txt(s, item, fl+Inches(0.34), jt, fw-Inches(0.44), Inches(0.3), size=8.5, color=DARK)
        box(s, fl+Inches(0.14), ft+Inches(2.82), fw-Inches(0.28), Inches(0.02), fill=GRAY_LINE)
        txt(s, valor, fl+Inches(0.14), ft+Inches(2.94), fw-Inches(0.18), Inches(0.5), size=15, bold=True, color=cor)
        txt(s, nota,  fl+Inches(0.14), ft+Inches(3.46), fw-Inches(0.18), Inches(0.3), size=7.5, color=GRAY, italic=True)
    footer(s, "10", c)

    # ── SLIDE 10 — IMPACTO FINANCEIRO ────────────────────────────────────────
    s = ns(prs)
    box(s, 0, 0, W, H, fill=WHITE)
    slide_header(s, "IMPACTO", "Impacto Financeiro",
                 f"Estimativa conservadora — base {c['faturamento_mensal']}/mês  ·  crescimento de 15% ao ano")

    mets2 = [
        ("Receita atual/mês",    c["faturamento_mensal"], "base de referência",      NAVY),
        ("Receita anual atual",  f"até R$ {rec*12:,}".replace(",","."), "referência 12 meses", NAVY),
        ("Incremento projetado", f"+R$ {incr:,.0f}".replace(",","."), "crescimento de 15%/ano", TEAL),
        ("Payback estimado",     f"~{pb:.0f} meses",    "do início do projeto",     TEAL),
    ]
    mw5 = Inches(2.22)
    for i, (lab, val, sub, cor) in enumerate(mets2):
        ml = Inches(0.3)+i*(mw5+Inches(0.1))
        box(s, ml, Inches(1.38), mw5, Inches(1.36), fill=GRAY_BG, line=GRAY_LINE, lw=Pt(0.5))
        txt(s, lab, ml+Inches(0.14), Inches(1.46), mw5-Inches(0.2), Inches(0.26), size=8, color=GRAY)
        txt(s, val, ml+Inches(0.14), Inches(1.74), mw5-Inches(0.2), Inches(0.64), size=18, bold=True, color=cor)
        txt(s, sub, ml+Inches(0.14), Inches(2.4),  mw5-Inches(0.2), Inches(0.22), size=7.5, color=GRAY)

    box(s, Inches(0.3), Inches(2.9), Inches(9.4), Inches(1.22), fill=TEAL_BG, line=TEAL, lw=Pt(1))
    box(s, Inches(0.3), Inches(2.9), Inches(0.04), Inches(1.22), fill=TEAL)
    txt(s, "Retorno sobre Investimento — Fases 1 e 2", Inches(0.46), Inches(2.98),
        Inches(4), Inches(0.3), size=10, bold=True, color=NAVY)
    txt(s, f"ROI ∼ {roi:.2f}×".replace(".",","), Inches(0.46), Inches(3.3),
        Inches(2.2), Inches(0.6), size=22, bold=True, color=TEAL)

    roi_str = f"{roi:.2f}×".replace(".",",")
    for k, (lab2, val2) in enumerate([
        ("Investimento F1+F2", f"R$ {inv:,}".replace(",",".")),
        ("Incremento ano 1",   f"R$ {incr:,.0f}".replace(",",".")),
        ("Múltiplo de retorno", roi_str),
        ("Payback estimado",   f"~{pb:.0f} meses"),
    ]):
        kl = Inches(3.2)+k*Inches(1.56)
        txt(s, lab2, kl, Inches(3.02), Inches(1.5), Inches(0.26), size=7.5, color=GRAY)
        txt(s, val2, kl, Inches(3.3),  Inches(1.5), Inches(0.38), size=11, bold=True, color=NAVY)

    box(s, Inches(0.3), Inches(4.26), Inches(9.4), Inches(0.56), fill=WHITE, line=GRAY_LINE, lw=Pt(0.75))
    txt(s, "⚠  Premissas conservadoras:", Inches(0.44), Inches(4.32), Inches(2.2), Inches(0.24),
        size=8.5, bold=True, color=NAVY)
    txt(s, c["premissas_text"], Inches(0.44), Inches(4.56), Inches(9.1), Inches(0.22), size=7.5, color=GRAY)
    footer(s, "11", c)

    # ── SLIDE 11 — MODELO COMERCIAL ──────────────────────────────────────────
    s = ns(prs)
    box(s, 0, 0, W, H, fill=WHITE)
    slide_header(s, "MODELO COMERCIAL", "Investimento. Resultado. Sem Surpresas.",
                 "Modelo Fixo — escopo e custo totalmente definidos desde o início")

    ll = Inches(0.3); lw = Inches(5.3)
    ot2 = Inches(1.38); oh2 = Inches(3.88)
    box(s, ll, ot2, lw, oh2, fill=WHITE, line=GRAY_LINE, lw=Pt(1))
    box(s, ll, ot2, lw, Inches(0.04), fill=TEAL)
    txt(s, "MODELO FIXO", ll+Inches(0.2), ot2+Inches(0.12), lw, Inches(0.24), size=8, bold=True, color=TEAL)
    txt(s, "Previsibilidade total para as duas partes.",
        ll+Inches(0.2), ot2+Inches(0.4), lw-Inches(0.3), Inches(0.26), size=9, color=GRAY)

    txt(s, "R$ 8.000", ll+Inches(0.2), ot2+Inches(0.76), lw-Inches(0.3), Inches(0.52),
        size=26, bold=True, color=TEAL)
    txt(s, "entrada — Fase 1 — início imediato",
        ll+Inches(0.2), ot2+Inches(1.3), lw-Inches(0.3), Inches(0.26), size=8.5, color=GRAY)

    txt(s, "+ R$ 16.000", ll+Inches(0.2), ot2+Inches(1.62), lw-Inches(0.3), Inches(0.44),
        size=18, bold=True, color=NAVY)
    txt(s, "na conclusão da Fase 2",
        ll+Inches(0.2), ot2+Inches(2.08), lw-Inches(0.3), Inches(0.26), size=8.5, color=GRAY)

    box(s, ll+Inches(0.2), ot2+Inches(2.44), lw-Inches(0.4), Inches(0.02), fill=GRAY_LINE)
    txt(s, "Total: R$ 24.000  ·  5 módulos  ·  12 semanas",
        ll+Inches(0.2), ot2+Inches(2.54), lw-Inches(0.3), Inches(0.3),
        size=11, bold=True, color=TEAL)

    box(s, ll+Inches(0.2), ot2+Inches(3.0), lw-Inches(0.4), Inches(0.72), fill=TEAL_BG)
    box(s, ll+Inches(0.2), ot2+Inches(3.0), Inches(0.04), Inches(0.72), fill=TEAL)
    txt(s, f"ROI projetado: {roi_str}  ·  Payback: ~{pb:.0f} meses\n"
           f"Crescimento de 15% na receita anual já cobre o investimento total.",
        ll+Inches(0.34), ot2+Inches(3.08), lw-Inches(0.56), Inches(0.58), size=8.5, color=NAVY)

    rl2 = Inches(5.8); rw = Inches(3.88)
    box(s, rl2, ot2, rw, oh2, fill=GRAY_BG, line=GRAY_LINE, lw=Pt(0.5))
    box(s, rl2, ot2, rw, Inches(0.04), fill=NAVY)
    txt(s, "O QUE ESTÁ INCLUÍDO", rl2+Inches(0.16), ot2+Inches(0.12), rw, Inches(0.22),
        size=7.5, bold=True, color=NAVY)
    for j2, item2 in enumerate([
        "5 módulos completos e documentados",
        "12 semanas de projeto estruturado",
        "Entregáveis práticos: protocolos e dashboards",
        "Reuniões semanais de acompanhamento",
        "Crescimento 100% da clínica — sem taxa sobre receita",
        "Acesso ao Programa de Acompanhamento pós-projeto",
    ]):
        jt2 = ot2 + Inches(0.46) + j2 * Inches(0.52)
        txt(s, "✔", rl2+Inches(0.16), jt2, Inches(0.24), Inches(0.38), size=9, bold=True, color=TEAL)
        txt(s, item2, rl2+Inches(0.42), jt2, rw-Inches(0.54), Inches(0.38), size=8.5, color=DARK)
    footer(s, "12", c)

    # ── SLIDE 12 — PRÓXIMOS PASSOS ────────────────────────────────────────────
    s = ns(prs)
    box(s, 0, 0, W, H, fill=WHITE)
    box(s, 0, 0, W, Inches(0.06), fill=TEAL)
    txt(s, "FLETICVISION  ·  PRÓXIMOS PASSOS", Inches(0.3), Inches(0.22),
        Inches(7), Inches(0.28), size=8, bold=True, color=TEAL)
    rule(s, Inches(0.54), l=Inches(0.3), w=Inches(9.4))
    txt(s, "Próximos Passos", Inches(0.3), Inches(0.64), Inches(9), Inches(0.56),
        size=22, bold=True, color=NAVY)
    txt(s, c["fecho_line"], Inches(0.3), Inches(1.22), Inches(9), Inches(0.3), size=10, color=GRAY)

    passos = [
        ("Esta semana",     "Validar o diagnóstico",
         "Confirmar se os dados e análises refletem a realidade da clínica. Ajustar qualquer ponto que não faça sentido."),
        ("Próximos 7 dias", "Reunião de alinhamento",
         "Definir escopo detalhado e data de início da Fase 1."),
        ("Dentro de 10 dias","Contrato e kickoff",
         "Assinatura do contrato, pagamento da entrada e início imediato da Fase 1."),
    ]
    for j, (prazo, titulo4, desc3) in enumerate(passos):
        pt = Inches(1.72)+j*Inches(1.06)
        rule(s, pt-Inches(0.06), l=Inches(0.3), w=Inches(9.4))
        txt(s, prazo,   Inches(0.3),  pt+Inches(0.04), Inches(1.4), Inches(0.28), size=8.5, bold=True, color=TEAL)
        txt(s, titulo4, Inches(1.82), pt+Inches(0.04), Inches(7.5), Inches(0.3),  size=11, bold=True, color=NAVY)
        txt(s, desc3,   Inches(1.82), pt+Inches(0.36), Inches(7.5), Inches(0.52), size=8.5, color=GRAY)

    rule(s, Inches(4.62), l=Inches(0.3), w=Inches(9.4))
    box(s, Inches(0.3), Inches(4.72), Inches(9.4), Inches(0.3), fill=TEAL_BG)
    box(s, Inches(0.3), Inches(4.72), Inches(0.04), Inches(0.3), fill=TEAL)
    txt(s, "Clínicas que concluem as Fases 1 e 2 têm acesso ao Programa de Acompanhamento & Escala da Fletic — "
           "acompanhamento estratégico contínuo para sustentar os resultados. Essa conversa acontece ao final da Fase 2.",
        Inches(0.42), Inches(4.76), Inches(9.1), Inches(0.24), size=8, italic=True, color=TEAL_DARK)

    box(s, Inches(0.3), Inches(5.1), Inches(5.5), Inches(0.34), fill=TEAL_BG)
    txt(s, c["fecho_line"], Inches(0.42), Inches(5.14), Inches(5.2), Inches(0.26),
        size=8.5, bold=True, color=NAVY)
    txt(s, "Dani Magalhães  ·  Simone Farah", Inches(6.1), Inches(5.12),
        Inches(3.5), Inches(0.24), size=9, bold=True, color=NAVY, align=PP_ALIGN.RIGHT)
    txt(s, "contato@fletic.com.br  ·  Proposta válida por 30 dias", Inches(6.1), Inches(5.34),
        Inches(3.5), Inches(0.22), size=8, color=GRAY, align=PP_ALIGN.RIGHT)
    footer(s, "13", c)

    # ── SLIDE 13 — PROGRAMA DE ACOMPANHAMENTO & ESCALA (cross-sell) ──────────
    s = ns(prs)
    box(s, 0, 0, W, H, fill=WHITE)
    # Dark navy top band
    box(s, 0, 0, W, Inches(1.52), fill=NAVY)
    box(s, 0, 0, W, Inches(0.06), fill=TEAL)
    txt(s, "FLETICVISION  ·  DEPOIS DO PROJETO", Inches(0.3), Inches(0.18),
        Inches(7), Inches(0.26), size=8, bold=True, color=TEAL)
    txt(s, "Programa de Acompanhamento & Escala",
        Inches(0.3), Inches(0.52), Inches(9.2), Inches(0.72),
        size=22, bold=True, color=WHITE)

    txt(s, "O que acontece depois das 12 semanas — para quem quer sustentar e ampliar os resultados.",
        Inches(0.3), Inches(1.58), Inches(9.2), Inches(0.3), size=9, color=GRAY)
    box(s, Inches(0.3), Inches(1.94), Inches(9.4), Inches(0.02), fill=GRAY_LINE)

    # 4 pillars of the accompaniment program
    prog_items = [
        (TEAL,  "Reunião Estratégica Mensal",
         "Todo mês revisamos KPIs, metas e prioridades com base nos dados reais. Decisões fundamentadas, não no piloto automático."),
        (NAVY,  "Acompanhamento de Indicadores Mensal",
         "Mantemos os painéis vivos com atualização mensal: novos dados, novos indicadores conforme a clínica evolui."),
        (TEAL,  "Suporte a Novas Decisões",
         "Antes de contratar, investir ou mudar modelo de atendimento — você tem nossa análise técnica."),
        (NAVY,  "Acesso Direto à Equipe Fletic",
         "Canal prioritário com Dani e Simone para dúvidas, decisões urgentes e oportunidades não mapeadas."),
    ]
    iw = (W - Inches(0.6) - Inches(0.36)) / 4
    for i, (col, title3, desc4) in enumerate(prog_items):
        il = Inches(0.3) + i * (iw + Inches(0.12))
        it = Inches(2.06)
        ih = Inches(2.68)
        box(s, il, it, iw, ih, fill=GRAY_BG)
        box(s, il, it, iw, Inches(0.05), fill=col)
        # Number badge
        box(s, il + Inches(0.14), it + Inches(0.18), Inches(0.32), Inches(0.32), fill=col)
        txt(s, str(i+1), il + Inches(0.14), it + Inches(0.16), Inches(0.32), Inches(0.36),
            size=11, bold=True, color=WHITE, align=PP_ALIGN.CENTER)
        txt(s, title3, il + Inches(0.14), it + Inches(0.62), iw - Inches(0.22),
            Inches(0.64), size=9, bold=True, color=NAVY)
        txt(s, desc4, il + Inches(0.14), it + Inches(1.34), iw - Inches(0.22),
            Inches(1.22), size=8, color=GRAY)

    # Pricing note / positioning block
    box(s, Inches(0.3), Inches(4.86), Inches(5.5), Inches(0.52), fill=TEAL_BG)
    box(s, Inches(0.3), Inches(4.86), Inches(0.04), Inches(0.52), fill=TEAL)
    txt(s, "Investimento anual definido ao final da Fase 2, com base nos resultados alcançados e nas metas de crescimento da clínica.",
        Inches(0.44), Inches(4.92), Inches(5.16), Inches(0.38), size=8, italic=True, color=TEAL_DARK)

    box(s, Inches(6.0), Inches(4.86), Inches(3.7), Inches(0.52), fill=GRAY_BG, line=GRAY_LINE, lw=Pt(0.75))
    txt(s, "Conversamos sobre isso no encerramento da Fase 2.",
        Inches(6.14), Inches(4.92), Inches(3.44), Inches(0.38), size=9, bold=True, color=NAVY)

    footer(s, "14", c)

    prs.save(c["output"])
    print(f"PPT gerado: {c['output']}  ({len(list(prs.slides))} slides)")


# ── CLIENT DATA ───────────────────────────────────────────────────────────────

ANA_PAULA = {
    "key":              "ana_paula",
    "nome":             "Ana Paula Monteiro",
    "dra":              "Dra. Ana Paula Monteiro",
    "a_clinica":        "a APR LTDA",
    "clinica":          "APR LTDA",
    "especialidade":    "Cardiologia & Cuidados Paliativos",
    "cidade":           "Rio de Janeiro – RJ",
    "mes_ano":          "Junho 2026",
    "faturamento_mensal": "até R$ 30.000",
    "receita_mensal":   30000,
    "scores":           [0.67, 1.00, 1.00, 0.33, 0.83],
    "score_final":      0.76,
    "pilar_critico_idx": 3,  # P4 Dados & Inteligência
    "titulo_capa":      "Estruturação do Modelo Assistencial\nda Dra. Ana Paula Monteiro",
    "teaser_text":      ("A Dra. Ana Paula tem o perfil e a disposição para mudança — carteira de pacientes crônicos "
                         "e especialidade de alto valor em cardiologia e cuidados paliativos. O que falta é a estrutura "
                         "que transforma essa base em operação previsível, recorrente e que funciona sem depender exclusivamente dela."),
    "gaps": [
        ("01", "Gestão 100% por percepção — zero indicadores formais",
         "Sem KPIs clínicos ou operacionais. Decisões sem base em dados — impossível identificar gargalos, medir resultados ou justificar investimentos.",
         RED),
        ("02", "Modelo presencial exclusivo — sem integração digital",
         "Cardiologia crônica e cuidados paliativos têm natureza de acompanhamento longitudinal. Sem telemedicina e sem protocolo híbrido, o potencial está desperdiçado.",
         RED),
        ("03", "Receita 100% transacional — sem recorrência estruturada",
         "Pacientes crônicos que deveriam retornar regularmente não têm programa de acompanhamento. Receita recorrente potencial não capturada.",
         ORANGE),
        ("04", "Tecnologia fragmentada — WhatsApp como sistema central",
         "Prontuário básico subutilizado, sem telemedicina, sem integração. Dados clínicos valiosos não se transformam em inteligência de gestão.",
         ORANGE),
    ],
    "modelo_atual": [
        "Receita 100% variável — apenas consultas avulsas",
        "Sem protocolo de acompanhamento para crônicos cardíacos",
        "Zero indicadores clínicos ou operacionais formais",
        "WhatsApp e agenda manual como únicos sistemas",
        "Sem telemedicina — atendimento exclusivamente presencial",
        "Decisões baseadas em percepção, não em dados",
    ],
    "modelo_estruturado": [
        "Receita recorrente via programas de acompanhamento cardíaco",
        "Protocolo de telemonitoramento e retorno programado para crônicos",
        "KPIs clínicos, operacionais e financeiros com dashboard semanal",
        "Prontuário + telemedicina + agenda integrados e funcionais",
        "Jornada do paciente documentada e escalável",
        "Decisões baseadas em dados — visibilidade real da operação",
    ],
    "resultado_line": ("Resultado esperado: previsibilidade financeira, retenção de pacientes crônicos cardíacos "
                       "e modelo assistencial híbrido que escala sem depender exclusivamente da Dra. Ana Paula."),
    "m01_resumo": ["Modelo híbrido definido","Segmentação de crônicos","Jornada AS-IS → TO-BE","Critérios de elegibilidade"],
    "m02_resumo": ["Protocolos de atendimento","Integração de agenda","Gestão de capacidade","Scripts por função"],
    "m03_resumo": ["Programas de crônicos","Precificação por valor","Projeção financeira","Estratégia de ROI"],
    "m04_resumo": ["PEP + telemedicina","Interoperabilidade","LGPD e segurança","Infraestrutura escalável"],
    "m05_resumo": ["KPIs clínicos e operac.","Dashboard gerencial","Indicadores financeiros","Rotina de decisão"],
    "m01_items": [
        "Mapeamento da jornada atual (AS-IS) da carteira de pacientes crônicos",
        "Desenho da jornada ideal (TO-BE) com protocolos de acompanhamento e retorno",
        "Segmentação da carteira por risco cardíaco e frequência de cuidado",
        "Estruturação dos serviços: consulta, retorno, cuidados paliativos e telemedicina",
        "Critérios de elegibilidade para atendimento digital vs. presencial",
    ],
    "m02_items": [
        "Protocolos assistenciais para consulta cardíaca e cuidados paliativos",
        "Scripts operacionais e fluxos por função (recepção, médico)",
        "Organização da agenda: blocos presenciais, digitais e de retorno",
        "Regras de alocação de capacidade e gestão de lista de espera",
        "Definição de responsabilidades — base para estruturação da equipe",
    ],
    "m03_items": [
        "Análise do modelo de receita atual — avulso vs. recorrente",
        "Programas de acompanhamento cardíaco longitudinal (contratos de cuidado)",
        "Precificação por complexidade: cardiologia geral vs. cuidados paliativos",
        "Simulação de impacto financeiro e projeção de receita recorrente",
        "Estratégia de retenção e aumento do LTV por paciente",
    ],
    "m04_items": [
        "Seleção de plataforma de telemedicina para acompanhamento cardíaco",
        "Fluxos digitais: pré-consulta e follow-up automatizados",
        "Integração entre prontuário eletrônico e agenda digital",
        "Padronização de uso das ferramentas pela equipe",
        "Política de segurança da informação — LGPD",
    ],
    "m05_items": [
        "KPIs clínicos: adesão, retorno, estratificação de risco cardíaco",
        "KPIs operacionais: ocupação, cancelamentos, tempo de espera",
        "Indicadores financeiros: receita por paciente, custo por serviço",
        "Dashboard gerencial com rotina de decisão semanal",
        "Estrutura de melhoria contínua para o Programa de Escala",
    ],
    "premissas_text": ("Crescimento de apenas 15% ao ano sobre base atual  ·  Sem ampliação de capacidade física  ·  "
                       "Resultado via recorrência e eficiência  ·  O resultado real tende a superar essa projeção com "
                       "a implementação de telemedicina e programas de acompanhamento cardíaco."),
    "fecho_line":   "A decisão de hoje define o ponto de partida da clínica de cardiologia que a Dra. Ana Paula quer construir.",
    "output":       "/tmp/proposta_comercial_ana_paula.pptx",
}

ETHEL = {
    "key":              "ethel",
    "nome":             "Ethel Pinella",
    "dra":              "Dra. Ethel Pinella",
    "a_clinica":        "a Dra. Ethel",
    "clinica":          "Ethel Pinella Clínica",
    "especialidade":    "Endoscopia & Nutrologia",
    "cidade":           "Leblon, Rio de Janeiro – RJ",
    "mes_ano":          "Junho 2026",
    "faturamento_mensal": "até R$ 30.000",
    "receita_mensal":   30000,
    "scores":           [1.58, 1.33, 1.17, 1.00, 1.25],
    "score_final":      1.29,
    "pilar_critico_idx": 3,  # P4 Dados & Inteligência
    "titulo_capa":      "Estruturação Operacional e Sustentabilidade\ndo Modelo Assistencial da Dra. Ethel Pinella",
    "teaser_text":      ("A Dra. Ethel tem a combinação certa: especialidade de alta demanda, localização privilegiada "
                         "no Leblon e pacientes com perfil premium. O que falta é a estrutura que transforma consultas "
                         "avulsas e procedimentos de endoscopia num modelo recorrente e escalável via nutrologia e "
                         "acompanhamento pós-procedimento."),
    "gaps": [
        ("01", "Modelo de receita 100% baseado em consultas e procedimentos avulsos",
         "Sem programas nutrológicos recorrentes ou protocolo de retorno pós-endoscopia. Receita flutua mês a mês sem previsibilidade.",
         RED),
        ("02", "Dados de pacientes dispersos — sem estratificação ou indicadores",
         "Carteira sem segmentação por perfil de risco ou frequência de acompanhamento em nutrologia. Decisões por percepção.",
         ORANGE),
        ("03", "Telemedicina subutilizada — sem protocolo ou integração",
         "Nutrologia e longevidade têm altíssima demanda por teleconsulta. Plataforma genérica em uso, sem protocolo — potencial desperdiçado.",
         RED),
        ("04", "Operação sem processos documentados — dependência da médica",
         "Qualquer crescimento fica limitado à capacidade de atendimento pessoal. Sem delegação ou protocolos formais, escala é impossível.",
         ORANGE),
    ],
    "modelo_atual": [
        "Receita 100% variável — consultas e procedimentos avulsos",
        "Telemedicina genérica sem protocolo ou integração de agenda",
        "Zero indicadores de acompanhamento nutrológico",
        "WhatsApp e agenda manual como únicos sistemas operacionais",
        "Sem programa estruturado pós-endoscopia ou nutrológico",
        "Médica é único ponto de entrega e contato da clínica",
    ],
    "modelo_estruturado": [
        "Receita recorrente via programas nutrológicos e retorno pós-endoscopia",
        "Telemedicina para follow-up nutrológico com protocolo definido",
        "KPIs clínicos e dashboard gerencial semanal",
        "Prontuário + telemedicina + agenda integrados e funcionais",
        "Programas de acompanhamento nutrológico e pós-procedimento",
        "Protocolos que funcionam sem depender exclusivamente da Dra. Ethel",
    ],
    "resultado_line": ("Resultado esperado: previsibilidade financeira, crescimento da carteira de pacientes "
                       "e operação de endoscopia e nutrologia que escala sem depender exclusivamente da Dra. Ethel."),
    "m01_resumo": ["Modelo híbrido definido","Segmentação da carteira","Jornada AS-IS → TO-BE","Critérios de elegibilidade"],
    "m02_resumo": ["Protocolos de atendimento","Integração de agenda","Gestão de capacidade","Scripts por função"],
    "m03_resumo": ["Programas nutrológicos","Precificação por valor","Projeção financeira","Estratégia de ROI"],
    "m04_resumo": ["PEP + telemedicina","Interoperabilidade","LGPD e segurança","Infraestrutura escalável"],
    "m05_resumo": ["KPIs clínicos e operac.","Dashboard gerencial","Indicadores financeiros","Rotina de decisão"],
    "m01_items": [
        "Mapeamento da jornada atual (AS-IS) da carteira de pacientes",
        "Desenho da jornada ideal (TO-BE) com protocolos nutrológicos e pós-endoscopia",
        "Segmentação da carteira por perfil de saúde e frequência de acompanhamento",
        "Estruturação dos serviços assistenciais por tipo e complexidade",
        "Critérios de elegibilidade para telemedicina vs. presencial",
    ],
    "m02_items": [
        "Protocolos assistenciais para consulta nutrológica e pós-endoscopia",
        "Scripts operacionais e fluxos por função (recepção, médico)",
        "Organização da agenda: blocos presenciais, digitais e de retorno",
        "Regras de alocação de capacidade e gestão de lista de espera",
        "Definição de responsabilidades — base para contratação de equipe",
    ],
    "m03_items": [
        "Análise do modelo de receita atual — avulso vs. recorrente",
        "Programas de acompanhamento nutrológico (pacotes mensais)",
        "Precificação por complexidade: nutrologia, longevidade e endoscopia",
        "Simulação de impacto financeiro e projeção de receita recorrente",
        "Estratégia de aumento de ticket médio por paciente",
    ],
    "m04_items": [
        "Seleção de plataforma de telemedicina dedicada para nutrologia",
        "Fluxos digitais: pré-consulta e follow-up automatizados",
        "Integração entre prontuário eletrônico e agenda digital",
        "Padronização de uso das ferramentas pela equipe",
        "Política de segurança da informação — LGPD",
    ],
    "m05_items": [
        "KPIs clínicos: adesão, retorno, estratificação de risco nutrológico",
        "KPIs operacionais: ocupação, cancelamentos, tempo de espera",
        "Indicadores financeiros: receita por paciente, custo por serviço",
        "Dashboard gerencial com rotina de decisão semanal",
        "Estrutura de melhoria contínua para o Programa de Escala",
    ],
    "premissas_text": ("Crescimento de apenas 15% ao ano sobre base atual  ·  Sem ampliação de capacidade física  ·  "
                       "Resultado via recorrência e eficiência  ·  O resultado real tende a superar essa projeção "
                       "com a implementação de programas de longevidade recorrente e telemedicina estruturada."),
    "fecho_line":   "A decisão de hoje define o ponto de partida da clínica de endoscopia e nutrologia que a Dra. Ethel quer construir.",
    "output":       "/tmp/proposta_comercial_ethel.pptx",
}

DANIELA_BORGES = {
    "key":              "daniela",
    "nome":             "Daniela Borges",
    "dra":              "Dra. Daniela Borges",
    "a_clinica":        "a Imagecor",
    "clinica":          "Imagecor",
    "especialidade":    "Cardiologia",
    "cidade":           "Catete, Rio de Janeiro – RJ",
    "mes_ano":          "Junho 2026",
    "faturamento_mensal": "até R$ 30.000",
    "receita_mensal":   30000,
    "scores":           [0.50, 0.50, 1.00, 0.33, 0.67],
    "score_final":      0.58,
    "pilar_critico_idx": 3,  # P4 Dados & Inteligência
    "titulo_capa":      "Estruturação Operacional e Crescimento\nda Imagecor",
    "teaser_text":      ("A Imagecor tem um ativo estratégico raro: exames cardiológicos próprios — Eco, Doppler e "
                         "Holter — que geram dados clínicos valiosos e justificam acompanhamento longitudinal. "
                         "O problema é que sem estrutura, esses dados não viram inteligência e os pacientes crônicos "
                         "não retornam. O que falta é o sistema — não a demanda."),
    "gaps": [
        ("01", "Taxa de retorno <50% em cardiologia crônica — receita desperdiçada",
         "70% de pacientes novos significa captação constante como única alavanca. Sem programa de retorno, a clínica reinicia o funil todo mês.",
         RED),
        ("02", "3 salas com 8 de 11 turnos preenchidos — capacidade ociosa",
         "Custo fixo integral, receita parcial. O problema não é demanda — é gestão de capacidade e retenção de pacientes.",
         RED),
        ("03", "Sem dados ou controle financeiro — 'muito trabalho, pouco resultado'",
         "Nota 1 para controle financeiro, nota 4 para dados. Sem dashboard ou indicadores, impossível identificar onde estão as perdas.",
         RED),
        ("04", "Dívidas declaradas + modelo 100% transacional",
         "Captação constante de novos pacientes com custo de aquisição elevado, sem recorrência — pressão financeira crescente e insustentável.",
         ORANGE),
    ],
    "modelo_atual": [
        "Receita 100% variável — consultas e exames avulsos",
        "Taxa de retorno <50% — crônicos cardíacos sem follow-up estruturado",
        "3 salas com capacidade ociosa — 8 de 11 turnos preenchidos",
        "WhatsApp e agenda manual como únicos sistemas operacionais",
        "Sem indicadores ou dashboard — gestão por percepção",
        "Dívidas declaradas e dependência de captação constante",
    ],
    "modelo_estruturado": [
        "Receita recorrente via programas de acompanhamento cardíaco",
        "Protocolo de retorno para pacientes pós-exame e crônicos cardíacos",
        "3 salas com ocupação otimizada — demanda gerenciada ativamente",
        "Prontuário + telemedicina + agenda integrados e automatizados",
        "Dashboard de indicadores: ocupação, retenção e receita por paciente",
        "Modelo financeiro equilibrado — crescimento sem aumento de captação",
    ],
    "resultado_line": ("Resultado esperado: transformar os exames de Eco e Doppler em porta de entrada para "
                       "acompanhamento recorrente — aumentando retenção, ocupação e previsibilidade financeira."),
    "m01_resumo": ["Jornada pós-exame definida","Segmentação da carteira","Protocolo de retorno","Critérios de elegibilidade"],
    "m02_resumo": ["Protocolos de retorno","Gestão das 3 salas","Regras de capacidade","Scripts por função"],
    "m03_resumo": ["Programas de crônicos","Precificação por valor","Projeção financeira","Estratégia de ROI"],
    "m04_resumo": ["PEP + telemedicina","Integração de exames","LGPD e segurança","Infraestrutura escalável"],
    "m05_resumo": ["KPIs de retenção","Dashboard de ocupação","Indicadores financeiros","Rotina de decisão"],
    "m01_items": [
        "Mapeamento da jornada atual (AS-IS) dos pacientes cardíacos e pós-exame",
        "Desenho da jornada ideal (TO-BE) com protocolo de retorno pós-Eco e Holter",
        "Segmentação da carteira: crônicos, agudos e pacientes pós-procedimento",
        "Estruturação dos serviços por tipo e frequência esperada de retorno",
        "Critérios de elegibilidade para telemedicina vs. presencial",
    ],
    "m02_items": [
        "Protocolos de retorno pós-exame (Eco, Doppler, Holter, MAPA)",
        "Scripts de comunicação com pacientes via WhatsApp e agenda",
        "Organização das 3 salas / 11 turnos — regras de alocação e prioridade",
        "Gestão de capacidade: eliminar ociosidade e criar lista de espera ativa",
        "Definição de responsabilidades e fluxos independentes da Dra. Daniela",
    ],
    "m03_items": [
        "Análise do modelo de receita atual — avulso vs. recorrente",
        "Programas de acompanhamento cardíaco recorrente (contratos de cuidado)",
        "Precificação por complexidade e valor percebido pelo paciente",
        "Simulação de impacto financeiro e estratégia de equilíbrio das dívidas",
        "Estratégia de aumento de ticket e receita sem aumentar captação",
    ],
    "m04_items": [
        "Integração do prontuário eletrônico com agenda e resultados de exames",
        "Plataforma de telemedicina para follow-up cardiológico",
        "Fluxos digitais: pré-consulta e entrega de resultados automatizados",
        "Padronização de uso das ferramentas pela equipe",
        "Política de segurança da informação — LGPD",
    ],
    "m05_items": [
        "KPIs clínicos: taxa de retorno, adesão, estratificação de risco cardíaco",
        "KPIs operacionais: ocupação de salas, cancelamentos, tempo de espera",
        "Indicadores financeiros: receita por paciente, custo por turno de sala",
        "Dashboard gerencial com rotina de decisão semanal",
        "Estrutura de melhoria contínua para o Programa de Escala",
    ],
    "premissas_text": ("Crescimento de apenas 15% ao ano sobre base atual  ·  Sem ampliação de capacidade física  ·  "
                       "Resultado via retenção e eficiência operacional  ·  O resultado real tende a superar essa "
                       "projeção com a ocupação plena das 3 salas e programas de retorno cardíaco estruturado."),
    "fecho_line":   "A decisão de hoje define o ponto de partida da Imagecor que a Dra. Daniela quer construir — com controle, crescimento e previsibilidade.",
    "output":       "/tmp/proposta_comercial_imagecor.pptx",
}


# ── Run ───────────────────────────────────────────────────────────────────────

if __name__ == "__main__":
    for client in [ANA_PAULA, ETHEL, DANIELA_BORGES]:
        gerar_pptx(client)
