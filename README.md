# physis-computer

**[CI badge](https://github.com/ilPez00/physis-computer/actions) · Linux x86_64 · Apache-2.0 corpus**

> See exactly what your agent would be handed for this task, and why it refused
> when it did. Run `physis q "…"` in any folder — no account, no network, no
> model.

`physis q` answers from the 145-primitive knowledge base that ships inside the
binary. Every line cites the primitive it came from. Try it in an empty directory:

```bash
cd /tmp/empty
physis q "how do I deploy without downtime"
```

```text
QUESTION how do I deploy without downtime
  cache miss · corpus 3928d9e4 · depth 30s
DIRECT ANSWER
  Declare replicas and a Pod template; the Deployment controller keeps exactly
  that many Pods running and moves between template versions by creating
  ReplicaSets. [k8s.deployment]
  Run two ReplicaSets at once: the new one grows as the old one shrinks, bounded
  by maxSurge and maxUnavailable, and only Pods that pass readiness join the
  Service. [k8s.deployment.rolling-update]
  Use expand/contract: add the new column or table, deploy code that writes both
  and reads either, backfill, switch reads, then remove the old shape in a later
  deploy. [design.schema-migration]
PRIMITIVES
  k8s.deployment — The replica count is declared; the Deployment controller converges Pods to it via ReplicaSets. (bm25)
  k8s.deployment.rolling-update — Maintain enough healthy replicas while replacing the old ReplicaSet. (bm25, compose-of:recipe.zero-downtime-deploy)
  design.schema-migration — Every schema change must be compatible with both the old and the new version of the application code while both are running. (bm25, compose-of:recipe.zero-downtime-deploy)
  …
COMMANDS
  kubectl get deployments -A
  kubectl rollout status deployment/api
  kubectl describe deployment/api
  [398 tokens of 400 budget · truncated]
```

That is the whole setup. No signup, no network, no model download, no telemetry.
Two binaries, about 25 MB.

---

## The 30-second tour

There is no splash screen. `physis demo` extracts a 14-file fixture to a temp
dir, puts it under git, and runs the engine's real loop on it: observe → ask →
plan → act → re-observe → verify → remember. Every number below is reproducible
by a reviewer running the same command — revision hashes are fresh per run, the
entity/relation counts are stable:

```text
physis demo — change the world, deterministically

stage 1 — OBSERVE
   83 entities, 96 relations
   revision: rA

stage 2 — ASK
   goal: "change timeout handling without breaking callers"
   focus: symbol:src/client.rs::request

stage 3 — PLAN FROM THE WORLD
   callers: 3 (send_a, send_b, send_c — CALLS …::request)
   tests: 3 (request_test_a/b/c — CALLS …::request)
   depends on: log, metrics, retry, timeout   (4 outgoing CALLS)
   constraint: public API unchanged
   context packet: 243/800 tok · random-projection (semantic: false)

stage 4 — ACT (canonical write path)
   edit src/client.rs: rename timeout → deadline
   wrote file:src/client.rs (1081 bytes) → +11 observations, revision rB
   added symbols: ["deadline"]   removed symbols: ["timeout"]

stage 5 — RE-OBSERVE
   revision: rB
   +1 file:src/client.rs --DEFINES--> symbol:src/client.rs::deadline
   +1 symbol:src/client.rs::request --CALLS--> symbol:src/client.rs::deadline
   -1 file:src/client.rs --DEFINES--> symbol:src/client.rs::timeout
   -1 symbol:src/client.rs::request --CALLS--> symbol:src/client.rs::timeout

stage 6 — VERIFY
   [PASS] request CALLS deadline (change applied)
   [PASS] request CALLS retry / metrics / log (behavior preserved)
   [PASS] request no longer CALLS timeout (old path removed)
   [PASS] send_a / send_b / send_c still CALLS request (public API unchanged)
   [PASS] request_test_a/b/c still CALLS request (tests still cover target)
   constraint: PASS · blast radius: NONE · tests: PASS

stage 7 — MEMORY
   remembered in revision rB
     N world write|src/client.rs bytes:1081
     N+1 memory:demo.rB outcome=renamed timeout→deadline, constraint=PASS

   world left at /tmp/physis-demo-PID
```

Two things survive scrutiny, in order. First: the engine reports an honest gap
and **abstains** when it has no basis to act — the default for a stranger's
first question. Run `physis computer .` on any repository for that default tour
(world, busiest symbols, decision trace, the bounded packet an agent would
receive). Second: it can change a world and check its own work, and it does both
on the record.

That abstention is the first half of the contract; the demo above is the
second — the engine acting on a world and checking its own work. Note `semantic: false`
in stage 3 and the conservative caller count: a wrong edge is worse than a
missing one, so you get fewer and an honest count. A semantic embedder and a
live model leg exist, feature-gated and off by default in this binary.

The same cognition trace is one `:cog` away in the TUI. On a first run it shows
the honest abstention (0.000 confidence, no-action) that `physis computer`
prints; once an option carries outcome history, `r` reruns and diffs the
selected value so you can see the machine change its mind and be told why.

> **Recording:** `asciinema rec demo.cast`, then `physis-hud .` and
> `:cog change timeout handling`. One GIF of the trace — here, an abstention —
> is worth this paragraph.

Point `physis computer .` at your own checkout to run the same tour there:

```text
physis-computer — first run
   1. THE WORLD
   2. THE BUSIEST SYMBOLS HERE
   3. A DECISION, AND WHY IT DID NOT MAKE ONE
   4. WHAT AN AGENT WOULD RECEIVE
   5. NEXT
```


---

## The TUI

```bash
physis-hud .
```

Twenty panes over one world. The interesting ones:

- **Cognition** — `:cog <line>` shows the decision trace live; `r` reruns and
  diffs the selected value. Never generated prose — candidates, scores, backend,
  escalation, verdict.
- **Notebook** — cells that reference real objects in the graph. Pin the focused
  object, ask a bounded question, get citations back.
- **Editor** — `:edit` opens a file, Enter stages a diff, the second Enter
  writes through the canonical path everything else uses. Stale writes refused.
- **Interview** — 145 knowledge primitives on Kubernetes, Rust and system design,
  with `:q` to ask, `:arch` to design, `:quiz` to be graded.
- **Graph / Relations / Scale / Diff** — the world, navigable. `l` cycles the lens
  over the same focused object; `b` walks back.

`physis-hud --snapshot --view <overview|graph|cognition>` renders one text frame
and exits — for CI, or to confirm the binaries are intact.
`physis-hud --setup` prints the honest gap report (intelligence, embedder,
escalation policy).

---

## It reads any corpus

Rust, TypeScript, JavaScript and Python are parsed for structure. Rust is
resolved by a line-level scanner (definitions, imports, bare calls);
TypeScript and JavaScript share the tree-sitter TypeScript grammar, and Python
uses tree-sitter. Point it at a checkout and it produces a world in one pass:

```bash
physis roots ~/src/api ~/src/web     # two directories, one namespaced world
physis observe ~/src/api             # persist one of them into .physis-next/
```

`roots` prints what it found across several directories, with ids namespaced
`r0:`/`r1:` so nothing collides. Nothing is written to disk.

---

## Knowledge without code

145 primitives ship inside the binary, so this works in an empty directory —
no checkout, no setup:

```bash
physis quiz kubernetes
physis q "how do I deploy without downtime"
```

---

## Install

```bash
# 1. verify the release (Linux x86_64)
tar -xzf physis-1.1.1-linux-x86_64.tar.gz
cd physis-1.1.1-linux-x86_64
sha256sum -c SHA256SUMS.txt            # outer checksums — aborts on any mismatch

# 2. install into ~/.local/bin (or: ./install.sh /usr/local/bin)
./install.sh --dry-run                  # prints where it writes, what it backs up, no network
./install.sh

# 3. prove it talks to nothing
strace -f -e trace=network physis q "how do I build a queue" 2>&1 | grep -c connect
# 0
```

Each prior executable is retained as `~/.local/bin/physis.backup-<sha256>` rather
than replaced, so a bad install is reversible without a reinstall. `install.sh`
is offline: it copies two binaries and the corpus; it makes no network call.

Checksums and signatures for every release are attached to the
[GitHub Release](https://github.com/ilPez00/physis-computer/releases/tag/v1.1.1)
alongside the archives.

---

## The interview primitive library (worked example)

The same machinery runs over a technical corpus instead of a codebase: knowledge
compiled into atomic primitives that are retrieved, ranked, cached and **composed**
— Kubernetes, Rust and architecture answers plus a `:quiz` loop.

```bash
physis arch "design a service receiving 50k events per minute and processing them asynchronously"
```

```text
ARCHITECTURE design a service receiving 50k events per minute and processing them asynchronously
  recipe recipe.async-job-processing · corpus 3928d9e4 · depth 30s
FLOW
  Ingress / API (validate + enqueue, fast)
     |  durable queue (bounded depth, backpressure at the edge)
     |  worker deployment (N consumers, bounded concurrency)
     |  database (idempotent writes keyed by job id)
     |  metrics: queue depth, in-flight, per-item latency
WHY EACH PIECE EXISTS
  design.producer-consumer — a queue decouples producer and consumer rates.
  design.bounded-queue — finite capacity + an overflow policy bounds latency.
  design.backpressure — push back / drop / buffer when producers outrun consumers.
  design.worker-pool — fixed consumers on one shared queue → chosen concurrency.
  design.idempotency — same effect once or many times makes retries safe.
  …
  [602 tokens of 600 budget · truncated]
```

`physis q "<question>"` composes DIRECT ANSWER / PRIMITIVES / COMMANDS /
FAILURE MODES / FOLLOW-UPS from the primitives it retrieved, each line citing its
source id; `physis quiz kubernetes` asks and grades against the concepts the item
declares; `physis cheat --track rust` prints one line per primitive (`rust.*` —
39 lines on this corpus). In the HUD the interview primitive library is
tab 18 (`:q`, `:arch`, `:quiz`, `:prim`, `:related`, `:explain`, `:cheat`,
`:interview`). Corpus, schema and design rationale: [`docs/TOUR.md`](docs/TOUR.md).

---

## What this does not do

Stated plainly, because a tool that hides its edges is not worth trusting:

- **Linux x86_64 only.** No macOS, no ARM, no Windows build.
- **The offline embedder is lexical, not semantic.** It reports
  `semantic: false` on every compile. A semantic leg exists behind a feature flag
  and is off by default.
- **Caller resolution is conservative.** Method dispatch, instance calls and
  calls through an imported package are withheld rather than guessed — a wrong
  caller is worse than a missing one, so you get fewer edges and an honest count.
- **No token-savings claim.** Earlier figures measured unlicensed binaries and
  were withdrawn. The retrieval reduction you see per compile is a measured
  figure for that query, not a session-wide saving.
- **No model ships in this binary.** `physis-q`/interview run on the primitive
  corpus; the language surface is optional and off by default.

---

## What is free, and what is paid

| | physis-computer (this) | Physis Context MCP |
|---|---|---|
| Price | free | €79 one-time, €50 for the first 50 |
| For | you, reading and editing | your **agent**, in your editor |
| The tools | you type them, see every receipt | it calls them automatically |
| Surface | 62 MCP tools over the local runtime (read/write/inspection, cognition, memory, interview, ops + workspace — the `physis serve` catalogue; 2 are deprecated aliases retained for compatibility) | 12 licensed, read-only tools for coding agents |
| Caller recall | honest about gaps: method dispatch, instance calls and imported-package calls are withheld rather than guessed | improved — not claimed here without a number; see the licensed build |
| Support | community | licensed support |

The binaries here link more of the engine than the paid product does — the free
tool is for a human at a terminal, the paid one is for an agent inside an editor.
Same code path, different caller.

Want the full engine source and the licensed cross-platform MCP server that
calls these tools automatically from your editor? See
[Physis Context MCP](https://github.com/ilPez00/physis-context-mcp) and
[physis-next](https://github.com/ilPez00/physis-next).

---

## License

- The interview corpus (`corpus/*.prim`) and documentation are licensed
  **Apache-2.0**.
- The `physis` and `physis-hud` binaries are redistributable with this package
  only, as-is, with no reverse engineering. They are not source-available; the
  engine source is the commercial product.

## Changes

See [`docs/CHANGELOG.md`](docs/CHANGELOG.md).
