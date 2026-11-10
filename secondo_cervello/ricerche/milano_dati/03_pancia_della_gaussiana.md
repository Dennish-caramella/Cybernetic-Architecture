# 03 — La "pancia della gaussiana": definizione, assi, soglie, quote (Milano)

Data: 2026-11-10. Stato: **nota di lavoro**, non capitolo di tesi. Figure e script in `pancia/`.
Marche: [V] verificato su fonte scaricata in questa sessione · [S] fonte secondaria (stampa, snippet di ricerca, da verificare) · [L] letteratura/canone non riletto qui · [I] inferenza o approssimazione mia · [H] ipotesi.

---

## 0. Attribuzione a Sanchez: esito della verifica

**Non trovata.** Ricerche web del 10/11/2026 su "Jose Sanchez" + "bell curve", "belly of the curve", "belly of the bell curve", "middle"/"design for the average" con *Architecture for the Commons*, Plethora Project, Block'hood/Common'hood: nessun risultato che leghi Sanchez alla curva a campana [V: assenza nei risultati]. Il paper ACADIA 2018 (`acadia18_108.pdf`, testo completo scaricato) non contiene "bell", "belly", "curve", "gauss", "middle", "majority", "average" [V]. La pagina Plethora del libro neppure [V].

Attenzione alla scheda `secondo_cervello/schede/11_Sanchez_We_Have_Always_Been_Parametric_...md` §5: afferma che Sanchez parla di *"reclaiming the belly of the bell curve"*. **Né questa frase né il titolo "We Have Always Been Parametric" risultano in rete** [V: ricerca esatta senza esiti]. La scheda va trattata come non affidabile su questo punto (probabile riassunto generato) finché non si controlla sul volume cartaceo (introduzione e capp. 1 e 3). Conferma la conclusione del report *Lotti per social housing partecipativo*.

**Formula consigliata per la tesi:** presentare la "pancia" come **costrutto dell'autore**, in dialogo con il terzo settore dei *commons* di Sanchez (pubblico / privato / commons), non come sua citazione. Esiste invece un aggancio istituzionale solido: la Regione Lombardia definisce la **"fascia grigia"** come i nuclei con *"una capacità economica che non consente né di sostenere un canone di locazione o un mutuo sul mercato abitativo privato né di accedere ad un servizio abitativo pubblico"* (DGR XII/5248 del 3/11/2025, allegato, pp. 5-6) [V]. È esattamente la pancia, detta con parole di una fonte citabile.

---

## 1. Che cosa misura la curva

### 1.1 Asse y
Quota (densità) di unità per intervallo di reddito. Unità ideale: **famiglia (nucleo)**, perché ERP, ISEE e canone si riferiscono al nucleo. Unità disponibile a scala comunale: **contribuente IRPEF** (MEF). Va detto sempre quale si usa.

### 1.2 Tre candidati per l'asse x

