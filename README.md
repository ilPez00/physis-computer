# physis-computer

**A terminal that builds a typed world out of your code, then shows you how it
decides.** Free, offline, no account. Linux x86_64.

Most tools tell you what they think. This one shows you the candidates, the
scores, the backend, and the exact bounded packet it would hand to an agent —
including the cases where it refuses to answer at all.

```bash
tar -xzf physis-<version>-linux-x86_64.tar.gz
cd physis-<version>-linux-x86_64
./install.sh
cd ~/your-project
physis computer
```

That is the whole setup. No account, no network, no model download, no
telemetry. Two binaries, about 25 MB.

---

## The 30-second tour

`physis computer` is not a splash screen. It runs the real engine on your
directory and prints what came back. On this repository:

```text
physis-computer — first run

1. THE WORLD
   1409 files, 219 dirs → 6436 entities, 11885 relations

2. THE BUSIEST SYMBOLS HERE
   114 edges  symbol:super::*
    73 edges  symbol:json
    65 edges  symbol:crates/physis-mcp/src/tests.rs::test
    59 edges  symbol:crates/physis-mcp/src/tests.rs::server

3. A DECISION, AND WHY IT DID NOT MAKE ONE
   CANDIDATES
     read the graph — p=0.000
     compile a context packet — p=0.000
     edit a file — p=0.000
   SELECTED
     (none)
   BACKEND
     deterministic:transitions
   CONFIDENCE
     0.000
   ESCALATED
     true
   ↳ no outcome history for any option, so it escalated instead of guessing.
     a machine that answers anyway is the thing this one refuses to be.

4. WHAT AN AGENT WOULD RECEIVE
   task: "what is this codebase and where do I start"
   19 objects · 787/800 tok · 21 omitted · strategies bm25+graph
   embedder random-projection (semantic: false)
     [file] file:corpus/k8s/resources-requests.prim — rank 0 (fused 0.033)
     [file] file:tasks/handoffs/LEDGER-AUDIT/ASSIGNMENT.md — rank 1 (fused 0.016)
```

Read section 3 again. It had enough to answer and **did not**, because no option
had cleared the confidence threshold, and it says so on the record. Most tools
hide that. This one leads with it.

Note `semantic: false` in section 4. That is a lexical hasher telling you it is
not a language model, because it is not one. Nothing here claims to be
something it is not.

## The TUI

```bash
physis-hud .
```

20 panes over one world. The interesting ones:

- **Cognition** — run `:cog <line>` and watch a decision resolve as an
  execution trace: goal, interpretation, steps, evidence, candidates with
  scores, backend, escalation, selected, latency, cost. Never generated prose.
- **Notebook** — cells that reference real objects in the graph. Pin the
  focused object, ask a bounded question over the cells, get citations back.
- **Editor** — `:edit` opens a file, Enter stages a diff, the second Enter
  writes through the same path everything else uses. Stale writes are refused.
- **Interview** — 145 knowledge primitives on Kubernetes, Rust and system
  design, with `:q` to ask, `:arch` to design, `:quiz` to be graded.
- **Graph / Relations / Diff / Scale** — the world, navigable. `l` cycles the
  lens without ever moving focus.

## It reads any corpus

Rust, TypeScript, JavaScript and Python are parsed structurally. Point it at a
checkout and it produces a world in one pass:

```bash
physis roots ~/src/api ~/src/web     # two directories, one namespaced world
physis observe ~/src/api             # persist one of them
```

`roots` prints what it found across several directories at once, with ids
namespaced `r0:`/`r1:` so nothing collides. Nothing is written to disk.

## Knowledge without code

145 primitives ship inside the binary, so this works in an empty directory —
no checkout, no setup:

```bash
physis quiz kubernetes
physis q "how do I deploy without downtime"
```

Real output, every line citing its source primitive:

```text
DIRECT ANSWER
  Declare replicas and a Pod template; the Deployment controller keeps exactly
  that many Pods running and moves between template versions by creating
  ReplicaSets. [k8s.deployment]
  Run two ReplicaSets at once: the new one grows as the old one shrinks, bounded
  by maxSurge and maxUnavailable, and only Pods that pass readiness join the
  Service. [k8s.deployment.rolling-update]
PRIMITIVES
  k8s.deployment — The replica count is declared; the Deployment controller
  converges Pods to it via ReplicaSets. (bm25)
  k8s.deployment.rolling-update — Maintain enough healthy replicas while
  replacing the old ReplicaSet. (bm25, compose-of:recipe.zero-downtime-deploy)
```

## Be an agent for thirty seconds

`physis mcp` calls **any** tool an agent calls, full parity, from your
terminal:

```bash
physis tools                                            # the catalogue
physis mcp physis.explain --arg question="what depends on corpus_dir"
physis mcp physis.impact --arg id=symbol:src/lib.rs::helper
```

