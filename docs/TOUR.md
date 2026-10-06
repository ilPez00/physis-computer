# The tour — twenty panes, in reading order

Every key below is wired and reachable. Where a pane has a caveat, the caveat
is stated rather than left for you to discover.

## Start here

| Key | What it does |
|---|---|
| `1` … `0`, `Tab` | Switch panes. Focus never changes when you do. |
| `l` | Cycle the **lens** over the same focused object — graph, relations, deps, history, context. The object stays; only the view of it moves. |
| `b` | Walk back, one focus at a time. |
| type anything | Searches, and focuses the top hit. |
| `/CALLS lang:ts` | Filter edges by verb, language, or crate. `crate:` and `lang:` combine with AND; `/` alone clears. |
| `/agent opencode <task>` | Preview the exact bounded packet a delegate would receive. Enter again to launch it. |
| `:help` | The full verb list. |

## The panes worth your time

### Cognition (19) — why this exists

`:cog <line>` interprets the line into a primitive program and shows the
execution trace: goal, interpretation, steps, evidence, candidates **with
scores**, backend, escalation, selected value, latency, cost.

`r` reruns and diffs the selected value old→new. The point is that you can see
the machine change its mind and be told why, rather than being handed a
sentence.

Every decision is a selection over bounded candidates with real numbers. When
nothing clears the threshold it abstains and says so. An 11.7× performance
claim was withdrawn from this project's marketing because the harness
producing it was measuring an unlicensed binary; the trace is where you can
check for yourself instead of trusting a number.

### Notebook (15) — thought attached to the graph

Cells reference world objects (`[[entity:…]]`). `n` pins the focused object, `a`
asks a bounded question over the packed cells, and the answer cites what it
used. `.physis-next/notebooks/`, plain JSON.

No reorder UI, no multiple notebooks yet. The read and ask paths work.

### Editor (17) — `:edit`

Opens a file. Enter stages a diff; the second Enter writes through the
canonical write path — the same one the CLI and the MCP server use, so the
change re-observes and the graph updates with focus preserved. Stale writes are
refused rather than clobbering a concurrent edit. `u` undoes.

File-granular: editing is per-file, not per-symbol.

### Interview (18) — 145 primitives

| Verb | Effect |
|---|---|
| `:q <question>` | Composes an answer from primitives, each line citing its id |
| `:arch <design>` | Composes an architecture answer from recipes plus primitives |
| `:quiz <track>` | Asks, then grades your answer against the concepts it declares |
| `:prim <id>` | One primitive at a chosen depth |
| `:related <id>` | Walk the concept graph |
| `:cheat --track rust` | One line per primitive |
| `:explain <id>` | Deep material — examples, failure modes, misuse signatures |

Kubernetes, Rust, and system design. This is the pane that works in a directory
with no code in it, because the corpus ships with the binary.

### Graph (0) and Relations (8)

The world. `j`/`k` move, Enter focuses the neighbour through the one focus
system. `/filter DEPENDS_ON` narrows by verb; `lang:ts` and `crate:<name>`
narrow by where.

### Scale (16)

`:zoom out|in|crate|file`. A lower-scale view of the same facts, with the
compression receipts that say what was represented and what was dropped.

The certification invariants are tested, but the certified encoding costs
roughly 31% more than the plain lift, so it is not wired into context packets
by default. The pane shows it; the compiler does not depend on it.

### Settings (14)

`e` to edit, Enter to stage, `s` to save and reload the runtime config, `r` to
reload, `d` to revert. Backend switches take effect without restarting.

### Live (9)

Change detection is content-hash gated, so a same-size edit still enters the
world. Deletions emit tombstones and drop the file, its symbols and every edge
touching them. The pane polls a bounded tree fingerprint every 2 s and
re-observes only when it moved — the status line names the refresh.

2 s is coarse by design. There is no inotify and no per-path debounce.

## Honest limits

- Rust, TypeScript, JavaScript and Python parse structurally. Other languages
  are observed as files without symbol structure.
- Method dispatch, instance calls and calls through imported packages are
  **withheld**, not guessed.
- The default embedder is lexical and labels itself `semantic: false` on every
  compile.
- Symbol-level editing is not implemented; the editor is file-granular.
- Token figures are heuristic units — a retrieval measurement, not provider
  token accounting or an API bill.