# Interview primitive library

Technical knowledge compiled into reusable primitives, so Physis can retrieve,
rank, cache and combine it instead of re-reading a textbook.

```
question → normalize → retrieve primitives → expand related → expand recipes
         → rank (RRF) → compose (answer)
```

Not `Kubernetes.md` + `Rust.md` + `SystemDesign.md`. A graph of executable
concepts, where one primitive is usable across many architecture problems:

```
reconciliation  ↕  desired-state  ↕  idempotence  ↕  retry  ↕  backoff
bounded-channel ↕  backpressure   ↕  worker-pool  ↕  semaphore ↕ load-shedding
```

## Layout

| Directory | Objects | What it is |
|---|---|---|
| `k8s/` | 45 | Kubernetes workloads, networking, config/state, operations, control plane |
| `rust/` | 38 | ownership, errors, sync, async/Tokio, HTTP, shutdown |
| `design/` | 27 | cross-cutting architecture primitives (backpressure, idempotency, caching…) |
| `recipes/` | 20 | compositions of primitives that answer architecture exercises |
| `quiz/` | 14 | interview questions with the concepts they grade |
| `CHEATSHEET.md` | — | generated one-line-per-primitive review sheet |

Every primitive is a `.prim` file — canonical text, already observed by
`physis observe` as an ordinary `file:` entity. Primitive ids (`prim:<id>`) are
*projection addresses* used for graph traversal; they are deliberately never
written into the canonical world, because a second graph is exactly what the
architecture forbids.

## The `.prim` format

Line-oriented, dependency-free (no YAML crate), code blocks round-trip
byte-for-byte:

```text
# comment
key: scalar value
key: |
  block scalar; leading 2 spaces are stripped, nested indentation survives
key:
  - list item
  - command with a reason => the diagnostic question it answers
```

Fields are independently retrievable — that is the point of the format. A caller
asks for `invariant` or `answer_30s` alone; nothing forces it to load the whole
object.

## Schema

| Field | Required | Purpose |
|---|---|---|
| `id` | yes | stable id, dotted (`k8s.deployment.rolling-update`) |
| `kind` | yes | `kubernetes` · `rust` · `design` · `recipe` · `quiz` |
| `title` | yes | human label |
| `aliases`, `tags` | — | retrieval vocabulary (weighted above prose) |
| `questions` | — | interview questions this primitive answers directly |
| `invariant` | yes | the one line that must stay true (also the WHY in `:arch`) |
| `answer_30s` | yes (primitives) | default payload |
| `answer_2m` | — | deep only |
| `when_to_use` / `avoid_when` | — | decision boundaries |
| `commands` | — | `cmd => what diagnostic question it answers` |
| `minimal_example` | — | deep only, real config/code |
| `failure_modes` | — | what actually breaks in production |
| `misuse` | — | `pattern => why it is wrong` (quiz grading uses these) |
| `follow_ups` | — | what an interviewer asks next |
| `related` | — | undirected concept edges (the graph) |
| `compose` | recipes | `primitive-id => why this recipe needs it` |
| `flow` | recipes | authored diagram for `:arch` |
| `properties` | recipes | what the composition buys |
| `track`, `question`, `expects`, `answer`, `hints` | quiz | grading vocabulary + model answer |
| `sources` | — | official docs; deep only, never in the default payload |

Corpus integrity is enforced at load, not assumed: duplicate ids, unresolved
`related`/`compose` targets, missing invariants/short answers, recipes without a
composition and quiz items without `expects` are all **load errors**. The
`tests/invariants/interview_corpus.rs` suite additionally proves that no
primitive is unreachable in the concept graph.

## Token discipline

```
name · one-line invariant · 30-second answer      ← default retrieval payload
2-minute answer · example · commands · sources    ← deep, loaded on demand
```

Measured over the current corpus: 110 primitives cost ~9.0k tokens at the
default depth and ~39.9k tokens deep — a 4.4× reduction on the surface that is
actually retrieved. A single `:q` answer is budgeted (400 tokens by default,
`:arch` 600) and reports what it dropped, because an answer that silently
exceeds its budget is not cheaper, just later.

