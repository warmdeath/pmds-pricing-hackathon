#!/usr/bin/env bash
# Markets, economics & finance crash course (terminal trainer).
#   course/run.sh              interactive menu
#   course/run.sh syllabus | learn 1.3 | practice [1.3|M2] | quiz [M1] | exam
#   course/run.sh review | glossary [term] | map | progress | selftest
set -euo pipefail
ROOT="$(cd "$(dirname "${BASH_SOURCE[0]}")/.." && pwd)"
cd "$ROOT"
export PYTHONDONTWRITEBYTECODE=1
exec uv run --quiet python course/trainer.py "$@"
