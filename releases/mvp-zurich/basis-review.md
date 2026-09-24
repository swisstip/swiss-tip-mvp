# Basis review of the mvp-zurich release

**Last update:** 18 September 2026

Release `mvp-zurich-2026-09-16-v1`, content digest `a83ca388c2c3252fd5c8158f167497831d46ca88ac4c055fd88aaa08442d0e9b`, 290 facts, 298 excerpts, 44 documents.

What this is: the result of an assistant reading every served excerpt on 16 September 2026 and saying what the excerpt is (an article of an act, an ordinance or a treaty, a directive, an authority's own guidance, a directory entry, a portal summary), who published the page, and which legal norm a guidance excerpt names. It is the review input for [institutions-and-provenance-weights.md](../../docs/architecture/institutions-and-provenance-weights.md); the data it renders lives in `curation.yaml` beside it (the `institutions`, `page_basis` and `ranking_policy` blocks and the `basis` of each citation), from which the build derives the served labels. No person has reviewed these rows.

Reading rules applied: an excerpt is `act`, `ordinance` or `treaty` only when it is the text of the norm (every Fedlex excerpt is; no excerpt of any other page reproduces a norm verbatim). A guidance excerpt that names an article stays `guidance`, and the named norm is recorded under `refers to`. The ch.ch pages are summaries. The `level` of a basis is the level of the body that enacted the norm or wrote the text; the institution's level is the level of the publisher and can differ from it, although on this release it never does.

Release `mvp-zurich-2026-09-17-v2` (content digest `be1dde1a7a2b2228dab715371a75940543abfab1a2c40706eeee6be79b5be974`, 417 facts, 485 excerpts, 90 documents) serves these rows unchanged, adds the 132 excerpts of the daily-life extension (listed at the end under "Daily-life excerpts"), and the 53 excerpts of the Zurich office contacts of release `mvp-zurich-2026-09-17-v1`, whose basis the assistant set when writing the facts on 17 September 2026; they are listed at the end under "Office-contact excerpts" and have not been reviewed either. The summary and institution tables below describe the release of 16 September.

## Summary

| Measure | Value |
| --- | --- |
| Excerpts by basis kind | 32 act, 6 ordinance, 39 treaty, 7 directive, 164 guidance, 26 directory, 24 summary |
| Facts by their strongest basis | 31 act, 6 ordinance, 37 treaty, 6 directive, 161 guidance, 26 directory, 23 summary |
| Documents by institution level | 27 federal, 14 cantonal, 3 municipal |
| Excerpts whose basis differs from the page default | 0 (every citation-level entry restates the page's kind and adds the article) |
| Concepts whose facts mix basis kinds | 8: `ahv-contribution-refund`, `bvg-cash-out-departure`, `family-separation`, `family-swiss`, `foreign-licence-exchange`, `tax-at-source-liability`, `zh-tax-at-source-liability`, `zh-tax-at-source-ordinary-assessment` |
| Guidance or directive excerpts naming a legal norm | 16 |
| Validation issues (institution missing, federal fact on a cantonal basis, norm missing) | 0 |

Two things the reading found that a build rule must handle when it derives the article from the anchor's heading path: Fedlex glues footnote numbers to article and paragraph numbers (the AIG heading `Art. 4384` is Article 43 with footnote 84, `Art. 4486` is Article 44 with footnote 86, `Absatz 169` is paragraph 1 with footnote 69), and the Agreement on the Free Movement of Persons numbers the articles of its Annex I from 1 again, so `I. Grundbestimmungen > Art. 1` is Article 1 of the agreement while `I. Allgemeine Bestimmungen > Art. 1` is Article 1 of Annex I. The norms below are written out per citation for that reason.

## Institutions

| Institution | Level | Jurisdiction | Excerpts |
| --- | --- | --- | ---: |
| Federal Office of Public Health FOPH | federal | CH | 15 |
| Federal Social Insurance Office FSIO | federal | CH | 6 |
| ch.ch, the information portal of the Confederation, cantons and communes (Federal Chancellery) | federal | CH | 24 |
| Federal Tax Administration FTA | federal | CH | 4 |
| Fedlex, the Swiss federal law collection (Federal Chancellery) | federal | CH | 77 |
| State Secretariat for Migration SEM | federal | CH | 62 |
| Central Compensation Office CCO | federal | CH | 16 |
| Canton of Zurich, Office for Municipalities, Naturalisation Division | cantonal | CH-ZH | 19 |
| Canton of Zurich, Health Directorate | cantonal | CH-ZH | 4 |
| Canton of Zurich, Migration Office | cantonal | CH-ZH | 8 |
| Canton of Zurich, Cantonal Tax Office | cantonal | CH-ZH | 20 |
| Canton of Zurich, Road Traffic Office | cantonal | CH-ZH | 19 |
| SVA Zürich, the cantonal social insurance office | cantonal | CH-ZH | 9 |
| City of Zurich, Naturalisation Division | municipal | CH-ZH-261 | 13 |
| City of Zurich, Population Office | municipal | CH-ZH-261 | 2 |

## Every excerpt

Grouped by page. `Rule` says which rule of the design's section 4.3 produced the basis: the citation's own entry, a page rule, or the guidance default.

### Krankenversicherung: Prämienverbilligung

Publisher: Federal Office of Public Health FOPH (federal, CH); attributed by rule `www.bag.admin.ch`; page: <https://www.bag.admin.ch/de/krankenversicherung-praemienverbilligung>

| Evidence | Fact jurisdiction | Basis | Rule | Refers to |
| --- | --- | --- | --- | --- |
| `e-premium-reduction-1-1` | CH | Federal authority guidance | default |  |
| `e-premium-reduction-2-1` | CH | Federal authority guidance | default |  |
| `e-premium-reduction-3-1` | CH | Federal authority guidance | default |  |
| `e-premium-reduction-4-1` | CH | Federal authority guidance | default |  |
| `e-premium-reduction-5-1` | CH | Federal authority guidance | default |  |

### Krankenversicherung: Versicherungspflicht für in der Schweiz wohnhafte Versicherte

Publisher: Federal Office of Public Health FOPH (federal, CH); attributed by rule `www.bag.admin.ch`; page: <https://www.bag.admin.ch/de/krankenversicherung-versicherungspflicht-fuer-in-der-schweiz-wohnhafte-versicherte>

| Evidence | Fact jurisdiction | Basis | Rule | Refers to |
| --- | --- | --- | --- | --- |
| `e-health-insurance-enrolment-1-1` | CH | Federal authority guidance | default |  |
| `e-health-insurance-enrolment-2-1` | CH | Federal authority guidance | default |  |
| `e-health-insurance-deadline-1-1` | CH | Federal authority guidance | default |  |
| `e-health-insurance-deadline-2-1` | CH | Federal authority guidance | default |  |
| `e-health-insurance-deadline-3-1` | CH | Federal authority guidance | default |  |
| `e-health-insurance-deadline-4-1` | CH | Federal authority guidance | default |  |
| `e-health-insurance-deadline-5-1` | CH | Federal authority guidance | default |  |
| `e-health-insurance-deadline-6-1` | CH | Federal authority guidance | default |  |
| `e-health-insurance-deadline-7-1` | CH | Federal authority guidance | default |  |
| `e-health-insurance-deadline-8-1` | CH | Federal authority guidance | default |  |

### Kann ich mein BVG-Altersguthaben bar beziehen, wenn ich die Schweiz endgültig verlasse? | BSV

Publisher: Federal Social Insurance Office FSIO (federal, CH); attributed by rule `faq.bsv.admin.ch`; page: <https://faq.bsv.admin.ch/de/berufliche-vorsorge-und-3-saeule/kann-ich-mein-bvg-altersguthaben-bar-beziehen-wenn-ich-die-schweiz>

| Evidence | Fact jurisdiction | Basis | Rule | Refers to |
| --- | --- | --- | --- | --- |
| `e-bvg-cash-out-departure-1-1` | CH | Federal authority guidance | default |  |
| `e-bvg-cash-out-departure-2-1` | CH | Federal authority guidance | default |  |
| `e-bvg-cash-out-departure-3-1` | CH | Federal authority guidance | default |  |
| `e-bvg-cash-out-departure-4-1` | CH | Federal authority guidance | default |  |
| `e-bvg-cash-out-departure-5-1` | CH | Federal authority guidance | default |  |
| `e-bvg-cash-out-departure-6-1` | CH | Federal authority guidance | default |  |

### Als Ausländerin oder Ausländer in der Schweiz arbeiten

Publisher: ch.ch, the information portal of the Confederation, cantons and communes (Federal Chancellery) (federal, CH); attributed by rule `www.ch.ch`; page: <https://www.ch.ch/de/auslander-in-der-schweiz/in-der-schweiz-arbeiten/>

| Evidence | Fact jurisdiction | Basis | Rule | Refers to |
| --- | --- | --- | --- | --- |
| `e-third-country-work-procedure-1-1` | CH | Portal summary of federal rules | page rule |  |
| `e-third-country-work-procedure-2-1` | CH | Portal summary of federal rules | page rule |  |
| `e-third-country-work-procedure-3-1` | CH | Portal summary of federal rules | page rule |  |
| `e-third-country-work-procedure-4-1` | CH | Portal summary of federal rules | page rule |  |
| `e-eu-permit-mobility-1-1` | CH | Portal summary of federal rules | page rule |  |
| `e-eu-self-employment-1-1` | CH | Portal summary of federal rules | page rule |  |
| `e-eu-job-search-1-1` | CH | Portal summary of federal rules | page rule |  |

### Aufenthaltsbewilligung für die Schweiz: Gesuch und Erneuerung

Publisher: ch.ch, the information portal of the Confederation, cantons and communes (Federal Chancellery) (federal, CH); attributed by rule `www.ch.ch`; page: <https://www.ch.ch/de/auslander-in-der-schweiz/einreise-in-die-schweiz/aufenthaltsbewilligung/>

| Evidence | Fact jurisdiction | Basis | Rule | Refers to |
| --- | --- | --- | --- | --- |
| `e-permit-types-1-1` | CH | Portal summary of federal rules | page rule |  |
| `e-permit-renewal-1-1` | CH | Portal summary of federal rules | page rule |  |
| `e-permit-renewal-1-2` | CH | Portal summary of federal rules | page rule |  |
| `e-permit-renewal-2-1` | CH | Portal summary of federal rules | page rule |  |
| `e-permit-renewal-3-1` | CH | Portal summary of federal rules | page rule |  |
| `e-permit-lost-1-1` | CH | Portal summary of federal rules | page rule |  |
| `e-family-separation-2-1` | CH | Portal summary of federal rules | page rule |  |
| `e-family-separation-3-1` | CH | Portal summary of federal rules | page rule |  |

### Gesuch um Familiennachzug in die Schweiz

Publisher: ch.ch, the information portal of the Confederation, cantons and communes (Federal Chancellery) (federal, CH); attributed by rule `www.ch.ch`; page: <https://www.ch.ch/de/auslander-in-der-schweiz/einreise-in-die-schweiz/familiennachzug/>

| Evidence | Fact jurisdiction | Basis | Rule | Refers to |
| --- | --- | --- | --- | --- |
| `e-family-swiss-2-1` | CH | Portal summary of federal rules | page rule |  |
| `e-family-eu-efta-1-1` | CH | Portal summary of federal rules | page rule |  |
| `e-family-requirements-1-1` | CH | Portal summary of federal rules | page rule |  |
| `e-family-requirements-2-1` | CH | Portal summary of federal rules | page rule |  |
| `e-family-requirements-3-1` | CH | Portal summary of federal rules | page rule |  |
| `e-family-member-rights-1-1` | CH | Portal summary of federal rules | page rule |  |

### Verlust, Diebstahl, Umtausch des Führerausweises in der Schweiz

Publisher: ch.ch, the information portal of the Confederation, cantons and communes (Federal Chancellery) (federal, CH); attributed by rule `www.ch.ch`; page: <https://www.ch.ch/de/ausweise-und-dokumente/fuhrerausweis/fuhrerausweis-umtauschen/>

| Evidence | Fact jurisdiction | Basis | Rule | Refers to |
| --- | --- | --- | --- | --- |
| `e-foreign-licence-exchange-3-1` | CH | Portal summary of federal rules | page rule |  |
| `e-foreign-licence-exchange-4-1` | CH | Portal summary of federal rules | page rule |  |
| `e-foreign-licence-exchange-5-1` | CH | Portal summary of federal rules | page rule |  |

### Schweizerische Quellensteuer QST

Publisher: Federal Tax Administration FTA (federal, CH); attributed by rule `www.estv.admin.ch`; page: <https://www.estv.admin.ch/de/quellensteuer>

| Evidence | Fact jurisdiction | Basis | Rule | Refers to |
| --- | --- | --- | --- | --- |
| `e-tax-at-source-liability-1-1` | CH | Federal authority guidance | default |  |
| `e-tax-at-source-liability-2-1` | CH | Federal authority guidance | default |  |
| `e-tax-at-source-liability-3-1` | CH | Federal authority guidance | default |  |
| `e-tax-at-source-liability-7-1` | CH | Federal authority guidance | default |  |

### AIG / LEI / FNIA, SR 142.20

Publisher: Fedlex, the Swiss federal law collection (Federal Chancellery) (federal, CH); attributed by rule `www.fedlex.admin.ch`; page: <https://www.fedlex.admin.ch/eli/cc/2007/758/de>

| Evidence | Fact jurisdiction | Basis | Rule | Refers to |
| --- | --- | --- | --- | --- |
| `e-aig-short-stay-1-1` | CH | Federal act: AIG, SR 142.20, Art. 10 | citation |  |
| `e-aig-short-stay-2-1` | CH | Federal act: AIG, SR 142.20, Art. 10 Abs. 2 | citation |  |
| `e-aig-work-permit-1-1` | CH | Federal act: AIG, SR 142.20, Art. 11 | citation |  |
| `e-aig-work-permit-2-1` | CH | Federal act: AIG, SR 142.20, Art. 11 Abs. 2 und 3 | citation |  |
| `e-aig-registration-1-1` | CH | Federal act: AIG, SR 142.20, Art. 12 | citation |  |
| `e-aig-registration-2-1` | CH | Federal act: AIG, SR 142.20, Art. 12 Abs. 2 und 3 | citation |  |
| `e-permit-l-1-1` | CH | Federal act: AIG, SR 142.20, Art. 32 | citation |  |
| `e-permit-l-2-1` | CH | Federal act: AIG, SR 142.20, Art. 32 Abs. 3 und 4 | citation |  |
| `e-permit-b-1-1` | CH | Federal act: AIG, SR 142.20, Art. 33 | citation |  |
| `e-permit-b-2-1` | CH | Federal act: AIG, SR 142.20, Art. 33 Abs. 3 bis 5 | citation |  |
| `e-permit-c-1-1` | CH | Federal act: AIG, SR 142.20, Art. 34 | citation |  |
| `e-permit-c-2-1` | CH | Federal act: AIG, SR 142.20, Art. 34 Abs. 2 bis 4 | citation |  |
| `e-permit-c-3-1` | CH | Federal act: AIG, SR 142.20, Art. 34 Abs. 5 | citation |  |
| `e-aig-study-1-1` | CH | Federal act: AIG, SR 142.20, Art. 27 | citation |  |
| `e-aig-study-2-1` | CH | Federal act: AIG, SR 142.20, Art. 27 Abs. 3 | citation |  |
| `e-integration-criteria-1-1` | CH | Federal act: AIG, SR 142.20, Art. 58a | citation |  |
| `e-integration-criteria-2-1` | CH | Federal act: AIG, SR 142.20, Art. 58a Abs. 2 | citation |  |
| `e-family-swiss-1-1` | CH | Federal act: AIG, SR 142.20, Art. 42 Abs. 1 | citation |  |
| `e-family-c-1-1` | CH | Federal act: AIG, SR 142.20, Art. 43 | citation | ELG, SR 831.30 |
| `e-family-c-2-1` | CH | Federal act: AIG, SR 142.20, Art. 43 Abs. 2 und 3 | citation |  |
| `e-family-b-1-1` | CH | Federal act: AIG, SR 142.20, Art. 44 | citation |  |
| `e-family-b-2-1` | CH | Federal act: AIG, SR 142.20, Art. 44 Abs. 2 und 3 | citation |  |
| `e-family-deadlines-1-1` | CH | Federal act: AIG, SR 142.20, Art. 47 | citation |  |
| `e-family-deadlines-2-1` | CH | Federal act: AIG, SR 142.20, Art. 47 Abs. 3 | citation |  |
| `e-family-deadlines-3-1` | CH | Federal act: AIG, SR 142.20, Art. 47 Abs. 4 | citation |  |
| `e-family-separation-1-1` | CH | Federal act: AIG, SR 142.20, Art. 50 Abs. 1 | citation |  |
| `e-canton-change-1-1` | CH | Federal act: AIG, SR 142.20, Art. 37 | citation |  |
| `e-canton-change-2-1` | CH | Federal act: AIG, SR 142.20, Art. 37 Abs. 2 bis 4 | citation |  |

### FZA / ALCP, SR 0.142.112.681

Publisher: Fedlex, the Swiss federal law collection (Federal Chancellery) (federal, CH); attributed by rule `www.fedlex.admin.ch`; page: <https://www.fedlex.admin.ch/eli/cc/2002/243/de>

| Evidence | Fact jurisdiction | Basis | Rule | Refers to |
| --- | --- | --- | --- | --- |
| `e-fza-overview-1-1` | CH | International agreement: FZA, SR 0.142.112.681, title and entry into force | citation |  |
| `e-fza-overview-1-2` | CH | International agreement: FZA, SR 0.142.112.681, Art. 1 | citation |  |
| `e-fza-overview-2-1` | CH | International agreement: FZA, SR 0.142.112.681, Art. 2 | citation |  |
| `e-fza-overview-3-1` | CH | International agreement: FZA, SR 0.142.112.681, Annex I, Art. 5 | citation |  |
| `e-fza-overview-4-1` | CH | International agreement: FZA, SR 0.142.112.681, Annex I, Art. 2 Abs. 4 | citation |  |
| `e-fza-entry-1-1` | CH | International agreement: FZA, SR 0.142.112.681, Annex I, Art. 1 | citation |  |
| `e-fza-job-search-1-1` | CH | International agreement: FZA, SR 0.142.112.681, Annex I, Art. 2 Abs. 1 | citation |  |
| `e-fza-employee-permit-1-1` | CH | International agreement: FZA, SR 0.142.112.681, Annex I, Art. 6 Abs. 1 | citation |  |
| `e-fza-employee-permit-2-1` | CH | International agreement: FZA, SR 0.142.112.681, Annex I, Art. 6 Abs. 2 | citation |  |
| `e-fza-employee-permit-3-1` | CH | International agreement: FZA, SR 0.142.112.681, Annex I, Art. 6 Abs. 3 | citation |  |
| `e-fza-employee-permit-4-1` | CH | International agreement: FZA, SR 0.142.112.681, Annex I, Art. 6 Abs. 4 und 5 | citation |  |
| `e-fza-employee-permit-5-1` | CH | International agreement: FZA, SR 0.142.112.681, Annex I, Art. 6 Abs. 6 | citation |  |
| `e-fza-mobility-1-1` | CH | International agreement: FZA, SR 0.142.112.681, Annex I, Art. 8 | citation |  |
| `e-fza-mobility-2-1` | CH | International agreement: FZA, SR 0.142.112.681, Annex I, Art. 14 | citation |  |
| `e-fza-self-employment-1-1` | CH | International agreement: FZA, SR 0.142.112.681, Annex I, Art. 12 Abs. 1 und 2 | citation |  |
| `e-fza-self-employment-2-1` | CH | International agreement: FZA, SR 0.142.112.681, Annex I, Art. 12 Abs. 3 | citation |  |
| `e-fza-self-employment-3-1` | CH | International agreement: FZA, SR 0.142.112.681, Annex I, Art. 12 Abs. 4 bis 6 | citation |  |
| `e-fza-cross-border-commuter-1-1` | CH | International agreement: FZA, SR 0.142.112.681, Annex I, Art. 7 | citation |  |
| `e-fza-cross-border-commuter-2-1` | CH | International agreement: FZA, SR 0.142.112.681, Annex I, Art. 13 | citation |  |
| `e-fza-family-members-1-1` | CH | International agreement: FZA, SR 0.142.112.681, Annex I, Art. 3 Abs. 1 | citation |  |
| `e-fza-family-members-2-1` | CH | International agreement: FZA, SR 0.142.112.681, Annex I, Art. 3 Abs. 2 | citation |  |
| `e-fza-family-members-3-1` | CH | International agreement: FZA, SR 0.142.112.681, Annex I, Art. 3 Abs. 3 | citation |  |
| `e-fza-family-members-4-1` | CH | International agreement: FZA, SR 0.142.112.681, Annex I, Art. 3 Abs. 4 und 5 | citation |  |
| `e-fza-non-working-1-1` | CH | International agreement: FZA, SR 0.142.112.681, Annex I, Art. 24 Abs. 1 | citation |  |
| `e-fza-non-working-2-1` | CH | International agreement: FZA, SR 0.142.112.681, Annex I, Art. 24 Abs. 2 | citation |  |
| `e-fza-non-working-3-1` | CH | International agreement: FZA, SR 0.142.112.681, Annex I, Art. 24 Abs. 3 | citation |  |
| `e-fza-non-working-4-1` | CH | International agreement: FZA, SR 0.142.112.681, Annex I, Art. 24 Abs. 4 | citation |  |
| `e-fza-non-working-5-1` | CH | International agreement: FZA, SR 0.142.112.681, Annex I, Art. 24 Abs. 5 bis 8 | citation |  |
| `e-fza-services-1-1` | CH | International agreement: FZA, SR 0.142.112.681, Art. 5 Abs. 1 | citation |  |
| `e-fza-services-1-2` | CH | International agreement: FZA, SR 0.142.112.681, Annex I, Art. 21 | citation |  |
| `e-fza-services-2-1` | CH | International agreement: FZA, SR 0.142.112.681, Annex I, Art. 17 | citation |  |
| `e-fza-services-3-1` | CH | International agreement: FZA, SR 0.142.112.681, Annex I, Art. 20 | citation |  |
| `e-fza-services-4-1` | CH | International agreement: FZA, SR 0.142.112.681, Annex I, Art. 22 Abs. 2 und 3 | citation |  |
| `e-fza-services-5-1` | CH | International agreement: FZA, SR 0.142.112.681, Annex I, Art. 23 | citation |  |
| `e-fza-right-to-remain-1-1` | CH | International agreement: FZA, SR 0.142.112.681, Annex I, Art. 4 Abs. 1 | citation |  |
| `e-fza-equal-treatment-1-1` | CH | International agreement: FZA, SR 0.142.112.681, Annex I, Art. 9 | citation |  |
| `e-fza-equal-treatment-2-1` | CH | International agreement: FZA, SR 0.142.112.681, Annex I, Art. 10 | citation |  |
| `e-fza-equal-treatment-3-1` | CH | International agreement: FZA, SR 0.142.112.681, Annex I, Art. 15 | citation |  |
| `e-fza-social-security-1-1` | CH | International agreement: FZA, SR 0.142.112.681, Art. 8 | citation |  |

### Fedlex: Ordinance on the Admission of Persons and Vehicles to Road Traffic, SR 741.51

Publisher: Fedlex, the Swiss federal law collection (Federal Chancellery) (federal, CH); attributed by rule `www.fedlex.admin.ch`; page: <https://www.fedlex.admin.ch/eli/cc/1976/2423_2423_2423/de>

| Evidence | Fact jurisdiction | Basis | Rule | Refers to |
| --- | --- | --- | --- | --- |
| `e-foreign-licence-exchange-1-1` | CH | Federal ordinance: VZV, SR 741.51, Art. 42 Abs. 3bis | citation |  |
| `e-foreign-licence-exchange-2-1` | CH | Federal ordinance: VZV, SR 741.51, Art. 42 Abs. 1 | citation |  |

### Fedlex: Tax at Source Ordinance of the FDF, SR 642.118.2

Publisher: Fedlex, the Swiss federal law collection (Federal Chancellery) (federal, CH); attributed by rule `www.fedlex.admin.ch`; page: <https://www.fedlex.admin.ch/eli/cc/2018/274/de>

| Evidence | Fact jurisdiction | Basis | Rule | Refers to |
| --- | --- | --- | --- | --- |
| `e-tax-at-source-liability-4-1` | CH | Federal ordinance: QStV, SR 642.118.2, Art. 9 Abs. 1 | citation | DBG, SR 642.11, Art. 89 Abs. 1 Bst. a |
| `e-tax-at-source-liability-5-1` | CH | Federal ordinance: QStV, SR 642.118.2, Art. 9 Abs. 3 | citation |  |
| `e-tax-at-source-liability-6-1` | CH | Federal ordinance: QStV, SR 642.118.2, Art. 9 Abs. 4 | citation |  |

### Fedlex: Vested Benefits Act, SR 831.42

Publisher: Fedlex, the Swiss federal law collection (Federal Chancellery) (federal, CH); attributed by rule `www.fedlex.admin.ch`; page: <https://www.fedlex.admin.ch/eli/cc/1994/2386_2386_2386/de>

| Evidence | Fact jurisdiction | Basis | Rule | Refers to |
| --- | --- | --- | --- | --- |
| `e-bvg-cash-out-departure-7-1` | CH | Federal act: FZG, SR 831.42, Art. 25f Abs. 1 | citation | BVG, SR 831.40, Art. 15 |
| `e-bvg-cash-out-departure-8-1` | CH | Federal act: FZG, SR 831.42, Art. 5 Abs. 1 Bst. a | citation |  |
| `e-bvg-cash-out-departure-8-2` | CH | Federal act: FZG, SR 831.42, Art. 5 Abs. 2 | citation |  |
| `e-bvg-cash-out-departure-9-1` | CH | Federal act: FZG, SR 831.42, Art. 4 | citation | BVG, SR 831.40, Art. 60 |

### Fedlex: ordinance on the refund of AHV contributions paid by foreign nationals, SR 831.131.12

Publisher: Fedlex, the Swiss federal law collection (Federal Chancellery) (federal, CH); attributed by rule `www.fedlex.admin.ch`; page: <https://www.fedlex.admin.ch/eli/cc/1996/688_688_688/de>

| Evidence | Fact jurisdiction | Basis | Rule | Refers to |
| --- | --- | --- | --- | --- |
| `e-ahv-contribution-refund-9-1` | CH | Federal ordinance: RV-AHV, SR 831.131.12, Art. 1 | citation |  |

### Der biometrische Ausländerausweis

Publisher: State Secretariat for Migration SEM (federal, CH); attributed by rule `www.sem.admin.ch`; page: <https://www.sem.admin.ch/sem/de/home/themen/aufenthalt/biometr_auslaenderausweis.html>

| Evidence | Fact jurisdiction | Basis | Rule | Refers to |
| --- | --- | --- | --- | --- |
| `e-biometric-permit-1-1` | CH | Federal authority guidance | default |  |
| `e-biometric-permit-2-1` | CH | Federal authority guidance | default |  |

### Die Ordentliche Einbürgerung

Publisher: State Secretariat for Migration SEM (federal, CH); attributed by rule `www.sem.admin.ch`; page: <https://www.sem.admin.ch/sem/de/home/integration-einbuergerung/schweizer-werden/ordentlich.html>

| Evidence | Fact jurisdiction | Basis | Rule | Refers to |
| --- | --- | --- | --- | --- |
| `e-naturalisation-ordinary-1-1` | CH | Federal authority guidance | default |  |
| `e-naturalisation-ordinary-3-1` | CH | Federal authority guidance | default |  |
| `e-naturalisation-ordinary-7-1` | CH | Federal authority guidance | default |  |
| `e-naturalisation-ordinary-8-1` | CH | Federal authority guidance | default |  |
| `e-naturalisation-ordinary-9-1` | CH | Federal authority guidance | default |  |

### FAQ - Fragen zur Personenfreizügigkeit

Publisher: State Secretariat for Migration SEM (federal, CH); attributed by rule `www.sem.admin.ch`; page: <https://www.sem.admin.ch/sem/de/home/themen/fza_schweiz-eu-efta/eu-efta_buerger_schweiz/faq.html>

| Evidence | Fact jurisdiction | Basis | Rule | Refers to |
| --- | --- | --- | --- | --- |
| `e-eu-employment-registration-deadline-1-1` | CH | Federal authority guidance | default |  |
| `e-eu-employment-registration-deadline-2-1` | CH | Federal authority guidance | default |  |

### FAQ - Schweizer Bürgerrecht

Publisher: State Secretariat for Migration SEM (federal, CH); attributed by rule `www.sem.admin.ch`; page: <https://www.sem.admin.ch/sem/de/home/integration-einbuergerung/schweizer-werden/faq.html>

| Evidence | Fact jurisdiction | Basis | Rule | Refers to |
| --- | --- | --- | --- | --- |
| `e-naturalisation-ordinary-2-1` | CH | Federal authority guidance | default | BüG, SR 141.0, Art. 9 |
| `e-naturalisation-ordinary-4-1` | CH | Federal authority guidance | default |  |
| `e-naturalisation-ordinary-5-1` | CH | Federal authority guidance | default |  |
| `e-naturalisation-ordinary-6-1` | CH | Federal authority guidance | default | BüV, SR 141.01, Art. 6 |
| `e-naturalisation-facilitated-spouse-7-1` | CH | Federal authority guidance | default |  |
| `e-naturalisation-facilitated-spouse-8-1` | CH | Federal authority guidance | default |  |
| `e-naturalisation-facilitated-spouse-9-1` | CH | Federal authority guidance | default | BüV, SR 141.01, Art. 25 |

### FAQ Aufenthalt und Integrationskriterien

Publisher: State Secretariat for Migration SEM (federal, CH); attributed by rule `www.sem.admin.ch`; page: <https://www.sem.admin.ch/sem/de/home/themen/aufenthalt/faq.html>

| Evidence | Fact jurisdiction | Basis | Rule | Refers to |
| --- | --- | --- | --- | --- |
| `e-language-evidence-1-1` | CH | Federal authority guidance | default |  |
| `e-language-evidence-2-1` | CH | Federal authority guidance | default |  |
| `e-social-assistance-review-1-1` | CH | Federal authority guidance | default |  |

### Kantonale Migrations- und Arbeitsmarktbehörden

Publisher: State Secretariat for Migration SEM (federal, CH); attributed by rule `www.sem.admin.ch`; page: <https://www.sem.admin.ch/sem/de/home/sem/kontakt/kantonale_behoerden/adressen_kantone_und.html>

| Evidence | Fact jurisdiction | Basis | Rule | Refers to |
| --- | --- | --- | --- | --- |
| `e-cantonal-migration-contact-ag-1` | CH-AG | Federal authority directory | page rule |  |
| `e-cantonal-migration-contact-ai-1` | CH-AI | Federal authority directory | page rule |  |
| `e-cantonal-migration-contact-ar-1` | CH-AR | Federal authority directory | page rule |  |
| `e-cantonal-migration-contact-be-1` | CH-BE | Federal authority directory | page rule |  |
| `e-cantonal-migration-contact-bl-1` | CH-BL | Federal authority directory | page rule |  |
| `e-cantonal-migration-contact-bs-1` | CH-BS | Federal authority directory | page rule |  |
| `e-cantonal-migration-contact-fr-1` | CH-FR | Federal authority directory | page rule |  |
| `e-cantonal-migration-contact-ge-1` | CH-GE | Federal authority directory | page rule |  |
| `e-cantonal-migration-contact-gl-1` | CH-GL | Federal authority directory | page rule |  |
| `e-cantonal-migration-contact-gr-1` | CH-GR | Federal authority directory | page rule |  |
| `e-cantonal-migration-contact-ju-1` | CH-JU | Federal authority directory | page rule |  |
| `e-cantonal-migration-contact-lu-1` | CH-LU | Federal authority directory | page rule |  |
| `e-cantonal-migration-contact-ne-1` | CH-NE | Federal authority directory | page rule |  |
| `e-cantonal-migration-contact-nw-1` | CH-NW | Federal authority directory | page rule |  |
| `e-cantonal-migration-contact-ow-1` | CH-OW | Federal authority directory | page rule |  |
| `e-cantonal-migration-contact-sg-1` | CH-SG | Federal authority directory | page rule |  |
| `e-cantonal-migration-contact-sh-1` | CH-SH | Federal authority directory | page rule |  |
| `e-cantonal-migration-contact-so-1` | CH-SO | Federal authority directory | page rule |  |
| `e-cantonal-migration-contact-sz-1` | CH-SZ | Federal authority directory | page rule |  |
| `e-cantonal-migration-contact-tg-1` | CH-TG | Federal authority directory | page rule |  |
| `e-cantonal-migration-contact-ti-1` | CH-TI | Federal authority directory | page rule |  |
| `e-cantonal-migration-contact-ur-1` | CH-UR | Federal authority directory | page rule |  |
| `e-cantonal-migration-contact-vd-1` | CH-VD | Federal authority directory | page rule |  |
| `e-cantonal-migration-contact-vs-1` | CH-VS | Federal authority directory | page rule |  |
| `e-cantonal-migration-contact-zg-1` | CH-ZG | Federal authority directory | page rule |  |
| `e-cantonal-migration-contact-zh-1` | CH-ZH | Federal authority directory | page rule |  |

### Meldeverfahren für kurzfristige Erwerbstätigkeit

Publisher: State Secretariat for Migration SEM (federal, CH); attributed by rule `www.sem.admin.ch`; page: <https://www.sem.admin.ch/sem/de/home/themen/fza_schweiz-eu-efta/meldeverfahren.html>

| Evidence | Fact jurisdiction | Basis | Rule | Refers to |
| --- | --- | --- | --- | --- |
| `e-eu-short-employment-1-1` | CH | Federal authority guidance | default |  |
| `e-eu-short-employment-2-1` | CH | Federal authority guidance | default |  |
| `e-notification-responsibility-1-1` | CH | Federal authority guidance | default |  |
| `e-posted-service-notification-1-1` | CH | Federal authority guidance | default | FZA, SR 0.142.112.681 |
| `e-posted-service-notification-2-1` | CH | Federal authority guidance | default |  |
| `e-uk-new-employment-1-1` | CH | Federal authority guidance | default | AIG, SR 142.20 |
| `e-uk-new-employment-2-1` | CH | Federal authority guidance | default | AIG, SR 142.20 |
| `e-uk-new-employment-3-1` | CH | Federal authority guidance | default | FZA, SR 0.142.112.681; Agreement between Switzerland and the United Kingdom on the mobility of service suppliers |

### Nicht-EU/EFTA-Angehörige

Publisher: State Secretariat for Migration SEM (federal, CH); attributed by rule `www.sem.admin.ch`; page: <https://www.sem.admin.ch/sem/de/home/themen/arbeit/nicht-eu_efta-angehoerige.html>

| Evidence | Fact jurisdiction | Basis | Rule | Refers to |
| --- | --- | --- | --- | --- |
| `e-third-country-work-1-1` | CH | Federal authority guidance | default |  |
| `e-third-country-work-2-1` | CH | Federal authority guidance | default |  |

### Residence

Publisher: State Secretariat for Migration SEM (federal, CH); attributed by rule `www.sem.admin.ch`; page: <https://www.sem.admin.ch/sem/en/home/themen/aufenthalt.html>

| Evidence | Fact jurisdiction | Basis | Rule | Refers to |
| --- | --- | --- | --- | --- |
| `e-permit-authority-1-1` | CH | Federal authority guidance | default |  |

### Verheiratet mit einer Schweizerin oder einem Schweizer

Publisher: State Secretariat for Migration SEM (federal, CH); attributed by rule `www.sem.admin.ch`; page: <https://www.sem.admin.ch/sem/de/home/integration-einbuergerung/schweizer-werden/verheiratet.html>

| Evidence | Fact jurisdiction | Basis | Rule | Refers to |
| --- | --- | --- | --- | --- |
| `e-naturalisation-facilitated-spouse-1-1` | CH | Federal authority guidance | default |  |
| `e-naturalisation-facilitated-spouse-2-1` | CH | Federal authority guidance | default |  |
| `e-naturalisation-facilitated-spouse-3-1` | CH | Federal authority guidance | default |  |
| `e-naturalisation-facilitated-spouse-4-1` | CH | Federal authority guidance | default |  |
| `e-naturalisation-facilitated-spouse-5-1` | CH | Federal authority guidance | default |  |
| `e-naturalisation-facilitated-spouse-6-1` | CH | Federal authority guidance | default |  |

### Anspruch auf AHV-Rentenzahlungen ausserhalb der Schweiz

Publisher: Central Compensation Office CCO (federal, CH); attributed by rule `www.zas.admin.ch`; page: <https://www.zas.admin.ch/de/anspruch-auf-ahv-rentenzahlungen-ausserhalb-der-schweiz>

| Evidence | Fact jurisdiction | Basis | Rule | Refers to |
| --- | --- | --- | --- | --- |
| `e-ahv-contribution-refund-10-1` | CH | Federal authority guidance | default |  |
| `e-ahv-pension-abroad-1-1` | CH | Federal authority guidance | default |  |
| `e-ahv-pension-abroad-2-1` | CH | Federal authority guidance | default |  |
| `e-ahv-pension-abroad-3-1` | CH | Federal authority guidance | default |  |
| `e-ahv-pension-abroad-4-1` | CH | Federal authority guidance | default |  |
| `e-ahv-pension-abroad-5-1` | CH | Federal authority guidance | default |  |
| `e-ahv-pension-abroad-6-1` | CH | Federal authority guidance | default |  |
| `e-ahv-pension-abroad-6-2` | CH | Federal authority guidance | default |  |

### Rückvergütungen

Publisher: Central Compensation Office CCO (federal, CH); attributed by rule `www.zas.admin.ch`; page: <https://www.zas.admin.ch/de/rueckverguetungen>

| Evidence | Fact jurisdiction | Basis | Rule | Refers to |
| --- | --- | --- | --- | --- |
| `e-ahv-contribution-refund-1-1` | CH | Federal authority guidance | default |  |
| `e-ahv-contribution-refund-2-1` | CH | Federal authority guidance | default |  |
| `e-ahv-contribution-refund-3-1` | CH | Federal authority guidance | default |  |
| `e-ahv-contribution-refund-4-1` | CH | Federal authority guidance | default |  |
| `e-ahv-contribution-refund-6-1` | CH | Federal authority guidance | default |  |
| `e-ahv-contribution-refund-7-1` | CH | Federal authority guidance | default |  |
| `e-ahv-contribution-refund-8-1` | CH | Federal authority guidance | default |  |

### Staatsangehörigkeit eines Staates mit Sozialversicherungsabkommen (AHV)

Publisher: Central Compensation Office CCO (federal, CH); attributed by rule `www.zas.admin.ch`; page: <https://www.zas.admin.ch/de/staatsangehoerigkeit-eines-staates-mit-sozialversicherungsabkommen-ahv>

| Evidence | Fact jurisdiction | Basis | Rule | Refers to |
| --- | --- | --- | --- | --- |
| `e-ahv-contribution-refund-5-1` | CH | Federal authority guidance | default |  |

### Einbürgerungsgesuch einreichen | Kanton Zürich

Publisher: Canton of Zurich, Office for Municipalities, Naturalisation Division (cantonal, CH-ZH); attributed by rule `www.zh.ch/de/migration-integration/einbuergerung`; page: <https://www.zh.ch/de/migration-integration/einbuergerung/ordentliche-einbuergerung/einbuergerungsgesuch-einreichen.html>

| Evidence | Fact jurisdiction | Basis | Rule | Refers to |
| --- | --- | --- | --- | --- |
| `e-zh-naturalisation-ordinary-8-1` | CH-ZH | Cantonal authority guidance | default |  |
| `e-zh-naturalisation-ordinary-9-2` | CH-ZH | Cantonal authority guidance | default |  |
| `e-zh-naturalisation-ordinary-11-1` | CH-ZH | Cantonal authority guidance | default |  |

### Erleichterte Einbürgerung | Kanton Zürich

Publisher: Canton of Zurich, Office for Municipalities, Naturalisation Division (cantonal, CH-ZH); attributed by rule `www.zh.ch/de/migration-integration/einbuergerung`; page: <https://www.zh.ch/de/migration-integration/einbuergerung/erleichterte-einbuergerung.html>

| Evidence | Fact jurisdiction | Basis | Rule | Refers to |
| --- | --- | --- | --- | --- |
| `e-zh-naturalisation-facilitated-1-1` | CH-ZH | Cantonal authority guidance | default |  |
| `e-zh-naturalisation-facilitated-2-1` | CH-ZH | Cantonal authority guidance | default |  |
| `e-zh-naturalisation-facilitated-3-1` | CH-ZH | Cantonal authority guidance | default |  |
| `e-zh-naturalisation-facilitated-4-1` | CH-ZH | Cantonal authority guidance | default |  |
| `e-zh-naturalisation-facilitated-5-1` | CH-ZH | Cantonal authority guidance | default |  |

### Ordentliche Einbürgerung | Kanton Zürich

Publisher: Canton of Zurich, Office for Municipalities, Naturalisation Division (cantonal, CH-ZH); attributed by rule `www.zh.ch/de/migration-integration/einbuergerung`; page: <https://www.zh.ch/de/migration-integration/einbuergerung/ordentliche-einbuergerung.html>

| Evidence | Fact jurisdiction | Basis | Rule | Refers to |
| --- | --- | --- | --- | --- |
| `e-zh-naturalisation-ordinary-1-1` | CH-ZH | Cantonal authority guidance | default |  |
| `e-zh-naturalisation-ordinary-2-1` | CH-ZH | Cantonal authority guidance | default |  |
| `e-zh-naturalisation-ordinary-3-1` | CH-ZH | Cantonal authority guidance | default |  |
| `e-zh-naturalisation-ordinary-4-1` | CH-ZH | Cantonal authority guidance | default |  |
| `e-zh-naturalisation-ordinary-5-1` | CH-ZH | Cantonal authority guidance | default |  |
| `e-zh-naturalisation-ordinary-6-1` | CH-ZH | Cantonal authority guidance | default |  |
| `e-zh-naturalisation-ordinary-7-1` | CH-ZH | Cantonal authority guidance | default |  |
| `e-zh-naturalisation-ordinary-9-1` | CH-ZH | Cantonal authority guidance | default |  |
| `e-zh-naturalisation-ordinary-10-1` | CH-ZH | Cantonal authority guidance | default |  |
| `e-zh-naturalisation-ordinary-12-1` | CH-ZH | Cantonal authority guidance | default |  |
| `e-zh-naturalisation-ordinary-13-1` | CH-ZH | Cantonal authority guidance | default |  |

### Prämienverbilligung Krankenversicherung | Kanton Zürich

Publisher: Canton of Zurich, Health Directorate (cantonal, CH-ZH); attributed by rule `www.zh.ch/de/gesundheit/`; page: <https://www.zh.ch/de/gesundheit/praemienverbilligung_krankenversicherung.html>

| Evidence | Fact jurisdiction | Basis | Rule | Refers to |
| --- | --- | --- | --- | --- |
| `e-zh-health-insurance-exemption-1-1` | CH-ZH | Cantonal authority guidance | default |  |
| `e-zh-premium-reduction-1-1` | CH-ZH | Cantonal authority guidance | default |  |
| `e-zh-premium-reduction-2-1` | CH-ZH | Cantonal authority guidance | default |  |
| `e-zh-premium-reduction-3-1` | CH-ZH | Cantonal authority guidance | default |  |

### Aufenthalt für EU/EFTA-Staatsangehörige | Kanton Zürich

Publisher: Canton of Zurich, Migration Office (cantonal, CH-ZH); attributed by rule `www.zh.ch/de/migration-integration/`; page: <https://www.zh.ch/de/migration-integration/aufenthalt/aufenthalt-fuer-euefta-staatsangehoerige.html>

| Evidence | Fact jurisdiction | Basis | Rule | Refers to |
| --- | --- | --- | --- | --- |
| `e-zh-eu-registration-1-1` | CH-ZH | Cantonal authority guidance | default |  |
| `e-zh-eu-registration-2-1` | CH-ZH | Cantonal authority guidance | default |  |
| `e-zh-eu-l-1-1` | CH-ZH | Cantonal authority guidance | default |  |
| `e-zh-eu-b-1-1` | CH-ZH | Cantonal authority guidance | default |  |
| `e-zh-eu-self-employment-1-1` | CH-ZH | Cantonal authority guidance | default |  |
| `e-zh-eu-nonworking-1-1` | CH-ZH | Cantonal authority guidance | default | Weisung des Migrationsamts zum Freizügigkeitsabkommen EU/EFTA |
| `e-zh-eu-family-documents-1-1` | CH-ZH | Cantonal authority guidance | default |  |

### Aufenthalt ohne Erwerbstätigkeit für Drittstaatsangehörige | Kanton Zürich

Publisher: Canton of Zurich, Migration Office (cantonal, CH-ZH); attributed by rule `www.zh.ch/de/migration-integration/`; page: <https://www.zh.ch/de/migration-integration/aufenthalt/aufenthalt-ohne-erwerbstaetigkeit-fuer-drittstaatsangehoerige.html>

| Evidence | Fact jurisdiction | Basis | Rule | Refers to |
| --- | --- | --- | --- | --- |
| `e-zh-third-country-retirement-1-1` | CH-ZH | Cantonal authority guidance | default |  |

### Merkblatt des kantonalen Steueramtes über die Quellenbesteuerung von Arbeitnehmerinnen und Arbeitnehmern | Kanton Zürich

Publisher: Canton of Zurich, Cantonal Tax Office (cantonal, CH-ZH); attributed by rule `www.zh.ch/de/steuern-finanzen/`; page: <https://www.zh.ch/de/steuern-finanzen/steuern/treuhaender/steuerbuch/steuerbuch-definition/zstb-87-3.html>

| Evidence | Fact jurisdiction | Basis | Rule | Refers to |
| --- | --- | --- | --- | --- |
| `e-zh-tax-at-source-liability-7-1` | CH-ZH | Cantonal directive: Zürcher Steuerbuch 87.3, Rz 24 | citation |  |
| `e-zh-tax-at-source-ordinary-assessment-8-1` | CH-ZH | Cantonal directive: Zürcher Steuerbuch 87.3, Rz 13 Abs. 1 | citation | StG ZH, LS 631.1, § 87 Abs. 1 |
| `e-zh-tax-at-source-ordinary-assessment-9-1` | CH-ZH | Cantonal directive: Zürcher Steuerbuch 87.3, Rz 13 Abs. 3 | citation |  |
| `e-zh-tax-at-source-ordinary-assessment-10-1` | CH-ZH | Cantonal directive: Zürcher Steuerbuch 87.3, Rz 13 Abs. 4 | citation |  |
| `e-zh-tax-at-source-ordinary-assessment-11-1` | CH-ZH | Cantonal directive: Zürcher Steuerbuch 87.3, Rz 15 Abs. 1 | citation | StG ZH, LS 631.1, § 87 Abs. 1 |
| `e-zh-tax-at-source-ordinary-assessment-11-2` | CH-ZH | Cantonal directive: Zürcher Steuerbuch 87.3, Rz 15 Abs. 5 | citation |  |
| `e-zh-tax-at-source-ordinary-assessment-12-1` | CH-ZH | Cantonal directive: Zürcher Steuerbuch 87.3, Rz 15 Abs. 4 | citation |  |

### Nachträgliche ordentliche Veranlagung beantragen | Kanton Zürich

Publisher: Canton of Zurich, Cantonal Tax Office (cantonal, CH-ZH); attributed by rule `www.zh.ch/de/steuern-finanzen/`; page: <https://www.zh.ch/de/steuern-finanzen/steuern/quellensteuer/nachtraegliche-ordentliche-veranlagung-oder-quellensteuerkorrekt.html>

| Evidence | Fact jurisdiction | Basis | Rule | Refers to |
| --- | --- | --- | --- | --- |
| `e-zh-tax-at-source-ordinary-assessment-4-1` | CH-ZH | Cantonal authority guidance | default |  |
| `e-zh-tax-at-source-ordinary-assessment-5-1` | CH-ZH | Cantonal authority guidance | default |  |
| `e-zh-tax-at-source-ordinary-assessment-6-1` | CH-ZH | Cantonal authority guidance | default |  |

### Quellensteuerpflichtige Personen | Kanton Zürich

Publisher: Canton of Zurich, Cantonal Tax Office (cantonal, CH-ZH); attributed by rule `www.zh.ch/de/steuern-finanzen/`; page: <https://www.zh.ch/de/steuern-finanzen/steuern/quellensteuer/Quellensteuerpflichtige-Personen.html>

| Evidence | Fact jurisdiction | Basis | Rule | Refers to |
| --- | --- | --- | --- | --- |
| `e-zh-tax-at-source-liability-1-1` | CH-ZH | Cantonal authority guidance | default |  |
| `e-zh-tax-at-source-liability-2-1` | CH-ZH | Cantonal authority guidance | default |  |
| `e-zh-tax-at-source-liability-3-1` | CH-ZH | Cantonal authority guidance | default |  |
| `e-zh-tax-at-source-liability-4-1` | CH-ZH | Cantonal authority guidance | default |  |
| `e-zh-tax-at-source-liability-5-1` | CH-ZH | Cantonal authority guidance | default |  |
| `e-zh-tax-at-source-liability-6-1` | CH-ZH | Cantonal authority guidance | default |  |
| `e-zh-tax-at-source-ordinary-assessment-1-1` | CH-ZH | Cantonal authority guidance | default |  |
| `e-zh-tax-at-source-ordinary-assessment-2-1` | CH-ZH | Cantonal authority guidance | default |  |
| `e-zh-tax-at-source-ordinary-assessment-3-1` | CH-ZH | Cantonal authority guidance | default |  |
| `e-zh-tax-at-source-ordinary-assessment-7-1` | CH-ZH | Cantonal authority guidance | default |  |

### Ausländischen Führerausweis umtauschen | Kanton Zürich

Publisher: Canton of Zurich, Road Traffic Office (cantonal, CH-ZH); attributed by rule `www.zh.ch/de/mobilitaet/`; page: <https://www.zh.ch/de/mobilitaet/fuehrerausweis-fahren-lernen/auslaendischer-fuehrerausweis/auslaendischen-fuehrerausweis-umtauschen.html>

| Evidence | Fact jurisdiction | Basis | Rule | Refers to |
| --- | --- | --- | --- | --- |
| `e-zh-foreign-licence-exchange-6-1` | CH-ZH | Cantonal authority guidance | default |  |
| `e-zh-foreign-licence-exchange-7-1` | CH-ZH | Cantonal authority guidance | default |  |
| `e-zh-foreign-licence-exchange-8-1` | CH-ZH | Cantonal authority guidance | default |  |
| `e-zh-control-drive-1-1` | CH-ZH | Cantonal authority guidance | default |  |
| `e-zh-control-drive-2-1` | CH-ZH | Cantonal authority guidance | default |  |
| `e-zh-control-drive-3-1` | CH-ZH | Cantonal authority guidance | default |  |

### So bereiten Sie sich gut auf Ihre Kontrollfahrt vor | Kanton Zürich

Publisher: Canton of Zurich, Road Traffic Office (cantonal, CH-ZH); attributed by rule `www.zh.ch/de/mobilitaet/`; page: <https://www.zh.ch/de/mobilitaet/fuehrerausweis-fahren-lernen/auslaendischer-fuehrerausweis/so-bereiten-sie-sich-gut-auf-ihre-kontrollfahrt-vor.html>

| Evidence | Fact jurisdiction | Basis | Rule | Refers to |
| --- | --- | --- | --- | --- |
| `e-zh-control-drive-4-1` | CH-ZH | Cantonal authority guidance | default |  |
| `e-zh-control-drive-5-1` | CH-ZH | Cantonal authority guidance | default |  |
| `e-zh-control-drive-6-1` | CH-ZH | Cantonal authority guidance | default |  |
| `e-zh-control-drive-7-1` | CH-ZH | Cantonal authority guidance | default |  |

### Umtausch eines ausländischen Führerausweises | Kanton Zürich

Publisher: Canton of Zurich, Road Traffic Office (cantonal, CH-ZH); attributed by rule `www.zh.ch/de/mobilitaet/`; page: <https://www.zh.ch/de/mobilitaet/fuehrerausweis-fahren-lernen/auslaendischer-fuehrerausweis.html>

| Evidence | Fact jurisdiction | Basis | Rule | Refers to |
| --- | --- | --- | --- | --- |
| `e-zh-foreign-licence-exchange-1-1` | CH-ZH | Cantonal authority guidance | default |  |
| `e-zh-foreign-licence-exchange-2-1` | CH-ZH | Cantonal authority guidance | default |  |
| `e-zh-foreign-licence-exchange-3-1` | CH-ZH | Cantonal authority guidance | default |  |
| `e-zh-foreign-licence-exchange-4-1` | CH-ZH | Cantonal authority guidance | default |  |
| `e-zh-foreign-licence-exchange-5-1` | CH-ZH | Cantonal authority guidance | default |  |
| `e-zh-foreign-licence-exchange-9-1` | CH-ZH | Cantonal authority guidance | default |  |
| `e-zh-foreign-licence-exchange-10-1` | CH-ZH | Cantonal authority guidance | default |  |
| `e-zh-foreign-licence-exchange-11-1` | CH-ZH | Cantonal authority guidance | default |  |
| `e-zh-foreign-licence-exchange-11-2` | CH-ZH | Cantonal authority guidance | default |  |

### Krankenversicherungspflicht: Wer kann sich befreien lassen?

Publisher: SVA Zürich, the cantonal social insurance office (cantonal, CH-ZH); attributed by rule `svazurich.ch`; page: <https://svazurich.ch/unsere-produkte/weitere-produkte/krankenversicherung--kvg-/krankenversicherungspflicht0/krankenversicherungspflicht-wer-hat-anspruch.html>

| Evidence | Fact jurisdiction | Basis | Rule | Refers to |
| --- | --- | --- | --- | --- |
| `e-zh-health-insurance-exemption-2-1` | CH-ZH | Cantonal authority guidance | default | KVG, SR 832.10 |
| `e-zh-health-insurance-exemption-3-1` | CH-ZH | Cantonal authority guidance | default |  |
| `e-zh-health-insurance-exemption-4-1` | CH-ZH | Cantonal authority guidance | default | KVG, SR 832.10 |
| `e-zh-health-insurance-exemption-5-1` | CH-ZH | Cantonal authority guidance | default |  |

### Prämienverbilligung: Wer hat Anspruch?

Publisher: SVA Zürich, the cantonal social insurance office (cantonal, CH-ZH); attributed by rule `svazurich.ch`; page: <https://svazurich.ch/unsere-produkte/weitere-produkte/krankenversicherung--kvg-/praemienverbilligung/wer-hat-anspruch-.html>

| Evidence | Fact jurisdiction | Basis | Rule | Refers to |
| --- | --- | --- | --- | --- |
| `e-zh-premium-reduction-4-1` | CH-ZH | Cantonal authority guidance | default |  |
| `e-zh-premium-reduction-5-1` | CH-ZH | Cantonal authority guidance | default |  |
| `e-zh-premium-reduction-6-1` | CH-ZH | Cantonal authority guidance | default |  |
| `e-zh-premium-reduction-7-1` | CH-ZH | Cantonal authority guidance | default |  |
| `e-zh-premium-reduction-8-1` | CH-ZH | Cantonal authority guidance | default |  |

### Erleichterte Einbürgerung | Stadt Zürich

Publisher: City of Zurich, Naturalisation Division (municipal, CH-ZH-261); attributed by rule `www.stadt-zuerich.ch/de/lebenslagen/einwohner-services/einbuergerung`; page: <https://www.stadt-zuerich.ch/de/lebenslagen/einwohner-services/einbuergerung/erleichterte-einbuergerung.html>

| Evidence | Fact jurisdiction | Basis | Rule | Refers to |
| --- | --- | --- | --- | --- |
| `e-city-zurich-naturalisation-facilitated-1-1` | CH-ZH-261 | Municipal authority guidance | default |  |
| `e-city-zurich-naturalisation-facilitated-2-1` | CH-ZH-261 | Municipal authority guidance | default |  |
| `e-city-zurich-naturalisation-facilitated-3-1` | CH-ZH-261 | Municipal authority guidance | default |  |
| `e-city-zurich-naturalisation-facilitated-4-1` | CH-ZH-261 | Municipal authority guidance | default |  |
| `e-city-zurich-naturalisation-facilitated-5-1` | CH-ZH-261 | Municipal authority guidance | default |  |
| `e-city-zurich-naturalisation-facilitated-6-1` | CH-ZH-261 | Municipal authority guidance | default |  |

### Ordentliche Einbürgerung | Stadt Zürich

Publisher: City of Zurich, Naturalisation Division (municipal, CH-ZH-261); attributed by rule `www.stadt-zuerich.ch/de/lebenslagen/einwohner-services/einbuergerung`; page: <https://www.stadt-zuerich.ch/de/lebenslagen/einwohner-services/einbuergerung/ordentliche-einbuergerung.html>

| Evidence | Fact jurisdiction | Basis | Rule | Refers to |
| --- | --- | --- | --- | --- |
| `e-city-zurich-naturalisation-1-1` | CH-ZH-261 | Municipal authority guidance | default |  |
| `e-city-zurich-naturalisation-2-1` | CH-ZH-261 | Municipal authority guidance | default |  |
| `e-city-zurich-naturalisation-3-1` | CH-ZH-261 | Municipal authority guidance | default |  |
| `e-city-zurich-naturalisation-4-1` | CH-ZH-261 | Municipal authority guidance | default |  |
| `e-city-zurich-naturalisation-5-1` | CH-ZH-261 | Municipal authority guidance | default |  |
| `e-city-zurich-naturalisation-6-1` | CH-ZH-261 | Municipal authority guidance | default |  |
| `e-city-zurich-naturalisation-7-1` | CH-ZH-261 | Municipal authority guidance | default |  |

### Zuzug in die Stadt Zürich | Stadt Zürich

Publisher: City of Zurich, Population Office (municipal, CH-ZH-261); attributed by rule `www.stadt-zuerich.ch/de/lebenslagen/einwohner-services/umziehen-melden/`; page: <https://www.stadt-zuerich.ch/de/lebenslagen/einwohner-services/umziehen-melden/zuzug.html>

| Evidence | Fact jurisdiction | Basis | Rule | Refers to |
| --- | --- | --- | --- | --- |
| `e-city-zurich-arrival-1-1` | CH-ZH-261 | Municipal authority guidance | default |  |
| `e-city-zurich-arrival-documents-1-1` | CH-ZH-261 | Municipal authority guidance | default |  |

## Office-contact excerpts (17 September 2026)

53 excerpts: 49 directory, 4 guidance. A `directory` label was set on the citation where the excerpt is an office's own contact entry (address, hours, telephone, e-mail, location list); the four excerpts of the City of Zurich appointment rules keep the page default, municipal guidance.

### Abteilung Einbürgerungen | Kanton Zürich

Canton of Zurich, Office for Municipalities, Naturalisation Division, <https://www.zh.ch/de/direktion-der-justiz-und-des-innern/gemeindeamt/abteilung-einbuergerungen.html>

| Evidence | Fact jurisdiction | Basis | Rule |
| --- | --- | --- | --- |
| `e-zh-naturalisation-division-contact-1-1` | CH-ZH | Cantonal authority directory | citation |
| `e-zh-naturalisation-division-contact-2-1` | CH-ZH | Cantonal authority directory | citation |
| `e-zh-naturalisation-division-contact-3-1` | CH-ZH | Cantonal authority directory | citation |
| `e-zh-naturalisation-division-contact-4-1` | CH-ZH | Cantonal authority directory | citation |

### Amt für Wirtschaft | Kanton Zürich

Canton of Zurich, Office for the Economy, <https://www.zh.ch/de/volkswirtschaftsdirektion/amt-fuer-wirtschaft.html>

| Evidence | Fact jurisdiction | Basis | Rule |
| --- | --- | --- | --- |
| `e-zh-economy-office-contact-1-1` | CH-ZH | Cantonal authority directory | citation |

### Beratung vor Ort

SVA Zürich, the cantonal social insurance office, <https://svazurich.ch/ueber-uns/sva-zuerich/kontakt/beratung-vor-ort.html>

| Evidence | Fact jurisdiction | Basis | Rule |
| --- | --- | --- | --- |
| `e-zh-sva-contact-1-1` | CH-ZH | Cantonal authority directory | citation |
| `e-zh-sva-contact-1-2` | CH-ZH | Cantonal authority directory | citation |
| `e-zh-sva-contact-2-1` | CH-ZH | Cantonal authority directory | citation |

### Einbürgerung und Stadtbürgerrecht | Stadt Zürich

City of Zurich, Naturalisation Division, <https://www.stadt-zuerich.ch/de/lebenslagen/einwohner-services/einbuergerung.html>

| Evidence | Fact jurisdiction | Basis | Rule |
| --- | --- | --- | --- |
| `e-city-zurich-naturalisation-contact-1-1` | CH-ZH-261 | Municipal authority directory | citation |
| `e-city-zurich-naturalisation-contact-1-2` | CH-ZH-261 | Municipal authority directory | citation |
| `e-city-zurich-naturalisation-contact-2-1` | CH-ZH-261 | Municipal authority directory | citation |

### Erwerbstätigkeit von Ausländerinnen und Ausländern | Kanton Zürich

Canton of Zurich, Office for the Economy, <https://www.zh.ch/de/wirtschaft-arbeit/erwerbstaetigkeit-auslaender.html>

| Evidence | Fact jurisdiction | Basis | Rule |
| --- | --- | --- | --- |
| `e-zh-economy-office-contact-2-1` | CH-ZH | Cantonal authority directory | citation |
| `e-zh-economy-office-contact-3-1` | CH-ZH | Cantonal authority directory | citation |

### Kontakt

SVA Zürich, the cantonal social insurance office, <https://svazurich.ch/ueber-uns/sva-zuerich/kontakt.html>

| Evidence | Fact jurisdiction | Basis | Rule |
| --- | --- | --- | --- |
| `e-zh-sva-contact-6-1` | CH-ZH | Cantonal authority directory | citation |

### Migrationsamt | Kanton Zürich

Canton of Zurich, Migration Office, <https://www.zh.ch/de/sicherheitsdirektion/migrationsamt.html>

| Evidence | Fact jurisdiction | Basis | Rule |
| --- | --- | --- | --- |
| `e-zh-migrationsamt-contact-1-1` | CH-ZH | Cantonal authority directory | citation |
| `e-zh-migrationsamt-contact-1-2` | CH-ZH | Cantonal authority directory | citation |
| `e-zh-migrationsamt-contact-2-1` | CH-ZH | Cantonal authority directory | citation |
| `e-zh-migrationsamt-contact-3-1` | CH-ZH | Cantonal authority directory | citation |

### Organisation | Kanton Zürich

Canton of Zurich, Migration Office, <https://www.zh.ch/de/sicherheitsdirektion/migrationsamt/organisation.html>

| Evidence | Fact jurisdiction | Basis | Rule |
| --- | --- | --- | --- |
| `e-zh-migrationsamt-contact-4-1` | CH-ZH | Cantonal authority directory | citation |

### Quellensteuer | Kanton Zürich

Canton of Zurich, Cantonal Tax Office, <https://www.zh.ch/de/steuern-finanzen/steuern/quellensteuer.html>

| Evidence | Fact jurisdiction | Basis | Rule |
| --- | --- | --- | --- |
| `e-zh-tax-office-contact-2-1` | CH-ZH | Cantonal authority directory | citation |

### Spezielle Öffnungszeiten

SVA Zürich, the cantonal social insurance office, <https://svazurich.ch/ueber-uns/sva-zuerich/kontakt/oeffnungszeiten-ueber-die-feiertage.html>

| Evidence | Fact jurisdiction | Basis | Rule |
| --- | --- | --- | --- |
| `e-zh-sva-contact-6-2` | CH-ZH | Cantonal authority directory | citation |
| `e-zh-sva-contact-7-1` | CH-ZH | Cantonal authority directory | citation |

### Standorte und Öffnungszeiten des Strassenverkehrsamts | Kanton Zürich

Canton of Zurich, Road Traffic Office, <https://www.zh.ch/de/sicherheitsdirektion/strassenverkehrsamt/standorte-oeffnungszeiten.html>

| Evidence | Fact jurisdiction | Basis | Rule |
| --- | --- | --- | --- |
| `e-zh-road-traffic-office-locations-10-1` | CH-ZH | Cantonal authority directory | citation |
| `e-zh-road-traffic-office-locations-10-2` | CH-ZH | Cantonal authority directory | citation |
| `e-zh-road-traffic-office-locations-11-1` | CH-ZH | Cantonal authority directory | citation |
| `e-zh-road-traffic-office-locations-11-2` | CH-ZH | Cantonal authority directory | citation |
| `e-zh-road-traffic-office-locations-12-1` | CH-ZH | Cantonal authority directory | citation |
| `e-zh-road-traffic-office-locations-13-1` | CH-ZH | Cantonal authority directory | citation |
| `e-zh-road-traffic-office-locations-14-1` | CH-ZH | Cantonal authority directory | citation |
| `e-zh-road-traffic-office-locations-2-2` | CH-ZH | Cantonal authority directory | citation |
| `e-zh-road-traffic-office-locations-3-1` | CH-ZH | Cantonal authority directory | citation |
| `e-zh-road-traffic-office-locations-3-2` | CH-ZH | Cantonal authority directory | citation |
| `e-zh-road-traffic-office-locations-4-1` | CH-ZH | Cantonal authority directory | citation |
| `e-zh-road-traffic-office-locations-5-1` | CH-ZH | Cantonal authority directory | citation |
| `e-zh-road-traffic-office-locations-6-1` | CH-ZH | Cantonal authority directory | citation |
| `e-zh-road-traffic-office-locations-7-1` | CH-ZH | Cantonal authority directory | citation |
| `e-zh-road-traffic-office-locations-8-1` | CH-ZH | Cantonal authority directory | citation |
| `e-zh-road-traffic-office-locations-9-1` | CH-ZH | Cantonal authority directory | citation |

### Steueramt | Kanton Zürich

Canton of Zurich, Cantonal Tax Office, <https://www.zh.ch/de/finanzdirektion/steueramt.html>

| Evidence | Fact jurisdiction | Basis | Rule |
| --- | --- | --- | --- |
| `e-zh-tax-office-contact-1-1` | CH-ZH | Cantonal authority directory | citation |

### Strassenverkehrsamt | Kanton Zürich

Canton of Zurich, Road Traffic Office, <https://www.zh.ch/de/sicherheitsdirektion/strassenverkehrsamt.html>

| Evidence | Fact jurisdiction | Basis | Rule |
| --- | --- | --- | --- |
| `e-zh-road-traffic-office-locations-1-1` | CH-ZH | Cantonal authority directory | citation |
| `e-zh-road-traffic-office-locations-2-1` | CH-ZH | Cantonal authority directory | citation |

### Telefon

SVA Zürich, the cantonal social insurance office, <https://svazurich.ch/ueber-uns/sva-zuerich/kontakt/telefon.html>

| Evidence | Fact jurisdiction | Basis | Rule |
| --- | --- | --- | --- |
| `e-zh-sva-contact-3-1` | CH-ZH | Cantonal authority directory | citation |
| `e-zh-sva-telephone-numbers-1-1` | CH-ZH | Cantonal authority directory | citation |
| `e-zh-sva-telephone-numbers-1-2` | CH-ZH | Cantonal authority directory | citation |
| `e-zh-sva-telephone-numbers-2-1` | CH-ZH | Cantonal authority directory | citation |

### Terminpflicht beim Personenmeldeamt | Stadt Zürich

City of Zurich, Population Office, <https://www.stadt-zuerich.ch/de/lebenslagen/einwohner-services/online-schalter/personenmeldeamt-terminpflicht.html>

| Evidence | Fact jurisdiction | Basis | Rule |
| --- | --- | --- | --- |
| `e-city-zurich-population-office-1-1` | CH-ZH-261 | Municipal authority directory | citation |
| `e-city-zurich-population-office-2-1` | CH-ZH-261 | Municipal authority guidance | default |
| `e-city-zurich-population-office-2-2` | CH-ZH-261 | Municipal authority guidance | default |
| `e-city-zurich-population-office-3-1` | CH-ZH-261 | Municipal authority guidance | default |
| `e-city-zurich-population-office-4-1` | CH-ZH-261 | Municipal authority guidance | default |
| `e-city-zurich-population-office-5-1` | CH-ZH-261 | Municipal authority directory | citation |
| `e-city-zurich-population-office-5-2` | CH-ZH-261 | Municipal authority directory | citation |

### Zuzug in die Stadt Zürich | Stadt Zürich

City of Zurich, Population Office, <https://www.stadt-zuerich.ch/de/lebenslagen/einwohner-services/umziehen-melden/zuzug.html>

| Evidence | Fact jurisdiction | Basis | Rule |
| --- | --- | --- | --- |
| `e-city-zurich-population-office-1-2` | CH-ZH-261 | Municipal authority directory | citation |

## Daily-life excerpts (17 September 2026)

132 excerpts of the 18 daily-life concepts and the three City of Zurich naturalisation facts read from data tables: 18 directory, 114 guidance. The assistant set a `directory` label on the citation where the excerpt is an office's own contact entry (address, hours, telephone, closing days); the other excerpts keep the page default, the guidance of the authority that wrote the page. No person has reviewed these labels.

### Abfuhr Bioabfall | Stadt Zürich

City of Zurich, Waste Disposal and Recycling (ERZ), <https://www.stadt-zuerich.ch/de/umwelt-und-energie/entsorgung/wo-und-wann-entsorgen/abfuhr-bioabfall.html>

| Evidence | Fact jurisdiction | Basis | Rule |
| --- | --- | --- | --- |
| `e-city-zurich-organic-paper-cardboard-1-1` | CH-ZH-261 | Municipal authority guidance | default |
| `e-city-zurich-organic-paper-cardboard-2-1` | CH-ZH-261 | Municipal authority guidance | default |
| `e-city-zurich-organic-paper-cardboard-3-1` | CH-ZH-261 | Municipal authority guidance | default |
| `e-city-zurich-organic-paper-cardboard-3-2` | CH-ZH-261 | Municipal authority guidance | default |

### Abfuhr Hauskehricht | Stadt Zürich

City of Zurich, Waste Disposal and Recycling (ERZ), <https://www.stadt-zuerich.ch/de/umwelt-und-energie/entsorgung/wo-und-wann-entsorgen/abfuhr-hauskehricht.html>

| Evidence | Fact jurisdiction | Basis | Rule |
| --- | --- | --- | --- |
| `e-city-zurich-household-waste-1-1` | CH-ZH-261 | Municipal authority guidance | default |
| `e-city-zurich-household-waste-3-1` | CH-ZH-261 | Municipal authority guidance | default |
| `e-city-zurich-household-waste-4-1` | CH-ZH-261 | Municipal authority guidance | default |
| `e-city-zurich-household-waste-6-1` | CH-ZH-261 | Municipal authority directory | citation |
| `e-city-zurich-household-waste-7-1` | CH-ZH-261 | Municipal authority guidance | default |

### Abfuhr Sperrgut, Metall, Elektrogeräte und Grubengut | Stadt Zürich

City of Zurich, Waste Disposal and Recycling (ERZ), <https://www.stadt-zuerich.ch/de/umwelt-und-energie/entsorgung/wo-und-wann-entsorgen/abfuhr-sperrgut-metall-elektro-grubengut.html>

| Evidence | Fact jurisdiction | Basis | Rule |
| --- | --- | --- | --- |
| `e-city-zurich-bulky-waste-pickup-1-1` | CH-ZH-261 | Municipal authority guidance | default |
| `e-city-zurich-bulky-waste-pickup-2-1` | CH-ZH-261 | Municipal authority guidance | default |
| `e-city-zurich-bulky-waste-pickup-2-2` | CH-ZH-261 | Municipal authority guidance | default |
| `e-city-zurich-bulky-waste-pickup-3-1` | CH-ZH-261 | Municipal authority guidance | default |
| `e-city-zurich-bulky-waste-pickup-3-2` | CH-ZH-261 | Municipal authority guidance | default |

### Abgabeübersicht

SERAFE AG, the Confederation's collection agency for the radio and television fee, <https://www.serafe.ch/de/abgabe/abgabeuebersicht/>

| Evidence | Fact jurisdiction | Basis | Rule |
| --- | --- | --- | --- |
| `e-radio-tv-household-fee-1-1` | CH | Federal authority guidance | default |
| `e-radio-tv-household-fee-2-1` | CH | Federal authority guidance | default |

### Anmeldung eines Hundes bei der Wohngemeinde | Stadt Zürich

City of Zurich, City Police, <https://www.stadt-zuerich.ch/de/stadtleben/veranstaltungen-und-bewilligungen/hundekontrolle/anmeldung.html>

| Evidence | Fact jurisdiction | Basis | Rule |
| --- | --- | --- | --- |
| `e-city-zurich-dog-registration-2-1` | CH-ZH-261 | Municipal authority guidance | default |
| `e-city-zurich-dog-registration-2-2` | CH-ZH-261 | Municipal authority guidance | default |
| `e-city-zurich-dog-registration-4-1` | CH-ZH-261 | Municipal authority guidance | default |

### Anwohnerparkkarte für Privatpersonen und Firmen | Stadt Zürich

City of Zurich, Traffic Department, <https://www.stadt-zuerich.ch/de/mobilitaet/parkieren/parkbewilligungen/anwohnerparkkarte.html>

| Evidence | Fact jurisdiction | Basis | Rule |
| --- | --- | --- | --- |
| `e-city-zurich-parking-permits-3-1` | CH-ZH-261 | Municipal authority guidance | default |
| `e-city-zurich-parking-permits-3-2` | CH-ZH-261 | Municipal authority guidance | default |

### Einbürgerung und Stadtbürgerrecht | Stadt Zürich

City of Zurich, Naturalisation Division, <https://www.stadt-zuerich.ch/de/lebenslagen/einwohner-services/einbuergerung.html>

| Evidence | Fact jurisdiction | Basis | Rule |
| --- | --- | --- | --- |
| `e-city-zurich-naturalisation-contact-3-1` | CH-ZH-261 | Municipal authority directory | citation |

### Einschulung | Stadt Zürich

City of Zurich, School Office, <https://www.stadt-zuerich.ch/de/bildung/volksschule/schullaufbahn/einschulung.html>

| Evidence | Fact jurisdiction | Basis | Rule |
| --- | --- | --- | --- |
| `e-city-zurich-kindergarten-1-2` | CH-ZH-261 | Municipal authority guidance | default |
| `e-city-zurich-kindergarten-3-2` | CH-ZH-261 | Municipal authority guidance | default |
| `e-city-zurich-kindergarten-3-3` | CH-ZH-261 | Municipal authority guidance | default |
| `e-city-zurich-kindergarten-4-1` | CH-ZH-261 | Municipal authority guidance | default |
| `e-city-zurich-kindergarten-5-1` | CH-ZH-261 | Municipal authority guidance | default |
| `e-city-zurich-kindergarten-7-1` | CH-ZH-261 | Municipal authority guidance | default |
| `e-city-zurich-kindergarten-7-2` | CH-ZH-261 | Municipal authority guidance | default |

### Entsorgungskalender | Stadt Zürich

City of Zurich, Waste Disposal and Recycling (ERZ), <https://www.stadt-zuerich.ch/de/umwelt-und-energie/entsorgung/entsorgungskalender.html>

| Evidence | Fact jurisdiction | Basis | Rule |
| --- | --- | --- | --- |
| `e-city-zurich-hazardous-waste-3-2` | CH-ZH-261 | Municipal authority guidance | default |
| `e-city-zurich-household-waste-5-1` | CH-ZH-261 | Municipal authority guidance | default |
| `e-city-zurich-household-waste-5-2` | CH-ZH-261 | Municipal authority guidance | default |
| `e-city-zurich-household-waste-5-3` | CH-ZH-261 | Municipal authority guidance | default |

### Erleichterte Einbürgerung | Stadt Zürich

City of Zurich, Naturalisation Division, <https://www.stadt-zuerich.ch/de/lebenslagen/einwohner-services/einbuergerung/erleichterte-einbuergerung.html>

| Evidence | Fact jurisdiction | Basis | Rule |
| --- | --- | --- | --- |
| `e-city-zurich-naturalisation-facilitated-7-1` | CH-ZH-261 | Municipal authority guidance | default |

### Erste Schritte | Stadt Zürich

City of Zurich, Population Office, <https://www.stadt-zuerich.ch/de/lebenslagen/neu-in-zuerich/erste-schritte.html>

| Evidence | Fact jurisdiction | Basis | Rule |
| --- | --- | --- | --- |
| `e-city-zurich-dog-registration-1-2` | CH-ZH-261 | Municipal authority guidance | default |
| `e-city-zurich-first-steps-1-1` | CH-ZH-261 | Municipal authority guidance | default |
| `e-city-zurich-first-steps-2-1` | CH-ZH-261 | Municipal authority guidance | default |
| `e-city-zurich-first-steps-3-1` | CH-ZH-261 | Municipal authority guidance | default |
| `e-city-zurich-first-steps-4-1` | CH-ZH-261 | Municipal authority guidance | default |
| `e-city-zurich-first-steps-5-1` | CH-ZH-261 | Municipal authority guidance | default |
| `e-city-zurich-first-steps-6-1` | CH-ZH-261 | Municipal authority guidance | default |
| `e-city-zurich-first-steps-7-1` | CH-ZH-261 | Municipal authority guidance | default |

### Fahrzeug importieren | Kanton Zürich

Canton of Zurich, Road Traffic Office, <https://www.zh.ch/de/mobilitaet/fahrzeuge-kontrollschilder/import-fahrzeuge/fahrzeug-importieren.html>

| Evidence | Fact jurisdiction | Basis | Rule |
| --- | --- | --- | --- |
| `e-zh-vehicle-registration-move-4-1` | CH-ZH | Cantonal authority guidance | default |
| `e-zh-vehicle-registration-move-4-2` | CH-ZH | Cantonal authority guidance | default |
| `e-zh-vehicle-registration-move-5-1` | CH-ZH | Cantonal authority guidance | default |
| `e-zh-vehicle-registration-move-5-2` | CH-ZH | Cantonal authority guidance | default |

### Grundsatz

SERAFE AG, the Confederation's collection agency for the radio and television fee, <https://www.serafe.ch/de/abgabebefreiung/grundsatz/>

| Evidence | Fact jurisdiction | Basis | Rule |
| --- | --- | --- | --- |
| `e-radio-tv-household-fee-1-2` | CH | Federal authority guidance | default |
| `e-radio-tv-household-fee-3-1` | CH | Federal authority guidance | default |

### Hunde | Kanton Zürich

Canton of Zurich, Veterinary Office, <https://www.zh.ch/de/umwelt-tiere/tiere/haustiere-heimtiere/hunde.html>

| Evidence | Fact jurisdiction | Basis | Rule |
| --- | --- | --- | --- |
| `e-zh-dog-keeping-1-1` | CH-ZH | Cantonal authority guidance | default |
| `e-zh-dog-keeping-1-2` | CH-ZH | Cantonal authority guidance | default |
| `e-zh-dog-keeping-2-1` | CH-ZH | Cantonal authority guidance | default |
| `e-zh-dog-keeping-3-1` | CH-ZH | Cantonal authority guidance | default |
| `e-zh-dog-keeping-4-1` | CH-ZH | Cantonal authority guidance | default |
| `e-zh-dog-keeping-4-2` | CH-ZH | Cantonal authority guidance | default |
| `e-zh-dog-keeping-5-1` | CH-ZH | Cantonal authority guidance | default |
| `e-zh-dog-keeping-5-2` | CH-ZH | Cantonal authority guidance | default |

### Hundekontrolle | Stadt Zürich

City of Zurich, City Police, <https://www.stadt-zuerich.ch/de/stadtleben/veranstaltungen-und-bewilligungen/hundekontrolle.html>

| Evidence | Fact jurisdiction | Basis | Rule |
| --- | --- | --- | --- |
| `e-city-zurich-dog-registration-1-1` | CH-ZH-261 | Municipal authority guidance | default |
| `e-city-zurich-dog-registration-2-3` | CH-ZH-261 | Municipal authority guidance | default |
| `e-city-zurich-dog-registration-3-1` | CH-ZH-261 | Municipal authority directory | citation |
| `e-city-zurich-dog-registration-3-2` | CH-ZH-261 | Municipal authority directory | citation |
| `e-city-zurich-dog-registration-5-1` | CH-ZH-261 | Municipal authority guidance | default |

### Kartonsammlung | Stadt Zürich

City of Zurich, Waste Disposal and Recycling (ERZ), <https://www.stadt-zuerich.ch/de/umwelt-und-energie/entsorgung/wo-und-wann-entsorgen/kartonsammlung.html>

| Evidence | Fact jurisdiction | Basis | Rule |
| --- | --- | --- | --- |
| `e-city-zurich-organic-paper-cardboard-4-1` | CH-ZH-261 | Municipal authority guidance | default |
| `e-city-zurich-organic-paper-cardboard-4-2` | CH-ZH-261 | Municipal authority guidance | default |
| `e-city-zurich-organic-paper-cardboard-6-1` | CH-ZH-261 | Municipal authority guidance | default |

### Kindergarten | Stadt Zürich

City of Zurich, School Office, <https://www.stadt-zuerich.ch/de/bildung/volksschule/schullaufbahn/kindergarten.html>

| Evidence | Fact jurisdiction | Basis | Rule |
| --- | --- | --- | --- |
| `e-city-zurich-kindergarten-1-1` | CH-ZH-261 | Municipal authority guidance | default |
| `e-city-zurich-kindergarten-2-1` | CH-ZH-261 | Municipal authority guidance | default |
| `e-city-zurich-kindergarten-3-1` | CH-ZH-261 | Municipal authority guidance | default |
| `e-city-zurich-kindergarten-6-1` | CH-ZH-261 | Municipal authority guidance | default |

### Kontakte und Öffnungszeiten des Steueramts | Stadt Zürich

City of Zurich, Tax Office, <https://www.stadt-zuerich.ch/de/lebenslagen/steuern/kontakt.html>

| Evidence | Fact jurisdiction | Basis | Rule |
| --- | --- | --- | --- |
| `e-city-zurich-tax-office-contact-1-1` | CH-ZH-261 | Municipal authority directory | citation |
| `e-city-zurich-tax-office-contact-1-2` | CH-ZH-261 | Municipal authority directory | citation |
| `e-city-zurich-tax-office-contact-2-1` | CH-ZH-261 | Municipal authority directory | citation |
| `e-city-zurich-tax-office-contact-2-2` | CH-ZH-261 | Municipal authority directory | citation |
| `e-city-zurich-tax-office-contact-3-1` | CH-ZH-261 | Municipal authority directory | citation |
| `e-city-zurich-tax-office-contact-4-1` | CH-ZH-261 | Municipal authority directory | citation |

### Kunststoffsammlung | Stadt Zürich

City of Zurich, Waste Disposal and Recycling (ERZ), <https://www.stadt-zuerich.ch/de/umwelt-und-energie/entsorgung/wo-und-wann-entsorgen/kunststoffsammlung.html>

| Evidence | Fact jurisdiction | Basis | Rule |
| --- | --- | --- | --- |
| `e-city-zurich-recycling-points-4-1` | CH-ZH-261 | Municipal authority guidance | default |

### Medizinischer Notfall – richtig handeln | Stadt Zürich

City of Zurich, Protection and Rescue Zurich, <https://www.stadt-zuerich.ch/de/stadtleben/notfall/notfaelle/medizinischer-notfall.html>

| Evidence | Fact jurisdiction | Basis | Rule |
| --- | --- | --- | --- |
| `e-city-zurich-medical-emergency-1-1` | CH-ZH-261 | Municipal authority guidance | default |
| `e-city-zurich-medical-emergency-1-2` | CH-ZH-261 | Municipal authority guidance | default |
| `e-city-zurich-medical-emergency-1-3` | CH-ZH-261 | Municipal authority guidance | default |
| `e-city-zurich-medical-emergency-2-1` | CH-ZH-261 | Municipal authority guidance | default |
| `e-city-zurich-medical-emergency-3-1` | CH-ZH-261 | Municipal authority guidance | default |

### Ordentliche Einbürgerung | Stadt Zürich

City of Zurich, Naturalisation Division, <https://www.stadt-zuerich.ch/de/lebenslagen/einwohner-services/einbuergerung/ordentliche-einbuergerung.html>

| Evidence | Fact jurisdiction | Basis | Rule |
| --- | --- | --- | --- |
| `e-city-zurich-naturalisation-8-1` | CH-ZH-261 | Municipal authority guidance | default |

### Papiersammlung | Stadt Zürich

City of Zurich, Waste Disposal and Recycling (ERZ), <https://www.stadt-zuerich.ch/de/umwelt-und-energie/entsorgung/wo-und-wann-entsorgen/papiersammlung.html>

| Evidence | Fact jurisdiction | Basis | Rule |
| --- | --- | --- | --- |
| `e-city-zurich-organic-paper-cardboard-5-1` | CH-ZH-261 | Municipal authority guidance | default |
| `e-city-zurich-organic-paper-cardboard-5-2` | CH-ZH-261 | Municipal authority guidance | default |
| `e-city-zurich-organic-paper-cardboard-6-2` | CH-ZH-261 | Municipal authority guidance | default |

### Parkbewilligungen | Stadt Zürich

City of Zurich, Traffic Department, <https://www.stadt-zuerich.ch/de/mobilitaet/parkieren/parkbewilligungen.html>

| Evidence | Fact jurisdiction | Basis | Rule |
| --- | --- | --- | --- |
| `e-city-zurich-parking-permits-5-1` | CH-ZH-261 | Municipal authority directory | citation |
| `e-city-zurich-parking-permits-5-2` | CH-ZH-261 | Municipal authority directory | citation |
| `e-city-zurich-parking-permits-6-1` | CH-ZH-261 | Municipal authority directory | citation |

### Parkscheibe für die Blaue Zone | Stadt Zürich

City of Zurich, Traffic Department, <https://www.stadt-zuerich.ch/de/mobilitaet/parkieren/parkbewilligungen/parkscheibe.html>

| Evidence | Fact jurisdiction | Basis | Rule |
| --- | --- | --- | --- |
| `e-city-zurich-parking-permits-1-1` | CH-ZH-261 | Municipal authority guidance | default |
| `e-city-zurich-parking-permits-2-1` | CH-ZH-261 | Municipal authority guidance | default |
| `e-city-zurich-parking-permits-2-2` | CH-ZH-261 | Municipal authority guidance | default |

### Recyclinghof | Stadt Zürich

City of Zurich, Waste Disposal and Recycling (ERZ), <https://www.stadt-zuerich.ch/de/umwelt-und-energie/entsorgung/wo-und-wann-entsorgen/recyclinghof.html>

| Evidence | Fact jurisdiction | Basis | Rule |
| --- | --- | --- | --- |
| `e-city-zurich-recycling-centres-1-1` | CH-ZH-261 | Municipal authority directory | citation |
| `e-city-zurich-recycling-centres-1-2` | CH-ZH-261 | Municipal authority guidance | default |
| `e-city-zurich-recycling-centres-1-3` | CH-ZH-261 | Municipal authority guidance | default |
| `e-city-zurich-recycling-centres-2-1` | CH-ZH-261 | Municipal authority directory | citation |
| `e-city-zurich-recycling-centres-2-2` | CH-ZH-261 | Municipal authority guidance | default |
| `e-city-zurich-recycling-centres-2-3` | CH-ZH-261 | Municipal authority guidance | default |
| `e-city-zurich-recycling-centres-3-1` | CH-ZH-261 | Municipal authority guidance | default |
| `e-city-zurich-recycling-centres-4-1` | CH-ZH-261 | Municipal authority guidance | default |
| `e-city-zurich-recycling-centres-5-1` | CH-ZH-261 | Municipal authority guidance | default |
| `e-city-zurich-recycling-centres-5-2` | CH-ZH-261 | Municipal authority guidance | default |

### Schulbotschafter*innen – Volksschule in verschiedenen Sprachen erklärt | Stadt Zürich

City of Zurich, School Office, <https://www.stadt-zuerich.ch/de/bildung/volksschule/schulorganisation/verschiedene-sprachen.html>

| Evidence | Fact jurisdiction | Basis | Rule |
| --- | --- | --- | --- |
| `e-city-zurich-school-languages-1-1` | CH-ZH-261 | Municipal authority guidance | default |
| `e-city-zurich-school-languages-2-1` | CH-ZH-261 | Municipal authority directory | citation |

### Schulferien und schulfreie Tage | Stadt Zürich

City of Zurich, School Office, <https://www.stadt-zuerich.ch/de/bildung/volksschule/schulferien.html>

| Evidence | Fact jurisdiction | Basis | Rule |
| --- | --- | --- | --- |
| `e-city-zurich-school-holidays-1-1` | CH-ZH-261 | Municipal authority guidance | default |
| `e-city-zurich-school-holidays-2-1` | CH-ZH-261 | Municipal authority guidance | default |
| `e-city-zurich-school-holidays-3-1` | CH-ZH-261 | Municipal authority guidance | default |

### Sonderabfall-Sammelstelle | Stadt Zürich

City of Zurich, Waste Disposal and Recycling (ERZ), <https://www.stadt-zuerich.ch/de/umwelt-und-energie/entsorgung/wo-und-wann-entsorgen/sonderabfall-sammelstelle.html>

| Evidence | Fact jurisdiction | Basis | Rule |
| --- | --- | --- | --- |
| `e-city-zurich-hazardous-waste-1-1` | CH-ZH-261 | Municipal authority directory | citation |
| `e-city-zurich-hazardous-waste-1-2` | CH-ZH-261 | Municipal authority guidance | default |
| `e-city-zurich-hazardous-waste-2-1` | CH-ZH-261 | Municipal authority guidance | default |
| `e-city-zurich-hazardous-waste-3-1` | CH-ZH-261 | Municipal authority guidance | default |
| `e-city-zurich-household-waste-6-2` | CH-ZH-261 | Municipal authority directory | citation |

### Steuererklärung für natürliche Personen der Stadt Zürich | Stadt Zürich

City of Zurich, Tax Office, <https://www.stadt-zuerich.ch/de/lebenslagen/steuern/natuerliche-personen/steuererklaerung.html>

| Evidence | Fact jurisdiction | Basis | Rule |
| --- | --- | --- | --- |
| `e-city-zurich-tax-return-1-1` | CH-ZH-261 | Municipal authority guidance | default |
| `e-city-zurich-tax-return-2-1` | CH-ZH-261 | Municipal authority guidance | default |
| `e-city-zurich-tax-return-3-1` | CH-ZH-261 | Municipal authority guidance | default |
| `e-city-zurich-tax-return-3-2` | CH-ZH-261 | Municipal authority guidance | default |
| `e-city-zurich-tax-return-4-1` | CH-ZH-261 | Municipal authority guidance | default |
| `e-city-zurich-tax-return-5-1` | CH-ZH-261 | Municipal authority guidance | default |

### Tagesbewilligungen | Stadt Zürich

City of Zurich, Traffic Department, <https://www.stadt-zuerich.ch/de/mobilitaet/parkieren/parkbewilligungen/tagesbewilligungen.html>

| Evidence | Fact jurisdiction | Basis | Rule |
| --- | --- | --- | --- |
| `e-city-zurich-parking-permits-4-1` | CH-ZH-261 | Municipal authority guidance | default |
| `e-city-zurich-parking-permits-4-2` | CH-ZH-261 | Municipal authority guidance | default |

### Umzug innerhalb oder in den Kanton Zürich melden | Kanton Zürich

Canton of Zurich, Road Traffic Office, <https://www.zh.ch/de/mobilitaet/fahrzeuge-kontrollschilder/umzug-melden.html>

| Evidence | Fact jurisdiction | Basis | Rule |
| --- | --- | --- | --- |
| `e-zh-vehicle-registration-move-1-1` | CH-ZH | Cantonal authority guidance | default |
| `e-zh-vehicle-registration-move-1-2` | CH-ZH | Cantonal authority guidance | default |
| `e-zh-vehicle-registration-move-2-1` | CH-ZH | Cantonal authority guidance | default |
| `e-zh-vehicle-registration-move-3-1` | CH-ZH | Cantonal authority guidance | default |

### Wertstoff-Sammelstellen | Stadt Zürich

City of Zurich, Waste Disposal and Recycling (ERZ), <https://www.stadt-zuerich.ch/de/umwelt-und-energie/entsorgung/wo-und-wann-entsorgen/wertstoff-sammelstellen.html>

| Evidence | Fact jurisdiction | Basis | Rule |
| --- | --- | --- | --- |
| `e-city-zurich-recycling-points-1-1` | CH-ZH-261 | Municipal authority guidance | default |
| `e-city-zurich-recycling-points-1-2` | CH-ZH-261 | Municipal authority guidance | default |
| `e-city-zurich-recycling-points-2-1` | CH-ZH-261 | Municipal authority guidance | default |
| `e-city-zurich-recycling-points-2-2` | CH-ZH-261 | Municipal authority guidance | default |
| `e-city-zurich-recycling-points-3-1` | CH-ZH-261 | Municipal authority guidance | default |

### Wo und wann entsorgen | Stadt Zürich

City of Zurich, Waste Disposal and Recycling (ERZ), <https://www.stadt-zuerich.ch/de/umwelt-und-energie/entsorgung/wo-und-wann-entsorgen.html>

| Evidence | Fact jurisdiction | Basis | Rule |
| --- | --- | --- | --- |
| `e-city-zurich-household-waste-7-2` | CH-ZH-261 | Municipal authority guidance | default |

### Züri-Sack | Stadt Zürich

City of Zurich, Waste Disposal and Recycling (ERZ), <https://www.stadt-zuerich.ch/de/umwelt-und-energie/entsorgung/zueri-sack.html>

| Evidence | Fact jurisdiction | Basis | Rule |
| --- | --- | --- | --- |
| `e-city-zurich-household-waste-1-2` | CH-ZH-261 | Municipal authority guidance | default |
| `e-city-zurich-household-waste-2-1` | CH-ZH-261 | Municipal authority guidance | default |
| `e-city-zurich-household-waste-2-2` | CH-ZH-261 | Municipal authority guidance | default |
| `e-city-zurich-recycling-points-4-2` | CH-ZH-261 | Municipal authority guidance | default |

## Voting-rights and tax-at-source tariff excerpts (18 September 2026)

Release `mvp-zurich-2026-09-18-v9` adds the 34 excerpts of the voting-rights topic and the two tax-at-source tariff concepts. The assistant set their basis when writing the facts on 18 September 2026: the Federal Constitution's articles as a federal act, the Constitution of the Canton of Zurich's as a cantonal act (the first excerpts whose basis level, cantonal, differs from their publisher's, Fedlex), the Tax at Source Ordinance's as a federal ordinance, ch.ch as a portal summary and the rest by the page default. No person has reviewed them.

### Fedlex: Constitution of the Canton of Zurich, SR 131.211

Fedlex, the Swiss federal law collection (Federal Chancellery), <https://www.fedlex.admin.ch/eli/cc/2006/14_fga/de>

| Evidence | Fact jurisdiction | Basis | Rule |
| --- | --- | --- | --- |
| `e-zh-political-rights-1-1` | CH-ZH | Cantonal act: KV ZH, SR 131.211, Art. 22 | citation |
| `e-zh-political-rights-4-1` | CH-ZH | Cantonal act: KV ZH, SR 131.211, Art. 40 | citation |

### Fedlex: Federal Constitution, SR 101

Fedlex, the Swiss federal law collection (Federal Chancellery), <https://www.fedlex.admin.ch/eli/cc/1999/404/de>

| Evidence | Fact jurisdiction | Basis | Rule |
| --- | --- | --- | --- |
| `e-political-rights-federal-1-1` | CH | Federal act: BV, SR 101, Art. 136 | citation |
| `e-political-rights-federal-2-1` | CH | Federal act: BV, SR 101, Art. 136 | citation |
| `e-political-rights-federal-5-1` | CH | Federal act: BV, SR 101, Art. 39 | citation |

### Fedlex: Tax at Source Ordinance of the FDF, SR 642.118.2

Fedlex, the Swiss federal law collection (Federal Chancellery), <https://www.fedlex.admin.ch/eli/cc/2018/274/de>

| Evidence | Fact jurisdiction | Basis | Rule |
| --- | --- | --- | --- |
| `e-tax-at-source-tariff-codes-1-1` | CH | Federal ordinance: QStV, SR 642.118.2, Art. 1 | page rule www.fedlex.admin.ch/eli/cc/2018/274/ |
| `e-tax-at-source-tariff-codes-2-1` | CH | Federal ordinance: QStV, SR 642.118.2, Art. 1 | page rule www.fedlex.admin.ch/eli/cc/2018/274/ |
| `e-tax-at-source-tariff-codes-3-1` | CH | Federal ordinance: QStV, SR 642.118.2, Art. 1 | page rule www.fedlex.admin.ch/eli/cc/2018/274/ |
| `e-tax-at-source-tariff-codes-3-2` | CH | Federal ordinance: QStV, SR 642.118.2, Art. 1 | page rule www.fedlex.admin.ch/eli/cc/2018/274/ |
| `e-tax-at-source-tariff-codes-4-1` | CH | Federal ordinance: QStV, SR 642.118.2, Art. 1 | page rule www.fedlex.admin.ch/eli/cc/2018/274/ |

### Merkblatt des kantonalen Steueramtes über die Quellenbesteuerung von Arbeitnehmerinnen und Arbeitnehmern | Kanton Zürich

Canton of Zurich, Cantonal Tax Office, <https://www.zh.ch/de/steuern-finanzen/steuern/treuhaender/steuerbuch/steuerbuch-definition/zstb-87-3.html>

| Evidence | Fact jurisdiction | Basis | Rule |
| --- | --- | --- | --- |
| `e-zh-tax-at-source-tariffs-11-1` | CH-ZH | Cantonal directive: Zürcher Steuerbuch 87.3 | page rule www.zh.ch/de/steuern-finanzen/steuern/treuhaender/steuerbuch/ |

### Quellensteuer-Tarife | Kanton Zürich

Canton of Zurich, Cantonal Tax Office, <https://www.zh.ch/de/steuern-finanzen/steuern/quellensteuer/quellensteuer-tarife.html>

| Evidence | Fact jurisdiction | Basis | Rule |
| --- | --- | --- | --- |
| `e-zh-tax-at-source-tariffs-1-1` | CH-ZH | Cantonal authority guidance | default |
| `e-zh-tax-at-source-tariffs-12-1` | CH-ZH | Cantonal authority guidance | default |
| `e-zh-tax-at-source-tariffs-2-1` | CH-ZH | Cantonal authority guidance | default |
| `e-zh-tax-at-source-tariffs-3-1` | CH-ZH | Cantonal authority guidance | default |
| `e-zh-tax-at-source-tariffs-4-1` | CH-ZH | Cantonal authority guidance | default |
| `e-zh-tax-at-source-tariffs-4-2` | CH-ZH | Cantonal authority guidance | default |
| `e-zh-tax-at-source-tariffs-5-1` | CH-ZH | Cantonal authority guidance | default |
| `e-zh-tax-at-source-tariffs-6-1` | CH-ZH | Cantonal authority guidance | default |
| `e-zh-tax-at-source-tariffs-7-1` | CH-ZH | Cantonal authority guidance | default |
| `e-zh-tax-at-source-tariffs-7-2` | CH-ZH | Cantonal authority guidance | default |
| `e-zh-tax-at-source-tariffs-8-1` | CH-ZH | Cantonal authority guidance | default |

### Schweizerische Quellensteuer QST

Federal Tax Administration FTA, <https://www.estv.admin.ch/de/quellensteuer>

| Evidence | Fact jurisdiction | Basis | Rule |
| --- | --- | --- | --- |
| `e-tax-at-source-tariff-codes-5-1` | CH | Federal authority guidance | default |

### So stimme ich ab | Kanton Zürich

Canton of Zurich, Statistical Office, elections and votes, <https://www.zh.ch/de/politik-staat/wahlen-abstimmungen/so-stimme-ich-ab.html>

| Evidence | Fact jurisdiction | Basis | Rule |
| --- | --- | --- | --- |
| `e-zh-political-rights-2-1` | CH-ZH | Cantonal authority guidance | default |
| `e-zh-political-rights-3-1` | CH-ZH | Cantonal authority guidance | default |
| `e-zh-political-rights-5-1` | CH-ZH | Cantonal authority guidance | default |
| `e-zh-political-rights-5-2` | CH-ZH | Cantonal authority guidance | default |

### Stimm- und Wahlrecht in der Schweiz

ch.ch, the information portal of the Confederation, cantons and communes (Federal Chancellery), <https://www.ch.ch/de/abstimmungen-und-wahlen/abstimmungen/stimm-und-wahlrecht/>

| Evidence | Fact jurisdiction | Basis | Rule |
| --- | --- | --- | --- |
| `e-political-rights-federal-3-1` | CH | Portal summary of federal rules | page rule www.ch.ch |
| `e-political-rights-federal-3-2` | CH | Portal summary of federal rules | page rule www.ch.ch |
| `e-political-rights-federal-4-1` | CH | Portal summary of federal rules | page rule www.ch.ch |
| `e-political-rights-federal-6-1` | CH | Portal summary of federal rules | page rule www.ch.ch |
| `e-political-rights-federal-7-1` | CH | Portal summary of federal rules | page rule www.ch.ch |

### Zurich: tax-at-source tariffs from 2026, basis and calculation parameters (PDF)

Canton of Zurich, Cantonal Tax Office, <https://www.zh.ch/content/dam/zhweb/bilder-dokumente/themen/steuern-finanzen/steuern/quellensteuer/quellensteuertarif/2026/grundlagen_und_berechnungsparameter_2026.pdf>

| Evidence | Fact jurisdiction | Basis | Rule |
| --- | --- | --- | --- |
| `e-zh-tax-at-source-tariffs-10-1` | CH-ZH | Cantonal authority guidance | default |
| `e-zh-tax-at-source-tariffs-9-1` | CH-ZH | Cantonal authority guidance | default |

## Expat-life excerpts (18 September 2026)

Release `mvp-zurich-2026-09-18-v19` adds the 118 excerpts of the expat-life extension. The subagents that drafted the facts gave the article of every Code of Obligations citation; the coordinating assistant set it as the basis (federal act) and left every other excerpt to the page rules (ch.ch as a portal summary) or the page default (the authority's guidance). No person has reviewed them.

### Anmeldung und Registrierung | arbeit.swiss

State Secretariat for Economic Affairs SECO, public employment service, <https://www.arbeit.swiss/de/anmeldung-und-registrierung>

| Evidence | Fact jurisdiction | Basis | Rule |
| --- | --- | --- | --- |
| `e-unemployment-benefit-7-1` | CH | Federal authority guidance | default |
| `e-unemployment-benefit-8-1` | CH | Federal authority guidance | default |

### Arbeitslosenentschädigung | Kanton Zürich

Canton of Zurich, Office for the Economy, <https://www.zh.ch/de/wirtschaft-arbeit/stellensuche-arbeitslosigkeit/arbeitslosenentschaedigung.html>

| Evidence | Fact jurisdiction | Basis | Rule |
| --- | --- | --- | --- |
| `e-zh-unemployment-benefit-1-1` | CH-ZH | Cantonal authority guidance | default |
| `e-zh-unemployment-benefit-2-1` | CH-ZH | Cantonal authority guidance | default |
| `e-zh-unemployment-benefit-2-2` | CH-ZH | Cantonal authority guidance | default |
| `e-zh-unemployment-benefit-3-1` | CH-ZH | Cantonal authority guidance | default |
| `e-zh-unemployment-benefit-4-1` | CH-ZH | Cantonal authority guidance | default |

### Benötigte Dokumente für die Heirat | Stadt Zürich

City of Zurich, Civil Registry Office, <https://www.stadt-zuerich.ch/de/lebenslagen/einwohner-services/heiraten/dokumente.html>

| Evidence | Fact jurisdiction | Basis | Rule |
| --- | --- | --- | --- |
| `e-city-zurich-marriage-9-1` | CH-ZH-261 | Municipal authority guidance | default |

### Die 3. Säule der Altersvorsorge: 3a und 3b in der Schweiz

ch.ch, the information portal of the Confederation, cantons and communes (Federal Chancellery), <https://www.ch.ch/de/pensionierung/altersvorsorge/3-saule--private-vorsorge-/>

| Evidence | Fact jurisdiction | Basis | Rule |
| --- | --- | --- | --- |
| `e-pillar-3a-2-1` | CH | Portal summary of federal rules | page rule www.ch.ch |
| `e-pillar-3a-3-2` | CH | Portal summary of federal rules | page rule www.ch.ch |
| `e-pillar-3a-4-2` | CH | Portal summary of federal rules | page rule www.ch.ch |
| `e-pillar-3a-5-1` | CH | Portal summary of federal rules | page rule www.ch.ch |
| `e-pillar-3a-6-1` | CH | Portal summary of federal rules | page rule www.ch.ch |
| `e-pillar-3a-7-1` | CH | Portal summary of federal rules | page rule www.ch.ch |
| `e-pillar-3a-8-1` | CH | Portal summary of federal rules | page rule www.ch.ch |

### EO bei Adoption

Federal Social Insurance Office FSIO, <https://www.bsv.admin.ch/de/eo-bei-adoption>

| Evidence | Fact jurisdiction | Basis | Rule |
| --- | --- | --- | --- |
| `e-parental-leave-7-1` | CH | Federal authority guidance | default |
| `e-parental-leave-8-1` | CH | Federal authority guidance | default |

### EO bei Mutterschaft

Federal Social Insurance Office FSIO, <https://www.bsv.admin.ch/de/eo-bei-mutterschaft>

| Evidence | Fact jurisdiction | Basis | Rule |
| --- | --- | --- | --- |
| `e-parental-leave-2-1` | CH | Federal authority guidance | default |
| `e-parental-leave-2-2` | CH | Federal authority guidance | default |
| `e-parental-leave-3-1` | CH | Federal authority guidance | default |
| `e-parental-leave-4-1` | CH | Federal authority guidance | default |

### EO bei Vaterschaft

Federal Social Insurance Office FSIO, <https://www.bsv.admin.ch/de/eo-bei-vaterschaft>

| Evidence | Fact jurisdiction | Basis | Rule |
| --- | --- | --- | --- |
| `e-parental-leave-5-1` | CH | Federal authority guidance | default |
| `e-parental-leave-5-2` | CH | Federal authority guidance | default |
| `e-parental-leave-6-1` | CH | Federal authority guidance | default |

### Ehevorbereitung | Stadt Zürich

City of Zurich, Civil Registry Office, <https://www.stadt-zuerich.ch/de/lebenslagen/einwohner-services/heiraten/ehevorbereitung.html>

| Evidence | Fact jurisdiction | Basis | Rule |
| --- | --- | --- | --- |
| `e-city-zurich-marriage-1-1` | CH-ZH-261 | Municipal authority guidance | default |
| `e-city-zurich-marriage-2-1` | CH-ZH-261 | Municipal authority guidance | default |
| `e-city-zurich-marriage-3-1` | CH-ZH-261 | Municipal authority guidance | default |
| `e-city-zurich-marriage-4-1` | CH-ZH-261 | Municipal authority guidance | default |

### FAQ zur Arbeitslosenentschädigung | arbeit.swiss

State Secretariat for Economic Affairs SECO, public employment service, <https://www.arbeit.swiss/de/faq-zur-arbeitslosenentschaedigung>

| Evidence | Fact jurisdiction | Basis | Rule |
| --- | --- | --- | --- |
| `e-unemployment-benefit-1-1` | CH | Federal authority guidance | default |
| `e-unemployment-benefit-2-1` | CH | Federal authority guidance | default |
| `e-unemployment-benefit-3-1` | CH | Federal authority guidance | default |
| `e-unemployment-benefit-4-1` | CH | Federal authority guidance | default |
| `e-unemployment-benefit-5-1` | CH | Federal authority guidance | default |
| `e-unemployment-benefit-6-1` | CH | Federal authority guidance | default |
| `e-unemployment-benefit-9-1` | CH | Federal authority guidance | default |
| `e-unemployment-benefit-9-2` | CH | Federal authority guidance | default |

### Familienzulagen - Übersicht

Federal Social Insurance Office FSIO, <https://www.bsv.admin.ch/de/familienzulagen>

| Evidence | Fact jurisdiction | Basis | Rule |
| --- | --- | --- | --- |
| `e-family-allowances-1-1` | CH | Federal authority guidance | default |
| `e-family-allowances-2-1` | CH | Federal authority guidance | default |
| `e-family-allowances-9-1` | CH | Federal authority guidance | default |

### Familienzulagen: Angestellte

SVA Zürich, the cantonal social insurance office, <https://svazurich.ch/unsere-produkte/weitere-produkte/weitere-leistungen/familienzulagen/angestellte.html>

| Evidence | Fact jurisdiction | Basis | Rule |
| --- | --- | --- | --- |
| `e-zh-family-allowances-2-1` | CH-ZH | Cantonal authority guidance | default |
| `e-zh-family-allowances-6-1` | CH-ZH | Cantonal authority guidance | default |
| `e-zh-family-allowances-7-1` | CH-ZH | Cantonal authority guidance | default |

### Familienzulagen: Nichterwerbstätige

SVA Zürich, the cantonal social insurance office, <https://svazurich.ch/unsere-produkte/weitere-produkte/weitere-leistungen/familienzulagen/nichterwerbstaetige.html>

| Evidence | Fact jurisdiction | Basis | Rule |
| --- | --- | --- | --- |
| `e-zh-family-allowances-3-1` | CH-ZH | Cantonal authority guidance | default |
| `e-zh-family-allowances-4-1` | CH-ZH | Cantonal authority guidance | default |
| `e-zh-family-allowances-5-1` | CH-ZH | Cantonal authority guidance | default |

### Familienzulagen: Sinn und Zweck

SVA Zürich, the cantonal social insurance office, <https://svazurich.ch/unsere-produkte/weitere-produkte/weitere-leistungen/familienzulagen/sinn-und-zweck.html>

| Evidence | Fact jurisdiction | Basis | Rule |
| --- | --- | --- | --- |
| `e-zh-family-allowances-1-1` | CH-ZH | Cantonal authority guidance | default |

### Fedlex: Code of Obligations, SR 220

Fedlex, the Swiss federal law collection (Federal Chancellery), <https://www.fedlex.admin.ch/eli/cc/27/317_321_377/de>

| Evidence | Fact jurisdiction | Basis | Rule |
| --- | --- | --- | --- |
| `e-rent-changes-2-2` | CH | Federal act: OR, SR 220, Art. 269d | citation |
| `e-rent-changes-6-1` | CH | Federal act: OR, SR 220, Art. 270 | citation |
| `e-tenancy-agreement-2-2` | CH | Federal act: OR, SR 220, Art. 257e | citation |
| `e-tenancy-agreement-5-1` | CH | Federal act: OR, SR 220, Art. 266c | citation |
| `e-tenancy-agreement-6-1` | CH | Federal act: OR, SR 220, Art. 266l | citation |
| `e-tenancy-agreement-7-2` | CH | Federal act: OR, SR 220, Art. 266m | citation |
| `e-tenancy-agreement-8-1` | CH | Federal act: OR, SR 220, Art. 264 | citation |

### Formulare im Mietwesen | Kanton Zürich

Canton of Zurich, Directorate of Justice and Home Affairs, tenancy forms, <https://www.zh.ch/de/direktion-der-justiz-und-des-innern/generalsekretariat/formulare-mietwesen.html>

| Evidence | Fact jurisdiction | Basis | Rule |
| --- | --- | --- | --- |
| `e-zh-initial-rent-form-1-1` | CH-ZH | Cantonal authority guidance | default |
| `e-zh-initial-rent-form-2-1` | CH-ZH | Cantonal authority guidance | default |
| `e-zh-initial-rent-form-3-1` | CH-ZH | Cantonal authority guidance | default |
| `e-zh-initial-rent-form-4-1` | CH-ZH | Cantonal authority guidance | default |

### Heiraten in der Schweiz

ch.ch, the information portal of the Confederation, cantons and communes (Federal Chancellery), <https://www.ch.ch/de/familie-und-partnerschaft/heirat--konkubinat--partenariat/heiraten/>

| Evidence | Fact jurisdiction | Basis | Rule |
| --- | --- | --- | --- |
| `e-marriage-switzerland-1-1` | CH | Portal summary of federal rules | page rule www.ch.ch |
| `e-marriage-switzerland-2-1` | CH | Portal summary of federal rules | page rule www.ch.ch |
| `e-marriage-switzerland-3-1` | CH | Portal summary of federal rules | page rule www.ch.ch |
| `e-marriage-switzerland-4-1` | CH | Portal summary of federal rules | page rule www.ch.ch |
| `e-marriage-switzerland-5-1` | CH | Portal summary of federal rules | page rule www.ch.ch |
| `e-marriage-switzerland-6-1` | CH | Portal summary of federal rules | page rule www.ch.ch |
| `e-marriage-switzerland-7-1` | CH | Portal summary of federal rules | page rule www.ch.ch |
| `e-marriage-switzerland-8-1` | CH | Portal summary of federal rules | page rule www.ch.ch |

### Heiraten mit ausländischem Pass und Wohnort Zürich | Stadt Zürich

City of Zurich, Civil Registry Office, <https://www.stadt-zuerich.ch/de/lebenslagen/einwohner-services/heiraten/hochzeitstermin-ohne-schweizer-pass/wohnort-zurich.html>

| Evidence | Fact jurisdiction | Basis | Rule |
| --- | --- | --- | --- |
| `e-city-zurich-marriage-5-1` | CH-ZH-261 | Municipal authority guidance | default |
| `e-city-zurich-marriage-6-1` | CH-ZH-261 | Municipal authority guidance | default |
| `e-city-zurich-marriage-7-1` | CH-ZH-261 | Municipal authority guidance | default |
| `e-city-zurich-marriage-8-1` | CH-ZH-261 | Municipal authority guidance | default |

### Hypothekarischer Referenzzinssatz

Federal Office for Housing BWO, <https://www.bwo.admin.ch/de/referenzzinssatz>

| Evidence | Fact jurisdiction | Basis | Rule |
| --- | --- | --- | --- |
| `e-rent-changes-3-1` | CH | Federal authority guidance | default |
| `e-rent-changes-4-1` | CH | Federal authority guidance | default |
| `e-rent-changes-5-1` | CH | Federal authority guidance | default |

### Krankenversicherung: Zur Sistierung der Unfalldeckung berechtigte Versicherte

Federal Office of Public Health FOPH, <https://www.bag.admin.ch/de/krankenversicherung-zur-sistierung-der-unfalldeckung-berechtigte-versicherte>

| Evidence | Fact jurisdiction | Basis | Rule |
| --- | --- | --- | --- |
| `e-accident-insurance-4-1` | CH | Federal authority guidance | default |
| `e-accident-insurance-5-1` | CH | Federal authority guidance | default |
| `e-accident-insurance-6-1` | CH | Federal authority guidance | default |
| `e-accident-insurance-7-1` | CH | Federal authority guidance | default |

### Leistungen und Voraussetzungen

Federal Social Insurance Office FSIO, <https://www.bsv.admin.ch/de/familienzulagen-leistungen-und-voraussetzungen>

| Evidence | Fact jurisdiction | Basis | Rule |
| --- | --- | --- | --- |
| `e-family-allowances-3-1` | CH | Federal authority guidance | default |
| `e-family-allowances-4-1` | CH | Federal authority guidance | default |
| `e-family-allowances-5-1` | CH | Federal authority guidance | default |
| `e-family-allowances-6-1` | CH | Federal authority guidance | default |
| `e-family-allowances-7-1` | CH | Federal authority guidance | default |
| `e-family-allowances-8-1` | CH | Federal authority guidance | default |

### Mietvertrag, Untermietvertrag, Pachtvertrag in der Schweiz.

ch.ch, the information portal of the Confederation, cantons and communes (Federal Chancellery), <https://www.ch.ch/de/wohnen/miete/mietvertrag-und-pachtvertrag/>

| Evidence | Fact jurisdiction | Basis | Rule |
| --- | --- | --- | --- |
| `e-tenancy-agreement-1-1` | CH | Portal summary of federal rules | page rule www.ch.ch |
| `e-tenancy-agreement-2-1` | CH | Portal summary of federal rules | page rule www.ch.ch |
| `e-tenancy-agreement-3-1` | CH | Portal summary of federal rules | page rule www.ch.ch |
| `e-tenancy-agreement-4-1` | CH | Portal summary of federal rules | page rule www.ch.ch |
| `e-tenancy-agreement-7-1` | CH | Portal summary of federal rules | page rule www.ch.ch |
| `e-tenancy-agreement-9-1` | CH | Portal summary of federal rules | page rule www.ch.ch |

### Umzug in die Schweiz

ch.ch, the information portal of the Confederation, cantons and communes (Federal Chancellery), <https://www.ch.ch/de/auslander-in-der-schweiz/in-der-schweiz-leben/umzug-in-die-schweiz/>

| Evidence | Fact jurisdiction | Basis | Rule |
| --- | --- | --- | --- |
| `e-moving-goods-customs-3-1` | CH | Portal summary of federal rules | page rule www.ch.ch |
| `e-moving-goods-customs-6-1` | CH | Portal summary of federal rules | page rule www.ch.ch |
| `e-moving-goods-customs-7-1` | CH | Portal summary of federal rules | page rule www.ch.ch |

### Umzug in die Schweiz: Vorgehen

Federal Office for Customs and Border Security FOCBS, <https://www.bazg.admin.ch/de/vorgehen-umzug-in-die-schweiz>

| Evidence | Fact jurisdiction | Basis | Rule |
| --- | --- | --- | --- |
| `e-moving-goods-customs-1-1` | CH | Federal authority guidance | default |
| `e-moving-goods-customs-2-1` | CH | Federal authority guidance | default |
| `e-moving-goods-customs-4-1` | CH | Federal authority guidance | default |
| `e-moving-goods-customs-4-2` | CH | Federal authority guidance | default |
| `e-moving-goods-customs-5-1` | CH | Federal authority guidance | default |

### Unfallversicherung: Wer ist obligatorisch versichert?

Federal Office of Public Health FOPH, <https://www.bag.admin.ch/de/unfallversicherung-wer-ist-obligatorisch-versichert>

| Evidence | Fact jurisdiction | Basis | Rule |
| --- | --- | --- | --- |
| `e-accident-insurance-1-1` | CH | Federal authority guidance | default |
| `e-accident-insurance-2-1` | CH | Federal authority guidance | default |
| `e-accident-insurance-3-1` | CH | Federal authority guidance | default |

### Urlaub und Erwerbsersatz bei Mutterschaft, Vaterschaft und Adoption

Federal Social Insurance Office FSIO, <https://www.bsv.admin.ch/de/eo-elternschaft>

| Evidence | Fact jurisdiction | Basis | Rule |
| --- | --- | --- | --- |
| `e-parental-leave-1-1` | CH | Federal authority guidance | default |
| `e-parental-leave-2-3` | CH | Federal authority guidance | default |

### Wegzug aus der Stadt Zürich | Stadt Zürich

City of Zurich, Population Office, <https://www.stadt-zuerich.ch/de/lebenslagen/einwohner-services/umziehen-melden/wegzug.html>

| Evidence | Fact jurisdiction | Basis | Rule |
| --- | --- | --- | --- |
| `e-city-zurich-departure-1-1` | CH-ZH-261 | Municipal authority guidance | default |
| `e-city-zurich-departure-2-1` | CH-ZH-261 | Municipal authority guidance | default |
| `e-city-zurich-departure-3-1` | CH-ZH-261 | Municipal authority guidance | default |
| `e-city-zurich-departure-4-1` | CH-ZH-261 | Municipal authority guidance | default |
| `e-city-zurich-departure-5-1` | CH-ZH-261 | Municipal authority guidance | default |
| `e-city-zurich-departure-6-1` | CH-ZH-261 | Municipal authority guidance | default |
| `e-city-zurich-departure-7-1` | CH-ZH-261 | Municipal authority guidance | default |

### Wegzug ins Ausland | Stadt Zürich

City of Zurich, Tax Office, <https://www.stadt-zuerich.ch/de/lebenslagen/steuern/natuerliche-personen/lebenssituationen/wegzug-ins-ausland.html>

| Evidence | Fact jurisdiction | Basis | Rule |
| --- | --- | --- | --- |
| `e-city-zurich-departure-8-1` | CH-ZH-261 | Municipal authority guidance | default |
| `e-city-zurich-departure-9-1` | CH-ZH-261 | Municipal authority guidance | default |

### Welche Beiträge kann ich in die Säule 3a einzahlen? | BSV

Federal Social Insurance Office FSIO, <https://faq.bsv.admin.ch/de/3-saeule/welche-beitraege-kann-ich-die-saeule-3a-einzahlen>

| Evidence | Fact jurisdiction | Basis | Rule |
| --- | --- | --- | --- |
| `e-pillar-3a-3-1` | CH | Federal authority guidance | default |
| `e-pillar-3a-4-1` | CH | Federal authority guidance | default |

### Wer kann eine Säule 3a (gebundene Selbstvorsorge) einrichten? | BSV

Federal Social Insurance Office FSIO, <https://faq.bsv.admin.ch/de/3-saeule/wer-kann-eine-saeule-3a-gebundene-selbstvorsorge-einrichten>

| Evidence | Fact jurisdiction | Basis | Rule |
| --- | --- | --- | --- |
| `e-pillar-3a-1-1` | CH | Federal authority guidance | default |

### Wohnen: Ruhezeiten, Mietzins und Mängel in der Schweiz

ch.ch, the information portal of the Confederation, cantons and communes (Federal Chancellery), <https://www.ch.ch/de/wohnen/miete/larm--mangel--mietzins/>

| Evidence | Fact jurisdiction | Basis | Rule |
| --- | --- | --- | --- |
| `e-rent-changes-1-1` | CH | Portal summary of federal rules | page rule www.ch.ch |
| `e-rent-changes-2-1` | CH | Portal summary of federal rules | page rule www.ch.ch |
| `e-rent-changes-6-2` | CH | Portal summary of federal rules | page rule www.ch.ch |
| `e-rent-changes-7-1` | CH | Portal summary of federal rules | page rule www.ch.ch |
| `e-rent-changes-8-1` | CH | Portal summary of federal rules | page rule www.ch.ch |
