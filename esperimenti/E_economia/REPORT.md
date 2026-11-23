# Report di laboratorio — Base E: motore economico e gap fondiario (ticket #19)

Stato: **non congelata; revisione indipendente: ripeti** (v2 con lo stesso motore). E1–E4 passano, E5 non si applica, E6 non scatta. Congelamento: decisione di Dennis dopo la revisione (§7). Report assemblato dal coordinatore dalla consegna dell'agente `economista-abitativo`.

## 1. Ipotesi e soglia
Testo completo in `esecuzioni/00_preregistrazione.txt` (SHA-256 `ce059fd6…`, commit b3b0df6, prima di ogni esecuzione). Scelte H1–H9 accettate provvisoriamente dal coordinatore, non da Dennis (`tesi/DECISIONI.md`, 22/11); H1 (η = 0,85) scelta dopo un'occhiata ai risultati, dichiarata.
Criteri: E1 riproducibilità (hash di contenuto); E2 invarianti T1–T8; E3 coerenza con OMI; E4 taratura (5% < quota della regione < 95%); E5 casi osservati (errore mediano ≤ 20%, massimo ≤ 40%, almeno 3 casi); E6 nessun parametro senza fonte cambia il segno di ΔL in più di metà dei lotti.

## 2. Dati e fonti
OMI 2025/2 (dati.comune.milano.it, CC BY) [V]; Base L v7 (SHA-256 del gpkg verificato) [V]; relazione tecnica DG 365/2026 (copia Assolombarda) [V]; bando SACC 2014 [V]; listino costi CCIAA Como-Lecco [V]; Eurostat [V]; oneri di urbanizzazione solo [S] (comune.milano.it non usato). Geocodifica dei compendi DG 365 con Nominatim [I]. Overpass non raggiungibile dal proxy: non aggirato.

## 3. Metodo
Valore residuo del developer (RICS, margine sul ricavo); prezzo del suolo sostenibile per la cooperativa L* con flusso di cassa scontato sul canone a costo; ΔL = L(regime) − L* per acquisto (max(VRA, 0)), diritto di superficie (α·L_mkt) e cessione (0). Stessi costi e oneri nei due regimi (test). Calcolo per FAR 0,5/1/2 (forbice); riuso con recupero e con demolizione; GFU solo in scenario. Monte Carlo (seme 4519, 20.000 punti), taratura K1 (vincolo di segno dalla DG 365), tornado, mappe 2D. Hash di contenuto `11e200fb…` identico in due esecuzioni.

## 4. Risultati
- **Taratura K1**: ai valori centrali il modello giudica in perdita i tre compendi del Piano Casa (VAN da −7,7% a −9,6% dei costi), il Comune li giudica sostenibili; la regione tarata è il 28,4% dei punti. Parametri più spostati: tasso del debito, costo di costruzione, indicizzazione.
- **Canone di pareggio con suolo gratuito** (mediana): 185 €/m²/anno a 30 anni, 111 a 60, 87 a 90. Il tetto del Piano Casa è 90.
- **Cooperativa che regge a 90 €/m²/anno e 60 anni** (quota della regione tarata): cessione 0,11; acquisto B 0,00, C 0,01, D 0,06, E 0,11. A 90 anni: cessione 0,59, acquisto E 0,58, B 0,04. A 30 anni: circa 0.
- **Lotti edificabili in cui la cooperativa regge in più di metà della regione** (FAR 1): canone 90 e 60 anni 0 su 216; canone 90 e 90 anni 216 in cessione, 85 in acquisto; canone 130 e 60 anni 216 in cessione, 178 in acquisto.
- **ΔL in acquisto** (mediana, €/m² di lotto, FAR 1, canone 90, 60 anni): B 3.783, C 1.837, D 875, E 635. In cessione 635 in tutte le fasce.
- **Valore residuo del developer ≤ 0**: 22% dei lotti a FAR 0,5, 39% a FAR 1, 59% a FAR 2.
- **Lotti da riusare**: con recupero dell'edificio la cooperativa regge in cessione nel 64% della regione (pareggio 83 €/m²/anno); con demolizione solo nell'8–11%.
- Tabelle: `tabelle/delta_L_lotti.csv`, `regione_sintesi.csv`, `taratura_K1.csv`, `tornado.csv`, `gfu_scenario.csv`, `eta070_informativa.csv`; casi in `casi_taratura.csv`.

