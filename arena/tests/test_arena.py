"""Arena self-tests.  Run from the repository root:

    uv run python -m unittest discover -s arena/tests -v

They import opponent classes but print nothing about their strategies.
"""

from __future__ import annotations

import csv
import json
import os
import shutil
import subprocess
import sys
import tempfile
import time
import unittest
import zipfile
from pathlib import Path
from time import perf_counter

sys.dont_write_bytecode = True  # never leave __pycache__ inside agent folders

ROOT = Path(__file__).resolve().parents[2]
sys.path.insert(0, str(ROOT / "arena" / "tools"))

import portal  # noqa: E402
from dme_simulator.agents.loader import discover_agent_bundles, load_agent_bundle_class  # noqa: E402
from dme_simulator.config import load_config  # noqa: E402
from dme_simulator.runner import (  # noqa: E402
    DecisionTimeout, _decide_with_timeout, _validate_decision,
)
from dme_simulator.simulation import DMESimulator  # noqa: E402

OPPONENTS = ROOT / "arena" / "opponents"
STARTER = ROOT / "src" / "dme_simulator" / "agents" / "my_agent"
RUN_SH = ROOT / "arena" / "run.sh"
ALL_CONFIGS = sorted((ROOT / "config").glob("*.yaml")) + sorted((ROOT / "arena" / "configs").glob("*.yaml"))
TURNS = 80
SAFE_MS = 50.0  # "well under" the 100 ms limit

STARTER_SOURCE = (STARTER / "agent.py").read_text()


def make_bundle(root: Path, name: str, source: str | None = None, extra: dict | None = None) -> Path:
    folder = root / name
    folder.mkdir(parents=True)
    (folder / "agent.py").write_text(STARTER_SOURCE if source is None else source)
    for rel, content in (extra or {}).items():
        path = folder / rel
        path.parent.mkdir(parents=True, exist_ok=True)
        if isinstance(content, bytes):
            path.write_bytes(content)
        else:
            path.write_text(content)
    return folder


def starter_with(body_line: str) -> str:
    """Insert one statement at the top of the starter's decide()."""
    return STARTER_SOURCE.replace(
        "        return Decision(", f"        {body_line}\n        return Decision(", 1
    )


class OpponentTests(unittest.TestCase):
    def test_field_has_39_loadable_opponents_with_spoiler_header(self):
        bundles = discover_agent_bundles([OPPONENTS])
        self.assertEqual(len(bundles), 39)
        self.assertEqual(len({b.name for b in bundles}), 39)
        for bundle in bundles:
            text = (bundle / "agent.py").read_text()
            self.assertIn("SPOILER WARNING", text.splitlines()[1], bundle.name)
            agent = load_agent_bundle_class(bundle)()
            self.assertTrue(callable(agent.decide))

    def test_every_opponent_is_fast_valid_and_never_crashes_on_every_config(self):
        bundles = discover_agent_bundles([OPPONENTS]) + [STARTER]
        classes = {b.name: load_agent_bundle_class(b) for b in bundles}
        for config_path in ALL_CONFIGS:
            with self.subTest(config=config_path.name):
                config = load_config(config_path)
                agents = {team: cls() for team, cls in classes.items()}
                simulator = DMESimulator(list(agents), config, seed=config.seed)
                slowest = 0.0
                for turn in range(1, TURNS + 1):
                    decisions = {}
                    for team, agent in agents.items():
                        if simulator.teams_state[team].bankrupt:
                            continue
                        state = simulator.get_team_state(team)
                        started = perf_counter()
                        try:
                            decision = _decide_with_timeout(agent, state, config.goods, 100.0)
                        except DecisionTimeout:
                            self.fail(f"{team} timed out on {config_path.name} turn {turn}")
                        elapsed = (perf_counter() - started) * 1000
                        _validate_decision(decision, state, config.goods)
                        if team != STARTER.name:
                            slowest = max(slowest, elapsed)
                        decisions[team] = decision
                    simulator.run_turn(decisions)
                self.assertLess(slowest, SAFE_MS, f"slowest decision {slowest:.1f} ms")


