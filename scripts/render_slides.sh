#!/usr/bin/env bash
# render_slides.sh -- Render AsciiDoc walkthroughs to Reveal.js HTML
#
# Usage:
#   scripts/render_slides.sh                          # render all walkthroughs
#   scripts/render_slides.sh docs/walkthroughs/foo.adoc  # render one file
#
# Output: build/slides/<name>.html
# Generated HTML is gitignored; this directory maps to /latest/demo/slides/
# in the Pages publishing layout.

set -euo pipefail

ROOT="$(cd "$(dirname "${BASH_SOURCE[0]}")/.." && pwd)"
OUT_DIR="$ROOT/build/slides"
REVEALJS_CDN="https://cdn.jsdelivr.net/npm/reveal.js@4"

# Locate asciidoctor-revealjs (user gem install lands in ~/.local/share/gem)
if command -v asciidoctor-revealjs &>/dev/null; then
  RENDER_CMD="asciidoctor-revealjs"
elif [[ -x "$HOME/.local/share/gem/ruby/3.3.0/bin/asciidoctor-revealjs" ]]; then
  RENDER_CMD="$HOME/.local/share/gem/ruby/3.3.0/bin/asciidoctor-revealjs"
else
  echo "asciidoctor-revealjs not found."
  echo "Install with: gem install asciidoctor-revealjs"
  exit 2
fi

mkdir -p "$OUT_DIR"

if [[ -n "${1:-}" ]]; then
  FILES=("$1")
else
  mapfile -t FILES < <(find "$ROOT/docs/walkthroughs" -name "*.adoc" | sort)
fi

for src in "${FILES[@]}"; do
  echo "Rendering: $src"
  "$RENDER_CMD" \
    -a revealjsdir="$REVEALJS_CDN" \
    -D "$OUT_DIR" \
    "$src"
done

echo "Output: $OUT_DIR/"
echo "(gitignored — maps to /latest/demo/slides/ in Pages layout)"
