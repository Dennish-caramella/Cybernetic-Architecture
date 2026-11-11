#!/bin/sh
# Revisione Base L v3: riesecuzione di run.py su una COPIA (run.py riscrive controllo_umano/ e controllo_secondo_codificatore/ con fogli vuoti).
# Uso: sh revisione/riesegui.sh /percorso/copia   (fuori dal repo; ~9 min da cache), poi confronta le tabelle con l'originale.
set -e; E=$(cd "$(dirname "$0")/../.." && pwd); C="$1/esperimenti"; mkdir -p "$C/L_lotti_v3"
ln -sfn "$E/L_lotti" "$C/L_lotti"; ln -sfn "$E/_cache" "$C/_cache"
cp -r "$E/L_lotti_v3/run.py" "$E/L_lotti_v3/test_lotti.py" "$E/L_lotti_v3/tabelle" "$E/L_lotti_v3/esecuzioni" "$E/L_lotti_v3/fig" "$C/L_lotti_v3/"
cd "$C/L_lotti_v3"; python3 run.py --no-fetch; python3 test_lotti.py; rm -rf controllo_umano controllo_secondo_codificatore
for f in tabelle/*.csv; do cmp -s "$f" "$E/L_lotti_v3/$f" && echo "uguale $f" || echo "DIVERSO $f"; done
python3 -c "import json; a, b = (json.load(open(p)) for p in ('esito_criteri.json', '$E/L_lotti_v3/esito_criteri.json')); print('chiavi diverse (escluso registro):', [k for k in a if k != 'registro' and a[k] != b.get(k)])"