class PortalTests(unittest.TestCase):
    def setUp(self):
        self.tmp = Path(tempfile.mkdtemp(prefix="arena_test_"))

    def tearDown(self):
        shutil.rmtree(self.tmp, ignore_errors=True)

    def assertRejected(self, upload, fragment):
        result = portal.validate(upload)
        self.assertFalse(result.ok, f"expected rejection containing {fragment!r}")
        self.assertIn(fragment, result.reason)

    def test_starter_is_accepted(self):
        result = portal.validate(make_bundle(self.tmp, "good_team"))
        self.assertTrue(result.ok, result.reason)
        self.assertEqual(result.agent_id, "good_team")
        self.assertEqual(result.class_name, "StarterAgent")

    def test_enclosing_folder_and_helpers_are_accepted(self):
        bundle = make_bundle(self.tmp / "upload", "nested_team",
                             extra={"strategy.py": "X = 1\n", "models/w.npy": b"\x93NUMPY"})
        result = portal.validate(bundle.parent)
        self.assertTrue(result.ok, result.reason)
        self.assertEqual(result.agent_id, "nested_team")

    def test_zip_is_accepted(self):
        make_bundle(self.tmp, "zipped_team")
        archive = self.tmp / "zipped_team.zip"
        with zipfile.ZipFile(archive, "w", zipfile.ZIP_DEFLATED) as zf:
            zf.write(self.tmp / "zipped_team" / "agent.py", "zipped_team/agent.py")
        result = portal.validate(archive)
        self.assertTrue(result.ok, result.reason)

    def test_exception_in_decide_is_rejected(self):
        self.assertRejected(make_bundle(self.tmp, "boom", starter_with("raise RuntimeError('x')")),
                            "exception")

    def test_slow_decide_is_rejected(self):
        self.assertRejected(make_bundle(self.tmp, "slow", starter_with("import time; time.sleep(0.15)")),
                            "decision timeout (100 ms)")

    def test_invalid_action_is_rejected(self):
        src = STARTER_SOURCE.replace("AssemblyOrder(name, 1)", 'AssemblyOrder("NOPE", 1)')
        self.assertRejected(make_bundle(self.tmp, "invalid", src), "invalid action")

    def test_wrong_return_type_is_rejected(self):
        self.assertRejected(make_bundle(self.tmp, "wrongtype", starter_with("return {}")),
                            "invalid action")

    def test_unused_helper_that_does_not_compile_is_rejected(self):
        self.assertRejected(make_bundle(self.tmp, "syntax", extra={"helper.py": "def f(:\n"}),
                            "does not compile")

    def test_two_agent_classes_are_rejected(self):
        src = STARTER_SOURCE + "\n\nclass Second(StarterAgent):\n    pass\n"
        self.assertRejected(make_bundle(self.tmp, "twoclasses", src), "could not be loaded")

    def test_constructor_arguments_are_rejected(self):
        src = STARTER_SOURCE.replace(
            "class StarterAgent(BaseAgent):",
            "class StarterAgent(BaseAgent):\n    def __init__(self, x):\n        self.x = x\n")
        self.assertRejected(make_bundle(self.tmp, "ctorargs", src), "could not be loaded")

    def test_file_rules(self):
        self.assertRejected(make_bundle(self.tmp, "hidden", extra={".env": "x"}), "hidden")
        self.assertRejected(make_bundle(self.tmp, "txt", extra={"notes.txt": "x"}), "extension")
        self.assertRejected(make_bundle(self.tmp, "upper", extra={"m.NPY": b"x"}), "extension")
        self.assertRejected(make_bundle(self.tmp, "cache", extra={"__pycache__/a.pyc": b"x"}),
                            "__pycache__")
        self.assertRejected(make_bundle(self.tmp, "two", extra={"sub/agent.py": STARTER_SOURCE}),
                            "exactly one agent.py")
        self.assertRejected(make_bundle(self.tmp, "badname", extra={"-x.py": ""}), "invalid name")
        many = {f"h{i}.py": "" for i in range(64)}
        self.assertRejected(make_bundle(self.tmp, "many", extra=many), "too many files")
        big = make_bundle(self.tmp, "big", extra={"w.bin": b"\0" * (portal.MAX_BYTES + 1)})
        self.assertRejected(big, "20 MiB")
        self.assertRejected(make_bundle(self.tmp, "latin", extra={"h.py": b"# \xe9\n"}), "UTF-8")
        outside = self.tmp / "outer"
        make_bundle(outside, "inner")
        (outside / "loose.py").write_text("")
        self.assertRejected(outside, "inside the folder containing agent.py")
        self.assertRejected(make_bundle(self.tmp / "taken", "Team_404"), "already taken")

    def test_zip_rules(self):
        make_bundle(self.tmp, "z")
        traversal = self.tmp / "trav.zip"
        with zipfile.ZipFile(traversal, "w") as zf:
            zf.write(self.tmp / "z" / "agent.py", "z/agent.py")
            zf.writestr("../evil.py", "")
        self.assertRejected(traversal, "traversal")
        nested = self.tmp / "nested.zip"
        with zipfile.ZipFile(nested, "w") as zf:
            zf.write(self.tmp / "z" / "agent.py", "z/agent.py")
            zf.writestr("z/inner.zip", b"PK")
        self.assertRejected(nested, "nested archives")
        broken = self.tmp / "broken.zip"
        broken.write_bytes(b"not a zip")
        self.assertRejected(broken, "corrupted")

    def test_wall_clock_deadline(self):
        src = STARTER_SOURCE.replace(
            "class StarterAgent(BaseAgent):",
            "import time\n\nclass StarterAgent(BaseAgent):\n"
            "    def __init__(self):\n        time.sleep(1.5)\n")
        old = portal.WALL_SECONDS
        portal.WALL_SECONDS = 1.0
        try:
            self.assertRejected(make_bundle(self.tmp, "sleepy", src), "wall-clock deadline")
        finally:
            portal.WALL_SECONDS = old


