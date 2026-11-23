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
    ok(r.n.E == 216 && r.n.R == 167 && r.n.A == 268 && r.n.G == 50 && r.dom == 701, `B2 ${t} 701 elementi disegnati (383 lotti, 268 aree di attivazione, 50 GFU) ${JSON.stringify(r.n)}`);
    ok(r.cls.join(";") == "E 216 / 216;R 167 / 167;A 268 / 268;G 50 / 50", `B2 ${t} conteggi in pagina ${r.cls.join("; ")}`);
    ok(r.nil == 88, `B3 ${t} 88 NIL del Lab`);
    ok(!r.dash.some((k) => ["city", "lab", "pp"].includes(k)) && r.dash.includes("lotti") && r.dash.includes("land") && r.dash.includes("pgt") && r.dash.includes("bld"), `B4 ${t} dashboard ${r.dash.join(",")}`);
    ok(r.bad.length == 0 && r.gdash, `B6 ${t} nessuna capacità per attivazione e GFU; GFU tratteggiate`);
    ok(r.tot.includes("16.389 / 32.885 / 65.885") && r.tot.includes("fuori dai totali"), `B6 ${t} totali edificabili`);
    ok(r.warn == 5 && /forbice/.test(r.page) && /non sono validati/.test(r.page) && /inconcludente/.test(r.page) && /non è un vincolo/.test(r.page) && /corpi idrici/.test(r.page) && /0,49/.test(r.page), `B8 ${t} cinque avvertenze (D5: validazione debole, corpi idrici)`);
    ok(!/lotti reggono|lotti che reggono/i.test(r.page) && !/Cooperativa ed edificio/i.test(r.page), `B8 ${t} nessun conteggio per la cessione, nessun pannello Cooperativa`);
    ok(r.vis, `${t} pannello dei lotti visibile`);
    ok([...ext].every((h) => h == "fonts.googleapis.com" || h == "fonts.gstatic.com"), `B1 ${t} host esterni: ${[...ext].join(", ") || "nessuno"}`);
    if (w == 400) ok(r.sw <= 400, `B5 ${t} nessuno scorrimento orizzontale (${r.sw})`);
    ok((scheme == "dark") == (r.bg == "rgb(0, 0, 0)"), `B5 ${t} tema ${r.bg}`);
    // revisione D1, D2, D6, D7
    const rv = await p.evaluate(() => { let rk; try { TOOLS().find((x) => x.name == "get_ranking").execute({ indicator: "d_tau" }); rk = "accettato"; } catch (x) { rk = "rifiutato"; }
      const L = (h) => { const c = h.match(/\d+/g).slice(0, 3).map((x) => +x / 255).map((x) => x <= 0.04045 ? x / 12.92 : ((x + 0.055) / 1.055) ** 2.4); return 0.2126 * c[0] + 0.7152 * c[1] + 0.0722 * c[2]; };
      const cr = (a, b) => { const x = L(a), y = L(b); return (Math.max(x, y) + 0.05) / (Math.min(x, y) + 0.05); };
      const hex = (h) => { h = h.trim().replace("#", ""); return `rgb(${parseInt(h.slice(0, 2), 16)}, ${parseInt(h.slice(2, 4), 16)}, ${parseInt(h.slice(4, 6), 16)})`; };
      const land = hex(getComputedStyle($("map")).getPropertyValue("--land")), lc = {};
      ["E", "R", "A", "G"].forEach((k) => { lc[k] = +cr(getComputedStyle(LOTS.find((x) => x.p.k == k).el).stroke, land).toFixed(2); });
      return { ind: IND_LIST, rk, rules: rules(), k1l: $("k1l").textContent, lc, live: $("lsch").getAttribute("aria-live"), tab0: LOTS.filter((x) => x.el.tabIndex === 0).length }; });
    ok(!/undefined/.test(rv.ind) && !/\b(pp_resb|pp_res|pp_neg|pp_rti|d_tau|d_dec|d_ist)\b/.test(rv.ind) && rv.rk == "rifiutato", `D1 ${t} indicatori del modello di domanda escluso fuori dalla chat (get_ranking d_tau ${rv.rk})`);
    ok(/383/.test(rv.k1l) && !/su 701/.test(rv.k1l) && /383 lotti/.test(rv.rules) && !/701 lotti/.test(rv.rules + r.page), `D2 ${t} conteggi per classe nel KPI e nella chat: ${rv.k1l}`);
    ok(Object.values(rv.lc).every((x) => x >= (scheme == "light" ? 3 : 5)), `D7 ${t} contrasto delle classi sul fondo della mappa ${JSON.stringify(rv.lc)}`);
    ok(rv.live == "polite" && rv.tab0 == 1, `D7 ${t} aria-live sulla scheda, un lotto nella sequenza di Tab`);
    await p.evaluate(() => LOTS.find((x) => x.el.tabIndex === 0).el.focus()); const f0 = await p.evaluate(() => document.activeElement.textContent);
    await p.keyboard.press("ArrowRight"); const f1 = await p.evaluate(() => document.activeElement.textContent);
    await p.keyboard.press("Enter"); await p.waitForTimeout(100);
    const kb = await p.evaluate(() => ({ sel: selLot && selLot.p.id, foc: document.activeElement.textContent, sch: $("lsch").textContent }));
    ok(f0 != f1 && f1.startsWith(kb.sel) && kb.foc == f1 && kb.sch.includes(kb.sel), `D7 ${t} tastiera: frecce ${f0.slice(0, 6)} → ${f1.slice(0, 6)}, Invio apre la scheda di ${kb.sel}, fuoco conservato`);
    const ec = await p.evaluate(async () => { dash = "eco"; met = "poor"; render(); await new Promise((r) => setTimeout(r, 200)); const x = { vis: !$("bNote").hidden, t: $("bNote").textContent }; dash = "lotti"; met = "lcl"; render(); return x; });
    ok(ec.vis && /CAP 20157/.test(ec.t) && /artefatto di dato/.test(ec.t) && /un solo reddito/.test(ec.t), `D6 ${t} avvertenza su Stipendi e affitti`);
    const sch = async (id) => { await p.fill("#lid", id); await p.dispatchEvent("#lid", "change"); await p.waitForTimeout(100); return p.textContent("#lsch"); };
    const aid = await p.evaluate(() => LOTS.find((L) => L.p.k == "A").p.id);
    const a = await sch(aid), g = await sch("G00652"), e = await sch("E00268");
    ok(/non verificato/.test(g) && /Fuori dai totali/.test(g), `B6 ${t} scheda GFU`);
    ok(/non applicabile/.test(a) && !/alloggi/.test(a), `B6 ${t} scheda attivazione senza capacità`);
    // M7: tre lotti contro lotti_v7.gpkg (valori letti con geopandas il 23/11/2026; SHA-256 del gpkg controllato da build.py)
    const REF = { E00349: [14489, 63, 126, 253, null, null, "non agganciata", "LAMBRATE - ORTICA"], R00127: [6882, 30, 60, 120, 72, null, "non agganciata", "LODI - CORVETTO"],
      E00205: [6805, 29, 59, 119, null, "GFU", "non agganciata", "RONCHETTO SUL NAVIGLIO - Q.RE LODOVICO IL MORO"] };
    for (const [id, x] of Object.entries(REF)) {
      const q = await p.evaluate((id) => LOTS.find((L) => L.p.id == id).p, id), s = await sch(id);
      const got = [q.area_m2, q.cap_far05, q.cap_far1, q.cap_far2, q.cap_recupero ?? null, q.gruppo_ambito ?? null, q.proprieta, q.nil_nome];
      ok(JSON.stringify(got) == JSON.stringify(x) && s.includes(x[0].toLocaleString("it-IT") + " m²") && !/\[L\] \[L\]|\[V\] catasto/.test(s) && /area della geometria/.test(s) && /Fonti della base/.test(s)
        && (id != "E00205" || /in ambito, stato non censito/.test(s)), `M7 D3 D4 M6 ${t} ${id} come nel gpkg e scheda corretta ${JSON.stringify(got)}`);
    }
    ok(/lago su oltre metà/.test(await sch("E00170")), `D5 ${t} nota sui corpi idrici per E00170`);
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
    // B9 zoom: rotella, pulsanti, pinch, trascinamento, clic su un lotto da zoomati
    if (!offline) {
      if (w < 860) await p.click("#dfold"); // pannello chiuso per vedere la mappa
      await p.evaluate(() => { dash = "lotti"; met = "lcl"; LF.cl.E = true; render(); setVB(FULL); fitText(); });
      const vw = () => p.evaluate(() => svg.viewBox.baseVal.width), W0 = await vw();
      const tgt = await p.evaluate(() => { const L = LOTS.filter((x) => x.p.k == "E").sort((a, b) => b.p.area_m2 - a.p.area_m2)[0]; const r = L.el.getBoundingClientRect(); return { id: L.p.id, x: r.x + r.width / 2, y: r.y + r.height / 2 }; });
      await p.mouse.move(tgt.x, tgt.y); for (let i = 0; i < 6; i++) { await p.mouse.wheel(0, -400); await p.waitForTimeout(50); }
      const W1 = await vw();
      const hit = await p.evaluate((id) => { const L = LOTS.find((x) => x.p.id == id), r = L.el.getBoundingClientRect();
        for (let i = 1; i < 20; i++) for (let j = 1; j < 20; j++) { const x = r.x + r.width * i / 20, y = r.y + r.height * j / 20; if (document.elementFromPoint(x, y) === L.el) return { x, y }; } return null; }, tgt.id);
      if (hit) await p.mouse.click(hit.x, hit.y);
      const clicked = await p.evaluate(() => selLot && selLot.p.id);
      await p.click("#zin"); const W2 = await vw(); await p.click("#zout"); await p.click("#zout"); const W3 = await vw();
      const b0 = await p.evaluate(() => svg.viewBox.baseVal.x); const box = await p.locator("#flat").boundingBox();
      await p.mouse.move(box.x + box.width / 2, box.y + box.height / 2); await p.mouse.down(); await p.mouse.move(box.x + box.width / 2 + 60, box.y + box.height / 2 + 20, { steps: 5 }); await p.mouse.up();
      const b1 = await p.evaluate(() => svg.viewBox.baseVal.x);
      const pinch = await p.evaluate(() => { const r = svg.getBoundingClientRect(), cx = r.x + r.width / 2, cy = r.y + r.height / 2, w0 = svg.viewBox.baseVal.width;
        const ev = (t, id, x, y) => svg.dispatchEvent(new PointerEvent(t, { pointerId: id, clientX: x, clientY: y, bubbles: true }));
        ev("pointerdown", 11, cx - 20, cy); ev("pointerdown", 12, cx + 20, cy); ev("pointermove", 12, cx + 30, cy); ev("pointermove", 12, cx + 80, cy); ev("pointerup", 11, cx, cy); ev("pointerup", 12, cx, cy);
        return svg.viewBox.baseVal.width < w0; });
      await p.click("#zrst"); await p.waitForTimeout(900); const W4 = await vw();
      const sw = await p.evaluate(() => getComputedStyle(LOTS[0].el).vectorEffect + " " + getComputedStyle(C[0].el).vectorEffect);
      ok(W1 < W0 / 3 && clicked == tgt.id && W2 < W1 && W3 > W2 && b1 < b0 && pinch && Math.abs(W4 - W0) < 1e-6 && sw == "non-scaling-stroke non-scaling-stroke" && !(await p.isHidden("#zin")),
        `B9 ${t} zoom: rotella ${W0.toFixed(1)}→${W1.toFixed(2)}, clic sul lotto ${tgt.id} da zoomati → ${clicked}, pulsanti +/− ${W2.toFixed(2)}/${W3.toFixed(2)}, trascinamento ${b0.toFixed(2)}→${b1.toFixed(2)}, pinch ${pinch}, ritorno ${W4.toFixed(1)}, spessore costante (${sw})`);
    }
    ok(err.length == 0, `B5 ${t} zero errori JS dopo le interazioni ${err.join(" | ")}`);
    await p.close();
  }
  await b.close();
})();
