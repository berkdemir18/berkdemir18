# Profil görsellerini çizer: python tasarim/render.py assets  (Playwright + Chrome gerekir; img/ ve shots/ yanında olmalı)
# Kullanım: python render.py <çıktı-klasörü>   (Playwright + Chrome gerekir)
import asyncio, base64, pathlib, sys
from playwright.async_api import async_playwright
from PIL import Image

ROOT = pathlib.Path(__file__).parent
OUT = pathlib.Path(sys.argv[1]); OUT.mkdir(parents=True, exist_ok=True)

def b64(p):
    return "data:image/png;base64," + base64.b64encode((ROOT / p).read_bytes()).decode()

HEAD = """<meta charset="utf-8">
<link href="https://fonts.googleapis.com/css2?family=Bricolage+Grotesque:opsz,wght@12..96,500;12..96,700;12..96,800&family=Inter:wght@400;500&family=JetBrains+Mono:wght@500&display=swap" rel="stylesheet">
<style>
:root{--paper:#EFE1C8;--paper2:#E6D4B6;--ink:#171611;--soft:#5B5547;--rust:#A54F22;--line:#CDB995}
*{margin:0;padding:0;box-sizing:border-box}
html,body{background:transparent}
.card{position:relative;overflow:hidden;background:var(--paper);color:var(--ink);border:2.5px solid var(--ink);border-radius:20px;font-family:Inter,sans-serif;-webkit-font-smoothing:antialiased}
.card::after{content:"";position:absolute;inset:0;pointer-events:none;opacity:.35;mix-blend-mode:multiply;
 background-image:url("data:image/svg+xml;utf8,<svg xmlns='http://www.w3.org/2000/svg' width='160' height='160'><filter id='n'><feTurbulence type='fractalNoise' baseFrequency='.9' numOctaves='2'/><feColorMatrix values='0 0 0 0 .45 0 0 0 0 .38 0 0 0 0 .25 0 0 0 .35 0'/></filter><rect width='160' height='160' filter='url(%23n)'/></svg>")}
.g{font-family:'Bricolage Grotesque',sans-serif}
.m{font-family:'JetBrains Mono',monospace;font-size:12px;letter-spacing:.14em;text-transform:uppercase}
</style>"""

def banner():
    return f"""<div class="card" style="width:1200px;height:520px">
<style>
.img{{position:absolute;right:-30px;top:-10px;width:760px;height:540px;background:url({b64('img/oda.png')}) center/cover;
  -webkit-mask-image:linear-gradient(90deg,transparent 0,#000 22%)}}
.l{{position:absolute;left:52px;top:48px;width:560px}}
.k{{color:var(--soft)}}
.n{{font-size:132px;line-height:.86;font-weight:800;letter-spacing:-.045em;margin-top:26px}}
.s{{font-size:30px;line-height:1.15;font-weight:700;letter-spacing:-.02em;margin-top:26px}}
.s span{{color:var(--rust)}}
.p{{font-size:17px;line-height:1.55;color:var(--soft);margin-top:18px;width:470px}}
.cap{{position:absolute;right:28px;bottom:22px;background:var(--ink);color:var(--paper);padding:7px 12px;border-radius:8px;font-size:11px}}
</style>
<div class="img"></div>
<div class="l"><div class="m k">Berk Demir · Ankara · YBS</div>
<div class="n g">Berk.</div>
<div class="s g">Kod yazmıyorum.<br><span>Yazdırıyorum.</span></div>
<div class="p">Ne istediğimi yapay zekâya anlatıyorum, beğenmezsem geri yolluyorum. Çok geri yolluyorum. Sonunda her gün kullandığım bir şey çıkıyor.</div></div>
<div class="cap m">Fig. 1 — Demir, benim odamda, benim yerime çalışırken</div>
</div>"""

PROJ = [
    ("kukreme", "Kükreme", "Tesla çok sessizdi. Artık değil.", "Gaza bastıkça gerçek motor sesi: ivmeölçer ve GPS'ten devri tahmin edip dyno kayıtlarını çalıyor.", "Web Audio"),
    ("akilli-urun-siralama", "Akıllı Ürün Sıralama", "Tek yorumlu 5 yıldıza inanma.", "Trendyol, Hepsiburada ve Amazon'da ürünleri yorum sayısı, fiyat ve satıcıya göre yeniden diziyor.", "Chrome eklentisi"),
    ("File-Finder", "File Finder", "Windows aramasını beklemekten yaşlandım.", "NTFS'in kayıt tablosunu okuyup 5 milyon dosya arasında saniyenin altında buluyor.", "Rust · Tauri"),
    ("Ajanda", "Ajanda", "Takvimim bende dursun.", "Bilgisayarda tek dosya, Google Takvim'le iki yönlü senkron. “cuma 14:30 vize” yaz, gerisini o halleder.", "Tauri · SQLite"),
]
SMALL = [
    ("DemirTube", "YouTube'a ne kadar ömür verdiğimi söyleyen eklenti. Bazen söylemese daha iyi."),
    ("agents-sync", "Yapay zekâ asistanlarımın kaybolan dosyaları aramasından bıktım, buldurttum."),
    ("Kokpit", "Film, dizi, not, hedef. Hepsi tek yerde, hiçbiri yapılmamış."),
    ("İlerleme", "Kurs, kitap, proje. 14 gün dokunmazsan “soğumuş” der, haklıdır da."),
]

