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
.card::after{content:"";position:absolute;inset:0;pointer-events:none;opacity:.35;
 background-image:url("data:image/svg+xml;utf8,<svg xmlns='http://www.w3.org/2000/svg' width='160' height='160'><filter id='n'><feTurbulence type='fractalNoise' baseFrequency='.9' numOctaves='2'/><feColorMatrix values='0 0 0 0 .45 0 0 0 0 .38 0 0 0 0 .25 0 0 0 .35 0'/></filter><rect width='160' height='160' filter='url(%23n)'/></svg>")}
.g{font-family:'Bricolage Grotesque',sans-serif}
.m{font-family:'JetBrains Mono',monospace;font-size:12px;letter-spacing:.14em;text-transform:uppercase}
</style>"""

def banner():
    return f"""<div class="card" style="width:1200px;height:520px;background:#F0D9B8">
<style>
.img{{position:absolute;right:0;top:0;width:680px;height:520px;background:url({b64('img/ciraklar.png')}) right center/auto 100% no-repeat;
  -webkit-mask-image:linear-gradient(90deg,transparent 0,#000 8%)}}
.l{{position:absolute;left:52px;top:48px;width:560px}}
.k{{color:var(--soft)}}
.n{{font-size:132px;line-height:.86;font-weight:800;letter-spacing:-.045em;margin-top:26px}}
.s{{font-size:30px;line-height:1.15;font-weight:700;letter-spacing:-.02em;margin-top:26px}}
.s span{{color:var(--rust)}}
.p{{font-size:17px;line-height:1.55;color:var(--soft);margin-top:18px;width:470px}}
.cap{{position:absolute;right:28px;bottom:22px;background:var(--ink);color:var(--paper);padding:7px 12px;border-radius:8px;font-size:11px}}
</style>
<div class="img"></div>
<div class="l"><div class="m k">github.com/berkdemir18</div>
<div class="n g">Berk.</div>
<div class="s g">Kod yazmıyorum.<br><span>Yazdırıyorum.</span></div>
<div class="p">Ne istediğimi yapay zekâya anlatıyorum, beğenmezsem geri yolluyorum. Çok geri yolluyorum. Sonunda her gün kullandığım bir şey çıkıyor.</div></div>
<div class="cap m">Fig. 1 — Demir, çıraklarına iş yaptırırken</div>
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


def heading(no, title, sub):
    return f"""<div class="card" style="width:1200px;height:110px;border:none;background:transparent">
<style>.card::after{{display:none}}
.hd{{position:absolute;left:8px;right:8px;bottom:22px;display:flex;align-items:baseline;gap:18px}}
.hd .n{{color:var(--rust);font-size:13px}}
.hd .t{{font-size:44px;font-weight:800;letter-spacing:-.035em;color:#8C7E66}}
.hd .s{{margin-left:auto;font-size:12px;color:#8C7E66}}
.ln{{position:absolute;left:8px;right:8px;bottom:8px;border-top:2px dashed #8C7E66;opacity:.55}}</style>
<div class="hd"><span class="m n">{no}</span><span class="t g">{title}</span><span class="m s">{sub}</span></div><div class="ln"></div></div>"""

STEPS = [
    ("fikir", "01", "Fikir", "Bir şey canımı sıkıyor. Windows araması mesela."),
    ("tabela", "02", "Tarif", "Ne istediğimi anlatıyorum. Uzun uzun."),
    ("laptop", "03", "Çırak yazar", "Kodu yapay zekâ yazıyor. Ben çay koyuyorum."),
    ("facepalm", "04", "Olmamış", "Deniyorum, beğenmiyorum, geri yolluyorum."),
    ("oldu", "05", "Oldu", "Her gün kullanıyorsam yayına çıkıyor."),
]

def process():
    cols = "".join(f"""<div class="st"><div class="im" style="background-image:url({b64('img/' + k + '.png')})"></div>
<div class="m n">{n}</div><div class="h g">{t}</div><div class="d">{d}</div></div>""" for k, n, t, d in STEPS)
    return f"""<div class="card" style="width:1200px;height:520px">
<style>
.row{{position:absolute;left:30px;right:30px;top:40px;display:flex;gap:16px}}
.st{{flex:1;position:relative}}
.im{{height:210px;background:center bottom/contain no-repeat}}
.st:nth-child(2) .im{{position:relative}}
.n{{color:var(--rust);margin-top:22px;font-size:11px}}
.h{{font-size:30px;font-weight:800;letter-spacing:-.03em;margin-top:6px}}
.d{{font-size:14.5px;line-height:1.5;color:var(--soft);margin-top:8px;padding-right:6px}}
.sign{{position:absolute;left:30px;top:44px;width:208px;text-align:center;font-family:'Bricolage Grotesque';font-weight:800;font-size:15px;line-height:1.1;transform:translateX(0)}}
.loop{{position:absolute;left:500px;right:270px;bottom:46px;height:46px;border:2.5px dashed var(--rust);border-top:none;border-radius:0 0 26px 26px}}
.loop::before{{content:"";position:absolute;left:-9px;top:-10px;border:8px solid transparent;border-bottom:12px solid var(--rust);border-top:none}}
.lt{{position:absolute;left:0;right:0;bottom:-30px;text-align:center;color:var(--rust);font-size:11px}}
</style>
<div class="row">{cols}</div>
<div class="sign" style="left:306px;top:58px;width:138px">ŞÖYLE<br>OLSUN</div>
<div class="loop"><div class="lt m">↺ gerektiği kadar tur</div></div>
</div>"""

def stats():
    nums = [("8", "proje"), ("12", "sürüm"), ("61", "commit"), ("0", "satır elle kod")]
    cells = "".join(f'<div class="c"><div class="v g">{v}</div><div class="m l">{l}</div></div>' for v, l in nums)
    return f"""<div class="card" style="width:1200px;height:230px">
<style>.cay{{position:absolute;right:40px;bottom:-6px;width:210px;height:230px;background:url({b64('img/cay.png')}) center bottom/contain no-repeat}}
.cs{{position:absolute;left:40px;right:290px;top:46px;display:flex}}
.c{{flex:1;border-left:2px dashed var(--line);padding-left:22px}}
.c:first-child{{border:none;padding-left:0}}
.v{{font-size:84px;font-weight:800;letter-spacing:-.05em;line-height:.9}}
.c:last-child .v{{color:var(--rust)}}
.l{{margin-top:12px;color:var(--soft);font-size:11px}}
.nt{{position:absolute;left:40px;bottom:24px;color:var(--soft);font-size:10.5px}}</style>
<div class="cs">{cells}</div><div class="cay"></div>
<div class="nt m">Ekim 2026 itibarıyla · public repolar</div></div>"""

def foot():
    return f"""<div class="card" style="width:1200px;height:240px">
<style>.z{{position:absolute;left:40px;bottom:-34px;width:250px;height:250px;background:url({b64('img/uyuyor.png')}) center/contain no-repeat}}
.t{{position:absolute;left:300px;top:76px;font-size:40px;font-weight:800;letter-spacing:-.03em;line-height:1.05}}
.t span{{color:var(--rust)}}
.s{{position:absolute;left:302px;top:160px;color:var(--soft)}}
.r{{position:absolute;right:40px;bottom:30px;text-align:right;color:var(--soft);font-size:11px}}</style>
<div class="z"></div>
<div class="t g">Demir uyuyor.<br><span>Yeni proje gelince uyanır.</span></div>
<div class="r m">Demir: maskot.<br>Çizimler yapay zekâ ile.</div>
</div>"""

JOBS = [("banner", banner()), ("h-isler", heading("01", "İşler", "Her gün kullandıklarım")), ("h-kucukler", heading("02", "Küçükler", "Bir derdi çözen ufak şeyler")), ("h-surec", heading("03", "Nasıl çıkıyor", "Kod yok, tarif var")), ("surec", process()), ("rakam", stats())] + [(f"p-{p[0].lower()}", card(*p)) for p in PROJ] + \
       [(f"s-{n.replace('İ','I').lower()}", small(n, d)) for n, d in SMALL] + [("son", foot())]

async def main():
    async with async_playwright() as p:
        b = await p.chromium.launch(executable_path=r"C:\Program Files\Google\Chrome\Application\chrome.exe")
        pg = await b.new_page(viewport={"width": 1300, "height": 800}, device_scale_factor=2)
        for key, html in JOBS:
            await pg.set_content(f"<html lang='tr'><head>{HEAD}</head><body>{html}</body></html>", wait_until="networkidle")
            await pg.evaluate("document.fonts.ready")
            png = OUT / f"{key}.png"
            await (await pg.query_selector(".card")).screenshot(path=str(png), omit_background=True)
            Image.open(png).save(OUT / f"{key}.webp", quality=88, method=6)
            png.unlink()
            print(key)
        await b.close()

asyncio.run(main())
