#!/usr/bin/env bash
# Install physis-computer. Linux x86_64, no root, no package manager.
#
# What this does, in two lines:
#   Verifies the bundled SHA256 checksums, then copies two binaries + the
#   interview corpus into the destination. No network, no package manager.
#
# Usage:
#   ./install.sh                 → ~/.local/bin
#   ./install.sh /usr/local/bin  → that directory (needs write access)
#   ./install.sh --dry-run       → print what would happen, change nothing
#
# Every prior executable is kept as .backup-<sha256> rather than replaced, so a
# bad install is reversible without a reinstall.
set -euo pipefail
HERE="$(cd "$(dirname "$0")" && pwd)"

# Parse args: --dry-run flag + optional destination directory.
DRY_RUN=0
DEST=""
for arg in "$@"; do
    case "$arg" in
        --dry-run) DRY_RUN=1 ;;
        -h|--help)
            sed -n '2,/^$/p' "$0" | sed 's/^# \{0,1\}//'
            exit 0 ;;
        *) DEST="$arg" ;;
    esac
done
DEST="${DEST:-$HOME/.local/bin}"

# Binaries live in ./bin/ when this is the unpacked public repository, and
# beside this script when it is the contents of a release tarball. Accept both
# rather than making the reader work out which layout they downloaded.
BIN_SRC="$HERE"
if [ ! -f "$HERE/physis" ] && [ -f "$HERE/bin/physis" ]; then
    BIN_SRC="$HERE/bin"
fi

if [ "$DRY_RUN" = 1 ]; then
    echo "[dry-run] destination:      $DEST"
    echo "[dry-run] binary source:    $BIN_SRC"
    echo "[dry-run] would verify:     $BIN_SRC/SHA256SUMS.txt (if present)"
    for executable in physis physis-hud; do
        if [ ! -f "$BIN_SRC/$executable" ]; then
            echo "[dry-run] missing $executable in $BIN_SRC — is this a complete download?" >&2
            exit 1
        fi
        if [ -e "$DEST/$executable" ]; then
            OLD_HASH="$(sha256sum "$DEST/$executable" | cut -d ' ' -f1)"
            echo "[dry-run] would back up existing $DEST/$executable → .backup-$OLD_HASH"
        fi
        echo "[dry-run] would install $executable → $DEST/$executable (0755)"
    done
    if [ -d "$HERE/corpus" ]; then
        CORPUS_DEST="$(cd "$DEST" 2>/dev/null && pwd)/../share/physis/corpus" || CORPUS_DEST="$DEST/../share/physis/corpus"
        echo "[dry-run] would install corpus → $CORPUS_DEST"
    fi
    echo "[dry-run] no files written, no network, no backups created."
    exit 0
fi

if [ -f "$BIN_SRC/SHA256SUMS.txt" ]; then
    (cd "$BIN_SRC" && sha256sum -c SHA256SUMS.txt) || {
        echo "checksum verification failed — refusing to install" >&2
        exit 1
    }
fi

mkdir -p "$DEST"
for executable in physis physis-hud; do
    if [ ! -f "$BIN_SRC/$executable" ]; then
        echo "missing $executable in $BIN_SRC — is this a complete download?" >&2
        exit 1
    fi
    if [ -e "$DEST/$executable" ]; then
        OLD_HASH="$(sha256sum "$DEST/$executable" | cut -d ' ' -f1)"
        cp -p "$DEST/$executable" "$DEST/$executable.backup-$OLD_HASH"
    fi
    install -m 755 "$BIN_SRC/$executable" "$DEST/$executable"
done

# The interview corpus is data, not code, and it is what lets `physis quiz`
# and `physis q` answer in any directory rather than only inside a Physis
# checkout. It goes beside the binaries at the exact prefix the runtime's
# shipped-corpus fallback searches, so the install location and the lookup
# cannot drift apart.
CORPUS_SRC="$HERE/corpus"
[ -d "$CORPUS_SRC" ] || CORPUS_SRC="$BIN_SRC/corpus"
if [ -d "$CORPUS_SRC" ]; then
    CORPUS_DEST="$(cd "$DEST" && pwd)/../share/physis/corpus"
    mkdir -p "$(dirname "$CORPUS_DEST")"
    rm -rf "$CORPUS_DEST"
    mkdir -p "$CORPUS_DEST"
    cp -R "$CORPUS_SRC/." "$CORPUS_DEST/"
    printf 'Installed interview corpus at %s\n' "$CORPUS_DEST"
fi

printf 'Installed physis-computer in %s\n' "$DEST"
printf 'Prior binaries retained as .backup-<sha256>.\n\n'
cat <<'NEXT'
Next:
  cd ~/your-project && physis computer     ← the 30-second tour
  physis-hud                               ← the full TUI

Nothing here needs an account, a network, or a model download.
NEXT