## Commands

```bash
physis interview                               # corpus status, kinds, fingerprint, token economy
physis q "how do I deploy without downtime?"   # composed answer
physis q "..." --depth deep --budget 900       # command intents + 2m material
physis arch "design a service receiving 100k events per minute"
physis quiz kubernetes                          # ask
physis quiz kubernetes --answer "…"             # grade against declared concepts
physis quiz rust --reveal                       # model answer (deep payload)
physis prim k8s.deployment.rolling-update --depth deep
physis prim "how does rolling update work" --search
physis related k8s.service --depth 1            # concept graph
physis cheat --track rust --commands            # one line per primitive

# Optional model paths (build with --features llm):
physis interview --llm                          # probe the resolved provider
physis q "…" --llm                              # add the semantic retrieval leg
physis quiz rust --answer "…" --llm             # model fills the declared rubric
```

HUD (`physis-hud`): tab 18 **Interview**, with the same verbs in the magic
textbox — `:q`, `:arch`, `:quiz`, `:prim`, `:related`, `:explain`, `:cheat`,
`:interview`, plus `:llm on|off|status` for the model paths. `j`/`k` walk the concept graph, Enter descends into the selected
primitive, `:explain` loads its deep reference. Store-free snapshots for
CI/docs: `--snapshot --view=cheat:rust`, `q:<question>`, `arch:<problem>`,
`prim:<id>`, `quiz:<track>`, `interview`.

MCP: one tool, `physis.interview`, with `verb` ∈ {q, arch, quiz, prim, related,
cheat, interview}.

## Retrieval pipeline

1. **normalize** — lowercase, punctuation to spaces, tiny stopword list. The same
   normalized string is the cache key, so wording differences collapse before
   anything else happens.
2. **exact leg** — id, alias, or a `questions:` entry listed on a primitive.
3. **lexical leg** — BM25 (`physis_projection::Bm25Projection`, the same scorer
   `physis search` uses) over *concept text only*: title, aliases, tags,
   questions, invariant, usage boundaries, failure modes. Commands, examples and
   sources are excluded — ranking on deep material drags pages into context.
4. **fusion** — `physis_search::fuse_rrf` (the same RRF the context compiler
   uses), constant k = 60.
5. **related expansion** — depth-1 neighbours of the top hits, decayed 0.35.
6. **recipe expansion** — a matched recipe contributes its composition, decayed
   0.55, but only when the question really lands on it (two overlapping concept
   tokens, or an exact alias match);
7. **semantic leg (optional, `--features llm` + `--llm`)** — a third RRF leg from
   the workspace embedder stack. Off by default because it costs a model round
   trip; every hit reports which legs ranked it.

Every hit carries `why` (`alias:rollout`, `question`, `bm25`,
`related-of:k8s.deployment`, `compose-of:recipe.zero-downtime-deploy`, `cache`).
Reasons are data, so a composed answer can show why each primitive is present
instead of asserting it. `:arch` goes further and prints each composed
primitive's *invariant* as its reason to exist.

## Cache

`normalized question → primitive ids (+ their content hashes)`, stored through
`physis_search::SemanticCache` with the corpus fingerprint as a declared
dependency and `physis_projection::HashEmbed` as the lookup embedder — lexical,
labelled as such, and dependency-validated. Composition itself is never cached:
it is cheap string assembly, and caching generated answer prose is exactly what
this design avoids. (The *semantic* leg has its own, different cache: the
embedder stack memoises vectors on disk by content hash.)

- unchanged corpus → `cache hit`
- any primitive edited → `cache invalidated (corpus)`, then recomputed
- `memo_stale_ids` names *which* primitives moved, so unchanged content is
  provably unchanged instead of re-rendered or re-embedded

## Grading: lexical floor, optional model layer

The deterministic grader is a **lexical coverage check over the concepts the
item declares** (`expects`) plus the misuses it declares (`misuse`): "did you
mention this concept", "did you walk into this declared mistake". It cannot
judge whether a sentence is true, and every rendered result says so
(`coverage … · lexical check over declared concepts, not a semantic judgement`).

