"""`arena/run.sh practice`: one match of your agent against the 39-team field.

The match is played by the unmodified simulator CLI. To see your sealed bids
(which the simulator does not record), your agent is wrapped in a thin
pass-through bundle that logs each observation/decision to a JSONL file and
returns the decision unchanged. The team ID stays your folder name, so the
agent's random seed and behaviour are identical to an unwrapped run.
"""

from __future__ import annotations

import subprocess
import sys
from datetime import datetime
from pathlib import Path

from common import ROOT, cli_command, python_env
from report import build_report

WRAPPER = '''"""Auto-generated pass-through wrapper used by `arena/run.sh practice`."""
import json
import time
from pathlib import Path

from dme_simulator.agents.base import BaseAgent
from dme_simulator.agents.loader import load_agent_bundle_class

USER_BUNDLE = Path(%(bundle)r)
LOG_PATH = Path(%(log)r)


def _num(value):
    try:
        return float(value)
    except Exception:
        return str(value)


def _dump(record):
    with LOG_PATH.open("a", encoding="utf-8") as stream:
        stream.write(json.dumps(record, default=_num) + "\\n")


class InstrumentedAgent(BaseAgent):
    def __init__(self):
        LOG_PATH.write_text("", encoding="utf-8")
        self._inner = load_agent_bundle_class(USER_BUNDLE)()
        self._auction_seen = 0
        self._sales_seen = 0

    def decide(self, state, goods_config):
        auctions = state.auction_transactions
        sales = state.sales_transactions
        record = {
            "turn": state.turn,
            "capital": state.capital,
            "inventory": dict(state.inventory),
            "lots": [[lot.good, lot.quantity, lot.reserve_price] for lot in state.auction_lots],
            "prev_auction": [[t.good, t.quantity, t.price] for t in auctions[self._auction_seen:]],
            "prev_sales": [[t.good, t.quantity, t.price] for t in sales[self._sales_seen:]],
        }
        self._auction_seen = len(auctions)
        self._sales_seen = len(sales)
        started = time.perf_counter()
        try:
            decision = self._inner.decide(state=state, goods_config=goods_config)
        except BaseException as error:
            record["ms"] = (time.perf_counter() - started) * 1000.0
            record["error"] = type(error).__name__ + ": " + str(error)
            _dump(record)
            raise
        record["ms"] = (time.perf_counter() - started) * 1000.0
        try:
            record["bids"] = [[b.good, b.quantity, b.price_per_unit] for b in decision.bids]
            record["assembly"] = [[a.recipe_name, a.quantity] for a in decision.assembly]
            record["listings"] = [[l.good, l.quantity, l.price] for l in decision.listings]
        except Exception as error:
            record["malformed"] = type(error).__name__ + ": " + str(error)
        _dump(record)
        return decision
'''


def write_wrapper(bundle: Path, run_dir: Path) -> Path:
    wrapper_dir = run_dir / "instrumented" / bundle.name
    wrapper_dir.mkdir(parents=True)
    (wrapper_dir / "agent.py").write_text(
        WRAPPER % {"bundle": str(bundle), "log": str(run_dir / "decisions.jsonl")},
        encoding="utf-8",
    )
    return wrapper_dir


def run_practice(args) -> int:
    bundle = Path(args.agent).resolve()
    if not (bundle / "agent.py").is_file():
        print(f"no agent.py in {bundle}")
        return 2
    config = Path(args.config).resolve()
    stamp = datetime.now().strftime("%Y%m%d-%H%M%S")
    run_dir = ROOT / "outputs" / "arena" / "practice" / stamp
    run_dir.mkdir(parents=True, exist_ok=False)
    wrapper = write_wrapper(bundle, run_dir)
    command = cli_command(
        config, extra_agent=wrapper, seed=args.seed, turns=args.turns,
        record=run_dir / "simulation.jsonl", output_dir=run_dir / "dashboards",
    )
    print(f"practice match: {config.relative_to(ROOT) if config.is_relative_to(ROOT) else config}"
          f" | agent {bundle.name} | seed {args.seed if args.seed is not None else 'scenario default'}")
    print("running 40 teams ...", flush=True)
    with (run_dir / "stdout.txt").open("w") as out, (run_dir / "stderr.txt").open("w") as err:
        result = subprocess.run(command, cwd=ROOT, stdout=out, stderr=err, env=python_env())
    (run_dir / "command.txt").write_text(" ".join(command) + "\n")
    if result.returncode != 0 or not (run_dir / "simulation.jsonl").exists():
        print("the simulation did not complete:")
        print((run_dir / "stderr.txt").read_text()[-3000:])
        return 1
    text = build_report(run_dir, bundle.name, config)
    print(text)
    return 0


if __name__ == "__main__":
    sys.exit("use arena/run.sh practice")