def card(slug, name, quip, desc, tag):
    return f"""<div class="card" style="width:600px;height:600px">
<style>
.w{{position:absolute;left:26px;right:26px;top:26px;height:300px;border:2.5px solid var(--ink);border-radius:12px;overflow:hidden;box-shadow:6px 6px 0 var(--ink);background:#111}}
.w img{{width:100%;height:100%;object-fit:cover;object-position:top}}
.t{{position:absolute;left:34px;right:34px;top:356px}}
.q{{font-size:16px;color:var(--rust);font-weight:700}}
.h{{font-size:46px;font-weight:800;letter-spacing:-.035em;line-height:1;margin-top:8px}}
.d{{font-size:15.5px;line-height:1.55;color:var(--soft);margin-top:12px}}
.f{{position:absolute;left:34px;right:34px;bottom:26px;display:flex;justify-content:space-between;align-items:center;border-top:2px dashed var(--line);padding-top:14px}}
.f .m{{font-size:11px;color:var(--soft)}}
.f .go{{background:var(--ink);color:var(--paper);border-radius:999px;padding:6px 14px;font-size:11px}}
</style>
<div class="w"><img src="{b64('shots/' + slug + '.png')}"></div>
<div class="t"><div class="q g">“{quip}”</div><div class="h g">{name}</div><div class="d">{desc}</div></div>
<div class="f"><span class="m">{tag}</span><span class="m go">Aç →</span></div>
</div>"""

def small(name, desc):
    return f"""<div class="card" style="width:600px;height:150px">
<style>.h{{position:absolute;left:30px;top:26px;font-size:34px;font-weight:800;letter-spacing:-.03em}}
.d{{position:absolute;left:30px;right:30px;top:76px;font-size:15px;line-height:1.5;color:var(--soft)}}
.a{{position:absolute;right:26px;top:30px;font-size:20px;font-weight:800}}</style>
<div class="h g">{name}</div><div class="a g">↗</div><div class="d">{desc}</div></div>"""

def foot():
    return f"""<div class="card" style="width:1200px;height:240px">
<style>.z{{position:absolute;left:40px;bottom:-34px;width:250px;height:250px;background:url({b64('img/uyuyor.png')}) center/contain no-repeat}}
.t{{position:absolute;left:300px;top:62px;font-size:40px;font-weight:800;letter-spacing:-.03em;line-height:1.05}}
.t span{{color:var(--rust)}}
.s{{position:absolute;left:302px;top:160px;color:var(--soft)}}
.r{{position:absolute;right:40px;bottom:30px;text-align:right;color:var(--soft);font-size:11px}}</style>
<div class="z"></div>
<div class="t g">Demir uyuyor.<br><span>Yeni proje gelince uyanır.</span></div>
<div class="s m">Beşiktaş · Ferrari · Valorant Plat · 202 film/dizi</div>
<div class="r m">Demir: Berk'in maskotu.<br>Çizimler yapay zekâ ile, fikir benden.</div>
</div>"""

JOBS = [("banner", banner())] + [(f"p-{p[0].lower()}", card(*p)) for p in PROJ] + \
       [(f"s-{n.replace('İ','I').lower()}", small(n, d)) for n, d in SMALL] + [("son", foot())]

async def main():
    async with async_playwright() as p:
        b = await p.chromium.launch(executable_path=r"C:\Program Files\Google\Chrome\Application\chrome.exe")
        pg = await b.new_page(viewport={"width": 1300, "height": 800}, device_scale_factor=2)
        for key, html in JOBS:
            await pg.set_content(f"<html><head>{HEAD}</head><body>{html}</body></html>", wait_until="networkidle")
            await pg.evaluate("document.fonts.ready")
            png = OUT / f"{key}.png"
            await (await pg.query_selector(".card")).screenshot(path=str(png), omit_background=True)
            Image.open(png).save(OUT / f"{key}.webp", quality=88, method=6)
            png.unlink()
            print(key)
        await b.close()

asyncio.run(main())
