// Profildeki "son yayınlar + diller" kartını GitHub API'den yeniden çizer (assets/yayinlar-{dark,light}.svg).
import { writeFileSync } from "node:fs";

const KULLANICI = "berkdemir18";
const DEPOLAR = [
  "kukreme",
  "akilli-urun-siralama",
  "DemirTube",
  "ilerleme",
  "Ajanda",
  "agents-sync",
  "File-Finder",
  "Kokpit",
  "BerkStream-Hub",
];
const token = process.env.GITHUB_TOKEN;

async function api(yol) {
  const r = await fetch(`https://api.github.com/${yol}`, {
    headers: { Accept: "application/vnd.github+json", ...(token && { Authorization: `Bearer ${token}` }) },
  });
  if (r.status === 404) return null;
  if (!r.ok) throw new Error(`${yol}: HTTP ${r.status}`);
  return r.json();
}

const aylar = ["Oca", "Şub", "Mar", "Nis", "May", "Haz", "Tem", "Ağu", "Eyl", "Eki", "Kas", "Ara"];
const tarih = (iso) => {
  const d = new Date(iso);
  return `${String(d.getUTCDate()).padStart(2, "0")} ${aylar[d.getUTCMonth()]} ${d.getUTCFullYear()}`;
};
const kac = (s) => String(s).replace(/&/g, "&amp;").replace(/</g, "&lt;").replace(/>/g, "&gt;");

// --- son yayınlar
const yayinlar = [];
for (const depo of DEPOLAR) {
  const liste = (await api(`repos/${KULLANICI}/${depo}/releases?per_page=5`)) ?? [];
  for (const y of liste) if (!y.draft && !y.prerelease) yayinlar.push({ depo, etiket: y.tag_name, tarih: y.published_at });
}
yayinlar.sort((a, b) => b.tarih.localeCompare(a.tarih));
// her projenin yalnız en son sürümü
const goruldu = new Set();
const son = yayinlar.filter((y) => !goruldu.has(y.depo) && goruldu.add(y.depo)).slice(0, 5);

// --- dil dağılımı
const toplam = {};
for (const depo of DEPOLAR) {
  const diller = (await api(`repos/${KULLANICI}/${depo}/languages`)) ?? {};
  for (const [dil, bayt] of Object.entries(diller)) toplam[dil] = (toplam[dil] ?? 0) + bayt;
}
const genel = Object.values(toplam).reduce((a, b) => a + b, 0);
const sirali = Object.entries(toplam).sort((a, b) => b[1] - a[1]);
const diller = sirali.slice(0, 5).map(([d, b]) => [d, b / genel]);
const digerOran = sirali.slice(5).reduce((a, [, b]) => a + b, 0) / genel;
if (digerOran > 0) diller.push(["Diğer", digerOran]);

// --- çizim
const TEMALAR = {
  dark: { bg: "#13110F", ink: "#F1EADF", mute: "#8C8276", faint: "#5A5249", line: "#2A2520", acc: "#E9A23B",
    ton: ["#E9A23B", "#C98A3A", "#A0754A", "#7D6650", "#5E5349", "#433D37"] },
  light: { bg: "#F5F0E7", ink: "#1B1714", mute: "#6F665B", faint: "#A79D90", line: "#DDD4C6", acc: "#B4650E",
    ton: ["#B4650E", "#C98A3A", "#B39066", "#9C8B76", "#BDB2A3", "#D6CDBF"] },
};
const MONO = "'JetBrains Mono', 'Cascadia Mono', SFMono-Regular, Consolas, Menlo, monospace";
const SERIF = "'Instrument Serif', Georgia, 'Times New Roman', serif";
const W = 1200, H = 380;

function ciz(t) {
  const p = [];
  p.push(`<rect x=".5" y=".5" width="${W - 1}" height="${H - 1}" rx="22" fill="${t.bg}" stroke="${t.line}"/>`);
  // sol: yayınlar
  p.push(`<text x="40" y="58" font-family="${MONO}" font-size="11" letter-spacing="1.8" fill="${t.mute}">SON YAYINLAR</text>`);
  son.forEach((y, i) => {
    const yy = 112 + i * 52;
    p.push(`<line x1="40" y1="${yy - 32}" x2="640" y2="${yy - 32}" stroke="${t.line}"/>`);
    p.push(`<text x="40" y="${yy}" font-family="${MONO}" font-size="12" fill="${t.faint}">${kac(tarih(y.tarih))}</text>`);
    p.push(`<text x="170" y="${yy + 1}" font-family="${SERIF}" font-size="24" fill="${t.ink}">${kac(y.depo)}</text>`);
    p.push(`<text x="640" y="${yy}" text-anchor="end" font-family="${MONO}" font-size="12" fill="${i === 0 ? t.acc : t.mute}">${kac(y.etiket)}</text>`);
  });
  // sağ: diller
  const X = 720, BW = 440;
  p.push(`<text x="${X}" y="58" font-family="${MONO}" font-size="11" letter-spacing="1.8" fill="${t.mute}">DEPOLARDAKİ DİLLER</text>`);
  let x = X;
  diller.forEach(([, o], i) => {
    const w = Math.max(2, o * BW);
    p.push(`<rect x="${x.toFixed(1)}" y="82" width="${(w - 2).toFixed(1)}" height="10" rx="2" fill="${t.ton[i]}"/>`);
    x += w;
  });
  diller.forEach(([d, o], i) => {
    const yy = 136 + i * 34;
    p.push(`<circle cx="${X + 5}" cy="${yy - 4}" r="4" fill="${t.ton[i]}"/>`);
    p.push(`<text x="${X + 20}" y="${yy}" font-family="${MONO}" font-size="12.5" fill="${t.ink}">${kac(d)}</text>`);
    p.push(`<text x="${X + BW}" y="${yy}" text-anchor="end" font-family="${MONO}" font-size="12.5" fill="${t.mute}">${(o * 100).toFixed(1).replace(".", ",")} %</text>`);
  });
  p.push(`<text x="${X}" y="${H - 34}" font-family="${MONO}" font-size="10.5" fill="${t.faint}">Depoların içi, benim bildiğim diller değil.</text>`);
  return `<svg xmlns="http://www.w3.org/2000/svg" width="${W}" height="${H}" viewBox="0 0 ${W} ${H}" role="img" aria-label="Son yayınlar ve depolardaki diller">${p.join("")}</svg>\n`;
}

for (const [ad, t] of Object.entries(TEMALAR)) writeFileSync(`assets/yayinlar-${ad}.svg`, ciz(t));
console.log(son.map((y) => `${tarih(y.tarih)}  ${y.depo}  ${y.etiket}`).join("\n"));
console.log(diller.map(([d, o]) => `${d} ${(o * 100).toFixed(1)}%`).join(" · "));
