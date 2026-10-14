// Profildeki sohbet balonlarını çizer (assets/sohbet-{dark,light}.svg).
// Canlı kısımlar: Ankara'da şu anki hava (open-meteo, anahtar gerekmez) ve en son yayınlanan sürüm.
import { readFileSync, writeFileSync } from "node:fs";

const KULLANICI = "berkdemir18";
const DEPOLAR = ["kukreme", "akilli-urun-siralama", "DemirTube", "ilerleme", "Ajanda", "agents-sync", "File-Finder", "Kokpit"];
const token = process.env.GITHUB_TOKEN;

async function api(yol) {
  const r = await fetch(`https://api.github.com/${yol}`, {
    headers: { Accept: "application/vnd.github+json", ...(token && { Authorization: `Bearer ${token}` }) },
  });
  if (r.status === 404) return null;
  if (!r.ok) throw new Error(`${yol}: HTTP ${r.status}`);
  return r.json();
}

// --- en son yayın
let son = null;
for (const depo of DEPOLAR) {
  const y = await api(`repos/${KULLANICI}/${depo}/releases/latest`);
  if (y && (!son || y.published_at > son.tarih)) son = { depo, etiket: y.tag_name, tarih: y.published_at };
}

// --- Ankara havası
const HAVA = [
  [[0], "açık", "☀️"], [[1, 2], "parçalı bulutlu", "⛅"], [[3], "kapalı", "☁️"], [[45, 48], "sisli", "🌫️"],
  [[51, 53, 55, 56, 57], "çiseliyor", "🌦️"], [[61, 63, 65, 66, 67, 80, 81, 82], "yağmurlu", "🌧️"],
  [[71, 73, 75, 77, 85, 86], "karlı", "🌨️"], [[95, 96, 99], "fırtınalı", "⛈️"],
];
let havaCumle = "bilmiyorum, dışarı çıkmadım.";
try {
  const r = await fetch("https://api.open-meteo.com/v1/forecast?latitude=39.93&longitude=32.86&current=temperature_2m,weather_code&timezone=Europe%2FIstanbul");
  const { current } = await r.json();
  const [, ad, ikon] = HAVA.find(([k]) => k.includes(current.weather_code)) ?? [, "garip", "🤷"];
  const derece = Math.round(current.temperature_2m);
  const yorum = derece <= 5 ? "Demir bile üşüyor." : derece >= 30 ? "Demir eriyor." : ad === "yağmurlu" ? "Tesla yıkanmış oldu." : "idare eder.";
  havaCumle = `Ankara'da şu an ${derece}°C, ${ad} ${ikon} ${yorum}`;
} catch {}

const aylar = ["Ocak", "Şubat", "Mart", "Nisan", "Mayıs", "Haziran", "Temmuz", "Ağustos", "Eylül", "Ekim", "Kasım", "Aralık"];
const gun = (iso) => { const d = new Date(iso); return `${d.getUTCDate()} ${aylar[d.getUTCMonth()]}`; };

const SOHBET = [
  ["o", "selam, sen kimsin?"],
  ["b", "Berk. 19 yaşındayım, Ankara'dayım, Ostim Teknik'te YBS okuyorum."],
  ["o", "yazılımcısın yani"],
  ["b", "Değilim. Hayatımda elle tek satır kod yazmadım."],
  ["b", "Ne istediğimi yapay zekâya anlatıyorum, olmamışsa geri yolluyorum. Bu repoların hepsi öyle çıktı."],
  ["o", "en sevdiğin hangisi?"],
  ["b", "Kükreme. Elektrikli arabada gaza basınca gerçek motor sesi geliyor. Tesla'nın ruhu yoktu, verdik."],
  ["o", "en son ne çıkardın?"],
  ["b", son ? `${son.depo} ${son.etiket}, ${gun(son.tarih)}. Demir test etti, beğenmedi, yine de çıkardım.` : "Şu an bir şey yok. Demir uyuyor."],
  ["o", "hava nasıl orda?"],
  ["b", havaCumle],
  ["o", "beşiktaş?"],
  ["b", "sorma."],
];

