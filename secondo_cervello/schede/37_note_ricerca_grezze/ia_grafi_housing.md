# AI-augmented urban planning: methods that complement or challenge Azadi's "Augmented Urban Planning" (graphs, KG, LLM, multi-agent, geospatial, housing site selection)

Verification legend: [V] = page opened and read via fetch; [U] = seen only in search-result titles/snippets or not retrievable, NOT verified. Fetch summaries came from a small model; numbers are as reported by the fetched page and should be re-checked against the PDF before quoting in a thesis.

## 0. Anchor: Azadi's framework (what the others are compared to)

### Takeaway
Azadi's PhD thesis (TU Eindhoven) proposes Augmented Urban Planning (AUP) with a Dynamic Knowledge Graph recording participation, an FMU Ontology and an open-source toolbox. It is the graph/semantic baseline.

### Cited Findings
- [V] Title "Augmented Urban Planning: A Systematic Framework for Sociotechnical Integration of Digital Representations in Urban Planning", author Shervin Azadi, PhD thesis, Built Environment, TU/e, page dated 23 Sept 2026, ISBN 978-90-386-6790-4; page notes an embargo with open-access PDF from 23 Sept 2027; no DOI on page — [TU/e research portal](https://research.tue.nl/en/publications/augmented-urban-planning-a-systematic-framework-for-sociotechnica/)
- [V] Per the page: argues Urban Digital Twins fall short on social, dynamic, value-laden aspects; AUP has three dimensions (interdisciplinary integration, consensual contextualization, procedural operationalization); treats digital twins as evolving collections of data and models; introduces the FMU Ontology linking planning processes to digital representations; a participatory approach "UDTing" tested in a workshop series; participation data recorded as a Dynamic Knowledge Graph and analysed with graph-based metrics; open-source toolbox — same source.

### Inferences
- Because the full text is embargoed, only the abstract is checkable. Any claim about FMU details beyond the abstract must wait.

### Gaps
- Full thesis text not accessible; no DOI.

## 1. AI/LLMs in participatory planning and public deliberation (2020-2026)

### Takeaway
Evidence exists that LLM mediation can raise agreement in online deliberation (Habermas Machine), and LLM-agent simulations of planners/residents exist for land-use planning, but critiques stress that simulated or machine-mediated deliberation is thin and not validated with real residents.

### Cited Findings
- [V] Habermas Machine: Tessler, Bakker, Jarrett, Sheahan, Chadwick, Koster, Evans, Campbell-Gillingham, Collins, Parkes, Botvinick, Summerfield, "AI can help humans find common ground in democratic deliberation", Science 2024. Reported: 5,734 participants (mostly UK, crowdsourced) plus a 200-person representative virtual citizens' assembly; AI statements preferred over human mediators' ~56% of the time; agreement up ~6-9 percentage points; viewing opinions without AI mediation produced no change; revised statements gave minority views weight 0.36 vs 0.29 share — via PDF mirror [rivista.ai copy of paper](https://www.rivista.ai/wp-content/uploads/2024/10/science.adq2852.pdf) (mirror, not the publisher page; science.org fetch failed). DOI 10.1126/science.adq2852 inferred from the URL I tried, which I could not open at the publisher — treat DOI as [U].
- [V] Critique of Habermas Machine (Sætra, CACM blog): "deliberation" mislabelled for isolated machine-mediated interaction; study did not measure trust, empathy, mutual respect; risk of "illusion of consensus"; perceived AI neutrality may reduce critical engagement — [CACM blog](https://cacm.acm.org/blogcacm/computation-and-deliberation-the-ghost-in-the-habermas-machine) (fetch gave author as "Sætra" only; first name/affiliation not verified).
- [V] LLM-agent participatory planning: Zhou, Jin, Lin, Li (Tsinghua), "Large Language Model for Participatory Urban Planning" — GPT-4V planner and ~1,000 GPT-3.5 resident agents per region built from census profiles, fishbowl discussion; tested in two Beijing regions; reported best on Satisfaction/Inclusion; limitations: omits land ownership, development cost, higher-level policy; needs are self-reported by LLM agents, so metrics measure fit to simulated needs, not real residents — [arXiv 2402.17161](https://arxiv.org/pdf/2402.17161)
- [V] LLM + chatbot participation platform concept: Zali, Baba ahmadi, Argany, Mostafavi, "Leveraging Large Language Models for Automated Assessment and Mapping in Participatory Urban Planning" (ISPRS Archives XLIX-B4-2026) — extracts location/issue/intensity from citizen text; prototype fine-tuned on ~2,000 Montreal transit tweets; no quantitative evaluation reported — [ISPRS PDF](https://isprs-archives.copernicus.org/articles/XLIX-B4-2026/671/2026/isprs-archives-XLIX-B4-2026-671-2026.pdf)
- [V] Empirical critique of LLM deliberation: Flechtner (Zurich/ETH), "The Deliberative Deficit", arXiv 2608.10186: 1,980 five-agent LLM runs, 12 citizen-assembly topics, 11 model configurations; LLM groups start with ~1/3 of human perspective diversity; DRI gains ~30% of human reference, negative on ethically contested topics; conclusion: tools yes, autonomous deliberative agents no. Preprint, not peer reviewed — [arXiv](https://arxiv.org/pdf/2608.10186)
- [V] Polis/vTaiwan: Roy, Lessig, Tang "Conversation Networks" (Feb 2025) describe Polis as an AI-supported deliberation tool, vTaiwan as "the first large-scale deployment of Polis", with bridging statements; proposes linking recorded facilitated conversations to Polis — [arXiv 2503.11714](https://arxiv.org/pdf/2503.11714). Note this is a proposal/position paper, not an evaluation of Polis outcomes.
- [U] A systematic review "Large Language Models in Urban Planning: A Systematic Review and Conceptual Framework" appears in search results — [record](https://produccioncientifica.usal.es/documentos/692222a4621d0957276de590) — not opened; authors and findings unknown.

### Inferences
- For a housing thesis, Zhou et al. is the closest precedent to "a model that stands in for residents' needs", and its own limitation (needs are LLM-generated) is exactly the legitimacy gap the PhD brief wants to close with real preference data.
- Habermas Machine addresses statement synthesis, not spatial choice; applying it to "which lot do residents prefer" is a design extension, not an existing result.

### Gaps
- Decidim: no source opened. Habermas Machine publisher page not opened. No peer-reviewed evaluation found of LLM summarisation in real municipal planning consultations. Agent-based stakeholder simulation literature beyond Zhou et al. not covered.

## 2. Knowledge graphs, GNNs, accessibility/MCDA for locating social housing

### Takeaway
GNNs on urban data exist but the opened example infers land use from mobility rather than selecting housing sites; GIS-MCDA for housing siting is an established older practice, but I opened none of the sources, so it remains unverified here.

### Cited Findings
- [V] Imperial College heterogeneous GNN for land-use inference: Zhai et al., arXiv 2406.13724 — London tube/bus/bike ridership + OSM/TfL networks, heterogeneous graph transformer beat GCN/GraphSAGE/GAT/RGCN baselines on six land-use indicators, with feature attribution and counterfactual explanations — [arXiv](https://arxiv.org/pdf/2406.13724)
- [U] Search hits only (not opened): GIS site selection for mass housing ([ResearchGate PDF](https://researchgate.net/profile/M-Taner-Senguen/publication/369539142_Geographic_Criteria_that_should_be_Employed_in_the_Site_Selection_and_Planning_for_Mass_Housing_Areas_with_the_Use_of_GIS/links/6420a98492cfd54f842fde44/Geographic-Criteria-that-should-be-Employed-in-the-Site-Selection-and-Planning-for-Mass-Housing-Areas-with-the-Use-of-GIS.pdf)); FIG 2006 paper by Alshalabi et al. ([PDF](https://fig.net/resources/proceedings/fig_proceedings/fig2006/papers/ts72/ts72_05_alshalabi_etal%20_0702.pdf)); a "Graph Neural Networks in Urban Intelligence" record ([HIT](https://scholar.hit.edu.cn/en/publications/graph-neural-networks-in-urban-intelligence/)).

### Inferences
- A defensible pipeline would be GIS-MCDA (transparent weights) as baseline, with learned models as challenger; I have no verified source that GNNs outperform MCDA for housing siting.

### Gaps
- No verified source on knowledge-graph/ontology-based plan evaluation other than Azadi; 15-minute city metrics; GIS-MCDA for brownfield housing. Not found/opened.

## 3. Risks and critique

### Takeaway
Critical urban scholarship shows algorithmic planning tools can present political choices as neutral. Pask/Alexander cybernetic debate on "who writes the objective function" was not found in sources.

### Cited Findings
- [V] Safransky (2020), "Geographies of Algorithmic Violence: Redlining the Smart City", IJURR 44(2); DOI 10.1111/1468-2427.12833 (as reported by fetch): algorithmic tools make decisions look neutral and technical, hiding political choices; case of a proprietary market value assessment in US cities steering investment/disinvestment, argued to risk municipal redlining — [IJURR](https://www.ijurr.org/?p=8344)
- [V] Sætra critique of Habermas Machine (illusion of consensus, trust in neutrality) — see Section 1.
- [V] Zhou et al. and Flechtner: simulated stakeholders/ agents are not validated substitutes for people — see Section 1.
- [U] Maynooth "Decentring" paper (Kitchin) surfaced in search: [MURAL](https://mural.maynoothuniversity.ie/14646/) — not opened.

### Inferences
- The thesis's plan to rank lots with a model whose weights encode "real needs" inherits the objective-function problem: someone chooses the criteria (cost, FAR, accessibility). Making the weights an object of participation is a design response, not something I found published.
- Safransky's market-value-assessment case is a direct analogue of using land cost as a siting criterion.

### Gaps
- No source found linking Pask/Alexander to AI planning objective functions. Solutionism (Morozov) and data justice (Taylor, Dencik) not verified.

## 4. Italian context

### Takeaway
Italian data sources exist but are mostly unverified; OMI price data carry reuse and reliability caveats.

### Cited Findings
- [V] OMI (Agenzia delle Entrate) quotations: semiannual min/max €/m2 per OMI zone and property type; community repo merges files from 1st half 2016; original download requires Fisconline/Entratel registration; citation "Agenzia Entrate - OMI"; the repo says terms are not an open license; zone cartography not bulk-downloadable; ~10% of value records have min/max 0; a 2018 ruling (sentenza n. 3197, as quoted by the repo) says OMI values indicate only rough estimates — [ondata repo](https://github.com/ondata/quotazioni-immobiliari-agenzia-entrate). Secondary source; check Agenzia terms directly.
- [U] Lombardia regeneration: search surfaced L.R. Lombardia 18/2019 ([record](https://legislazionetecnica.it/lt_link/normativa/WExNTFIxODIwMTkjQTM=)), the Regione geoportal technical sheet on "aree della rigenerazione" ([PDF](https://www.geoportale.regione.lombardia.it/documents/10180/0/SchedaTecnica_AreeRigenerazione/82fc39a6-644f-4dcd-bdba-0b0e34e9a198)) and ANCI Lombardia slides — none readable/opened. Contents not verified.

### Inferences
- Lombardia appears to publish regeneration-area geodata; if so it could seed a candidate-lot layer, to be confirmed.

### Gaps
- PGT structure (Documento di Piano / Piano delle Regole / Piano dei Servizi), indice di edificabilità (IF/IT/UF), ERS rules, ISTAT census bases, OSM use, comuni open data: nothing verified.

## 5. Existing tools

### Takeaway
UrbanSim and Envision Tomorrow documentation was verified; Forma partially; CityScope only at a high level; TestFit not checked.

### Cited Findings
- [V] UrbanSim: open-source (Python) microsimulation land-use model; agents include households, firms, developers, parcels; annual steps; discrete choice (multinomial logit); parcel template needs parcel database and development cost data; documented limits include treating regulations as binding, assuming stable behaviour, inability to predict individual large events — [UrbanSim docs](https://cloud.urbansim.com/docs/general/documentation/urbansim.html)
- [V] Envision Tomorrow: open-access scenario planning package by Fregonese Associates, with MRC additions; analysis tools plus scenario sketching; needs ArcGIS 10.4.1; described as CC0 4.0 licensed (as given on the page; license wording unusual, verify) — [URENIO ICOS](https://icos.urenio.org/applications/envision-tomorrow/) (third-party aggregator)
- [V] Autodesk Forma Site Design: cloud site planning tool with 3D massing, a housing tool, sun/daylight/wind/noise/microclimate analyses; "Site Automation" generates layout options; wind and noise rapid analyses use ML predictions (vendor claim) — [Autodesk](https://www.autodesk.com/products/forma-site-design/overview). Does not address affordability or participation in what I read.
- [V] MIT CityScope: concept of shared interactive computation for urban planning; part of City Science; all current development said to be open source; deployments worldwide; page gives no mechanics — [MIT Media Lab](https://www.media.mit.edu/projects/cityscope/overview/)
- [U] TestFit; Urban Analytics Lab: not searched.

### Inferences
- UrbanSim is the strongest existing model for the "developer behaviour" side (what the market builds), which is the dynamic the thesis critiques; it could serve as the baseline against which a needs-driven siting model is contrasted.
- None of the verified tools documents a mechanism for residents' choice among candidate lots to retrain the model; that is the gap the thesis would occupy.

### Gaps
- CityScope technical architecture, TestFit, Urban Analytics Lab, Spacemaker pre-Autodesk history not covered.
