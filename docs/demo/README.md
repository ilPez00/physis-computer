# physis-gui demo

`docs/demo/physis-gui-demo.mp4` — 27s screen recording of the physis-next GUI (v1.8.7),
built on feather (6c / 7 G / x86_64) against `/home/gio/dev/aion` on Xorg :1.
Every frame is deterministic output: the same world, same verbs, same snapshot.

Shown, in order:

1. Graph ("Overview") tab — the most-related set around one root: rings,
   predicate counts, neighbor list, side panel.
2. Command box — `/agent opencode explain the budget`: preview on first
   Enter (bound context packet), launch on second Enter, live progress while
   the delegate runs, then the result is ingested and the world is
   re-observed (delta count in the status line).
3. Modes — command-box grammar toggle (`:` verb · `/` filter · `@` agent),
   editor Insert/Normal, graph layout (Radial · Tree · List cycle), focus
   mode (hide sidebar, `f` key).

Contains no source code — GUI surface only. Recorded with ffmpeg x11grab on
feather; 1280x720, libx264, ~1.7 MB.

`docs/demo/physis-gui-demo-1.8.7.mp4` — 56s captioned walkthrough of the
1.8.7 desktop (Linux x86_64, GLIBC ≤ 2.39): observe, search, compile, the host
joining the same world, the notebook, the editor, and the receipt that says what
changed. Recorded with `scripts/record-desktop.sh`; the rig and the facts it
encodes are in that script's header. No synthetic frames — every pixel is the
release binary.
