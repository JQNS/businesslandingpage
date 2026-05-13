#!/usr/bin/env bash
# Package the project into a .zip with index.html at the root of the archive.
#
# Usage:
#   ./package-site.sh
#   ./package-site.sh ~/Desktop/my-site.zip
#
# Default output: ../<folder-name>-site-YYYYMMDD-HHMMSS.zip (next to this folder)

set -euo pipefail

ROOT="$(cd "$(dirname "$0")" && pwd)"
DEFAULT_OUT="$(dirname "$ROOT")/$(basename "$ROOT")-site-$(date +%Y%m%d-%H%M%S).zip"
OUT="${1:-$DEFAULT_OUT}"
OUT="$(cd "$(dirname "$OUT")" && pwd)/$(basename "$OUT")"

cd "$ROOT"

# If writing the zip inside this folder, exclude it from the archive.
# (Avoid empty-array "${arr[@]}" with `set -u` — fails on some Bash versions.)
COMMON_EXCLUDES=(
  -x "*.git/*"
  -x ".git/*"
  -x ".git"
  -x "*.DS_Store"
  -x "*__pycache__/*"
  -x "*.py[cod]"
  -x ".venv/*"
  -x "venv/*"
  -x "node_modules/*"
)

if [[ "$OUT" == "$ROOT"/* ]]; then
  REL="${OUT#$ROOT/}"
  zip -r "$OUT" . -x "$REL" "${COMMON_EXCLUDES[@]}"
else
  zip -r "$OUT" . "${COMMON_EXCLUDES[@]}"
fi

echo "Created: $OUT"
echo "Check layout (index.html at archive root):"
unzip -l "$OUT" | head -25
