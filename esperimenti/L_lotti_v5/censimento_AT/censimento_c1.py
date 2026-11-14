"""Scrive censimento_AT/fonti_AT.csv e codifica_1.csv (codificatore 1 = esecutore) dal foglio vuoto. Uso: python -I censimento_c1.py <cartella censimento_AT>"""
import sys, os, pandas as pd
d = sys.argv[1]; F = pd.read_csv(os.path.join(d, "foglio_vuoto.csv"), dtype=str).fillna("")
ACC = "2026-11-14"
REG = "https://www.cartografia.servizirl.it/arcgis1/rest/services/territorio/programmi/MapServer/1/query?where=CODICE_PROGETTO%3D164&outFields=*&returnGeometry=false&f=json"
FS = "https://www.fsitaliane.it/content/dam/fsitaliane/Documents/old-media-ed-eventi/comunicati-stampa-e-news/anno-2017/mese-giugno/2017_06_22_CS_Scali_ferroviari.pdf"
CDP = "https://www.cdp.it/resources/cms/documents/Lombardia_Milano_Caserma_Mameli.pdf"
INV = "https://www.invimit.it/firmato-il-protocollo-dintesa-tra-comune-di-milano-e-invimit-sgr-per-lo-sviluppo-sostenibile-dellarea-di-piazza-darmi/"
ELENCO = ("https://www.comune.milano.it/en/argomenti/rigenerazione-urbana/pubblicazioni-urbanistiche/strumenti-urbanistici-di-attuazione-del-pgt-e-loro-varianti-"
          "documentazione-vas-relativa-alle-proposte-di-trasformazione-urbanistica")
