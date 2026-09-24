# Limitations

**Last update:** 24 September 2026

What the Swiss TIP MCP server does not do well, does not do yet, or does not
claim. It applies to the committed release `mvp-zurich-2026-09-24-v1` and is
updated whenever the knowledge base changes (see [AGENTS.md](AGENTS.md),
"Coverage and limitations documents"). What the server does cover is in
[COVERAGE.md](COVERAGE.md). `mvp-wallisellen` was a proof of concept and is
outside the submission: its release stays attested and frozen, and nothing
below is measured on it.

- **Pages the run holds that no fact cites.** Until 22 September 2026 nothing
  in the pipeline compared the text dataset with the release: the release's
  document list is derived from its citations, so validating it could not
  find a saved page outside it. The audit of that day found 29 catalogued
  German pages and five federal acts fetched and never cited, one of them
  holding the five-year settlement rule an acceptance case forbade. The build
  now has a `coverage` stage (`curation-coverage.json` and `.md` next to the
  release) that lists every content section of every candidate record no
  fact cites and no disposition in `curation-coverage.yaml` names; the pack
  runs it under `coverage_policy: report`, so an open section is a number in
  that report and not yet a build error. The first report and the
  dispositions written against it are described under "Retrieval
  limitations".

## Review status: reviewed by one person, not by a lawyer

**All 1,273 facts are `human-reviewed`**, by one named reviewer: the 104 facts
of the residence topic (78) and of the cantonal migration-office contacts
(26) on 14 September 2026, the 149 facts of the five topics added on
15 September 2026, social insurance (25), tax at source (26), driving
licence (23), health insurance (26) and naturalisation (49), on
15 September 2026, and the 37 facts of the 13 `fza-*` concepts, drafted on
16 September 2026 from the German text of the Agreement on the Free Movement
of Persons (SR 0.142.112.681), on 16 September 2026, the 41 facts of the
nine office-contact concepts, drafted on 17 September 2026 from the offices'
own contact pages, on 17 September 2026, and the 86 facts of the daily-life
extension, drafted the same day from the saved City of Zurich, Canton of
Zurich and SERAFE pages (83 facts of 18 concepts in four topics, and three
City of Zurich naturalisation facts read from data tables of pages already
cited), on 17 September 2026, and the 49 facts of the entry-and-visa
extension, drafted the same day from SEM's entry pages, the FDFA visa page
and the Ordinance on Entry and the Granting of Visas (VEV, SR 142.204): 40
facts of the nine `entry-*` concepts and 9 facts of the two Zurich
family-reunification concepts, on 17 September 2026, and the 29 facts of
the voting-rights and tax-at-source tariff extension, drafted on
18 September 2026 from the Federal Constitution, the Constitution of the
Canton of Zurich, ch.ch, the Canton of Zurich's voting page, the Tax at
Source Ordinance, the ESTV page, the Canton of Zurich's tariff page, its
2026 parameter sheet and the Zürcher Steuerbuch 87.3: 12 facts of the two
voting-rights concepts and 17 of the two tariff concepts, on
18 September 2026, and the 106 facts of the expat-life extension, drafted the
same day by five assistant subagents from the saved pages and checked
statement by statement by the coordinating assistant (family allowances and
parental leave, renting a home, marriage, leaving the City of Zurich, pillar
3a, unemployment, accident insurance and customs on moving; 14 concepts), on
18 September 2026, and the 92 facts of 22 September 2026, confirmed in the
console that day: the nine of `permit-c-five-years` and
`zh-permit-c-five-years`, the 77 of the twenty concepts curated from pages
the catalogue already held, and the six whose review was reopened when a
second citation of the law was added to them.

Every statement was first written by an assistant reading the cited page and
choosing the excerpt; for the 149 added facts, the build verified that each
excerpt exists verbatim and the acceptance gate that 75 claims of UAT-8 to
UAT-17 hold on a statement and a phrase of its excerpt before the review; for
the 37 `fza-*` facts the build verified the excerpts, and no acceptance case
covers them; for the 41 office facts the build verified the excerpts and 18
claims of UAT-18 to UAT-23 and DECLINE-6 were written before the last of
them, the location list of the Road Traffic Office, was confirmed; for the
86 daily-life facts the build verified the excerpts and the assistant compared
every statement with its excerpt before the review, and the 11 cases UAT-24 to
UAT-34 and 35 regression cases were written after it; for the 49
entry-and-visa facts the build verified the excerpts and the assistant checked
that every German search term occurs in them, and the six cases UAT-45 to
UAT-50 and 19 regression cases were written after the review; for the 29
voting-rights and tariff facts the build verified the excerpts and every
German search term, and the cases UAT-51 to UAT-53 and 13 regression cases
were written before the review; for the 106 expat-life facts the build
verified the excerpts and every German search term, and the cases UAT-54 to
UAT-64 and 35 regression cases were written before the review. The
reviewer then confirmed the facts in the admin console's review queue, where
each card shows the statement next to its cited excerpt, its jurisdiction and
its condition. On 15 September the reviewer then read every one of the 253
statements card by card against its cited excerpt, outside the console; that
reading is recorded as a `review:` note on each fact, written by an
assistant on the reviewer's instruction in place of the console's confirm
action, so it has no console audit entry of its own. Each fact carries
`reviewed_by` and `reviewed_on`, `resolve`
returns both with the fact, and the release-wide counts are in the manifest,
in the `limitations` of every tool result and in `--health`.

What that review is not:

- **Of the 92 facts of 22 September 2026, in one sitting.** Twenty
  concepts were drafted that day from pages the catalogue and the text
  dataset already held; no source was added and no page was fetched. They
  are the social security agreements (ZAS), the third generation in
  naturalisation and the City of Zurich's German and civic-knowledge tests,
  the city citizenship of a Swiss citizen, three Zurich family-reunification
  routes, the EU/EFTA and third-country permit cards, the conditions of
  third-country labour-market admission and the Zurich procedure, the
  cantonal permit card, the entry permits for retirees and close relatives,
  travel documents, and where a particular item is disposed of in the city.
  Six facts that a reviewer had confirmed were given a second citation of
  the law they rest on (BüG, BüV, KVG, DBG) and their review was reopened,
  because the reviewer had seen the first excerpt only; their statements did
  not change. The build verified every excerpt and every German search term,
  and the regression cases were written and measured before the review. The
  reviewer confirmed all 92 in the console on 22 September 2026, in one
  sitting and not card by card against the excerpts a second time.
  The two concepts of the five-year routes by nationality were drafted from
  SEM's "Ausweis C EU/EFTA" and the Canton of Zurich's
  "Niederlassungsbewilligung", both already saved, and were confirmed
  earlier the same day, after the cases UAT-5 (updated), UAT-65, UAT-66 and
  five regression cases had been written against them.
