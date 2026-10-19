# physis-gui demo

`docs/demo/physis-gui-demo.mp4` — 27s screen recording of the physis-next GUI
(v1.3.3), built on feather and run against `/home/gio/dev/aion` on Xorg :1.

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
