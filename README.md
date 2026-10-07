# physis-computer

**[CI badge](https://github.com/ilPez00/physis-computer/actions) · Linux x86_64 · version 1.2.0 · Apache-2.0 corpus**

> **No account. No network. No model. It still decides — and abstains rather than guess.**

Free as in free beer: the binaries are gratis, and the
valuable engine lives in [physis-next](https://github.com/ilPez00/physis-next).
This repo exists so you can run the receipts before
you buy the engine — that is the whole funnel. Every
decision below was made by a deterministic program
with **zero learned parameters**, in sub-0.1 ms, with
no account, no network and no model. The network part
is checkable after install —
`strace -f -e trace=network physis q "how do I build a queue" 2>&1 | grep -c connect`
prints `0`:

`physis q` answers from the 157-primitive
knowledge base that ships with the release —
installed beside the binary, found by a
fixed-prefix fallback, so it works in any
directory. Every line cites its primitive:

```bash
cd /tmp/empty
physis q "how do I deploy without downtime"
```

```text
QUESTION how do I deploy without downtime
  cache miss · corpus cd6d0070 · depth 30s
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
  design.graceful-shutdown — Stop accepting, finish in-flight work (idempotent or requeueable) within a deadline, then exit -- with clients retrying in the window where the endpoint list and the process disagree. (bm25, compose-of:recipe.zero-downtime-deploy)
  design.health-checking — Separate liveness (should this process be restarted) from readiness (should traffic be sent here), and keep both cheap and dependency-aware in the right direction. (bm25, compose-of:recipe.zero-downtime-deploy)
COMMANDS
  kubectl get deployments -A
  kubectl rollout status deployment/api
  kubectl describe deployment/api
  [398 tokens of 400 budget · truncated]
```

> `tok` in these transcripts is the engine's heuristic content unit — its own budget accounting, not model tokens, not a bill.

No signup, no model download, no telemetry. Two binaries, about 26 MB (measured).

## Shock 1 — zero parameters, on the record

Bench, arm A deterministic (`experiments/cognition/results/system_one_bench.json`, v1.2.0):

| task | n | accuracy | ECE | p50 latency |
|---|---|---|---|---|
| intent classification | 20 | **20/20** | 0.000 | 0.0 ms |
| tool routing | 15 | **14/15** | 0.000 | 0.009 ms |
| command selection | 108 | **107/108** | 0.058 | 0.056 ms |

- The single tool-routing miss **escalated** (escalation
  rate 1/15) — the machine said "I don't know" instead
  of guessing; the design, not a bug.
- The neural arms (embed `bge-small-en-v1.5`, causal `smollm2-135m`,
  `ollama` LLM) are **skipped** — weights absent on this host, the
  LLM leg opt-in. Skipped ≠ tied: not run, no evidence either way.

## Shock 2 — abstention is the default

`physis computer .` on a stranger's repo — 46 files, never observed:

```text
1. THE WORLD
   46 files, 16 dirs → 75 entities, 12 relations

2. THE BUSIEST SYMBOLS HERE
   …

3. A DECISION, AND WHY IT DID NOT MAKE ONE
   CANDIDATES
     read the graph — p=0.000
     compile a context packet — p=0.000
     edit a file — p=0.000
   SELECTED
     (none)
   CONFIDENCE
     0.000
   ESCALATED
     true
   ↳ no outcome history for any option, so it escalated instead of guessing.
     a machine that answers anyway is the thing this one refuses to be.

4. WHAT AN AGENT WOULD RECEIVE
   task: "what is this codebase and where do I start" ·
   31 objects · 677/800 tok · 0 omitted · strategies bm25+graph ·
   embedder random-projection (semantic: false)

5. NEXT
   …

   offline · no account · nothing sent anywhere
```

Every candidate sits at p=0.000 because there is no outcome history
for any option — the default for a stranger's first question.
**The honest gap is the report.**

## The 30-second tour

There is no splash screen. `physis demo` extracts a 14-file fixture
to a temp dir, puts it under git, and runs the engine's real loop:
observe → ask → plan → act → re-observe → verify → remember.
Revision hashes are fresh per run; counts are stable:

```text
physis demo — change the world, deterministically

stage 1 — OBSERVE
   84 entities, 117 relations
   revision: cc8d0e9

stage 2 — ASK
   goal: "change timeout handling without breaking callers"
   focus: symbol:src/client.rs::request

stage 3 — PLAN FROM THE WORLD
   callers: 4 (send_a, send_b, send_c — CALLS …::request)
   tests: 3 (request_test_a/b/c — CALLS …::request)
   depends on: symbol:src/client.rs::retry, symbol:src/client.rs::timeout, symbol:src/client.rs::metrics, symbol:src/client.rs::log
   context packet: 313/800 tok · random-projection · semantic: false

stage 4 — ACT (canonical write path)
   edit src/client.rs: rename timeout → deadline
   wrote file:src/client.rs (1081 bytes) → +15 observations, revision f019077
   added symbols: ["deadline"]
   removed symbols: ["timeout"]

stage 5 — RE-OBSERVE
   revision: f019077
   +1 file:src/client.rs --DEFINES--> symbol:src/client.rs::deadline
   +1 symbol:src/client.rs::request --CALLS--> symbol:src/client.rs::deadline
   -1 file:src/client.rs --DEFINES--> symbol:src/client.rs::timeout
   -1 symbol:src/client.rs::request --CALLS--> symbol:src/client.rs::timeout

stage 6 — VERIFY
   [PASS] request CALLS deadline (change applied)
   [PASS] request CALLS retry (behavior preserved)
   [PASS] request CALLS metrics (behavior preserved)
   [PASS] request CALLS log (behavior preserved)
   [PASS] request no longer CALLS timeout (old path removed)
   [PASS] send_a still CALLS request (public API unchanged)
   [PASS] request_test_a still CALLS request (tests still cover target)
   constraint: PASS · blast radius: NONE · tests: PASS

stage 7 — MEMORY
   remembered in revision f019077
     203 world write|src/client.rs bytes:1081
     218 memory memory:demo.f019077 text=physis demo · outcome=renamed timeout→deadline in src/client.rs; constraint=PASS

   world left at /tmp/physis-demo-4067249
```

Two things survive scrutiny. First, the engine acts on a
world and checks its own work — structurally, not in prose
(callers, tests and the old path verified by edge;
`semantic: false` in stage 3 is the honest lexical-embedder
label).

> **Recording:** `asciinema rec demo.cast`, then
> `physis-hud` and `:cog change timeout handling`.

## `physis solve` — the verification ladder

`physis solve` states a desired world as a constraint, surveys the
affected world, opens an **isolated worktree** (the sandbox: cwd
pinned there, never in your checkout), executes a caller-supplied
act, verifies with bounded checks, and reconciles the delta into an
append-only constraint log (`.physis-next/constraints.jsonl`).

The acceptance checks are a **ladder**. `--check` is repeatable and
carries a rung — `level:name:command`, `name:command` (level
defaults to `tests`), or a bare command. Levels, in order: syntax →
static → types → lint → tests → targeted → property → invariant →
model → formal. Three rules, all fail-closed:

- **The ladder stops at the first failing rung.** A check
  that cannot pass tells the next rung nothing, and an
  unreached rung is never evidence.
- **A timeout is `unverifiable`, never a pass.**
- **`success` requires every declared check to have run
  and passed** — a stopped ladder cannot read as success.

Unknown levels are rejected at parse time — a typo cannot silently
downgrade the evidence. With `--editor <cmd>`, every attempt runs the
**whole ladder**, the re-plan prompt carries each failing check's
bounded stderr/stdout tail, and the report and JSON output carry a
**delta score**: the final attempt's changed surface — added +
removed lines, headers excluded. Lower is more minimal.

Two true stories:

1. **The ladder caught a real defect no prose
   review had.** The first end-to-end run failed
   the `static` rung (`cargo fmt --all -- --check`
   in the task worktree): a staged edit had
   shipped unformatted in HEAD (`5e93e9a`). A
   failed rung is a failed verdict, never a
   silent skip.
2. **The loop's own regression test merged to
   main** as `73f76fb` (`test(query): regression
   tests for the root-tag stripper`), machinery
   at `ec5bc9f`.

End-to-end receipt, on physis-next itself, scripted
editor (no model) — ladder `static:fmt:cargo fmt
--all -- --check` + `types:check:cargo check
-p physis-task` (`docs/HANDOFF_2026-10-06.md`):

```text
attempt 1: editor completed apply completed checks [fmt[static]:passed check[types]:passed] (+5 -0)
checks:
  fmt -> passed (completed [static] in 576 ms — …)
  check -> passed (completed [types] in 7630 ms — …)
verdict: success
delta: 121 subject(s)
delta score: 5 (+5 -0)
constraint log: seq 28
```

## We withdrew our own number

An earlier release claimed an **11.7×** performance figure. It was
retracted: the harness producing it was measuring an **unlicensed
binary**, so the number never described this product (receipts
`2d710ff`, `43a28d9`; `docs/commercial/MARKET.md`).

The retraction is the feature: no number
to trust, only a trace you can run
yourself — every decision prints its
candidates, scores, backend and escalation.

## The TUI

20 panes over one world — run `physis-hud` (`--path <dir>`
targets another; default `.`). The interesting ones:

- **Cognition** — `:cog <line>` shows the decision
  trace — candidates, scores, backend, escalation,
  verdict, never generated prose; `r` reruns and
  diffs the selected value.
- **Notebook** — cells that reference real objects in
  the graph. Pin the focused object, ask a bounded
  question, get citations back.
- **Editor** — `:edit` opens a file, Enter stages a
  diff, the second Enter writes through the canonical
  path everything else uses. Stale writes refused.
- **Interview** — 157 knowledge primitives (Kubernetes,
  Rust, system design): `:q` asks, `:arch` designs,
  `:quiz` grades, `:cheat` prints the cheat sheet.
- **Graph / Relations / Scale / Diff** — the world,
  navigable. `l` cycles the lens over the same focused
  object; `b` walks back.
- **Settings** and **Live** — backend switches without
  a restart; change detection is content-hash gated,
  polling a bounded tree fingerprint every 2 s.

`physis-hud --snapshot --view <overview|graph|cognition>`
renders one text frame and exits — for CI, or to confirm
the binaries are intact. `--setup` prints the honest gap
report (intelligence, embedder, escalation policy).

## It reads any corpus

Rust, TypeScript, JavaScript and Python are parsed for structure
(Rust by a line-level scanner — definitions, imports, bare calls;
TypeScript and JavaScript share the tree-sitter TypeScript grammar;
Python uses tree-sitter). Go joins through the doc-comment
primitives (`--doc-comments`): `.go` files index package, import,
const, type, var and function definitions, and `doc:`/`text:`
entities are opt-in. `physis roots ~/src/api ~/src/web` prints two
directories as one namespaced world (ids prefixed `r0:`/`r1:`,
nothing collides, nothing written to disk), and `physis observe
~/src/api` persists one of them into `.physis-next/`.

Caller resolution is measured, not asserted: on the
frozen benchmark corpus, cross-file caller recall went
**0.278 → 1.000** at precision 1.000 (F1 0.435 →
1.000, invented edges 0). The licensed whole-repo
figure — 0.132, N=32, uncapped grep — has **not**
been re-run and still stands as the last whole-repo
measurement; different scope, stated as such
(`docs/RETROSPECTIVE_2026-10-07.md`).

## Knowledge without code

157 primitives ship with the release (installed
beside the binary), so this works in an empty
directory — no checkout, no setup:
`physis quiz kubernetes`, `physis q "how do I
build a queue"`.

`physis cheat --track rust` covers 44 rust
primitives, budget-bounded — the default
900-token budget prints 28 and says so:
`[28/44 lines · 897 tokens of 900 budget ·
truncated]`. A bigger budget prints the rest.

## Install

```bash
# 1. verify the release archive — every file, aborts on any mismatch
tar -xzf physis-1.2.0-linux-x86_64.tar.gz
cd physis-1.2.0-linux-x86_64
sha256sum -c SHA256SUMS.txt
./install.sh                        # → ~/.local/bin (or: ./install.sh /usr/local/bin)

./install.sh --dry-run              # repo clone: where it writes, what it backs up — no network
./install.sh

strace -f -e trace=network physis q "how do I build a queue" 2>&1 | grep -c connect   # 0 — proves it talks to nothing
```

Each prior executable is retained as `~/.local/bin/physis.backup-<sha256>`,
so a bad install is reversible without a reinstall. `install.sh` is
offline: it verifies the bundled checksums, then copies two binaries
and the corpus — no network call. Checksums and signatures for every
release are attached to the
[GitHub Release](https://github.com/ilPez00/physis-computer/releases/tag/v1.2.0).

## What is free, and what is paid

| | physis-computer (this) | Physis Context MCP |
|---|---|---|
| Price | free | €49 one-time founding (first 25 licences), €79 after |
| For | you, reading and editing | your **agent**, in your editor |
| The tools | you type them, see every receipt | it calls them automatically |
| Surface | the full `physis serve` catalogue: 62 tool definitions — 60 distinct advertised on `tools/list` + 2 deprecated aliases dropped from the wire list but still callable | 12 licensed, read-only tools for coding agents |
| Caller recall | honest about gaps: method dispatch, instance calls, imported-package calls and Rust macros are withheld rather than guessed | improved — not claimed here without a number; see the licensed build |
| Support | community | licensed support |

The binaries here link more of the engine than the paid product does — the free tool is for a human at a terminal, the paid one is for an agent inside an editor. Same code path, different caller.

Want the full engine source and the licensed cross-platform MCP server that calls these tools automatically from your editor? See [Physis Context MCP](https://github.com/ilPez00/physis-context-mcp) and [physis-next](https://github.com/ilPez00/physis-next).

## What this does not do

Stated plainly, because a tool that hides its edges is not worth trusting:

- **Linux x86_64 only.** No macOS, no ARM, no Windows build.
- **The offline embedder is lexical, not semantic** — it
  reports `semantic: false` on every compile; a semantic
  leg exists behind a feature flag and is off by default.
- **Caller resolution is conservative.** Method
  dispatch, instance calls, imported-package calls
  and Rust macros are withheld, not guessed — a
  wrong edge is worse than a missing one. Zero
  callers never proves safety; it proves only
  that no edge cleared the bar.
- **No token-savings claim.** Earlier figures measured unlicensed
  binaries and were withdrawn; retrieval figures above are per-query
  measurements, not session-wide savings, and `tok` is a heuristic
  content unit, not model tokens, not a bill.
- **No model ships in this binary** — `physis q`/interview
  run on the primitive corpus; the language surface is
  optional and off by default.

## License

- The interview corpus (`corpus/*.prim`) and documentation are
  licensed **Apache-2.0**.
- The `physis` and `physis-hud` binaries are redistributable with
  this package only, as-is, no reverse engineering — not
  source-available; the engine source is the commercial product.

## Changes

See [`docs/CHANGELOG.md`](docs/CHANGELOG.md).
