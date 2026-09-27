# Polish civic participation acceptance tests

**Last update:** 27 September 2026

These questions test whether a calling assistant uses the planned
`mvp-poland` release as the source for how residents of Kraków, Warsaw and
Katowice take part in their city: the participatory budget, the local
initiative and grants for non-governmental organisations, and public
consultations, district councils, the citizens' resolution initiative and
the debate on the report on the state of the city. The useful comparison is
the same assistant answering once with Swiss TIP and once without it. A
fluent general answer is a failure when it carries one city's rule into
another, gives the law as it stood before a 2026 amendment, or treats a
consultation or a draft as binding.

The served places are the communes of Kraków (`PL-12-61-011`), Warsaw
(`PL-14-65-011`) and Katowice (`PL-24-69-011`), with the national acts that
apply to all three (`PL`). Each of the three cities is also a county; the
cases name the city, never the county.

## Status

Nothing of this is served yet. The server does not accept Polish places
until the country-neutral hierarchy, the TERYT place register and the Polish
text handling of the
[implementation plan](https://github.com/swisstip/swiss-tip/blob/main/docs/product/poland-implementation-plan.md)
are built, and the pack has no curation or release. What exists:

- the source catalogue `releases/mvp-poland/sources.json` and the page
  inventory `releases/mvp-poland/sources.md`, which list every page the
  expected answers below rest on;
- the expected answers, researched on 27 September 2026 from those official
  pages by one assistant per city and topic and checked by a second,
  independent assistant that reopened every page and every quote. Where the
  checker corrected an answer, the corrected answer is given. No person has
  reviewed them yet.

The expected answers become the claims of an `acceptance.yaml` only after
their facts are curated from the saved pages and reviewed; until then they
are the specification of what the pack must serve. Many of them depend on
the date: an edition's timetable, a call that is open, an amendment in force
since 1 September 2026. Each is written as of 27 September 2026, and a case
that is replayed later states that date in the request.

## How to run the questions

Once a release exists, as for the Swiss packs:

1. Start a fresh conversation and give the assistant access to Swiss TIP.
2. State the city the user lives in, unless the question names it or
   deliberately leaves it out, and today's date (27 September 2026 for the
   answers below).
3. Ask the question verbatim, in Polish, and save the final answer and all
   tool results.
4. Repeat it in a fresh conversation with Swiss TIP unavailable as the
   control.
5. Score the answer against the case, not against fluency, and ask each
   question several times.

## General acceptance criteria

Every Swiss TIP run must satisfy all of these criteria:

- It uses the facts returned for the resolved city and does not carry a
  rule, a threshold, an office or a date of another city into the answer.
- It keeps national law and the city's own resolution apart: the act sets
  the frame (for example the 300 signatures of art. 41a), the city sets the
  procedure (who may sign, how, where to file).
- It gives the law in force on the stated date, including the amendment of
  the public benefit act in force since 1 September 2026, and says when a
  city page still shows an older rule.
- It separates what is decided from what is proposed or pending: a draft
  programme, a resolution under consultation, an act waiting for the
  President's signature, an edition whose timetable is not published.
- It does not present a consultation, a draft or a council debate as
  binding, and it does not invent a turnout threshold, a fee or a deadline.
- It links the official citations returned by Swiss TIP and treats
  `STALE`, `OUT_OF_COVERAGE` and named gaps as real limits instead of
  answering around them from memory.
- It answers in the user's language; the release's statements are
  editorial summaries of Polish pages, and the excerpt is the authoritative
  text.

Efficiency is recorded, not a pass condition: a question should need at
most four tool calls. Most need one `search` and one `resolve`.

## Open points before curation

The research left these open; they limit the cases above rather than add
new ones:

- **Warsaw.** The city portal `um.warszawa.pl`, its district servers and
  the record pages of its Public Information Bulletin are saved through the
  downloader's browser session. Warsaw's document server is not: it
  publishes no robots.txt of its own, so the report on the 13th edition of
  the participatory budget and the mayor's consolidated order 825/2019 are
  missing, and the cases that cite them (PL-CIV-6, PL-CIV-8 and PL-CIV-9)
  must be curated from the resolutions and the portal pages. The
  consolidated local-initiative resolution, cited by PL-CIV-19 and
  PL-CIV-21, is a scan without a text layer; its original and amendment
  must be found in the voivodeship's journal.
- **Katowice.** The participatory-budget portal `bo.katowice.eu` mostly did
  not accept connections on 27 September 2026: 12 of its 28 pages are
  saved. PL-CIV-10 to PL-CIV-13 cite it, so they need a retry of the
  download before their facts can be curated; the council's budget
  resolutions are saved from the Public Information Bulletin, which
  answered every request.
- **National guidance.** The two gov.pl pages on the 2026 amendment are not
  saved, because the site's robots.txt redirects outside the entry's
  allowlist; PL-CIV-14 rests on the act itself, which is saved.
- **Date-bound answers.** The pack is first shown at HackYeah on 3-4
  October 2026, and several answers written on 27 September are out of
  date by then: Kraków's voting closed on 28 September (PL-CIV-2 and
  PL-CIV-4; the list of projects to be carried out is due by 13 November),
  Katowice's consultation on the 2027 cooperation programme closed on 29
  September (PL-CIV-26), and Katowice's 2027 local-initiative call opens
  on 1 October (PL-CIV-23 and PL-CIV-25). These cases are restated as of
  3 October before they become claims, and every replay states its date in
  the request.
- **Not yet published** (recheck on these dates): Kraków's 14th edition of
  the participatory budget; Warsaw's announcement for the 2028 budget (late
  October 2026); Katowice's 2027 local-initiative call (from 1 October
  2026); the 2027 cooperation programmes of all three cities (October to
  November 2026).
- **Pending law.** The amendment of the gmina act on district and estate
  councils (Sejm process 2649) was sent to the President on 4 September 2026
  and is not published; the district-council cases must be rechecked when
  it is.
- **Stale city pages.** All three cities still show the small-grant limits
  that applied before 1 September 2026 on some official pages or in a
  current order; the pack must serve the Act and say which city page is
  out of date.
- **Not researched.** Local referendums, petitions to the council, youth
  and senior councils.

## Case index