fonti = []  # ambito_id, fonte_url, fonte_titolo, fonte_ente, data_fonte, tipo_accesso, data_accesso, marca, contenuto
cod = {}
for _, r in F.iterrows():
    a = r.ambito_id
    fonti.append((a, r.fonte_ambito.split(";")[0].strip().split(" (")[0], "Scheda o strato regionale dell'ambito 2030", "Regione Lombardia (mosaico PGT / programmazione negoziata)",
                  "2020-02-05" if a.startswith("MA_") else ("2017-08-01" if a.startswith("ADP") else "2012-10-10 (perimetro 2012)"), "ufficiale raggiungibile", ACC, "V",
                  "previsione del PGT 2030 (PA/AS) o dell'AdP; per le GFU solo il perimetro AT 2012 sostitutivo"))
    if a.startswith("ADP_"):
        fonti.append((a, REG, "Stato Programmazione Negoziata: AdP Scali ferroviari (CODICE_PROGETTO 164)", "Regione Lombardia", "2017-08-01", "ufficiale raggiungibile", ACC, "V",
                      "decreto di approvazione n. 754 del 01/08/2017; delibera di adesione 6198 del 19/12/2007; STATO 'In attuazione' (campo del servizio, data di aggiornamento non dichiarata)"))
        fonti.append((a, FS, "CS: sottoscritto l'Accordo per il grande piano di riqualificazione delle 7 aree dismesse", "Ferrovie dello Stato Italiane", "2017-06-22", "ufficiale raggiungibile", ACC, "V",
                      "AdP firmato il 22/06/2017; 65% della ST a verde; San Cristoforo oasi 100%; Porta Genova 70% non residenziale; >= 30% residenza sociale e convenzionata"))
        cod[a] = ("A", "ignoto", "no", REG, "Stato Programmazione Negoziata: AdP Scali ferroviari", "Regione Lombardia", "2017-08-01", ACC, "si", "V", "",
                  "AdP approvato (decreto 754 del 01/08/2017) stato regionale In attuazione; cantieri e piani attuativi dei singoli scali non verificati da fonte ufficiale")
    elif a == "MA_6":
        fonti.append((a, CDP, "Lombardia - Milano - Caserma Mameli (scheda immobile)", "CDP Real Asset SGR", "2023-01-13", "ufficiale raggiungibile", ACC, "V",
                      "'Ad ottobre 2021 è stato approvato il Piano Urbanistico Attuativo (PUA)': 71.044 mq di SUL; bonifica da Piano Operazioni di Bonifica approvato"))
        cod[a] = ("A", "ignoto", "no", CDP, "Lombardia - Milano - Caserma Mameli (scheda immobile)", "CDP Real Asset SGR", "2023-01-13", ACC, "si", "V", "",
                  "PUA approvato a ottobre 2021 secondo CDP; stato del cantiere non verificato")
    elif a == "GFU_5263":
        fonti.append((a, INV, "Firmato il protocollo d'intesa tra Comune di Milano e Invimit SGR per lo sviluppo sostenibile dell'area di Piazza d'Armi", "Invimit SGR", "2025-12-23",
                      "ufficiale raggiungibile", ACC, "V", "protocollo approvato con delibera di Giunta; 80% a parco; ~122.000 mq di 144.000 mq di SL del PGT; residenze in larga parte a locazione "
                      "calmierata; prossimo passo: Convenzione Urbanistica Quadro"))
        cod[a] = ("B", "no", "no", INV, "Protocollo d'intesa Comune di Milano - Invimit SGR (Piazza d'Armi)", "Invimit SGR", "2025-12-23", ACC, "si", "V", "",
                  "protocollo d'intesa; nessun atto attuativo approvato; la fonte indica residenza ammessa (informativo per la regola GFU)")
    else:
        snip = {"MA_5": ("https://www.comune.milano.it/en/aree-tematiche/rigenerazione-urbana-e-urbanistica/archivio-2023",
                         "risultato di ricerca: PA7 adottato con DGC 1965 del 29/12/2022 e approvato con delibera n. 465 del 05/04/2023 [S]: non aperto"),
                "MA_17": ("https://www.comune.milano.it/en/aree-tematiche/rigenerazione-urbana-e-urbanistica/attuazione-pgt/pa3-viale-molise-ex-macello-piano-attuativo-obbligatorio",
                          "risultato di ricerca: VAS (DD 7541 del 12/09/2023); approvazione del PA attesa secondo la stampa [S]"),
                "GFU_5267": ("https://www.comune.milano.it/en/aree-tematiche/rigenerazione-urbana-e-urbanistica/attuazione-pgt/bovisa-goccia-villapizzone-grande-funzione-urbana",
                             "risultato di ricerca: accordo di programma Comune-Politecnico di ottobre 2022 [S]; non presente nello strato regionale della programmazione negoziata [V]"),
                "GFU_5281": ("https://www.comune.milano.it/en/aree-tematiche/urbanistica-ed-edilizia/attuazione-pgt/porto-di-mare-ambito-di-trasformazione-urbana",
                             "risultato di ricerca: GFU Porto di Mare; determina dirigenziale n. 196 del 17/01/2023 [S]")}.get(a)
        if snip:
            fonti.append((a, snip[0], "pagina di attuazione PGT (non aperta: sito escluso)", "Comune di Milano", "", "non usata (decisione di Dennis 14/11)", ACC, "S", snip[1]))
        cod[a] = ("N", "ignoto", "no", "", "", "", "", ACC, "no", "L", snip[0] if snip else ELENCO,
                  (snip[1] if snip else "nessuna fonte ufficiale raggiungibile trovata (ricerche: codice PA + nome + piano attuativo approvato / convenzione)"))
pd.DataFrame(fonti, columns=["ambito_id", "fonte_url", "fonte_titolo", "fonte_ente", "data_fonte", "tipo_accesso", "data_accesso", "marca", "contenuto"]).to_csv(os.path.join(d, "fonti_AT.csv"), index=False)
C = F.copy(); cols = ["categoria", "cantiere", "attuazione_conclusa", "fonte_url", "fonte_titolo", "fonte_ente", "data_fonte", "data_accesso", "fonte_ufficiale", "marca", "documento_da_aprire", "nota"]
for i, r in C.iterrows(): C.loc[i, cols] = cod[r.ambito_id]
out = os.path.join(d, "codifica_1.csv")
if os.path.exists(out): sys.exit("codifica_1.csv esiste: non sovrascrivo")
C.to_csv(out, index=False); print(C.categoria.value_counts().to_dict())
