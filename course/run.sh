#!/usr/bin/env bash
# Markets, economics & finance crash course (terminal trainer).
#   course/run.sh              interactive menu
#   course/run.sh syllabus | learn 1.3 | practice [1.3|M2] | quiz [M1] | exam
#   course/run.sh review | glossary [term] | map | progress | selftest
#   course/run.sh web          browser version on http://localhost:8765
set -euo pipefail
ROOT="$(cd "$(dirname "${BASH_SOURCE[0]}")/.." && pwd)"
cd "$ROOT"
export PYTHONDONTWRITEBYTECODE=1
if [ "${1:-}" = "web" ]; then
  uv run --quiet python course/web/build.py
  echo "Margin Notes is running at http://localhost:8765  (Ctrl+C to stop)"
  exec uv run --quiet python -m http.server 8765 --bind 127.0.0.1 --directory course/web/dist
fi
exec uv run --quiet python course/trainer.py "$@"