| ID | Where | Copy-paste question | Main trap |
| --- | --- | --- | --- |
| PL-CIV-1 | National law | Ile co najmniej musi wynosić budżet obywatelski w Krakowie - 0,5% tegorocznego budżetu miasta? | Assistants usually say '0.5% of the budget' or '0.5% of the current/next year's budget'. They miss that the base is expenditure in the last submitted budget execution report, and that the council cannot drop selected projects. |
| PL-CIV-2 | Kraków | Moja córka ma 13 lat i mieszka z nami w Krakowie. Czy może sama zagłosować w budżecie obywatelskim? | Generic assistants often assume an age threshold (16, or 18, or parental consent) because many Polish cities set one, or they tie eligibility to zameldowanie. Kraków's rules say 'bez względu na wiek' and count actual residence. |
| PL-CIV-3 | Kraków | Czy w tegorocznym budżecie obywatelskim Krakowa muszę wybrać po trzy projekty dzielnicowe i trzy ogólnomiejskie, żeby mój głos był ważny? | The repealed 2021 rules had every voter vote for three city-wide and three district projects, and old guides repeat that. Other assistants give the generic 'one vote for one project' model used in some cities. |
| PL-CIV-4 | Kraków | Do kiedy mogę zagłosować w budżecie obywatelskim w Krakowie i ile pieniędzy jest do podziału? | A model trained on 2025 data gives the 12th-edition answer: 51 million zł, voting until 3 October. Others assume voting in June, as in some other cities, or mix up the edition's year label (BO 2026) with the year the projects are carried out (2027). |
| PL-CIV-5 | Kraków | Mieszkam na Podgórzu, ale zameldowana jestem w Nowej Hucie. Na projekty której dzielnicy mogę głosować? | Generic answers tie eligibility to the meldunek address, or say any district can be chosen. Kraków's rules make actual residence decisive and limit district votes to the district of residence. |
| PL-CIV-6 | Warsaw | Jestem obcokrajowcem, mieszkam na stałe w Warszawie, ale nie mam numeru PESEL. Czy mogę zagłosować w budżecie obywatelskim? | Generic assistants say 'every resident can vote regardless of citizenship or registration' and stop there. In Warsaw, the PESEL field on the ballot excludes residents who have no PESEL, even though meldunek is not needed. |
| PL-CIV-7 | Warsaw | Moja córka ma 11 lat. Czy może sama zagłosować w warszawskim budżecie obywatelskim albo zgłosić projekt? | Generic assistants often state a national or typical age limit (16, or 18 'as in elections'), or confuse Warsaw with cities that set an age threshold. In Warsaw, voting is open at any age and 13 is only the threshold for taking part without consent. |
| PL-CIV-8 | Warsaw | Mieszkam na Woli, ale pracuję na Mokotowie. Czy mogę głosować na projekty z Mokotowa i na ile projektów mogę oddać głos? | Generic assistants assume you may vote only in your district of residence, or give a points-based or single-choice scheme borrowed from other cities. They also miss that voting twice voids all of your votes. |
| PL-CIV-9 | Warsaw | Chcę zgłosić projekt do kolejnej edycji warszawskiego budżetu obywatelskiego. Od kiedy do kiedy mogę to zrobić i ile podpisów poparcia potrzebuję do projektu lokalnego? | Generic assistants tend to give an older window (7-21 January in the 12th edition, or May-June in 2019) or guess 'spring'. They also give a generic or higher signature count, and do not know that authors are excluded or that the next edition's details are not yet published. |
| PL-CIV-10 | Katowice | Mieszkam na Osiedlu Tysiąclecia w Katowicach. Czy w budżecie obywatelskim mogę oddać głosy lokalne jednocześnie na projekt z Ligoty i na projekt z Brynowa? | A generic assistant usually says either that you can vote only for your own district's projects, or that you can spread votes across any districts. Katowice allows any district, but only one. |
| PL-CIV-11 | Katowice | Moja córka ma 12 lat. Czy może głosować w katowickim budżecie obywatelskim albo zgłosić własny projekt? | Generic assistants often assume a minimum age of 16 or 18, or that children cannot submit projects. |
| PL-CIV-12 | Katowice | Mieszkam w Katowicach, ale nie jestem tu zameldowany. Czy mogłem zagłosować w XIII edycji budżetu obywatelskiego i do kiedy trzeba było się dopisać? | A generic assistant tends to say only registered residents can vote, that you must register in advance, or it misses the edition-specific cut-off dates and the PESEL requirement. |
| PL-CIV-13 | Katowice | Ile podpisów poparcia potrzebuję w Katowicach, żeby zgłosić projekt lokalny w Zarzeczu, a ile dla projektu ogólnomiejskiego? | A generic assistant gives one fixed number for every district (like other cities' rules) or confuses local and city-wide requirements. |
| PL-CIV-14 | National law | Nasze stowarzyszenie z Katowic chce w październiku 2026 r. dostać mały grant z pominięciem konkursu (art. 19a). Jaka jest maksymalna kwota i czy projekt musi się zmieścić w 90 dniach? | Generic assistants rely on pre-2026 law and answer 10 000 zł, a maximum of 90 days, 20 000 zł per year and 20 %. They also miss the transitional rule for offers filed before 1 September 2026. |
| PL-CIV-15 | Kraków | Nasze stowarzyszenie z Krakowa chce dostać mały grant (art. 19a) od miasta na projekt za 18 000 zł, który potrwa pięć miesięcy. Czy to możliwe? | A generic assistant, or one reading older Kraków pages (the ngo.krakow.pl instruction of 2025-02-26, the RPW 2026 text, the county's 'Małe granty na 2026 r.' item), will answer 10 000 zł and 90 days, which is the pre-September-2026 law. It may also apply the county's (Powiat krakowski) rules to the city. |
| PL-CIV-16 | Kraków | Chcę złożyć wniosek o inicjatywę lokalną w Krakowie przez ePUAP - czy tak można i do kiedy muszę go złożyć, jeśli nasz piknik sąsiedzki ma być za miesiąc? | A generic assistant says 'any time through ePUAP' or gives a fixed call date. City pages (BIP ?dok_id=68716, the obywatelski.krakow.pl call of January 2026) still cite the repealed order 985/2020 and ePUAP, and none of them mentions the 8-week rule. |
| PL-CIV-17 | Kraków | Czy fundacja może sama złożyć w Krakowie wniosek o inicjatywę lokalną i ile podpisów mieszkańców trzeba zebrać? | A generic assistant treats the local initiative like an NGO grant: it says an NGO can apply on its own, and it knows neither the Kraków minimum of 2 applicants and 15 supporters nor the 60-point threshold. |
| PL-CIV-18 | Kraków | Czy w ramach inicjatywy lokalnej w Krakowie możemy wybudować odcinek kanalizacji i zapłacić sobie za pracę przy projekcie? | A generic assistant reads national art. 19b(1)(1), which mentions sewers and water mains, and answers yes. It does not know Kraków's exclusion or the ban on paying the initiators. |
| PL-CIV-19 | Warsaw | Do kiedy trwa w Warszawie nabór wniosków o inicjatywę lokalną w 2026 r. i ile pieniędzy maksymalnie może dostać nasza grupa sąsiedzka? | A generic assistant treats local initiative like the participatory budget or a grant call. It invents a call deadline and a per-project amount, or says the city pays a grant to the group, which Warsaw explicitly rules out. It may also mix it up with the 2000 zł Inicjatywy Sąsiedzkie. |
| PL-CIV-20 | Warsaw | Nasza fundacja chce w Warszawie mały grant (art. 19a) na projekt trwający 4 miesiące za 18 000 zł. Czy to możliwe i jaki jest roczny limit? | Most online sources, generic LLM knowledge and even a 2016 page on Warsaw's own NGO portal still say a maximum of 10 000 zł, a maximum of 90 days and 20 000 zł a year. The assistant would wrongly say the project is impossible. It may also miss that Warsaw only accepts offers through witkac.pl calls. |
| PL-CIV-21 | Warsaw | Mój 16-letni syn i jego kolega, niezameldowani w Warszawie, chcą złożyć wniosek o inicjatywę lokalną (np. odnowienie boiska). Czy mogą i czy potrzebują listy podpisów? | A generic assistant assumes applicants must be adult, registered residents, or copies the participatory budget's mandatory signature thresholds. In Warsaw's local initiative, age and registration do not matter and signatures are optional scoring points. |
| PL-CIV-22 | Warsaw | Czy Warszawa ma już uchwalony program współpracy z NGO na 2027 rok i do kiedy ogłosi konkursy ofert na cały 2027 rok? | An assistant either cites the 2026 dates (28 Nov 2025) as if they were current, presents the 2027 draft as adopted, or relies on the stale BIP overview that still describes the 2025 programme. |
| PL-CIV-23 | Katowice | Prowadzę stowarzyszenie w Katowicach. Czy możemy złożyć wniosek o inicjatywę lokalną i dostać dotację na nasz projekt sąsiedzki? | Generic assistants describe the local initiative as a grant programme that NGOs apply to. Katowice's rules (Zarządzenie 1182/2020, 2026 brochure) forbid NGO applications in the organisation's own name and pay no grant at all. |
| PL-CIV-24 | Katowice | Ile maksymalnie można dostać w Katowicach w trybie małego grantu (art. 19a) i jak długo może trwać takie zadanie? | Generic assistants answer '10 000 zł and 90 days', which was true only before 1 September 2026. The city's own older 'Pozyskaj grant' page and Zarządzenie 1317/2026 still show the old limits, and the city page ties the transition to the contract date where the Act uses the offer submission date. |
| PL-CIV-25 | Katowice | Chcę zgłosić inicjatywę lokalną w Katowicach na 2027 rok. Do kiedy mogę złożyć wniosek, ile podpisów muszę zebrać i czy mogę go wysłać przez ePUAP? | Assistants tend to invent a fixed signature threshold (confusing this with the participatory budget), suggest rolling year-round applications, or point to ePUAP or SEKAP. The KATOobywatel page on a city domain still lists SEKAP. |
| PL-CIV-26 | Katowice | Czy nasza organizacja może jeszcze zgłosić uwagi do programu współpracy Katowic z organizacjami pozarządowymi na 2027 rok i jaka kwota jest w nim przewidziana? | A generic answer gives no concrete dates, assumes the consultation is already over or not yet started, and confuses the annual programme (at least 60 million zł) with the new multi-year programme (at least 18 million zł a year). |
| PL-CIV-27 | National law | Mieszkam na stałe w Warszawie, jestem obywatelką Ukrainy. Czy mój podpis liczy się pod obywatelską inicjatywą uchwałodawczą do Rady m.st. Warszawy i ile podpisów trzeba zebrać? | Assistants often say any resident may sign, or they give wrong thresholds (1 000 signatures, 5 % or 15 %). They may also treat the rules for the participatory budget and the resolution initiative as the same. |
| PL-CIV-28 | National law | Czy wybory do rad dzielnic w Krakowie odbywają się razem z wyborami samorządowymi, tak jak w Warszawie? | Assistants apply Warsaw's model (18 statutory districts elected with the city council) to every Polish city. They also do not know the statutory ban on holding auxiliary-unit elections on general election days. |
| PL-CIV-29 | Kraków | Chcę zabrać głos w debacie nad raportem o stanie Krakowa. Czy wystarczy zapisać się na sesji i ile podpisów potrzebuję? | A generic assistant tends to give the 20-signature threshold, which applies only to municipalities up to 20,000 inhabitants. It may also suggest signing up on the spot or online, or not mention the 15-speaker cap and the day-before deadline. |
| PL-CIV-30 | Kraków | Czy mogę poprzeć obywatelską inicjatywę uchwałodawczą w Krakowie przez internet, podpisując e-dowodem albo podpisem kwalifikowanym? | A generic assistant usually says any electronic signature works, including e-dowód and qualified signatures, or that municipal initiatives need handwritten paper lists. It will not know the OBIU module or that a signature cannot be withdrawn. |
| PL-CIV-31 | Kraków | Kiedy są następne wybory do rady dzielnicy w Krakowie i czy jako obywatelka Niemiec mieszkająca na stałe w Podgórzu mogę w nich głosować? | A generic assistant assumes district councils were elected with the April 2024 municipal elections and gives 2029, or says only Polish citizens may vote. It may also not know that Kraków's district councils have their own 5-year cycle set in their statutes. |
| PL-CIV-32 | Kraków | Ilu mieszkańców musi podpisać wniosek o konsultacje społeczne w Krakowie i czy ich wynik jest dla miasta wiążący? | A generic assistant often confuses consultations with a local referendum, with a turnout threshold and binding result. It may give another city's or a made-up signature threshold (e.g. 1,000), or point to dialogspoleczny.krakow.pl, which now hosts an unrelated lifestyle blog. |
| PL-CIV-33 | Warsaw | Chcę złożyć w Warszawie obywatelski projekt uchwały w sprawie należącej do zadań powiatu. Ile podpisów mieszkańców muszę zebrać i komu złożyć projekt? | A generic answer quotes only art. 41a u.s.g. and says '300 signatures'. It misses that Warsaw is also a powiat and that its resolution routes county tasks to the 500-signature threshold. It may also invent a committee size or claim the President receives the draft. |
| PL-CIV-34 | Warsaw | Ile podpisów trzeba zebrać w Warszawie, żeby złożyć wniosek o konsultacje społeczne w sprawie mojej dzielnicy, do kogo go złożyć i czy na liście poparcia trzeba podać PESEL? | The original 2013 resolution, still widely quoted, required PESEL. A generic assistant may also give a single national threshold or say residents cannot start consultations at all. It is also likely to miss the separate 200 and 1,000 thresholds and the different recipients. |
| PL-CIV-35 | Warsaw | Do kiedy i z iloma podpisami muszę się zgłosić, żeby zabrać głos w debacie nad raportem o stanie Warszawy w 2027 roku, i jak długo mogę mówić? | A generic answer says 'by 31 May', which is actually the President's deadline for presenting the report. It may also say 20 signatures (the threshold for gminy under 20,000) or claim there is no time limit (only councillors are unlimited in this debate). It cannot know Warsaw's planned 2027 session date. |
| PL-CIV-36 | Warsaw | Czy rady osiedli w Warszawie wybiera się razem z wyborami samorządowymi, tak jak rady dzielnic? Kiedy będą następne wybory do mojej rady dzielnicy? | Generic assistants tend to merge Warsaw's districts with neighbourhood councils. They may assume rady osiedli are elected in the April local elections, or that Warsaw's district councils are appointed rather than directly elected. |
| PL-CIV-37 | Katowice | Mieszkam na Nikiszowcu (Dzielnica nr 16 Janów-Nikiszowiec). Czy 8 listopada 2026 r. mogę głosować w wyborach do mojej rady dzielnicy? | A generic assistant will say that district council elections take place on 8 November 2026 across Katowice, or that district councils work normally. It will not know that seven districts lost their elections for lack of candidates, or about the 10% re-run rule. |
| PL-CIV-38 | Katowice | Chcę zabrać głos w debacie nad raportem o stanie miasta Katowice. Ilu podpisów potrzebuję i do kiedy muszę się zgłosić? | Assistants often give 20 signatures (the threshold for small municipalities), say no signatures are needed, or assume registration is on the day of the session. |
| PL-CIV-39 | Katowice | Ile podpisów trzeba zebrać w Katowicach pod obywatelskim projektem uchwały i czy na liście poparcia trzeba podać PESEL? | Assistants may give 500, 1,000 or a percentage threshold, or say PESEL is required. PESEL was in the earlier Katowice resolution IV/65/19 and is common in other cities, but the rules the city cites (VII/128/19) ask for date of birth instead. |
| PL-CIV-40 | Katowice | Ilu mieszkańców musi poprzeć wniosek o przeprowadzenie konsultacji społecznych w Katowicach, czy osoba spoza Katowic może w nich uczestniczyć i czy potrzebna jest minimalna frekwencja? | A generic assistant may cite a percentage threshold, say anyone including non-residents may join (the unannulled-looking text of the resolution suggests this), or invent a turnout threshold that makes consultations binding. |

## Participatory budget

### PL-CIV-1 - National law

**Question:** Ile co najmniej musi wynosić budżet obywatelski w Krakowie - 0,5% tegorocznego budżetu miasta?

*(What is the minimum size of Kraków's participatory budget - 0.5% of the city's budget for the current year?)*

**Expected answer:** The participatory budget is mandatory in Kraków because it is a city with county rights. The minimum is at least 0.5 % of the city's expenditures shown in the last submitted budget execution report, not of the current year's planned budget (art. 5a ust. 5). The city council may not remove or substantially change winning projects when adopting the budget (art. 5a ust. 4). Kraków's resolution may not require more signatures than 0.1 % of the residents of the pool area (art. 5a ust. 7 pkt 2).

**Why the control may fail:** Assistants usually say '0.5% of the budget' or '0.5% of the current/next year's budget'. They miss that the base is expenditure in the last submitted budget execution report, and that the council cannot drop selected projects.

**Sources:**

- <https://api.sejm.gov.pl/eli/acts/DU/2026/662/text.pdf>

### PL-CIV-2 - Kraków

**Question:** Moja córka ma 13 lat i mieszka z nami w Krakowie. Czy może sama zagłosować w budżecie obywatelskim?

*(My daughter is 13 and lives with us in Kraków. Can she vote in the participatory budget herself?)*

**Expected answer:** Yes. Kraków sets no minimum age: every person living in Kraków may vote regardless of age or nationality. With a PESEL she gives her PESEL; people without one give a City Office (UMK) identification code on paper, or date of birth and sex online. Registration (zameldowanie) is not required; actual residence counts. She may vote once, for up to 3 district projects in her own district and up to 3 city-wide projects; one of each is enough for a valid vote. In the 13th edition voting runs until 23:59 on 28 September 2026. At a voting point any photo document with her name, such as a school ID, is accepted.

**Why the control may fail:** Generic assistants often assume an age threshold (16, or 18, or parental consent) because many Polish cities set one, or they tie eligibility to zameldowanie. Kraków's rules say 'bez względu na wiek' and count actual residence.

The verifier corrected the researcher's expected answer; the corrected answer is the one above.

**Sources:**

- <https://budzet.krakow.pl/aktualnosci/337439,1909,komunikat,glosowanie_w_13__edycji_budzetu_obywatelskiego_miasta_krakowa_rozpoczete.html>
- <https://budzet.krakow.pl/o-budzecie-obywatelskim/307506,artykul,kto-i-jak-moze-wziac-udzial.html>
- <https://budzet.krakow.pl/jak-zaglosowac/322395,artykul,punkty-glosowania.html>
- <https://www.bip.krakow.pl/zarzadzenia/2026/1115/X19UUF9fOTIyNjI=/1.pdf>

### PL-CIV-3 - Kraków

**Question:** Czy w tegorocznym budżecie obywatelskim Krakowa muszę wybrać po trzy projekty dzielnicowe i trzy ogólnomiejskie, żeby mój głos był ważny?

*(In this year's Kraków participatory budget, do I have to pick three district and three city-wide projects for my vote to count?)*

**Expected answer:** No. Since the 2026 rules (resolution XLV/926/26 and the President's voting rules in order 1115/2026), a voter may pick at most 3 district projects (in their own district) and at most 3 city-wide projects, ranked 3 to 1 points. The vote is valid as long as it includes at least one district and one city-wide project.

**Why the control may fail:** The repealed 2021 rules had every voter vote for three city-wide and three district projects, and old guides repeat that. Other assistants give the generic 'one vote for one project' model used in some cities.

**Sources:**

- <https://www.bip.krakow.pl/zarzadzenia/2026/1115/X19UUF9fOTIyNjI=/1.pdf>
- <https://www.bip.krakow.pl/_inc/rada/uchwaly/show_pdf.php?id=116917>
- <https://www.bip.krakow.pl/?dok_id=167&sub_dok_id=167&sub=uchwala&query=id%3D28840%26typ%3Du>

### PL-CIV-4 - Kraków

**Question:** Do kiedy mogę zagłosować w budżecie obywatelskim w Krakowie i ile pieniędzy jest do podziału?

*(Until when can I vote in Kraków's participatory budget, and how much money is being allocated?)*

**Expected answer:** 13th edition: voting runs 11-28 September 2026 and closes at 23:59 on 28 September (online; paper points close at their posted hours). The pool is 54 million zł: 10.8 million for city-wide projects (50,000-2,160,000 zł each) and 43.2 million for district projects, split among the 18 districts (e.g. Nowa Huta 3,345,161.23 zł). The list of projects to be carried out is due by 13 November 2026, and chosen projects start in 2027.

**Why the control may fail:** A model trained on 2025 data gives the 12th-edition answer: 51 million zł, voting until 3 October. Others assume voting in June, as in some other cities, or mix up the edition's year label (BO 2026) with the year the projects are carried out (2027).

The verifier corrected the researcher's expected answer; the corrected answer is the one above.

**Sources:**

- <https://budzet.krakow.pl/aktualnosci/310128,1909,komunikat,harmonogram_13__edycji_budzetu_obywatelskiego_miasta_krakowa.html>
- <https://www.bip.krakow.pl/zarzadzenia/2026/1115/X19UUF9fOTIyNjI=/1.pdf>
- <https://budzet.krakow.pl/aktualnosci/337439,1909,komunikat,glosowanie_w_13__edycji_budzetu_obywatelskiego_miasta_krakowa_rozpoczete.html>
- <https://budzet.krakow.pl/aktualnosci/307995,1909,komunikat,srodki_na_projekty_w_13__edycji_budzetu_obywatelskiego.html>
- <https://plikimpi.krakow.pl/zalacznik/546699>
- <https://budzet.krakow.pl/307557,artykul,dla-autorow-projektow.html>
- <https://www.krakow.pl/aktualnosci/290981,26,komunikat,budzet_obywatelski___oto_tegoroczny_harmonogram.html>

### PL-CIV-5 - Kraków

**Question:** Mieszkam na Podgórzu, ale zameldowana jestem w Nowej Hucie. Na projekty której dzielnicy mogę głosować?

*(I live in Podgórze but my registered address (meldunek) is in Nowa Huta. Which district's projects can I vote for?)*

**Expected answer:** Only the district where you actually live, here Podgórze (District XIII; if you live in Podgórze Duchackie, District XI). District projects can be chosen only by residents of that district, and zameldowanie is not required: actual residence counts, so you give your real Kraków address when voting. You can also pick up to 3 city-wide projects.

**Why the control may fail:** Generic answers tie eligibility to the meldunek address, or say any district can be chosen. Kraków's rules make actual residence decisive and limit district votes to the district of residence.

The verifier corrected the researcher's expected answer; the corrected answer is the one above.

**Sources:**

- <https://edziennik.malopolska.uw.gov.pl/WDU_K/2026/511/akt.pdf>
- <https://budzet.krakow.pl/aktualnosci/337439,1909,komunikat,glosowanie_w_13__edycji_budzetu_obywatelskiego_miasta_krakowa_rozpoczete.html>
- <https://www.bip.krakow.pl/zarzadzenia/2026/1115/X19UUF9fOTIyNjI=/1.pdf>

### PL-CIV-6 - Warsaw

**Question:** Jestem obcokrajowcem, mieszkam na stałe w Warszawie, ale nie mam numeru PESEL. Czy mogę zagłosować w budżecie obywatelskim?

*(I am a foreigner living permanently in Warsaw but I have no PESEL number. Can I vote in the participatory budget?)*

**Expected answer:** No, not without a PESEL. A valid vote requires a PESEL number: the ballot must contain it (§ 38 of the resolution) and the data are checked against the CRBDEL register (§ 39). In the 13th edition, foreigners without a PESEL could not vote. They can submit a project, because no PESEL is needed to submit. Registration (meldunek) is not required.

**Why the control may fail:** Generic assistants say 'every resident can vote regardless of citizenship or registration' and stop there. In Warsaw, the PESEL field on the ballot excludes residents who have no PESEL, even though meldunek is not needed.

The verifier corrected the researcher's expected answer; the corrected answer is the one above.

**Sources:**

- <https://cdn.um.warszawa.pl/documents/57254/151437340/Raport+z+przeprowadzenia+13.+edycji+bud%C5%BCetu+obywatelskiego.pdf/868165f4-4859-c0e5-0aa0-e47a726a75ef?t=1788178439102>
- <https://cdn.um.warszawa.pl/documents/57254/125266192/Uchwa%C5%82a+Rady+m.st.+Warszawy+z+dnia+11+kwietnia+2019+r.+w+sprawie+konsultacji+spo%C5%82ecznych+z+mieszka%C5%84cami+m.st.+Warszawy+w+formie+bud%C5%BCetu+obywatelskiego+%28uwzgl%C4%99dnia+zmiany+z+2024+roku%29.doc/4bca3581-017e-5b92-728b-d4870cc828d9?t=1734701114722>
- <https://um.warszawa.pl/waw/bo/glosowanie-na-projekty-13-edycja->

### PL-CIV-7 - Warsaw

**Question:** Moja córka ma 11 lat. Czy może sama zagłosować w warszawskim budżecie obywatelskim albo zgłosić projekt?

*(My daughter is 11. Can she vote in Warsaw's participatory budget or submit a project?)*

**Expected answer:** She can take part, since Warsaw sets no minimum age for voting or submitting, but not entirely on her own. Because she is under 13, she needs a parent's or guardian's consent. From 13 a person may take part alone.

**Why the control may fail:** Generic assistants often state a national or typical age limit (16, or 18 'as in elections'), or confuse Warsaw with cities that set an age threshold. In Warsaw, voting is open at any age and 13 is only the threshold for taking part without consent.

The verifier corrected the researcher's expected answer; the corrected answer is the one above.

**Sources:**

- <https://um.warszawa.pl/waw/bo/zglaszanie-projektow-13-edycja->
- <https://um.warszawa.pl/waw/bo/glosowanie-na-projekty-13-edycja->

### PL-CIV-8 - Warsaw

**Question:** Mieszkam na Woli, ale pracuję na Mokotowie. Czy mogę głosować na projekty z Mokotowa i na ile projektów mogę oddać głos?

*(I live in Wola but work in Mokotów. Can I vote for Mokotów projects, and how many projects can I pick?)*

**Expected answer:** Yes. The district and local area you vote in do not have to match where you live or are registered. You choose one district (for example Mokotów) and one local area within it. You may pick up to 5 district projects there, up to 5 local projects in that area, and up to 5 city-wide projects, for at most 15 votes. You may vote only once: if you vote twice, all your votes are invalid.

**Why the control may fail:** Generic assistants assume you may vote only in your district of residence, or give a points-based or single-choice scheme borrowed from other cities. They also miss that voting twice voids all of your votes.

**Sources:**

- <https://um.warszawa.pl/waw/bo/glosowanie-na-projekty-13-edycja->
- <https://cdn.um.warszawa.pl/documents/57254/125266192/Uchwa%C5%82a+Rady+m.st.+Warszawy+z+dnia+11+kwietnia+2019+r.+w+sprawie+konsultacji+spo%C5%82ecznych+z+mieszka%C5%84cami+m.st.+Warszawy+w+formie+bud%C5%BCetu+obywatelskiego+%28uwzgl%C4%99dnia+zmiany+z+2024+roku%29.doc/4bca3581-017e-5b92-728b-d4870cc828d9?t=1734701114722>
- <https://cdn.um.warszawa.pl/documents/57254/151437340/Raport+z+przeprowadzenia+13.+edycji+bud%C5%BCetu+obywatelskiego.pdf/868165f4-4859-c0e5-0aa0-e47a726a75ef?t=1788178439102>

### PL-CIV-9 - Warsaw

**Question:** Chcę zgłosić projekt do kolejnej edycji warszawskiego budżetu obywatelskiego. Od kiedy do kiedy mogę to zrobić i ile podpisów poparcia potrzebuję do projektu lokalnego?

*(I want to submit a project to the next edition of Warsaw's participatory budget. When can I do it, and how many support signatures do I need for a local project?)*

**Expected answer:** Under the current resolution (Table 5, 'od 2027'), projects are submitted from 1 December to 13 January, starting in the year two years before the budget year. For the next, 14th edition (budget for 2028) that means 1 December 2026 to 13 January 2027. This is inferred from the standing rule: no 14th-edition timetable was found on the city's pages as of 27 September 2026, and rule changes were put to consultation in June 2026, so confirm it with the city. A local project needs a list with at least 5 signatures of people living in that local area, not counting the project's authors. District projects need 10 and city projects 15.

**Why the control may fail:** Generic assistants tend to give an older window (7-21 January in the 12th edition, or May-June in 2019) or guess 'spring'. They also give a generic or higher signature count, and do not know that authors are excluded or that the next edition's details are not yet published.

The verifier corrected the researcher's expected answer; the corrected answer is the one above.

**Sources:**

- <https://edziennik.mazowieckie.pl/WDU_W/2024/10017/oryginal/akt.pdf>
- <https://cdn.um.warszawa.pl/documents/57254/125266192/Uchwa%C5%82a+Rady+m.st.+Warszawy+z+dnia+11+kwietnia+2019+r.+w+sprawie+konsultacji+spo%C5%82ecznych+z+mieszka%C5%84cami+m.st.+Warszawy+w+formie+bud%C5%BCetu+obywatelskiego+%28uwzgl%C4%99dnia+zmiany+z+2024+roku%29.doc/4bca3581-017e-5b92-728b-d4870cc828d9?t=1734701114722>
- <https://um.warszawa.pl/waw/bo/zglaszanie-projektow-13-edycja->
- <https://um.warszawa.pl/waw/bo/-/jakie-zmiany-w-bo-2026>
- <https://um.warszawa.pl/waw/bo/harmonogram-14-edycja>

### PL-CIV-10 - Katowice

**Question:** Mieszkam na Osiedlu Tysiąclecia w Katowicach. Czy w budżecie obywatelskim mogę oddać głosy lokalne jednocześnie na projekt z Ligoty i na projekt z Brynowa?

*(I live in Osiedle Tysiąclecia in Katowice. In the participatory budget, can I give my local votes to one project in Ligota and another in Brynów?)*

**Expected answer:** No. All 3 local votes must go to projects in ONE district of your choice, which need not be your own. You may use them in Ligota-Panewniki or in one Brynów district (Brynów is split between two districts), but not in both. You also have 3 votes for city-wide projects. In each category you can give 3 points to one project, 1 and 2 to two projects, or 1 each to three; votes you leave unused are lost once you confirm. For 2026 this is moot: XIII voting closed on 23.09.2026, and the XIV edition timetable has not been published.

**Why the control may fail:** A generic assistant usually says either that you can vote only for your own district's projects, or that you can spread votes across any districts. Katowice allows any district, but only one.

The verifier corrected the researcher's expected answer; the corrected answer is the one above.

**Sources:**

- <https://bo.katowice.eu/add/file/1400396404-cacb130edfbd3c1f0946a973a7a73b461c1ca0cd3d0085b2637a8787a957f942.pdf?v=0>
- <https://bo.katowice.eu/aktualnosci-szczegoly-1400011925-1400440187-ae4cf6512123566ec9509c952f497dc8>
- <https://bo.katowice.eu/budzet-obywatelski-strefa-wnioskodawcy-2026-e194d11e4b050409d10d5f0c4a4bdc4f>
- <https://bo.katowice.eu/budzet-obywatelski-harmonogram-2026-4d92e16b9138332a4a9832eff7f14ec5>

### PL-CIV-11 - Katowice

**Question:** Moja córka ma 12 lat. Czy może głosować w katowickim budżecie obywatelskim albo zgłosić własny projekt?

*(My daughter is 12. Can she vote in the Katowice participatory budget or submit her own project?)*

**Expected answer:** Yes to both in principle. Katowice sets no minimum age, and a resident under 16 takes part with the support of a parent or legal guardian. To submit a project, the guardian gives written support with a legible signature. To vote, she enters her PESEL and mother's maiden name, the guardian gives consent in the voting app, and the vote is confirmed with an SMS code. She can use this in the next (XIV) edition: XIII submissions closed on 9.04.2026 and voting closed on 23.09.2026, and no XIV dates have been published yet.

**Why the control may fail:** Generic assistants often assume a minimum age of 16 or 18, or that children cannot submit projects.

The verifier corrected the researcher's expected answer; the corrected answer is the one above.

**Sources:**

- <https://bo.katowice.eu/aktualnosci-szczegoly-1400011925-1400440187-ae4cf6512123566ec9509c952f497dc8>
- <https://bo.katowice.eu/add/file/1400396404-cacb130edfbd3c1f0946a973a7a73b461c1ca0cd3d0085b2637a8787a957f942.pdf?v=0>
- <https://bo.katowice.eu/glosowanie/instrukcja.php>

### PL-CIV-12 - Katowice

**Question:** Mieszkam w Katowicach, ale nie jestem tu zameldowany. Czy mogłem zagłosować w XIII edycji budżetu obywatelskiego i do kiedy trzeba było się dopisać?

*(I live in Katowice but am not registered (zameldowany) here. Could I vote in the XIII edition of the participatory budget, and by when did I have to add myself?)*

**Expected answer:** Yes, as a Katowice resident. The voting register automatically included people registered for permanent or temporary stay on 24.08.2026. Anyone else could add themselves only while voting ran (10-23.09.2026), with a written declaration giving name, mother's maiden name, PESEL and Katowice address. It could be filed in person with an ID document at the Punkt Konsultacyjny (Rynek 13, room 205) or a stationary voting point, by ePUAP or e-Doręczenia by 22.09, or by e-mail as a file signed with a profil zaufany or qualified signature by 23.09 at 14:00. Mayor's order 1402/2026 § 10 ust. 4 names only in-person filing at the Punkt Konsultacyjny; the website also allowed the other channels. Voting is now closed.

**Why the control may fail:** A generic assistant tends to say only registered residents can vote, that you must register in advance, or it misses the edition-specific cut-off dates and the PESEL requirement.

The verifier corrected the researcher's expected answer; the corrected answer is the one above.

**Sources:**

- <https://bo.katowice.eu/c75553c5bcdfe462bdc21523778e1c3a>
- <https://bo.katowice.eu/add/file/1400396411-4ab15b6f5401db2cbd53b970073dc9811c2704eba26159f372e1420a09082dac.pdf?v=0>
- <https://bo.katowice.eu/budzet-obywatelski-harmonogram-2026-4d92e16b9138332a4a9832eff7f14ec5>

### PL-CIV-13 - Katowice

**Question:** Ile podpisów poparcia potrzebuję w Katowicach, żeby zgłosić projekt lokalny w Zarzeczu, a ile dla projektu ogólnomiejskiego?

*(How many supporting signatures do I need in Katowice to submit a local project in Zarzecze, and how many for a city-wide project?)*

**Expected answer:** Zarzecze needs just 1 supporting resident of Zarzecze. A city-wide project needs at least 50 other Katowice residents. The local number varies by district, from 1 to 24 (e.g. Ligota-Panewniki 24, Śródmieście 22), under annex 2 of the Regulamin as amended by resolution XI/195/25. Support can be given on paper using the official template or signed electronically with a profil zaufany or mObywatel. Paper originals of scanned lists must be delivered within 7 days when requested.

**Why the control may fail:** A generic assistant gives one fixed number for every district (like other cities' rules) or confuses local and city-wide requirements.

**Sources:**

- <https://bo.katowice.eu/add/file/1400396414-305e53ab504f979ee24dd8f62ea26b0126a5d08cd257474c8d8158c8ee32e00d.pdf?v=0>
- <https://dzienniki.slask.eu/WDU_S/2025/653/akt.pdf>
- <https://bo.katowice.eu/budzet-obywatelski>
- <https://bo.katowice.eu/budzet-obywatelski-strefa-wnioskodawcy-2026-e194d11e4b050409d10d5f0c4a4bdc4f>

## Local initiative and grants for NGOs

### PL-CIV-14 - National law

**Question:** Nasze stowarzyszenie z Katowic chce w październiku 2026 r. dostać mały grant z pominięciem konkursu (art. 19a). Jaka jest maksymalna kwota i czy projekt musi się zmieścić w 90 dniach?

*(Our Katowice association wants a small grant without a competition (art. 19a) in October 2026. What is the maximum amount, and must the project fit within 90 days?)*

**Expected answer:** For offers submitted on or after 1 September 2026 the cap is 20 000 zł per task. There is no longer any 90-day limit on duration. One organisation may receive at most 40 000 zł a year in this mode from the city. The mode may use at most 30 % of the grants the city plans for NGO tasks. Legal basis: art. 19a as amended by Dz.U. 2026 poz. 1040, in force 1 Sep 2026. The offer is published for 7 days in the BIP, on the notice board and on the website, and anyone may comment within 7 days. Only offers submitted before 1 September 2026 remain under the old 10 000 zł / 90-day rules.

**Why the control may fail:** Generic assistants rely on pre-2026 law and answer 10 000 zł, a maximum of 90 days, 20 000 zł per year and 20 %. They also miss the transitional rule for offers filed before 1 September 2026.

**Sources:**

- <https://api.sejm.gov.pl/eli/acts/DU/2026/1040/text.pdf>
- <https://api.sejm.gov.pl/eli/acts/DU/2025/1338/text.pdf>
- <https://www.gov.pl/web/pozytek/juz-od-wrzesnia-nowe-rozwiazania-dla-organizacji-pozarzadowych>

### PL-CIV-15 - Kraków

**Question:** Nasze stowarzyszenie z Krakowa chce dostać mały grant (art. 19a) od miasta na projekt za 18 000 zł, który potrwa pięć miesięcy. Czy to możliwe?

*(Our Kraków association wants a city small grant (art. 19a) of 18 000 zł for a five-month project. Is that possible?)*

**Expected answer:** Yes, in principle, if the offer is filed on or after 1 September 2026. Since Dz. U. 2026 poz. 1040, art. 19a allows up to 20 000 zł per task with no 90-day limit, and the yearly cap per organisation is 40 000 zł. Kraków's NGO portal (news of 1 September 2026) and its 19a guide apply 20 000 / 40 000 zł. The guide recommends filing at least 30 days before the start (on paper, through e-Doręczenia or through the NGO Generator). The offer is assessed within 7 working days, and offers are considered only until the relevant department's published pool is used up. Offers filed before 1 September 2026 stay under the old rules (10 000 zł, 90 days). Caveat: the text of RPW 2026 (§ 7 ust. 16) and the RPW 2027 draft still say 10 000 zł and 90 days, and BIP shows no amending resolution. The Mayor decides whether the task is purposeful, and there is no appeal.

**Why the control may fail:** A generic assistant, or one reading older Kraków pages (the ngo.krakow.pl instruction of 2025-02-26, the RPW 2026 text, the county's 'Małe granty na 2026 r.' item), will answer 10 000 zł and 90 days, which is the pre-September-2026 law. It may also apply the county's (Powiat krakowski) rules to the city.

The verifier corrected the researcher's expected answer; the corrected answer is the one above.

**Sources:**

- <https://api.sejm.gov.pl/eli/acts/DU/2026/1040/text.pdf>
- <https://ngo.krakow.pl/aktualnosci/335876,52,komunikat,male_granty___wieksze_mozliwosci__zmiany_w_art__19a_juz_obowiazuja.html>
- <https://plikimpi.krakow.pl/zalacznik/616490>
- <https://ngo.krakow.pl/start/239723,artykul,instrukcja_postepowania_przy_skladaniu_ofert_w_trybie_malych_zlecen_art__19a.html>
- <https://www.bip.krakow.pl/_inc/rada/uchwaly/show_pdf.php?id=142747>
- <https://www.bip.krakow.pl/plik.php?zid=703079&wer=0&new=t&mode=shw>
- <https://ngo.krakow.pl/granty/323706,1061,komunikat,male_granty_na_2026_r__.html>

### PL-CIV-16 - Kraków

**Question:** Chcę złożyć wniosek o inicjatywę lokalną w Krakowie przez ePUAP - czy tak można i do kiedy muszę go złożyć, jeśli nasz piknik sąsiedzki ma być za miesiąc?

*(I want to file a Kraków local initiative application through ePUAP. Can I, and what is the deadline if our neighbourhood picnic is in a month?)*

**Expected answer:** Under order 1575/2026 of 29 July 2026, which replaced order 985/2020, you can file in person at the UMK information and filing desk, by post, or by electronic delivery as an attachment to a general letter with a trusted, qualified or personal signature. e-PUAP is no longer listed, although the older call page still mentions it. The application must be filed at least 8 weeks before the planned start. A picnic one month away is too soon: the application would be rejected on formal grounds. There is no fixed call deadline: the 2026 call is open until the 275 000 zł pool runs out.

**Why the control may fail:** A generic assistant says 'any time through ePUAP' or gives a fixed call date. City pages (BIP ?dok_id=68716, the obywatelski.krakow.pl call of January 2026) still cite the repealed order 985/2020 and ePUAP, and none of them mentions the 8-week rule.

**Sources:**

- <https://obywatelski.krakow.pl/aktualnosci/305442,2144,komunikat,ogloszenie_o_naborze_wnioskow_w_trybie_inicjatywy_lokalnej_na_2026_r_.html>
- <https://www.bip.krakow.pl/?dok_id=68716>
- <https://www.bip.krakow.pl/zarzadzenia/2026/1575/X19BS19fOTY1NDA=/1575_2026.pdf>

### PL-CIV-17 - Kraków

**Question:** Czy fundacja może sama złożyć w Krakowie wniosek o inicjatywę lokalną i ile podpisów mieszkańców trzeba zebrać?

*(Can a foundation file a Kraków local initiative application on its own, and how many residents' signatures are needed?)*

**Expected answer:** No. Residents are the applicants: at least 2 residents acting directly, or residents acting through an NGO or an art. 3(3) entity with its seat in Kraków (not a social cooperative), and the organisation only represents them. An application from an NGO in its own name, from an NGO seated outside Kraków, through a social cooperative, or from a single resident is rejected on formal grounds. A named list of support signed by at least 15 Kraków residents with their addresses is required. A positive district council opinion attached when filing adds 10 points; at least 60 of 100 points are needed.

**Why the control may fail:** A generic assistant treats the local initiative like an NGO grant: it says an NGO can apply on its own, and it knows neither the Kraków minimum of 2 applicants and 15 supporters nor the 60-point threshold.

**Sources:**

- <https://www.bip.krakow.pl/zarzadzenia/2026/1575/X19BS19fOTY1NDA=/1575_2026.pdf>
- <https://www.bip.krakow.pl/_inc/rada/uchwaly/show_pdf.php?id=92871>

### PL-CIV-18 - Kraków

**Question:** Czy w ramach inicjatywy lokalnej w Krakowie możemy wybudować odcinek kanalizacji i zapłacić sobie za pracę przy projekcie?

*(Can we build a stretch of sewer under a Kraków local initiative and pay ourselves for the work?)*

**Expected answer:** Not through Kraków's general local initiative procedure. Resolution LXXXI/1969/17 excludes building or extending sewers and water mains from this procedure and says separate city council resolutions set the procedure and criteria for them. Those resolutions are not covered here, so check them before assuming it is impossible. Paying yourselves is ruled out: the city may buy items, carry out works or hire specialists, but the people carrying out the initiative may not be paid (application form, annex 1 to order 1575/2026). Also excluded are tasks that conflict with city plans, tasks whose yearly upkeep after the contract would exceed 30% of their value, and tasks on land the city does not hold unless the landholder consents.

**Why the control may fail:** A generic assistant reads national art. 19b(1)(1), which mentions sewers and water mains, and answers yes. It does not know Kraków's exclusion or the ban on paying the initiators.

The verifier corrected the researcher's expected answer; the corrected answer is the one above.

**Sources:**

- <https://www.bip.krakow.pl/_inc/rada/uchwaly/show_pdf.php?id=92871>
- <https://www.bip.krakow.pl/zarzadzenia/2026/1575/X19UUF9fOTMwMDY=/1._Zalacznik_nr_1_do_Zarzadzenia_-_formularz_wniosku.pdf>
- <https://api.sejm.gov.pl/eli/acts/DU/2025/1338/text.pdf>

### PL-CIV-19 - Warsaw

**Question:** Do kiedy trwa w Warszawie nabór wniosków o inicjatywę lokalną w 2026 r. i ile pieniędzy maksymalnie może dostać nasza grupa sąsiedzka?

*(Until when does Warsaw accept local-initiative applications in 2026, and what is the maximum amount of money our neighbours' group can get?)*

**Expected answer:** There is no call and no deadline: applications are accepted all year. There is no fixed funding limit; each request is checked against the budget funds that can be committed. The office does not give the group money or a grant. It can buy services or materials and lend space or equipment, the activities must be free for participants, and the group may not profit. At least two residents (or an NGO seated in Warsaw acting for them) apply, on paper, at any City Office intake point, e.g. the district WOM. The answer is due within 30 days (60 in complicated cases). An application scoring under 24 points under Resolution LXI/1692/2013 is not carried out. Apply about 3 months before the activity. Inicjatywy Sąsiedzkie is a different scheme: support of up to 2000 zł for neighbourhood activities, with calls once or twice a year, run by Fundacja Stocznia with city funds.

**Why the control may fail:** A generic assistant treats local initiative like the participatory budget or a grant call. It invents a call deadline and a per-project amount, or says the city pays a grant to the group, which Warsaw explicitly rules out. It may also mix it up with the 2000 zł Inicjatywy Sąsiedzkie.

The verifier corrected the researcher's expected answer; the corrected answer is the one above.

**Sources:**

- <https://um.warszawa.pl/waw/sasiedzka/inicjatywa>
- <https://um.warszawa.pl/documents/54320/17190460/tekstujednoliconyuchNrLXI16922013douchNrLXXX264220.pdf/3e474de0-f255-dabc-8f7a-d92d6e761f67?t=1684836909735>

### PL-CIV-20 - Warsaw

**Question:** Nasza fundacja chce w Warszawie mały grant (art. 19a) na projekt trwający 4 miesiące za 18 000 zł. Czy to możliwe i jaki jest roczny limit?

*(Our foundation wants a small grant (art. 19a) in Warsaw for a 4-month project costing 18 000 zł. Is that possible, and what is the annual limit?)*

**Expected answer:** Yes, for offers submitted on or after 1 Sep 2026. The act of 19 June 2026 (Dz.U. 2026 poz. 1040) raised the per-task cap to 20 000 zł and removed the 90-day limit. The annual cap per organisation from Warsaw is 40 000 zł, and the city's small grants may use at most 30% of planned grants per bureau or district. Warsaw applies Ordinance 1620/2026 (in effect from 1 Sep 2026). The offer must be filed in the witkac.pl Generator during an open bureau or district nabór, cannot be completed afterwards, is published for 7 days of comments, and the decision follows within 10 working days. Offers filed before 1 Sep 2026 stay under the old limits: 10 000 zł, 90 days, 20 000 zł a year.

**Why the control may fail:** Most online sources, generic LLM knowledge and even a 2016 page on Warsaw's own NGO portal still say a maximum of 10 000 zł, a maximum of 90 days and 20 000 zł a year. The assistant would wrongly say the project is impossible. It may also miss that Warsaw only accepts offers through witkac.pl calls.

**Sources:**

- <https://api.sejm.gov.pl/eli/acts/DU/2026/1040/text.pdf>
- <https://api.sejm.gov.pl/eli/acts/DU/2025/1338/text.pdf>
- <https://bip.warszawa.pl/documents/53882/185769/1620_1709.docx/59fd0b17-453c-d11a-c73a-1e64c725bd68?t=1789649587471>
- <https://um.warszawa.pl/waw/ngo/-/procedura-1620-2026>
- <https://um.warszawa.pl/documents/59210/169590547/Procedura+1620_1709zal1.docx/bc287806-ffa3-acf6-c3d7-655a249da93c?t=1789716231231>
- <https://um.warszawa.pl/waw/ngo/-/male-granty-w-biurze-marketingu-miasta-urzedu-m-st-warszawy>

### PL-CIV-21 - Warsaw

**Question:** Mój 16-letni syn i jego kolega, niezameldowani w Warszawie, chcą złożyć wniosek o inicjatywę lokalną (np. odnowienie boiska). Czy mogą i czy potrzebują listy podpisów?

*(My 16-year-old son and his friend, not registered as residents in Warsaw, want to submit a local-initiative application (e.g. refurbishing a pitch). Can they, and do they need a list of signatures?)*

**Expected answer:** Yes, provided they actually live in Warsaw. At least two Warsaw residents may apply regardless of age and of registered address (zameldowanie). If the initiative is accepted, an adult (e.g. a parent) must sign the contract. A support list is optional and only adds points: 0 points with no list or fewer than 10 signatures, 2 points for 10-30, 4 points for more than 30. The application needs at least 24 points in total to be carried out. District coordinators can help write it.

**Why the control may fail:** A generic assistant assumes applicants must be adult, registered residents, or copies the participatory budget's mandatory signature thresholds. In Warsaw's local initiative, age and registration do not matter and signatures are optional scoring points.

The verifier corrected the researcher's expected answer; the corrected answer is the one above.

**Sources:**

- <https://warszawa19115.pl/en/-/inicjatywa-lokalna>
- <https://um.warszawa.pl/waw/sasiedzka/inicjatywa>
- <https://um.warszawa.pl//documents/54320/17190460/_Inicjatywa-lokalna-w-Warszawie-krok-po-kroku_proj_03.pdf/06b789af-55aa-9add-553d-30645315a0fe?t=1755001907766>
- <https://um.warszawa.pl/documents/54320/17190460/tekstujednoliconyuchNrLXI16922013douchNrLXXX264220.pdf/3e474de0-f255-dabc-8f7a-d92d6e761f67?t=1684836909735>
- <https://um.warszawa.pl/waw/sasiedzka/inicjatywa-koordynatorzy>

### PL-CIV-22 - Warsaw

**Question:** Czy Warszawa ma już uchwalony program współpracy z NGO na 2027 rok i do kiedy ogłosi konkursy ofert na cały 2027 rok?

*(Has Warsaw already adopted its NGO cooperation programme for 2027, and by when will it announce open competitions for the whole of 2027?)*

**Expected answer:** As of 27 Sep 2026 only a draft exists. It was consulted with NGOs until 21 Sep 2026 and no adopted resolution was found. The draft proposes announcing competitions for all of 2027 or its first half by 30 Nov 2026, with the same envelope as 2026: at most 350 million zł, of which at least 150 million zł for competitions and small grants. The programme in force is Resolution XXVI/1007/2025 for 2026, whose equivalent deadline was 28 Nov 2025. The BIP overview page is stale and still shows the 2025 programme.

**Why the control may fail:** An assistant either cites the 2026 dates (28 Nov 2025) as if they were current, presents the 2027 draft as adopted, or relies on the stale BIP overview that still describes the 2025 programme.

**Sources:**

- <https://um.warszawa.pl/waw/ngo/-/program-wspolpracy-m-st-warszawy-z-organizacjami-pozarzadowymi-w-2026>
- <https://bip.warszawa.pl/documents/53790/1552420/1007_uch_2025_.docx/3f2e2df8-0d35-8f84-d97a-db28cb112d4c?t=1758800855834>
- <https://bip.warszawa.pl/program-wspolpracy-m.st.-warszawy-z-organizacjami-pozarzadowymi>
- <https://um.warszawa.pl/waw/ngo/-/jaki-program-wspolpracy-z-organizacjami-pozarzadowymi-w-2027-roku>
- <https://um.warszawa.pl/documents/59210/167722323/Projekt_Uchwa%C5%82a_Program+wsp%C3%B3lpracy+w+2027_6_08.docx/e41137cc-4982-b0da-0e9d-c7a48365f026?t=1788180797305>

### PL-CIV-23 - Katowice

**Question:** Prowadzę stowarzyszenie w Katowicach. Czy możemy złożyć wniosek o inicjatywę lokalną i dostać dotację na nasz projekt sąsiedzki?

*(I run an association in Katowice. Can we apply for a local initiative and get a grant for our neighbourhood project?)*

**Expected answer:** Not in your association's own name. In Katowice the applicants are residents, either directly or through an NGO seated in Katowice that only passes on and represents their application; an application from an NGO in its own name may be rejected on formal grounds (order 1182/2020). The local initiative is not a grant: no dotacja is paid to the applicant, the city pays its expenses directly from its budget, and the city department or unit chooses contractors under public procurement law, so you cannot pick suppliers. Residents contribute social work, goods or money (art. 19e), and the scoring mainly rewards social work. Accepted initiatives are carried out under a fixed-term civil-law contract with the city. Applications are accepted from 1 October to 15 November of the year before the project year. For money paid to your association you would need a small grant (art. 19a) or an open competition.

**Why the control may fail:** Generic assistants describe the local initiative as a grant programme that NGOs apply to. Katowice's rules (Zarządzenie 1182/2020, 2026 brochure) forbid NGO applications in the organisation's own name and pay no grant at all.

The verifier corrected the researcher's expected answer; the corrected answer is the one above.

**Sources:**

- <https://katowice.eu/dla-mieszkanca/zaangazuj-sie/inicjatywa-lokalna>
- <https://bip.katowice.eu/Lists/Zarzadzenia/Attachments/11903/1182-2020a.pdf>
- <https://katowice.eu/SiteAssets/dla-mieszka%c5%84ca/zaanga%c5%bcuj-si%c4%99/inicjatywa-lokalna/broszura%20inicjatywa%20lokalna%202026.pdf>

### PL-CIV-24 - Katowice

**Question:** Ile maksymalnie można dostać w Katowicach w trybie małego grantu (art. 19a) i jak długo może trwać takie zadanie?

*(What is the maximum small grant (art. 19a) in Katowice and how long may the task last?)*

**Expected answer:** For offers submitted on or after 1 September 2026: up to 20 000 zł per task and at most 40 000 zł per organisation per calendar year. The 90-day limit no longer appears in the statute, and the national cap on small grants rises from 20% to 30% of planned NGO grants (Act of 19 June 2026, Dz. U. 2026 poz. 1040). Katowice's current small-grants page states the 20 000 / 40 000 zł limits. Offers submitted before 1 September 2026 keep the old rules: 10 000 zł, 90 days, 20 000 zł. Offers go through eNGO or e-Doręczenia and are published for 7 days in BIP, during which anyone may comment.

**Why the control may fail:** Generic assistants answer '10 000 zł and 90 days', which was true only before 1 September 2026. The city's own older 'Pozyskaj grant' page and Zarządzenie 1317/2026 still show the old limits, and the city page ties the transition to the contract date where the Act uses the offer submission date.

**Sources:**

- <https://api.sejm.gov.pl/eli/acts/DU/2026/1040/text.pdf>
- <https://katowice.eu/dla-mieszkanca/zaangazuj-sie/wspolpraca-z-ngo/dotacje/male-granty>
- <https://katowice.eu/dla-mieszkanca/zaangazuj-sie/pozyskaj-grant/male-granty>
- <https://api.sejm.gov.pl/eli/acts/DU/2025/1338/text.pdf>
- <https://bip.katowice.eu/Lists/Zarzadzenia/Attachments/16014/1317-2026a.pdf>

### PL-CIV-25 - Katowice

**Question:** Chcę zgłosić inicjatywę lokalną w Katowicach na 2027 rok. Do kiedy mogę złożyć wniosek, ile podpisów muszę zebrać i czy mogę go wysłać przez ePUAP?

*(I want to submit a local initiative in Katowice for 2027. What is the deadline, how many signatures do I need, and can I send it via ePUAP?)*

**Expected answer:** There is one call a year, from 1 October to 15 November of the year before the project year, so 1 October-15 November 2026 for projects in 2027. The city has not yet published the 2027 call page. Because 15 November 2026 is a Sunday, the city's own reasoning from 2025 (a deadline falling on a non-working day moves to the next working day) suggests Monday 16 November 2026, but this is an inference until the call is published. No minimum number of signatures is set, but a named support list of people living in Katowice is mandatory; more supporters give more points (up to 20 people: 1 point; 21-50: 2-3 points; over 50: 4-5 points). An application needs at least 51 of 68 points. ePUAP was accepted only until the end of 2025; submit on paper at Rynek 1, by post to ul. Młyńska 4, or by e-Doręczenia. The project must finish within 2027, and the 2026 edition had 1 000 000 zł for 190 projects.

**Why the control may fail:** Assistants tend to invent a fixed signature threshold (confusing this with the participatory budget), suggest rolling year-round applications, or point to ePUAP or SEKAP. The KATOobywatel page on a city domain still lists SEKAP.

**Sources:**

- <https://katowice.eu/dla-mieszkanca/zaangazuj-sie/inicjatywa-lokalna>
- <https://dzienniki.slask.eu/WDU_S/2020/5506/akt.pdf>
- <https://katowice.eu/SiteAssets/dla-mieszka%c5%84ca/zaanga%c5%bcuj-si%c4%99/inicjatywa-lokalna/broszura%20inicjatywa%20lokalna%202026.pdf>
- <https://katowice.eu/dla-mieszkanca/zaangazuj-sie/inicjatywa-lokalna/oceny-wnioskow-o-realizacje-zadan-publicznych-w-ramach-inicjatywy-lokalnej>

### PL-CIV-26 - Katowice

**Question:** Czy nasza organizacja może jeszcze zgłosić uwagi do programu współpracy Katowic z organizacjami pozarządowymi na 2027 rok i jaka kwota jest w nim przewidziana?

*(Can our NGO still comment on Katowice's 2027 programme of cooperation with NGOs, and what amount does it foresee?)*

**Expected answer:** Yes, until 29 September 2026: the consultation on the draft resolution runs from 15.09 to 29.09.2026. Send the opinion form by post to Wydział Polityki Społecznej (ul. Młyńska 4), hand it in at the Kancelaria (Rynek 1), e-mail it to agnieszka.lis@katowice.eu, or attach it on pks.katowice.eu. The draft plans at least 60 000 000 zł for 2027, the same as in 2026. It sits alongside the multi-year programme 2026-2030 (Resolution XXIII/423/25), which plans at least 18 000 000 zł a year. The 2026 programme itself is Resolution XXI/355/25 of 23.10.2025.

**Why the control may fail:** A generic answer gives no concrete dates, assumes the consultation is already over or not yet started, and confuses the annual programme (at least 60 million zł) with the new multi-year programme (at least 18 million zł a year).

**Sources:**

- <https://katowice.eu/dla-mieszkanca/zaangazuj-sie/wspolpraca-z-ngo/konsultacje-programu/konsultacje-programu-2027>
- <https://katowice.eu/ngo/SiteAssets/dla-mieszkanca/zaangazuj-sie/wspolpraca-z-ngo/konsultacje-programu/konsultacje-programu-2027/projekt%20uchwa%c5%82y%20-%20Program%20wsp%c3%b3%c5%82pracy%20miasta%20Katowice%20z%20organizacjami%20pozarz%c4%85dowymi%20na%202027.pdf>
- <https://bip.katowice.eu/Lists/Dokumenty/Attachments/148849/SESJA%20XXI-355-25.pdf>
- <https://bip.katowice.eu/Lists/Dokumenty/Attachments/149826/SESJA%20XXIII-423-25.pdf>

## Consultations and resident voice

### PL-CIV-27 - National law

**Question:** Mieszkam na stałe w Warszawie, jestem obywatelką Ukrainy. Czy mój podpis liczy się pod obywatelską inicjatywą uchwałodawczą do Rady m.st. Warszawy i ile podpisów trzeba zebrać?

*(I am a Ukrainian citizen living permanently in Warsaw. Does my signature count for a citizens' resolution initiative to the Warsaw City Council, and how many signatures are needed?)*

**Expected answer:** No. Art. 41a of the gmina act limits the initiative group to residents who have active voting rights to the city council. Under Electoral Code art. 10 § 1 pkt 3 lit. a these are Polish, EU and UK citizens who are 18 by election day and permanently reside in the gmina, so a Ukrainian citizen's signature is not counted. In a gmina with more than 20 000 residents, which includes Warsaw, the group needs at least 300 eligible residents. The council must debate the draft at the next session after it is filed, and within 3 months at the latest. The Warsaw City Council's own resolution sets the detailed rules (committee, promotion, formal requirements). These electoral-rights conditions apply to the resolution initiative. The participatory-budget provisions (art. 5a) refer to residents ('mieszkańcy') and leave the voting rules to each city's resolution.

**Why the control may fail:** Assistants often say any resident may sign, or they give wrong thresholds (1 000 signatures, 5 % or 15 %). They may also treat the rules for the participatory budget and the resolution initiative as the same.

The verifier corrected the researcher's expected answer; the corrected answer is the one above.

**Sources:**

- <https://api.sejm.gov.pl/eli/acts/DU/2026/662/text.pdf>
- <https://api.sejm.gov.pl/eli/acts/DU/2025/365/text.pdf>

### PL-CIV-28 - National law

**Question:** Czy wybory do rad dzielnic w Krakowie odbywają się razem z wyborami samorządowymi, tak jak w Warszawie?

*(Are district council elections in Kraków held together with the local government elections, as in Warsaw?)*

**Expected answer:** No. Only Warsaw's district councils are elected together with the city council, under the Electoral Code (Warsaw system act art. 7 ust. 1 and art. 35a ust. 2 of the gmina act). In Kraków, Katowice and other gminas, auxiliary-unit election rules come from the unit's statute adopted by the city council (art. 35). Those elections may not be ordered on the day of Sejm/Senate, presidential, European Parliament, local-council or mayoral elections (art. 35a ust. 1). A district council outside Warsaw has at most 21 members (art. 37 ust. 1). The actual election dates must be taken from each city's own resolutions.

**Why the control may fail:** Assistants apply Warsaw's model (18 statutory districts elected with the city council) to every Polish city. They also do not know the statutory ban on holding auxiliary-unit elections on general election days.

**Sources:**

- <https://api.sejm.gov.pl/eli/acts/DU/2026/662/text.pdf>
- <https://api.sejm.gov.pl/eli/acts/DU/2018/1817/text.pdf>

### PL-CIV-29 - Kraków

**Question:** Chcę zabrać głos w debacie nad raportem o stanie Krakowa. Czy wystarczy zapisać się na sesji i ile podpisów potrzebuję?

*(I want to speak in the debate on Kraków's report on the state of the city. Is signing up at the session enough, and how many signatures do I need?)*

**Expected answer:** No, signing up at the session is not enough. Under art. 28aa of the municipal act, you file a written application with the Chair of the City Council, backed by at least 50 signatures. Kraków has over 20,000 inhabitants; the 20-signature threshold is only for smaller municipalities. The deadline is the day before the day for which the report session is called. Residents speak in the order the Chair received their applications, and at most 15 may speak unless the Council raises the number. For the 2025 report, the Chair's (now archival) notice asked for applications at the City Council Chancellery secretariat, Plac Wszystkich Świętych 3-4, room 204 (7:30-15:30), by 23 June 2026 for the 24 June 2026 session, and kept the limit at 15. The mayor presents the report every year by 31 May, and the council debates it at the session on the vote of discharge (absolutorium). A new notice will set the place and deadline for the next debate.

**Why the control may fail:** A generic assistant tends to give the 20-signature threshold, which applies only to municipalities up to 20,000 inhabitants. It may also suggest signing up on the spot or online, or not mention the 15-speaker cap and the day-before deadline.

The verifier corrected the researcher's expected answer; the corrected answer is the one above.

**Sources:**

- <https://www.bip.krakow.pl/?news_id=254764>
- <https://api.sejm.gov.pl/eli/acts/DU/2026/662/text.pdf>

### PL-CIV-30 - Kraków

**Question:** Czy mogę poprzeć obywatelską inicjatywę uchwałodawczą w Krakowie przez internet, podpisując e-dowodem albo podpisem kwalifikowanym?

*(Can I support a citizens' resolution initiative in Kraków online, signing with my e-ID or a qualified signature?)*

**Expected answer:** In the city's OBIU module (bip.krakow.pl/obiu), you can sign only with a trusted signature (profil zaufany). Qualified signatures and personal (e-ID) signatures are not accepted there, even though resolution II/9/18, as amended in 2021/2022, allows all three in principle. To sign in OBIU you must live in Kraków, have active voting rights for the City Council and hold a valid, confirmed profil zaufany. A signature given in OBIU cannot be withdrawn. Committees may also collect support on paper lists or through other legally compliant electronic tools they choose, so check how a given committee collects. An initiative needs at least 300 residents with voting rights, and the committee needs at least 5.

**Why the control may fail:** A generic assistant usually says any electronic signature works, including e-dowód and qualified signatures, or that municipal initiatives need handwritten paper lists. It will not know the OBIU module or that a signature cannot be withdrawn.

The verifier corrected the researcher's expected answer; the corrected answer is the one above.

**Sources:**

- <https://www.bip.krakow.pl/_inc/rada/uchwaly/show_pdf.php?id=103448>
- <https://www.bip.krakow.pl/uslugi/BR-1>
- <https://www.bip.krakow.pl/?dok_id=161982>
- <https://www.bip.krakow.pl/_inc/rada/uchwaly/show_pdf.php?id=123241>
- <https://www.bip.krakow.pl/?dok_id=197749>

### PL-CIV-31 - Kraków

**Question:** Kiedy są następne wybory do rady dzielnicy w Krakowie i czy jako obywatelka Niemiec mieszkająca na stałe w Podgórzu mogę w nich głosować?

*(When is the next district council election in Kraków, and can I vote as a German citizen living permanently in Podgórze?)*

**Expected answer:** The current (9th-term) district councils were elected on 10 December 2023. Under the district statutes, their term is 5 years from election (BIP labels it 2023-2028). The City Council must set the next regular election for a non-working day between 14 days before and 30 days after the end of the term. That means roughly late November 2028 to early January 2029, and no date has been ordered yet. Under the statutes (§84), an EU citizen who is not Polish may vote for the district council if they are 18 by polling day and live permanently in the district. In 2023 the city told voters they had to be on the voter list: either registered for permanent residence in the district or entered, on request, in the Central Voter Register for a permanent voting district there. Podgórze is District XIII. Kraków has 18 districts; in 2023 almost all councils had 21 members, and districts IX and XVII had 15.

**Why the control may fail:** A generic assistant assumes district councils were elected with the April 2024 municipal elections and gives 2029, or says only Polish citizens may vote. It may also not know that Kraków's district councils have their own 5-year cycle set in their statutes.

The verifier corrected the researcher's expected answer; the corrected answer is the one above.

**Sources:**

- <https://www.bip.krakow.pl/?dok_id=175077>
- <https://bip.krakow.pl/?dok_id=170635>
- <https://www.bip.krakow.pl/_inc/rada/uchwaly/show_pdf.php?id=122172>
- <https://www.bip.krakow.pl/?dok_id=172027>
- <https://www.krakow.pl/aktualnosci/277171,26,komunikat,dzialaj_na_rzecz_lokalnej_spolecznosci__wez_udzial_w_wyborach_do_rad_dzielnic_.html>

### PL-CIV-32 - Kraków

**Question:** Ilu mieszkańców musi podpisać wniosek o konsultacje społeczne w Krakowie i czy ich wynik jest dla miasta wiążący?

*(How many residents must sign a request for public consultations in Kraków, and is the result binding on the city?)*

**Expected answer:** At least 300 Kraków residents must sign. The support list gives each person's name, address, PESEL and signature. A District Council, a group of at least 8 NGOs and several city bodies can also request consultations: the Public Benefit Council, the Council of Kraków Seniors, a council committee, the Youth City Council, a Civic Dialogue Commission, and the County Social Council for Persons with Disabilities. The request goes to the Department of Dialogue, Consultations and Civic Contact (ul. Zabłocie 22, room 13) or any City Office filing desk. The Mayor decides within 30 days and gives reasons if the request is refused. A consultation uses at least 3 forms, including at least one open meeting or workshop, and lasts at least 21 days. It is valid whatever the turnout, but the result is NOT binding on the city: it is auxiliary material to be taken into account. The report is published within 30 days, or at most 60 in justified cases. Current consultations are listed at obywatelski.krakow.pl.

**Why the control may fail:** A generic assistant often confuses consultations with a local referendum, with a turnout threshold and binding result. It may give another city's or a made-up signature threshold (e.g. 1,000), or point to dialogspoleczny.krakow.pl, which now hosts an unrelated lifestyle blog.

The verifier corrected the researcher's expected answer; the corrected answer is the one above.

**Sources:**

- <https://www.bip.krakow.pl/_inc/rada/uchwaly/show_pdf.php?id=102069>
- <https://www.bip.krakow.pl/uslugi/DK-2>

### PL-CIV-33 - Warsaw

**Question:** Chcę złożyć w Warszawie obywatelski projekt uchwały w sprawie należącej do zadań powiatu. Ile podpisów mieszkańców muszę zebrać i komu złożyć projekt?

*(I want to submit a citizens' draft resolution in Warsaw on a matter that is a county (powiat) task. How many residents' signatures do I need, and to whom do I submit it?)*

**Expected answer:** Warsaw is both a gmina and a powiat. Resolution XXI/540/2019 (§ 6 ust. 4) takes the signature count from the Municipal Self-Government Act (u.s.g.) for gmina tasks and from the County Self-Government Act (u.s.p.) for powiat tasks. For a county task, u.s.p. art. 42a ust. 2 pkt 2 requires at least 500 residents with voting rights to the Rada m.st. Warszawy (a gmina task would need 300). A committee of at least 5 residents is formed, and its members count toward the total. Signatures are collected on the annex 2 list template. The committee submits the draft, with its justification, the committee declaration and the signature lists, to the Chair of the City Council (Przewodniczący Rady Miasta). The President checks the signatures within 7 days. If there are too few, the Chair gives the committee 7 days to add more. The council must take up the draft at its next session and no later than 3 months after submission (u.s.p. art. 42a ust. 3; u.s.g. art. 41a ust. 3 for gmina tasks).

**Why the control may fail:** A generic answer quotes only art. 41a u.s.g. and says '300 signatures'. It misses that Warsaw is also a powiat and that its resolution routes county tasks to the 500-signature threshold. It may also invent a committee size or claim the President receives the draft.

The verifier corrected the researcher's expected answer; the corrected answer is the one above.

**Sources:**

- <https://edziennik.mazowieckie.pl/WDU_W/2019/13009/akt.pdf>
- <https://api.sejm.gov.pl/eli/acts/DU/2026/662/text.pdf>
- <https://api.sejm.gov.pl/eli/acts/DU/2025/1684/text.pdf>

### PL-CIV-34 - Warsaw

**Question:** Ile podpisów trzeba zebrać w Warszawie, żeby złożyć wniosek o konsultacje społeczne w sprawie mojej dzielnicy, do kogo go złożyć i czy na liście poparcia trzeba podać PESEL?

*(In Warsaw, how many signatures are needed to request a public consultation on a district matter, where do I file it, and must supporters give their PESEL number?)*

**Expected answer:** For a district matter, at least 200 residents of that district with voting rights to its district council must back the request. A city-wide matter needs 1,000 residents with voting rights to the Rada m.st. Warszawy and goes to the President. A district request goes to the district board (zarząd dzielnicy), filed at the district's Wydział Obsługi Mieszkańców, which decides within 30 days. Since resolution LXIII/2076/2022 (in force 4 May 2022), the list needs only the full name, the address as it appears in the voter register, and a handwritten signature. PESEL is no longer required.

**Why the control may fail:** The original 2013 resolution, still widely quoted, required PESEL. A generic assistant may also give a single national threshold or say residents cannot start consultations at all. It is also likely to miss the separate 200 and 1,000 thresholds and the different recipients.

**Sources:**

- <https://bip.warszawa.pl/documents/53790/4419672/tekstujednoliconyuchNrLXI1741472.docx/21fdfe56-cd61-564e-37ac-344675147770?t=1722122566652>
- <https://warszawa19115.pl/-/wniosek-o-przeprowadzenie-konsultacji>
- <https://edziennik.mazowieckie.pl/WDU_W/2022/4668/akt.pdf>
- <https://edziennik.mazowieckie.pl/WDU_W/2013/8442/akt.pdf>

### PL-CIV-35 - Warsaw

**Question:** Do kiedy i z iloma podpisami muszę się zgłosić, żeby zabrać głos w debacie nad raportem o stanie Warszawy w 2027 roku, i jak długo mogę mówić?

*(By when, and with how many signatures, must I sign up to speak in the 2027 debate on the report on the state of Warsaw, and how long may I speak?)*

**Expected answer:** The report is debated at the absolutoria session, which the BIP schedule (published 21 September 2026) sets for 24 June 2027; the date can change. File a written request with the Chair of the Rada m.st. Warszawy, backed by at least 50 signatures, by the day before the session at the latest. If the date holds, that is 23 June 2027. At most 15 residents speak, in the order their requests arrived, unless the council raises the number. In practice councillors and the President take precedence. A resident's speech is limited to 8 minutes (statute § 30 ust. 3).

**Why the control may fail:** A generic answer says 'by 31 May', which is actually the President's deadline for presenting the report. It may also say 20 signatures (the threshold for gminy under 20,000) or claim there is no time limit (only councillors are unlimited in this debate). It cannot know Warsaw's planned 2027 session date.

**Sources:**

- <https://api.sejm.gov.pl/eli/acts/DU/2026/662/text.pdf>
- <https://bip.warszawa.pl/documents/53790/4419672/tekstujednoliconyuchwa%C5%82yN1500848.docx/1e48d61c-227c-15d0-f632-e0165c397b0d?t=1722102951478>
- <https://bip.warszawa.pl/documents/53790/91553219/protokol_XXXVII_sesji_25-26_06_2026.docx/f863c61c-ce86-63d6-b048-bbe936a265ac?t=1788872472326>
- <https://bip.warszawa.pl/web/rada-warszawy/harmonogram>

### PL-CIV-36 - Warsaw

**Question:** Czy rady osiedli w Warszawie wybiera się razem z wyborami samorządowymi, tak jak rady dzielnic? Kiedy będą następne wybory do mojej rady dzielnicy?

*(Are Warsaw's neighbourhood councils (rady osiedli) elected together with the local elections, like the district councils? When are the next elections to my district council?)*

**Expected answer:** No. Warsaw's 18 district councils (rady dzielnic) belong to the districts, which statute makes mandatory, and they are elected together with the Rada m.st. Warszawy. The last election was on 7 April 2024 (term 2024-2029), so the next is due with the 2029 local elections; no date had been ordered as of September 2026. Neighbourhood councils (rady osiedli, samorządy mieszkańców) are lower-level units below the districts. They are not elected in the local elections: each district council calls their elections itself, and the voting method varies by district. Wawer's 13 osiedla elected councils on 24 November and 1 December 2024 and on 30 March 2025, at voters' meetings (resolution 54/XII/2025), for a 5-year term. Praga-Południe held a ballot in 8 osiedla on 24 May 2026, 10:00-20:00 (resolution 146/XXX/2026). In Śródmieście (9 osiedla) the councils are advisory, have no budget of their own and are unpaid.

**Why the control may fail:** Generic assistants tend to merge Warsaw's districts with neighbourhood councils. They may assume rady osiedli are elected in the April local elections, or that Warsaw's district councils are appointed rather than directly elected.

The verifier corrected the researcher's expected answer; the corrected answer is the one above.

**Sources:**

- <https://bip.warszawa.pl/web/guest/-/dzielnice-m-st-warszawy>
- <https://api.sejm.gov.pl/eli/acts/DU/2018/1817/text.pdf>
- <https://api.sejm.gov.pl/eli/acts/DU/2024/109/text.pdf>
- <https://api.sejm.gov.pl/eli/acts/DU/2026/662/text.pdf>
- <https://wawer.um.warszawa.pl/-/wybory-do-rad-osiedli-w-dzielnicy-wawer-2025>
- <https://srodmiescie.um.warszawa.pl/-/czym-jest-rada-osiedla>

### PL-CIV-37 - Katowice

**Question:** Mieszkam na Nikiszowcu (Dzielnica nr 16 Janów-Nikiszowiec). Czy 8 listopada 2026 r. mogę głosować w wyborach do mojej rady dzielnicy?

*(I live in Nikiszowiec (District 16 Janów-Nikiszowiec). Can I vote for my district council on 8 November 2026?)*

**Expected answer:** No. The City Council ordered elections for 8 Nov 2026 in all 22 districts (resolution XXVII/504/26). On 24 Sept 2026, however, the electoral commission of District 16 Janów-Nikiszowiec announced there will be no election there: it registered 16 candidates, and at least 23 (50% more than the seats) were needed. The BIP lists identical notices for districts 2, 5, 14, 15, 20 and 22. The election can be ordered again only after a new residents' initiative backed by at least 10% of the district's voters, and the City Council then sets the date. The District 16 council and board are currently not functioning. No non-election notice was published for the other 15 districts, which are scheduled to vote on 8 Nov from 7:00 to 19:00, one vote per voter.

**Why the control may fail:** A generic assistant will say that district council elections take place on 8 November 2026 across Katowice, or that district councils work normally. It will not know that seven districts lost their elections for lack of candidates, or about the 10% re-run rule.

The verifier corrected the researcher's expected answer; the corrected answer is the one above.

**Sources:**

- <https://bip.katowice.eu/Lists/Dokumenty/Attachments/151743/uchwa%C5%82a%20XXVII-504-26.pdf>
- <https://bip.katowice.eu/Lists/Dokumenty/Attachments/151738/Komunikat.pdf>
- <https://bip.katowice.eu/SiteAssets/Lists/Dokumenty/Uprawnienia/Obwieszczenie%20OKW%20RD%202%20Za%C5%82%C4%99ska%20Ha%C5%82da%20-%20Bryn%C3%B3w%20cz%C4%99%C5%9B%C4%87%20zachodnia.pdf>
- <https://dzienniki.slask.eu/WDU_S/2021/7673/akt.pdf>
- <https://bip.katowice.eu/RadaMiasta/Dzielnice/jednostka.aspx?idj=10>

### PL-CIV-38 - Katowice

**Question:** Chcę zabrać głos w debacie nad raportem o stanie miasta Katowice. Ilu podpisów potrzebuję i do kiedy muszę się zgłosić?

*(I want to speak in the debate on the Katowice report on the state of the city. How many signatures do I need, and by when must I apply?)*

**Expected answer:** Submit a written request to the Chair of the City Council supported by at least 50 signatures, because Katowice has over 20,000 residents. File it no later than the day before the session at which the report is presented. That is the session deciding on discharge (absolutorium), where the report is taken first; in 2026 it was the 29th session on 23 June 2026, and the date for 2027 is not yet known. Residents speak in the order their requests arrive, up to 15 unless the Council decides to allow more. In 2026 the Chair proposed, following earlier years, at most 3 minutes per resident. The Mayor must present the report by 31 May.

**Why the control may fail:** Assistants often give 20 signatures (the threshold for small municipalities), say no signatures are needed, or assume registration is on the day of the session.

The verifier corrected the researcher's expected answer; the corrected answer is the one above.

**Sources:**

- <https://api.sejm.gov.pl/eli/acts/DU/2026/662/text.pdf>
- <https://bip.katowice.eu/Lists/Dokumenty/Attachments/153113/Protok%C3%B3%C5%82%20z%20XXIX%20sesji%20Rady%20%E2%80%94%20BIP.pdf>

### PL-CIV-39 - Katowice

**Question:** Ile podpisów trzeba zebrać w Katowicach pod obywatelskim projektem uchwały i czy na liście poparcia trzeba podać PESEL?

*(How many signatures are needed in Katowice for a citizens' draft resolution, and must supporters give their PESEL on the list?)*

**Expected answer:** At least 300 people with the right to vote for the City Council. First, at least 5 such voters form a committee by written declarations giving name and address, and the committee informs the City Council, handing over the declarations. Promotion and signature collection may start from the day the declaration is filed with the Council. Under resolution VII/128/19, supporters give their name(s), address and date of birth and sign by hand; PESEL is not requested. The committee files the draft with the signature lists on paper or via ePUAP. The Council must debate it at the next session after filing, and no later than 3 months after filing.

**Why the control may fail:** Assistants may give 500, 1,000 or a percentage threshold, or say PESEL is required. PESEL was in the earlier Katowice resolution IV/65/19 and is common in other cities, but the rules the city cites (VII/128/19) ask for date of birth instead.

The verifier corrected the researcher's expected answer; the corrected answer is the one above.

**Sources:**

- <https://dzienniki.slask.eu/WDU_S/2022/6249/akt.pdf>
- <https://bip.katowice.eu/Lists/Dokumenty/Attachments/111746/sesja%20VII-128-19.pdf>
- <https://katoobywatel.katowice.eu/niezbednik/inicjatywa-uchwalodawcza/>
- <https://api.sejm.gov.pl/eli/acts/DU/2026/662/text.pdf>

### PL-CIV-40 - Katowice

**Question:** Ilu mieszkańców musi poprzeć wniosek o przeprowadzenie konsultacji społecznych w Katowicach, czy osoba spoza Katowic może w nich uczestniczyć i czy potrzebna jest minimalna frekwencja?

*(How many residents must back a request for public consultations in Katowice, can a non-resident take part, and is there a minimum turnout?)*

**Expected answer:** At least 100 residents must back the request. The request names a contact person with full details including PESEL, and the supporters' list gives names, addresses, PESEL and signatures. If there are errors, the office asks for corrections within 7 days. The Mayor answers in writing within a month, and a refusal can be appealed to the City Council within 14 days. Non-residents have no formal right to take part: §1(5) of resolution XXXVIII/860/13, which listed participants including non-residents, was annulled by the Silesian Voivode, and the Gliwice Administrative Court dismissed the city's complaint on that point (the annulment of §2(4)(4) was reversed). There is no turnout threshold: consultations are valid however many take part, and the result is not binding. The resolution names konsultacje.katowice.eu, which now redirects to the consultation section of katowice.eu.

**Why the control may fail:** A generic assistant may cite a percentage threshold, say anyone including non-residents may join (the unannulled-looking text of the resolution suggests this), or invent a turnout threshold that makes consultations binding.

The verifier corrected the researcher's expected answer; the corrected answer is the one above.

**Sources:**

- <https://dzienniki.slask.eu/WDU_S/2013/4873/akt.pdf>
- <https://katowice.eu/dla-mieszkanca/zaangazuj-sie/konsultacje-spoleczne/konsultacje-z-mieszkancami>
- <https://bip.katowice.eu/UrzadMiasta/AktyPrawaMiejscowego/szczegoly.aspx?idr=60538&menu=582>
