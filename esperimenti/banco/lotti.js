/* ---------- banco: lotti della Base L v7 e Base E v2 (esperimenti/banco/build.py) ---------- */
const BL = /*__BL__*/null;
const KL = { E: "lotto edificabile", R: "lotto da riusare", A: "area di attivazione", G: "GFU: edificabile per destinazione, non verificato" };
const KC = { E: "var(--kE)", R: "var(--kR)", A: "var(--kA)", G: "var(--kG)" }; // banco.css: chiari nel tema scuro, scuri nel tema chiaro (≥ 3:1)
const LF = { cl: { E: true, R: true, A: true, G: true }, pr: "", am: "", st: "" };
let selLot = null;
const LOTS = BL.lotti.map((x) => {
  const p = x.p, poly = x.r.map((r) => decU(r, 0.001));
  p.ci = byId[p.nil_id] ?? -1;
  const el = G("path", { d: poly.map((r) => dstr(r, true)).join(""), class: "k" + p.k, tabindex: -1, role: "button" }, $("lotti"));
  G("title", {}, el).textContent = `${p.id} · ${KL[p.k]} · ${n0(p.area_m2)} m²`;
  el.setAttribute("aria-label", el.textContent);
  el.addEventListener("click", (e) => { e.stopPropagation(); lotSel(p.id); });
  el.addEventListener("keydown", (e) => { // tastiera: Invio o spazio apre la scheda; frecce al lotto visibile successivo o precedente
    if (e.key === "Enter" || e.key === " ") { e.preventDefault(); lotSel(p.id); return; }
    const d = { ArrowRight: 1, ArrowDown: 1, ArrowLeft: -1, ArrowUp: -1 }[e.key]; if (!d) return;
    e.preventDefault(); const vis = LOTS.filter((x) => x.el.style.display !== "none"), i = vis.findIndex((x) => x.el === el), n = vis[(i + d + vis.length) % vis.length].el;
    el.tabIndex = -1; n.tabIndex = 0; n.focus();
  });
  return { p, poly, el };
});
const lotOk = (p) => LF.cl[p.k] && (!LF.pr || p.proprieta === LF.pr) && (!LF.am || (LF.am === "-" ? !p.gruppo_ambito : p.gruppo_ambito === LF.am)) && (!LF.st || (LF.st === "-" ? !p.stato_riferimento : p.stato_riferimento === LF.st));
const pc = (x) => String(x).replace(".", ",");
const fa = (a) => a.map(n0).join(" / ");
const q2 = (x) => x > 0 && x < 0.005 ? "≈ 0" : pc(x.toFixed(2)); // quote: due decimali (revisione M2)
const WARN = `<div class="card warn"><h5>Avvertenze</h5><ul>
<li>La <b>capacità è una forbice</b> (FAR 0,5 / 1 / 2), non un valore unico [H].</li>
<li>I <b>lotti GFU non sono validati</b>: perimetri 2012 sostitutivi [H], destinazione non verificata [L]; fuori dai totali, capacità solo come scenario.</li>
<li>La validazione fotografica <b>C5 è inconcludente</b> (controllo umano 0,737 nella fascia 0,65–0,75): la Base L v7 è congelata <b>per decisione di Dennis</b> (22/11), non per una misura.</li>
<li><b>Validazione debole per alcune classi</b>: quota stimata di lotti liberi o dismessi 0,55–0,59 per i lotti da riusare e 0,49 per gli AdP (contro 0,72–0,82 fuori ambito e nei piani attuativi); <b>nessuna maschera dei corpi idrici</b>: un lotto può contenere acqua (es. E00170). Fonte: Base L v7, REPORT §4, §6, §7 e VERSIONE.md.</li>
<li>La <b>Base E v2 non è un vincolo</b> di fattibilità per lotto: le quote sono quote della regione dei parametri, non probabilità; η senza fonte; errore di taratura non misurato.</li></ul></div>`;
function lotInit() {
  const opt = (id, l, o) => `<label class="sel-row"><span class="h">${l}</span><select id="${id}" class="s2">${o.map(([v, t]) => `<option value="${v}">${t}</option>`).join("")}</select></label>`;
  $("bLotti").innerHTML = WARN + `<div><p class="h">CLASSI</p><div class="bars" id="lcl"></div></div>` +
    opt("lpr", "PROPRIETÀ", [["", "tutte"], ["pubblico comunale", "pubblico comunale"], ["Demanio", "Demanio"], ["non agganciata", "non agganciata"]]) +
    opt("lam", "AMBITO PGT 2030", [["", "tutti"], ["PA", "PA (piano attuativo)"], ["ADP", "AdP Scali"], ["GFU", "GFU"], ["-", "fuori ambito"]]) +
    opt("lst", "STATO ATTUATIVO", [["", "tutti"], ["A", "A attuazione avviata"], ["B", "B in istruttoria"], ["C", "C solo previsione"], ["non determinato [L]", "N non determinato [L]"], ["-", "non censito"]]) +
    `<label class="sel-row"><span class="h">CERCA ID</span><input id="lid" class="s2 lin" placeholder="es. E00168"></label>
<div class="card" id="ltot"></div><div class="card" id="lsch" aria-live="polite"><p class="note">Clic su un lotto della mappa o cerca un id. Da tastiera: Tab fino ai lotti, frecce per passare da uno all'altro, Invio per la scheda.</p></div>
<details class="card"><summary><b>Base E v2: canone di pareggio e cessione</b></summary><div id="leco"></div></details>
<details class="card"><summary><b>Legenda delle marche</b></summary><table>
<tr><td>[V]</td><td>qui: valore letto dalle basi congelate (SHA-256 controllato al build). Nel protocollo [V] vuol dire "verificato in questa sessione": i valori del singolo lotto non sono stati riverificati sulle fonti originali</td></tr><tr><td>[S]</td><td>fonte secondaria</td></tr>
<tr><td>[I]</td><td>inferenza</td></tr><tr><td>[H]</td><td>ipotesi o parametro scelto</td></tr><tr><td>[L]</td><td>lacuna: il dato manca</td></tr></table></details>
<details class="card"><summary><b>Fonti e riproducibilità</b></summary><div id="lfon"></div></details>`;
  $("lcl").innerHTML = ["E", "R", "A", "G"].map((k) => `<button type="button" data-k="${k}"><i class="sw" style="border:2px ${k === "G" ? "dashed" : "solid"} ${KC[k]}"></i><span class="tr"><span class="lb">${esc(KL[k])}</span></span><span class="vv"></span></button>`).join("");
  $("lcl").querySelectorAll("button").forEach((bt) => { bt.onclick = () => { LF.cl[bt.dataset.k] = !LF.cl[bt.dataset.k]; render(); }; });
  [["lpr", "pr"], ["lam", "am"], ["lst", "st"]].forEach(([id, k]) => { $(id).onchange = () => { LF[k] = $(id).value; render(); }; });
  $("lid").onchange = () => { const id = $("lid").value.trim().toUpperCase(); if (!lotSel(id)) $("lsch").innerHTML = '<p class="note">Nessun lotto con questo id.</p>'; };
  const c = BL.ces;
  $("leco").innerHTML = `<p class="note">Canone di pareggio con suolo gratuito, nuovo, €/m²/anno (5% · mediana · 95%) [H]. Uguale per tutti i lotti: il lato cooperativa non ha geografia. Fonte: Base E v2, tabelle/c_star_per_regione.csv.</p>
<table><tr><th>Durata</th><th>Regione</th><th>5%</th><th>med.</th><th>95%</th></tr>${BL.cstar.map((r) => `<tr><td>${r[0]} anni</td><td>${esc(r[1])}${r[1].startsWith("bandi") ? " [S]" : ""}</td><td>${r[2]}</td><td>${r[3]}</td><td>${r[4]}</td></tr>`).join("")}</table>
<p>Cessione del diritto di superficie (nuovo, 90 €/m²/anno, FAR 1): quota della regione tarata in cui la cooperativa regge ${q2(c[60][0])} a 60 anni e ${q2(c[90][0])} a 90 anni; a 90 anni per strato di r − g da ${q2(c[90][2])} (S0) a ${q2(c[90][5])} (S3); ${q2(c[90][1])} nella regione dei bandi deserti [S], che segue quasi per costruzione dal modello [I]. <b>Non robusta</b>: dipende da η (0,07–0,24 per terzi di η, REPORT E v2 §5) [H]. Uguale per tutti i lotti: non si contano i lotti.</p>
<p class="note">Formulazioni ammesse (REPORT E v2 §5, §8): canone di pareggio come forbice; acquisto solo per le fasce B, C, D; cessione solo come quota con strati. Con suolo gratuito a 60 anni, 90 €/m²/anno non bastano per il nuovo nel 98% della regione tarata (F-a); il 5° percentile è 96,8 nella regione tarata, 102,0 nel cubo, 140,4 nei bandi deserti. Per il recupero (R1) il 5° percentile tarato a 60 anni è 72,8: in una parte della regione tarata 90 €/m²/anno bastano [I]. Fonte: tabelle/c_star_per_regione.csv, REPORT E v2 §4.</p>`;
  $("lfon").innerHTML = `<p>Mappa, NIL, DUSAF, PGT, DBT, OMI e metro: Spatial Milano Lab (prototipo del 27/10/2026, recuperato; fonti negli strati). Lotti: Base L v7 (congelata il 22/11/2026; licenze per lotto nella scheda). Economia: Base E v2 (congelata il 23/11/2026). Nessuna immagine AGEA.</p>
<p><b>Due annate OMI</b>: le dashboard del Lab usano OMI 2024 (2° semestre) su zone OMI 2021 riportate ai NIL; la Base E v2 e la zona OMI nella scheda del lotto usano OMI 2025/2.</p>
<p><b>Licenze</b> (come dichiarate nelle basi, <code>L_lotti/run.py</code>; non verificate sui siti dei titolari [L]):</p>
<table><tr><td>Catasto, Agenzia delle Entrate</td><td>CC BY 4.0</td></tr><tr><td>DBT 2020, Comune di Milano</td><td>CC BY 2.5 IT</td></tr><tr><td>DUSAF, Regione Lombardia</td><td>CC BY 4.0 [I] (licenza della versione 8.0 non letta)</td></tr><tr><td>PGT, mosaico Regione Lombardia</td><td>[L] non dichiarata</td></tr><tr><td>NIL ds964, ds503, ds677, ds2813, Comune di Milano</td><td>CC BY 4.0</td></tr><tr><td>Demanio (ds2688, ds2689)</td><td>CC BY 3.0 IT</td></tr><tr><td>Bonifiche ds600, Città Metropolitana</td><td>CC0</td></tr><tr><td>OMI, Agenzia delle Entrate</td><td>[L]</td></tr><tr><td>MEF, Istat (dashboard del Lab)</td><td>[L]</td></tr><tr><td>OpenStreetMap (indirizzi con cui il Lab riporta i CAP ai NIL)</td><td>ODbL, © OpenStreetMap contributors [L]</td></tr></table>
<p>Geometrie dei lotti semplificate di ${BL.tol} m (topologia preservata); superfici e capacità sono quelle della base. SHA-256 dei file letti al build:</p>
<table>${Object.entries(BL.sha).map(([k, v]) => `<tr><td class="mono">${esc(k)}</td><td class="mono">${v.slice(0, 12)}…</td></tr>`).join("")}</table>`;
}
function lotSel(id) {
  const L = LOTS.find((x) => x.p.id === id); if (!L) return false;
  selLot = L; if (dash !== "lotti") { dash = "lotti"; met = "lcl"; }
  if ($("lid").value.trim().toUpperCase() === id) { let x0 = 1e9, y0 = 1e9, x1 = -1e9, y1 = -1e9; L.poly.forEach((r) => r.forEach(([x, y]) => { x0 = Math.min(x0, x); y0 = Math.min(y0, y); x1 = Math.max(x1, x); y1 = Math.max(y1, y); })); const m = Math.max(x1 - x0, y1 - y0, .3); zoomed = L.p.ci; zoomVB([x0 - m, y0 - m, x1 - x0 + 2 * m, y1 - y0 + 2 * m]); }
  render(); return true;
}
const ST = { A: "A attuazione avviata", B: "B in istruttoria", C: "C solo previsione" };
const LNOTE = { E00170: ["lago su oltre metà della superficie (4,65 ha); la base non ha maschera dei corpi idrici: superficie utile e capacità sovrastimate", "[V] REPORT L v7 §7 · [I] sovrastima"] };
function lotCard(p) {
  const row = (a, b, m) => `<tr><th>${a}</th><td>${b}${m ? ` <span class="mono">${m}</span>` : ""}</td></tr>`, C3 = (a) => fa(a) + " alloggi (FAR 0,5 / 1 / 2)";
  let h = `<h5>${esc(p.id)} <span class="tag"><i aria-hidden="true" style="color:${KC[p.k]};font-style:normal">●</i> ${esc(KL[p.k])}</span></h5><table class="sch">`;
  if (p.k === "G") h += row("Nota", "<b>non verificato</b>: " + esc(p.verifica_destinazione) + "; classe se verificata: " + esc(p.classe_se_verificata), "[H] [L]");
  h += row("Superficie", n0(p.area_m2) + " m²: area della geometria della base (EPSG:32632) dopo unioni, ritagli e rimozione delle sovrapposizioni tra classi; non è la superficie catastale", "[V] Base L v7");
  if (LNOTE[p.id]) h += row("Problema noto", LNOTE[p.id][0], LNOTE[p.id][1]);
  if (p.k === "E") h += row("Capacità", C3([p.cap_far05, p.cap_far1, p.cap_far2]), "[H] ⌊0,70·FAR·area/80⌋");
  if (p.k === "R") h += row("Capacità", C3([p.cap_far05, p.cap_far1, p.cap_far2]) + " con demolizione e ricostruzione; recupero " + n0(p.cap_recupero) + "; scenario: " + esc(p.scenario_principale), "[H] recupero ⌊0,70·volume/3,2/80⌋");
  if (p.k === "A") h += row("Capacità", "non applicabile (area di attivazione, non destinata ad abitazioni)");
  if (p.k === "G") h += row("Capacità", "solo scenario, non verificato: " + C3([p.cap_scen_far05, p.cap_scen_far1, p.cap_scen_far2]) + (p.cap_scen_recupero ? "; recupero " + n0(p.cap_scen_recupero) : "") + ". Fuori dai totali.", "[H]");
  h += row("Origine", esc(p.origine) + (p.nota ? " — " + esc(p.nota) : ""), "[V] Base L v7");
  h += row("NIL", esc(p.nil_nome), "[V] ds964");
  h += row("Ambito PGT 2030", p.gruppo_ambito ? `${esc(p.ambito_pgt)} (${esc(p.codice_pgt)}, ${esc(p.gruppo_ambito)}); ${esc(p.strumento)}; data ${esc(p.data_ambito ?? "—")}; residenza 2030: ${esc(p.residenza_2030 ?? "—")}` + (p.fonte_ambito ? `; fonte: <span class="mono">${esc(p.fonte_ambito)}</span>` : "") : "fuori dagli ambiti 2030", p.gruppo_ambito === "GFU" ? "[H] perimetro 2012 sostitutivo" : "[V] pgt2030");
  const sm = p.marca_stato_riferimento;
  h += row("Stato attuativo", p.stato_riferimento ? esc(ST[p.stato_riferimento] || p.stato_riferimento.replace(" [L]", "")) + (p.fonte_stato_c1 ? `; fonte (codifica 1): <span class="mono">${esc(p.fonte_stato_c1)}</span>` : "") : (p.gruppo_ambito ? "in ambito, stato non censito" : "non censito (fuori dagli ambiti)"), sm ? (sm === "[L]" ? "[L] censimento" : "censimento: " + (sm === "V / ufficiale" ? "[V] fonte ufficiale" : "fonte " + esc(sm))) : "");
  h += row("Proprietà", esc(p.proprieta) + (p.proprieta === "non agganciata" ? " (non significa privata)" : "") + (p.proprieta_conflitto ? "; conflitto tra fonti" : ""), "[V] ds677, Demanio" + (p.proprieta === "non agganciata" ? " · [L] proprietà ignota" : ""));
  if (p.vincoli_noti) h += row("Vincoli noti", esc(p.vincoli_noti), "[V] ds600, PGT");
  if (p.potenziale_vuoto) h += row("Possibile area con potenziale", "sì (attributo informativo)", "[H] DUSAF 133/134 + DBT");
  if (p.omi) h += row("Zona OMI", esc(p.omi), "[V] OMI 2025/2");
  if (p.k === "E" || p.k === "R") {
    let t = "";
    if (!p.eco) t = "Acquisto non mostrato: fascia OMI E (E7, non informativo) o fascia mancante. Valgono i valori di pagina.";
    else for (const [v, a] of Object.entries(p.eco)) t += `<div><b>${{ nuovo: "nuovo", R2: "demolizione e ricostruzione", R1: "recupero (quota non robusta)" }[v]}</b>: canone di pareggio con suolo a mercato ${a[0]}–${a[2]} €/m²/anno (mediana ${a[1]}); quota della regione tarata in cui l'acquisto regge a 90 €/m²/anno: ${q2(a[3])}</div>`;
    h += row("Base E v2", t + `<div class="note">60 anni, FAR 1, valore finale nullo, regione tarata, 5–95%. Quote della regione dei parametri, non probabilità. Non è un vincolo.</div>`, "[H] H1–H19");
  }
  return h + row("Fonti della base", esc(p.fonti) + "; licenze: " + esc(p.licenze), "fonti e licenze dell'intera base, non verifiche di questo lotto") + "</table>";
}
function renderLotti() {
  RAMP = HUE.lab; document.documentElement.style.setProperty("--theme", RAMP[4]);
  const v = { E: 0, R: 0, A: 0, G: 0 }, vn = { E: 0, R: 0, A: 0, G: 0 };
  LOTS.forEach((L) => { const s = lotOk(L.p); L.el.style.display = s ? "" : "none"; L.el.classList.toggle("hot", L === selLot); if (s) { v[L.p.k]++; if (sel >= 0 && L.p.ci === sel) vn[L.p.k]++; } });
  if (selLot && !$("lotti").contains(document.activeElement)) $("lotti").appendChild(selLot.el);
  if (![...$("lotti").children].some((e) => e.tabIndex === 0 && e.style.display !== "none")) { LOTS.forEach((L) => (L.el.tabIndex = -1)); const f = selLot && selLot.el.style.display !== "none" ? selLot : LOTS.find((L) => L.el.style.display !== "none"); if (f) f.el.tabIndex = 0; }
  const T = BL.tot;
  $("k1").textContent = n0(v.E + v.R); $("k1l").textContent = `lotti visibili su 383 (edificabili e da riusare) · più ${n0(v.A)} / 268 aree di attivazione e ${n0(v.G)} / 50 lotti GFU fuori dai totali`;
  $("k2").textContent = sel >= 0 ? n0(vn.E + vn.R) : "–"; $("k2l").textContent = sel >= 0 ? `lotti visibili in ${C[sel].n} · più ${n0(vn.A)} aree di attivazione e ${n0(vn.G)} GFU` : "Seleziona un NIL";
  $("lcl").querySelectorAll("button").forEach((bt) => { const k = bt.dataset.k; bt.setAttribute("aria-pressed", LF.cl[k]); bt.querySelector(".vv").textContent = `${n0(v[k])} / ${n0(T.n[k])}`; });
  const c = T.cap;
  $("ltot").innerHTML = `<h5>Capacità della base <span class="mono">[H]</span></h5><table class="sch"><tr><th>Edificabili</th><td>${fa(c.E)} alloggi (FAR 0,5 / 1 / 2)</td></tr><tr><th>Da riusare</th><td>${fa(c.R)}; recupero ${n0(T.cap_rec_R)}</td></tr><tr><th>Attivazione</th><td>non applicabile</td></tr><tr><th>GFU</th><td>fuori dai totali; scenari non validati: ${T.gfu_scen.map((s) => `${esc(s[0])}: ${fa(s.slice(1))}`).join("; ")}</td></tr></table><p class="note" id="ltotn">Totale della base (edificabili): ${fa(c.E)} alloggi. GFU e aree di attivazione fuori dai totali. Fonte: Base L v7, tabelle/scenari_capacita.csv.</p>`;
  if (selLot) $("lsch").innerHTML = lotCard(selLot.p);
  $("src").textContent = "Fonte: Base L v7 (lotti, congelata il 22/11/2026) sui NIL dello Spatial Milano Lab; Base E v2 (congelata il 23/11/2026). Colori: classi dei lotti; GFU tratteggiate.";
}
lotInit();
SC.splice(9, 3, { user: "Mostrami i lotti della Base L v7.", d: "lotti", m: "lcl", html: () => {
  const T = BL.tot;
  return `<p>La Base L v7 ha ${K(n0(T.n.E) + " lotti edificabili")}, ${n0(T.n.R)} lotti da riusare e ${n0(T.n.A)} aree di attivazione; i ${n0(T.n.G)} lotti GFU stanno in una classe separata, <b>non verificata</b> e fuori dai totali.</p><ul><li>Capacità degli edificabili, come forbice: ${K(fa(T.cap.E) + " alloggi")} a FAR 0,5 / 1 / 2 [H].</li><li>La validazione C5 è inconcludente: la base è congelata per decisione di Dennis, non per una misura.</li><li>La Base E v2 accompagna i lotti con il canone di pareggio come forbice; non è un vincolo.</li></ul>` + cite("Base L v7, VERSIONE.md (22/11/2026)") + cite("Base E v2, VERSIONE.md (23/11/2026)") + `<p class="note">Clic su un lotto per la scheda; filtri e avvertenze nel pannello.</p>`;
} });
NAMES.splice(9, 3, "Base L v7: lotti");
/* zoom e spostamento della mappa piatta: viewBox dell'SVG (setVB del Lab); linee a spessore costante con vector-effect */
const flatOn = () => !svg.classList.contains("off");
const svgPt = (x, y) => new DOMPoint(x, y).matrixTransform(svg.getScreenCTM().inverse());
function zoomAt(f, x, y) {
  const b = svg.viewBox.baseVal, w = Math.min(FULL[2], Math.max(FULL[2] / 400, b.width * f)), k = w / b.width;
  vbAnim++; setVB([x - (x - b.x) * k, y - (y - b.y) * k, b.width * k, b.height * k]); fitText();
}
const zoomMid = (f) => { const b = svg.viewBox.baseVal; zoomAt(f, b.x + b.width / 2, b.y + b.height / 2); };
[["zin", () => zoomMid(1 / 1.5)], ["zout", () => zoomMid(1.5)], ["zrst", () => { zoomed = -1; zoomVB(FULL); }]].forEach(([id, fn]) => {
  const old = $(id).onclick; $(id).onclick = (e) => flatOn() ? fn() : old(e);
});
svg.addEventListener("wheel", (e) => { e.preventDefault(); const p = svgPt(e.clientX, e.clientY); zoomAt(Math.exp(e.deltaY * 0.0015), p.x, p.y); }, { passive: false });
const PTR = new Map(); let pan = null, moved = false;
svg.addEventListener("pointerdown", (e) => { PTR.set(e.pointerId, [e.clientX, e.clientY]); moved = false; pan = null; });
svg.addEventListener("pointermove", (e) => {
  if (!PTR.has(e.pointerId)) return;
  const prev = PTR.get(e.pointerId); PTR.set(e.pointerId, [e.clientX, e.clientY]);
  if (PTR.size === 2) { // pinch: rapporto delle distanze attorno al punto medio
    const [a, b] = [...PTR.values()], d = Math.hypot(a[0] - b[0], a[1] - b[1]), m = svgPt((a[0] + b[0]) / 2, (a[1] + b[1]) / 2);
    if (pan && pan.d) zoomAt(pan.d / d, m.x, m.y); pan = { d }; moved = true; return;
  }
  if (Math.hypot(e.clientX - prev[0], e.clientY - prev[1]) === 0) return;
  if (!pan) pan = { x: e.clientX, y: e.clientY };
  if (!moved && Math.hypot(e.clientX - pan.x, e.clientY - pan.y) < 4) return;
  if (!moved) try { svg.setPointerCapture(e.pointerId); } catch (x) { }
  moved = true; const p0 = svgPt(prev[0], prev[1]), p1 = svgPt(e.clientX, e.clientY), b = svg.viewBox.baseVal;
  vbAnim++; setVB([b.x - (p1.x - p0.x), b.y - (p1.y - p0.y), b.width, b.height]);
});
["pointerup", "pointercancel"].forEach((t) => svg.addEventListener(t, (e) => { PTR.delete(e.pointerId); if (!PTR.size) pan = null; }));
svg.addEventListener("click", (e) => { if (moved) { e.stopPropagation(); e.preventDefault(); moved = false; } }, true); // dopo un trascinamento niente clic
