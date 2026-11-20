"""Two-way sync between the terminal trainer and the browser version."""

import json
import os
import shutil
import socket
import subprocess
import sys
import tempfile
import time
import unittest
import urllib.request
from pathlib import Path

sys.dont_write_bytecode = True
HERE = Path(__file__).resolve().parents[1]
sys.path.insert(0, str(HERE))

import progress  # noqa: E402

LAPTOP = {
    "read": {"F1.1": "2026-03-01", "F1.2": "2026-03-01"},
    "stats": {"F1.1": {"right": 3, "wrong": 1}},
    "cards": {"F1.1-1": {"box": 2, "due": "2026-03-02", "lesson": "F1.1", "t": 100},
              "gen:percent-of": {"box": 1, "due": "2026-03-01", "lesson": "F2.1", "t": 300}},
    "exams": [],
    "fund": {"passed": {"F1.1": "2026-03-01", "F1.2": "2026-03-01"}, "finals": [], "final_passed": False},
    "updated": 1000,
}
PHONE = {
    "read": {"F1.1": "2026-02-28", "F1.3": "2026-03-02"},
    "stats": {"F1.1": {"right": 2, "wrong": 4}, "F1.3": {"right": 3, "wrong": 0}},
    "cards": {"F1.1-1": {"box": 3, "due": "2026-03-05", "lesson": "F1.1", "t": 200},
              "gen:percent-of": {"box": 2, "due": "2026-03-03", "lesson": "F2.1", "t": 250}},
    "exams": [{"date": "2026-03-02", "right": 15, "total": 20, "grade": 22.5}],
    "fund": {"passed": {"F1.3": "2026-03-02"}, "finals": [{"date": "2026-03-02", "right": 20, "total": 30, "grade": 20.0}],
             "final_passed": True},
    "updated": 2000,
}


class MergeRules(unittest.TestCase):
    def test_rules(self):
        m = progress.merge(LAPTOP, PHONE)
        self.assertEqual(set(m["fund"]["passed"]), {"F1.1", "F1.2", "F1.3"})
        self.assertTrue(m["fund"]["final_passed"])
        self.assertEqual(m["read"]["F1.1"], "2026-02-28")                 # earliest date kept
        self.assertEqual(m["cards"]["F1.1-1"]["box"], 3)                   # newer answer (t=200) wins
        self.assertEqual(m["cards"]["gen:percent-of"]["box"], 1)           # newer answer (t=300) wins
        self.assertEqual(m["stats"]["F1.1"], {"right": 3, "wrong": 4})     # max of each count
        self.assertEqual(len(m["fund"]["finals"]), 1)
        self.assertEqual(m["updated"], 2000)

    def test_order_and_repetition_do_not_matter(self):
        ab, ba = progress.merge(LAPTOP, PHONE), progress.merge(PHONE, LAPTOP)
        self.assertEqual(ab, ba)
        self.assertEqual(progress.merge(ab, PHONE), ab)
        self.assertEqual(progress.merge(ab, ab), ab)

    def test_old_terminal_files_and_garbage(self):
        old = {"read": {}, "stats": {}, "cards": {"x": {"box": 1, "due": "2026-01-01"}}, "exams": []}
        self.assertIn("x", progress.merge(old, None)["cards"])
        self.assertEqual(progress.merge("nonsense", None)["fund"]["passed"], {})


