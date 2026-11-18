"""`submit` and `leaderboard`: the arena's version of the organizers' portal.

Scoring follows README section 1.5: every (scenario, seed) is one match; each
match ranks all agents by final cash (highest first); the overall ranking is
the arithmetic mean of each agent's ranks across all matches (lower is
better). Only the latest submission before the deadline counts.
"""

from __future__ import annotations

import csv
import json
import os
import re
import subprocess
import time
from concurrent.futures import ThreadPoolExecutor, as_completed
from datetime import datetime
from pathlib import Path

import clock
from common import CONFIGS, ROOT, STATE, cli_command, python_env
from portal import validate
from report import _ranks

SUBMISSIONS_CSV = STATE / "submissions.csv"
SUBMISSIONS_DIR = STATE / "submissions"
SEEDS_PER_SCENARIO = int(os.environ.get("ARENA_SEEDS", "8"))
TURNS_OVERRIDE = int(os.environ["ARENA_TURNS"]) if os.environ.get("ARENA_TURNS") else None
CSV_FIELDS = ["submission", "timestamp", "agent", "status", "counted", "avg_rank",
              "position", "mean_cash", "matches", "timeouts", "errors", "reason"]
LINE_RE = re.compile(r"^  (.+?)\s+capital=(\S+)\s+goods=(\d+)\s*$")
TURN_RE = re.compile(r"^Turn (\d+)$")


def final_scenarios() -> list[Path]:
    return sorted(CONFIGS.glob("final_*.yaml"))


def _scenario_seed(config: Path) -> int:
    match = re.search(r"^seed:\s*(\d+)", config.read_text(), re.M)
    return int(match.group(1)) if match else 0


def _parse_match(stdout: str) -> tuple[dict[str, list[float]], set[str]]:
    """Per-team cash after every turn (finals print progress every turn)."""
    series: dict[str, list[float]] = {}
    bankrupt: set[str] = set()
    for line in stdout.splitlines():
        if TURN_RE.match(line):
            continue
        hit = LINE_RE.match(line)
        if not hit:
            continue
        team, cash, _ = hit.groups()
        if cash == "BANKRUPT":
            bankrupt.add(team)
            value = 0.0
        else:
            value = float(cash.replace("$", "").replace(",", ""))
        series.setdefault(team, []).append(value)
    return series, bankrupt


def _run_match(config: Path, seed: int, bundle: Path) -> dict:
    command = cli_command(config, extra_agent=bundle, seed=seed, turns=TURNS_OVERRIDE)
    started = time.perf_counter()
    run = subprocess.run(command, cwd=ROOT, capture_output=True, text=True, env=python_env())
    if run.returncode != 0:
        raise RuntimeError(f"{config.name} seed {seed} failed:\n{run.stderr[-2000:]}")
    series, bankrupt = _parse_match(run.stdout)
    me = bundle.name
    final = {team: values[-1] for team, values in series.items()}
    return {
        "scenario": config.stem, "seed": seed, "seconds": time.perf_counter() - started,
        "final": final, "bankrupt": sorted(bankrupt),
        "ranks": _ranks(final, bankrupt),
        "series": series,
        "my_timeouts": len(re.findall(rf"Agent {re.escape(me)} reached the decide timeout", run.stderr)),
        "my_errors": len(re.findall(rf"Agent {re.escape(me)} failed or returned an invalid", run.stderr)),
    }


def _standings(matches: list[dict]) -> list[dict]:
    teams = sorted({team for m in matches for team in m["final"]})
    rows = []
    for team in teams:
        ranks = [m["ranks"][team] for m in matches]
        cash = [m["final"][team] for m in matches]
        rows.append({"team": team, "avg_rank": sum(ranks) / len(ranks),
                     "mean_cash": sum(cash) / len(cash)})
    rows.sort(key=lambda r: (r["avg_rank"], -r["mean_cash"]))
    for position, row in enumerate(rows, 1):
        row["position"] = position
    return rows


