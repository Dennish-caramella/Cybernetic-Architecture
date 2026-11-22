# Base L v7 — congelata il 2026-11-22

Ticket #40. Una correzione è una nuova versione con un nuovo ticket (PROTOCOLLO_LABORATORIO.md).

**Stato**: congelata **per decisione di Dennis** (`tesi/DECISIONI.md`, 22/11). Per la regola pre-registrata C1–C4, C6 e C8 passano; **C5 è inconcludente** (controllo umano 0,737; C5a dei modelli 0,722 ma con codificatore 1 sostituito, vedi REVISIONE.md). Non è un "passa" misurato.

**Contenuto** (hash di contenuto `49327c8a864d…`, identico in tutte le esecuzioni; l'hash del file .gpkg cambia a ogni scrittura anche a contenuto uguale: vale quello di contenuto):
- 216 lotti edificabili, 167 lotti da riusare, 268 aree di attivazione; 50 lotti GFU (classe separata); tessuto consolidato 0.
- Capacità edificabili (alloggi, FAR 0,5 / 1 / 2): 16.389 / 32.885 / 65.885; scenari con le GFU in `tabelle/scenari_capacita.csv` (a FAR 1: 40.608 senza Bovisa, 45.683 con Bovisa). Usare la forbice, non un valore unico.

**File e SHA-256 (al momento del congelamento)**
- 5d464a3c9b3ac195c8f6a3146cff1a5619445a71250c2a9d9f11ab53768d22ac  lotti_v7.gpkg
- a3129b5aa63aea217dd5f5994f7ebe0ba87d29909dac7450e24d8d0ae6cf90ea  run.py
- fcad5213d9bf8681b78d6a29d9bfa411caa94742096f0d354c5956d45a2ba09a  test_lotti.py
- ea9d6fda23f2f21c5310a009db9a91eb891a89d1441bab1b91190610ec5692cf  chiavi/campione_chiave_v7.csv
- 7f1950267b93529e775861ee3df3a97302fd5b4cf80a468395711d333a73b3b4  esito_criteri.json
- 998bf5d35b92f9b54c4093bc0ca92c04b3f6ece2ef1dbc4d966fba87779d7f97  tabelle/scenari_capacita.csv
- 64c3a355781e42c66410a54e58f2ebad595ac91b937d59a61495e0eef3655b7c  controllo_umano/codifica_umana.csv
- 0446b8bc921a9959004af87ab001b2b8711c86ce59fe952f3c1ac2145f37e222  controllo_umano/chiave_umano.csv
- 7f98ab3197ef716ade8af8f4b86e70822226b898d555a28fe834e83b7fa2677b  esecuzioni/00_preregistrazione.txt
- 97e3d908999ff7bbf83da1f26d06ee6e5c874566caf88ad5545e49a341fbf42e  controllo_umano/PREREG_controllo_umano.txt

**Limiti da portare nelle prove successive**
- Validazione: modelli linguistici (Opus al posto di Fable nel codificatore 1, deviazione registrata) e un solo codificatore umano su 60 lotti; fuori ambito e piani attuativi reggono (0,72–0,82), AdP (0,49) e riuso (0,55–0,59) sono deboli.
- Le aree di attivazione piccole o verdi sono spesso non giudicabili da foto.
- Non fatti: maschera dei corpi idrici (es. E00170, lago su oltre metà), due scenari di capacità (cantiere v6 e formulazione superata) in `scenari_capacita.csv`, riproducibilità da zero senza cache.
- GFU: perimetri 2012 sostitutivi [H], destinazioni non verificate [L].
- Banco, Base P/E e A1–A4 devono dichiarare la capacità come forbice e non mostrare le GFU come edificabili validate.
