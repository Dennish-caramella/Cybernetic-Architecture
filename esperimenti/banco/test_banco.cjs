// Criteri A2-A8 di PIANO.md. Uso: NODE_PATH=$(npm root -g) node test_banco.cjs [cartella_screenshot] [eseguibile_chromium]
const { chromium } = require("playwright"), path = require("path"), fs = require("fs");
const FILE = "file://" + path.join(__dirname, "banco.html"), SHOT = process.argv[2], EXE = process.argv[3];
const ok = (c, m) => { console.log((c ? "PASSA " : "FALLISCE ") + m); if (!c) process.exitCode = 1; };
(async () => {
  const b = await chromium.launch(EXE ? { executablePath: EXE } : {});
  ok(fs.statSync(path.join(__dirname, "banco.html")).size < 5e6, "A7 banco.html < 5 MB");
  for (const [w, scheme] of [[1280, "light"], [400, "light"], [400, "dark"], [1280, "dark"]]) {
    const p = await b.newPage({ viewport: { width: w, height: 800 }, colorScheme: scheme }), err = [], ext = new Set();
    p.on("pageerror", x => err.push(String(x)));
    p.on("console", x => x.type() == "error" && err.push(x.text()));
    p.on("request", r => { const u = new URL(r.url()); if (u.protocol.startsWith("http")) ext.add(u.host); });
    await p.goto(FILE, { waitUntil: "networkidle" });
    const t = `${w}px ${scheme}:`;
    const r = await p.evaluate(() => {
      const n = {}, bad = [];
      all.forEach(l => { const q = l.feature.properties; n[q.k] = (n[q.k] || 0) + 1;
        if ("AG".includes(q.k) && (q.cap_far05 || q.cap_far1 || q.cap_far2 || q.cap_recupero)) bad.push(q.id); });
      return { n, bad, nil: D.nil.features.length, dash: all.filter(l => l.feature.properties.k == "G").every(l => l.options.dashArray),
        dom: [...document.querySelectorAll("#tot td[data-k]")].map(x => x.dataset.k + " " + x.textContent),
        tot: document.getElementById("totnote").textContent, warn: document.querySelectorAll("#avvertenze li").length,
        sw: document.documentElement.scrollWidth, bg: getComputedStyle(document.body).backgroundColor, page: document.body.innerText };
    });
    ok(err.length == 0, `A5 ${t} zero errori JS ${err.join(" | ")}`);
    ok(r.n.E == 216 && r.n.R == 167 && r.n.A == 268 && r.n.G == 50 && all701(r.n), `A2 ${t} 701 lotti per classe ${JSON.stringify(r.n)}`);
    ok(r.dom.join(";") == "E 216 / 216;R 167 / 167;A 268 / 268;G 50 / 50", `A2 ${t} conteggi in pagina ${r.dom.join("; ")}`);
    ok(r.nil == 88, `A2 ${t} 88 NIL`);
    ok(r.bad.length == 0 && r.dash, `A3 ${t} nessuna capacità per attivazione e GFU; GFU tratteggiate`);
    ok(r.tot.includes("16.389 / 32.885 / 65.885") && r.tot.includes("fuori dai totali"), `A4 ${t} totali edificabili`);
    ok(r.warn == 4 && /forbice/.test(r.page) && /non sono validati/.test(r.page) && /inconcludente/.test(r.page) && /non è un vincolo/.test(r.page), `A8 ${t} quattro avvertenze`);
    ok(!/lotti reggono|lotti che reggono/i.test(r.page), `A8 ${t} nessun conteggio di lotti per la cessione`);
    ok([...ext].every(h => h == "cdnjs.cloudflare.com" || h == "tile.openstreetmap.org"), `A6 ${t} host esterni ${[...ext].join(", ")}`);
    if (w == 400) ok(r.sw <= 400, `A5 ${t} nessuno scorrimento orizzontale (scrollWidth ${r.sw})`);
    ok((scheme == "dark") == (r.bg == "rgb(22, 23, 26)"), `A5 ${t} tema ${r.bg}`);
    // schede: GFU, attivazione, edificabile; filtro di classe
    const sch = async id => { await p.fill("#fid", id); await p.dispatchEvent("#fid", "change"); return p.textContent("#scheda"); };
    const g = await sch("G00652"), a = await sch((await p.evaluate(() => all.find(l => l.feature.properties.k == "A").feature.properties.id)));
    const e = await sch("E00268");
    ok(/non verificato/.test(g) && /Fuori dai totali/.test(g), `A3 ${t} scheda GFU: non verificato, fuori dai totali`);
    ok(/non applicabile/.test(a) && !/alloggi/.test(a), `A3 ${t} scheda attivazione senza capacità`);
    ok(/alloggi \(FAR 0,5 \/ 1 \/ 2\)/.test(e) && /Base E v2/.test(e) && /Proprietà/.test(e) && /Stato attuativo/.test(e), `${t} scheda edificabile completa`);
    await p.uncheck('#fcl input[data-k="E"]');
    ok((await p.textContent('#tot td[data-k="E"]')).startsWith("0 /"), `${t} filtro di classe`);
    await p.check('#fcl input[data-k="E"]');
    ok(err.length == 0, `A5 ${t} zero errori JS dopo le interazioni`);
    if (SHOT) await p.screenshot({ path: path.join(SHOT, `banco_${w}_${scheme}.png`), fullPage: w == 400 });
    await p.close();
  }
  await b.close();
})();
function all701(n) { return Object.values(n).reduce((a, b) => a + b, 0) == 701; }
