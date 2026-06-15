"""
METTA — Listas de Presença v3
Cabeçalho: faixa preta + texto METTA em dourado (sem imagem embutida)
Corpo: tabela clara com contagem de P/F
"""
from reportlab.pdfgen import canvas
from reportlab.lib.pagesizes import A4, landscape
from reportlab.lib import colors

BLACK     = colors.HexColor('#000000')
GOLD      = colors.HexColor('#E9A820')
GOLD_DK   = colors.HexColor('#B07C0A')
HDR_ROW   = colors.HexColor('#F3F3F0')
ALT_ROW   = colors.HexColor('#FAFAF7')
WHITE     = colors.white
DARK      = colors.HexColor('#1A1A1A')
GRAY      = colors.HexColor('#4A4A4A')
GRID      = colors.HexColor('#DDDDDD')
GREEN     = colors.HexColor('#1A7A3C')
RED       = colors.HexColor('#C0392B')

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
    "E1":(True,True),"E2":(True,True),"E3":(True,True),"E4":(True,True),
    "E5":(False,False),"E6":(True,True),"E7":(True,True),"E8":(False,False),
    "E9":(True,True),"E10":(True,True),"E11":(True,True),"E12":(True,True),
    "E13":(True,True),"E14":(True,True),"E15":(True,True),"E16":(False,False),
    "E17":(False,False),"E18":(True,True),"E19":(True,True),"E20":(True,True),
    "E21":(True,True),"E22":(True,True),"E23":(True,True),"E24":(True,True),
}
ALUNOS = ["Ana Paula Monteiro","Ethel Pinella"]

def draw_header(c, pw, ph, hdr_h=72):
    c.setFillColor(BLACK)
    c.rect(0, ph - hdr_h, pw, hdr_h, fill=1, stroke=0)
    # logo em texto
    c.setFont("Helvetica-Bold", 22)
    c.setFillColor(GOLD)
    c.drawCentredString(pw/2, ph - hdr_h + 42, "SIMONE FARAH")
    c.setFont("Helvetica", 11)
    c.setFillColor(colors.white)
    c.drawCentredString(pw/2, ph - hdr_h + 22, "M E N T O R I A   M E T T A")
    # linha dourada abaixo do header
    c.setStrokeColor(GOLD)
    c.setLineWidth(1.5)
    c.line(0, ph - hdr_h, pw, ph - hdr_h)
    return hdr_h

def draw_subtitle(c, pw, ph, hdr_h, title, sub):
    y = ph - hdr_h - 16
    c.setFont("Helvetica-Bold", 13)
    c.setFillColor(DARK)
    c.drawCentredString(pw/2, y, title)
    y -= 12
    c.setFont("Helvetica", 8)
    c.setFillColor(GOLD_DK)
    c.drawCentredString(pw/2, y, sub)
    return y - 8

def row_bg(c, x, y, w, h, bg):
    c.setFillColor(bg)
    c.rect(x, y - h, w, h, fill=1, stroke=0)

def cell(c, txt, cx, cy, w, h, font="Helvetica", size=8, color=DARK, align="c"):
    c.setFont(font, size)
    c.setFillColor(color)
    if align == "c":
        c.drawCentredString(cx + w/2, cy - h + h*0.28, str(txt))
    else:
        c.drawString(cx + 3, cy - h + h*0.28, str(txt))

def grid(c, x, y, col_ws, h):
    c.setStrokeColor(GRID)
    c.setLineWidth(0.25)
    cx = x
    for w in col_ws:
        c.rect(cx, y-h, w, h, fill=0, stroke=1)
        cx += w

def pv(present): return "P" if present else "F"
def pc(present): return GREEN if present else RED

