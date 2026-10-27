#!/usr/bin/env python3
"""Esecuzione: python run_pipeline.py [--fixture] [--sensibilita]

Modalità reale: scarica da OpenStreetMap (serve rete) e legge i file ufficiali presenti in data_raw/.
Modalità --fixture: usa dati SINTETICI di collaudo in data_test/ (servono solo a provare il codice).
"""
import argparse
from pathlib import Path

from milano_pipeline import build, export

ap = argparse.ArgumentParser()
ap.add_argument("--fixture", action="store_true", help="usa data_test/ (dati sintetici) e scrive in data_output_test/")
ap.add_argument("--sensibilita", action="store_true", help="test di sensibilità alla risoluzione H3 (più lento)")
a = ap.parse_args()
root = Path(__file__).parent
if a.fixture:
    R = build.run_all(root, "config/pipeline.yaml", "tests/sources_test.yaml", "data_test", synthetic=True,
                      sensibilita=a.sensibilita, out_dir="data_output_test")
else:
    R = build.run_all(root, "config/pipeline.yaml", "config/sources.yaml", "data_raw", synthetic=False,
                      sensibilita=a.sensibilita, out_dir="data_output")
out = export.export_all(R)
print("Scritto in", out)
print("Celle:", len(R["cells"]), "| lotti candidati:", len(R["lots"]), "| K:", R["cluster_report"]["k_scelto"])
