# Related work

**Last update:** 18 September 2026

Swiss TIP is not the only project that gives AI assistants Swiss public
information. This document names the closest projects and says how Swiss TIP
differs from them. It also shows how a client can run a complementary server
next to Swiss TIP.

The survey was made on 18 September 2026 from public web pages. Everything
said here about another product comes from its own pages, except the
ZüriCityGPT MCP server, which was called directly on that day (the tool
list and one search).

## What Swiss TIP does differently

- **Facts prepared in advance, not passed through.** The other Swiss MCP
  servers found here send the caller's query to a live API or a site search
  and return whatever comes back. Swiss TIP serves facts that were written
  and reviewed before release. Each fact quotes an exact excerpt of an
  official page, with its URL, access date and hashes, inside a versioned
  release.
- **Applicability as part of the request.** `resolve` takes a jurisdiction
  (country, canton, municipality), a date and the user's situation, and it
  applies federal rules to every canton and cantonal rules to their
  municipalities. With a search-based server, the caller has to work out
  whether a page applies. ZüriCityGPT's operator names the confusion of city
  and cantonal responsibilities as a known weakness.
- **Gaps are named.** `OUT_OF_COVERAGE`, `NEEDS_CONTEXT` and `STALE` tell the
  caller what is missing and why. A search server returns weaker hits
  instead.
- **Every fact states its review status and legal basis** (law, directive,
  guidance or summary).
- **No live requests at run time.** The server answers from the release
  alone.

The other servers are better in some respects, and Swiss TIP does not try
to replace them:
- They are broader. mcp-swiss alone has about 76 tools.
- They serve live data: waste collection dates by street, timetables and
  parking.
- They read federal acts in full: the Fedlex servers return complete acts,
  while Swiss TIP quotes only the excerpts its facts rest on.

## Swiss MCP servers

