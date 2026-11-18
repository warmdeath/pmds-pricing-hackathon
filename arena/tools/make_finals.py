#!/usr/bin/env python3
# =============================================================================
#  !!! SPOILER WARNING !!!  Builds the HELD-OUT evaluation scenarios.
#  Do NOT read this file or arena/configs/final_*.yaml during your attempt.
# =============================================================================
"""Write arena/configs/final_*.yaml from config/default.yaml / scaled_market.yaml."""
import copy
from pathlib import Path

import yaml

ROOT = Path(__file__).resolve().parents[2]
HEADER = """# =============================================================================
#  !!! SPOILER WARNING !!!  HELD-OUT EVALUATION SCENARIO -- DO NOT READ.
#  Like the organizers' private scenarios, this file is meant to stay unseen.
#  `arena/run.sh submit` plays it over several seeds.
# =============================================================================
"""


def load(name):
    return yaml.safe_load((ROOT / "config" / name).read_text())


def scale_supply(cfg, factors):
    for good, f in factors.items():
        s = cfg["suppliers"][good]
        s["production_min"] = max(1, round(s["production_min"] * f))
        s["production_max"] = max(s["production_min"], round(s["production_max"] * f))
        s["stock_capacity"] = max(s["production_max"], round(s["stock_capacity"] * f))


def scale_wtp(cfg, f):
    for seg in cfg["consumer_market"]["segments"].values():
        for good, (lo, hi) in seg["willingness_to_pay"].items():
            seg["willingness_to_pay"][good] = [round(lo * f, 1), round(hi * f, 1)]


def finish(cfg, name, seeds):
    cfg["agents"]["directory"] = "opponents"
    cfg["output"]["directory"] = f"../outputs/arena/{name}"
    cfg["output"]["dashboard"] = "none"
    cfg["output"]["render_plots"] = False
    cfg["output"]["progress_interval_turns"] = 1
    text = HEADER + f"# evaluation: seeds {seeds[0]}..{seeds[0]}+N-1, N = ARENA_SEEDS (default 8)\n" + yaml.safe_dump(cfg, sort_keys=False)
    (ROOT / "arena" / "configs" / f"{name}.yaml").write_text(text)


# 1) default-like market, a bit busier, 40 turns
a = load("default.yaml")
a["seed"] = 1101
scale_supply(a, {"CHIP": 1.4, "DISPLAY": 1.5, "BATTERY": 1.5, "CASING": 1.5})
a["consumer_market"].update(base_customers=38, amplitude=12)
finish(a, "final_1", [1101, 1102, 1103])

# 2) scaled-like market, scarce chips, 40 turns
b = load("scaled_market.yaml")
b["turns"] = 40
b["seed"] = 2201
scale_supply(b, {"CHIP": 0.8, "DISPLAY": 1.1, "BATTERY": 1.1, "CASING": 1.1})
b["initial_state"]["starting_capital"] = 50000.0
b["consumer_market"].update(base_customers=140, amplitude=45)
finish(b, "final_2", [2201, 2202, 2203])

# 3) long, lean default-like market: 80 turns, less capital, budget-heavy crowd
c = load("default.yaml")
c["turns"] = 80
c["seed"] = 3301
c["initial_state"]["starting_capital"] = 9000.0
scale_supply(c, {"CHIP": 1.2, "DISPLAY": 1.1, "BATTERY": 1.2, "CASING": 1.2})
c["consumer_market"].update(base_customers=32, amplitude=14, period_divisor=8.0)
segs = c["consumer_market"]["segments"]
segs["BUDGET"]["share"], segs["MAINSTREAM"]["share"], segs["PREMIUM"]["share"] = 0.55, 0.32, 0.13
scale_wtp(c, 0.92)
finish(c, "final_3", [3301, 3302, 3303])

# 4) long boom: 80 turns, big scaled market, richer premium segment
d = load("scaled_market.yaml")
d["turns"] = 80
d["seed"] = 4401
d["initial_state"]["starting_capital"] = 40000.0
scale_supply(d, {"CHIP": 1.1, "DISPLAY": 1.3, "BATTERY": 1.3, "CASING": 1.3})
d["consumer_market"].update(base_customers=150, amplitude=50, period_divisor=6.0)
segs = d["consumer_market"]["segments"]
segs["BUDGET"]["share"], segs["MAINSTREAM"]["share"], segs["PREMIUM"]["share"] = 0.40, 0.35, 0.25
scale_wtp(d, 1.1)
finish(d, "final_4", [4401, 4402, 4403])
print("wrote final_1..final_4")
