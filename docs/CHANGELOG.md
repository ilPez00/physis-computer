# Changelog

All notable changes to **physis-computer** (the free, binary-only giveaway) are
documented here. This file is staged into the public repository alongside the
binaries; engine source is not — see the License section.

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
   the `physis demo` transcript (stable 84 entities / 96 relations, real rA/rB
   git revisions). The `physis q` hero answer is the verbatim engine output.
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
