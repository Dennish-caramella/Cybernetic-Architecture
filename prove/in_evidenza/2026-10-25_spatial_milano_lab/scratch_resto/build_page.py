"""Incorpora osm_mb.json, istat_mb.json, hex_mb.json e detail_mb.json in spatial-mb.src.html e scrive spatial-agent-prototype.html (la pagina da pubblicare)."""
src = open("spatial-mb.src.html", encoding="utf-8").read()
parts = {"OSM": "osm_mb.json", "IST": "istat_mb.json", "HEX": "hex_mb.json", "DET": "detail_mb.json"}
data = "\n".join(f"const {k}={open(f, encoding='utf-8').read()};" for k, f in parts.items())
assert "/*__DATA__*/" in src
open("spatial-agent-prototype.html", "w", encoding="utf-8").write(src.replace("/*__DATA__*/", data))
print("scritto spatial-agent-prototype.html", len(data) // 1024, "KB di dati")
