# Swiss TIP - Round 2 pitch (up to two minutes)

**Last update:** 16 September 2026

*Spoken script: about two minutes at a measured pace, for the round where
technical depth is judged.*

Moving to Zurich, a B permit holder wants to bring their teenage child after
four years, or their marriage is breaking down before the three-year mark, or
they fear their permit is automatically revoked over social assistance.
These are not edge cases we invented: they are questions where a generic AI
assistant reliably gets the law wrong, missing a statutory exception, citing
the wrong article, or predicting a loss the law does not actually require.

Swiss TIP is an MCP server that gives an assistant grounded access to
authoritative Swiss public information instead. The server never writes the
answer: it returns typed facts, the exact excerpt of the official page they
rest on, a citation with URL and access date, and an explicit status:
supported, needs more context, out of coverage, or stale. The calling
assistant still owns the conversation; Swiss TIP owns the evidence.

Our development pattern combines two disciplines. First, contract-first
engineering: every tool request and result is a typed, tested Pydantic
contract with an exported JSON Schema, checked before any of our packages
and apps - ingestion, extraction, build, runtime, server and console - is
allowed to touch it. Second, evaluation-driven development: instead of
trusting unit tests alone, we run six of our acceptance-test questions
through a real LLM against the live server, two standing relocation cases
and four further edge cases, and every run is logged with its transcript.
On an earlier release all six came back correct and cited, though five of
them took more tool calls than our budget allows. On the reviewed releases
of 14 September the two standing cases pass the automatic content checks again; their
answers still await grading by hand, and the four edge cases a rerun. We ran every one
of the six blind too, with no tools at all, to make grounding measurable
rather than assumed: zero of six held up without the server. One scenario
landed on the right date by coincidence, but for the wrong reason - it
never states the rule that its own sibling scenario, asked three minutes
later, gets backwards. The rest invent deadlines, a renamed federal office
and a web address that has not been current since 2015.

Today's release follows a newcomer to Zurich beyond the permit: social
insurance when leaving, tax at source, the foreign driving licence, health
insurance and naturalisation, at the federal, cantonal and city level, from
official pages that are almost all in German, with the facts stated in
English: 77 concepts, 290 facts, every one checked by one named reviewer
against the official excerpt it cites.
That review rides on each fact, not in a footnote: the assistant sees who
confirmed a statement and when, can tell the user, and for a question where
only a confirmed statement will do it asks for reviewed facts only and gets a
named gap for anything unconfirmed. Reliability becomes something the caller
can filter on. A corpus of more than 12,000 pages from sources for all 26
cantons is already acquired for the next release, to be built with the same
tooling and served through the same contract. We have put a Codex
multi-agent setup on the goal of finishing it: residence permits for the whole
of Switzerland.

Swiss TIP: cited, honest answers an assistant can trust, built to extend.

---

## Additional info for Q&A

- **Contract-first evidence:** `docs/architecture/tool-contracts.md` and its
  exported schema bundle; every package under `packages/` and every app under
  `apps/` ships its own offline `unittest` suite that needs no network
  (`./.venv/Scripts/python.exe -m unittest discover -s packages/runtime/tests`,
  and the same for each folder, counts them).
- **Evaluation-driven evidence:** the execution table of
  [docs/product/user-acceptance-tests.md](../product/user-acceptance-tests.md)
  records every live run, passing or not. The acceptance-test questions of
  UAT-1 and UAT-3 to UAT-6 passed on grounding against the real server on release
  `mvp-zurich-2026-09-13-v2`, the last release with clean end-to-end passes:
  UAT-1 within its budget of 3 calls, the four edge cases over their call
  budget (7 to 8 calls). On release v5 four of nine
  live sessions completed and each failed at least one mandatory criterion;
  the other five were cut off by provider rate limits. On the first reviewed
  release (`mvp-zurich-2026-09-14-v1`) the standing cases ran twice over HTTP against the container
  image: the harness's content checks passed every time, and the answers are
  not yet assessed by hand
  (record `.local/experiments/2026-09-14-container-http-acceptance.md`). The Czech
  registration standing case on v2 is recorded verbatim in Appendix A of
  `.local/experiments/2026-09-13-standing-cases-exchanges.md`.
  The cases were also run blind as a no-server control: the four edge
  cases (family reunification deadline, marital separation exception,
  L-to-C permit timing, social assistance revocation) in
  `.local/experiments/2026-09-13-edge-case-questions.md`,
  the standing case in
  `.local/experiments/2026-09-13-standing-cases-control.md`.
  Every verdict is re-gradeable from the saved transcript, not just the
  harness's automatic check.
- **Efficiency measured, not assumed:** a separate record,
  `.local/experiments/2026-09-13-caller-efficiency.md`,
  measures tool-call and byte cost per question and the server-side changes
  that cut it, directly against the challenge's agent-efficiency criterion.
- **Agent-built next release:** the swiss-residence knowledge base (all 26
  cantons) was worked on by a Codex multi-agent setup in the original
  hackathon repository; it was never built or reviewed and is not part of
  the MVP, so do not quote its numbers as served.
- **Offline gate:** `scripts/test/mcp/check_server.py` runs a round trip
  against the committed KB1 release without a model, over stdio or, with
  `--url`, over Streamable HTTP; the container workflow runs it against the
  built image before pushing it.
- **Scope honesty:** all 290 KB1 facts are `human-reviewed` (release
  `mvp-zurich-2026-09-16-v1`): one named reviewer confirmed each in the admin
  console's review queue, which shows the statement next to its cited
  excerpt; 249 of them in bulk groups that stay marked on the fact, among them
  all 149 facts of the five topics added on 15 September and 29 of the 37
  facts drafted from the EU free movement agreement on 16 September. It is not a legal
  review and not an independent second opinion; say so if asked. The ten
  acceptance cases of the added topics (UAT-8 to UAT-17) pass the model-free
  check in the build and have no live caller run yet; do not quote them as
  run. The review status is reported in
  every tool result, not just in documentation. It is reported twice: each
  `resolve` fact carries its own `review_status` (plus `reviewed_on` and
  `reviewed_by` once confirmed), and every result's `limitations` name the
  counts for the whole release. A caller that must not relay an unconfirmed
  statement sends `reviewed_only`; concepts with no reviewed fact then answer
  `OUT_OF_COVERAGE` with a `review_status_not_met` gap. On today's release
  every fact passes the filter, and the answer carries the reviewer's name
  and date; a new, unreviewed fact added later would be withheld from such a
  caller until someone confirms it.
