"""5-hour hackathon clock (virtual 14:00 -> 19:00)."""

from __future__ import annotations

import json
import time
from datetime import datetime, timedelta

from common import HACKATHON_HOURS, STATE

CLOCK_FILE = STATE / ".clock"
VIRTUAL_START = "14:00"


def load() -> dict | None:
    if not CLOCK_FILE.exists():
        return None
    return json.loads(CLOCK_FILE.read_text())


def start(force: bool = False) -> int:
    state = load()
    if state and not force:
        print("the clock is already running (started "
              f"{datetime.fromtimestamp(state['start']):%Y-%m-%d %H:%M:%S}).")
        print("use `arena/run.sh clock reset` to discard it, then `clock start` again.")
        return 1
    STATE.mkdir(parents=True, exist_ok=True)
    CLOCK_FILE.write_text(json.dumps({"start": time.time(), "hours": HACKATHON_HOURS}))
    print("Hackathon started. Good luck!")
    return show()


def reset() -> int:
    if CLOCK_FILE.exists():
        CLOCK_FILE.unlink()
    print("clock cleared.")
    return 0


def deadline() -> float | None:
    state = load()
    if not state:
        return None
    return state["start"] + state["hours"] * 3600.0


def is_late(moment: float | None = None) -> bool:
    end = deadline()
    return end is not None and (moment or time.time()) > end


def _hm(seconds: float) -> str:
    seconds = max(0, int(seconds))
    return f"{seconds // 3600}:{seconds % 3600 // 60:02d}:{seconds % 60:02d}"


def show() -> int:
    state = load()
    if not state:
        print("clock not started. `arena/run.sh clock start` starts the 5-hour hackathon.")
        return 0
    now = time.time()
    begin = state["start"]
    end = begin + state["hours"] * 3600.0
    v0 = datetime.strptime(VIRTUAL_START, "%H:%M")
    virtual_now = v0 + timedelta(seconds=min(now, end) - begin)
    virtual_end = v0 + timedelta(hours=state["hours"])
    print(f"hackathon : {v0:%H:%M} - {virtual_end:%H:%M} (virtual)  |  real "
          f"{datetime.fromtimestamp(begin):%a %H:%M} - {datetime.fromtimestamp(end):%a %H:%M}")
    if now >= end:
        print(f"status    : FINISHED at {virtual_end:%H:%M} -- submissions are now late and do not count")
    else:
        done = (now - begin) / (end - begin)
        bar = "#" * int(done * 30) + "." * (30 - int(done * 30))
        print(f"now       : {virtual_now:%H:%M} (virtual)   [{bar}]")
        print(f"time left : {_hm(end - now)}   (deadline {datetime.fromtimestamp(end):%H:%M:%S} real)")
    return 0
