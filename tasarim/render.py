# Profil görsellerini çizer: python tasarim/render.py assets/v6  (Playwright + Chrome gerekir; shots/ yanında olmalı. Tasarım değişince klasör adını artır: GitHub aynı adlı görseli önbellekten verir)
# Tek tema: koyu terminal. GitHub'ın açık temasında da terminal penceresi gibi durur.
import asyncio, base64, pathlib, sys
from playwright.async_api import async_playwright
from PIL import Image

ROOT = pathlib.Path(__file__).parent
OUT = pathlib.Path(sys.argv[1]); OUT.mkdir(parents=True, exist_ok=True)

def b64(p):
    return "data:image/png;base64," + base64.b64encode((ROOT / p).read_bytes()).decode()

HEAD = """<meta charset="utf-8">
<link href="https://fonts.googleapis.com/css2?family=JetBrains+Mono:wght@400;500;700;800&family=Inter:wght@400;500;600;700&display=swap" rel="stylesheet">
<style>
:root{--bg:#0A0D0C;--panel:#0E1311;--bar:#121916;--line:#1E2925;--text:#E4ECE8;--dim:#8B9A93;--mute:#56645D;--acc:#4ADE80;--warn:#F2B84B;--err:#F07167}
*{margin:0;padding:0;box-sizing:border-box}
html,body{background:transparent}
.card{position:relative;overflow:hidden;background:var(--bg);color:var(--text);border:1.5px solid var(--line);border-radius:14px;font-family:Inter,sans-serif;-webkit-font-smoothing:antialiased}
.card::before{content:"";position:absolute;inset:0;pointer-events:none;
 background-image:linear-gradient(var(--line) 1px,transparent 1px),linear-gradient(90deg,var(--line) 1px,transparent 1px);background-size:40px 40px;opacity:.35;
 -webkit-mask-image:radial-gradient(ellipse at 70% 30%,#000 0,transparent 75%)}
.card>*{position:relative}
.m{font-family:'JetBrains Mono',monospace}
.acc{color:var(--acc)} .dim{color:var(--dim)} .mute{color:var(--mute)} .warn{color:var(--warn)} .err{color:var(--err)}
.bar{height:44px;display:flex;align-items:center;gap:14px;padding:0 18px;border-bottom:1.5px solid var(--line);background:var(--bar);font-family:'JetBrains Mono';font-size:14px;color:var(--dim)}
.bar .sq{display:flex;gap:7px}.bar .sq i{width:11px;height:11px;border-radius:3px;background:var(--line)}
.bar .st{margin-left:auto;display:flex;align-items:center;gap:8px}
.bar .st b{width:8px;height:8px;border-radius:50%;background:var(--acc)}
.shot{border:1.5px solid var(--line);border-radius:10px;overflow:hidden;background:#000}
.shot img{width:100%;height:100%;object-fit:cover;object-position:top;display:block}
.chip{display:inline-block;font-family:'JetBrains Mono';font-size:13px;color:var(--dim);border:1.5px solid var(--line);border-radius:6px;padding:4px 9px;margin-right:6px}
.chip.g{color:var(--acc);border-color:#1F4A33;background:#0F1F17}
.cur{display:inline-block;width:.4em;height:.82em;background:var(--acc);vertical-align:-.06em;margin-left:.08em}
</style>"""

def bar(path, status="çalışıyor"):
    return f'<div class="bar"><span class="sq"><i></i><i></i><i></i></span><span>{path}</span><span class="st"><b></b>{status}</span></div>'

LOG = [
    ("12:04:11", "intent", "dim", '"windows araması yavaş, düzelt"', ""),
    ("12:04:13", "plan", "dim", "ajan → mimari, 4 adım", ""),
    ("12:09:40", "build", "dim", "ajan yazdı: 1.284 satır", ""),
    ("12:10:02", "review", "err", 'berk: "olmamış"', '<span class="err">✗</span>'),
    ("12:31:55", "build", "dim", "ajan baştan yazdı", ""),
    ("12:32:20", "review", "acc", 'berk: "oldu bu iş"', '<span class="acc">✓</span>'),
    ("12:32:21", "scan", "acc", "sır taraması: 0 sızıntı", '<span class="acc">✓</span>'),
    ("12:32:30", "ship", "acc", "file-finder v0.1.1 yayında", '<span class="acc">✓</span>'),
]