def _append_csv(row: dict) -> None:
    STATE.mkdir(parents=True, exist_ok=True)
    new = not SUBMISSIONS_CSV.exists()
    with SUBMISSIONS_CSV.open("a", newline="", encoding="utf-8") as stream:
        writer = csv.DictWriter(stream, fieldnames=CSV_FIELDS)
        if new:
            writer.writeheader()
        writer.writerow({key: row.get(key, "") for key in CSV_FIELDS})


def _read_csv() -> list[dict]:
    if not SUBMISSIONS_CSV.exists():
        return []
    with SUBMISSIONS_CSV.open(newline="", encoding="utf-8") as stream:
        return list(csv.DictReader(stream))


def submit(upload: str, max_workers: int | None) -> int:
    submitted_at = time.time()
    late = clock.is_late(submitted_at)
    clock_running = clock.load() is not None
    stamp = datetime.fromtimestamp(submitted_at).strftime("%Y-%m-%d %H:%M:%S")
    number = len(_read_csv()) + 1
    sub_id = f"{number:03d}_{datetime.fromtimestamp(submitted_at):%Y%m%d-%H%M%S}"
    target = SUBMISSIONS_DIR / sub_id

    print(f"submission {sub_id}: {upload}")
    print("portal validation ...", flush=True)
    result = validate(upload, keep_dir=target)
    if not result.ok:
        _append_csv({"submission": sub_id, "timestamp": stamp, "agent": Path(upload).name,
                     "status": "rejected", "counted": "no", "reason": result.reason})
        print("UPLOAD REJECTED")
        print("reason: " + result.reason)
        return 1
    print(f"  valid: {result.agent_id} ({result.class_name}), {len(result.files)} file(s), "
          f"3 default-scenario turns in {result.wall_seconds:.2f} s")
    if late:
        print("  NOTE: the hackathon deadline has passed -- this submission is LATE and will not count.")
    elif not clock_running:
        print("  note: hackathon clock not started (`arena/run.sh clock start`); submission counts.")

    jobs = [(config, _scenario_seed(config) + offset)
            for config in final_scenarios() for offset in range(SEEDS_PER_SCENARIO)]
    workers = max(1, min(max_workers or (os.cpu_count() or 1), len(jobs)))
    print(f"evaluation: {len(final_scenarios())} private scenarios x {SEEDS_PER_SCENARIO} seeds "
          f"= {len(jobs)} matches, {workers} parallel workers", flush=True)
    matches: list[dict] = []
    started = time.perf_counter()
    with ThreadPoolExecutor(max_workers=workers) as pool:
        futures = [pool.submit(_run_match, config, seed, result.bundle_dir) for config, seed in jobs]
        for done, future in enumerate(as_completed(futures), 1):
            match = future.result()
            matches.append(match)
            print(f"  [{done:2d}/{len(jobs)}] match done ({time.perf_counter() - started:5.1f} s)",
                  flush=True)
    matches.sort(key=lambda m: (m["scenario"], m["seed"]))
    standings = _standings(matches)
    mine = next(row for row in standings if row["team"] == result.agent_id)
    timeouts = sum(m["my_timeouts"] for m in matches)
    errors = sum(m["my_errors"] for m in matches)
    status = "late" if late else "on_time"
    payload = {"submission": sub_id, "timestamp": stamp, "agent": result.agent_id,
               "status": status, "matches": matches, "standings": standings}
    (target / "results.json").write_text(json.dumps(payload), encoding="utf-8")
    _append_csv({"submission": sub_id, "timestamp": stamp, "agent": result.agent_id,
                 "status": status, "counted": "no" if late else "yes",
                 "avg_rank": f"{mine['avg_rank']:.3f}", "position": mine["position"],
                 "mean_cash": f"{mine['mean_cash']:.2f}", "matches": len(matches),
                 "timeouts": timeouts, "errors": errors})
    if timeouts or errors:
        print(f"  your agent: {timeouts} decision timeout(s), {errors} rejected decision(s) "
              "across all matches (empty decisions were used)")
    print()
    if late:
        print("LATE submission results (NOT counted; the official leaderboard is unchanged):")
        _print_table(payload)
        return 0
    return leaderboard()


