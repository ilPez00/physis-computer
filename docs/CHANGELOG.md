# Changelog

All notable changes to **physis-computer** (the free, binary-only giveaway) are
documented here. This file is staged into the public repository alongside the
binaries; engine source is not — see the License section.

## [1.8.4] — 2026-10-23

The confirmation loop, the desktop's world lens, and TypeScript that resolves.

### Added
- **Crystallization has a confirmation loop, and it is measured.** A rule
  compiled from a task is only ever compiled from an outcome a check passed;
  activation stays a human decision; after activation the rule is judged by
  what was measured, not by what was claimed. The 10-task experiment in the
  engine repo: 10/10 first pass served by measured experience, 10/10 replays
  served by the compiled rules, 0 escalations. `physis cognition --confirm`
  and the `physis.cognition.confirm` MCP tool expose it; the MCP surface is 78
  tools.
- **The desktop overlay** (`physis-gui --overlay`, X11 first): a borderless,
  always-on-top, semi-transparent shell summoned by Super+Space and dismissed
  by Esc. It paints the world as a lens over the same deterministic
  most-related set the application window uses — positions cached per world
  revision, a radial menu of read-only actions, a keyboard path (Tab, Enter,
  1-4) and honest focus. `--watch` re-observes on an interval and pulses the
  edges a delta touched.
- **A first launch introduces the machine by observing**: an overlay opened on
  an unobserved tree runs the real pipeline and says what it saw, instead of
  showing an empty canvas.