# ── Turma 1 paisagem ──────────────────────────────────────────────────────────
def turma1(out):
    pw, ph = A4
    c = canvas.Canvas(out, pagesize=A4)
    c.setTitle("Lista de Presença — Turma 1 METTA 2026")
    HDR_H = 72
    draw_header(c, pw, ph, HDR_H)
    y = draw_subtitle(c, pw, ph, HDR_H,
        "LISTA DE PRESENÇA — TURMA 1  ·  2026",
        "Mentoria METTA  ·  Simone Farah & Danielle Magalhães")

    c_enc=28; c_data=52; c_tema=265; c_aluno=62
    n=len(ALUNOS)
    total_w = c_enc+c_data+c_tema+c_aluno*n
    x0=(pw-total_w)/2
    col_ws=[c_enc,c_data,c_tema]+[c_aluno]*n
    HDR=17; ROW=13

    # header row
    row_bg(c, x0, y, total_w, HDR, HDR_ROW)
    cx=x0
    for h_txt,w in zip(["Enc.","Data","Tema"]+[a.split()[0] for a in ALUNOS],col_ws):
        cell(c,h_txt,cx,y,w,HDR,font="Helvetica-Bold",size=9); cx+=w
    grid(c,x0,y,col_ws,HDR); y-=HDR

    for i,(enc,data,tema) in enumerate(MEETINGS):
        bg=WHITE if i%2==0 else ALT_ROW
        row_bg(c,x0,y,total_w,ROW,bg)
        cx=x0
        cell(c,enc,cx,y,c_enc,ROW,size=8); cx+=c_enc
        cell(c,data,cx,y,c_data,ROW,size=8); cx+=c_data
        cell(c,tema,cx,y,c_tema,ROW,size=8,align="l"); cx+=c_tema
        for idx in range(n):
            pr=PRESENCA.get(enc,(False,)*n)[idx]
            cell(c,pv(pr),cx,y,c_aluno,ROW,font="Helvetica-Bold",size=10,color=pc(pr)); cx+=c_aluno
        grid(c,x0,y,col_ws,ROW); y-=ROW

    # sumário
    y-=8
    total=len(MEETINGS)
    parts=[]
    for idx,nome in enumerate(ALUNOS):
        p=sum(1 for enc,_,_ in MEETINGS if PRESENCA.get(enc,(False,)*n)[idx])
        f=total-p
        pct=round(p/total*100)
        parts.append(f"{nome.split()[0]}: {p}P / {f}F ({pct}%)")
    c.setFont("Helvetica-Bold",9); c.setFillColor(DARK)
    c.drawString(x0,y,f"Total: {total} encontros   |   "+"   ·   ".join(parts))
    y-=10
    c.setFont("Helvetica",8); c.setFillColor(GREEN); c.drawString(x0,y,"P = Presente")
    c.setFillColor(RED); c.drawString(x0+75,y,"F = Falta")

    c.setFont("Helvetica-Oblique",7); c.setFillColor(GRAY)
    c.drawCentredString(pw/2,12,"Mentoria METTA  ·  Simone Farah & Danielle Magalhães  ·  fletic.com.br")
    c.save(); print(f"✅ {out}")

# ── Individual retrato ────────────────────────────────────────────────────────
def individual(nome, col_idx, out):
    pw, ph = A4
    c = canvas.Canvas(out, pagesize=A4)
    c.setTitle(f"Lista de Presença — {nome} — METTA 2026")
    HDR_H=72
    draw_header(c,pw,ph,HDR_H)
    y=draw_subtitle(c,pw,ph,HDR_H,
        f"LISTA DE PRESENÇA  ·  {nome.upper()}",
        "Mentoria METTA — 2026  ·  Simone Farah & Danielle Magalhães")

    c_enc=32; c_data=58; c_tema=295; c_pres=55
    total_w=c_enc+c_data+c_tema+c_pres
    x0=(pw-total_w)/2
    col_ws=[c_enc,c_data,c_tema,c_pres]
    HDR=17; ROW=13

    row_bg(c,x0,y,total_w,HDR,HDR_ROW)
    cx=x0
    for h_txt,w in zip(["Enc.","Data","Tema","Presença"],col_ws):
        cell(c,h_txt,cx,y,w,HDR,font="Helvetica-Bold",size=9); cx+=w
    grid(c,x0,y,col_ws,HDR); y-=HDR

    for i,(enc,data,tema) in enumerate(MEETINGS):
        pr=PRESENCA.get(enc,(False,False))[col_idx]
        bg=WHITE if i%2==0 else ALT_ROW
        row_bg(c,x0,y,total_w,ROW,bg)
        cx=x0
        cell(c,enc,cx,y,c_enc,ROW,size=8); cx+=c_enc
        cell(c,data,cx,y,c_data,ROW,size=8); cx+=c_data
        cell(c,tema,cx,y,c_tema,ROW,size=8,align="l"); cx+=c_tema
        cell(c,pv(pr),cx,y,c_pres,ROW,font="Helvetica-Bold",size=10,color=pc(pr))
        grid(c,x0,y,col_ws,ROW); y-=ROW

    total=len(MEETINGS)
    p=sum(1 for enc,_,_ in MEETINGS if PRESENCA.get(enc,(False,False))[col_idx])
    f=total-p; pct=round(p/total*100)
    y-=10
    c.setFont("Helvetica-Bold",9); c.setFillColor(DARK)
    c.drawString(x0,y,f"Total: {total} encontros   |   Presenças: {p}   |   Faltas: {f}   |   Frequência: {pct}%")
    y-=10
    c.setFont("Helvetica",8); c.setFillColor(GREEN); c.drawString(x0,y,"P = Presente")
    c.setFillColor(RED); c.drawString(x0+75,y,"F = Falta")

    c.setFont("Helvetica-Oblique",7); c.setFillColor(GRAY)
    c.drawCentredString(pw/2,12,"Mentoria METTA  ·  Simone Farah & Danielle Magalhães  ·  fletic.com.br")
    c.save(); print(f"✅ {out}")

turma1('/tmp/v3_Turma1.pdf')
individual("Ana Paula Monteiro", 0, '/tmp/v3_AnaPaula.pdf')
individual("Ethel Pinella",      1, '/tmp/v3_Ethel.pdf')
print("Gerados.")
