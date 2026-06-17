"""
METTA — Listas de Presença v4
Cabeçalho: faixa preta + logo real METTA
Corpo: tabela clara com marcadores ✔/✘ e bom respiro
"""
import os, base64
from reportlab.pdfgen import canvas
from reportlab.lib.pagesizes import A4
from reportlab.lib import colors
from reportlab.lib.utils import ImageReader

_DIR = os.path.dirname(os.path.abspath(__file__))
LOGO_PATH = os.path.join(_DIR, "metta_logo.png")

BLACK   = colors.HexColor('#000000')
GOLD    = colors.HexColor('#E9A820')
GOLD_DK = colors.HexColor('#B07C0A')
HDR_ROW = colors.HexColor('#F3F3F0')
ALT_ROW = colors.HexColor('#FAFAF7')
WHITE   = colors.white
DARK    = colors.HexColor('#1A1A1A')
GRAY    = colors.HexColor('#4A4A4A')
GRID    = colors.HexColor('#DDDDDD')
GREEN   = colors.HexColor('#1A7A3C')
RED     = colors.HexColor('#C0392B')

MEETINGS = [
    ("E1",  "09/01","Diagnóstico e Autoconhecimento"),
    ("E2",  "16/01","Estratégia e Propósito"),
    ("E3",  "23/01","Mentalidade e Técnica de Vendas"),
    ("E4",  "30/01","Programa de Acompanhamento"),
    ("E5",  "06/02","Role Play e Hotseat"),
    ("E6",  "13/02","Treinamento de Secretária e Equipe"),
    ("E7",  "20/02","Indicadores Estratégicos e Clínicos"),
    ("E8",  "27/02","Telemedicina Moderna"),
    ("E9",  "06/03","Jornada Híbrida do Paciente"),
    ("E10", "13/03","IA na Gestão e Assistência"),
    ("E11", "20/03","Infoproduto do Zero ao Lançamento"),
    ("E12", "27/03","Comunicação Assertiva e Difícil"),
    ("E13", "03/04","Formatos de Atuação, Escala e Parcerias"),
    ("E14", "10/04","Jornada Híbrida do Paciente"),
    ("E15", "17/04","Role Play e Hotseat"),
    ("E16", "24/04","Role Play e Hotseat"),
    ("E17", "08/05","Autogestão Emocional, Limites e Resiliência"),
    ("E18", "15/05","Arquitetura de Hábitos, Agenda e Energia"),
    ("E19", "22/05","Planejamento Financeiro, Precificação e Valor"),
    ("E20", "29/05","Marca Pessoal e Posicionamento Público"),
    ("E21", "05/06","Automação com Claude Code"),
    ("E22", "05/06","Automação com Claude Code"),
    ("E23", "11/06","Roadmap e Business Plan"),
    ("E24", "19/06","Autonomia Profissional e Carreira de Longo Prazo"),
]

PRESENCA = {
    # (Ana Paula, Ethel)  — fonte: METTA_Relatorio_Presenca_Turma1_2026.docx
    "E1": (False,True),  "E2": (True, True),  "E3": (False,True),  "E4": (False,True),
    "E5": (False,False), "E6": (True, True),  "E7": (False,True),  "E8": (True, True),
    "E9": (True, True),  "E10":(True, True),  "E11":(True, True),  "E12":(True, True),
    "E13":(True, False), "E14":(True, True),  "E15":(True, False), "E16":(False,False),
    "E17":(False,False), "E18":(True, True),  "E19":(True, False), "E20":(True, True),
    "E21":(True, True),  "E22":(True, True),  "E23":(True, True),  "E24":(True, True),
}
ALUNOS = ["Ana Paula Monteiro", "Ethel Pinella"]

CHECK = chr(0x34)   # Zapf-Dingbats heavy checkmark
CROSS = chr(0x38)   # Zapf-Dingbats heavy ballot X

def pv(present): return CHECK if present else CROSS
def pc(present): return GREEN if present else RED

LOGO_H_CONTENT = 60   # logo height in content area (pt)
LOGO_W_CONTENT = LOGO_H_CONTENT * (330 / 160)
LOGO_MARGIN    = 10   # vertical gap between logo and title