// --- çizim
const TEMA = {
  dark: { zemin: "#0D1117", o: "#262A31", oYazi: "#E6EDF3", b: "#A54F22", bYazi: "#FFF6EA", soluk: "#7D8590" },
  light: { zemin: "#FFFFFF", o: "#ECEDEF", oYazi: "#1F2328", b: "#A54F22", bYazi: "#FFF6EA", soluk: "#8B949E" },
};
const FONT = "-apple-system, BlinkMacSystemFont, 'Segoe UI', 'Helvetica Neue', Arial, sans-serif";
const avatar = "data:image/png;base64," + readFileSync(new URL("./avatar96.png", import.meta.url)).toString("base64");
const kac = (s) => s.replace(/&/g, "&amp;").replace(/</g, "&lt;").replace(/>/g, "&gt;");

// Kaba genişlik tahmini (17px sistem fontu): dar harfler daha az yer kaplar.
const genislik = (s) => K * [...s].reduce((t, c) => t + (/[iılIj.,:'’ !|]/.test(c) ? 4.6 : /[mwMWğĞ]/.test(c) ? 13.5 : /\p{Extended_Pictographic}/u.test(c) ? 20 : /[A-ZÇÖŞÜİ]/.test(c) ? 11 : 8.9), 0);
function sar(metin, max) {
  const satirlar = [""];
  for (const k of metin.split(" ")) {
    const aday = satirlar.at(-1) ? `${satirlar.at(-1)} ${k}` : k;
    if (genislik(aday) > max && satirlar.at(-1)) satirlar.push(k);
    else satirlar[satirlar.length - 1] = aday;
  }
  return satirlar;
}

const K = 1.3; // 17px tahmin tablosu → 22px
const W = 1200, MAX = 640, SATIR = 30, PX = 22, PY = 14, ARA = 7, GRUP = 20;
function ciz(t) {
  const p = [];
  let y = 40;
  SOHBET.forEach(([kim, metin], i) => {
    const onceki = SOHBET[i - 1]?.[0], sonraki = SOHBET[i + 1]?.[0];
    if (i && onceki !== kim) y += GRUP - ARA;
    const satirlar = sar(metin, MAX);
    const bw = Math.ceil(Math.max(...satirlar.map(genislik))) + PX * 2;
    const bh = satirlar.length * SATIR + PY * 2 - 3;
    const sag = kim === "b";
    const x = sag ? W - 96 - bw : 40;
    const gecikme = (i * 0.35).toFixed(2);
    p.push(`<g class="m" style="animation-delay:${gecikme}s">`);
    p.push(`<rect x="${x}" y="${y}" width="${bw}" height="${bh}" rx="24" fill="${sag ? t.b : t.o}"/>`);
    satirlar.forEach((s, j) => p.push(`<text x="${x + PX}" y="${y + PY + 22 + j * SATIR}" font-family="${FONT}" font-size="22" fill="${sag ? t.bYazi : t.oYazi}">${kac(s)}</text>`));
    if (sag && sonraki !== "b") p.push(`<image href="${avatar}" x="${W - 84}" y="${y + bh - 58}" width="58" height="58"/>`);
    p.push(`</g>`);
    y += bh + ARA;
  });
  y += 22;
  p.push(`<text x="${W - 96}" y="${y}" text-anchor="end" font-family="${FONT}" font-size="15" fill="${t.soluk}">Okundu · her gün kendiliğinden güncellenir</text>`);
  const H = y + 24;
  return `<svg xmlns="http://www.w3.org/2000/svg" width="${W}" height="${H}" viewBox="0 0 ${W} ${H}" role="img" aria-label="Berk ile kısa sohbet">
<style>.m{opacity:0;animation:g .45s ease-out forwards}@keyframes g{from{opacity:0;transform:translateY(8px)}to{opacity:1;transform:none}}@media (prefers-reduced-motion:reduce){.m{animation:none;opacity:1}}</style>
${p.join("\n")}
</svg>\n`;
}

for (const [ad, t] of Object.entries(TEMA)) writeFileSync(`assets/sohbet-${ad}.svg`, ciz(t));
console.log(son, havaCumle);
