"""Course self-tests:  uv run python -m unittest discover -s course/tests -v"""

import io
import json
import os
import subprocess
import sys
import tempfile
import unittest
from pathlib import Path

sys.dont_write_bytecode = True
HERE = Path(__file__).resolve().parents[1]
sys.path.insert(0, str(HERE))

import fundamentals as F  # noqa: E402
from rich.console import Console  # noqa: E402
from rich.markdown import Markdown  # noqa: E402
from rich.panel import Panel  # noqa: E402
from rich.table import Table  # noqa: E402


class Quit(Exception):
    pass


def fake_ui(correct: bool):
    console = Console(file=io.StringIO(), width=100)
    return F.UI(console, ask=lambda *_: "", pause=lambda *_: None,
                run_mcq=lambda *a, **k: correct, run_exercise=lambda *a, **k: correct,
                shuffled=lambda q, rng: q, save=lambda s: None, record=lambda *a: None,
                Markdown=Markdown, Panel=Panel, Table=Table, Quit=Quit)


def fresh_state():
    return {"read": {}, "stats": {}, "cards": {}, "exams": [],
            "fund": {"passed": {}, "finals": [], "final_passed": False}}


class Content(unittest.TestCase):
    def test_size_and_integrity(self):
        problems, stats = F.selftest_problems()
        self.assertEqual(problems, [])
        self.assertGreaterEqual(stats["lessons"], 200)
        self.assertEqual(stats["units"], 18)
        self.assertGreaterEqual(stats["exercises"], 600)

    def test_every_unit_has_practice(self):
        from fgenerators import FGENERATORS
        units = {g.lesson.split(".")[0] for g in FGENERATORS}
        self.assertEqual(units, {u.id for u in F.units()})


class Unlocking(unittest.TestCase):
    def setUp(self):
        os.environ.pop("COURSE_UNLOCK_ALL", None)

    def test_lessons_unlock_in_order(self):
        state = fresh_state()
        self.assertTrue(F.is_unlocked(state, "F1.1"))
        self.assertFalse(F.is_unlocked(state, "F1.2"))
        self.assertFalse(F.cmd_check(fake_ui(False), state, "F1.1"))
        self.assertFalse(F.is_unlocked(state, "F1.2"))
        self.assertTrue(F.cmd_check(fake_ui(True), state, "F1.1"))
        self.assertTrue(F.is_unlocked(state, "F1.2"))
        self.assertFalse(F.is_unlocked(state, "F1.3"))
        self.assertFalse(F.cmd_check(fake_ui(True), state, "F2.1"))  # locked

    def test_final_gate(self):
        state = fresh_state()
        F.cmd_final(fake_ui(True), state, minutes=5, n=10, seed=1)
        self.assertFalse(F.general_unlocked(state))            # lessons not done
        for lesson in F.lessons():
            state["fund"]["passed"][lesson.id] = "2026-01-01"
        F.cmd_final(fake_ui(False), state, minutes=5, n=10, seed=1)
        self.assertFalse(F.general_unlocked(state))            # failed
        self.assertEqual(state["fund"]["finals"][-1]["grade"], 0)
        F.cmd_final(fake_ui(True), state, minutes=5, n=30, seed=2)
        self.assertTrue(F.general_unlocked(state))
        self.assertEqual(state["fund"]["finals"][-1]["grade"], 30)

    def test_final_covers_many_units(self):
        import random
        items = F.final_items(random.Random(3), 30)
        units = set()
        for kind, item in items:
            units.add((item.lesson if kind == "gen" else item.lesson).split(".")[0])
        self.assertGreaterEqual(len(units), 15)


class CLI(unittest.TestCase):
    def run_cli(self, *args, state_file):
        env = dict(os.environ, COURSE_STATE=str(state_file), PYTHONDONTWRITEBYTECODE="1")
        env.pop("COURSE_UNLOCK_ALL", None)
        return subprocess.run([sys.executable, str(HERE / "trainer.py"), *args], env=env,
                              capture_output=True, text=True, input="", timeout=120).stdout

    def test_general_course_is_gated(self):
        with tempfile.TemporaryDirectory() as tmp:
            state = Path(tmp) / "s.json"
            out = self.run_cli("learn", "1.3", "--no-pause", state_file=state)
            self.assertIn("unlocks after", out)
            data = fresh_state()
            data["fund"]["final_passed"] = True
            state.write_text(json.dumps(data))
            out = self.run_cli("learn", "1.3", "--no-pause", state_file=state)
            self.assertIn("Elasticity", out)

    def test_fundamentals_commands(self):
        with tempfile.TemporaryDirectory() as tmp:
            state = Path(tmp) / "s.json"
            self.assertIn("FUNDAMENTALS", self.run_cli("f", state_file=state))
            self.assertIn("What economics studies",
                          self.run_cli("f", "next", "--no-pause", state_file=state))
            self.assertIn("locked", self.run_cli("f", "learn", "F5.1", state_file=state))
            self.assertIn("F4.3", self.run_cli("f", "unit", "F4", state_file=state))

    def test_selftest(self):
        with tempfile.TemporaryDirectory() as tmp:
            self.assertIn("all checks passed", self.run_cli("selftest", state_file=Path(tmp) / "s.json"))


if __name__ == "__main__":
    unittest.main()