def draw_header(c, pw, ph, hdr_h=90):
    # Solid black band
    c.setFillColor(BLACK)
    c.rect(0, ph - hdr_h, pw, hdr_h, fill=1, stroke=0)
    # "METTA" text in the band
    c.setFont("Helvetica-Bold", 22)
    c.setFillColor(GOLD)
    c.drawCentredString(pw/2, ph - hdr_h + 38, "S I M O N E  F A R A H")
    c.setFont("Helvetica", 11)
    c.setFillColor(WHITE)
    c.drawCentredString(pw/2, ph - hdr_h + 20, "M E N T O R I A   M E T T A")
    # Gold separator line
    c.setStrokeColor(GOLD)
    c.setLineWidth(2)
    c.line(0, ph - hdr_h, pw, ph - hdr_h)

def draw_subtitle(c, pw, ph, hdr_h, title, sub):
    # Logo in content area (white background)
    logo_x = (pw - LOGO_W_CONTENT) / 2
    logo_y = ph - hdr_h - LOGO_MARGIN - LOGO_H_CONTENT
    try:
        c.drawImage(ImageReader(LOGO_PATH), logo_x, logo_y,
                    width=LOGO_W_CONTENT, height=LOGO_H_CONTENT, mask='auto')
    except Exception:
        pass  # if logo fails, skip — header text is already there
    y = logo_y - LOGO_MARGIN - 12
    c.setFont("Helvetica-Bold", 13)
    c.setFillColor(DARK)
    c.drawCentredString(pw/2, y, title)
    y -= 14
    c.setFont("Helvetica", 9)
    c.setFillColor(GOLD_DK)
    c.drawCentredString(pw/2, y, sub)
    return y - 14

def row_bg(c, x, y, w, h, bg):
    c.setFillColor(bg)
    c.rect(x, y - h, w, h, fill=1, stroke=0)

def cell_text(c, txt, cx, cy, w, h, font="Helvetica", size=8, color=DARK, align="c"):
    c.setFont(font, size)
    c.setFillColor(color)
    bl = cy - h + h * 0.30
    if align == "c":
        c.drawCentredString(cx + w/2, bl, str(txt))
    else:
        c.drawString(cx + 5, bl, str(txt))

def cell_dingbat(c, sym, cx, cy, w, h, color=DARK):
    c.setFont("ZapfDingbats", 12)
    c.setFillColor(color)
    c.drawCentredString(cx + w/2, cy - h + h * 0.28, sym)

def draw_grid(c, x, y, col_ws, h):
    c.setStrokeColor(GRID)
    c.setLineWidth(0.3)
    cx = x
    for w in col_ws:
        c.rect(cx, y - h, w, h, fill=0, stroke=1)
        cx += w

def draw_legend(c, x, y):
    c.setFont("ZapfDingbats", 10); c.setFillColor(GREEN)
    c.drawString(x, y, CHECK)
    c.setFont("Helvetica", 8); c.setFillColor(GREEN)
    c.drawString(x + 13, y, "= Presente")
    c.setFont("ZapfDingbats", 10); c.setFillColor(RED)
    c.drawString(x + 85, y, CROSS)
    c.setFont("Helvetica", 8); c.setFillColor(RED)
    c.drawString(x + 98, y, "= Falta")

def draw_footer(c, pw):
    c.setFont("Helvetica-Oblique", 7)
    c.setFillColor(GRAY)
    c.drawCentredString(pw/2, 14,
        "Mentoria METTA  ·  Simone Farah & Danielle Magalhães  ·  fletic.com.br")