@unittest.skipUnless(shutil.which("node"), "node not installed")
class BrowserParity(unittest.TestCase):
    def test_browser_merge_matches_python(self):
        src = (HERE / "web" / "app.html").read_text(encoding="utf-8")
        js = src.split("<script>")[1].split("</script>")[0]
        start = js.index("/* Same rules as course/progress.py merge()")
        end = js.index("/* ---------- lookups ---------- */")
        program = js[start:end] + (
            "\nconst [a, b] = JSON.parse(require('fs').readFileSync(0, 'utf8'));"
            "\nprocess.stdout.write(JSON.stringify([mergeStates(a, b), mergeStates(b, a), mergeStates(a, null)]));")
        out = subprocess.run(["node", "-e", program], input=json.dumps([LAPTOP, PHONE]), capture_output=True,
                             text=True, timeout=30)
        self.assertEqual(out.returncode, 0, out.stderr)
        js_ab, js_ba, js_a = json.loads(out.stdout)
        self.assertEqual(js_ab, progress.merge(LAPTOP, PHONE))     # 20 == 20.0 compares equal
        self.assertEqual(js_ba, progress.merge(PHONE, LAPTOP))
        self.assertEqual(js_a, progress.merge(LAPTOP, None))
        # a JS-written file merged back in Python must not duplicate attempts
        round_trip = progress.merge(progress.merge(LAPTOP, PHONE), js_ab)
        self.assertEqual(len(round_trip["fund"]["finals"]), 1)
        self.assertEqual(len(round_trip["exams"]), 1)


class LocalServerAndSyncCommand(unittest.TestCase):
    def setUp(self):
        self.tmp = Path(tempfile.mkdtemp())
        self.state = self.tmp / "progress.json"
        self.env = dict(os.environ, COURSE_STATE=str(self.state), HOME=str(self.tmp), PYTHONDONTWRITEBYTECODE="1")

    def tearDown(self):
        shutil.rmtree(self.tmp, ignore_errors=True)

    def test_server_shares_the_terminal_file(self):
        (HERE / "web" / "dist").mkdir(exist_ok=True)
        with socket.socket() as s:
            s.bind(("127.0.0.1", 0))
            port = s.getsockname()[1]
        proc = subprocess.Popen([sys.executable, str(HERE / "web" / "serve.py")],
                                env=dict(self.env, COURSE_WEB_PORT=str(port)),
                                stdout=subprocess.DEVNULL, stderr=subprocess.DEVNULL)
        try:
            url = f"http://127.0.0.1:{port}/api/progress"
            for _ in range(50):
                try:
                    urllib.request.urlopen(url, timeout=1)
                    break
                except OSError:
                    time.sleep(0.1)
            # the browser saves its progress
            req = urllib.request.Request(url, data=json.dumps(PHONE).encode(), method="PUT",
                                         headers={"Content-Type": "application/json"})
            json.loads(urllib.request.urlopen(req, timeout=5).read())
            # the terminal saves its own progress into the same file
            env_state = progress.read_file(self.state)
            self.assertIn("F1.3", env_state["fund"]["passed"])
            progress.save(dict(LAPTOP), self.state)
            # the browser reads back both
            got = json.loads(urllib.request.urlopen(url, timeout=5).read())
            self.assertEqual(set(got["fund"]["passed"]), {"F1.1", "F1.2", "F1.3"})
            self.assertTrue(got["fund"]["final_passed"])
        finally:
            proc.terminate()
            proc.wait(timeout=5)

    def test_sync_command_two_way(self):
        progress.write_file(progress.normalise(LAPTOP), self.state)
        downloads = self.tmp / "Downloads"
        downloads.mkdir()
        (downloads / "margin-notes-progress (1).json").write_text(json.dumps(PHONE))
        out = subprocess.run([sys.executable, str(HERE / "trainer.py"), "sync"], env=self.env,
                             capture_output=True, text=True, timeout=60)
        self.assertEqual(out.returncode, 0, out.stderr + out.stdout)
        merged = progress.read_file(self.state)
        self.assertEqual(set(merged["fund"]["passed"]), {"F1.1", "F1.2", "F1.3"})   # browser → terminal
        export = json.loads((downloads / progress.EXPORT_NAME).read_text())
        self.assertEqual(set(export["fund"]["passed"]), {"F1.1", "F1.2", "F1.3"})   # terminal → browser file
        self.assertIn("Load progress file", out.stdout)


if __name__ == "__main__":
    unittest.main()
