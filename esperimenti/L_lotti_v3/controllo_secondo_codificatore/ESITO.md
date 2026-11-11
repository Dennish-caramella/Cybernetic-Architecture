# Accordo tra codificatori — Base L v3

Calcolato dal coordinatore l'11/11/2026 con `accordo.py` (risultati in `accordo.json`).

- **Procedura.** Il secondo codificatore è stato diviso in due agenti (A: C001–C100, B: C101–C200). Lavoravano in cartelle isolate con solo le immagini e le istruzioni, senza accesso al progetto, al campione o alla chiave. Gli hash dei fogli sono stati registrati prima del confronto: A `1ca0df73…`, B `88b6daca…`, foglio unito `3095055d…` (`codifica_secondo.sha256`) [V].
- **Accordo sulla codifica binaria** (libera o dismessa = L, C, D): 0,90; kappa di Cohen 0,785 [V].
- **Accordo sulle 7 categorie di Q1**: 0,835; kappa 0,768 [V]. Le discordanze principali sono V↔L (verde curato o incolto), I↔L e I↔U (binari, piazzali) [V, matrice in `accordo.json`]. Per convenzione un kappa tra 0,61 e 0,80 si considera un accordo "sostanziale" (Landis e Koch, 1977) [S, convenzione da verificare sul testo].
- **C5a ricalcolato** su 100 lotti, soglia 0,70:

  | Codifica | Valore | IC Wilson 95% |
  |---|---|---|
  | primo codificatore (esecutore) | 0,58 | [0,482; 0,672] |
  | secondo codificatore (cieco) | 0,65 | [0,553; 0,736] |
  | entrambi d'accordo sul sì | 0,55 | [0,452; 0,644] |

- **Base (100 particelle qualsiasi)**: primo 0,11, secondo 0,12 [0,070; 0,198].
- **Per origine** (secondo codificatore): AT 0,41 [0,22; 0,64]; DUSAF 13 0,73 [0,54; 0,86]; terreno comunale confermato 6/6.

**Lettura.** Il giudizio sulle immagini è affidabile: due codificatori indipendenti concordano sul 90% dei casi. L'esito di C5a non cambia: con nessuna delle due codifiche la stima raggiunge 0,70. Il punto debole resta l'ingresso degli ambiti di trasformazione (AT) ancora in uso.