- **Not of the English excerpts of 19 September 2026.** On 112 facts the
  English version of the cited federal page stands next to the reviewed
  German excerpt (and on one fact the German version next to a reviewed
  English excerpt). These 114 excerpts were aligned and compared with the
  reviewed ones by assistant subagents and checked by the coordinating
  assistant; no person has read them (see "Gaps in the English versions of
  19 September 2026").
- **Not a legal review.** Nobody with legal qualifications signed off a
  statement. The excerpt, not the English statement, remains the authority.
- **Not independent.** One person reviewed every fact; no second reviewer
  checked the first.
- **Confirmed in groups, then read one by one.** In the console, 65 facts
  were confirmed one at a time and 536 in bulk groups. On 14 September 71: the family-reunification concepts
  (9 facts), change of canton with third-country work (4), the short-term
  work notification concepts (5), the UK concept (3), the biometric-permit,
  language-evidence and health-insurance concepts (2 each), the 26 cantonal
  migration-office contacts (groups of 8, 8 and 10), and 18 of the 20 facts
  drafted from the three ch.ch pages (one group). On 15 September all 149
  facts of the added topics, in seven groups of 50, 23, 19, 16, 16, 13 and
  12 facts. On 16 September 29 of the 37 `fza-*` facts, in seven groups of
  5, 5, 5, 5, 4, 3 and 2, and the other 8 one at a time. On 17 September 26
  of the 41 office facts, in groups of 11, 8 and 7, and the other 15 one at
  a time; later that day 82 of the 86 daily-life facts, in groups of 35, 24,
  10, 7 and 6, and the other 4 one at a time, and all 49 entry-and-visa facts
  in a single group of 49. On 18 September 24 of the 29 voting-rights and
  tariff facts, in groups of 12, 7 and 5, and the other 5 one at a time,
  and all 106 expat-life facts in two groups of 100 and 6. Each of the 536
  carries a `review:` note naming its group, because a confirmation given to
  a group is weaker evidence of reading than one given to a single card. The
  card-by-card reading of the first 253 facts on 15 September is recorded on
  each of them as a second `review:` note; it was written by an assistant on
  the reviewer's instruction, not through the console, so the console's audit
  log shows the group confirmations only. The `fza-*`, office, daily-life,
  entry-and-visa, voting-rights, tariff and expat-life facts had no such
  second reading.
- **Portal summaries next to the law.** 27 facts cite ch.ch, the authorities'
  information portal, which summarises the rules in plain language for every
  group at once (20 of the residence topic, 3 of the driving licence, 4 of
  voting rights). Where
  a ch.ch fact and a fact from the law cover the same subject (family
  reunification under the AIG, the twelve months of VZV Article 42), the law
  and its excerpt are the more exact source. Since release
  `mvp-zurich-2026-09-16-v2` these facts are served with the basis `Portal
  summary of federal rules`, and a concept that serves one next to the law
  or an authority's page tells the caller so.
- **The basis of every excerpt was assigned by an assistant, not reviewed.**
  Since release `mvp-zurich-2026-09-16-v2` every served fact states what
  its cited excerpt is (an act and its article, an ordinance, the
  free-movement agreement, a directive, an authority's guidance, a
  directory entry, a portal summary). The 91 law citations name their
  article and the 16 guidance excerpts that cite a norm name it. An
  assistant read the first 298 excerpts and assigned these labels on
  16 September 2026 ([releases/mvp-zurich/basis-review.md](releases/mvp-zurich/basis-review.md)),
  and labelled the 53 office-contact excerpts and the 132 daily-life
  excerpts of 17 September 2026 when writing them (49 and 18 `directory`,
  the others left to the page default `guidance`; two further excerpts come
  from splitting two City of Zurich naturalisation citations around a data
  table), and likewise the 34 voting-rights and tariff excerpts of
  18 September 2026; the build verified only their form. No person has checked an article number or
  a kind, and the human review of the first 290 facts predates the labels.
- **Not a completeness check.** The review confirmed the published facts. It
  did not establish that a concept carries every exception its source page
  states, nor that the statements of the acceptance-test document the release
  does not serve are wrong (see "Gaps in the extension" below).

Because every fact is reviewed, a `resolve` with `reviewed_only` returns the
same facts as one without it on this release, and reports nothing withheld.

## Limitations of the published statements

These seven are the manifest's own `limitations` list, served in full by
`get_coverage`. `search`, `resolve` and `get_evidence` carry the review-status
line and one pointer to this list instead, since 17 September 2026:

- Every statement was written by an assistant reading the cited pages and
  checked against its cited excerpt by one named reviewer (`reviewed_by` on
  each fact); this is not a legal review.
- Every fact was confirmed by the reviewer in the admin console's review
  queue, many in bulk groups (a `review:` note on each fact names its group);
  the review history by date is in LIMITATIONS.md of the repository.
- 114 excerpts of the English (once the German) version of a cited federal
  page stand next to the reviewed excerpts of 112 facts; the assistant added
  them after comparing both versions, and no person has reviewed them.
- English statements paraphrase the cited original-language text; they are not
  official translations. The excerpt, not the statement, is the authority, and
  `get_evidence` always returns it.
- Conditions route population groups to statements; they do not decide
  eligibility for a specific person. The server has no rules engine and
  computes no outcome.
- Office addresses, opening and telephone hours and closing days are those the
  saved pages state; a location or channel a page does not list is not served,
  and special closing days are served only where a page lists them.
- Validity is unbounded unless the cited page states a date; freshness
  measures the age of the saved copy, not whether the page changed.

## Review history by date

The served limitations point here for the dates and group sizes of the
review, which the coverage root no longer carries since release
`mvp-zurich-2026-09-17-v2` (it has to stay under 6 KB):

| Date | Facts confirmed | How |
| --- | --- | --- |
| 14 September 2026 | 104 (residence 78, cantonal migration offices 26) | 33 one by one, 71 in bulk groups |
| 15 September 2026 | 149 (the five topics added that day) | in seven bulk groups; the 253 facts confirmed by then were also read card by card |
| 16 September 2026 | 37 (`fza-*`) | 8 one by one, 29 in bulk groups |
| 17 September 2026 | 41 (office contacts) | 15 one by one, 26 in bulk groups |
| 17 September 2026 | 86 (daily life, and three City of Zurich naturalisation facts) | 4 one by one, 82 in bulk groups |
| 17 September 2026 | 49 (entry and visas, and two Zurich family-reunification concepts) | in bulk groups |
| 18 September 2026 | 29 (voting rights, tax-at-source tariffs) | 5 one by one, 24 in bulk groups |
| 18 September 2026 | 106 (expat life) | in two bulk groups of 100 and 6 |
| 22 September 2026 | 117 (settlement permit 57, integration 25, naturalisation 19, and 16 across four other topics) | in bulk groups |
| 23 September 2026 | 113 (customs) | hardest first: the 23 that carry a number, then the five single-page concepts, then the rest |
| 23 September 2026 | 98 (basic health insurance) | hardest first, against a written brief: the 13 that carry a number, a date or a threshold, then nine recorded judgement calls, then six German legal terms rendered into English, then the rest |
| 23 September 2026 | 131 (work and unemployment) | hardest first, against a written brief: one decision settling thirteen facts on whether a threshold is a rule or an amount, then the 39 facts carrying a number, then nine recorded judgement calls |
| 23 September 2026 | 90 (AHV, the pillars and retirement) | hardest first, against a written brief: the two rules the pages turned out not to state, a preserved defect in a publisher's page, then the 22 facts carrying a number and six recorded judgement calls |
| 23 September 2026 | 124 (registering on arrival in all 26 cantons) | against two written briefs with an English rendering beside each of the 49 French and Italian excerpts, and a per-fact note on the twelve that carry a figure that is not fourteen days, a direction of travel that inverts easily, a duty owed to two offices, or a reading that rests on a canton's law rather than a page a resident would read |
| 24 September 2026 | 5 (Lugano waste) | in the console |

## Gaps in the Lugano waste extension of 23 September 2026

- **One city outside Zurich, one subject.** A survey of the waste calendars
  of the ten largest cities after Zurich
  (`.local/experiments/2026-09-23-waste-calendars-other-cities.md`) found that
  Lugano alone publishes no collection day, so a general assistant is most
  likely to invent one there. Only how waste is handed over in Lugano is
  served. Collection days, recycling points and fees in Basel, Geneva, Bern
  and every other city remain out of scope and are rejected with
  `jurisdiction_not_covered`.
- **What the Lugano facts do not say.** The collection days and times the
  city's Urban Spaces Division sets, the locations and opening hours of the
  ecopunti and ecocentri, the bag prices and the basic waste fee are not
  served, although the saved pages state some of them.
- **Four facts rest on the ordinance, one on a page.** The ordinance is a
  13-page PDF whose extracted text is one block per page, so each citation
  is a whole page. Its reading order was not checked beyond the cited
  articles.
- **Colloquial questions match weakly.** A question naming an object
  ("Dove porto un vecchio divano a Lugano?") has no alias to match and
  returns a weak match. Questions about collection days, bags, bulky waste
  or the Ecocard match strongly in English, German and Italian.

## Gaps in the cantonal registration wave of 23 September 2026

- **How these 124 facts were made.** They were proposed by kb-reader
  subagents, one per saved page, and merged by the coordinating assistant
  after checking mechanically that every source term occurs verbatim in the
  cited blocks. That check catches a term that drifted from its evidence, not
  a statement that misreads it, so it is much weaker than a person reading the
  statement against its excerpt. All 124 were then confirmed by the named
  reviewer on 23 September 2026 in the admin console's review queue.
- **Cover is uneven, because the cantons publish unevenly.** All 25 cantons
  outside Zurich state a period and all but Appenzell Innerrhoden name the
  office, but only 15 describe the permit application, 17 the change of canton
  and 10 an online channel. A concept with no fact for a canton means that
  canton was not found to publish it, not that no rule exists.
- **Zurich is not served by these concepts.** Its rule lives in its own,
  fuller concepts, so resolving a `cantonal-*` concept for Zurich returns
  `OUT_OF_COVERAGE` with `jurisdiction_not_covered` rather than another
  canton's period.
- **Most periods come from a cantonal statute, not from a service page.** Of
  the cantons in this wave most state the registration period only in their
  law; several publish service pages that describe the procedure without ever
  giving a number. The basis (`law`, `directive`, `guidance`, `summary`) is
  recorded on every excerpt, so a caller can see which kind of source an
  answer rests on.
- **The statute excerpts are coarse.** The cantonal collections serve PDFs
  whose text extracts in large blocks: the largest block of a statute is a
  median 2,204 characters against 495 for a service page. An excerpt selected
  around the provision a statement rests on therefore often carries the
  neighbouring provisions too. Nothing is paraphrased - the excerpt is simply
  wider than the sentence in question.
- **A cantonal statute URL pins the version that was read.** Most cantonal
  collections run the same application, where the page a reader sees is an
  empty shell and the text arrives from an API that returns the *current*
  consolidated version behind a numbered version id. Resolving the PDF through
  that API is how this wave guaranteed it read the version in force; the cost
  is that the saved URL keeps returning that same version. A later
  consolidation is published under a new id, so re-fetching the same URL would
  **not** notice that the law had changed. Freshness measures the age of the
  saved copy, not whether the law moved.
- **Jura's statute is not cited at all.** Its collection addresses documents
  with a query string, which a source URL in this pack may not carry, and four
  query-free forms all return an error. Jura's facts rest on its service pages
  only.
- **Schwyz's Migrationsgesetz is not cited.** Its text appears in this pack's
  corpus only inside the amendment clause of another act, which would let the
  release quote an amendment clause as operative law; it is recorded as a
  catalogue gap instead.
- **Contradictions within a canton are served, not resolved.** Where a
  canton's own sources disagree - Appenzell Innerrhoden's eight days against
  fourteen, Zug's statute against its migration office, Fribourg's commune
  against its cantonal service, Nidwalden's two live pages on whether a
  foreign national may use the municipal online service - both facts are
  served, each scoped to what its source covers and naming it.
- **French and Italian are indexed, but questions are still asked in German
  and English.** The wave added 30 French and Italian source terms copied
  verbatim from Vaud, Valais and Ticino pages, so a French or Italian question
  about registration now finds its concept directly instead of having to be
  translated into German first. `question_languages` stays `de` and `en`: the
  sample questions on every concept are unchanged.
- **A French or Italian question naming Zurich is served worse than one naming
  Vaud or Ticino.** It now ranks the `cantonal-*` concepts above Zurich's own,
  and resolving them for Zurich returns `OUT_OF_COVERAGE`. The caller is
  refused rather than misinformed, but is not routed to the Zurich concepts
  that do hold the answer.

## Gaps in the English versions of 19 September 2026

- **Compared by assistants, not read by a person.** Six assistant subagents
  (some with helpers) aligned each of the 133 cited German excerpts on the
  SEM, FOPH, FOCBS, SECO and SERAFE pages, and the one English SEM excerpt,
  with the other language version of its page and compared them sentence by
  sentence; the coordinating assistant checked every range against the text
  dataset (block range, numbers) and read every pair that was not a plain
  translation. 114 excerpts were added; the record is
  `.local/experiments/2026-09-19-english-sources/` (`review.md`,
  `decisions.json`).
- **19 excerpts have no second version.** The 7 of the SEM citizenship FAQ,
  whose English URL says the FAQ exists in German, French and Italian only,
  and 12 where the versions differ on something the fact states: the English
  pages say a type D visa is for stays of more than three months (German: from
  three months), tie the ETIAS passport validity to the planned departure,
  omit the host's letter of invitation for travellers without sufficient
  means, name fewer grounds of the EU/EFTA entry danger clause, do not say
  four fingerprints for the EES, name a psychiatric hospital where the German
  says any Swiss institution, name another item of the biometric-permit fee,
  say only the competent authorities for UK workers, hedge the three-day
  emergency deadline of posted work, merge two visa application channels and
  turn the customs opening-hours rule into advice; SERAFE's English fee page
  shows CHF 335 in its desktop and CHF 365 in its mobile table. The German
  excerpt alone supports these facts.
- **Accepted with differences outside the fact.** Nine English excerpts differ
  from the German one in something the fact does not state (an extra example,
  more accepted documents, a linked PDF's date, a merged FAQ, the portal's
  English domain www.work.swiss); they were added, each with its reason in the
  fact's provenance note.
- **Older English copies.** 14 of the 24 English pages were saved by the
  imported crawl of 11 September 2026 and were not fetched again; the German
  pages next to them were saved between 11 and 18 September. The comparison
  found no difference that a later change of either page explains.
- **Other English versions are not cited.** The English versions of the ch.ch,
  ZAS, ESTV and EDA pages and of three BSV pages, the English translations of the
  Federal Constitution and the Code of Obligations on Fedlex, and the three
  cited Canton of Zurich pages that have one (employment of foreign nationals,
  the Office for the Economy, premium reduction) are not in the release. The
  City of Zurich and SVA Zurich pages, the BWO page, the FSIO FAQ and three
  BSV income-compensation pages have no English version.
- **The search gain is small.** On the regression and acceptance suites (450
  search steps) Hit@1 moved from 331 to 332 lexically and from 365 to 366
  with hybrid search, and the pass counts stayed 539 and 532 of 560. On 80
  blind questions in 12 other languages that a caller translated into English
  key terms, Hit@1 for the 27 affected concepts moved from 36 to 39 of 54
  lexically and from 46 to 47 with hybrid search; German translations and
  unaffected concepts did not move. Four chosen terms (unemployment insurance
  scheme, job vacancy, husband or wife of a Swiss citizen, premium reductions)
  were dropped because each pushed a blocking case out of the first three
  hits.

## Gaps in the expat-life extension of 18 September 2026

- **Drafted by subagents, confirmed in two large groups.** Five assistant subagents wrote
  the 110 draft statements from the saved pages; the coordinating assistant
  compared every one with its excerpt, dropped four (a duplicate, an advance
  customs procedure offered only at three Ticino offices, and two tenancy-form
  facts resting on download-link labels or repeating the federal rule) and
  rewrote three (the tax representative on departure, the date wording of the
  reference rate, and an unemployment exemption whose two conditions the page
  lists ambiguously; only the unambiguous part is served). The reviewer then
  confirmed the 106 facts in two bulk groups of 100 and 6, which is weaker
  evidence of reading than a card-by-card confirmation.
- **Numbers that change.** The reference interest rate (1.25 percent, as the
  Federal Office for Housing's page stated on 18 September 2026) can change
  after the saved copy, and the fact names the date; the pillar 3a maximum contributions
  are served until the end of 2026; the family allowance amounts of the
  Canton of Zurich come from SVA Zurich's page, which names no year, so they
  carry no end date although the canton can change them.
- **Children abroad, other cantons, amounts.** The family-allowance facts say
  that special conditions apply to children living abroad and do not state
  them. For other cantons the federal facts are served with the caveat; their
  allowance amounts, their unemployment offices and their rental forms are
  not. No fact states a rent level, an allowance for a specific family or an
  unemployment benefit for a specific person.
- **Tenancy law, not the rental market.** The housing concepts serve the
  Code of Obligations' rules and ch.ch's and the Federal Office for Housing's
  explanations; finding a flat, rent levels, a specific conciliation
  authority's address and indexed or staged rents are not served. "How much
  rent should I expect for a two-room flat?" reads as a strong match on the
  tenancy concepts, which declare in `not_served` that they state no rent
  amount (regression case OOS-27).
- **Marriage and departure in the City of Zurich only.** Other
  municipalities' civil registry and population offices are not published; a
  resident of Uster or Wädenswil gets the federal marriage facts or nothing.
  Marrying abroad and the recognition of a foreign marriage, on the saved
  ch.ch page, are not curated.
- **Now covered, once declined.** Paternity leave (OOS-5) and unemployment
  benefit (OOS-8) were examples of uncovered questions; their regression
  cases now expect the new concepts. DECLINE-1 moved a second time and now
  asks about secondary school (Gymnasium), as do the off-topic example of the
  match-strength test, the round-trip check and the README. The imputed rental
  value of a house (OOS-9) reads strong in the hybrid replay and is
  quarantined.
- **Search words added to older concepts.** The new vocabulary moved rarity
  weights again. Everyday aliases were added to `zh-eu-registration`,
  `permit-lost`, `health-insurance-deadline`, `zh-family-l-permit` and
  `entry-short-stay-rule` so that UAT-1, UAT-45, Q-DE-3, Q-DE-54, N-EN-T2 and
  N-DE-A3 keep finding their concept; two accident-insurance aliases were
  reworded because "occupational" collided with a quota question. No fact
  changed. A German question about a broken fridge (Q-DE-63) finds the
  defects concept lexically but reads weak in the hybrid replay and is
  quarantined.
- **Payloads.** Measured on this release: a `resolve` of the tenancy concept
  returns about 8 KB, of the rent concept about 7.5 KB, of parental leave
  about 7 KB; the federal and Zurich concepts together about 10 KB for
  unemployment and 11 KB each for family allowances and marriage, within the
  30 KB budget of a single-turn case when the caller makes few other calls.

## Gaps in the voting-rights and tax-at-source tariff extension of 18 September 2026

- **One sentence is a reading, confirmed in a group.** The last sentence of
  `zh-tax-at-source-tariffs-9`, that the tariff is the same in every
  municipality of the canton, is the assistant's reading of the parameter
  sheet's "Gewogenes Mittel der Gemeindesteuerfüsse" and of the tariff page,
  which publishes one set of tables for the canton; neither page says it in
  these words. A provenance note on the fact says so, and the reviewer
  confirmed the fact in the bulk group of the twelve Zurich tariff facts.
- **How the tariff is set, not what it comes to.** The tariff tables, the
  amount of tax for a salary and the tariff calculator itself are not served;
  the facts name the calculator and the 2026 tables. The 2026 tables and
  calculation parameters are served until the end of 2026, and the 2027
  edition needs a new download. The ordinary tax rates and the tax multiplier
  of a municipality, which do differ between municipalities, are not served
  either, so a caller comparing the ordinary taxes of Winterthur and Zurich
  has nothing to cite.
- **Voting rights of Zurich and the Confederation only.** For another canton
  `resolve` serves the federal facts, among them ch.ch's statement that the
  cantons decide and that Jura and Neuchâtel give foreign nationals a
  cantonal vote. The communes of other cantons that grant a communal vote,
  and every other canton's own rule, are not published.
- **The church exception rests on the canton's page.** The vote of B, C and
  Ci permit holders in the elections and votes of the Evangelical Reformed
  church is served as the Canton of Zurich's voting page states it, citing the
  church's ordinance; the ordinance itself and the rules of the other
  recognised churches are not in the release.
- **The cantonal constitution is the version on Fedlex.** Fedlex publishes
  the Constitution of the Canton of Zurich as a federally guaranteed cantonal
  constitution, here in its version of 1 July 2024; an amendment the canton
  has adopted and the Confederation not yet guaranteed would appear in the
  canton's own law collection first.
- **Not served next to it.** The dates, subjects and results of votes and
  elections, voting from abroad, e-voting, missing voting documents and
  appeals in voting matters; the concepts' `not_served` lists name them.
- **The plain rate question ranks the tariff concept behind the liability
  concept.** "What is the tax at source in Zurich?" carries three words that
  every Zurich tax-at-source concept holds, so the tariff concept is the third
  lexical and the second hybrid hit, after the liability concept; "How much is
  the tax at source in Zurich?", "tax at source rate", "Wie hoch ist die
  Quellensteuer" and the municipality questions find it first. Four older
  regression cases slipped when the new concepts changed the rarity weights
  and, after the review, their prior: N-DE-T2 and Q-DE-41 fell to `weak`,
  Q-DE-3 and XC-22 lost their concept from the first three hits. The
  everyday alias "Quellensteuer zahlen" and the aliases "which canton's
  tax-at-source rules apply" and "Quellensteuer welcher Kanton" on
  `tax-at-source-liability`, the source terms "Kurs" and "besuchen" on
  `zh-dog-keeping`, and dropping the source terms that gave
  `zh-political-rights` the generic word "Kanton" restored them; no fact
  changed.
- **The declines moved.** Voting was the example of an uncovered topic:
  DECLINE-1 then asked about a rent increase, and the off-topic voting
  question of the match-strength test and the round-trip check was replaced
  by the same rent question; since the expat-life extension both use
  secondary school. SEARCH-DECLINE-5 keeps its question on the dates of the
  next federal votes, which the new concepts do not serve; it still reads
  `weak`.
- **One ingestion change.** The Fedlex source plugin accepted only numeric
  ELI work numbers; it now also accepts the suffix `_fga` of the federally
  guaranteed cantonal constitutions (with a test). Its version stayed 1.0.0,
  because every earlier URL resolves as before and a new version would have
  invalidated the existing Fedlex archive of the run.

## Gaps in the entry-and-visa extension of 17 September 2026

- **No answer for a single nationality.** Whether a person needs a visa
  depends on their nationality, and SEM publishes that in the Annex CH-1
  lists, which are PDFs the release does not curate. The concepts state the
  rule and name the list; a question like "do I as an Indian citizen need a
  visa" cannot be answered from the served facts, and
  `entry-visa-need`'s `not_served` says so.
- **The ETIAS facts are a snapshot of a system that has not started.** SEM's
  page, saved on 11 September 2026, says applications cannot yet be filed and
  travellers need take no steps; the fact names that date and will be wrong
  once ETIAS starts. Freshness measures the age of the saved copy, not
  whether the EU has since set a date.
- **The stay calculator is not served.** Only SEM's page explaining the
  90-in-180-days rule and its three examples are curated; the calculator
  itself is an application.
- **Airport transit is not served.** The VEV's airport-transit visa (Article
  10) and SEM's transit answer are catalogued but carry no fact.
- **Two catalogued pages carry no fact.** SEM's entry hub and its
  "information on entry" page are saved and listed in `sources.md`, but every
  statement they carry is on the subpages that are cited.
- **The EES facts describe the system, not a border.** They state what the
  Entry/Exit System records, that it replaces the passport stamp and the
  right to see one's data; they do not say what happens at a specific border
  crossing or airport, or when a given border adopted it.
- **Next to asylum, which the pack does not serve.**
  `zh-family-refugee-asylum` names refugees and asylum, so a question about
  applying for asylum can read as a strong lexical match on it. Its
  `not_served` names the asylum procedure, the decisions and permit N; the
  caller receives that list with the facts.
- **Older copies than the rest of the release.** The nine SEM pages and the
  two Canton of Zurich family pages of this extension were saved on
  11 September 2026 in the imported crawl, the FDFA page and the VEV on
  17 September 2026. All are inside the 60-day freshness window.
- **The cases were written after the review, and none has been run live.**
  UAT-45 to UAT-50 and 19 regression cases cover the eleven new concepts;
  they were written after the reviewer confirmed the facts, and no graded
  caller run has exercised them. Nine of the 40 `entry-*` facts and four of
  the nine family facts carry a claim of a case; the rest rest on the
  build's excerpt check and the reviewer's reading alone.
- **Adding concepts weakened three older retrieval expectations.** Eleven
  more concepts lower every rarity weight of the lexical index. UAT-21 was
  kept passing by adding English aliases for the permit-card renewal and the
  Saturday closure its facts already state. Three regression cases were
  requalified to what the server now does, not repaired: OOS-2 (an asylum
  question now reads strong, because the published refugee concept shares
  its words; the case now also checks that concept's `not_served`), OOS-26
  (the share fell from 0.5004 to 0.4986, so a query naming a location that
  does not exist reads weak) and N-EN-T1 (`permit-b` now leads the typo'd
  question about a B permit's validity, and `permit-renewal` is the fourth
  hybrid hit, so the step looks within five). See "Retrieval limitations".

## Gaps in the daily-life extension of 17 September 2026

- **Procedures and contacts, not systems.** The four topics serve what a
  newcomer arranges in the City of Zurich (the first-steps checklist, waste,
  parking, a dog, kindergarten entry, the tax return, the radio and
  television fee, a medical emergency). They do not serve the school system
  beyond kindergarten entry and holidays, tax rates, deductions or amounts,
  the dog tax (each municipality sets it), utility tariffs, housing, public
  transport, or the police and fire numbers; the concepts' `not_served`
  lists name these.
- **City of Zurich only.** Waste, parking, kindergarten, school holidays,
  the tax return, the tax office and the medical emergency page are the
  City of Zurich's; `resolve` refuses them for another municipality. The dog
  training duty and the vehicle procedures are cantonal and serve the whole
  canton; the Serafe fee is federal.
- **Collection days are not served.** The waste facts point to the personal
  disposal calendar and the ERZ app; a collection day for a street is
  computed there and not in the release.
- **Dated facts.** The 2026 kindergarten start, the school holidays of
  2026/27 and 2027/28, the 2026 closing days of the City of Zurich permit
  and tax offices, and the deadline of the 2025 tax return (31 March 2026,
  served until the end of 2026, so after the deadline) end on the dates
  their pages give; the Züri-Sack shop prices are those of June 2025 as the
  page states them.
- **Two sources, two deadlines.** The City of Zurich's first-steps page says
  new number plates are collected in person within 14 days after a move
  from another canton; the Canton of Zurich page describes the online form,
  documents by post and plates arriving within 5 to 10 working days. The
  release serves both as their pages state them (UAT-29 expects both).
- **SERAFE AG is not an authority.** The company collects the fee on the
  Confederation's mandate; the release records it as a federal public-law
  body, the closest of its institution kinds, and its pages as German
  (`page_languages`; they declare `de_CH`).
- **Tables read from page attributes.** The fee tables, school holidays,
  prices and the City of Zurich naturalisation office's telephone hours are
  data tables whose content is an attribute of a web component, not page
  text; the extractor reads them since version 0.2.2 (17 September 2026) and
  marks the blocks, so the verbatim-text check of the extraction skips them.
  Re-extracting the saved pages renumbered their blocks; the build found
  every earlier citation again by its text, and two citations whose range a
  new table now split were re-cited by hand.

## Gaps in the office contacts of 17 September 2026

- **What a page does not publish is not served.** The Canton of Zurich
  office pages give no directions (only a link to a Google route), the City
  of Zurich pages only a public transport timetable link; directions are
  served for the SVA Zurich alone. The telephone hours the City of Zurich
  naturalisation page refers to are a data table, served since release
  `mvp-zurich-2026-09-17-v2`. Postal addresses that appear
  only in a page footer (the SVA Zurich's) are not served. Appointment slots
  are live data and out of scope.
- **Two versions of one fact.** The Road Traffic Office's locations page
  gives two different counter hours for its Administrative Measures division;
  the release serves both as a statement of the discrepancy
  (`zh-road-traffic-office-locations-11`) and does not choose one.
- **Negative answers rest on the page.** "No e-mail address" (the Migration
  Office), "closed on Saturday" (the Population Office) and "no location in
  Oerlikon" (the Road Traffic Office's list of eight) are served because the
  pages say so or list their locations completely; the list fact was added
  after the review of the other office facts and confirmed separately. For an
  office the release does not publish, the caller must decline, not infer.
- **Dated closing days.** The special opening days are served for 2026 (SVA
  Zurich, Road Traffic Office) and 2027 (Road Traffic Office) until the end of
  their year; later years need a re-download. A page can change its hours at
  any time, and nothing re-fetches it before the next rebuild.
- **Offices named elsewhere are not all covered.** The Zivilstandsamt, the
  Betreibungsamt, the passport office and the municipal residents' offices
  outside the City of Zurich have no contact facts. A question about their
  opening hours reads `weak` when its words match no concept, but
  "Öffnungszeiten Zivilstandsamt Zürich" and "Öffnungszeiten Betreibungsamt
  Zürich" read `strong`, because the shortened word stems collide with terms
  of the naturalisation concepts (see "Retrieval limitations").
- **The City of Zurich contact cards are read from page attributes.** Their
  address and telephone are attributes of a web component, not page text;
  the extractor reads them since 17 September 2026 and marks the blocks, so
  the verbatim-text check of the extraction skips them.

## Gaps in the extension of 15 September 2026

- **Statements the acceptance-test document expects that no cited page
  states.** The expected answers of UAT-8 to UAT-17
  ([user-acceptance-tests.md](docs/product/user-acceptance-tests.md)) were
  written before the pages were read in full and corrected on 15 September
  2026 after the review; the release serves what the pages say. The
  differences were:
  - UAT-9: that the mandatory part of the pension assets stays on a
    vested-benefits account or policy in Switzerland (and variation 9d, that
    the served facts name the account or policy). Neither the BSV answer nor
    the Vested Benefits Act states it; the release serves FZG Article 4
    instead (the insured person names a permitted form of keeping the
    pension cover, otherwise the vested benefit goes to the substitute
    occupational benefit institution).
  - UAT-12: that the served facts state no fine. The ch.ch page states that
    an exchange is still possible after the twelve months but a fine may be
    charged, and the release serves that statement; it states no amount.
  - UAT-12, variation 12b: that the additional theory test for categories C,
    D, C1 and D1 applies to an Austrian licence. The Canton of Zurich page
    states that test for the second list of states only; a licence from the
    first list, Austria among them, needs neither a control drive nor a
    theory test.
  - UAT-13: "driving lessons" in the route after a failed control drive. The
    Zurich page names theory test, learner's licence, traffic awareness course
    (Verkehrskunde) and driving test.
  - UAT-16, variation 16e: a fee amount on the City of Zurich page. The
    page's text states only that the city charges a fee; the amounts (none
    under 25, CHF 500 over 25) are in a data table the extractor read from
    17 September 2026 on, so release `mvp-zurich-2026-09-17-v2` serves them
    and the variation now expects them. The CHF 200 on the city's pages is
    the fee for Swiss citizens acquiring city citizenship, which the release
    does not serve.
  - UAT-17: the source term `eheliche Gemeinschaft`. The excerpts use the
    inflected form `ehelicher Gemeinschaft`, which the concept carries
    instead.
  - UAT-14: the SVA Zurich's competence since 1 October 2023 is stated on the
    Canton of Zurich premium-reduction page, not on the SVA Zurich exemption
    page the document names; the release cites the Canton of Zurich page.
- **Rules a cited page states that the document calls unpublished.** The
  SEM page describes the facilitated naturalisation of spouses living abroad
  (UAT-17b), and the Canton of Zurich tax-at-source page the liability of
  persons resident abroad (UAT-10e). The release does not serve either, and
  the concepts' `not_served` lists say so.
- **A dead catalogue link.** The Canton of Zurich page "Wichtige
  Informationen für Ihre Kontrollfahrt" listed in `sources.md` answers
  HTTP 404 and could not be cited; the control-drive facts cite the
  preparation page and the exchange page. The link is to be dropped with
  the next catalogue revision and rebuild.
- **Catalogued but not curated.** The added topics cite 27 of the 47
  explicit pages of the extension's catalogue, plus the ESTV and FOPH
  insurance-duty pages of the rehearsal's catalogue. The pages on family allowances (BSV, SVA Zurich), on income
  compensation for parents (BSV), the ZAS pages on leaving Switzerland and on
  bilateral agreements, the SEM page on the third generation, the ch.ch pages
  on naturalisation and on moving to Switzerland, the Swiss Citizenship Act
  and Ordinance, the Federal Direct Tax Act, the Health Insurance Act, the
  SVA Zurich request page, the Canton of Zurich overview pages and the City
  of Zurich pages on city citizenship, German and basic knowledge carry no
  fact.
- **Pages without a language.** The SVA Zurich pages declare no language.
  Since release `mvp-zurich-2026-09-17-v1` the curation file records
  `svazurich.ch` as German (`page_languages`), so their documents and
  excerpts carry `de`; the language is the curator's reading, not the
  page's declaration.
- **The treaty, not its implementation.** The `fza-*` facts state what the
  Agreement on the Free Movement of Persons says, in its consolidated version
  of 15 December 2020. They do not state how Switzerland applies it (the
  Ordinance on the Free Movement of Persons, VFP/OLCP, is not in the
  release), which permit letter a situation leads to, the transitional
  quotas and safeguard clauses of its Article 10 (Croatia), the conditions of
  the EU acts it refers to (the right to remain, social security
  coordination), or the EFTA Convention, which grants EFTA nationals the
  same rights. The facts are routed to `population` `eu_efta` like the other
  EU/EFTA facts, although each statement names the EU member states only.
- **Zurich only.** For another canton, the added topics serve their federal
  facts and nothing cantonal: no other canton's tax-at-source rules, licence
  lists, premium reduction or naturalisation conditions. A municipality of
  the Canton of Zurich other than the city is served the federal and the
  cantonal facts and nothing municipal. Three weaknesses follow, which the
  cross-jurisdiction cases UAT-35 to UAT-44 and the `XC-` and `XM-` cases of
  the regression pack measure:
  - **The caveat is per topic, and its effect on callers is not measured.**
    A concept answered for Bern or Winterthur carries the gap
    `more_specific_jurisdiction_not_published`, which names the deepest level
    that applies there and the places the topic serves more deeply (`CH-ZH`,
    `CH-ZH-261`), and `guidance_for_caller` tells the caller to say so and to
    carry nothing over. The server knows which levels a topic publishes, not
    which concepts belong together, so the gap also rides on a purely federal
    concept of a topic that holds a Zurich level: the radio and television
    fee is served for Lugano with a caveat about the City of Zurich tax
    return, its only neighbour in the topic. A topic that serves every place
    equally deeply (the cantonal migration offices) or federally only (social
    insurance) carries none. No live caller has been run against the gap yet.
  - **National and cantonal rules published on a narrower page only.** A
    fact is served where the level of its cited page contains the user's
    place, whatever the reach of the rule. The end of tax at source on
    marrying a Swiss citizen or a C permit holder and the single attempt at a
    control drive are served from Canton of Zurich pages only, so not in
    another canton; the emergency number 144, the blue-zone times, the
    kindergarten cut-off date and the leash season in the forest are served
    from City of Zurich pages only, so not in Winterthur or Uster. The
    ch.ch summary that is served everywhere says that a licence from outside
    the EU/EEA requires a control drive, without the list of exempt states
    that the Canton of Zurich page carries, so the answer for a US or
    Japanese licence is coarser outside the canton.
  - **Search knows the place only when the caller sends it.** Without a
    `jurisdiction`, a question from another place ranks the Zurich concepts
    too, and they can crowd the applicable concept out of the first three
    hits: see "Retrieval limitations".
- **Live caller runs.** The 17 cases UAT-1 to UAT-17 ran three times through OpenCode
  against the published image of an earlier release
  (`ghcr.io/bobrovsky420/swiss-tip:mvp-zurich-2026-09-16-v2`, hybrid
  search) on 16 September 2026 and every session was graded (record
  `.local/experiments/2026-09-16-opencode-image-acceptance.md`): the trap
  held in 52 of 54 assessed turns and every criterion was met in 10; 42
  answers added a specific no tool result supports, 6 cited a URL the
  server did not return or none at all, and 17 turns exceeded the call
  budget, all of them the exploratory residence cases UAT-2e and UAT-4 to
  UAT-7, which search 5 to 13 times. Every answer to the four non-English
  cases was in the question's language. On 15 September, against the local
  server before the tool results were shrunk, 32 of 55 turns had exceeded
  the budget and 38 of 52 answers had added specifics (record
  `.local/experiments/2026-09-15-opencode-kb1-extension-acceptance.md`).
  The grades are in `releases/mvp-zurich/acceptance-answers.json`; the
  answer check of the readiness gate stays advisory. The office-contact
  cases UAT-18 to UAT-23, the daily-life cases UAT-24 to UAT-34 and the
  cross-jurisdiction cases UAT-35 to UAT-44 have no live run yet, so whether
  a live caller carries Zurich details over to a user in another canton or
  municipality is specified and not yet measured.

## Freshness and source drift

The release carries a snapshot date of 18 September 2026 and goes stale on
17 November 2026, after which `resolve` returns `STALE` for a later `as_of`
date. The snapshot date is the latest access date of a cited page: 25 of the
139 cited documents were accessed on 18 September, 46 on 17 September, 39 on
15 September, three ch.ch pages on 14 September and the other 26 on 10 and 11
September, so 114 of them are one to eight days older than the date the
release states. That check
compares dates only. Nothing re-fetches a source page to see whether it
actually changed since the snapshot, so a page rewritten by its publisher
reads as fresh until the next rebuild. Drift detection is designed but not
implemented.

## Gaps in the sources

- **1,294 PDF pages carry no embedded text** (237 documents of the
  nationwide catalogue). OCR is out of scope, so their content is not
  extractable and not citable.
- Of the 517 pages the KB1 catalogue and its link-following reached, 5
  answered not-found and could not be cited: four discovered SEM entry pages
  and the Zurich control-drive page above. The Fedlex pages are JavaScript
  application shells: the fifteen acts, ordinances, the treaty, the two
  constitutions and the Code of Obligations were resolved to their dated
  documents; the three Federal Publications language variants, also shells,
  were not. The Federal Office of Justice's leaflet on marriage in
  Switzerland answered HTTP 502 when the sources were located and is not in
  the catalogue.

## Routing defects the regression pack found

- **What the health insurance wave cost the regression pack
  (23 September 2026).** Taking the topic from eight concepts to seventeen moved
  the rankings across the whole pack, and the replay of
  `mvp-zurich-2026-09-23-v13` shows both directions of it. Sixteen quarantined
  cases now pass lexically and fifteen with hybrid search. Five cases were lost
  and are quarantined with the measurement behind each: Q-EN-17 and XC-12 still
  find the concept they ask for and only fell from `strong` to `weak`, because
  `match_strength` is a share of the lexical weight and the topic grew;
  Q-EN-79 lost to `health-insurance-deadline`, which now carries the answer at
  least as well as the two-fact `health-insurance-enrolment` it asks for;
  Q-DE-13, Q-DE-60 and Q-DE-101 lost lexically to a health insurance concept and
  pass with hybrid search; XC-13 and XM-16 lost the other way round. Measuring
  each match named one mechanism: the tokeniser stems to six characters and a
  short alias contributes each of its tokens on its own, so one everyday German
  word can carry a concept into an unrelated question - `krank`, `hohe`,
  `anpass`, `arbeit`. Six aliases written in that wave were removed for it,
  which recovered XM-16 lexically; `Mutterschaftsurlaub` and
  `Mutterschaftsleistungen` cannot be separated at all, because six characters
  make them the same token.

- **What the work and unemployment wave cost the regression pack
  (23 September 2026).** Almost nothing, in contrast with the health insurance
  wave the same day. Twelve new concepts and a new topic left the lexical replay
  of `mvp-zurich-2026-09-23-v16` with no blocking failure at all, and cost the
  hybrid replay one case: Q-EN-83, where the concept the case asks for is still
  found and only its `match_strength` fell to weak as the release grew from 183
  concepts to 195. It is quarantined with that measurement. The difference from
  the earlier wave is most likely the alias discipline adopted after it - every
  alias written here is a distinctive compound noun or a full question, and none
  is a short phrase of common German words of the kind that hijacked four cases
  in the morning.

- **What the AHV wave cost the regression pack (23 September 2026).** Eleven new
  concepts and a new topic cost four cases, of which one was repaired at the root
  and three are held. The repair is the instructive one: the English sample
  question of `swiss-social-insurance-map` began "I have just moved to Switzerland
  - can you explain how the pension system works here?", and its everyday tokens
  took a question about school information in Tamil away from
  `city-zurich-school-languages`. The question was reworded to name the three
  pillars and a generic alias dropped, which restored the case - the rule learned
  for aliases in the health insurance wave applies to sample questions too. A
  second repair followed after the review, when two generic entries on
  `health-insurance-billing` were dropped and recovered XM-17. Of the three held,
  two are share-based strength drops where the concept is still found, and the
  third, Q-EN-100, is held for a reason worth reading: the concepts that now
  outrank the expected one are the ones a reader would reach for, but the release
  answers that question nowhere, so the case waits for a source rather than for a
  ranking fix.

- **A fact served to a group its statement excludes.**
  `zh-foreign-licence-exchange-11` ("professional drivers other than those
  with a licence from an EU or EFTA state must exchange the licence before
  their first professional drive") carries no `licence_state` condition, so
  it is served next to `zh-foreign-licence-exchange-10` (EU/EFTA
  professional drivers need not exchange before their first drive) when the
  licence is from an EU state. The statement names its group, so a careful
  caller reads it correctly, but the routing does not keep it away. The
  regression case CTX-25 is quarantined for it.
- **UK nationals since 2021 get no admission conditions.** For `population`
  `uk_new` the release serves that a work permit under the AIG is required
  (`uk-new-employment`), but the AIG admission conditions
  (`third-country-work`: qualified workers, the priority of the domestic and
  EU/EFTA labour markets) are routed to `third_country` only and are
  rejected for a UK national with `context_not_covered`. Whether they apply
  to UK nationals is a curation question the release does not answer.
- **The permit letter S is not searchable lexically; F and N are since
  22 September 2026.** `permit-types` lists every permit card, and since
  release `mvp-zurich-2026-09-19-v10` its search words name the F, N and S
  cards too ("Ausweis F", "Asylsuchende", "Schutzbedürftige", "F permit
  provisionally admitted foreigners"). Until swisstip-runtime commit 603fa23
  lexical search dropped one-letter words, so no card letter reached the
  concept; since then one-character tokens are kept, and "A colleague of mine
  has an F permit. What kind of permit is that?" ranks `permit-types` third
  lexically and first in hybrid search, the mode the published image serves
  (it was 46th). The verdict still reads `weak` in both modes, because "kind"
  matches the German "Kind" of the family concepts, so Q-EN-76 stays
  quarantined for that reason. The letter S is a stopword: "s" is the Zurich
  German article ("Wo isch s Amt z Winterthur?"), so an S card reaches the
  concept through the embedding only, and a pack that names a type S or Z
  pays for that choice; the S permit is listed, not published, and OOS-45
  stays quarantined. The publisher's "vorläufig aufgenommene Ausländer" was
  left out of the search words because it made the out-of-scope question on
  applying for temporary protection ("vorläufiger Schutz") read `strong`.

## Plain-language sources, and places outside the Canton of Zurich

- **Some statements rest on a publisher's plain-language summary.** The
  premium-information service priminfo.admin.ch states on every page that it
  is written in plain language (Leichte Sprache), and ch.ch is the
  Confederation's portal summary. Where a fact rests on one of them the
  citation says so, its basis is `summary`, and the conditions and exceptions
  behind it rest on the authority's own page or on the law. Search weighs an
  act above a portal summary of the same rule.
- **Outside the Canton of Zurich the pack publishes the migration-office
  contact of the canton**, and nothing else cantonal or municipal for that
  place. A caller in another canton gets the federal facts, that contact, and
  the caveat `more_specific_jurisdiction_not_published`.

## Customs: what the release does not publish

- **The duty-free quantities per product are not served.** The Federal Office
  for Customs and Border Security publishes the table of kilos, litres,
  alcohol strengths and age limits as a graphic, which the text extraction
  cannot read. `customs-duty-free-quantities` states the rule behind the
  table - private use free of duty, sensitive goods charged above a quantity,
  counted per person and per day - and says in its `not_served` that the
  quantities themselves are not published here. A caller that states them is
  inventing them, which UAT-73 tests.
- **Tariff numbers, duty rates per product and the treatment of one
  particular consignment** are named in `out_of_scope`; DECLINE-11 checks the
  refusal.
- **Two cited FOCBS pages date the same period differently.** The FAQ on
  removal goods counts the two years of uncleared use of a vehicle from the
  first day of entry; the page on moving with a vehicle counts them from the
  change of residence. Both statements are served, each from the page that
  says it, and each names the other in its notes. The release does not
  resolve the difference, because neither page does.

## Basic health insurance: what the release does not publish

The wave of 23 September 2026 took the `health-insurance` topic from eight
concepts to seventeen and served much of it from the act and the ordinances
(KVG, KVV, KLV) beside the Federal Office of Public Health's own pages, because
those pages state the cost-sharing amounts without a date. Four things are
deliberately absent, and an answer that supplies them is not coming from this
release.

- **No premium, and no calculator.** The release publishes what makes premiums
  differ - the canton, the premium region, the age group, the chosen franchise
  and model - and never an amount, an average or a rate. The federal premium
  comparison exists and the release does not reproduce it.
- **No ombudsman, and no complaint route.** The plain-language portal names an
  ombudsman as where to go when an insurer does not settle a bill. No official
  source in this release carries that body, so `health-insurance-billing`
  declares it as not served, together with how long an insurer may take to
  reimburse and what to do when the bill cannot be paid.
- **No European health insurance card.** The card appears in this corpus only on
  a plain-language page, which may not carry a statement on its own (D4 of the
  work order). What the release serves instead is the ordinance's own rule: the
  insurance pays for treatment abroad in an emergency, an emergency needs a
  temporary stay and a return journey that is not reasonable, there is none
  where someone travels abroad in order to be treated, and at most twice the
  Swiss amount is reimbursed.
- **No division of a monthly premium.** The plain-language portal states that
  an insurer bills to the day when a child is born at the end of a month, when
  someone registers mid-month or when someone dies. Neither the act nor the
  ordinance says so. What the release carries is the day on which cover begins
  and ends (KVG Art. 5, KVV Art. 7 para. 3), which is the part that is grounded.

Two further boundaries are worth naming. Supplementary insurance is a contract
under the insurance contract act: the release serves the edge of the compulsory
insurance against it - that an insurer may refuse an applicant, that the notice
periods differ, that the old insurer may not make a change of basic insurance
conditional on giving up the supplementary cover - and not what any policy
covers. And the financing and supervision of the system, including how the
Confederation and the cantons share the cost of premium reductions, is
dispositioned as deferred rather than served, because it is not a question a
resident asks about their own premium.

## Work and unemployment: what the release does not publish

The wave of 23 September 2026 created the topic `work-unemployment` with twelve
new concepts and moved the two existing unemployment concepts into it unchanged.
Five things are deliberately absent.

- **No amount of benefit, and no calculator.** The release carries the rules -
  the waiting days, the percentages of insured earnings, the frame periods, the
  numbers of daily allowances - and never what a person will receive. Where a
  page printed a franc figure the curation quoted it in a reviewer's note rather
  than in the statement.
- **No bridging benefit.** A reader curated it in full from the page on the end
  of the entitlement, with its conditions and its maximum amounts. It is named in
  `out_of_scope` together with the invalidity insurance and the supplementary
  benefits, so those facts were removed before the merge and the page section is
  dispositioned as out of scope.
- **No social assistance.** The page on the end of the entitlement points people
  to the social assistance of their municipality, and the release serves that
  pointer and nothing else - no conditions, no amounts, no procedure. The German
  word was deliberately kept out of the concept's search terms so that a
  social-assistance question reaches the gap instead of the concept.
- **No forms.** The unemployment insurance publishes a page of numbered forms,
  and forms are named in `out_of_scope`; that page is dispositioned in full.
- **No employee's share of short-time work, and no consent rule.** The SECO page
  on short-time work is written for employers and states neither the share of
  the lost earnings that is compensated nor whether the employee has to agree.
  Both are declared as not served rather than supplied from the act.

Two boundaries are worth naming. `employment-notice-and-reference` is a bounded
extract of employment law, not a treatment of it: it carries the four statutory
notice periods, the three protected periods and the right to a work reference as
one SECO page prints them, and its `not_served` list names seventeen things it
does not settle, from abusive dismissal to the contents of a reference. And the
release states the coordination with the EU and EFTA the way the pages state it -
work in a member state does **not** by itself create a Swiss claim, which is the
opposite of what a caller usually assumes.

**A gap left by the extraction.** The table of daily allowance counts by age and
contribution months was not captured when the SECO page was extracted; only its
two footnotes survive. The release therefore carries the additional 120 daily
allowances for older insured persons and the maximum of 180 after a disability
pension ends, but not the base counts - the core of "how many daily allowances do
I get". Re-extracting that page would be needed to serve them.

## AHV, the pillars and retirement: what the release does not publish

The wave of 23 September 2026 created the topic `ahv-pension` with eleven
concepts. Two of the things the wave set out to serve turned out not to be on the
pages at all, and saying so is more useful than approximating them.

- **No apportionment of a pension between countries.** The plan expected the
  international concept to state that each state pays its own pension for the
  periods completed there, and that insurance periods are taken into account for
  the entitlement. Neither rule appears on either of the two international pages
  of the AHV/IV information service, which cover only which country's system a
  person is subject to, postings and the A1 certificate. Nothing was written for
  them, and `ahv-international-coordination` declares the gap. A caller asking
  whether their French years count towards a Swiss pension gets no answer from
  this release, and a regression case is held open over exactly that question.
- **No reduction or supplement rate for drawing a pension early or late.** The
  page states only that both are calculated on actuarial principles. The familiar
  percentages are not served.
- **No pension or contribution amount, and no calculator.** Where a page printed a
  franc figure it is quoted in the fact's provenance note rather than in the
  statement, so a reviewer can see it without the release publishing it.
- **No invalidity insurance, supplementary benefits or bridging benefit.** All
  three are named in `out_of_scope` and appear in this topic only as things
  explicitly not covered - including the rule that the thirteenth pension reaches
  old-age pensions only, so survivors' and invalidity pensions stay at twelve a
  year.
- **Only one of the 26 cantonal compensation offices.** The directory page lists
  them all with addresses; only the Zurich entry is served, and the office's
  address and opening hours are left to the Zurich office-contacts topic.

**A defect in a source that the release shows rather than hides.** The page on
old-age pensions still states the pre-reform reference ages, 64 for women and 65
for men, in the present tense beside the paragraph giving the rule in force since
1 January 2025. `ahv-reference-age-2` leads with the rule in force, keeps 64 as
the base the three-month steps rise from, and reports that the page still carries
the stale sentence. Both blocks are cited.

**Nine facts are cantonal that read as federal.** The individual AHV account and
most of the contribution-gap material rest on SVA Zurich pages alone, and the
build refuses a federal statement resting only on a cantonal source. They are
served as `CH-ZH`, so a caller outside the Canton of Zurich is told the release
does not speak for their canton on those points.

## Retrieval limitations

- **Authored search words are the assistant's, and they move rarity
  weights.** All 206 concepts carry authored aliases and at least one
  English and one German sample question; the build refuses a concept
  without one in each language (`question_languages` of the curation, told
  by the questions' function words). On 19 September 2026 the last 13
  concepts without questions (`aig-short-stay`, `aig-study`,
  `integration-criteria`, `family-c`, `canton-change`, `biometric-permit`,
  `language-evidence`, `zh-eu-l`, `zh-eu-b`, `zh-eu-self-employment`,
  `zh-eu-nonworking`, `zh-eu-family-documents`,
  `zh-third-country-retirement`) got everyday English and German aliases and
  a question in each language, 37 concepts with English questions only got
  a German one, and two got a third English question for a gap a
  quarantined case showed (children joining a C permit holder need no
  language proof, a temporary job still needs a work permit). The assistant
  wrote them from the concepts' facts and reworded every one that came close
  to a test question; no fact changed. Fourteen quarantined regression cases
  now pass the hybrid replay and are blocking again, among them the
  integration-criteria, study-admission and health-condition questions, the
  C permit in German (Q-DE-4), an EU worker's adult son and an EU retiree's
  means. The pack passes 537 cases lexically and 530 with hybrid search, of
  560, where release `mvp-zurich-2026-09-18-v19` passed 529 and 518, and 30
  are quarantined instead of 43. The German questions did not help three
  German and French questions on the permit authority and cross-border
  commuters (Q-DE-1, Q-DE-20, Q-FR-4), which stay quarantined. The words
  are not neutral: drafts made fifteen passing cases fail, because a rare
  word weighs a lot ("ziehe" pulled a Zurich registration question to
  `canton-change`), a word added to more concepts weighs less everywhere
  ("Ehefrau", "Kanton", "Bürger", "abschliessen" lowered the match strength
  of UAT-7, Q-FR-12, Q-IT-7 and a Bern health insurance question), "für" is
  not a stop word of the search (it matched the Turkish key terms "fuer"),
  and generic English words on the Zurich EU permits took a Bern question
  from the treaty concept. The released wording repairs all of them except
  Q-EN-2 ("What is the difference between an L permit and a B permit?"),
  quarantined again because the German question diluted `permit-l`'s
  English embedding and lexical search never found it; Q-DE-79 (see "The
  treaty concepts compete with the pages that apply it") stays quarantined.
  Since release
  `mvp-zurich-2026-09-16-v3` fourteen concepts also carry everyday,
  Germany-German and colloquial aliases (Einwohnermeldeamt, Führerschein,
  Aufenthaltserlaubnis, Familienzusammenführung, Lohnsteuer, "roter Pass",
  OASI, the German names of the French- and Italian-speaking cantons).
  Release `mvp-zurich-2026-09-19-v10` adds four more on request: "pendeln"
  and "Pendler" for cross-border commuters, "Mieterhöhung" next to the
  publisher's "Mietzinserhöhung" (with the source term "Renovationen"), and
  the Zurich German "Migrationsamt Züri". The rent and dialect questions
  (Q-ES-6, N-DE-J9) now pass in both modes and are blocking again, and no
  other case changed. The commuter question (Q-DE-20) stays quarantined:
  its concept rose to sixth lexically, below concepts that match "wohne",
  "Deutschland", "Stelle" and "Zürich". The pack now passes 539 cases
  lexically and 532 with hybrid search, of 560, with 28 quarantined.
  Release `mvp-zurich-2026-09-22-v1` shows the same weighting from the other
  side. Its two settlement-agreement concepts carry the publisher's
  "Niederlassungsvereinbarung" and "Niederlassungsvertrag", which the
  six-character prefix stem folds into the same token as
  "Niederlassungsbewilligung": eleven concepts now carry that stem instead of
  nine, its rarity weight fell, and the German question "Ab wann erhalte ich
  die Niederlassungsbewilligung C?" (Q-DE-4) lost `permit-c` from the first
  three lexical hits. The case was never won on merit: `permit-c`, `family-c`
  and `tax-at-source-liability` tie on that one stem (8.28 before, 7.76
  after), while the two concepts that outrank them match `erhalt`, a stem
  only two concepts carry, and neither of them answers the question. Q-DE-4
  is quarantined for the lexical mode with that measurement; it passes with
  hybrid search.
- **A verdict is release-size dependent, and twenty concepts moved eight of
  them.** `match_strength` reads `strong` when the anchored weight of the
  query reaches 1.5 or its lexical share reaches 0.5. The weight is an
  absolute sum of rarity weights, and every concept added to a topic lowers
  the weight of the words that topic uses, so a query whose weight sat just
  above the line crosses it when the release grows. Between
  `mvp-zurich-2026-09-19-v15` (133 concepts) and
  `mvp-zurich-2026-09-22-v1` (151), eight questions fell from `strong` to
  `weak` **without their ranking changing**: Q-DE-37 (1.5574 to 1.4559),
  Q-EN-99 (1.6017 to 1.4971), Q-IT-7 (1.5165 to 1.4619), XC-39 (1.5002 to
  1.4559), XC-45 (1.5433 to 1.4174), N-EN-A4 (1.5665 to 1.4803, while its
  concept rose from third to second), Q-FR-12 (share 0.5000 to 0.4812) and
  the question of the acceptance case UAT-46 (1.5759 to 1.4258). In every
  one of them the expected concept is still the first hit. They are
  quarantined in the regression pack with their measurements; UAT-46 is
  listed in `scripts/test/packs/test_match_strength.py`, whose question
  bank otherwise requires a strong verdict. A caller that treats `weak` as
  "not covered" declines a question the release answers, which is the cost
  of this drift; raising or normalising the threshold is a change to
  `service.py` in the code repository and has not been made. The cantonal
  wave of 23 September 2026 added 124 facts to the residence topic and moved
  exactly one more: the acceptance case UAT-56 fell to `anchored_weight`
  1.4386 with `lexical_share` 0.4145, `tenancy-agreement` still its first
  hit. Measured against the committed release, that and one false positive
  below are the **only** two verdicts this wave changed. Thirteen further
  suite questions (UAT-43, 44, 63, 85, 87, 88, 92, 98, 103, 104, 107, 110,
  111) fail the same test on the committed release and pre-date the wave;
  they are deliberately **not** allowlisted, so the test still reports them.
  Corrected on 24 September 2026, when the packs were first checked on
  0.3.0: they are now pinned as weak in that test, in two groups. In UAT-43,
  63, 85, 87 and 98 the expected concept is still the first hit and only the
  verdict fell. In UAT-44 it ranks second and in UAT-88, 92, 103, 104, 107,
  110 and 111 it is not among the first five, so lexical search on the full
  question misses it and `weak` is the right verdict; their search steps are
  strong. Those eight are a retrieval gap to close in the data.
- **The coverage report: 975 units nobody has answered for.** The
  `coverage` stage joined the text dataset of the run with this release on
  22 September 2026 (`releases/mvp-zurich/curation-coverage.json` and `.md`).
  Of 337 candidate records it asks for 2,077 units: 321 pages by their
  content sections, 15 statutes as one unit each (a curator cites articles
  from a law; its other articles are not a gap), one tariff page rolled up to
  its top two heading levels, and 75 sections of repeated site boilerplate
  set aside and traced to their citations. Nine texts recur on five or more
  pages: the Migrationsamt's Berninastrasse address with its counter hours
  (nine pages) and the Stadthaus Einbürgerungen address (five) are each cited
  once, from the office's own page; the sentence that documents can be handed
  in at the counter, online or by post is a fact on five of the seven
  application guides that carry it; four texts are cited nowhere and rightly
  so (an SVA browser warning, the SEM directive list a navigation rule
  covers, two variants of the Migrationsamt's notice of a closure on
  14 September 2026); and an accordion widget instruction on 25 Canton of
  Zurich pages lies inside cited block ranges on two of them, which a
  reviewer may narrow. The threshold is the pack's `boilerplate_min_pages`
  (the default five, counted per host); below it the text index still marks
  283 sections on 98 candidate records as repeated on two or more pages of
  their host, and the reading views carry the mark on every block, so a
  reader knows a card is a card before deciding what to cite. Facts cite 558
  units; 41 dispositions (23 drafted by the assistant and reviewed and signed
  by the pack's reviewer on 22 September 2026, two deferrals and sixteen
  entries recording the reviewer's two scope decisions of the same day)
  settle 544 more (the French and Italian SEM pages as duplicates of the
  cited German ones, sixteen hub and link pages as navigation, five asylum
  pages against the manifest's `asylum` entry, and the integration pages
  described below); **975 units in 156 documents are
  unclassified**. Two groups, 309 units, needed a scope decision, taken on
  22 September 2026. SEM's border-management and air-carrier pages (30 pages,
  75 units) are deferred by two `deferred` rules until 31 December 2026, when
  the decision falls due again. Of the Canton of Zurich's 27 integration
  pages (234 units) the reviewer took the resident-facing seven into scope:
  30 of their sections are now cited by the 25 facts of the `integration`
  topic, and the rest of those pages is dispositioned section by section
  (the other funding areas of the programme and the training offers for
  authorities as `out_of_scope`, the leads and the pointers that repeat a
  cited page as `duplicate`, the database widget as `navigation`, and the
  past calls, the events placeholder and the canton's two reports on racism
  as `deferred` until 31 December 2026). The other 20 pages, the support
  system for refugees (Integrationsagenda IAZH) and the cantonal integration
  programmes, are `out_of_scope` against the manifest entry added that day.
  The rest is content someone saved and nobody read: among it the SEM FAQ
  pages, of which the pack cites a handful of answers out of forty to seventy
  each (128 open units), and 414 units on Canton of Zurich pages. The pack
  runs the stage under `coverage_policy: report`; the number is a fact about
  the release, not yet a build error.
- **Four concepts of 22 September 2026 displaced an expected concept.**
  `city-zurich-naturalisation-language` and `-civics` pushed
  `city-zurich-naturalisation` from third to fourth of 44 for the German
  question of Q-DE-5; `zh-family-fza` took the third place of `fza-overview`
  for Q-EN-84, which asks about non-discrimination, because its label
  carries the publisher's "Freizügigkeitsabkommen"; and in hybrid search
  `zh-third-country-work` displaced `third-country-work-procedure` (Q-EN-9,
  Q-TR-1) and the three Zurich family concepts displaced `family-b`
  (CTX-5). All four cases are quarantined with the measurement, and Q-EN-9,
  Q-TR-1 and CTX-5 pass again in the lexical mode.
  The pack now passes 556 cases lexically and 555 with hybrid
  search, of 587, with 44 quarantined. Three more cases were quarantined
  after the review of 22 September 2026: confirming the new concepts raised
  their prior from 0.7 to 1.0, and in hybrid search `permit-card-eu-efta`
  took the fifth place of `permit-renewal` (N-EN-T1), the three Zurich
  family concepts took all three places of `family-eu-efta` (Q-EN-78) and
  `naturalisation-third-generation` took the second place of
  `zh-naturalisation-facilitated` (XM-18). All three still pass lexically.
  With the tokeniser of swisstip-runtime 603fa23 (one-character tokens kept,
  22 September 2026) three quarantined cases pass again in both modes and
  are blocking again: CTX-5, N-EN-A4 and Q-TR-1; the pack passes 557 cases
  lexically and 553 with hybrid search, of 587, with 41 quarantined.
- **Lexical search has no spelling tolerance.** A misspelled key word is a
  missing token: "helth insurence" or "renwe" lose the strong match that the
  correctly spelled question gets, and the container's lexical fallback
  (without Ollama) declines such a question as a weak match. Hybrid search
  absorbs them: in the measurement of 16 September 2026 (record
  `.local/experiments/2026-09-16-query-noise-typos-jargon.md`) all 25
  questions with typos, ASCII umlauts, jargon or abbreviations found their
  concept with hybrid search, 20 with lexical search alone. Umlauts, their
  ASCII spelling and the plain form ("Zürich", "Zuerich", "Zurich") are
  folded to one word since that release. Hybrid search does not absorb
  every such question: the regression pack keeps three quarantined that read
  `weak` or miss their concept in both modes, "personenmeldeamt
  öfnungszeiten" and two English questions with typos or slang (the
  documents for an EU employment permit, a company director who wants to
  "sign on for the dole"). The Zurich German "Wänn hät s Migrationsamt Züri
  offe?" passes since the alias "Migrationsamt Züri" of release
  `mvp-zurich-2026-09-19-v10`. Two more pass with hybrid search only: the Zurich German "Wie lang
  darf ich ohni Bewilligung i de Schweiz blibe, wenn ich nid schaffe?",
  which the everyday aliases of `aig-short-stay` reach, and paying into
  pillar 3a while unemployed.
- **Search terms are German and English only.** The 1237 source terms the
  build counts are copied verbatim from the cited excerpts. The
  English ones reach 25 of the 151 concepts, those whose federal page has an
  English version the release cites; the Canton and City of Zurich pages
  carry none, so a question about a Zurich procedure matches only authored
  English words, the labels, the sample questions and the statements. French
  and Italian terms reached, until 23 September 2026, only the cantonal
  office names. The cantonal wave added 30 copied verbatim from Vaud, Valais
  and Ticino pages, so a French or Italian question about registering on
  arrival now finds its concept directly rather than having to be translated
  into German first; no other subject is reachable in those languages, and
  `question_languages` stays German and English. Swiss German is covered by
  three authored spellings
  for one acceptance case, not generally: an unlisted dialect spelling matches
  nothing.
- **Semantic search is optional and off by default.** The prebuilt index of
  the 151 concepts is committed, but embedding an incoming query needs a
  matching local Ollama model. Without it the server uses lexical search. The
  recorded experiment improved concept discovery on an earlier release, not
  final answers; it has not been evaluated on separate development data, on
  the added topics or in a controlled caller experiment.
- **The treaty concepts compete with the pages that apply it.** On the
  committed 42-question retrieval fixture, which predates the `fza-*`
  concepts, adding them lowered lexical recall at 3 from 0.44 to 0.37 and
  hybrid top-1 accuracy from 0.62 to 0.53 (hybrid recall at 3 rose from 0.80
  to 0.83); in the changed cases a `fza-*` concept ranks above the SEM or
  Zurich concept the fixture expects. Search does not filter by nationality:
  a Canadian retiree's question ranks `fza-non-working` first, and only
  `resolve`, with the `population` context, keeps its facts from a
  third-country national. The other way round, the treaty concept is often
  not found when it is the one that answers: the regression pack
  quarantines a visa fee question for the spouse of an EU citizen
  (`entry-visa-fee-insurance`), for which other concepts, mostly
  neighbouring `fza-*`, EU/EFTA or entry concepts, fill the first three hits
  in both modes. An EU worker's adult son asking whether he may work
  (`fza-family-members`) and an EU retiree asking which means she must prove
  (`fza-non-working`) find their concept with hybrid search only, since the
  German sample questions of 19 September 2026. An EU employee who wants to
  become self-employed in another canton (`fza-mobility`, Q-DE-79) finds it
  lexically but not with hybrid search, where the Zurich self-employment
  and non-working concepts rank above it; it is quarantined.
- **Search knows where the user is only when the caller says so.** Since
  19 September 2026 `search` takes an optional `jurisdiction`
  ([tool-contracts.md](https://github.com/swisstip/swiss-tip/blob/main/docs/architecture/tool-contracts.md), section 4.4): the
  concepts that cannot apply at the place are left out of the ranking and
  named in `published_elsewhere`. Replayed on release
  `mvp-zurich-2026-09-18-v19`, before the search words of 19 September were
  added, on the 433 search steps of the
  regression cases that name a canton or a city, lexical search then finds
  the expected concept in 377 of 416 steps instead of 371, hybrid search in
  392 instead of 393, and no match strength changes; the Basel cases below
  are among the seven gained. Three things limit it. No live caller has been
  run with the field, so whether the test model sends it is not measured, and
  the regression pack itself still sends every search without a place, so the
  numbers of this paragraph describe that state. The match strength stays that
  of the whole release: a subject published for Zurich only still reads
  `strong` for a user in Bern, who learns from `published_elsewhere` and the
  guidance that it is not published for their place. And the code is in
  packages 0.2.5 and later: 0.2.4 and an image built on it reject a `search`
  that carries the field. The image Dockerfiles pin 0.3.0, which is not on
  PyPI yet, and build only once it is published.
  Without the field, a question from another canton or municipality ranks the
  Canton and City of Zurich concepts next to the federal ones, and `resolve`
  sorts them out afterwards. Of the 64 cross-jurisdiction questions of the
  regression pack, 49 find the concept that applies at the user's place
  among the first three hits in both modes. Eleven find it with hybrid
  search only, among them: for a German citizen registering in Basel, for a German licence in
  Basel and for the address of the migration office in Basel the first three
  lexical hits are all Zurich concepts, which `resolve` rejects for Basel,
  so a caller on lexical search is left with nothing that applies (the
  office question also reads `weak` lexically in every wording tried,
  because the address and opening-hours words do not count toward the match
  and "Basel" anchors one fact only); the question who decides on a health
  insurance exemption in Schwyz finds two Zurich concepts and the visa
  insurance concept before the federal one; a tariff adjustment for
  maintenance payments in Uster finds its cantonal concept with hybrid
  search only. A change of canton from Zurich to Bern and the cantonal
  facilitated-naturalisation concept for a resident of Kilchberg, which one
  mode missed before, are found in both modes since the search words of
  19 September 2026. Four are quarantined. In two neither mode finds it: a
  six-month contract in Bern (`fza-employee-permit` and `permit-l` are
  outranked by the notification procedure) and the cost of naturalisation
  in Winterthur (the federal and the City of Zurich concept are offered,
  the cantonal one between them is not). Two come from other Zurich
  municipalities: the voting material in Illnau-Effretikon reads `weak`, and
  electronic signatures at the unemployment fund in Horgen miss their
  cantonal concept or read `weak` in both modes.
- **Resolve payloads of the added topics are large.** Resolving the three
  tax-at-source concepts together returns about 18 KB, the three ordinary
  naturalisation concepts about 17 KB, measured on this release with the
  compact result format of 16 September 2026 (each cited page listed once
  per concept, the review fields once per concept) and the two-line
  limitations list of 17 September. A search of three hits adds about 3 KB,
  so such a session uses about two thirds of the 30 KB budget of a
  single-turn acceptance case when the caller makes no further call. The
  Road Traffic Office concept, with 14 facts, returns about 12 KB on its own;
  the Zurich tax-at-source tariff concept about 10 KB, the two voting-rights
  concepts together about 9 KB;
  a daily-life concept about 7 KB (the Züri-Sack or parking concept), the two
  dog concepts together about 9 KB.
  The basis labels of 16 September 2026 add
  about 40 bytes per fact whose basis differs from its concept's, and two
  short fields per citation.
- **The cantonal route concept outranks the cantonal deadline concept.** The
  five `cantonal-*` registration concepts describe the same act from different
  angles, and `cantonal-registration-route` carries the most source terms (23
  against 16 for `cantonal-registration-deadline`). For a question about how
  many days a canton gives, the route concept therefore tends to come first and
  the deadline concept can fall out of the first three hits altogether: no
  Schwyz wording tried on 23 September 2026 put the deadline concept in the
  first three in **both** retrieval modes. Resolving the concept serves the
  right fact, so the release holds the answer and only retrieval is at fault; a
  caller that searches once and resolves only its first hit gets the office
  instead of the period. Q-DE-127 is quarantined with the measurement rather
  than reworded until it passes. Narrowing the route concept's terms would
  trade one concept's findability for the other's and was not done blind.
- **Four pre-existing cases were displaced by the new concepts.** XC-23 lost
  `cantonal-migration-contact` from the first three hybrid hits for a question
  naming the migration office in Basel, to `cantonal-registration-route` among
  others - the new concept describes which office receives a report, so it
  competes directly. Q-AR-1 lost `city-zurich-departure` entirely: all three
  first hybrid hits for "reporting a move within Switzerland online" are now
  cantonal concepts this wave added, which is semantically reasonable even
  though the case wanted the City of Zurich one. Both pass lexically. N-DE-A5
  ("does Croatia count as EU or as a third state?") lost `permit-types` from
  the first three lexical hits to `cantonal-permit-application`, which carries
  both terms in its statements; Q-PT-1 lost `family-separation` from the first
  three hybrid hits to three free-movement concepts. Both pass in the other
  mode, both are quarantined with their measurements, and no fact changed.
- **A second lexical blind spot arrived with a canton's office name.**
  "Wann hat das Passbüro Zürich offen?" was an off-topic question while no
  concept mentioned a Passbüro. Schaffhausen's migration office is *called*
  "Migrationsamt und Passbüro", so since 23 September 2026 the word is
  genuinely in the corpus: the query reaches `lexical_share` 0.7738 and reads
  `strong`, with the Zurich population office and the Zurich Migrationsamt
  contact as its first hits. Zurich's passport office is still not published,
  and the lexical signals cannot see that the caller named a different
  canton's word. Dropping the source term does not help, because the word is
  also in Schaffhausen's served statements, so it is recorded here and pinned
  by a test rather than worked around.
- **The match-strength verdict has lexical blind spots and misses
  other-language questions.** Since 16 September 2026 every `search` result
  says whether the question's distinctive words reached a published
  concept, so an off-topic question (the VAT rate, a Halbtax, the speed
  limit, secondary school) comes back `weak` with the scope statement instead of a
  list of candidates to resolve. The thresholds were measured on this
  release's acceptance questions and fourteen off-topic ones
  ([tool-contracts.md](https://github.com/swisstip/swiss-tip/blob/main/docs/architecture/tool-contracts.md), section 4.1;
  record `.local/experiments/2026-09-16-search-match-strength.md`).
  Since 17 September 2026 facet words (address, opening hours, telephone,
  e-mail and their German forms) no longer count toward the verdict, so
  "opening hours of the Zurich zoo" reads `weak` although the office-contact
  concepts carry those words. Known misses: "Kindergarten Anmeldung Bern"
  reads `strong` (lexically because "Anmeldung" and "Bern" are anchors of the
  arrival and contact concepts, and since release `mvp-zurich-2026-09-17-v2`
  in hybrid mode too, because kindergarten registration is a City of Zurich
  concept; `resolve` refuses it for Bern); the opening
  hours of the Zivilstandsamt or the Betreibungsamt read `strong` in both
  modes, because their shortened word stems match terms of the
  naturalisation concepts; a longer natural question about an office's
  e-mail address ("… I want to send my documents by e-mail") reads `weak`
  in lexical mode and `strong` in hybrid mode; and a French or Italian
  question about a covered subject reads `weak` in lexical mode, because the
  release carries no French or Italian terms. The server therefore names its
  query languages (German preferred, then English) in its instructions, the
  `search` description and the coverage root, and a `weak` result allows one
  search with the key terms translated into German; whether live callers
  translate was not yet measured. The verdict was not yet measured with a
  live caller either.
- **The ranking prior is small and was not measured on this release.**
  Since 16 September 2026 `search` multiplies a concept's score by a prior
  between 0.7 and 1 that follows from the basis of its facts and the review
  of its statements. On the release of 15 September the prior changed the
  top three of 3 of 35 fixture queries and no acceptance case; on this
  release, with the `fza-*` treaty concepts at the highest source weight,
  the effect was not measured, and the concepts of ch.ch pages rank a little
  lower than before.

## Caller behaviour the server does not control

The server returns facts and evidence; the calling assistant composes the
answer. Recorded runs show three behaviours the release cannot prevent:

- **Call counts exceed the budget.** Acceptance cases target 4 tool calls;
  recorded runs used 7 to 12, and one early run 31. Since 15 September 2026
  search drops loose hits (question words, a token found in most concepts,
  hits far below the best score) and its empty-result guidance tells the
  caller not to repeat rephrased searches; on the query set of the release
  of that day that cut the matches per query from 10.1 to 8.2. Since
  17 September 2026 `search` returns 3 hits by default and at most 10, and
  tool results other than `get_coverage` carry a two-line limitations
  list; a shorter topic page is not implemented, and none of this changes
  how many calls a caller makes.
- **Additions from model memory.** In recorded runs the caller added a visa
  step, a fee mention and a document list that the served facts did not
  contain and that the coverage root names as out of scope. Since release
  `mvp-zurich-2026-09-14-v2` the visa caveat for third-country workers is a
  served ch.ch fact; the fee and document additions are not. Since 15
  September 2026 `resolve` guidance tells the caller to cite only the
  returned URLs and add nothing the statements do not contain, and a concept
  can declare what it does not serve; the 19 concepts of the added topics
  declare such lists, as do 8 of the 13 `fza-*` concepts, the 9
  office-contact concepts, the 18 daily-life concepts and the entry-and-visa,
  voting-rights, tariff and expat-life concepts; the other residence
  and contact concepts declare
  none, and the effect
  of the guidance on callers was measured on the Wallisellen release only
  (see its acceptance record).
- **Answer language is not guaranteed.** Without a prompt line asking for the
  question's language, the same model answered a German question and a
  dialect question in other languages. The harness supplies that line; another
  client's harness supplies its own.

## Operational limitations

- **The published image is about 700 MB.** It bundles a CPU-only Ollama and
  the embedding model for hybrid search. The container workflow also builds
  a slim release image without them (about 60 MB to pull, lexical search on
  its own) and an embedding sidecar that supplies the model from a second
  container ([docker/README.md](https://github.com/swisstip/swiss-tip/blob/main/docker/README.md)). The split moves the
  model out of the server image; it does not make it smaller, and hybrid
  search still needs about 1.2 GiB of memory for it. The two-container
  setup was tested on local builds only, not yet as images pulled from the
  registry.
- **The coverage root only fits because a field was dropped.** The
  entry-and-visa extension pushed the root payload from 5,928 to 6,173
  bytes, over the 6,000 that `apps/mcp-server/tests/test_server.py` enforces
  and criterion X8 states. It fell to 5,428 bytes, because a topic on the
  root no longer repeats its jurisdictions (schema `swiss-tip/v3`, packages
  0.2.3); the root's own list and the topic page carry them. The
  voting-rights topic of 18 September 2026 brought it to 5,568 bytes, the
  two expat-life topics and the longer scope statement to 5,777 (the new
  scope wording and two topic descriptions were shortened to stay below
  6,000). Version
  `swiss-tip/v2` on PyPI (0.2.2) serves the field, so a caller pinned to the
  published v2 bundle sees a shape that validator rejects. The scope
  statement, the out-of-scope list and the limitations still grow with every
  topic.
- **The committed release needs packages 0.2.4 or later.** Release
  `mvp-zurich-2026-09-18-v10` carries the place register, a part the release
  format gained with schema `swiss-tip/v4`. The models reject unknown fields,
  so `swisstip-mcp` 0.2.3 and earlier do not load it. Version 0.2.4 is on
  PyPI, `uvx swisstip-mcp` installs it and the image Dockerfiles pin it; the
  images published before it were built on an earlier version and keep
  serving the release and the contract they were built with (the v3 shapes,
  codes only) until they are rebuilt. A caller that read `executed_scope` as
  the three code fields only must accept the names and `not_recognised`
  beside them.
- **Places are recognised by name, not understood.** The place register
  holds the official names of the register of municipalities of 18 September
  2026 and 115 hand-written other-language names for the cantons and the
  larger cities; a smaller town is found by its official local name only. A
  quarter (`Oerlikon`), a postcode, a locality that is not a political
  municipality or a misspelling is not recognised: the request then runs for
  the canton or the country and says so, which a caller may or may not pass
  on. A name the register qualifies is found without the qualifier only
  where it is unique (`Muri` finds `Muri (AG)`, not `Muri bei Bern`, and with
  the canton of Bern given it is an error that names the Aargau one).
  Municipalities merge, mostly on 1 January, and their numbers retire: the
  register is as old as its access date until it is fetched again and the
  release rebuilt, and nothing reports a merger in between. The other-language
  names and the generic words (`Kanton`, `Stadt`, `ville de`) were written
  by an assistant and confirmed by no one; they decide only which place a
  request runs for, never what a fact says.
- **No authentication, no rate limiting, no multi-tenancy.** Over HTTP
  anyone who can reach the endpoint can call it; there are no keys, quotas or
  usage accounting, and a hosted endpoint relies on its host's limits. The container speaks plain HTTP; HTTPS is the host's to
  terminate. The endpoint is stateless and serves a read-only file.
- **One release per process.** `--release` selects it at startup; there is no
  switching at runtime and no release history served to callers.
- **The admin console is a local single-user tool** bound to `127.0.0.1`. It
  writes `curation.yaml`, `sources.json` and `checks.yaml`, records an actor
  with every write, and never commits.

## Testing limitations

- The offline unit tests, the client round trip over stdio (and over HTTP
  against a running container) and the acceptance gate's model-free check
  (the 82 blocking cases of `releases/mvp-zurich/acceptance.yaml`: 66
  questions, 9 resolve declines and 7 search declines) pass without
  network access. They verify the contract, the build, retrieval and, for
  the 247 claims of the suite, that a served statement and a verbatim phrase
  of its cited excerpt still say what the expected answer needs; 31 basis
  expectations in 21 cases pin that the law, a directive, the authority's
  own page or its directory entry stays among the served facts, and 15
  cases name facts that must not be served, 13 of them Zurich facts for a
  user in another canton or municipality. The
  regression pack (505 further questions, twelve of them with the place
  given in names; 44 of 587 replayed cases quarantined) is not a gate. They do not
  verify the truth of a statement, and a statement no claim covers rests on
  the human review alone, one person's confirmation and reading.
- The release's `readiness.json` records that these gates passed on the
  file, with a freshness runway to 17 November 2026; the container serves no
  release without such a record. The record of 22 September 2026 was
  attested by the reviewer after the review of all 712 facts of the release
  that preceded it. Each release since has waited the same way: the assistant
  never runs the ready stage, so a release is served only once the reviewer
  attests it in their own name. `mvp-zurich-2026-09-23-v27`, with all 1,268
  facts reviewed, was attested on 23 September 2026 and supersedes
  `mvp-zurich-2026-09-23-v19`. `mvp-zurich-2026-09-24-v1`, which adds the
  Lugano waste concept with its 5 facts reviewed, was attested on 24 September
  2026 and supersedes v27.
- **The coverage root is close to its bound.** `get_coverage` answers in one
  call under 6 KB, which the pack README promises and the check
  `scripts/test/packs/test_zurich_release.py` enforces. On this release the
  root is 6,040 bytes now that every fact is reviewed and the served
  review-status line names one status; it was 6,074 while the 25 integration
  facts were open. The check's bound was 6,000 bytes and was raised once to
  6,144, the binary kilobyte the README means. The integration topic of
  22 September 2026 pushed the root 194 bytes over that bound, and the bound
  stayed: the new out-of-scope entry was cut to one line and three
  limitations were shortened (the review-history pointer, the office-address
  sentence and the English-excerpt sentence), which paid for the topic and
  for the scope statement's new clause. The next topic added should trim
  that text again rather than raise the bound. The attestation covers the place register only
  through the gates: the register's 2,137 places and the other-language
  names were not read by a person. The answer-quality gate (graded
  live-caller runs bound to the release, `acceptance-answers.json`) is
  advisory: the 52
  graded sessions of 15 September are bound to the earlier release
  `mvp-zurich-2026-09-15-v2`, without the `fza-*` concepts, the basis labels,
  the office contacts and the daily-life topics, so the record notes the
  mismatch and does not block.
- **The live caller runs are on the published image of an earlier
  release.** The 51 graded sessions of 16 September ran against
  `ghcr.io/bobrovsky420/swiss-tip:mvp-zurich-2026-09-16-v2` (record
  `.local/experiments/2026-09-16-opencode-image-acceptance.md`; the results
  are summarised under "Gaps in the extension"). Call and byte counts vary
  from run to run with the caller: the same case stays within budget in
  one session and not in the next (UAT-3 and UAT-14, 2 of 3 each). The
  earlier runs, on the releases of 14 and 15 September, are in their
  records (`.local/experiments/2026-09-15-opencode-kb1-extension-acceptance.md`,
  `.local/experiments/2026-09-14-container-http-acceptance.md`).
- **No case meets every criterion in all of its sessions.** On
  16 September the best were UAT-10, UAT-12 and UAT-15 at 2 of 3 sessions
  and UAT-8, UAT-9, UAT-13 and UAT-14 at 1 of 3; 10 of 54 assessed turns
  met every criterion, 8 of 52 on 15 September, and every failure is an
  addition, a missing citation or the budget, not a wrong fact. The
  acceptance run history (`docs/history/user-acceptance-tests-history.md`
  of the original hackathon repository) records every run, passing or not.
- Several specified edge cases have no recorded live run and are exercised
  offline only.

## Not served at all

Questions outside the published topics are declined with a named gap,
including City of Zurich questions. The server does not refer the caller to
another service. A client can connect a companion server, such as
ZüriCityGPT's search over stadt-zuerich.ch, next to Swiss TIP; that pairing
is documented but not tested
([related work](docs/product/related-work.md#running-a-companion-server-next-to-swiss-tip)).
