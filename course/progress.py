"""One progress format for the terminal trainer and the browser version.

Both sides store the same JSON (course/.progress.json on disk; claude.ai storage
or this file for the browser) and combine copies with the same merge rules, so
syncing in either direction, any number of times, never loses progress:

- read lessons, passed lessons: union (earliest date kept);
- final passed: true if true anywhere;
- finals and exams: union of attempts;
- review cards: per card, the most recently answered version wins (field "t");
- answer statistics: per lesson, the larger count of right and of wrong.

The browser's mergeStates() in course/web/app.html implements the same rules;
course/tests/test_sync.py checks that both produce identical results.
"""

from __future__ import annotations

import glob
import json
import os
import time
from pathlib import Path

HERE = Path(__file__).resolve().parent
STATE_FILE = Path(os.environ.get("COURSE_STATE", HERE / ".progress.json"))
EXPORT_NAME = "margin-notes-progress.json"


def blank() -> dict:
    return {"read": {}, "stats": {}, "cards": {}, "exams": [],
            "fund": {"passed": {}, "finals": [], "final_passed": False}, "updated": 0}


def normalise(s: dict | None) -> dict:
    out = blank()
    if not isinstance(s, dict):
        return out
    out["read"] = dict(s.get("read") or {})
    out["stats"] = {k: {"right": int(v.get("right", 0)), "wrong": int(v.get("wrong", 0))}
                    for k, v in (s.get("stats") or {}).items() if isinstance(v, dict)}
    out["cards"] = {k: dict(v) for k, v in (s.get("cards") or {}).items() if isinstance(v, dict)}
    out["exams"] = list(s.get("exams") or [])
    f = s.get("fund") or {}
    out["fund"] = {"passed": dict(f.get("passed") or {}), "finals": list(f.get("finals") or []),
                   "final_passed": bool(f.get("final_passed"))}
    out["updated"] = int(s.get("updated") or 0)
    return out


def _num(v) -> str:
    """Canonical number text, identical in Python and JavaScript (20.0 and 20 -> '20')."""
    try:
        return f"{float(v):.6f}".rstrip("0").rstrip(".")
    except (TypeError, ValueError):
        return str(v)


def _attempt_key(e: dict) -> str:
    return f"{e.get('date')}|{_num(e.get('right'))}|{_num(e.get('total'))}|{_num(e.get('grade'))}"


def _union_attempts(a: list, b: list) -> list:
    seen, out = set(), []
    for e in a + b:
        k = _attempt_key(e)
        if k not in seen:
            seen.add(k)
            out.append(e)
    return sorted(out, key=lambda e: (str(e.get("date")), _attempt_key(e)))


def _union_dates(a: dict, b: dict) -> dict:
    out = dict(a)
    for k, v in b.items():
        if k not in out or str(v) < str(out[k]):
            out[k] = v
    return dict(sorted(out.items()))


def merge(a: dict | None, b: dict | None) -> dict:
    a, b = normalise(a), normalise(b)
    cards = dict(a["cards"])
    for k, c in b["cards"].items():
        if k not in cards or c.get("t", 0) > cards[k].get("t", 0):
            cards[k] = c
    stats = {k: dict(v) for k, v in a["stats"].items()}
    for k, v in b["stats"].items():
        cur = stats.setdefault(k, {"right": 0, "wrong": 0})
        cur["right"] = max(cur["right"], v["right"])
        cur["wrong"] = max(cur["wrong"], v["wrong"])
    return {
        "read": _union_dates(a["read"], b["read"]),
        "stats": dict(sorted(stats.items())),
        "cards": dict(sorted(cards.items())),
        "exams": _union_attempts(a["exams"], b["exams"]),
        "fund": {"passed": _union_dates(a["fund"]["passed"], b["fund"]["passed"]),
                 "finals": _union_attempts(a["fund"]["finals"], b["fund"]["finals"]),
                 "final_passed": a["fund"]["final_passed"] or b["fund"]["final_passed"]},
        "updated": max(a["updated"], b["updated"]),
    }


def now_ms() -> int:
    return int(time.time() * 1000)


def read_file(path: Path = STATE_FILE) -> dict:
    try:
        return normalise(json.loads(Path(path).read_text()))
    except (OSError, json.JSONDecodeError):
        return blank()


def write_file(state: dict, path: Path = STATE_FILE) -> None:
    path = Path(path)
    tmp = path.with_suffix(path.suffix + ".tmp")
    tmp.write_text(json.dumps(state, indent=1))
    os.replace(tmp, path)


def save(state: dict, path: Path = STATE_FILE) -> dict:
    """Merge with what is on disk (the browser may have written meanwhile), then write."""
    state["updated"] = now_ms()
    merged = merge(read_file(path), state)
    write_file(merged, path)
    return merged


def download_dirs() -> list[Path]:
    """Folders where a browser on this machine saves downloads (Linux, macOS, WSL)."""
    dirs = [Path.home() / "Downloads"]
    dirs += [Path(p) for p in glob.glob("/mnt/c/Users/*/Downloads")]
    return [d for d in dirs if d.is_dir()]


def find_exports() -> list[Path]:
    """Progress files saved from the browser, newest first (browsers add ' (1)' etc.)."""
    files = []
    for d in download_dirs():
        files += [Path(p) for p in glob.glob(str(d / "margin-notes-progress*.json"))]
    return sorted(files, key=lambda p: p.stat().st_mtime, reverse=True)
