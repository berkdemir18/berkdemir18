# Profil kartlarini cizer: python tasarim/render.py assets  (Playwright + Chrome gerekir)
import asyncio, base64, pathlib, sys
from playwright.async_api import async_playwright

ROOT = pathlib.Path(__file__).parent
OUT = pathlib.Path(sys.argv[1])
OUT.mkdir(parents=True, exist_ok=True)

THEMES = {
    "dark":  dict(bg="#13110F", surf="#1B1815", ink="#F1EADF", mute="#8C8276", faint="#5A5249", line="#2A2520", acc="#E9A23B", frame="#24201C"),
    "light": dict(bg="#F5F0E7", surf="#EDE6DA", ink="#1B1714", mute="#6F665B", faint="#A79D90", line="#DDD4C6", acc="#B4650E", frame="#E4DCCF"),
}

FONTS = '<link href="https://fonts.googleapis.com/css2?family=Instrument+Serif:ital@0;1&family=Inter:wght@400;500;600&family=JetBrains+Mono:wght@400;500&display=swap" rel="stylesheet">'

def css(t):
    v = "".join(f"--{k}:{c};" for k, c in t.items())
    return f"""
:root{{{v}}}
*{{margin:0;padding:0;box-sizing:border-box}}
html,body{{background:transparent}}
.card{{background:var(--bg);border:1px solid var(--line);border-radius:22px;overflow:hidden;position:relative;color:var(--ink);
  font-family:Inter,sans-serif;-webkit-font-smoothing:antialiased}}
.mono{{font-family:'JetBrains Mono',monospace;font-size:11px;letter-spacing:.16em;text-transform:uppercase;color:var(--mute)}}
.serif{{font-family:'Instrument Serif',serif;font-weight:400}}
.acc{{color:var(--acc)}}
"""

def b64(p):
    return "data:image/png;base64," + base64.b64encode(pathlib.Path(p).read_bytes()).decode()

def gauge(t):
    import math
    cx, cy, r = 210, 220, 180
    s = []
    for i in range(81):
        a = math.radians(205 - i * (230 / 80))
        big = i % 10 == 0
        r1 = r - (16 if big else 8)
        red = i >= 66
        col = "var(--acc)" if red else ("var(--mute)" if big else "var(--line)")
        s.append(f'<line x1="{cx+r*math.cos(a):.1f}" y1="{cy-r*math.sin(a):.1f}" x2="{cx+r1*math.cos(a):.1f}" y2="{cy-r1*math.sin(a):.1f}" stroke="{col}" stroke-width="{2 if big else 1.1}" stroke-linecap="round"/>')
        if big:
            s.append(f'<text x="{cx+(r-36)*math.cos(a):.1f}" y="{cy-(r-36)*math.sin(a)+4:.1f}" text-anchor="middle" font-family="JetBrains Mono" font-size="12" fill="{"var(--acc)" if red else "var(--faint)"}">{i//10}</text>')
    na = math.radians(205 - 58 * (230 / 80))
    s.append(f'<path d="M {cx} {cy} L {cx+(r-26)*math.cos(na):.1f} {cy-(r-26)*math.sin(na):.1f}" stroke="var(--acc)" stroke-width="2.4" stroke-linecap="round"/>')
    s.append(f'<circle cx="{cx}" cy="{cy}" r="6" fill="var(--bg)" stroke="var(--acc)" stroke-width="2.4"/>')
    s.append(f'<text x="{cx}" y="{cy+44}" text-anchor="middle" font-family="JetBrains Mono" font-size="10" letter-spacing="2" fill="var(--faint)">x1000 RPM</text>')
    return f'<svg width="420" height="300" viewBox="0 0 420 300">{"".join(s)}</svg>'

PROJ = [
    ("01", "Kükreme", "Tesla'da gaza bastıkça gerçek motor sesi. İvmeölçer ve GPS'ten devri tahmin edip dyno kayıtlarını çalıyor.", ["Web Audio", "Sensör füzyonu"], "kukreme"),
    ("02", "Akıllı Ürün Sıralama", "Trendyol, Hepsiburada ve Amazon'da ürünleri yıldıza değil yorum sayısı, fiyat ve satıcıya göre yeniden diziyor.", ["Chrome", "Manifest V3"], "akilli-urun-siralama"),
    ("03", "File Finder", "NTFS'in kendi kayıt tablosunu okuyan dosya arama. 5 milyon dosyada saniyenin altında.", ["Rust", "Tauri"], "File-Finder"),
    ("04", "Ajanda", "Takvim bilgisayarda tek dosyada, Google Takvim'le iki yönlü senkron. “cuma 14:30 vize” yazınca ekliyor.", ["TypeScript", "Tauri", "SQLite"], "Ajanda"),
]
SMALL = [
    ("05", "DemirTube", "YouTube'da neyi gerçekten izlediğini ölçen Chrome eklentisi"),
    ("06", "agents-sync", "AI talimat dosyalarındaki kırık yolları bulan CLI"),
    ("07", "Kokpit", "Film, dizi, not ve hedefler tek masaüstünde"),
    ("08", "İlerleme", "Kurs, kitap, proje: tahta aç, maddeleri yapıştır, tik at"),
]

