"""Entry point behind arena/run.sh."""

from __future__ import annotations

import argparse
import os
import subprocess
import sys
from pathlib import Path

sys.path.insert(0, str(Path(__file__).resolve().parent))

from common import DEFAULT_AGENT, PRACTICE_CONFIG, ROOT, OPPONENTS, python_env  # noqa: E402


def main() -> int:
    parser = argparse.ArgumentParser(prog="arena/run.sh", description="PMDS practice hackathon")
    sub = parser.add_subparsers(dest="command", required=True)

    practice = sub.add_parser("practice", help="one match on practice.yaml + feedback report")
    practice.add_argument("agent", nargs="?", default=str(DEFAULT_AGENT),
                          help="agent folder (default: src/dme_simulator/agents/my_agent)")
    practice.add_argument("--seed", type=int, help="seed override (default: the scenario's seed)")
    practice.add_argument("--turns", type=int, help="turn override (default: the scenario's turns)")
    practice.add_argument("--config", default=str(PRACTICE_CONFIG), help="scenario YAML")

    submit = sub.add_parser("submit", help="portal validation + full private evaluation")
    submit.add_argument("agent", nargs="?", default=str(DEFAULT_AGENT),
                        help="agent folder or .zip (default: src/dme_simulator/agents/my_agent)")
    submit.add_argument("--max-workers", type=int, help="parallel matches (default: CPU count)")

    sub.add_parser("leaderboard", help="official leaderboard of your latest counted submission")

    clock = sub.add_parser("clock", help="hackathon timer: `clock`, `clock start`, `clock reset`")
    clock.add_argument("action", nargs="?", default="status", choices=["status", "start", "reset"])

    dash = sub.add_parser("dashboards", help="simulator batch dashboards over several seeds")
    dash.add_argument("agent", nargs="?", default=str(DEFAULT_AGENT))
    dash.add_argument("--simulations", type=int, default=3)
    dash.add_argument("--seed", type=int)
    dash.add_argument("--max-workers", type=int)
    dash.add_argument("--turns", type=int)

    sub.add_parser("selftest", help="run the arena's own test suite")

    args = parser.parse_args()
    if args.command == "selftest":
        return subprocess.run([sys.executable, "-m", "unittest", "discover", "-s",
                               str(ROOT / "arena" / "tests"), "-v"], cwd=ROOT,
                              env=python_env()).returncode
    if args.command == "practice":
        from practice import run_practice
        return run_practice(args)
    if args.command == "submit":
        from evaluate import submit as do_submit
        return do_submit(args.agent, args.max_workers)
    if args.command == "leaderboard":
        from evaluate import leaderboard
        return leaderboard()
    if args.command == "clock":
        import clock as hackathon_clock
        return {"status": hackathon_clock.show, "start": hackathon_clock.start,
                "reset": hackathon_clock.reset}[args.action]()
    if args.command == "dashboards":
        output = ROOT / "outputs" / "arena" / "dashboards"
        command = [sys.executable, "-m", "dme_simulator", "--config", str(PRACTICE_CONFIG),
                   "--agents-dir", str(OPPONENTS), "--extra-agent", str(Path(args.agent).resolve()),
                   "--simulations", str(args.simulations), "--ui", "none",
                   "--output-dir", str(output)]
        if args.seed is not None:
            command += ["--seed", str(args.seed)]
        if args.max_workers:
            command += ["--max-workers", str(args.max_workers)]
        if args.turns:
            command += ["--turns", str(args.turns)]
        code = subprocess.run(command, cwd=ROOT, env=python_env()).returncode
        print(f"mean-curve dashboards: {output}")
        return code
    return 2


if __name__ == "__main__":
    os.chdir(Path(__file__).resolve().parents[2])
    sys.exit(main())