This is the same dispatch function the MCP server uses — one implementation,
three surfaces (CLI, TUI, MCP). So the receipts you see here are the receipts
an agent would get.

## What is free, and what is paid

| | physis-computer (this) | Physis Context MCP |
|---|---|---|
| Price | free | €79 one-time, €50 for the first 50 |
| For | you, reading and editing | your **agent**, in your editor |
| The tools | you type them, see every receipt | it calls them automatically |
| Caller recall | honest about gaps | improved, measured |

The binaries here link more of the engine than the paid product does. That is
not an accident and it is not generosity with someone else's money: the free
tool is for a human at a terminal, the paid one is for an agent inside an
editor. Same code path, different caller.

The paid product also ships cross-crate caller resolution and support. If you
want an agent reading your codebase rather than you reading it, that is the
product. [Physis Context MCP](https://github.com/ilPez00/physis-context-mcp).

## What this does not do

Stated plainly, because a tool that hides its edges is not worth trusting:

- **Linux x86_64 only.** No macOS, no ARM, no Windows build.
- **The offline embedder is lexical, not semantic.** It reports
  `semantic: false` on every compile. A semantic leg exists behind a feature
  flag and is off by default.
- **Caller resolution is conservative.** Method dispatch, instance calls and
  calls through an imported package are withheld rather than guessed. A wrong
  caller is worse than a missing one, so you get fewer edges and an honest
  count — not a confident wrong answer.
- **No token-savings claim.** An earlier 11.7× figure was withdrawn because the
  harness that produced it was measuring an unlicensed binary. The measured
  figure is smaller, applies to specific queries, and is not a session-wide
  saving. We would rather quote nothing than quote that.

## Build it yourself

The engine source is not in this repository. What ships here is two compiled
binaries and 145 data files.

```bash
./install.sh                 # verify, install, keep a backup of any prior build
./install.sh /usr/local/bin  # elsewhere, if you have write access
```

Apache-2.0. See [LICENSE](LICENSE).

## What you can do here

The shipped `physis` binary at v1.1.1 exposes the full first-run surface:

| Verb | What it does |
|---|---|
| `physis computer` | Run the engine on your directory; print the world, the busiest symbols, a decision + why it refused, and the bounded packet an agent would receive. |
| `physis roots <paths…>` | Survey two or more trees into one world with per-root `r0:/r1:` ids; writes nothing to disk. |
| `physis observe <path>` | Persist a tree store (`.physis-next/`) — the on-disk graph behind every other verb. |
| `physis compile "<query>"` | Compile a bounded, receipt-carrying context packet for a query (hard budget, bm25+graph). |
| `physis embed "<text>"` | Tokenize text through the resolved embedder with an honest backend label. |
| `physis deps "<id>"` | Walk the graph: dependents, reverse deps, callers. |
| `physis solve --intent … --target … --constraint … --editor <cmd> --check <cmd>` | Open an isolated git worktree, state the constraint, run the editor (prompt on stdin), extract the diff, apply it, run the check, derive the verdict, and append to `constraints.jsonl`. `--execute <cmd>` is an alternative to `--editor` for a one-shot act. |
| `physis-hud .` | The 20-pane TUI: cognition, notebook, editor, graph, relations, diff, scale, … |
| `physis mcp <tool> --arg k=v` | Call any of 61 MCP tools from the shell (`physis.describe` to list, `physis.search` to resolve a name to its canonical id). |

`physis-hud --snapshot --view <overview\|graph\|cognition>` renders one text frame
and exits — useful for CI or to confirm the binaries are intact.
`physis-hud --setup` prints the honest gap report (intelligence, embedder,
escalation policy).

## How this repository ships

This tree is *staged*, not assembled. `scripts/stage-physis-computer.sh` in the
engine checkout copies an **explicit allowlist** (`README.md`, `LICENSE`,
`install.sh`, `docs/TOUR.md`, the `corpus/` data, and the two release binaries)
into this directory — and then **asserts** nothing else got in. The gate is the
point: a marketing giveaway must not become an IP leak.

```
$ bash scripts/stage-physis-computer.sh /path/physis-computer
[gate] no engine source in the staged tree
  OK: 0 .rs files, no workspace manifest, no research, no commercial package
```

The check is `find` for any `*.rs` / `Cargo.toml` / `Cargo.lock` and a
forbidden-path list that includes `crates/`, `apps/`, `docs/commercial/`,
`.physis`, and `.git`. It exits 1 on a single match. Treat it as tamper-evident,
not tamper-proof: the protection is the allowlist construction, not a filter
applied after the fact.

`BUILD.txt` at the tree root records where the stage ran:

```
staged_from=<engine HEAD sha>
staged_state=clean            # a dirty source tree fails the stage
engine_source=private (not included, by decision)
files=154
```

Run `physis computer` on this tree to confirm the binaries are intact — it
prints real entity/relation counts from the corpus instead of a splash screen.