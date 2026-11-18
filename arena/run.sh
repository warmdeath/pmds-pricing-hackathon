#!/usr/bin/env bash
# PMDS dynamic-pricing practice hackathon.
#   arena/run.sh practice [AGENT_DIR] [--seed N] [--turns N]
#   arena/run.sh submit   [AGENT_DIR|ZIP] [--max-workers N]
#   arena/run.sh leaderboard
#   arena/run.sh clock [start|reset]
#   arena/run.sh selftest
#   arena/run.sh dashboards [AGENT_DIR] [--simulations N] [--seed N] [--max-workers N] [--turns N]
set -euo pipefail
ROOT="$(cd "$(dirname "${BASH_SOURCE[0]}")/.." && pwd)"
cd "$ROOT"
export PYTHONDONTWRITEBYTECODE=1   # keep __pycache__ out of your agent folder
export MPLBACKEND=Agg
if [ "$#" -eq 0 ]; then
  sed -n '2,8p' "$0" | sed 's/^# \{0,1\}//'
  exit 0
fi
# `clock` with no action means status
exec uv run --quiet python arena/tools/arena.py "$@"
