---
name: build-knowledge-graph
description: Build or extend the Swiss knowledge graph (graphs/<graph>/) with Claude Code agents, the way packs are built - sources, fetch, Derive from packs, reader agents writing cited nodes and edges into graph.yaml as assistant-authored-unreviewed, orientation checks, compile, then hand over to review in the admin console. Use for "build the knowledge graph", "extend the graph with <domain/canton/source>", "add <X> to the graph".
---

# Build or extend a knowledge graph

**Last update:** 24 September 2026

The graph is the orientation `get_knowledge_graph` serves before search: which
level of the state sets the rules of a domain, who carries them out and decides,
the office a person deals with at their place, the laws and the authoritative
source, and the pitfalls. Design: `swiss-tip/docs/architecture/knowledge-graph.md`.
Worked example: `swiss-tip/docs/product/agent-built-knowledge-graph.md`.

Arguments: `build <graph>` (default `ch`) or `extend <what>` (a domain, a canton,
a source). The session runs in this repository (`swiss-tip-mvp`) with the code
repository next to it (`../swiss-tip`) and the shared `.venv` one level up.

## Rules for the coordinator and every agent

Repeat them in every agent prompt.

- **Never type a quotation.** Every node summary and edge rests on an excerpt
  that already exists: a pack's evidence ID (`releases/<pack>/release.json`) or a
  block range of the graph's own text dataset (`.local/graph-<graph>/text/`).
- **Never translate a name.** `names` are copied verbatim from a cited excerpt;
  the compile refuses a name no excerpt contains.
- **Never set `human-reviewed`, never attest.** Agents write
  `assistant-authored-unreviewed`; only the admin console's review sets
  `human-reviewed` with a person's name.
- **Never invent an office, a law or a competence.** A claim without an excerpt
  that states it is left out and listed as a gap.
- **Never edit an item a person touched** (author other than `derive` or an
  agent, or any review status other than the unreviewed ones).
- Use only the relation vocabulary of `swisstip.core.graph.RELATIONS`, with its
  endpoint kinds.

## Steps

Commands assume `PY=../.venv/bin/python` (Windows: `..\.venv\Scripts\python.exe`)
and are run from this repository.

1. **Scope.** Read `graphs/<graph>/graph.yaml` (if it exists) and the pack
   topics (`releases/*/curation.yaml`). Decide the domains, roles and levels the
   build or extension adds; write them down as a skeleton list with node IDs
   (`domain.<slug>`, `role.<slug>`, ...). Bridge each pack topic to its domains
   with `graph_nodes` in the pack's `curation.yaml`.
2. **Sources.** Launch `graph-scout` agents (one per missing area, in parallel)
   for pages no pack carries yet (constitution articles, federalism overviews).
   Add what they return to `graphs/<graph>/sources.json` and `sources.md`,
   bumping the catalogue version.
3. **Fetch and extract.**
   `$PY -m swisstip.builder.cli <graph> --graph --packs-dir . --until validate-text --download`
   (in the admin console: Graph > Runs > Run).
4. **Derive.** `$PY -m swisstip.builder.cli <graph> --graph --packs-dir . --from derive --until derive --apply-derive`.
   It adds places, institutions, laws, sources and the `legal_basis`,
   `published_by`, `authoritative_source` and `instance` links from the packs.
5. **Readers.** Prepare one evidence packet per domain group
   (`.local/graph-<graph>/readers/<group>.json`: the evidence IDs, URLs, bases
   and excerpts of the bridged topics, plus the graph's own text records) and
   launch one `graph-reader` agent per packet, in parallel, with the skeleton
   list. Each writes `.local/graph-<graph>/readers/<group>-proposal.yaml`.
6. **Merge.** Convert every proposal's evidence IDs into citations
   (`pack: {pack, evidence_id, excerpt_sha256}` or `text: {document_id,
   first_block, last_block}`), drop duplicates and anything citing an unknown
   excerpt, and append to `graph.yaml`. Keep the proposals' gaps in a note.
7. **Checks.** Launch `graph-checker` for `graphs/<graph>/checks.yaml`: one case
   per acceptance question of the packs that touches the graph, plus one
   question without a place.
8. **Compile and check.**
   `$PY -m swisstip.builder.cli <graph> --graph --packs-dir . --from compile`.
   Fix what the compiler refuses (unknown endpoints, names not in the excerpt,
   an instance without a place) until the stage passes.
9. **Embed.** Name the graph in each pack's curation
   (`knowledge_graph: ../../graphs/<graph>/graph.json`) and rebuild the pack, or,
   when its run is not at hand, `$PY -m swisstip.build.graph_cli embed releases/<pack>`.
10. **Hand over.** Report the counts (nodes, edges, review statuses, dropped
    items, gaps) and tell the person to review in the admin console
    (Review > Graph, or Graph > Explore), then to re-accept and attest the packs.
