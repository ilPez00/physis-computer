# Changelog

All notable changes to **physis-computer** (the free, binary-only giveaway) are
documented here. This file is staged into the public repository alongside the
binaries; engine source is not — see the License section.

## [1.1.1] — 2026-10-06

### Added
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

### Changed
- README overhauled for honesty and reproducibility. The 30-second tour is now
  the `physis demo` transcript (stable 83 entities / 96 relations, real rA/rB
  git revisions). The `physis q` hero answer is the verbatim engine output.
  Every prose claim that can be checked is backed by a command below.
- Free-vs-paid table reconciled with the source: the local runtime exposes the
  full `physis serve` catalogue (62 tool definitions, 59 distinct; 2 deprecated
  aliases retained for compatibility). The paid Physis Context MCP remains a
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
