#!/usr/bin/env python3
import asyncio
from playwright.async_api import async_playwright

# Fotos sem microfone extraídas do upload da sessão
dani_b64   = open('/tmp/new_dani_b64.txt').read().strip()
simone_b64 = open('/tmp/new_simone_b64.txt').read().strip()

HTML = f"""<!DOCTYPE html>
<html>
<head>
<meta charset="UTF-8"/>
<style>
* {{ margin:0; padding:0; box-sizing:border-box; }}
body {{
  width: 1080px;
  height: 1350px;
  overflow: hidden;
  font-family: 'Georgia', serif;
  background: #0d1f33;
  display: flex;
  flex-direction: column;
}}

.photos {{
  display: flex;
  height: 690px;
  flex-shrink: 0;
}}

.photo-wrap {{
  flex: 1;
  position: relative;
  overflow: hidden;
}}

.photo-wrap .img {{
  position: absolute;
  inset: 0;
  background-size: cover;
  background-position: center top;
}}

.photo-wrap.dani .img {{
  background-image: url('data:image/jpeg;base64,{dani_b64}');
  background-position: center 8%;
}}

.photo-wrap.simone .img {{
  background-image: url('data:image/jpeg;base64,{simone_b64}');
  background-position: center 10%;
}}

.photo-wrap .fade {{
  position: absolute;
  inset: 0;
  background: linear-gradient(
    to bottom,
    rgba(13,31,51,0.0) 50%,
    rgba(13,31,51,0.88) 100%
  );
}}

.photo-wrap.dani::after {{
  content: '';
  position: absolute;
  top: 0; bottom: 0; right: 0;
  width: 2px;
  background: rgba(13,31,51,0.7);
}}

.photo-name {{
  position: absolute;
  bottom: 16px;
  left: 22px;
  right: 22px;
  z-index: 2;
}}
.photo-name .nm {{
  font-size: 16px;
  font-weight: 700;
  color: #fff;
  font-family: 'Georgia', serif;
  margin-bottom: 3px;
}}
.photo-name .rl {{
  font-size: 11px;
  color: #0F7173;
  letter-spacing: 1px;
  font-family: 'Georgia', serif;
}}

/* ── Faixa MASTERCLASS ── */
.masterclass-bar {{
  background: #1B3A5C;
  border-top: 3px solid #0F7173;
  border-bottom: 3px solid #0F7173;
  padding: 18px 60px;
  display: flex;
  align-items: center;
  justify-content: space-between;
  flex-shrink: 0;
}}

.masterclass-label {{
  display: flex;
  align-items: center;
  gap: 14px;
}}

.mc-dot {{
  width: 10px; height: 10px;
  border-radius: 50%;
  background: #0F7173;
  flex-shrink: 0;
}}

.mc-text {{
  font-size: 22px;
  font-weight: 700;
  color: #ffffff;
  letter-spacing: 5px;
  text-transform: uppercase;
  font-family: 'Georgia', serif;
}}

.mc-badge {{
  font-size: 13px;
  font-weight: 700;
  color: #0F7173;
  letter-spacing: 2.5px;
  text-transform: uppercase;
  font-family: 'Georgia', serif;
  border: 1px solid #0F7173;
  padding: 6px 16px;
}}

/* ── Conteúdo ── */
.content {{
  flex: 1;
  background: #0d1f33;
  padding: 24px 60px 44px 60px;
  display: flex;
  flex-direction: column;
  justify-content: space-between;
}}

.title {{
  font-family: 'Georgia', serif;
  font-size: 48px;
  font-weight: 400;
  color: #fff;
  line-height: 1.18;
}}
.title em {{
  color: #0F7173;
  font-style: normal;
}}

.subtitle {{
  font-size: 18px;
  color: rgba(255,255,255,0.60);
  font-family: 'Georgia', serif;
  font-style: italic;
  line-height: 1.55;
  margin-top: 10px;
}}
.subtitle strong {{
  color: rgba(255,255,255,0.82);
  font-style: normal;
  font-weight: 400;
}}

.dates {{
  display: flex;
  gap: 12px;
}}
.date-pill {{
  background: rgba(255,255,255,0.07);
  border: 1px solid rgba(255,255,255,0.18);
  padding: 12px 26px;
}}
.date-day {{
  font-size: 10px;
  font-weight: 700;
  color: #0F7173;
  letter-spacing: 3px;
  text-transform: uppercase;
  font-family: 'Georgia', serif;
  margin-bottom: 3px;
}}
.date-date {{
  font-size: 21px;
  font-weight: 700;
  color: #fff;
  font-family: 'Georgia', serif;
  line-height: 1.1;
}}
.date-time {{
  font-size: 13px;
  color: rgba(255,255,255,0.50);
  font-family: 'Georgia', serif;
  margin-top: 3px;
}}

.top-bar {{
  height: 4px;
  background: #0F7173;
  flex-shrink: 0;
}}
</style>
</head>
<body>

<div class="top-bar"></div>

<div class="photos">
  <div class="photo-wrap dani">
    <div class="img"></div>
    <div class="fade"></div>
    <div class="photo-name">
      <div class="nm">Dani Magalhães</div>
      <div class="rl">CEO · Fletic — Médica</div>
    </div>
  </div>
  <div class="photo-wrap simone">
    <div class="img"></div>
    <div class="fade"></div>
    <div class="photo-name">
      <div class="nm">Simone Farah</div>
      <div class="rl">CMO · Fletic — Médica</div>
    </div>
  </div>
</div>

<div class="masterclass-bar">
  <div class="masterclass-label">
    <div class="mc-dot"></div>
    <div class="mc-text">Masterclass Gratuita</div>
  </div>
  <div class="mc-badge">Online · Ao Vivo</div>
</div>

<div class="content">
  <div>
    <div class="title">A medicina que<br>ninguém te ensinou<br>na <em>faculdade</em></div>
    <div class="subtitle">
      Gestão, carreira e <strong>modelo phygital</strong> para médicos<br>
      que querem construir algo além do plantão.
    </div>
  </div>

  <div class="dates">
    <div class="date-pill">
      <div class="date-day">Terça-feira</div>
      <div class="date-date">08 · Jul</div>
      <div class="date-time">20h30 · ao vivo</div>
    </div>
    <div class="date-pill">
      <div class="date-day">Quarta-feira</div>
      <div class="date-date">09 · Jul</div>
      <div class="date-time">20h30 · ao vivo</div>
    </div>
  </div>
</div>

</body>
</html>"""

async def main():
    async with async_playwright() as p:
        browser = await p.chromium.launch(
            executable_path="/opt/pw-browsers/chromium-1194/chrome-linux/chrome"
        )
        page = await browser.new_page(viewport={"width": 1080, "height": 1350})
        await page.set_content(HTML, wait_until="networkidle")
        await page.screenshot(path="/tmp/card_masterclass_v5.png", full_page=False)
        await browser.close()
    print("Gerado: /tmp/card_masterclass_v5.png")

asyncio.run(main())