class RunShEndToEnd(unittest.TestCase):
    """Drive arena/run.sh exactly as a participant would, in an isolated state dir."""

    @classmethod
    def setUpClass(cls):
        cls.state = Path(tempfile.mkdtemp(prefix="arena_state_"))
        cls.env = dict(os.environ, ARENA_STATE_DIR=str(cls.state), ARENA_SEEDS="1",
                       ARENA_TURNS="6")

    @classmethod
    def tearDownClass(cls):
        shutil.rmtree(cls.state, ignore_errors=True)

    def run_sh(self, *args, expect=0):
        result = subprocess.run([str(RUN_SH), *args], cwd=ROOT, env=self.env,
                                capture_output=True, text=True, timeout=600)
        self.assertEqual(result.returncode, expect, result.stdout + result.stderr)
        return result.stdout

    def rows(self):
        with (self.state / "submissions.csv").open() as stream:
            return list(csv.DictReader(stream))

    def test_full_day(self):
        out = self.run_sh("clock")
        self.assertIn("not started", out)
        out = self.run_sh("clock", "start")
        self.assertIn("time left", out)
        self.run_sh("clock", "start", expect=1)

        out = self.run_sh("practice", "--turns", "6")
        for section in ("PRACTICE FEEDBACK", "PER TURN", "[CHIP]", "[LAPTOP]", "TOTALS",
                        "FINAL STANDINGS", "stock at the end"):
            self.assertIn(section, out)
        self.assertNotIn("__pycache__", {p.name for p in STARTER.iterdir()})

        out = self.run_sh("leaderboard")
        self.assertIn("no counted submission", out)
        out = self.run_sh("submit")
        self.assertIn("OFFICIAL LEADERBOARD", out)
        self.assertIn("(you)", out)
        self.assertEqual(out.count(" │ "), 40 * 3)  # 40 rows x 3 inner separators
        self.assertTrue(list(self.state.glob("submissions/*/leaderboard_cash.png")))

        broken = Path(tempfile.mkdtemp()) / "broken_team"
        broken.mkdir()
        (broken / "agent.py").write_text("this is not python\n")
        out = self.run_sh("submit", str(broken), expect=1)
        self.assertIn("UPLOAD REJECTED", out)

        clock_file = self.state / ".clock"
        data = json.loads(clock_file.read_text())
        data["start"] = time.time() - 6 * 3600
        clock_file.write_text(json.dumps(data))
        self.assertIn("FINISHED", self.run_sh("clock"))
        out = self.run_sh("submit")
        self.assertIn("LATE", out)

        rows = self.rows()
        self.assertEqual([r["status"] for r in rows], ["on_time", "rejected", "late"])
        self.assertEqual([r["counted"] for r in rows], ["yes", "no", "no"])
        out = self.run_sh("leaderboard")
        self.assertIn(rows[0]["submission"], out.splitlines()[0])

        out = self.run_sh("clock", "reset")
        self.assertIn("cleared", out)

    def test_dashboards_batch(self):
        out = self.run_sh("dashboards", "--simulations", "2", "--turns", "3", "--max-workers", "2")
        self.assertIn("mean-curve dashboards", out)


if __name__ == "__main__":
    unittest.main()
