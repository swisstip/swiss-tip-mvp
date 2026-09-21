# SwissTIP - One-minute jury pitch

**Last update:** 21 September 2026

*Spoken script: approximately one minute at a measured pace.*

Moving to Zurich - which rules apply to you?

SwissTIP goes beyond web search and RAG: a governed knowledge platform with versioned evidence, explicit scope and traceable sources.

Our prototype combines source ingestion, AI-assisted extraction, scoped retrieval, optional semantic ranking and a working MCP server. Evidence stays tied to its source and jurisdiction.

Our goal is simple: ask in your language, without translating your search terms first. The assistant asks for missing context and makes insufficient evidence explicit.

Our Zurich release serves reviewed facts from German official pages, from residence permits to tax at source, health insurance, the foreign driving licence and naturalisation, and finds them from German questions; nationwide coverage and more languages come next.

The opportunity goes further: potential myAI integration, reuse across assistants, and a platform that banks, insurers and other regulated institutions could use as a governed source of truth for regulatory and compliance knowledge.

SwissTIP: trusted knowledge, reusable across AI.

---

## Additional info for Q&A

The served Zurich release holds 77 concepts and 290 facts from 44 cited documents in seven topics: residence permits and registration (with the text of the EU free movement agreement), the cantonal migration offices, social insurance on arrival and departure, tax at source, the foreign driving licence, health insurance and premium reduction, and naturalisation, at the federal, Canton of Zurich and City of Zurich levels. Every fact is `human-reviewed` by one named reviewer against its cited excerpt, the 149 facts of the moving-to-Switzerland and naturalisation topics and 29 of the 37 treaty facts in bulk groups; it is not a legal review ([COVERAGE.md](../../COVERAGE.md), [LIMITATIONS.md](../../LIMITATIONS.md)). Its search terms are German and English: German questions, including one Zurich German case, rank the right concept first offline, while French and Italian terms exist only where an excerpt is French or Italian. The seventeen acceptance cases pass the model-free check; the ten cases of the added topics have no live caller run yet.

For the next release, the nationwide corpus, fetched and extracted outside Git, holds **12,117 official pages** of 12,461 download targets, from a catalogue of **59 federal and cantonal sources covering all 26 cantons**, with a text dataset of 12,117 records ([releases/README.md](../../releases/README.md)). Its 304 concept candidates passed automated review only; no KB2 release is built or served.

These are source-preparation statistics. Exhaustive coverage, semantic interpretation, translation equivalence and OCR remain incomplete. [Corpus statistics and limitations](full-presentation.md#slide-26---additional-info-nationwide-residence-permit-corpus) are available as backup material outside the one-minute spoken script.

If asked how SwissTIP compares with existing solutions: other Swiss MCP servers (the Fedlex servers, mcp-swiss, the City of Zurich open data server, ZüriCityGPT's site search) pass queries through to live data, and chatbots such as ZüriCityGPT or the migration office chatbots answer people directly. SwissTIP is the evidence layer any assistant can call. It serves reviewed facts with a jurisdiction and date scope, and it names what it does not cover. It complements those servers rather than replacing them: a client can connect ZüriCityGPT's server next to SwissTIP for City of Zurich questions outside its topics ([related work](../product/related-work.md)).