def banner():
    rows = "".join(f'<div class="r"><span class="mute">{t}</span><span class="k {c}">{k}</span><span class="v">{v}</span><span class="ok">{ok}</span></div>' for t, k, c, v, ok in LOG)
    return f"""<div class="card" style="width:1200px;height:560px">
<style>
.l{{position:absolute;left:48px;top:84px;width:520px}}
.p{{font-size:20px}}
.n{{font-size:128px;font-weight:800;letter-spacing:-.06em;line-height:1;margin-top:14px}}
.s{{font-size:34px;font-weight:700;letter-spacing:-.025em;line-height:1.15;margin-top:26px}}
.d{{font-size:18px;line-height:1.6;color:var(--dim);margin-top:18px;width:470px}}
.lg{{position:absolute;right:36px;top:84px;width:560px;height:436px;background:var(--panel);border:1.5px solid var(--line);border-radius:10px;padding:20px 22px;font-family:'JetBrains Mono';font-size:14.5px}}
.lg .h{{display:flex;justify-content:space-between;color:var(--mute);border-bottom:1.5px dashed var(--line);padding-bottom:12px;margin-bottom:12px}}
.r{{display:grid;grid-template-columns:86px 72px 1fr 18px;gap:10px;line-height:2.15}}
.r .v{{color:var(--text)}}
.lg .f{{position:absolute;left:22px;right:22px;bottom:18px;color:var(--mute);font-size:13px}}
</style>
{bar("berk@github: ~", "online")}
<div class="l"><div class="p m"><span class="acc">$</span> whoami</div>
<div class="n m">berk<span class="cur"></span></div>
<div class="s">Kod yazmıyorum.<br><span class="acc">Yazdırıyorum.</span></div>
<div class="d">Ne istediğimi yapay zekâ ajanlarına tarif ediyorum, çıkanı deniyorum, beğenmezsem geri yolluyorum. Çok geri yolluyorum.</div></div>
<div class="lg"><div class="h"><span>tail -f build.log</span><span>tipik bir gün</span></div>{rows}
<div class="f">// gerçek log değil ama gerçeğe çok yakın</div></div>
</div>"""

def heading(no, path, note):
    return f"""<div class="card" style="width:1200px;height:104px;border:none;background:transparent">
<style>.card::before{{display:none}}
.hd{{position:absolute;left:6px;right:6px;bottom:24px;display:flex;align-items:baseline;gap:18px;font-family:'JetBrains Mono'}}
.hd .n{{font-size:16px;color:var(--mute)}}
.hd .t{{font-size:40px;font-weight:800;letter-spacing:-.04em;color:#C9D4CF}}
.hd .t span{{color:var(--acc)}}
.hd .s{{margin-left:auto;font-size:15px;color:var(--mute)}}
.ln{{position:absolute;left:6px;right:6px;bottom:8px;border-top:1.5px dashed #56645D;opacity:.6}}</style>
<div class="hd"><span class="n">{no}</span><span class="t"><span>~/</span>{path}</span><span class="s"># {note}</span></div><div class="ln"></div></div>"""

def hero():
    return f"""<div class="card" style="width:1200px;height:500px">
<style>
.w{{position:absolute;right:30px;top:74px;width:704px;height:396px}}
.t{{position:absolute;left:36px;top:80px;width:400px}}
.q{{font-family:'JetBrains Mono';font-size:16px;color:var(--mute);margin-top:22px;line-height:1.5}}
.h{{font-family:'JetBrains Mono';font-size:60px;font-weight:800;letter-spacing:-.05em;line-height:1;margin-top:10px}}
.d{{font-size:18px;line-height:1.6;color:var(--dim);margin-top:16px}}
.f{{position:absolute;left:36px;width:400px;bottom:30px;display:flex;justify-content:space-between;align-items:center}}
.go{{font-family:'JetBrains Mono';font-size:15px;color:var(--acc)}}
</style>
{bar("~/berkos — son commit 2026-10-28", "yayında")}
<div class="w shot"><img src="{b64('shots/berkos.png')}"></div>
<div class="t"><span class="chip g">[yeni]</span><span class="chip">v1.1</span>
<div class="q">// televizyon açılınca reklam değil, saat karşılasın.</div>
<div class="h">BerkOS</div>
<div class="d">Google TV için sakin bir ana ekran: saat, hava, maçlar, kaldığın yer ve boşta dönen tablolar.</div></div>
<div class="f"><span><span class="chip">google tv</span><span class="chip">android</span></span><span class="go">aç ↗</span></div>
</div>"""

