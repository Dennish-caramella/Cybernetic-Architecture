# Confronto: analisi dati tipiche Bartlett RC14 (Londra) e pipeline Milano

Fonte: schede 36 (RC14), 34 (RC3/RC10/RC11/RC14), 32 (Meta London). Stato fonti: le schede dichiarano che per molti progetti i metodi sono estratti da parole chiave nella pagina (affidabili sul "quali metodi", non sul "come"). [S] = dalle schede, [I] = mia inferenza.

## 1. Cosa fanno tipicamente (32 progetti RC14 letti, 2020-2026) [S]
Flusso ricorrente in 5 passi: (1) strati di dati aperti su Londra a griglia; (2) riduzione (PCA, correlazioni, t-SNE); (3) clustering (K-Means, DBSCAN, SOM); (4) analisi spaziale (Space Syntax, VGA, isovist); (5) generazione/ottimizzazione/simulazione.
Frequenza indicativa: PCA/correlazione ~20; clustering ~20; Space Syntax e visibilità ~16; modelli generativi di immagini ~15; simulazione ~13; ottimizzazione evolutiva ~8.
Esempi più vicini a noi: IIG (2020, PCA + K-Means su griglia 10x10 m + analisi segmenti Depthmap), IsoChronic City (2022, PCA, K-Means, step depth, GA multi-obiettivo), Food-Topia (2023, PCA, K-Means, angular segment), ND2 (2023, ML per idoneità del suolo, indici composti), Re-Surge (2020, ML per destinazioni d'uso).

## 2. Dati usati [S]
Deprivazione (IMD), densità, verde, rumore, inquinamento, GPS, social media, Google Street View, OpenStreetMap, rete stradale (segmenti), criminalità, alberi, salute.

## 3. Cosa NON fanno (importante per la tesi) [S]
- Nessuna scheda riporta pesi, soglie, formule o metriche di validazione dei cluster: non reperito.
- Nessun progetto RC14 usa K-Means per "individuare lotti di social housing"; i cluster descrivono tipi di luogo. L'identificazione di aree di azione nei progetti viene da sovrapposizioni di strati e indici composti (es. ND2, "food desert index"), non dal cluster da solo. [I]
- Partecipazione: RC11/RC14 trattano il ML come strumento del progettista; l'utente non è oggetto di progetto. La partecipazione compare in RC3 (ANIMA, TetrAgora, Diffusive Habitats), ma come input dell'utente, con pesi non esposti. Meta London (AADRL) ha 4 sviluppatori + 1 pubblico con funzioni di ricavo, e la critica è proprio che le regole non sono esposte.

## 4. Confronto con la pipeline Milano
| Famiglia Bartlett | Pipeline attuale | Giudizio [I] |
|---|---|---|
| Dati a griglia, PCA, clustering | Sì (H3 res 9, PCA, K-Means con validazione) | allineato; noi aggiungiamo stabilità e senza etichette |
| Space Syntax (integrazione, step depth) | NO | lacuna principale: è ~metà dei progetti. Richiede rete stradale a segmenti |
| Indice di deprivazione | Parziale (OMI, età, NIL; reddito solo per CAP) | lacuna: serve indicatore di disagio a scala fine (ISTAT/Comune) |
| Ambiente (verde, rumore, inquinamento, alberi) | Solo verde | lacune: rumore, qualità dell'aria, alberi (da cercare nel Comune/ARPA) |
| Simulazione ad agenti | NO | fase successiva (gioco/negoziazione) |
| Idoneità/indici composti | Sì (WLC con pesi esposti, sensibilità) | più esplicito dei progetti Bartlett |

## 5. Dati più importanti per questo tipo di analisi (proposta) [I]
Nucleo: (a) bisogno/disagio abitativo, (b) uso del suolo e suolo disponibile, (c) accessibilità ai servizi, (d) rete stradale per Space Syntax, (e) forma costruita (DBT). Secondari: ambiente (rumore, aria, verde, alberi).

## 6. Conseguenza sul piano
- Il grafo/rete stradale non è un dettaglio rimandabile: serve a Space Syntax (integrazione, scelta) oltre che all'accessibilità. Va ricavato dal DBT o da fonte comunale; decidere con Dennis se OSM solo per questo.
- Aggiungere come strato candidato un indicatore di disagio a scala fine e dati ambientali dal Comune (da cercare).
- Mantenere l'onestà metodologica: i progetti Bartlett non dichiarano validazione; la nostra pipeline sì.