def _official() -> tuple[dict | None, list[dict]]:
    rows = _read_csv()
    counted = [r for r in rows if r["counted"] == "yes"]
    if not counted:
        return None, rows
    latest = counted[-1]
    path = SUBMISSIONS_DIR / latest["submission"] / "results.json"
    return json.loads(path.read_text(encoding="utf-8")), rows


def leaderboard() -> int:
    payload, rows = _official()
    if payload is None:
        print("no counted submission yet. Submit with `arena/run.sh submit`.")
        return 0
    later = rows[rows.index(next(r for r in rows if r["submission"] == payload["submission"])) + 1:]
    print(f"OFFICIAL LEADERBOARD -- submission {payload['submission']} ({payload['timestamp']}),"
          f" agent {payload['agent']}")
    scenarios = sorted({m["scenario"] for m in payload["matches"]})
    print(f"{len(payload['matches'])} matches over {len(scenarios)} private scenarios; "
          "ranked by average rank (lower is better)")
    if later:
        kinds = ", ".join(f"{r['submission']}={r['status']}" for r in later)
        print(f"later submissions not counted: {kinds}")
    _print_table(payload)
    png = _plot(payload)
    if png:
        print(f"\ncash-over-turns plot: {png}")
    return 0


def _print_table(payload: dict) -> None:
    from rich.console import Console
    from rich.table import Table

    me = payload["agent"]
    table = Table(show_lines=False, header_style="bold")
    table.add_column("rank", justify="right")
    table.add_column("team name")
    table.add_column("final cash (mean)", justify="right")
    table.add_column("average rank", justify="right")
    for row in payload["standings"]:
        name = row["team"].replace("_", " ")
        style = None
        if row["team"] == me:
            name = f"▶ {name}  (you)"
            style = "bold black on bright_yellow"
        table.add_row(str(row["position"]), name, f"{row['mean_cash']:,.2f}",
                      f"{row['avg_rank']:.2f}", style=style)
    console = Console(highlight=False)
    console.print(table)
    mine = next(r for r in payload["standings"] if r["team"] == me)
    print(f"you: position {mine['position']} of {len(payload['standings'])}, "
          f"average rank {mine['avg_rank']:.2f}, mean final cash {mine['mean_cash']:,.2f}")


def _plot(payload: dict) -> Path | None:
    try:
        import matplotlib
        matplotlib.use("Agg")
        import matplotlib.pyplot as plt
    except ImportError:
        return None
    me = payload["agent"]
    scenarios = sorted({m["scenario"] for m in payload["matches"]})
    cols = 2 if len(scenarios) > 1 else 1
    rows = (len(scenarios) + cols - 1) // cols
    figure, axes = plt.subplots(rows, cols, figsize=(7.5 * cols, 4.8 * rows), squeeze=False)
    for index, scenario in enumerate(scenarios):
        axis = axes[index // cols][index % cols]
        matches = [m for m in payload["matches"] if m["scenario"] == scenario]
        teams = sorted(matches[0]["series"])
        length = min(len(m["series"][t]) for m in matches for t in teams)
        turns = list(range(1, length + 1))
        for team in teams:
            mean = [sum(m["series"][team][i] for m in matches) / len(matches) for i in range(length)]
            if team == me:
                axis.plot(turns, mean, color="#d93025", linewidth=2.8, zorder=5, label=f"{me} (you)")
            else:
                axis.plot(turns, mean, color="#9aa0a6", linewidth=0.8, alpha=0.55)
        axis.plot([], [], color="#9aa0a6", linewidth=0.8, label="other teams")
        axis.set_title(f"{scenario} -- mean cash over {len(matches)} seeds")
        axis.set_xlabel("turn")
        axis.set_ylabel("cash")
        axis.grid(alpha=0.3)
        axis.legend(loc="upper left", fontsize=8)
    for index in range(len(scenarios), rows * cols):
        axes[index // cols][index % cols].axis("off")
    figure.suptitle(f"Submission {payload['submission']} -- cash over turns per evaluation scenario")
    figure.tight_layout()
    path = SUBMISSIONS_DIR / payload["submission"] / "leaderboard_cash.png"
    figure.savefig(path, dpi=110)
    plt.close(figure)
    return path
