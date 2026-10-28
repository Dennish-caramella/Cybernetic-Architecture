// Verifica del prototipo: sintassi dello script, motore di voto, percorso dei dati di lab.json.
// Uso: node lab/prototype/test_proto.mjs   (dopo build_proto.py)
import fs from "node:fs";
import vm from "node:vm";
import path from "node:path";
import assert from "node:assert/strict";
import { fileURLToPath } from "node:url";

const here = path.dirname(fileURLToPath(import.meta.url));
const html = fs.readFileSync(path.join(here, "site", "spatial-milano-lab.html"), "utf8");
const lab = JSON.parse(fs.readFileSync(path.join(here, "site", "data", "lab.json"), "utf8"));
const out = {};

// 1. sintassi: compila lo script della pagina
const js = [...html.matchAll(/<script>([\s\S]*?)<\/script>/g)].map((m) => m[1]).join("\n");
new vm.Script(js, { filename: "page.js" });
out.syntax = "ok";

// 2. motore: estratto dalla pagina, eseguito da solo
const eng = js.slice(js.indexOf("/*LAB-ENGINE-START*/"), js.indexOf("/*LAB-ENGINE-END*/"));
const E = vm.runInNewContext(eng + ";LabEngine", { Math, Float64Array, Array, isFinite });
let seed = 7; const rnd = () => ((seed = (seed * 1103515245 + 12345) % 2147483648) / 2147483648);
const X = lab.sites.map((s) => s.x), m = lab.criteria.length;
// teach-back: oltre la soglia il segno si inverte, sotto no
for (let k = 0; k < 200; k++) {
  const w = Array.from({ length: m }, () => rnd()); const s = w.reduce((a, b) => a + b); w.forEach((_, j) => (w[j] /= s));
  const a = X[(rnd() * X.length) | 0], b = X[(rnd() * X.length) | 0], t = E.teach(w, a, b);
  if (!t.best) continue;
  const at = (tt) => { const v = w.slice(); v[t.best.j] += tt; return E.dot(v.map((x) => x / (1 + tt)), a.map((x, j) => x - b[j])); };
  const tt = t.best.t, eps = 1e-6 * Math.sign(tt || 1);
  assert.ok(Math.sign(at(tt + eps)) !== Math.sign(t.delta) || Math.abs(at(tt + eps)) < 1e-9, "teach-back non inverte");
  assert.ok(t.best.to >= -1e-12 && t.best.to <= 1 + 1e-12, "peso fuori da [0,1]");
}
out.teach = "ok";
// recupero dei pesi: 25 risposte simulate (logistiche, beta 15) con domande attive su siti reali
const tv = (p, q) => p.reduce((s, v, j) => s + Math.abs(v - q[j]), 0) / 2, res = [];
for (let r = 0; r < 8; r++) {
  const wt = lab.archetypes[r % 4].mu, P = E.make(m, 1000, rnd), tv0 = tv(E.mean(P), wt);
  for (let q = 0; q < 25; q++) {
    const cand = Array.from({ length: 300 }, () => (rnd() * X.length) | 0), { pair } = E.pickPair(P, X, cand);
    const [a, b] = pair, pa = 1 / (1 + Math.exp(-15 * E.dot(wt, X[a].map((x, j) => x - X[b][j]))));
    if (rnd() < pa) E.update(P, X[a], X[b]); else E.update(P, X[b], X[a]);
  }
  res.push([tv0, tv(E.mean(P), wt)]);
}
const mean = (k) => res.reduce((s, x) => s + x[k], 0) / res.length;
out.weight_recovery = { tv_prior: +mean(0).toFixed(3), tv_after_25: +mean(1).toFixed(3) };
assert.ok(mean(1) < mean(0) * 0.8, "il voto non avvicina i pesi veri");

// 3. dati: decodifica come la pagina, coerenza con il CORE incorporato
const c0 = html.indexOf("const CORE = ") + 13, coreTxt = html.slice(c0, html.indexOf("const $ = ", c0)).trim().replace(/;$/, "");
const CORE = JSON.parse(coreTxt), U = CORE.meta.unit_km, u = lab.meta.unit_km;
const dec = (a, k) => { const o = []; let x = 0, y = 0; for (let i = 0; i < a.length; i += 2) { x += a[i]; y += a[i + 1]; o.push([x * k, y * k]); } return o; };
let bx = [1e9, 1e9, -1e9, -1e9]; CORE.nil.forEach((n) => n.rings.forEach((r) => dec(r, U).forEach(([x, y]) => { bx = [Math.min(bx[0], x), Math.min(bx[1], y), Math.max(bx[2], x), Math.max(bx[3], y)]; })));
const nilIds = new Set(CORE.nil.map((n) => n.id)); let outside = 0;
lab.sites.forEach((s) => { assert.ok(nilIds.has(s.nil), "NIL sconosciuto " + s.nil); s.g.forEach((rs) => rs.forEach((r) => dec(r, u).forEach(([x, y]) => { if (x < bx[0] || x > bx[2] || y < bx[1] || y > bx[3]) outside++; }))); assert.equal(s.x.length, m); });
assert.equal(outside, 0, "vertici fuori dal comune");
const ids = new Set(lab.sites.map((s) => s.id));
lab.portfolios.forEach((p) => { assert.equal(p.sites.length, p.dw.length); p.sites.forEach((id) => assert.ok(ids.has(id), "sito mancante " + id)); });
["AT", "ERP", "AMB_DEG", "RIG"].forEach((g) => assert.ok(lab.audit[g] && lab.audit[g].claim_it, "audit " + g));
const ppHit = CORE.nil.filter((n) => lab.nil[n.id] && lab.nil[n.id].res_basket_med != null).length;
out.data = { sites: lab.sites.length, portfolios: lab.portfolios.length, nil_with_pp: ppHit, lab_json_mb: +(fs.statSync(path.join(here, "site", "data", "lab.json")).size / 1e6).toFixed(2) };
assert.ok(ppHit >= 85);
console.log(JSON.stringify(out));
