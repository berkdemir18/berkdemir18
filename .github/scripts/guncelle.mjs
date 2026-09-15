// Profil README'sindeki "son yayınlar" ve "dil dağılımı" bloklarını GitHub API'den yeniden üretir.
import { readFileSync, writeFileSync } from "node:fs";

const KULLANICI = "berkdemir18";
const DEPOLAR = ["DemirTube", "File-Finder", "Ajanda", "agents-sync", "ilerleme", "Kokpit", "siber-yol-haritasi", "berkin-dondurma-sitesi"];
const token = process.env.GITHUB_TOKEN;

async function api(yol) {
  const r = await fetch(`https://api.github.com/${yol}`, {
    headers: { Accept: "application/vnd.github+json", ...(token && { Authorization: `Bearer ${token}` }) },
  });
  if (r.status === 404) return null;
  if (!r.ok) throw new Error(`${yol}: HTTP ${r.status}`);
  return r.json();
}

const uzunluk = (s) => [...s].length;
const bosluk = (s, n) => s + " ".repeat(Math.max(0, n - uzunluk(s)));
const aylar = ["Oca", "Şub", "Mar", "Nis", "May", "Haz", "Tem", "Ağu", "Eyl", "Eki", "Kas", "Ara"];
const tarih = (iso) => {
  const d = new Date(iso);
  return `${String(d.getUTCDate()).padStart(2, "0")} ${aylar[d.getUTCMonth()]} ${d.getUTCFullYear()}`;
};

// --- son yayınlar
const yayinlar = [];
for (const depo of DEPOLAR) {
  const liste = (await api(`repos/${KULLANICI}/${depo}/releases?per_page=5`)) ?? [];
  for (const y of liste) if (!y.draft && !y.prerelease) yayinlar.push({ depo, etiket: y.tag_name, tarih: y.published_at });
}
yayinlar.sort((a, b) => b.tarih.localeCompare(a.tarih));
const yayinBlok = ["```text", ...yayinlar.slice(0, 5).map((y) => `  ${tarih(y.tarih)}   ${bosluk(y.depo, 13)} ${y.etiket}`), "```"].join("\n");

// --- dil dağılımı
const toplam = {};
for (const depo of DEPOLAR) {
  const diller = (await api(`repos/${KULLANICI}/${depo}/languages`)) ?? {};
  for (const [dil, bayt] of Object.entries(diller)) toplam[dil] = (toplam[dil] ?? 0) + bayt;
}
const genel = Object.values(toplam).reduce((a, b) => a + b, 0);
const sirali = Object.entries(toplam).sort((a, b) => b[1] - a[1]);
const gosterilen = sirali.slice(0, 5);
const digerBayt = sirali.slice(5).reduce((a, [, b]) => a + b, 0);
if (digerBayt > 0) gosterilen.push(["Diğer", digerBayt]);

const GENISLIK = 60;
const CUBUK = 36;
const satir = (ic) => `│${bosluk(ic, GENISLIK)}│`;
const kenar = (bas, son) => bas + "─".repeat(GENISLIK + 1 - uzunluk(bas)) + son;
const dilSatirlari = gosterilen.map(([dil, bayt]) => {
  const oran = bayt / genel;
  const dolu = Math.round(oran * CUBUK);
  const yuzde = (oran * 100).toFixed(1).replace(".", ",").padStart(5);
  return satir(`  ${bosluk(dil, 11)} ${"█".repeat(dolu)}${"░".repeat(CUBUK - dolu)}  ${yuzde} %`);
});
const mb = (genel / 1048576).toFixed(1).replace(".", ",");
const dilBlok = [
  "```text",
  kenar("┌─ depolardaki dil dağılımı ", "┐"),
  satir(""),
  ...dilSatirlari,
  satir(""),
  kenar(`└─ toplam ~${mb} MB · ${DEPOLAR.length} depo `, "┘"),
  "```",
].join("\n");

// --- README'ye yaz
const degistir = (metin, ad, blok) => {
  const re = new RegExp(`(<!-- ${ad}:BASLA -->)[\\s\\S]*?(<!-- ${ad}:BITIR -->)`);
  if (!re.test(metin)) throw new Error(`${ad} işaretleri README'de yok`);
  return metin.replace(re, `$1\n${blok}\n$2`);
};
let readme = readFileSync("README.md", "utf8");
readme = degistir(readme, "YAYINLAR", yayinBlok);
readme = degistir(readme, "DILLER", dilBlok);
writeFileSync("README.md", readme);
console.log(`${yayinBlok}\n${dilBlok}`);