PROJ = [
    ("DemirTube", "DemirTube", "youtube'a ne kadar ömür verdim?", "İzleme geçmişini sadece cihazında tutup analiz eden Chrome eklentisi: süre bütçesi, pişmanlık oranı, kanal karnesi.", ["chrome", "react"], "veri cihazda"),
    ("agents-sync", "agents-sync", "ajanlar olmayan dosyaya bakıyordu.", "CLAUDE.md, AGENTS.md ve .cursorrules içindeki kırık dosya yollarını bulan, doğrusunu öneren linter.", ["node", "cli"], None),
    ("File-Finder", "File Finder", "windows aramasını beklemekten yaşlandım.", "NTFS'in kayıt tablosunu okuyup 5 milyon dosya arasında saniyenin altında buluyor.", ["rust", "tauri"], "çevrimdışı"),
    ("Ajanda", "Ajanda", "takvimim bende dursun.", "Bilgisayarda tek dosya, Google Takvim'le iki yönlü senkron. “cuma 14:30 vize” yaz, gerisini o halleder.", ["tauri", "sqlite"], "veri cihazda"),
]
SMALL = [
    ("Kükreme", "Tesla'da gaza bastıkça gerçek motor sesi. Tesla çok sessizdi, artık değil.", None),
    ("Akıllı-Ürün", "Trendyol, Hepsiburada, Amazon'da ürünleri yıldıza değil kanıta göre dizer.", None),
    ("Kokpit", "Film, dizi, not, hedef. Hepsi tek yerde, hiçbiri yapılmamış.", "veri cihazda"),
    ("İlerleme", "Kurs, kitap, proje. 14 gün dokunmazsan “soğumuş” der, haklıdır da.", None),
]

def card(slug, name, quip, desc, tags, lock):
    chips = "".join(f'<span class="chip">{t}</span>' for t in tags) + (f'<span class="chip g">⛨ {lock}</span>' if lock else "")
    return f"""<div class="card" style="width:600px;height:640px">
<style>
.w{{position:absolute;left:22px;right:22px;top:66px;height:300px}}
.t{{position:absolute;left:28px;right:28px;top:390px}}
.q{{font-family:'JetBrains Mono';font-size:15px;color:var(--mute)}}
.h{{font-family:'JetBrains Mono';font-size:40px;font-weight:800;letter-spacing:-.05em;line-height:1;margin-top:10px}}
.d{{font-size:17.5px;line-height:1.55;color:var(--dim);margin-top:12px}}
.f{{position:absolute;left:28px;right:28px;bottom:24px;display:flex;justify-content:space-between;align-items:center}}
.go{{font-family:'JetBrains Mono';font-size:15px;color:var(--acc)}}
</style>
{bar("~/" + slug.lower())}
<div class="w shot"><img src="{b64('shots/' + slug + '.png')}"></div>
<div class="t"><div class="q">// {quip}</div><div class="h">{name}</div><div class="d">{desc}</div></div>
<div class="f"><span>{chips}</span><span class="go">aç ↗</span></div>
</div>"""

def small(name, desc, lock):
    tag = f'<span class="chip g">⛨ {lock}</span>' if lock else ""
    return f"""<div class="card" style="width:600px;height:180px">
<style>.h{{position:absolute;left:26px;top:26px;font-family:'JetBrains Mono';font-size:26px;font-weight:800;letter-spacing:-.04em}}
.h .acc{{font-weight:500}}
.d{{position:absolute;left:26px;right:26px;top:76px;font-size:17px;line-height:1.55;color:var(--dim)}}
.a{{position:absolute;right:24px;top:26px;display:flex;align-items:center;gap:12px;font-family:'JetBrains Mono';font-size:18px;color:var(--acc)}}</style>
<div class="h"><span class="acc">$ ./</span>{name.replace("İ", "i").lower()}</div><div class="a">{tag}↗</div><div class="d">{desc}</div></div>"""

STEPS = [
    ("01", "fikir", "Bir şey canımı sıkıyor. Windows araması mesela."),
    ("02", "tarif", "Ne istediğimi anlatıyorum. Uzun uzun, örnekle."),
    ("03", "ajan yazar", "Kodu yapay zekâ yazıyor. Ben mimariyi tutuyorum."),
    ("04", "dene + tara", "Kullanıyorum, kırmaya çalışıyorum, sır taraması."),
    ("05", "ship", "Her gün kullanıyorsam yayına çıkıyor."),
]

