// Criteri di PIANO.md. Uso: NODE_PATH=$(npm root -g) node test_banco.cjs [cartella_screenshot] [eseguibile_chromium]
const { chromium } = require("playwright"), path = require("path"), fs = require("fs");
const FILE = "file://" + path.join(__dirname, "banco.html"), SHOT = process.argv[2], EXE = process.argv[3];
const ok = (c, m) => { console.log((c ? "PASSA " : "FALLISCE ") + m); if (!c) process.exitCode = 1; };
(async () => {
  const b = await chromium.launch(EXE ? { executablePath: EXE } : {});
  ok(fs.statSync(path.join(__dirname, "banco.html")).size < 5e6, "B7 banco.html < 5 MB");
  for (const [w, scheme, offline] of [[1280, "dark", false], [1280, "light", false], [400, "light", false], [400, "dark", false], [1280, "dark", true]]) {
    const p = await b.newPage({ viewport: { width: w, height: 800 }, colorScheme: scheme }), err = [], ext = new Set(), t = `${w}px ${scheme}${offline ? " senza rete" : ""}:`;
    if (offline) await p.route(/^https?:/, (r) => r.abort());
    p.on("pageerror", (x) => err.push(String(x)));
    p.on("console", (x) => x.type() == "error" && !(offline && /Failed to load resource/.test(x.text())) && err.push(x.text()));
    p.on("request", (r) => { const u = new URL(r.url()); if (u.protocol != "file:" && u.protocol != "data:") ext.add(u.host); });
    await p.goto(FILE, { waitUntil: offline ? "load" : "networkidle" });
    await p.waitForFunction(() => cur === 9, null, { timeout: 15000 });
    if (w < 860) { await p.click("#dfold"); }
    await p.waitForTimeout(800);
    const r = await p.evaluate(() => {
      const n = {}, bad = []; LOTS.forEach((L) => { const q = L.p; n[q.k] = (n[q.k] || 0) + 1; if ("AG".includes(q.k) && (q.cap_far05 || q.cap_far1 || q.cap_far2 || q.cap_recupero)) bad.push(q.id); });
      return { n, bad, dom: document.querySelectorAll("#lotti path").length, nil: document.querySelectorAll("#com path").length, dash: Object.keys(D),
        gdash: [...document.querySelectorAll("#lotti path.kG")].every((e) => getComputedStyle(e).strokeDasharray != "none"),
        cls: [...document.querySelectorAll("#lcl button")].map((x) => x.dataset.k + " " + x.querySelector(".vv").textContent),
        tot: $("ltot").textContent, warn: document.querySelectorAll("#bLotti .warn li").length, page: document.body.innerText + $("bLotti").textContent,
        sw: document.documentElement.scrollWidth, bg: getComputedStyle(document.body).backgroundColor, vis: !$("bLotti").hidden && !$("dash").classList.contains("fold") };
    });
    ok(err.length == 0, `B5 ${t} zero errori JS ${err.join(" | ")}`);
    ok(r.n.E == 216 && r.n.R == 167 && r.n.A == 268 && r.n.G == 50 && r.dom == 701, `B2 ${t} 701 lotti disegnati ${JSON.stringify(r.n)}`);
    ok(r.cls.join(";") == "E 216 / 216;R 167 / 167;A 268 / 268;G 50 / 50", `B2 ${t} conteggi in pagina ${r.cls.join("; ")}`);
    ok(r.nil == 88, `B3 ${t} 88 NIL del Lab`);
    ok(!r.dash.some((k) => ["city", "lab", "pp"].includes(k)) && r.dash.includes("lotti") && r.dash.includes("land") && r.dash.includes("pgt") && r.dash.includes("bld"), `B4 ${t} dashboard ${r.dash.join(",")}`);
    ok(r.bad.length == 0 && r.gdash, `B6 ${t} nessuna capacità per attivazione e GFU; GFU tratteggiate`);
    ok(r.tot.includes("16.389 / 32.885 / 65.885") && r.tot.includes("fuori dai totali"), `B6 ${t} totali edificabili`);
    ok(r.warn == 4 && /forbice/.test(r.page) && /non sono validati/.test(r.page) && /inconcludente/.test(r.page) && /non è un vincolo/.test(r.page), `B8 ${t} quattro avvertenze`);
    ok(!/lotti reggono|lotti che reggono/i.test(r.page) && !/Cooperativa ed edificio/i.test(r.page), `B8 ${t} nessun conteggio per la cessione, nessun pannello Cooperativa`);
    ok(r.vis, `${t} pannello dei lotti visibile`);
    ok([...ext].every((h) => h == "fonts.googleapis.com" || h == "fonts.gstatic.com"), `B1 ${t} host esterni: ${[...ext].join(", ") || "nessuno"}`);
    if (w == 400) ok(r.sw <= 400, `B5 ${t} nessuno scorrimento orizzontale (${r.sw})`);
    ok((scheme == "dark") == (r.bg == "rgb(0, 0, 0)"), `B5 ${t} tema ${r.bg}`);
    const sch = async (id) => { await p.fill("#lid", id); await p.dispatchEvent("#lid", "change"); await p.waitForTimeout(100); return p.textContent("#lsch"); };
    const aid = await p.evaluate(() => LOTS.find((L) => L.p.k == "A").p.id);
    const a = await sch(aid), g = await sch("G00652"), e = await sch("E00268");
    ok(/non verificato/.test(g) && /Fuori dai totali/.test(g), `B6 ${t} scheda GFU`);
    ok(/non applicabile/.test(a) && !/alloggi/.test(a), `B6 ${t} scheda attivazione senza capacità`);
    ok(/alloggi \(FAR 0,5 \/ 1 \/ 2\)/.test(e) && /Base E v2/.test(e) && /canone di pareggio/.test(e) && /Proprietà/.test(e) && /Stato attuativo/.test(e), `${t} scheda edificabile con Base E v2`);
    if (SHOT && !offline) await p.screenshot({ path: path.join(SHOT, `banco_${w}_${scheme}.png`), fullPage: w == 400 });
    await p.click('#lcl button[data-k="E"]');
    ok((await p.textContent('#lcl button[data-k="E"] .vv')).startsWith("0 /"), `${t} filtro di classe`);
    // strati del Lab: DUSAF, PGT, DBT, con i lotti sopra
    const st = await p.evaluate(async () => {
      const out = {};
      for (const [k, m] of [["land", "lucat"], ["pgt", "lucat"], ["bld", "dbt_vol"]]) { dash = k; met = m; lay.lotti = true; render(); await new Promise((r) => setTimeout(r, 300));
        out[k] = { dusaf: document.querySelectorAll("#lu_dusaf path").length, pgt: document.querySelectorAll("#lu_pgt path").length, fill: C.filter((c) => c.el.style.fill.startsWith("rgb") || c.el.style.fill.startsWith("#")).length, lotti: !$("lotti").classList.contains("off") }; }
      return out; });
    ok(st.land.dusaf > 0 && st.pgt.pgt > 0 && st.bld.fill > 80 && st.land.lotti && st.bld.lotti, `B3 ${t} strati del Lab con lotti sopra ${JSON.stringify(st)}`);
    if (SHOT && !offline && w == 1280) await p.screenshot({ path: path.join(SHOT, `banco_${w}_${scheme}_dbt.png`) });
    ok(err.length == 0, `B5 ${t} zero errori JS dopo le interazioni ${err.join(" | ")}`);
    await p.close();
  }
  await b.close();
})();