- **TypeScript/TSX imports resolve.** `import { helper } from "./util"` becomes
  an edge to the file it names (extensionless and `index.ts` in Node's order);
  a bare specifier becomes a `package:` entity; per-file import bindings decide
  bare calls; a name that travels through a re-export barrel is a labelled
  MAY_CALL. Frozen benchmark: precision 1.000, recall 1.000, invented edges 0.
- **One version, one command.** `just version <n>` rewrites every artifact that
  carries the release version and then runs the checker, so a bump that misses
  a location fails in the same command.

### Fixed
- A compiled rule could never fire: the engine required replay evidence before
  the first replay, so promotion was unreachable by construction. Activation is
  now the gate and measurement is the demotion.
- The transition cache normalised confidence over every action in the log, so
  ten known actions silently vetoed a confident decision. It normalises over the
  candidates offered for the decision.
- Every TypeScript import created a phantom node (`symbol:./util`) that joined
  with nothing. Unresolved specifiers now produce no entity at all.
- The root README stated 1.2.0 while the workspace shipped 1.8.3; the version
  line is now pinned to the workspace version by a test.
- `physis cognition --confirm` was idempotent only within a one-second window:
  it compared serialized bodies, and `created_at` moves. It compares the rule.

### Not in this release
- No macOS or ARM build; Linux x86_64 (GLIBC <= 2.39) and Windows x86_64.
- The overlay is X11-first. The Wayland layer-shell path is not implemented.
- A real external user has not walked the published path yet; the engine repo
  records a rehearsal (`docs/stranger-01.md`) and the friction it found.

## [1.8.3] — 2026-10-22

The desktop rebuilt, and the two library crates a third party can depend on.

### Added
- The desktop overhaul, in four slices: the sidebar is grouped into
  captioned sections (observe · reason · system) with Settings pinned last;
  the theme gained tokens and a density knob; the graph view became an
  instrument — eased edges, weighted layout, a minimap, live sweeps, and
  cuts that truncate honestly instead of pretending to be complete; the
  notebook is a workspace now, with chat, insights and an ask row.
- The machine prepares ahead: intent chips and hover packets tell you what
  a thing will do before you click it.
- A pulse bar, a focus echo and a command box that behaves like a surface.
- `physis-kernel` and `physis-language` are on **crates.io** (Apache-2.0).
  A third party can now depend on the kernel's observation and relation
  types, and on the language's checked inference, with `cargo add`.
  Their READMEs are compiled as doctests, so a snippet cannot ship a
  variant name that does not exist.

### Fixed
- The language README named variants that did not exist; it now compiles.
- Reading a large file no longer costs a full read before the size check.

### Not in this release
- No macOS or ARM build yet; Linux x86_64 (GLIBC <= 2.39) and Windows x86_64
  only. The macOS release jobs did not start: GitHub Actions refused them
  with a billing failure, so the bytes were never built and are not claimed
  here. When that is settled, the next patch carries macOS.

## [1.8.1] — 2026-10-21

Editor tabs, and the captioned walkthrough.

### Added
- The editor keeps tabs: every open file is listed, the front one is marked,
  each is closable, and opening an object that is already open focuses its tab
  instead of duplicating it. The per-file context budget rides along.
- The captioned desktop walkthrough (56 s) ships in `docs/demo/`.

### Added (late in the day, still on the same tag)
- A Windows x86_64 build joins the release after all:
  `physis-1.8.1-windows-x86_64.zip`, cross-compiled with mingw-w64
  (`BUILD.txt` inside the zip records provenance). The desktop, corpus and
  command line work; the terminal tab refuses with a clear reason — a PTY is
  a POSIX thing and Windows has none. The executables are unsigned.

### Not in this release
- No macOS or ARM build yet; Linux x86_64 (GLIBC <= 2.39) and Windows x86_64
  only. Server jobs to build those are returning errors — when they run
  again, the next patch carries macOS.

## [1.8.0] — 2026-10-21

The M2 batch: steps, the fleet, and a warm session that costs less.

### Added
- Runnable notebook steps: a cell can hold a textbox program; `run steps` (or
  `:nb run`) executes them in cell order, one trace per step, stopping at the
  first failure, and each run appends a receipt to the observation log.
- The fleet: configured aion nodes (`.physis/aion-nodes.json`) in the context
  panel and on the graph's outer ring; `/status` is probed only when asked.
  One shared client now serves the desktop, the HUD and the MCP bridge.
- The learning loop confirms but never auto-activates: a passing delegate
  leaves a `transition:` observation and a quarantined rule; only
  `physis cognition --activate <pattern>` promotes one.
- A warm session reuses the context packet it built before: the engine skips
  the recompile and the model reads identical bytes. Measured, paired, and
  published as "Shock 3" — cheaper, not smaller.
- The guide carries a session budget (calls, bytes, top tool) from the usage
  ledger.

### Not in this release
- No macOS, Windows or ARM build yet; Linux x86_64 only, GLIBC <= 2.39.

## [1.7.0] — 2026-10-20

Runnable steps and the fleet.

### Added
- Notebook step cells: a cell can hold a textbox program; `run steps` (or
  `:nb run`) executes them in cell order, one trace per step, stopping at the
  first failure, and each run appends a receipt to the observation log.
- The fleet: configured aion nodes (`.physis/aion-nodes.json`) appear in the
  context panel and on the graph's outer ring, with `/status` probed only on
  request. One shared client (`physis-fleet`) now serves the desktop, the HUD
  and the MCP bridge.

### Not in this release
- No macOS, Windows or ARM build yet; Linux x86_64 only, GLIBC ≤ 2.39.

## [1.6.0] — 2026-10-20

The desktop rework: the same world, arranged left to right, driven by mouse.

### Added
- A sectioned left rail (views, focus, world, recent) with a colour tick per
  section and a 3px accent bar on the active view.
- A window-wide right context panel: the focused object's identity, evidence
  and blast radius, with mouse actions for every verb it owns.
- Spawning inside a node: a spawned context packet, a staged agent task and a
  pinned notebook cell each open as a closable card on that object.
- The magic box moved to a bottom-centred bar with the hotkey map beside it as
  clickable compact chips (`⌃⇧Tab`), so the GUI needs no typing.
- The notebook is a three-column workspace (cells · selected cell · ask) with
  inline note editing (Enter saves, Esc cancels) and a per-cell context budget
  that cycles lean → full → off.
- A semantic colour ramp (raised, recessed, line, soft and faint ink) instead
  of one-off literals.

### Changed
- The graph's side panel folded into the window-wide context panel; depth,
  layout cycling and back now live in the graph header.

## [1.5.0] — 2026-10-20

The optional-model release: where a measurement justifies a model, the machine
may use one — and remains fully itself without one. Every model role is
default-OFF; the default build still opens no socket.

### Added
- Tier-3 language-surface scorer (`lang_backend=tiny`, feature `llm`): a
  selection-only engine over the candidates the machine already computed.
  Strict `VERDICT:<id> P:<0..100>` contract; prose, an off provider, a timeout
  or a non-candidate id is an abstain, never an answer. `T3` appears in the
  cascade tier status.
- Exact target-tokenizer accounting: `--tokenizer` on `compile`/`context` and
  an optional `tokenizer` argument on MCP `context_stats` print exact tokens
  next to the heuristic, each named. Counts equal `llama-tokenize` on the same
  bytes for the reference GGUF.
- Model role registry with gate verdicts: `physis llm status` renders a ROLES
  block (embed / causal / language scorer / tokenizer / reranker) with
  `[loaded|gate-failed|absent]` and the one-line reason; MCP
  `physis.intelligence` reads the same registry.

### Not in this release (honest limits)
- Measurement arms (8B-A1B delegate, small-arm matrix, rendering n≥3,
  ColBERT staging) are a pre-registered protocol, not results; delegate stays
  experimental, the reranker flag stays off.
- The scorer's self-reported `P` is uncalibrated until bench weights land;
  belief fusion and calibration are planned, not shipped.
- Default behaviour is unchanged: no account, no network, no model.

## [1.4.1] — 2026-10-20

### Fixed
- The GUI Diff tab no longer panics when no diff was run.

## [1.4.0] — 2026-10-20

The desktop release: the same world, navigable by mouse without a terminal.

### Added
- `physis-gui` — 22 tabs, Simple (nine core tabs) and Advanced depths, a
  `Ctrl+K` command palette with verb and id completion, 14 hotkeys, and
  `.physis/gui.json` layout persistence.
- Notebook workspace in the GUI: a selector over every notebook in the
  store, cell reorder, per-reference re-baseline, compile-context and
  ask-agent actions.
- Host in the repository graph: `scan host` / `:host` adds services,
  processes, sockets, the machine and boot to the same snapshot, with
  per-kind rendering and a Live inventory.
- Multi-root worlds: `observe roots` merges N trees with `r0:`/`r1:` ids
  and a graph badge naming each root.
- Receipt-bound change: delta flash on every re-observe, hover blast radius
  (callers, related tests, top three), and a cognition timeline with tier
  badges and per-step scores.
- MCP: notebook tools and an opt-in usage ledger (76 tool definitions, 74
  advertised, 49 on the native tier).
- One dark theme across GUI and HUD, generated help text, and a Settings
  usage section that reads the MCP ledger when present.

### Fixed
- Version guard: adapters and the commercial manifest now agree with the
  workspace (34 packages).
- `clippy -D warnings` clean across the workspace; rustfmt clean.
- The MCP usage-log path resolves through the `Env` provider instead of
  reading the process environment directly.

### Not in this release
- macOS, Windows and ARM builds: Linux x86_64 only, GLIBC ≤ 2.39.
- No recording ships in the repository yet.

## [1.3.1] — 2026-10-19 (AUD-03: truthful free first minute)

### Fixed
- `install.sh` no longer installs without verifying. A missing
  `SHA256SUMS.txt` previously passed silently, and in the `bin/`
  (public-repo) layout the top-level manifest was never found, so
  those archives verified nothing at all. The manifest is now
  required — found beside the script or beside the binaries, verified
  from its own directory — and a missing manifest or any mismatch
  aborts the install loudly. `--dry-run` is labeled a plan: it prints
  the manifest it will verify and fails on a missing one instead of
  the old "(if present)" wording.
- README: the CI badge linked to a repository layout that carries no
  workflows — removed. "about 26 MB" is now the measured 27.6 MB
  (14.9 + 12.7 MB). The signature promise is gone: the archive ships
  `SHA256SUMS.txt` only, and the README says checksums only. The
  `physis computer` transcript is a real run on a never-observed
  14-file repo (82 entities, 103 relations), replacing counts from a
  repository that does not ship. The first-minute path (demo → q →
  quiz, outside any checkout) is written into the Install section
  with commands proven against this exact build.
- CHANGELOG: the 1.2.0 demo transcript line said "96 relations"; the
  binary prints 117. Corrected.

### Known limit (stated, not hand-edited)
- `dist/physis-1.2.0-linux-x86_64.tar.gz` (sha256 a550e049…) was
  packed before the AUD-02 fix landed in `scripts/open-release.sh`,
  so the README inside the archive on disk is still the engine
  README, not this product README. The fix is committed; the next
  repack carries the product README. The archive itself was not
  touched — its hash matches `dist/SHA256SUMS.txt`, and the inner
  `physis`/`physis-hud` hashes are the ones recorded in the archive's
  own `SHA256SUMS.txt`.

## [1.2.0] — 2026-10-07

### Added
- `physis solve` verification ladder: `--check` is repeatable and
  each check carries a rung level — `level:name:command`,
  `name:command`, or a bare command (level defaults to `tests`).
  Levels run syntax → static → types → lint → tests → targeted →
  property → invariant → model → formal, in order, and the ladder
  **stops at the first failing rung**: a check that cannot pass
  tells the next rung nothing, and an unreached rung is never
  evidence. `success` still requires every declared check to have
  run and passed — a stopped ladder cannot read as success.
- Repair evidence: with `--editor`, every attempt now runs the
  whole ladder, and the re-plan prompt carries each failing
  check's bounded stderr/stdout tail beside the previous diff and
  its size. The report and the JSON output carry a **delta
  score** (`delta_score`): the final attempt's changed surface —
  added + removed lines, headers excluded. Lower is more minimal.

### Fixed
- One internal formatting defect the ladder itself caught in the
  engine tree (a staged edit had shipped unformatted).

## [1.1.1] — 2026-10-06

### Added (retroactively documented — all shipped in 1.1.1)
- `physis demo` — an end-to-end, offline, reproducible 7-stage loop bundled
  inside the binary: it extracts a 14-file demo fixture to a temp dir, puts it
  under git, then ** observe → ask → plan → act → re-observe → verify →
  remember**. The change is a rename of the `timeout` deadline gate to
  `deadline`; the engine rewrites it through the canonical write path,
  diffs the A→B world, and verifies structurally that callers/tests are
  unchanged. Run it anywhere: `physis demo`. No account, no network.
- `install.sh --dry-run` — prints where it writes, what it backs up, and
  whether checksums verify, without touching the filesystem or making any
  network call.
- `--doc-comments` on `physis observe` / `physis roots` — opt-in
  doc-comment and text-file primitives (`doc:` / `text:` entities),
  and the Go grammar: `.go` files now index package, import, const,
  type, var and function definitions, so a Go checkout becomes a
  queryable world too.
- Styled cognition trace views in `physis-hud` (section views over
  the deterministic cognition output).
- The interview corpus grew 145 → 157 primitives (12 new
  timeout/design entries).

### Changed
- README overhauled for honesty and reproducibility. The 30-second tour is now
   the `physis demo` transcript (stable 84 entities / 117 relations, real
   per-run git revisions). The `physis q` hero answer is the verbatim engine output.
   Every prose claim that can be checked is backed by a command below.
- Free-vs-paid table reconciled with the source: the local runtime exposes the
   full `physis serve` surface (62 tool definitions in the catalogue,
   60 advertised on `tools/list` — the protocol layer drops the 2
   deprecated aliases; 58 distinct + 2 deprecated aliases retained
   for compatibility). The paid Physis Context MCP remains a
   12-tool, read-only, licensed surface for coding agents. The unproven
   "caller recall: improved, measured" cell was replaced with an honest
   "improved — not claimed here without a number."
- License section clarified: Apache-2.0 applies to the corpus
   (`corpus/*.prim`) and documentation; the binaries are redistributable with
   this package only and are not source-available.

### Fixed
- The old hero tour cited `crates/...` and `client::request` ids that did not
  exist in the staged repository. It now runs on a self-contained fixture
  with canonical `src/client.rs::request` ids, so "on this repository" is true.

## [0.1.0-alpha.1]

- First public alpha of the physis-computer giveaway (binaries + 145-primitive
  interview corpus). Abstention-first `physis computer` tour; `physis q`/`arch`/
  `quiz`/`cheat` over the primitive library.