| Server | Operator | What it serves | Relation to Swiss TIP |
| --- | --- | --- | --- |
| ZüriCityGPT MCP, `https://zuericitygpt.ch/mcp` | [Liip](https://www.liip.ch/en/blog/webmcp-making-liipgpt-tools-discoverable-by-browser-ai-agents) | Three tools: `search` over its knowledge base of stadt-zuerich.ch pages (with a mode limited to city council decisions), `get_waste_collection` and `get_timetable_info`. A search returns the page URL, title, page date and text, not a generated answer. No authentication. | The closest complement: City of Zurich topics that the Swiss TIP release does not publish. |
| [Zurich Open Data MCP](https://www.liip.ch/en/blog/city-of-zurich-s-900-open-data-sets-now-have-an-mcp-server), `https://zurich-opendata-mcp.liipgpt.ch/mcp` | Hayal Oezkan, hosted by Liip | 21 tools over six City of Zurich open data interfaces (the data catalogue, geodata, the city parliament, tourism, linked data, parking), plus the two city tools of ZüriCityGPT | Open data rather than rules. The city lists it among the [third-party applications](https://www.stadt-zuerich.ch/de/politik-und-verwaltung/statistik-und-daten/open-government-data/anwendungen/anwendungen-2026/ckan-mcp-server.html) that use its data; it does not operate it. |
| [mcp-swiss](https://github.com/vikramgorla/mcp-swiss) | vikramgorla (GitHub) | About 76 tools over federal and other open data: transport, weather, geodata, the commercial register, parliament, statistics, waste collection | Broad live data and no rules on residence or procedures |
| [Fedlex Connector](https://fedlex-connector.ch/), [fedlex-mcp](https://github.com/malkreide/fedlex-mcp), [switzerland-law-mcp](https://github.com/Ansvar-Systems/switzerland-law-mcp) | Jeremy Bacharach (a private project, over 20,000 queries a month by its own count for August 2026), malkreide, Ansvar Systems | Federal legislation through the Fedlex SPARQL endpoint | Full texts of acts, with no cantonal practice, no applicability check and no coverage statement |
| [schwaizer-opendata-mcp](https://github.com/ishumilin/schwaizer-opendata-mcp), [Pipeworx opendata.swiss](https://www.pulsemcp.com/servers/pipeworx-opendata-swiss) | Community | The opendata.swiss catalogue | Metadata about datasets, not answers |
| [malkreide's single-source servers](https://github.com/malkreide/swiss-public-data-mcp) | malkreide | Transport, federal statistics, court decisions, electricity, public media news and others | Each one wraps a single source |

## Chatbots on the same subjects

These are finished products for people, not tools that another assistant
can call.

- **[ZüriCityGPT](https://www.liip.ch/en/blog/zuricitygpt-10-months-later)**
  (Liip) is a chatbot over stadt-zuerich.ch pages, with a variant that uses
  only [open models](https://www.liip.ch/en/blog/zuricitygpt-oss-version-using-only-open-source-models).
  A model writes each answer from pages it retrieves.
- **The chatbot of the Canton of Zurich migration office**
  ([Abraxas](https://www.abraxas.ch/de/referenzen/migrationsamt-zh-chatbot))
  answers questions about entry procedures and links to the forms and
  directives. Migration offices in
  [Basel-Landschaft](https://www.baselland.ch/politik-und-behorden/direktionen/sicherheitsdirektion/medienmitteilungen/dreisprachiger-chatbot-beim-amt-fuer-migration-und-buergerrecht)
  (in German, English and French) and
  [Basel-Stadt](https://polizeiticker.ch/artikel/eumzug-und-chatbot-im-kanton-basel-stadt-neue-digitale-dienstleistungen-im-bevolkerungs-und-im-migrationsamt-171937)
  run similar chatbots.
- **SynerKI** is the Canton of Zurich's AI service platform for its own
  administration: CHF 2.76 million for the project, with annual running
  costs of CHF 3.87 million
  ([Netzwoche](https://www.netzwoche.ch/news/2026-07-10/kanton-zuerich-treibt-ki-einsatz-in-der-verwaltung-voran)).
- **Relocation assistants** from relocation firms and custom GPTs, and
  **legal AI for lawyers**
  ([DeepLegal](https://www.deeplegal.swiss/en/), [Silex](https://silex.legal/en),
  [Legislator](https://legislator.ch/about), [Omnilex](https://omnilex.ai/en)).
  The legal tools answer with citations to Swiss law and are paid products
  for professionals.

## The same idea abroad

- **[GOV.UK Chat](https://gds.blog.gov.uk/2026/05/14/gov-uk-chat-launches/)**
  opened in the GOV.UK app in May 2026. It answers from the government's
  published guidance, about 80,000 pages. It is a chatbot built by a
  government, not a server for other assistants.
- **France** publishes an official MCP server for its open data catalogue,
  [mcp.data.gouv.fr](https://www.numerique.gouv.fr/actualites/serveur-mcp-datagouv-retex-clarifications-donnees-publiques-ia/).
  [Albert](https://www.info.gouv.fr/actualite/ia-connaissez-vous-albert),
  the French government's AI assistant, helps the advisers who assist the
  public with administrative procedures, and its answers link to their
  sources.
- **In the United States**, a GSA report on
  [improving LLM access to federal data](https://digitalcorps.gsa.gov/pdfs/MCP_Report.pdf)
  recommends that agencies publish MCP servers, so that authoritative
  sources stay available next to community tools. GSA also runs an
  [MCP hackathon](https://www.gsa.gov/artificial-intelligence/ai-community-of-practice/events-and-training/mcp-server-and-ai-agent-government-hackathon)
  across government.

## Running a companion server next to Swiss TIP

MCP clients can connect several servers at once. A client that connects both
Swiss TIP and the ZüriCityGPT server can search stadt-zuerich.ch when Swiss
TIP declines a City of Zurich question with `OUT_OF_COVERAGE`. The caller
makes that choice. Swiss TIP never names or calls the other server.

OpenCode, in `opencode.json`:

```json
{
  "$schema": "https://opencode.ai/config.json",
  "mcp": {
    "swiss_tip": {
      "type": "remote",
      "url": "http://127.0.0.1:8000/mcp",
      "enabled": true,
      "timeout": 60000
    },
    "zuericitygpt": {
      "type": "remote",
      "url": "https://zuericitygpt.ch/mcp",
      "enabled": true
    }
  }
}
```

Claude Code:

```shell
claude mcp add --transport http swiss-tip http://127.0.0.1:8000/mcp
claude mcp add --transport http zuericitygpt https://zuericitygpt.ch/mcp
```

Each client puts the server name in front of the tool names
(`swiss_tip_search` and `zuericitygpt_search` in OpenCode), so the two
`search` tools do not clash.

This combination fits Swiss TIP's decline guidance. After
`OUT_OF_COVERAGE`, the caller must tell the user that Swiss TIP does not
cover the question, and it must not present an answer from general
knowledge as grounded. An answer built from the companion's results carries
that server's page citations. It carries none of Swiss TIP's guarantees: no
human review, no applicability check, no excerpt hashes and no stale date.

Status: this setup is documented but not tested. The ZüriCityGPT server
answered its tool list and a search on 18 September 2026. The two servers
have not been run together through the acceptance harness, and the Swisscom
test harness connects Swiss TIP alone.

## Why Swiss TIP does not refer the user to other services

A decline names the gap and nothing else. It does not add a link to
ZüriCityGPT or to any other service, for three reasons:
- A Swiss TIP response carries only evidence from the release. A pointer to
  another service whose answers are unreviewed, or written by a model,
  would break that.
- A test harness that connects Swiss TIP alone has no way to call a server
  that a response names.
- Combining servers belongs in the client's configuration, where the user
  decides which services to trust.