def process():
    nodes = "".join(f"""<div class="nd{' on' if n == '05' else ''}"><div class="k m">{n}</div><div class="h m">{t}</div><div class="d">{d}</div></div>""" + ('<div class="ar m">→</div>' if n != "05" else "") for n, t, d in STEPS)
    agents = "".join(f'<span class="chip">{a}</span>' for a in ["claude", "gemini", "glm", "deepseek"])
    return f"""<div class="card" style="width:1200px;height:430px">
<style>
.row{{position:absolute;left:30px;right:30px;top:80px;display:flex;align-items:stretch}}
.nd{{flex:1;background:var(--panel);border:1.5px solid var(--line);border-radius:10px;padding:18px 16px 20px}}
.nd.on{{border-color:#1F4A33;background:#0F1F17}}
.nd .k{{font-size:13px;color:var(--mute)}}
.nd .h{{font-size:22px;font-weight:800;letter-spacing:-.04em;margin-top:8px}}
.nd.on .h{{color:var(--acc)}}
.nd .d{{font-size:15.5px;line-height:1.5;color:var(--dim);margin-top:8px}}
.ar{{width:34px;display:flex;align-items:center;justify-content:center;color:var(--mute);font-size:20px}}
.loop{{position:absolute;left:520px;width:440px;top:282px;height:40px;border:1.5px dashed var(--err);border-top:none;border-radius:0 0 18px 18px}}
.loop::before{{content:"";position:absolute;left:-7px;top:-9px;border:6px solid transparent;border-bottom:10px solid var(--err);border-top:none}}
.lt{{position:absolute;left:0;right:0;bottom:-28px;text-align:center;font-size:13.5px;color:var(--err)}}
.ag{{position:absolute;left:30px;bottom:28px;font-family:'JetBrains Mono';font-size:14px;color:var(--mute);display:flex;align-items:center;gap:12px}}
</style>
{bar("~/surec — nasıl çıkıyor", "döngüde")}
<div class="row">{nodes}</div>
<div class="loop"><div class="lt m">olmamış → baştan · gerektiği kadar tur</div></div>
<div class="ag">masadaki ajanlar:<span>{agents}</span></div>
</div>"""

def stats():
    nums = [("9", "proje"), ("13", "sürüm"), ("63", "commit"), ("0", "satır elle kod")]
    cells = "".join(f'<div class="c"><div class="v m">{v}</div><div class="l m">{l}</div></div>' for v, l in nums)
    return f"""<div class="card" style="width:1200px;height:250px">
<style>
.cs{{position:absolute;left:36px;right:36px;top:78px;display:flex}}
.c{{flex:1;border-left:1.5px dashed var(--line);padding-left:26px}}
.c:first-child{{border:none;padding-left:0}}
.v{{font-size:80px;font-weight:800;letter-spacing:-.06em;line-height:.95}}
.c:last-child .v{{color:var(--acc)}}
.l{{margin-top:12px;color:var(--dim);font-size:15px}}
</style>
{bar("~/ $ stats --public", "ekim 2026")}
<div class="cs">{cells}</div></div>"""

def foot():
    return f"""<div class="card" style="width:1200px;height:200px">
<style>.t{{position:absolute;left:40px;top:42px;font-family:'JetBrains Mono';font-size:20px;line-height:1.8}}
.b{{font-size:30px;font-weight:800;letter-spacing:-.04em;color:var(--text)}}
.r{{position:absolute;right:40px;bottom:34px;text-align:right;font-family:'JetBrains Mono';font-size:14px;line-height:1.7;color:var(--mute)}}</style>
<div class="t"><div><span class="acc">$</span> exit</div><div class="b">oturum kapandı. yeni proje gelince tekrar bağlanır<span class="cur"></span></div></div>
<div class="r">yapım malzemesi: tarif, sabır<br>ve çok fazla “olmamış”</div>
</div>"""

JOBS = [("banner", banner()), ("hero-berkos", hero()),
        ("h-isler", heading("01", "isler", "her gün kullandıklarım")), ("h-kucukler", heading("02", "kucukler", "bir derdi çözen ufak şeyler")),
        ("h-surec", heading("03", "surec", "kod yok, tarif var")), ("surec", process()), ("rakam", stats())] + \
       [(f"p-{p[0].lower()}", card(*p)) for p in PROJ] + \
       [("s-" + s[0].translate(str.maketrans("İıüÜşŞçÇğĞöÖ", "iiuussccggoo")).lower(), small(*s)) for s in SMALL] + [("son", foot())]

async def main():
    async with async_playwright() as p:
        b = await p.chromium.launch(executable_path=r"C:\Program Files\Google\Chrome\Application\chrome.exe")
        pg = await b.new_page(viewport={"width": 1300, "height": 800}, device_scale_factor=2)
        for key, html in JOBS:
            await pg.set_content(f"<html lang='tr'><head>{HEAD}</head><body>{html}</body></html>", wait_until="networkidle")
            await pg.evaluate("document.fonts.ready")
            png = OUT / f"{key}.png"
            await (await pg.query_selector(".card")).screenshot(path=str(png), omit_background=True)
            Image.open(png).save(OUT / f"{key}.webp", quality=90, method=6)
            png.unlink()
            print(key)
        await b.close()

asyncio.run(main())