With `--features llm` and a resolved provider, `--llm` adds a model that fills in
**the same declared rubric** — it does not get to invent a rubric:

- the prompt contains the question, the declared concepts, the declared misuses
  and the answer — no corpus text, so the rating is about the answer;
- the reply is parsed defensively (first balanced JSON object, fences and prose
  tolerated) and every label is matched against the declared sets;
- labels outside the rubric are reported in `ignored` and never merged;
- `missing` and `coverage` are recomputed locally from the declared set, so a
  model cannot widen or shrink what it is graded against;
- the output always names who judged it: `graded by lexical` or
  `graded by llm:ollama:gemma4:e2b`, plus the model's notes;
- a failed call (unreachable provider, bad JSON, timeout) leaves the lexical
  verdict in place and records the reason (`llm unavailable, graded lexically:
  …`). Degradation is stated, never silent.

`PRIMITIVES TO REVIEW` stays deterministic: it comes from curated vocabulary
(id, title, aliases, tags) and the item's authored `related` set.

## Model providers (feature `llm`)

Default-off, like every model backend in this workspace: a checkout builds and
runs with no socket. Enable per surface with `--features llm`
(`physis-cli`, `physis-hud`, `physis-mcp`, or the crate itself).

| Env | Meaning |
|---|---|
| `PHYSIS_LLM=off` | disable explicitly, even when a provider is reachable |
| `PHYSIS_OLLAMA_URL` | ollama base URL (default `http://127.0.0.1:11434`) |
| `PHYSIS_LLM_MODEL` | chat model; when unset the first chat model in `/api/tags` is used, preferring small instruct families (`gemma`, `llama`, `phi`, …; embedding models are skipped) |
| `PHYSIS_LLM_URL` + `PHYSIS_LLM_KEY` | OpenAI-compatible endpoint and key |
| `PHYSIS_OPENAI_URL` + `PHYSIS_OPENAI_KEY` | same, shared with the embedder stack |
| `PHYSIS_LLM_TIMEOUT_SECS` | per-call budget (default 30s — a local model may load) |
| `PHYSIS_LLM_LIVE=1` | opt in to the live model tests (they are skipped by default) |

Two things the LLM is used for, and nothing else:

1. **Semantic retrieval leg** — `select_with_cache` (the same embedder stack
   `physis search` uses, disk-memoised under `.physis-next/embed-cache`) embeds
   the query and the primitive concept texts; the cosine ranking joins exact and
   BM25 as a third RRF leg. Every hit says which legs ranked it
   (`bm25, semantic`). The first call embeds the corpus concept texts once
   (memoised on disk by the embedder stack, so the cost is paid per changed
   document, not per query); warm calls are a disk-cache lookup.
2. **Semantic grading**, as described above.

The model never writes the answer: composition stays primitive-based, so a
`:q --llm` answer is still three cheap primitives with citations rather than one
generated paragraph.

## Sources

`sources:` holds the authoritative reference for each primitive (official
Kubernetes docs, `doc.rust-lang.org`, Tokio `docs.rs`, Axum/Tower docs) and is
rendered only at deep depth. Nothing here claims behaviour those sources do not
document; where a claim is operational practice rather than documentation
(backoff with jitter, pool sizing, queue bounds), the source is the practice
reference (AWS Builders' Library, Google SRE book).

## Adding a primitive

1. Pick the directory by kind; the file name is free, the `id` is the contract.
2. Write the invariant first — if you cannot state one line that must stay true,
   the concept is not atomic yet.
3. Add `related:` edges. An unreferenced primitive fails the invariant suite, and
   that is intentional: isolated knowledge is knowledge nobody will retrieve.
4. Cite a source. If you cannot, mark the claim as practice, not documentation.
5. Run `cargo test -p physis-tests --test invariants interview` and
   `physis interview`. The corpus fingerprint changes, and dependent cache
   entries invalidate on the next query — by design, not by accident.
