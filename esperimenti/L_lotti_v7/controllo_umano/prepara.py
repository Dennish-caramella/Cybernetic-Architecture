"""Controllo umano di C5 (PREREG_controllo_umano.txt): estrae 10 lotti per strato (seme 8811), scrive la chiave e il file HTML per Dennis.
Uso: python prepara.py   (si rifiuta se la chiave esiste). HTML (immagini AGEA, sola visione) in ../../_cache/L_lotti_v7/controllo_umano/, non in git."""
import base64, io, json, os, sys
import numpy as np, pandas as pd, geopandas as gpd
import importlib.util
_sp = importlib.util.spec_from_file_location("run_v7", os.path.join(os.path.dirname(os.path.abspath(__file__)), "..", "run.py"))  # nome diverso: run.py importa "run" di v1
run = importlib.util.module_from_spec(_sp); _sp.loader.exec_module(run)  # guard __main__: servono solo orto_image, CL, ID, STRATI

HERE = os.path.dirname(os.path.abspath(__file__)); KEY = os.path.join(HERE, "chiave_umano.csv")
OUT = os.path.join(HERE, "..", "..", "_cache", "L_lotti_v7", "controllo_umano"); SEED, N = 8811, 10
if os.path.exists(KEY): raise SystemExit("chiave già presente: non sovrascrivo")
L = gpd.read_file(os.path.join(HERE, "..", "lotti_v7.gpkg"), layer="lotti"); pop = L[L.classe.isin(run.CL)]
st = pd.Series(np.where(pop.lotto_at == 1, "D", "F"), index=pop.index) + "-" + pop.classe.map(run.ID)
rng = np.random.default_rng(SEED); sel = []
for h in run.STRATI:
    ids = pop.index[st == h][np.argsort(pop.id[st == h].values)]; sel += list(ids[rng.choice(len(ids), N, replace=False)])
cod = np.argsort(rng.permutation(len(sel))); S = pop.loc[sel].assign(strato=st[sel].values)
S["codice"] = ["H%02d" % (c + 1) for c in cod]; S = S.sort_values("codice")
os.makedirs(OUT, exist_ok=True); cards = []
for c, g in zip(S.codice, S.geometry):
    f = os.path.join(OUT, c + ".jpg")
    if not os.path.exists(f): run.orto_image(g, f, 800)
    cards.append((c, base64.b64encode(open(f, "rb").read()).decode()))
S[["codice", "id", "strato", "classe", "ambito_id", "gruppo_ambito", "lotto_at", "area_m2"]].to_csv(KEY, index=False)
Q = [("L", "libera: suolo nudo, sterrato, prato o incolto non curato, piazzale vuoto"), ("C", "cantiere"), ("D", "edificato dismesso o degradato (tetti rotti o crollati, vegetazione su edifici o piazzali, nessun segno d'uso)"),
     ("U", "edificato o area in uso (cortili, parcheggi pieni, pertinenze)"), ("V", "verde curato (parco, giardino) o agricolo coltivato"), ("I", "infrastruttura in uso (binari attivi, strade, piazzali di servizio)"), ("X", "non giudicabile")]
legenda = "".join(f"<li><b>{k}</b> {t}</li>" for k, t in Q)
card = lambda c, b: (f'<section id="{c}"><h3>{c}</h3><img src="data:image/jpeg;base64,{b}" alt="{c}"><div class="q">' +
                     "".join(f'<label><input type="radio" name="{c}" value="{k}"> {k}</label>' for k, _ in Q) + f'<input class="n" name="n_{c}" placeholder="nota (facoltativa)"></div></section>')
html = f"""<!doctype html><meta charset="utf-8"><meta name="viewport" content="width=device-width,initial-scale=1"><title>Controllo umano C5, Base L v7</title>
<style>body{{font:15px system-ui;max-width:900px;margin:auto;padding:12px}}img{{max-width:100%;border:1px solid #888}}section{{margin:18px 0;padding-bottom:10px;border-bottom:1px solid #ccc}}.q label{{margin-right:14px;font-size:18px}}.n{{width:60%;margin-top:6px}}button{{font-size:17px;padding:8px 14px}}</style>
<h1>Controllo umano C5 — Base L v7</h1><p>60 immagini aeree AGEA 2018–2019 (licenza di sola visione: <b>non diffondere</b>). Per ciascuna guarda la parte <b>dentro il contorno rosso</b> e scegli la categoria che occupa la parte più grande dell'area (non la più interessante). Se nessuna supera la metà scegli comunque la maggiore. Il lavoro si salva da solo in questo browser; alla fine premi «Scarica CSV» e rimandami il file.</p>
<ul>{legenda}</ul><p><button onclick="out()">Scarica CSV</button> <span id="cnt"></span></p>{"".join(card(c, b) for c, b in cards)}
<p><button onclick="out()">Scarica CSV</button></p>
<script>const K="c5umano8811",cs={json.dumps([c for c, _ in cards])};let s={{}};try{{s=JSON.parse(localStorage.getItem(K)||"{{}}")}}catch(e){{}}
function ren(){{let n=0;cs.forEach(c=>{{if(s[c]&&s[c][0])n++;}});document.getElementById("cnt").textContent=n+" / 60 codificate"}}
cs.forEach(c=>{{const v=s[c];if(v){{const r=document.querySelector(`input[name="${{c}}"][value="${{v[0]}}"]`);if(r)r.checked=true;document.querySelector(`input[name="n_${{c}}"]`).value=v[1]||""}}}});ren();
document.addEventListener("input",e=>{{cs.forEach(c=>{{const r=document.querySelector(`input[name="${{c}}"]:checked`);s[c]=[r?r.value:"",document.querySelector(`input[name="n_${{c}}"]`).value]}});try{{localStorage.setItem(K,JSON.stringify(s))}}catch(x){{}};ren()}});
function out(){{const t="codice,Q1,nota\\n"+cs.map(c=>[c,(s[c]||[])[0]||"",((s[c]||[])[1]||"").replace(/[,\\n]/g," ")].join(",")).join("\\n")+"\\n";const a=document.createElement("a");a.href=URL.createObjectURL(new Blob([t],{{type:"text/csv"}}));a.download="codifica_umana.csv";a.click()}}</script>"""
open(os.path.join(OUT, "controllo_umano.html"), "w").write(html); print(len(S), S.strato.value_counts().to_dict(), os.path.getsize(os.path.join(OUT, "controllo_umano.html")) // 1024, "KB")
