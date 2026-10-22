// Render slide HTML (dari lib/slides.py) ke PNG 1080x1350, plus PDF untuk LinkedIn.
//
// Pakai:
//   node lib/render.mjs <file.html> <folder-output> [cover.png]
// Contoh:
//   node lib/render.mjs konten/2026-10-22-fondasi-ai-05/slides.html konten/2026-10-22-fondasi-ai-05/output konten/2026-10-22-fondasi-ai-05/output/cover.png
//
// Hasil:
//   slide-02.png, slide-03.png, ... (nomor diambil dari id "s2", "s3", ...)
//   carousel-linkedin.pdf (cover di halaman pertama kalau path cover diberikan)
import { chromium } from "playwright";
import { mkdirSync, existsSync, readdirSync } from "node:fs";
import { resolve, join } from "node:path";
import { pathToFileURL } from "node:url";

const [, , htmlArg, outArg, coverArg] = process.argv;
if (!htmlArg || !outArg) {
  console.error("Pakai: node lib/render.mjs <file.html> <folder-output> [cover.png]");
  process.exit(1);
}
const htmlPath = resolve(htmlArg);
const outDir = resolve(outArg);
mkdirSync(outDir, { recursive: true });

// CHROMIUM_PATH opsional, kalau mau pakai Chrome/Chromium yang sudah ada di laptop.
const exe = process.env.CHROMIUM_PATH;
const browser = await chromium.launch(exe ? { executablePath: exe } : {});
const page = await browser.newPage({ viewport: { width: 1080, height: 1350 }, deviceScaleFactor: 1 });
await page.goto(pathToFileURL(htmlPath).href);
await page.evaluate(() => document.fonts.ready);
// Tunggu auto-fit teks selesai (hanya ada kalau slide dibuat dengan build()).
await page.waitForFunction(() => window.__fitDone === undefined || window.__fitDone === true, null, { timeout: 15000 });

const ids = await page.$$eval(".s", (els) => els.map((e) => e.id));
const files = [];
for (const id of ids) {
  const n = String(id.replace(/\D/g, "") || files.length + 2).padStart(2, "0");
  const file = join(outDir, `slide-${n}.png`);
  await page.locator(`#${id}`).screenshot({ path: file });
  files.push(file);
  console.log("ditulis", file);
}

// PDF LinkedIn: cover (opsional) + semua slide, satu halaman 1080x1350 per gambar.
const images = [];
if (coverArg && existsSync(resolve(coverArg))) images.push(resolve(coverArg));
images.push(...files.sort());
const pdfHtml = `<!doctype html><html><head><style>
@page{size:1080px 1350px;margin:0}html,body{margin:0}
img{display:block;width:1080px;height:1350px;page-break-after:always;object-fit:cover}
</style></head><body>${images.map((f) => `<img src="${pathToFileURL(f).href}">`).join("")}</body></html>`;
const pdfPage = await browser.newPage();
await pdfPage.setContent(pdfHtml, { waitUntil: "load" });
const pdfFile = join(outDir, "carousel-linkedin.pdf");
await pdfPage.pdf({ path: pdfFile, width: "1080px", height: "1350px", printBackground: true });
console.log("ditulis", pdfFile);

await browser.close();
