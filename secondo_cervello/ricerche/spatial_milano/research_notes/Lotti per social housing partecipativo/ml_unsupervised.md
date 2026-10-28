# Unsupervised ML in urban analytics, geodemographics and housing: fit for a participatory social-housing site-selection platform in Milan

Context assumed: 88 NIL (Nuclei di Identità Locale), ~120k parcels, ~230k building volumes, socio-economic indicators. Research date: October 2026. Tool budget meant several primary texts could only be read at abstract level; these are flagged.

## 1. Geodemographic classifications (OAC, London OAC, US): pipeline, validation, critiques

### Takeaway
The UK OAC tradition is a mature, open, census-only pipeline. It runs variable selection, transformation, standardisation, k-means and hierarchical nesting, then names clusters and writes pen portraits. It is good for describing *types of place*. It is not good for allocating resources to individuals, and it brings known risks: ecological fallacy, MAUP and stigmatising labels. With only 88 NIL, a full OAC-style typology adds little; a parcel/census-section-level typology is more plausible but is descriptive context, not a decision rule.

### Cited Findings
- 2011 OAC is documented in Gale, Singleton, Bates & Longley (2016), JOSIS. It updates the 2001 OAC method using 2011 Census data. Keywords: geodemographics, cluster analysis, k-means. Structure: 8 Supergroups, 26 Groups, 76 Subgroups. — [JOSIS article page](https://josis.org/index.php/josis/article/view/66); [Liverpool repository](https://livrepository.liverpool.ac.uk/3033343/)
- The 2011 OAC methodology was shaped by a reported user engagement exercise. — [JOSIS](https://josis.org/index.php/josis/article/view/66)
- London OAC (Longley & Singleton) reapplied the 2011 OAC method to London-only data. It found 8 Super Groups the most parsimonious, partitioned into 21 Groups, with no merit in further Sub Groups. This shows local reclassification changes the optimal granularity. — [2011 LOAC Report, GLA](https://data.london.gov.uk/download/2k85d/dee3abe9-80a1-452f-83d1-a5f720491fe0/2011%20LOAC%20Report.pdf)
- UNVERIFIED (from memory; I could not extract the PDF text): the 2011 OAC started from ~167 candidate variables and reduced them to 60. It applied an inverse hyperbolic sine transform and range standardisation, then ran k-means many times (order of 10,000 runs) per level, keeping the lowest within-cluster sum of squares. PCA was *not* used to reduce dimensions in the final OAC. Check against the [UCL Discovery PDF](https://discovery.ucl.ac.uk/id/eprint/1498873/1/Longley%20et%20al%20creating%20the%202011%20area%20classification%20for%20output%20areas%2015062016.pdf).
- US: Spielman & Singleton (2015, Annals AAG) built an open geodemographic typology of all US census tracts. They argue that ACS tract estimates have large margins of error, but errors largely cancel when tracts are treated as multivariate profiles. The typology was grounded in concepts, domains and measures, and validated against Chicago city data and FEC data. — [IDEAS/RePEc](https://ideas.repec.org/a/taf/raagxx/v105y2015i5p1003-1025.html); [openICPSR data/code](https://www.openicpsr.org/openicpsr/project/100235/version/V5/view)
- Self-organising maps as geodemographic engine: Spielman & Thill (2008, CEUS) applied a Kohonen SOM to 79 attributes for NYC census tracts. They linked a "social space" map to a geographic map, and argued that typical social-area class labels can obscure complexity. — [Springer-linked record / IJHG listing](https://www.sciweavers.org/node/280129) (abstract-level only)
- Practical pipeline guidance (Rey, Arribas-Bel & Wolf, *Geographic Data Science with Python*): standardise first (robust_scale or z-scores); transform (log/Box-Cox) before scaling. k-means and Ward give unconstrained clusters; Ward with a connectivity matrix gives regions. CH scores: k-means 106.9, Ward 98.5, queen-constrained 62.5, KNN-constrained 54.4. Profile clusters on *unscaled* means plus per-cluster distributions. Labels are nominal. The book gives no automatic rule for k. — [GDS book ch. on clustering](https://geographicdata.science/book/notebooks/10_clustering_and_regionalization.html)
- Ecological fallacy critique: geodemographics assumes members of a group are alike. Areas assigned to a cluster need not be similar, and households within an area need not be homogeneous. — [Springer, Population Research and Policy Review, s11113-007-9042-9](https://springerlink.bibliotecabuap.elogim.com/doi/10.1007/s11113-007-9042-9) (via search summary; full text not read)
- Critiques of geodemographics have been grouped as representational (Goss 1995), discriminatory (Burrows et al. 2005; Graham 2005) and intrusive (Monmonier 2002; Curry 1998). — same source as above (search summary)
- Burrows & Gane (2006, *Sociology* 40(5)) argue that geodemographic classifications embedded in software sorting make "automated spatiality" part of how social class is constituted. — [White Rose eprints](https://eprints.whiterose.ac.uk/7517); [ANU portal](https://researchportalplus.anu.edu.au/en/publications/geodemographics-software-and-class/)
- MAUP: results depend on the scale and zoning of areal units. First identified by Gehlke & Biehl (1934); systematised by Openshaw (1984), CATMOG 38. It has a scale component and a zoning component. — [Wikipedia: MAUP](https://en.wikipedia.org/wiki/Modifiable_areal_unit_problem) (secondary; cite Openshaw 1984 directly in the report)

### Inferences
- For 88 NIL, k-means with k of 5 to 8 gives clusters of ~10 to 18 units. Stability across seeds and k will be fragile, and statistical gain over simply reading a ranked indicator table is small.
- The sensible geodemographic unit in Milan is the ISTAT census section (sezione di censimento). The NIL is too coarse, and parcels/buildings carry no census attributes. A typology there could be aggregated *up* to NIL and *joined down* to parcels as context.
- Cluster names (pen portraits) are the most dangerous output in a participatory, public-facing setting. A label like "struggling estates" attached to a NIL where social housing is being sited invites stigma and NIMBY framing. Prefer neutral, descriptive, variable-based labels, or show profiles without names.
- Validation should include: stability across seeds and bootstraps (e.g. adjusted Rand), silhouette/CH, external validation against variables not used in clustering, and local stakeholder review of whether the types "make sense". Only the last is in the OAC user-engagement spirit.

### Gaps
- Exact 2011 OAC variable counts, transformations and run counts not verified from full text (PDF extraction failed). Also not verified: the 2021 OAC update (Wyszomierski, Longley, Singleton et al.).
- No Milan-specific geodemographic classification of the 88 NIL found. ISTAT's 2024 Milan deep-dive for the parliamentary inquiry on peripheries uses the 88 NIL to compare socio-economic conditions and spot disadvantaged areas. It is not a cluster study. — [ISTAT Approfondimento Milano](https://www.istat.it/wp-content/uploads/2024/06/Approfondimento_Milano.pdf). The municipal PGT NIL fact sheets give per-NIL indicators. — [PGT NIL schede 1–15](https://www.pgt.comune.milano.it/pgt_file_download/b!88kfkdym6ka1FQJ8CP8l_1ken78aR3NJkcxoQgfR2kK4M-X2Jz8iSJx6ToAzeiZ_/01IBPLUZSH6ZAWIO5PSVAYZTIM3OJIUMVK/02PS_NIL_Schede_01_15_20190305.pdf)
- Singleton & Spielman (2014, *Professional Geographer*) and the Longley et al. GIS textbook were not opened.

## 2. PCA for composite indices (deprivation, housing vulnerability, SoVI) vs expert/participatory weighting

### Takeaway
PCA-derived weights reflect *variance structure*, not *importance*. For a normative choice ("where should social housing go, and for whom?") they are the wrong default. The best evidence is SoVI: it is PCA-based, and it proved internally inconsistent and sometimes moved against theory. Major official deprivation indices use expert or consultative *domain* weights, and use factor analysis only *within* domains. Recommendation: use PCA as a diagnostic (redundancy, correlation structure) and let participants set weights, with sensitivity analysis shown.

### Cited Findings
- Spielman et al. (2020, *Natural Hazards* 100:417–436): multiple SoVI computations for the same place with the same data can give strikingly different results. Increases in vulnerability-raising variables (e.g. unemployment) often *decrease* measured SoVI. The authors caution against using SoVI in policy. Code is open (geoss/sovi-validity). — [USGS record](https://pubs.usgs.gov/publication/70208758); [Springer PDF](https://link.springer.com/content/pdf/10.1007/s11069-019-03820-z.pdf); [ORNL](https://impact.ornl.gov/en/publications/evaluating-social-vulnerability-indicators-criteria-and-their-app/)
- Tate (2012, *Natural Hazards* 63:325–347): deductive index ranks are most sensitive to transformation choice. Hierarchical ranks are most sensitive to weighting scheme. Inductive (PCA-type, SoVI-like) ranks are most sensitive to indicator set and analysis scale. — [EconPapers](https://econpapers.repec.org/RePEc:spr:nathaz:v:63:y:2012:i:2:p:325-347)
- Tate (2013) Monte Carlo uncertainty analysis of a hierarchical SoVI: high-magnitude uncertainty in rankings. Precision decreases as vulnerability increases, so the places that matter most are ranked least reliably. — [Princeton collaborate](https://collaborate.princeton.edu/en/publications/uncertainty-analysis-for-a-social-vulnerability-index/)
- English IMD: domain weights rest on expert judgement and consultation. Factor analysis weights indicators *within* some domains; others use equal-weighted standardised indicators. Domain scores are exponentially transformed, then combined by the set weights. — [IoD2019 Technical Report](https://assets.publishing.service.gov.uk/media/5d8b387740f0b609909b5908/IoD2019_Technical_Report.pdf); [IoD2015 Technical Report](https://assets.publishing.service.gov.uk/government/uploads/system/uploads/attachment_data/file/464485/English_Indices_of_Deprivation_2015_-_Technical-Report.pdf)
- A preference-based test of IMD domain weights found them broadly similar to the expert weights, but suggested changing two. — [Napier repository](https://napier-repository.worktribe.com/OutputFile/1354729) (search summary only)
- Scottish SIMD: fixed domain weights from original Oxford research; factor analysis creates within-domain indicator weights. — [SIMD technical notes (archived)](https://nrs.preservation.mirrorweb.com/public/20190115070953mp_/https://www2.gov.scot/Resource/0050/00504773.pdf)
- OECD/JRC Handbook on Constructing Composite Indicators (2008) splits weighting into *statistical* methods (PCA/factor analysis, Benefit-of-the-Doubt, unobserved components) and *participatory* methods (budget allocation by experts or public, AHP, conjoint analysis). — [JRC handbook PDF](https://knowledge4policy.ec.europa.eu/sites/default/files/jrc47008_handbook_final.pdf); [OECD page](https://www.oecd.org/en/publications/handbook-on-constructing-composite-indicators_533411815016.html) (taxonomy via secondary citation; chapter text not read)

### Inferences
- PCA weights are only as defensible as the claim "the dominant axis of covariance = what we care about". For site selection, covariance among indicators (e.g. foreign-born share with low income) does not equal a policy priority. Using it can import bias silently.
- PCA sign and rotation are arbitrary. Components change with the indicator set and with the 88-unit sample. This mirrors Tate's finding that inductive indices are most sensitive to indicator set and scale.
- Good use of PCA here: detect redundant indicators before participants weight them, avoiding double-counting; and show a 2-D biplot as a teaching aid.
- Participatory budget allocation (e.g. "distribute 100 points") or AHP fits the platform. Report rank sensitivity, e.g. Monte Carlo over plausible weights à la Tate, so users see which NIL/parcels are robustly high and which flip.

### Gaps
- Current IoD2025 English weights not checked.
- No Italian/Milan housing-vulnerability index with PCA weights examined. The ISTAT Indice di Vulnerabilità Sociale e Materiale (IVSM) would be the natural comparator but was not researched here.

## 3. t-SNE and UMAP: what they are for, and risks of over-reading

### Takeaway
Both are non-linear embeddings for *visual exploration*. Cluster sizes and inter-cluster distances in t-SNE are not interpretable. Random data can produce apparent clusters, and results vary with perplexity and seed. UMAP claims better global structure, but this is partial and disputed. In a participatory platform with 88 NIL they add little and risk misleading lay users. At most, offer them as an internal analyst tool for exploring parcel/building feature space.

### Cited Findings
- Wattenberg, Viégas & Johnson (2016, Distill) say perplexity balances local vs global structure, with a typical range of 5 to 50, and several values should be compared. Perplexity must be lower than the number of points. — [Distill: How to Use t-SNE Effectively](https://distill.pub/2016/misread-tsne/)
- Same source: t-SNE expands dense clusters and contracts sparse ones, so "you cannot see relative sizes of clusters in a t-SNE plot." Distances between well-separated clusters "may mean nothing." — [Distill](https://distill.pub/2016/misread-tsne/)
- Same source: random Gaussian noise can show clumps at low perplexity. Runs should continue to convergence, and results can differ across runs. — [Distill](https://distill.pub/2016/misread-tsne/)
- McInnes, Healy & Melville (2018): UMAP is competitive with t-SNE for visualisation and "arguably preserves more of the global structure", with better run time. The umap-learn README says it preserves "some aspects" of global structure and pairs with HDBSCAN "only with a little care". — [arXiv 1802.03426](https://arxiv.org/pdf/1802.03426v3.pdf); [umap GitHub](https://github.com/ml-lab/umap)
- Chari & Pachter (2023, *PLOS Comput Biol*), "The specious art of single-cell genomics": 2-D t-SNE/UMAP embeddings distort high-dimensional structure badly. They are counterproductive for exploratory analysis; an autoencoder can force data into an arbitrary shape (an elephant). — [PMC10434946](https://pmc.ncbi.nlm.nih.gov/articles/PMC10434946)
- Rebuttal: Lause, Berens & Kobak (2024, *PLOS Comput Biol*). They agree distances are distorted, but show the embeddings preserve local neighbourhoods and cell types, and that the critique used inadequate quality metrics. — [PMC11446450](https://pmc.ncbi.nlm.nih.gov/articles/PMC11446450)

### Inferences
- The consensus across both sides: *local neighbourhoods* are roughly kept; *global distances, cluster sizes, densities and gaps* are not reliable. In a public tool, a lay user will read "far apart on the map = very different", and that reading is wrong.
- Running clustering on UMAP coordinates (UMAP→HDBSCAN) adds hyperparameter-dependent structure. Cluster in the original standardised space, or on PCA scores, and use UMAP only to *display* the clusters.
- If shown at all, show it with captions ("positions approximate; distances not meaningful"). Link it to the real map so users can check against geography.

### Gaps
- No urban-studies paper found that systematically evaluates t-SNE/UMAP misreading in planning contexts. Urban applications exist (e.g. street-view or POI embeddings), but none were reviewed here. Flag as a literature gap.

## 4. Spatially constrained clustering / regionalisation and spatial autocorrelation for housing-stress hotspots

### Takeaway
Regionalisation (SKATER, REDCAP, max-p, AZP, Ward with connectivity) builds contiguous, homogeneous zones. It trades statistical fit for geographic coherence, and max-p can enforce a minimum size (e.g. households). Global Moran's I and LISA detect clustering and hot/cold spots, but need permutation inference and multiple-testing correction. For Milan, these are best applied *below* NIL level (census sections or grid cells) to find intra-NIL housing-stress pockets the NIL boundaries hide (a MAUP response).

### Cited Findings
- PySAL spopt offers max-p, AZP, SA3, SKATER, Ward (spatially constrained), Region-k-means and Random Regions. — [PySAL spopt](https://pysal.org/spopt/). REDCAP is not listed there; it is available in GeoDa/rgeoda/pygeoda. — [rgeoda redcap](https://rdrr.io/cran/rgeoda/man/redcap.html)
- SKATER prunes a minimum spanning tree built on contiguity. First-order REDCAP with single linkage equals SKATER; full-order REDCAP variants update contiguity as clusters merge. REDCAP is from Guo (2008). — [Anselin, intro book vol. 2, REDCAP](https://lanselin.github.io/introbook_vol2/redcap.html); [GeoDa workbook](https://geodacenter.github.io/workbook/9c_spatial3/lab9c.html)
- GeoDa worked example: BSS/TSS 0.4627 for REDCAP vs 0.4325 for SKATER vs 0.4641 for SCHC (spatially constrained hierarchical). Largest cluster 107 obs (SKATER) vs 77 (REDCAP). Methods differ materially in region sizes. — [GeoDa workbook lab 9c](https://geodacenter.github.io/workbook/9c_spatial3/lab9c.html)
- Few comparative studies of regionalisation methods exist. A 2022 preprint compares Agglomerative, SKATER, REDCAP, AZP and max-p on social-determinants-of-health data; Aydin et al. (2021, IJGIS) give a quantitative comparison. — [arXiv 2209.11836](https://arxiv.org/abs/2209.11836v1) (abstract only)
- Max-p (Duque, Anselin & Rey 2012, *J. Regional Science* 52(3)) finds the maximum number of homogeneous regions such that each region's spatially extensive attribute (e.g. households, population) exceeds a threshold. The number of regions is endogenous; there is no compactness constraint. — [ASU record](https://asu.elsevierpure.com/en/publications/the-max-p-regions-problem/); [spopt R docs](https://rdrr.io/cran/spopt/man/max_p_regions.html)
- Regionalisation lowers fit (CH) versus unconstrained clustering but yields much more compact regions (higher isoperimetric quotient). The trade-off cannot be removed. — [GDS book](https://geographicdata.science/book/notebooks/10_clustering_and_regionalization.html)
- LISA: each location is tested, so at α=0.05 ~5% of locations look significant by chance. Bonferroni is conservative; FDR is more flexible. — [PySAL esda local Moran guide](https://pysal.org/esda/stable/user-guide/local_spatial_autocorrelation.html)
- Conditional permutation inference is safer than the analytic approximation for skewed variables. Run global Moran's I first. Isolated significant units may be false positives. — [MetricGate docs](https://metricgate.com/docs/anselin-local-moran-spdep/) (commercial documentation; lower authority, consistent with PySAL)

### Inferences
- With 88 NIL, LISA has low power, and the queen-contiguity neighbour count is small. Results will be unstable and dominated by edge effects (city boundary). Run LISA on census sections or a 250 m grid aggregated from parcels/buildings. Display NIL as context overlays only.
- Max-p with a minimum-households threshold is the most policy-relevant regionalisation. It can produce "housing-need zones" with statistically meaningful populations that cut across NIL. Participants can then discuss zones rather than arbitrary administrative units.
- Hotspot maps carry the same stigmatisation risk as cluster labels. Frame them as "where need is concentrated", not as "problem areas".
- Regionalisation is unstable to weights matrix choice and variable set. Show two or three variants, or a co-assignment frequency map, rather than one "true" regionalisation.

### Gaps
- Aydin et al. (2021) results not read. No Milan-specific LISA/regionalisation study of housing stress found in this pass.

## 5. Clustering for household archetypes (personas) and latent class analysis

### Takeaway
LCA (model-based, probabilistic, works on categorical survey indicators, gives fit indices such as BIC) has become the standard way to derive housing-situation typologies from household microdata. k-means/GMM are alternatives for continuous variables. Archetypes are useful as *communication devices* in a participatory platform ("a single parent on €18k renting privately") when grounded in microdata. Treat them as illustrative, not as eligibility categories.

### Cited Findings
- English Housing Survey 2019-20 segmentation of private renters: 6 latent classes based on financial and family circumstances (DLUHC, 2022). This is a direct governmental precedent for household archetypes in housing policy. — [GOV.UK EHS segmentation](https://gov.uk/government/publications/english-housing-survey-a-segmentation-analysis-of-private-renters/english-housing-survey-a-segmentation-analysis-of-private-renters)
- EU-SILC 2010–2023 LCA identified three "degrees" of housing precariousness: quality, cost and security. Precariousness is more common in Southern and Eastern Europe, and equally severe in the reduced-rent sector. Directly relevant to Italy. — [Tilburg University record](https://research.tilburguniversity.edu/en/publications/degrees-of-housing-precariousness-a-latent-class-analysis-of-hous/) (abstract-level)
- LCA on 4,355 Australian children using nine binary housing indicators (tenure, condition, affordability, stability, crowding, etc.) produced housing typologies linked to health. — [J Urban Health 2024](https://link.springer.com/article/10.1007/s11524-024-00925-0) (abstract-level)
- US mothers with children: LCA found four housing-insecurity subgroups ("Stable", "Unstable", "Rent-Focused", "Strategic Bill-Paying"). — [PLoS ONE 2024 via DOAJ](https://doaj.org/article/feff365735d949a3ac534ca7e6701c48) (abstract-level)

### Inferences
- For Milan, the natural data are EU-SILC (Italy) or ISTAT household surveys, plus municipal ERP/SAP waiting-list data if available, not the parcel/NIL dataset. Archetypes are a *demand-side* layer; site selection is *supply-side*. The platform should keep them conceptually separate and link them only via matching (which sites suit which archetype: accessibility, services, unit sizes).
- Persona design: derive from LCA classes, report class size and uncertainty, and use neutral names. Validate with housing associations or tenant unions, so personas are not built from the analyst's assumptions.
- Do not let archetype membership drive allocation. That reintroduces the ecological fallacy at household level, and it may conflict with legal allocation criteria (Lombardy regional rules for SAP; not researched here).

### Gaps
- No Italian/Milan LCA of housing need was found in this pass. Lombardy SAP allocation rules and Milan waiting-list microdata availability were not researched.

## 6. Explainability, communicating ML to non-experts, and the proper role of ML vs value judgements

### Takeaway
The literature converges on a division of labour. Computation describes, structures and tests robustness; weighting and trade-offs are value judgements for people. For a participatory site-selection platform: transparent indicators plus participant-set weights (MCDA), with ML in a supporting role (redundancy checks, typologies as context, hotspot detection, sensitivity/uncertainty display). ML should not produce a black-box "best site".

### Cited Findings
- Malczewski (2006), as cited in a spatial MCDA review: GIS analyses and visualises spatial data, while MCDA structures the decision problem and evaluates alternatives. — [Korea Science SMCDA review PDF](https://koreascience.or.kr/article/JAKO202108455995290.pdf) (secondary citation)
- GIS-MCDA weights are mostly expert-elicited, adding subjectivity (Veronesi et al. 2017). — [Harper Adams repository](https://hau.repository.guildhe.ac.uk/17282/1/Fabio%20Veronesi%20Automatic%20selection%20upload.pdf)
- Spatially explicit weight-sensitivity analysis can reveal how robust each stakeholder's evaluation is, and where sensitivity concentrates geographically. — [Springer chapter 978-3-540-74757-4_3](https://link.springer.com/chapter/10.1007/978-3-540-74757-4_3) (abstract-level)
- Marttunen et al. describe five approaches to eliciting stakeholder criteria weights, from expert-driven to personal interviews. — [VTT record](https://cris.vtt.fi/en/publications/how-to-design-and-realize-participation-of-stakeholders-in-mcda-p/)
- Boroushaki & Malczewski (2010) built web-based collaborative GIS-MCDA and consensus measurement. These are relevant precedents for a participatory platform (citation only; content not read). — via [Korea Science review](https://koreascience.or.kr/article/JAKO202108455995290.pdf)
- SoVI's documented instability is a cautionary tale: data-driven indices handed to policy without uncertainty communication. — [Spielman et al. 2020, USGS](https://pubs.usgs.gov/publication/70208758)
- Spielman & Thill note that class labels can obscure complexity, which argues for showing profiles and distributions, not just names. — [record](https://www.sciweavers.org/node/280129)

### Inferences
Verdict per method, for this platform:

- **PCA**: YES as a diagnostic (indicator redundancy, biplot teaching aid). NO as the source of decision weights.
- **k-means / hierarchical (Ward)**: Limited at NIL level (n=88). Useful on census sections or parcels/buildings for *descriptive* typologies, e.g. building-stock types from volume, age and use. Report stability. Use neutral labels.
- **GMM**: Useful where soft membership matters (parcels in transition, mixed areas). Gives probabilities that can be shown as uncertainty. BIC for k is helpful.
- **SOM**: Historically used in geodemographics (Spielman & Thill 2008). The linked "attribute map + geographic map" view is pedagogically nice. Lay users need guidance. Optional.
- **t-SNE / UMAP**: Analyst-only exploration of high-dimensional parcel features. Do not expose them as decision visuals; if shown, add strong caveats.
- **SKATER / REDCAP / max-p**: YES at sub-NIL scale. Max-p with a household floor is best for defining "need zones" that are statistically robust and policy-meaningful. Show variants.
- **Moran's I / LISA**: YES for hotspot detection at fine scale, with permutation inference and FDR. At NIL level, indicative only.
- **LCA**: YES for household archetypes from survey microdata (EU-SILC/ISTAT). Use as communication personas and for needs-to-site matching, not as eligibility criteria.

Communication principles (derived from the cited material):
1. Show raw indicators and their maps first, ML outputs second.
2. Let people set weights, and show rank sensitivity bands, not single ranks.
3. Avoid evocative cluster names.
4. Display uncertainty (cluster membership probability, LISA significance, regionalisation co-assignment).
5. Document the pipeline openly, as the OAC and Spielman–Singleton projects do.

### Gaps
- No empirical study was found that tests how lay participants interpret cluster maps, t-SNE/UMAP plots or LISA maps in planning workshops. This is a real evidence gap; the report should flag it rather than assert effects.
- Explainable-AI (XAI) methods such as SHAP mostly concern supervised models. They were not researched here, as out of scope for unsupervised methods.
- Not verified: specific Italian participatory GIS-MCDA social-housing precedents.