# ── Turma 1 — retrato ─────────────────────────────────────────────────────────
def turma1(out):
    pw, ph = A4
    c = canvas.Canvas(out, pagesize=A4)
    c.setTitle("Lista de Presença — Turma 1 METTA 2026")
    HDR_H = 90
    draw_header(c, pw, ph, HDR_H)
    y = draw_subtitle(c, pw, ph, HDR_H,
        "LISTA DE PRESENÇA — TURMA 1  ·  2026",
        "Mentoria METTA  ·  Simone Farah & Danielle Magalhães")

    n = len(ALUNOS)
    c_enc = 30; c_data = 52; c_tema = 255; c_aluno = 70
    total_w = c_enc + c_data + c_tema + c_aluno * n
    x0 = (pw - total_w) / 2
    col_ws = [c_enc, c_data, c_tema] + [c_aluno] * n
    HDR = 20; ROW = 16

    row_bg(c, x0, y, total_w, HDR, HDR_ROW)
    cx = x0
    for h_txt, w in zip(["Enc.", "Data", "Tema"] + [a.split()[0] for a in ALUNOS], col_ws):
        cell_text(c, h_txt, cx, y, w, HDR, font="Helvetica-Bold", size=9)
        cx += w
    draw_grid(c, x0, y, col_ws, HDR)
    y -= HDR

    for i, (enc, data, tema) in enumerate(MEETINGS):
        bg = WHITE if i % 2 == 0 else ALT_ROW
        row_bg(c, x0, y, total_w, ROW, bg)
        cx = x0
        cell_text(c, enc,  cx, y, c_enc,  ROW, size=8); cx += c_enc
        cell_text(c, data, cx, y, c_data, ROW, size=8); cx += c_data
        cell_text(c, tema, cx, y, c_tema, ROW, size=8, align="l"); cx += c_tema
        for idx in range(n):
            pr = PRESENCA.get(enc, (False,)*n)[idx]
            cell_dingbat(c, pv(pr), cx, y, c_aluno, ROW, color=pc(pr))
            cx += c_aluno
        draw_grid(c, x0, y, col_ws, ROW)
        y -= ROW

    y -= 14
    total = len(MEETINGS)
    parts = []
    for idx, nome in enumerate(ALUNOS):
        p = sum(1 for enc,_,_ in MEETINGS if PRESENCA.get(enc,(False,)*n)[idx])
        f = total - p; pct = round(p/total*100)
        parts.append(f"{nome.split()[0]}: {p} pres. / {f} falt. ({pct}%)")
    c.setFont("Helvetica-Bold", 9); c.setFillColor(DARK)
    c.drawString(x0, y, f"Total: {total} encontros   |   " + "   ·   ".join(parts))
    draw_legend(c, x0, y - 12)
    draw_footer(c, pw)
    c.save(); print(f"✅ {out}")

# ── Individual — retrato ───────────────────────────────────────────────────────
def individual(nome, col_idx, out):
    pw, ph = A4
    c = canvas.Canvas(out, pagesize=A4)
    c.setTitle(f"Lista de Presença — {nome} — METTA 2026")
    HDR_H = 90
    draw_header(c, pw, ph, HDR_H)
    y = draw_subtitle(c, pw, ph, HDR_H,
        f"LISTA DE PRESENÇA  ·  {nome.upper()}",
        "Mentoria METTA — 2026  ·  Simone Farah & Danielle Magalhães")

    c_enc=34; c_data=60; c_tema=310; c_pres=66
    total_w = c_enc+c_data+c_tema+c_pres
    x0 = (pw - total_w) / 2
    col_ws = [c_enc, c_data, c_tema, c_pres]
    HDR = 20; ROW = 16

    row_bg(c, x0, y, total_w, HDR, HDR_ROW)
    cx = x0
    for h_txt, w in zip(["Enc.", "Data", "Tema", "Presença"], col_ws):
        cell_text(c, h_txt, cx, y, w, HDR, font="Helvetica-Bold", size=9)
        cx += w
    draw_grid(c, x0, y, col_ws, HDR)
    y -= HDR

    for i, (enc, data, tema) in enumerate(MEETINGS):
        pr = PRESENCA.get(enc, (False, False))[col_idx]
        bg = WHITE if i % 2 == 0 else ALT_ROW
        row_bg(c, x0, y, total_w, ROW, bg)
        cx = x0
        cell_text(c, enc,  cx, y, c_enc,  ROW, size=8); cx += c_enc
        cell_text(c, data, cx, y, c_data, ROW, size=8); cx += c_data
        cell_text(c, tema, cx, y, c_tema, ROW, size=8, align="l"); cx += c_tema
        cell_dingbat(c, pv(pr), cx, y, c_pres, ROW, color=pc(pr))
        draw_grid(c, x0, y, col_ws, ROW)
        y -= ROW

    total = len(MEETINGS)
    p = sum(1 for enc,_,_ in MEETINGS if PRESENCA.get(enc,(False,False))[col_idx])
    f = total - p; pct = round(p/total*100)
    y -= 14
    c.setFont("Helvetica-Bold", 9); c.setFillColor(DARK)
    c.drawString(x0, y,
        f"Total: {total} encontros   |   Presenças: {p}   |   Faltas: {f}   |   Frequência: {pct}%")
    draw_legend(c, x0, y - 12)
    draw_footer(c, pw)
    c.save(); print(f"✅ {out}")

