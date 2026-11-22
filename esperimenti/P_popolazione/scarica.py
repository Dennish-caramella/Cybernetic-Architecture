"""Base P v1: scarica i dati grezzi in esperimenti/_cache/P_popolazione/raw/ e scrive dati_metadati.csv (url, licenza, data, sha256).
Uso: python3 -I scarica.py   (rifà solo i file mancanti)"""
import csv, hashlib, json, os, time, urllib.request

QUI = os.path.dirname(os.path.abspath(__file__))
RAW = os.path.join(QUI, "..", "_cache", "P_popolazione", "raw")
CKAN = "https://dati.comune.milano.it/api/3/action/package_show?id="
# (nome locale, pacchetto CKAN, sottostringa dell'url della risorsa)
COMUNE = [
    ("ds1441.zip", "ds1441-famiglie-tipologie-per-quartiere", "ds1441_popolazione_famiglie_tipologia_quartiere.zip"),
    ("ds139.zip", "ds139-popolazione-famiglie-tipologia-quartiere", "ds139_popolazione_famiglie_tipologia_quartiere_2007_2021.zip"),
    ("ds1457_titolo.csv", "ds1457-censimento-abitazioni-occupate-suddivisione-per-nil", "titolo_di_godimento_dellabitazione.csv"),
    ("ds205.csv", "ds205-sociale-caratteristiche-demografiche-territoriali-quartiere", ".csv"),
    ("ds71.csv", "ds71-popolazione-movimento-naturale-migratorio", ".csv"),
    ("ds752_2024_25.csv", "ds752_iscritti-nelle-universita-milanesi-anno-accademico-2017-avanti", "2024-25.csv"),
    ("ds964_nil.geojson", "ds964-nil-vigenti-pgt-2030", ".geojson"),
    ("ds634_civici.zip", "ds634-numeri-civici-coordinate", "final_csv.zip"),
    ("ds390.zip", "ds390-popolazione-pendolari-movimenti-interni-sezione-censimento-origine-destinazione-2011c", "2011c.zip"),
    ("ds391.zip", "ds391-popolazione-pendolari-in-uscita-sezione-censimento-origine-destinazione-2011c", "2011c.zip"),
    ("ds98_sezioni2011.geojson", "ds98_infogeo_sezioni_censimento_localizzazione_2011c", ".geojson"),
    ("ds47_nidi.geojson", "ds47-istruzione-asili-nido-localizzazione-delle-strutture", ".geojson"),
    ("ds3014_infanzia.geojson", "ds3014-infogeo-scuole-infanzia-localizzazione-2025-2026", ".geojson"),
    ("ds3015_primarie.geojson", "ds3015-infogeo-scuole-primarie-localizzazione-2025-2026", ".geojson"),
    ("ds3016_sec1.geojson", "ds3016-infogeo-scuole-secondarie-i-grado-localizzazione-2025-2026", ".geojson"),
    ("ds78_sec2.geojson", "ds78_infogeo_scuole_secondarie_ii_grado_localizzazione_", ".geojson"),
    ("ds94_atenei.geojson", "ds94-infogeo-atenei-sedi-localizzazione", ".geojson"),
    ("ds234_mmg.geojson", "ds234-sociale-medici-medicina-generale", ".geojson"),
    ("ds2841_confine.geojson", "ds2841-confini-amministrativi-del-comune-di-milano", ".geojson"),
    ("ds3024_omi_loc.csv", "ds3024-quotazioni-immobiliari-omi-locazione-semestre-2025-2", ".csv"),
    ("ds3023_zone_omi.geojson", "ds3023-zone-e-perimetri-omi-2025-2", ".geojson"),
]
MEF = "https://www1.finanze.gov.it/finanze/analisi_stat/public/v_4_0_0/contenuti/"
SDMX = "https://esploradati.istat.it/SDMXWS/rest/data/IT1,"
ALTRI = [  # (nome, url, licenza dichiarata dal sito, header Accept)
    ("mef_comunale_2024.zip", MEF + "Redditi_e_principali_variabili_IRPEF_su_base_comunale_CSV_2024.zip", "MEF-DF open data (licenza non letta in sessione)", None),
    ("mef_subcomunale_2024.zip", MEF + "Redditi_e_principali_variabili_IRPEF_su_base_subcomunale_CSV_2024.zip", "MEF-DF open data (licenza non letta in sessione)", None),
    ("istat_hudw_2021.csv", SDMX + "DF_DCSS_HUDW_1_COM,1.0/.015146........", "ISTAT CC BY 3.0 IT (dichiarata sul sito ISTAT, non riletta)", "application/vnd.sdmx.data+csv;version=1.0.0"),
    ("istat_redd_fam_lomb.csv", SDMX + "32_292_DF_DCCV_REDNETFAMFONTERED_9,1.0/.ITC4............", "ISTAT CC BY 3.0 IT (dichiarata sul sito ISTAT, non riletta)", "application/vnd.sdmx.data+csv;version=1.0.0"),
]

def get(url, accept=None):
    h = {"User-Agent": "tesi-base-P/1.0"}
    if accept: h["Accept"] = accept
    for k in range(3):
        try: return urllib.request.urlopen(urllib.request.Request(url, headers=h), timeout=300).read()
        except Exception as e:
            if k == 2: raise
            time.sleep(5)

def main():
    os.makedirs(RAW, exist_ok=True)
    meta = os.path.join(QUI, "dati_metadati.csv")
    righe = {r["file"]: r for r in csv.DictReader(open(meta))} if os.path.exists(meta) else {}
    todo = []
    for nome, pkg, sub in COMUNE:
        if nome in righe and os.path.exists(os.path.join(RAW, nome)): continue
        d = json.loads(get(CKAN + pkg))["result"]
        res = [r for r in d["resources"] if sub in r["url"]]
        todo.append((nome, res[0]["url"], f"{d.get('license_title')} (CKAN {pkg}, modificato {d.get('metadata_modified','')[:10]})", None))
    todo += [a for a in ALTRI if not (a[0] in righe and os.path.exists(os.path.join(RAW, a[0])))]
    for nome, url, lic, acc in todo:
        b = get(url, acc)
        open(os.path.join(RAW, nome), "wb").write(b)
        righe[nome] = dict(file=nome, url=url, licenza=lic, scaricato=time.strftime("%Y-%m-%dT%H:%M:%SZ", time.gmtime()),
                           byte=len(b), sha256=hashlib.sha256(b).hexdigest())
        print("ok", nome, len(b))
    with open(meta, "w", newline="") as f:
        w = csv.DictWriter(f, ["file", "url", "licenza", "scaricato", "byte", "sha256"]); w.writeheader()
        for k in sorted(righe): w.writerow(righe[k])

if __name__ == "__main__":
    main()