def hero(t):
    idx = "".join(f'<div class="ix"><span class="acc">{n}</span>{name}</div>' for n, name, *_ in PROJ) + '<div class="ix"><span class="acc">05–08</span>Daha küçükler ↓</div>'
    return f"""<div class="card" style="width:1200px;height:500px">
<style>
.top{{position:absolute;left:56px;right:56px;top:44px;display:flex;justify-content:space-between}}
.name{{position:absolute;left:52px;top:108px;font-size:150px;line-height:.9;letter-spacing:-.02em}}
.name i{{color:var(--acc)}}
.sub{{position:absolute;left:58px;top:272px;width:560px;font-size:19px;line-height:1.5;color:var(--mute)}}
.sub b{{color:var(--ink);font-weight:500}}
.g{{position:absolute;right:44px;top:72px}}
.idx{{position:absolute;left:56px;right:56px;bottom:40px;display:flex;border-top:1px solid var(--line);padding-top:18px}}
.ix{{flex:1;font-family:'JetBrains Mono';font-size:12.5px;color:var(--mute);display:flex;gap:10px}}
</style>
<div class="top"><div class="mono">Berk Demir — Ankara</div><div class="mono">YBS · Ostim Teknik · 2026</div></div>
<div class="name serif">Berk <i>Demir</i></div>
<div class="sub"><b>Her gün kullandığım araçları tasarlıyorum.</b> Windows, Chrome ve arabada çalışan; fikri, kararı ve testi bana ait, kodu yapay zekâyla yazılmış küçük ürünler.</div>
<div class="g">{gauge(t)}</div>
<div class="idx">{idx}</div>
</div>"""

def card(t, n, name, desc, tags, shot):
    tg = "".join(f'<span class="tag">{x}</span>' for x in tags)
    return f"""<div class="card" style="width:600px;height:560px">
<style>
.win{{position:absolute;left:24px;right:24px;top:24px;height:318px;border-radius:12px;overflow:hidden;background:var(--frame);border:1px solid var(--line)}}
.bar{{height:26px;display:flex;align-items:center;gap:6px;padding-left:12px}}
.bar i{{width:8px;height:8px;border-radius:50%;background:var(--line)}}
.win img{{display:block;width:100%;height:292px;object-fit:cover;object-position:top}}
.meta{{position:absolute;left:32px;right:32px;top:372px}}
.row{{display:flex;justify-content:space-between;align-items:baseline}}
.t{{font-size:44px;line-height:1;margin-top:10px;letter-spacing:-.01em}}
.d{{font-size:15px;line-height:1.55;color:var(--mute);margin-top:12px;max-width:520px}}
.tags{{position:absolute;left:32px;bottom:26px;display:flex;gap:8px}}
.tag{{font-family:'JetBrains Mono';font-size:11px;color:var(--mute);border:1px solid var(--line);border-radius:999px;padding:4px 10px}}
.go{{position:absolute;right:32px;bottom:30px;font-family:'JetBrains Mono';font-size:11.5px;color:var(--acc);letter-spacing:.08em}}
</style>
<div class="win"><div class="bar"><i></i><i></i><i></i></div><img src="{b64(ROOT/'shots'/(shot+'.png'))}"></div>
<div class="meta"><div class="row"><span class="mono acc">{n}</span></div><div class="t serif">{name}</div><div class="d">{desc}</div></div>
<div class="tags">{tg}</div><div class="go">AÇ →</div>
</div>"""

def small(t, n, name, desc):
    return f"""<div class="card" style="width:600px;height:128px">
<style>
.s{{position:absolute;left:32px;right:32px;top:30px}}
.t{{font-size:34px;line-height:1;margin-top:8px}}
.d{{position:absolute;right:32px;top:0;bottom:0;width:250px;display:flex;align-items:center;justify-content:flex-end;text-align:right;font-size:14px;line-height:1.5;color:var(--mute)}}
</style>
<div class="s"><span class="mono acc">{n}</span><div class="t serif">{name}</div></div><div class="d">{desc}</div>
</div>"""

def foot(t):
    return f"""<div class="card" style="width:1200px;height:96px;border:none;background:transparent">
<style>.f{{position:absolute;inset:0;display:flex;align-items:center;justify-content:center;gap:28px}}
.f span{{font-family:'JetBrains Mono';font-size:11.5px;letter-spacing:.16em;text-transform:uppercase;color:var(--faint)}}
.f i{{width:4px;height:4px;border-radius:50%;background:var(--acc)}}</style>
<div class="f"><span>Beşiktaş</span><i></i><span>Ferrari</span><i></i><span>Kod: yapay zekâ · Karar: ben</span></div></div>"""

JOBS = [("hero", hero, ())] + [(f"p{p[0]}", card, p) for p in PROJ] + [(f"s{s[0]}", small, s) for s in SMALL] + [("foot", foot, ())]

async def main():
    async with async_playwright() as p:
        b = await p.chromium.launch(executable_path=r"C:\Program Files\Google\Chrome\Application\chrome.exe")
        pg = await b.new_page(viewport={"width": 1300, "height": 800}, device_scale_factor=2)
        for theme, t in THEMES.items():
            for key, fn, args in JOBS:
                await pg.set_content(f"<html><head><meta charset='utf-8'>{FONTS}<style>{css(t)}</style></head><body>{fn(t, *args)}</body></html>", wait_until="networkidle")
                await pg.evaluate("document.fonts.ready")
                el = await pg.query_selector(".card")
                png = OUT / f"{key}-{theme}.png"
                await el.screenshot(path=str(png), omit_background=True)
        await b.close()

asyncio.run(main())