# Auto-extrai logo se não existir
_LOGO_B64 = "iVBORw0KGgoAAAANSUhEUgAAAUoAAACgCAIAAADl47ICAAAACXBIWXMAAA7EAAAOxAGVKw4bAAAE1mlUWHRYTUw6Y29tLmFkb2JlLnhtcAAAAAAAPD94cGFja2V0IGJlZ2luPSfvu78nIGlkPSdXNU0wTXBDZWhpSHpyZVN6TlRjemtjOWQnPz4KPHg6eG1wbWV0YSB4bWxuczp4PSdhZG9iZTpuczptZXRhLyc+CjxyZGY6UkRGIHhtbG5zOnJkZj0naHR0cDovL3d3dy53My5vcmcvMTk5OS8wMi8yMi1yZGYtc3ludGF4LW5zIyc+CgogPHJkZjpEZXNjcmlwdGlvbiByZGY6YWJvdXQ9JycKICB4bWxuczpBdHRyaWI9J2h0dHA6Ly9ucy5hdHRyaWJ1dGlvbi5jb20vYWRzLzEuMC8nPgogIDxBdHRyaWI6QWRzPgogICA8cmRmOlNlcT4KICAgIDxyZGY6bGkgcmRmOnBhcnNlVHlwZT0nUmVzb3VyY2UnPgogICAgIDxBdHRyaWI6Q3JlYXRlZD4yMDI2LTAxLTA2PC9BdHRyaWI6Q3JlYXRlZD4KICAgICA8QXR0cmliOkV4dElkPjQ3MmFmYWIzLTY5MmMtNDMyMi04NGJjLWNhMmE0ZjRkOGYzMjwvQXR0cmliOkV4dElkPgogICAgIDxBdHRyaWI6RmJJZD41MjUyNjU5MTQxNzk1ODA8L0F0dHJpYjpGYklkPgogICAgIDxBdHRyaWI6VG91Y2hUeXBlPjI8L0F0dHJpYjpUb3VjaFR5cGU+CiAgICA8L3JkZjpsaT4KICAgPC9yZGY6U2VxPgogIDwvQXR0cmliOkFkcz4KIDwvcmRmOkRlc2NyaXB0aW9uPgoKIDxyZGY6RGVzY3JpcHRpb24gcmRmOmFib3V0PScnCiAgeG1sbnM6ZGM9J2h0dHA6Ly9wdXJsLm9yZy9kYy9lbGVtZW50cy8xLjEvJz4KICA8ZGM6dGl0bGU+CiAgIDxyZGY6QWx0PgogICAgPHJkZjpsaSB4bWw6bGFuZz0neC1kZWZhdWx0Jz5TaW1vbmVGYXJhaF9Mb2dvX0NhYmXDp2FsaG8gKDMzMCB4IDE2MCBwaXhlbHMpIC0gMjwvcmRmOmxpPgogICA8L3JkZjpBbHQ+CiAgPC9kYzp0aXRsZT4KIDwvcmRm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"

if not os.path.exists(LOGO_PATH):
    with open(LOGO_PATH, 'wb') as _f:
        _f.write(base64.b64decode(_LOGO_B64))

if __name__ == "__main__":
    turma1('/tmp/v4_Turma1.pdf')
    individual("Ana Paula Monteiro", 0, '/tmp/v4_AnaPaula.pdf')
    individual("Ethel Pinella",      1, '/tmp/v4_Ethel.pdf')
    print("Gerados.")