| # | Asse x | Pro | Contro | Dati per Milano |
|---|---|---|---|---|
| A | **Reddito complessivo IRPEF per contribuente** (lordo) | Ufficiale, comunale, annuale, per classi | Individuo ≠ famiglia; lordo; esclude redditi esenti/cedolare/finanziari; niente patrimonio | MEF a.i. 2024 [V] — usato in fig. b |
| B | **Reddito disponibile equivalente della famiglia** (scala OCSE modificata o ISEE) | Unità corretta, confrontabile tra nuclei | Non pubblicato a scala comunale; serve microdato (EU-SILC/IT-SILC, Banca d'Italia IBF) o ISEE aggregati INPS | Da cercare [H: ISTAT/INPS a scala provinciale] |
| C | **Reddito residuo dopo il canone di mercato** (capacità di pagare): reddito disponibile − canone di riferimento − paniere minimo | È la grandezza teoricamente giusta per la crisi abitativa: la pancia diventa "chi ha reddito residuo < soglia minima a mercato ma > requisito ERP" | Serve definire canone di riferimento (per dimensione del nucleo e zona OMI) e paniere minimo (es. soglia di povertà assoluta ISTAT per area metropolitana) | Combinazione B + OMI [I] |

**Raccomandazione [I]:** A per la figura empirica di oggi (è l'unica fonte comunale completa); C come **definizione operativa** della tesi (popolazione bersaglio del modello di fabbisogno), costruita a partire da B quando si avrà il microdato. Il report *Lotti...* propone già "gap di accessibilità per NIL (OMI − affitto sostenibile)": è C su base territoriale.

### 1.3 Perché "gaussiana" è una metafora
- La distribuzione dei redditi è **asimmetrica a destra**, non normale. A Milano (a.i. 2024): reddito medio per contribuente **41.865 €**, mentre la mediana cade a circa **26.000 €** (il 50,1% dei contribuenti con reddito > 0 sta sotto i 26.000) [V, calcolo su MEF]. Media ≫ mediana è la firma dell'asimmetria. Il 4,9% oltre 120.000 € dichiara da solo il 33% del reddito complessivo (14,0 su 42,4 mld) [V, calcolo].
- Modelli standard: **lognormale** e **Dagum** (Burr III) [L: Kleiber & Kotz 2003, *Statistical Size Distributions in Economics and Actuarial Sciences*]. Sui dati raggruppati MEF il Dagum si adatta meglio della lognormale, ma nessuno dei due riproduce bene la classe 26-55k (attesi 303.000 contro 328.425 osservati con Dagum) [V, `pancia.py`]: i fit servono solo a interpolare dentro le classi, non come modello.
- **Dove la metafora regge:** su scala **logaritmica** del reddito la lognormale *è* una gaussiana; la "campana" ricompare (fig. b, pannello destro). Dire "campana sul logaritmo del reddito" è corretto.
- **Dove inganna:** (1) suggerisce simmetria: le code non sono speculari, la coda destra è lunga e sottile, quella sinistra è larga; (2) suggerisce che la pancia sia "media ± σ": invece **le soglie sono istituzionali** (ISEE, canone), non statistiche; (3) "pancia" evoca la maggioranza: con le soglie reali la pancia è **un quarto-due quinti** dei contribuenti, non la maggioranza, mentre la coda sinistra per reddito pesa la metà (§3); (4) rischio di confondere distribuzione dei **redditi** (popolazione bersaglio) con media delle **preferenze** (vedi report *Lotti...*, §"La pancia della gaussiana è una fascia di reddito").

---

## 2. Le soglie

Tutte le soglie ISEE vanno tradotte sull'asse x. Conversione usata [I], per **nucleo di una persona, lavoratore dipendente, in affitto con canone ≥ 7.000 €/anno, patrimonio nullo** (scala di equivalenza = 1):
ISR = reddito complessivo − min(20% redd. lavoro dip., 3.000) − min(canone, 7.000) (DPCM 159/2013 art. 4 c. 2-4) [V, testo 2013; il DPCM 13/2025 ha modificato l'art. 4: controllare il testo vigente]. Quindi **reddito lordo ≈ ISEE + 10.000**.

| Soglia | Valore normativo | Fonte | Equivalente lordo (persona sola, in affitto) |
|---|---|---|---|
| **S1. Accesso ERP/SAP** | ISEE ≤ 16.000 €, più patrimonio ≤ 22.000 € (1 pers.) / 16.000 + 5.000×PSE | RR Lombardia 4/2017 art. 7 c. 1 lett. c, testo coordinato con RR 2/2025 [V] | **≈ 26.000 €** [I] (coincide col limite di classe MEF) |
| Permanenza ERP | ISEE ≤ 35.000 € | RR 4/2017, decadenza [V] | ≈ 45.000 € [I] |
| **S2a. Tetto housing sociale ("fascia grigia")** | ISEE tra 14.000 e 40.000 € nei bandi ALER Milano di housing sociale (es. bando "Cova"); avviso 65 alloggi Municipi 3-4-6-8 ISEE max 40.000 | stampa (Affaritaliani, Milanofree) [S] — bando originale non scaricato (host bloccato) | ≈ 50.000 € [I] |
| Piano Casa Comune di Milano | 10.000 alloggi in 10 anni (6.500 città, 3.500 hinterland); canoni circa 375-675 € per 50 m² (ex Palasharp, San Romanello, Bovisasca) | stampa [S]; requisiti di reddito non trovati in fonte ufficiale | — |
| **S2b. Sostenibilità del mercato** | canone ≤ 30% del reddito | regola convenzionale [L]; il Piano Casa nazionale 2026 la usa come "soglia di sostenibilità del 30%" [S] | v. sotto |

**Canone di mercato di riferimento [V]:** OMI-Agenzia delle Entrate, *Statistiche trimestrali residenziale IV 2025*, tab. 8: a Milano i nuovi contratti ordinari di lungo periodo (ORD_L, 4+4) sono 7.701 per 110 mln €/anno → **14.284 €/anno ≈ 1.190 €/mese per abitazione** (tutti i nuovi contratti per intero: 18.363 per 252 mln → ≈ 1.144 €/mese). Limiti: media per contratto, non per m² né per tipologia; mln arrotondati; documento letto da copia su fimaamilano.it, non dal sito AdE.

- **S2b-lordo:** 14.284 / 0,30 = **47.613 € lordi** (soglia "generosa": il 30% del lordo è più del 30% del netto).
- **S2b-netto:** 30% del netto di un dipendente → **≈ 81.000 € lordi** [I, calcolo IRPEF 2024 semplificato in `pancia.py`: INPS 9,19%, aliquote 23/35/43, detrazione art. 13 TUIR, addizionali forfettarie 2,3%; ignora esonero contributivo e cuneo 2024; solo ordine di grandezza].

Le due soglie di mercato delimitano una **zona di transizione 47-81k**: dipende dalla definizione di sostenibilità, non dai dati. Notevole [I]: S2a (ISEE 40k ≈ 50k lordi) e S2b-lordo (≈ 48k) quasi coincidono, quindi il tetto dei bandi "fascia grigia" è coerente con la regola del 30% sul lordo.

---

## 3. Quote calcolate (Milano, contribuenti IRPEF, a.i. 2024)

Dati [V]: MEF-Dipartimento Finanze, *Redditi e principali variabili IRPEF su base comunale*, a.i. 2024 (dichiarazioni 2025), riga MILANO: 1.052.520 contribuenti; 1.013.593 con reddito complessivo; 206 con reddito ≤ 0 (esclusi) → base **1.013.387**. Classi: 0-10k 208.362 · 10-15k 89.347 · 15-26k 210.434 · 26-55k 328.425 · 55-75k 67.330 · 75-120k 60.251 · >120k 49.238.

Quote per zona (classi MEF rispettate; dentro la classe tagliata interpolazione con forma Dagum, tra parentesi interpolazione uniforme) [V+I]:

| Definizione della soglia destra | Sinistra (≤ 26k) | **Pancia** | Destra |
|---|---|---|---|
| Mercato, canone = 30% del lordo (47,6k) — **fig. b** | 50,1% | **27,1%** (24,2%) | 22,7% (25,7%) |
| Fascia grigia ISEE 40k (≈ 50k) | 50,1% | **29,0%** (26,8%) | 20,9% (23,0%) |
| Mercato, canone = 30% del netto (≈ 81k) | 50,1% | **40,4%** (39,9%) | 9,5% (10,0%) |

Lettura: **sul piano individuale, la pancia è tra un quarto e due quinti dei contribuenti milanesi** (circa 245.000-410.000 persone), secondo la definizione di sostenibilità. Ordine di grandezza coerente con la stima regionale ripresa da ANSA del 37-38% dei lavoratori dipendenti milanesi (citata nel report *Lotti...*) [S].

**La coda sinistra al 50% non significa "metà di Milano ha diritto all'ERP".** Contiene: il 20,6% sotto i 10.000 € (part-time, pensioni minime, secondi percettori, studenti, redditi parziali dell'anno); persone che vivono in nuclei con altri redditi; proprietari di casa (esclusi dall'ERP per patrimonio e titolarità); chi ha redditi non IRPEF. Per un nucleo di 3 persone con due percettori la soglia ERP sale a circa 45.600 € lordi **complessivi**, cioè ≈ 22.800 € ciascuno [I: ISEE 16.000 × 2,04 + 7.000 + 2 × 3.000]. La quota "eleggibile ERP" per famiglie sarà quindi molto più bassa: è il dato da produrre con il microdato (asse B).

---

## 4. Figure

- `pancia/fig_a_pancia_concettuale.png|.svg` — campana stilizzata con le tre zone (tutela pubblica ERP/SAP · pancia: commons / ceto medio senza risposta · mercato e committenza privata), soglie qualitative, nota "schema non in scala".
- `pancia/fig_b_pancia_empirica_milano.png|.svg` — sinistra: istogramma per densità delle classi MEF (asse lineare), fit Dagum e lognormale, soglie 26k / 47,6k / 81k, quote per zona; destra: stessa distribuzione su asse logaritmico, dove la campana ricompare.
- `pancia/pancia.py` — riproduce tutto (`python pancia.py`); `pancia/mef_irpef_milano_2024.csv` — riga Milano estratta dal file MEF.

Palette: blu-grigio (tutela), ocra (pancia), grigio (mercato) con tratteggi nella fig. a; leggibile in bianco e nero.

---

## 5. Limiti (da dichiarare in tesi)
1. **Contribuente ≠ famiglia.** Le soglie sono per nucleo; la distribuzione è per individuo. È il limite principale.
2. **Lordo ≠ disponibile.** Reddito complessivo IRPEF prima di imposte e contributi; esclude redditi esenti, a cedolare secca, finanziari. La soglia di mercato cambia molto (48k contro 81k) secondo lordo/netto.
3. **Niente patrimonio.** ISEE ed ERP contano patrimonio e proprietà; la pancia di inquilini e quella di proprietari non sono la stessa popolazione. Il bersaglio della tesi sono soprattutto **inquilini e nuovi entranti** [I].
4. **Classi grossolane.** Sette classi, una aperta; la soglia 47,6k cade dentro la classe 26-55k: la quota della pancia ha un'incertezza di ±3 punti secondo l'interpolazione.
5. **Canone medio cittadino.** Un'unica media OMI per contratto; non distingue dimensione, zona OMI, stato dell'immobile. Per la tesi: soglie per NIL/zona OMI e per dimensione del nucleo.
6. **Conversione ISEE → reddito** valida solo per persona sola, dipendente, in affitto, senza patrimonio. Testo DPCM 159/2013 letto nella versione 2013 (modificato dal DPCM 13/2025).
7. Fonti [S] (bandi ALER, Piano Casa) da sostituire con i bandi originali.

## 6. Come dirlo nella tesi (proposta di formulazione)
> Chiamo "pancia" della distribuzione — con una metafora che non va presa alla lettera, perché la distribuzione dei redditi è asimmetrica e la "campana" compare solo su scala logaritmica — l'insieme dei nuclei il cui reddito supera la soglia di accesso ai servizi abitativi pubblici (ISEE 16.000 €, RR Lombardia 4/2017) ma non basta a sostenere un canone di mercato entro il 30% del reddito. È ciò che la Regione Lombardia chiama "fascia grigia" (DGR XII/5248/2025). A Milano, su base individuale, vale tra il 27% e il 40% dei contribuenti IRPEF (a.i. 2024), secondo che la sostenibilità si misuri sul reddito lordo o netto. Il termine indica una **popolazione** definita da soglie istituzionali, non la media delle preferenze, e dialoga con il terzo settore dei *commons* proposto da Sanchez (2020) senza essergli attribuito.

Evitare: "secondo Sanchez la pancia della gaussiana..."; "la maggioranza dei milanesi"; "media ± deviazione standard".

## 7. Prossimi passi
- Asse B/C: cercare ISEE aggregati INPS per Milano o microdato IT-SILC/IBF (Lombardia) per passare a **famiglie** e **reddito residuo**.
- Canoni OMI per zona e per m² (banca dati quotazioni, semestre 2025-2) → soglia S2b per NIL e per dimensione del nucleo.
- Scaricare i bandi ALER "fascia grigia" e i requisiti del Piano Casa del Comune (fonte primaria).
- Verificare il volume di Sanchez (introduzione, capp. 1 e 3) e correggere la scheda 11 §5.

## Fonti scaricate/consultate in questa sessione
- MEF-DF, IRPEF su base comunale CSV a.i. 2024: https://www1.finanze.gov.it/finanze/analisi_stat/public/v_4_0_0/contenuti/Redditi_e_principali_variabili_IRPEF_su_base_comunale_CSV_2024.zip [V]
- Regione Lombardia, testo RR 4/2017 con modifiche (I-II adeguamento): https://www.regione.lombardia.it/content/dam/rl/canali-tematici-servizi/08-politiche-sociali/01-abitare-in-lombardia/red-normativa-in-materia-di-servizi-abitativi-pubblici/allegati/Modifiche%20testo%20RR%204-2017-I%20-%20II%20adeguamento.pdf [V]
- Regione Lombardia, allegato DGR XII/5248 del 3/11/2025 (housing sociale, "fascia grigia"): https://www.regione.lombardia.it/content/dam/rl/canali-tematici-servizi/08-politiche-sociali/10-housing-sociale/red-housing-sociale/allegati/All_Delibera%205248%20del%2003_11_2025.pdf [V]
- OMI-AdE, Statistiche trimestrali residenziale IV 2025 (copia): https://www.fimaamilano.it/public/filetiny/Agenzia%20delle%20Entrate/statisticheomi_res_iv_2025.pdf [V]
- DPCM 159/2013 (ISEE), art. 4: https://www.bollettinoadapt.it/wp-content/uploads/2015/12/DPCM_159_2013.pdf [V, versione 2013]
- Sanchez, ACADIA 2018: https://papers.cumincad.org/data/works/att/acadia18_108.pdf [V]; Plethora Project, pagina del libro: https://www.plethora-project.com/architecture-for-the-commons [V]
- Stampa su bandi ALER e Piano Casa (snippet di ricerca, non letti per intero): affaritaliani.it, milanofree.it, quifinanza.it [S]
