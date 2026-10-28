"""Crea site/: spatial-milano.html (con core.json e indice dei tasselli incorporati) e site/data/ (pgt.json, dusaf.json, t/<tx>_<ty>.json) da pubblicare insieme."""
import json, os, shutil

src = open("spatial-mi.src.html", encoding="utf-8").read()
assert "/*__CORE__*/" in src
core = json.load(open("out/core.json", encoding="utf-8"))
tiles = json.load(open("out/tiles.json", encoding="utf-8"))
for n in core["nil"]:  # indicatori DBT e catasto per NIL
    n["ind"].update({k: (round(v, 2) if isinstance(v, float) else v) for k, v in tiles["nil"].get(str(n["id"]), {}).items()})
core["tiles"] = {"tile": tiles["tile"], "index": tiles["index"], "uses": tiles["uses"]}
shutil.rmtree("site/data", ignore_errors=True)
os.makedirs("site/data/t", exist_ok=True)
open("site/spatial-milano.html", "w", encoding="utf-8").write(src.replace("/*__CORE__*/", json.dumps(core, separators=(",", ":"), ensure_ascii=False)))
for f in ("pgt.json", "dusaf.json"):
    shutil.copy(f"out/{f}", f"site/data/{f}")
for f in os.listdir("out/t"):
    shutil.copy(f"out/t/{f}", f"site/data/t/{f}")
size = sum(os.path.getsize(os.path.join("site/data/t", f)) for f in os.listdir("site/data/t"))
print("site pronto:", os.path.getsize("site/spatial-milano.html") // 1024, "KB pagina,", len(os.listdir("site/data/t")), "tasselli,", round(size / 1e6, 1), "MB")
