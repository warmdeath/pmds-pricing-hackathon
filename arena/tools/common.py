"""Shared paths and helpers for the arena tools."""

from __future__ import annotations

import os
import sys
from pathlib import Path

ROOT = Path(__file__).resolve().parents[2]
ARENA = ROOT / "arena"
OPPONENTS = ARENA / "opponents"
CONFIGS = ARENA / "configs"
PRACTICE_CONFIG = CONFIGS / "practice.yaml"
DEFAULT_AGENT = ROOT / "src" / "dme_simulator" / "agents" / "my_agent"
# Per-attempt state (clock, submissions). Tests point this elsewhere.
STATE = Path(os.environ.get("ARENA_STATE_DIR", ARENA)).resolve()
HACKATHON_HOURS = 5.0


def python_env() -> dict[str, str]:
    env = dict(os.environ)
    env["PYTHONDONTWRITEBYTECODE"] = "1"
    env["MPLBACKEND"] = "Agg"
    return env


def cli_command(
    config: Path,
    *,
    extra_agent: Path,
    seed: int | None = None,
    turns: int | None = None,
    record: Path | None = None,
    output_dir: Path | None = None,
) -> list[str]:
    """The unmodified simulator CLI with the arena field and one extra agent."""
    command = [
        sys.executable, "-m", "dme_simulator",
        "--config", str(config),
        "--agents-dir", str(OPPONENTS),
        "--extra-agent", str(extra_agent),
        "--ui", "none",
    ]
    if seed is not None:
        command += ["--seed", str(seed)]
    if turns is not None:
        command += ["--turns", str(turns)]
    if record is not None:
        command += ["--record", str(record)]
    if output_dir is not None:
        command += ["--output-dir", str(output_dir)]
    return command
