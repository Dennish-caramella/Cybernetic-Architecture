# PGT 2030: cosa scaricare e dove metterlo

Decisione del 14/11/2026: nella Base L v5 gli ambiti di trasformazione si leggono dal **PGT 2030 vigente** (non dal PGT 2012 dello strato regionale).

## 1. Scaricato automaticamente dall'agente (non devi fare nulla)
Schede del Piano delle Regole PGT 2030, pubblicate il 05/02/2020, dal mosaico della Regione Lombardia. Verificate raggiungibili il 14/11/2026 [V]:
https://www.cartografia.servizirl.it/schede_pgt/015146/015146_20200205_MA_1.pdf
… fino a MA_18 (`015146_20200205_MA_<n>.pdf`, n = 1…18).

## 2. Da scaricare TU dal browser
Il sito del Comune blocca le richieste automatiche: queste pagine le devi aprire tu. Salva i file in questa cartella, con questi nomi:

**Cartella dove metterli:** `esperimenti/_cache/pgt2030/` (la cartella è esclusa da git, quindi non pesa sul repo).

| Cosa | Dove trovarlo | Nome del file da salvare |
|---|---|---|
| Documento di Piano PGT 2030 (ambiti di trasformazione, allegati) | https://pgt.comune.milano.it/ | `documento_di_piano_2030.pdf` |
| Elenco degli strumenti attuativi e delle varianti | https://www.comune.milano.it/en/argomenti/rigenerazione-urbana/pubblicazioni-urbanistiche/strumenti-urbanistici-di-attuazione-del-pgt-e-loro-varianti-documentazione-vas-relativa-alle-proposte-di-trasformazione-urbanistica | `elenco_strumenti_attuativi.pdf` (o salva la pagina come PDF) |
| Scali ferroviari: accordo di programma e allegati | https://www.comune.milano.it/en/-/adp-scali-ferroviari-ratifica-allegati-alla-delibera-di-c.c.-n.-19-2017 | `adp_scali_2017.pdf` |
| Piazza d'Armi | https://www.comune.milano.it/en/-/piazza-d-armi.-liberata-l-area-ora-avanti-con-la-messa-in-sicurezza | `piazza_darmi.pdf` (salva la pagina) |
| Porto di Mare | https://www.comune.milano.it/en/aree-tematiche/urbanistica-ed-edilizia/attuazione-pgt/porto-di-mare-ambito-di-trasformazione-urbana | `porto_di_mare.pdf` (salva la pagina) |
| Toffetti | https://www.comune.milano.it/toffetti-n.90-92-94-piano-attuativo | `toffetti.pdf` (salva la pagina) |

Se una pagina non si apre, o il file non esiste più, dimmelo: la sostituiamo con quella giusta. Non serve scaricare niente altro.

## 3. Per le immagini dei lotti
Non serve chiedere al Comune le foto delle aree degradate. Per localizzare un lotto usiamo immagini satellitari recenti, dell'area della particella. La fonte da confermare è Sentinel-2 (Copernicus, libera, 10 m, aggiornata), che l'agente verificherà prima di usarla.

## 4. Il controllo sui 20 casi (C7)
Lo consideriamo superato, come da tua conferma del 14/11. Per registrare il numero preciso di casi concordi mi serve il file compilato `esperimenti/L_lotti_v3/controllo_umano/modulo_dennis.csv`; se lo hai compilato, mettilo nella stessa cartella dei link o dimmi dove si trova.