## 5. Esito
E1–E4 passano per la regola; la revisione propone **ripeti** (G1–G3). **E5 non si applica** (nessun caso osservato utilizzabile: il piano economico del Piano Casa e gli esiti dei bandi non sono pubblicati); E6 non scatta (massimo 0,389). La base è tarata solo da un vincolo di segno: **congelarla è decisione di Dennis** (pre-registrazione §6.4), dopo la revisione.

## 6. Limiti
- K1 è un solo vincolo di segno; il ramo developer non è tarato su compravendite di suolo. L'asta comunale dei diritti edificatori del 2023 (678 €/m² di SL, [S]) contro un valore residuo mediano di 189 €/m² in fascia D/E suggerisce che il developer **sottostimi il suolo di circa 3,6 volte** [I], quindi ΔL in acquisto è probabilmente sottostimato.
- La durata T domina: da 30 a 90 anni cambia il segno di ΔL per l'89% dei lotti.
- Lato cooperativa uguale in tutte le zone (nessun canone legato alla posizione); oneri da [S]; le quote sono quote del cubo dei parametri, non probabilità.
- η: con 0,70 la cooperativa regge molto meno (cessione 0,039 invece di 0,114).

## 7. Revisione indipendente
Testo completo in `REVISIONE.md`. **Esito proposto: ripeti** (pre-registrazione v2, stesso motore). Motore corretto e riprodotto (hash identico; lotto E00173 ricalcolato a mano).
- **G1**: la regione tarata vive dove il tasso di sconto della cooperativa r è vicino all'indicizzazione dei canoni g (r ≤ g nel 27,8% dei punti); la quota "cessione regge a 90 anni" scende da 0,59 a 0,36 con r − g ≥ 0,5 punti, e il "216 lotti su 216" diventa 0 sotto la quota 0,5.
- **G2**: E6 verificato solo a 60 anni e 90 €/m²; a 90 anni g e δ (senza fonte) cambiano il segno di ΔL nel 93–94% dei lotti.
- **G3**: in periferia il modello dà al suolo valore zero (fascia E: valore residuo mediano −467 €/m² di SL), contro 678 €/m² dell'asta comunale 2023 [S].
- Da correggere: VF = 0 decide il confronto (con valore finale l'acquisto regge in 149 lotti su 216 al punto base); T è una decisione; K1 è un'asserzione del Comune; nessuna geografia sul lato cooperativa; analisi pre-registrate mancanti; η senza fonte; riuso dipendente da ρ.
- Formulazioni corrette: "a 90 €/m² e 60 anni la cooperativa non paga il suolo di mercato" regge solo con VF = 0; "regge con suolo ceduto e 90 anni" va riscritta come "regge in circa metà della regione, solo se r supera di poco g". L'uscita più robusta è il canone di pareggio con la sua forbice.
- Rischi: non usare la Base E come vincolo in B0–B6 finché G3 non è risolto (spingerebbe verso la periferia).

## 8. Cosa passa alla prova successiva
`tabelle/delta_L_lotti.csv` (per lotto, FAR, variante, durata, canone, regime); il canone di pareggio come soglia per la fascia grigia; avvertenze su η, durata e ramo developer. Lettura per la tesi da **non** usare così (vedi §7): il risultato robusto è il canone di pareggio con suolo gratuito (circa 111 €/m²/anno a 60 anni, sopra il tetto di 90), con la sua forbice.
