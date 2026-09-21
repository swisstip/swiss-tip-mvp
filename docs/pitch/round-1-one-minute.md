# Swiss TIP - Round 1 pitch (one minute)

**Last update:** 21 September 2026

*Spoken script: about one minute at a measured pace.*

Moving to Zurich, a B permit holder wants to bring their teenage child after
four years, or their marriage is breaking down before the three-year mark, or
they fear losing their permit over social assistance. Ask a generic AI
assistant these questions and it invents conditions, cites law articles that
do not exist, and in every one of our recorded runs it missed the exception.

Swiss TIP is an MCP server that gives an assistant grounded access to
authoritative Swiss sources instead. It never composes the answer itself: it
returns cited facts, the exact excerpt they rest on, and an honest "not
covered" when it does not know.

We built it contract-first, with typed, tested contracts before any package
touched them, then tested it the only way that counts: six of our
acceptance-test questions run through a real LLM against the live server. On
release `mvp-zurich-2026-09-13-v2` all six came back correct and cited,
though five took more tool calls than we budget. The same six questions with
no server at all: zero out of six reliably correct, inventing deadlines, a
renamed authority and a stale web address instead.

Swiss TIP: cited answers an assistant can trust, not another retrieval demo.

---

## Additional info for Q&A

The committed KB1 release (`mvp-zurich-2026-09-16-v1`) covers federal law,
Canton Zurich and the City of Zurich from official pages that are almost all
German, with English statements, in seven topics: residence permits and
registration (with the text of the EU free movement agreement), the cantonal
migration offices, social insurance on arrival and departure, tax at source,
the foreign driving licence, health insurance and premium reduction, and
naturalisation. It holds
77 concepts and 290 facts, every one `human-reviewed` against its cited
excerpt by a named reviewer. The ten
acceptance cases of the added topics (UAT-8 to UAT-17) pass the model-free
check and have no live caller run yet. Every fact the server
returns carries that status, the reviewer and the date on the fact itself, so
the calling assistant can say who stands behind a statement, and a caller
facing a critical question can send `reviewed_only`, which serves confirmed
facts only and names a gap for anything unconfirmed. A
corpus of 12,117 official pages (of 12,461 download targets) from sources
for all 26 cantons is already fetched and extracted for the next release,
to be built with the same tooling and contract.
The acceptance-test questions of UAT-1 and UAT-3 to UAT-6
([docs/product/user-acceptance-tests.md](../product/user-acceptance-tests.md))
passed on grounding against the real server on release
`mvp-zurich-2026-09-13-v2`, four of them over the call budget; that is the
last release with clean end-to-end passes. On the reviewed releases since,
the standing cases pass the harness's content checks and are not assessed by
hand (record `.local/experiments/2026-09-14-container-http-acceptance.md`);
the execution table of the acceptance tests records every run. The standing
relocation case (Czech EU registration deadline) is recorded in
`.local/experiments/2026-09-13-standing-cases-exchanges.md`,
and the four further edge cases (family reunification deadline, marital
separation exception, L-to-C permit timing, social assistance revocation)
are recorded verbatim in
`.local/experiments/2026-09-13-edge-case-questions.md`.
They were also run blind as a no-server control; the standing case's
blind runs are in
`.local/experiments/2026-09-13-standing-cases-control.md`.
