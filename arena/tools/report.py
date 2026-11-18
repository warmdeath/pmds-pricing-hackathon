"""Feedback report for one practice match: facts about your agent, no advice.

Sources:
* ``simulation.jsonl``  -- the simulator's own ``--record`` file (per-turn
  report: lots, units won, spend, production, listings, sales, market prices);
* ``decisions.jsonl``   -- the pass-through wrapper's log (your sealed bids,
  requested assembly/listings, decide time, own transactions);
* ``stderr.txt``        -- simulator warnings (timeouts / rejected decisions).
"""

from __future__ import annotations

import csv
import json
import re
from pathlib import Path

DASH = "-"


def _load_jsonl(path: Path) -> list[dict]:
    if not path.exists():
        return []
    return [json.loads(line) for line in path.read_text(encoding="utf-8").splitlines() if line]


def _fmt(value, digits=0, empty=DASH):
    if value is None:
        return empty
    if isinstance(value, str):
        return value
    if digits == 0:
        return f"{value:,.0f}"
    return f"{value:,.{digits}f}"


def _table(headers: list[str], rows: list[list], right: set[int] | None = None) -> str:
    right = right if right is not None else set(range(1, len(headers)))
    cells = [[str(c) for c in row] for row in rows]
    widths = [max(len(h), *(len(r[i]) for r in cells)) if cells else len(h)
              for i, h in enumerate(headers)]

    def line(values):
        return "  ".join(
            v.rjust(widths[i]) if i in right else v.ljust(widths[i])
            for i, v in enumerate(values)
        ).rstrip()

    out = [line(headers), line(["-" * w for w in widths])]
    out += [line(r) for r in cells]
    return "\n".join(out)


def _sparkline(values: list[float], width: int = 60) -> str:
    if not values:
        return ""
    blocks = " ▁▂▃▄▅▆▇█"
    step = max(1, len(values) / width)
    sampled = [values[min(len(values) - 1, int(i * step))] for i in range(min(width, len(values)))]
    lo, hi = min(sampled), max(sampled)
    span = hi - lo or 1.0
    return "".join(blocks[1 + int((v - lo) / span * 7.999)] for v in sampled)


def _ranks(final: dict[str, float], bankrupt: set[str]) -> dict[str, float]:
    """Average ranks by final cash, highest first; bankrupt teams last."""
    keyed = sorted(final, key=lambda t: (t in bankrupt, -final[t]))
    ranks: dict[str, float] = {}
    i = 0
    while i < len(keyed):
        j = i
        key = (keyed[i] in bankrupt, final[keyed[i]])
        while j + 1 < len(keyed) and (keyed[j + 1] in bankrupt, final[keyed[j + 1]]) == key:
            j += 1
        for k in range(i, j + 1):
            ranks[keyed[k]] = (i + j) / 2 + 1
        i = j + 1
    return ranks


def _paid_from_bids(bids: list[list], units: int) -> float | None:
    """Pay-your-bid: the units you won are filled from your highest bids down."""
    if units <= 0:
        return None
    total = 0.0
    left = units
    for _, qty, price in sorted(bids, key=lambda b: -b[2]):
        take = min(left, int(qty))
        total += take * price
        left -= take
        if left <= 0:
            break
    filled = units - left
    return total / filled if filled else None


def build_report(run_dir: Path, me: str, config_path: Path) -> str:
    frames = [r for r in _load_jsonl(run_dir / "simulation.jsonl") if r.get("type") == "frame"]
    meta = next(r for r in _load_jsonl(run_dir / "simulation.jsonl") if r.get("type") == "metadata")
    log = {r["turn"]: r for r in _load_jsonl(run_dir / "decisions.jsonl")}
    stderr = (run_dir / "stderr.txt").read_text(encoding="utf-8", errors="replace")
    materials = meta["raw_materials"]
    goods = meta["finished_goods"]
    teams = meta["team_ids"]
    turns = len(frames) - 1
    from dme_simulator.config import load_config

    recipe_output = {
        name: recipe.output_good for name, recipe in load_config(config_path).goods.recipes.items()
    }

    flags: dict[int, list[str]] = {}
    for match in re.finditer(rf"Agent {re.escape(me)} reached the decide timeout .* turn (\d+)", stderr):
        flags.setdefault(int(match.group(1)), []).append("TIMEOUT->empty decision")
    for match in re.finditer(
        rf"Agent {re.escape(me)} failed or returned an invalid decision on turn (\d+)", stderr
    ):
        flags.setdefault(int(match.group(1)), []).append("ERROR/INVALID->empty decision")

    start_cash = frames[0]["teams"][me]["capital"]
    last = frames[-1]["teams"]
    final = {t: last[t]["capital"] for t in teams}
    bankrupt = {t for t in teams if last[t]["bankrupt"]}
    ranks = _ranks(final, bankrupt)
    ordered = sorted(teams, key=lambda t: ranks[t])

    out: list[str] = []
    title = f"PRACTICE FEEDBACK  --  team {me}"
    out += ["=" * 78, title, "=" * 78]
    out.append(f"scenario: {config_path.name}   seed: {meta['seed']}   turns: {turns}   "
               f"teams: {len(teams)}")
    out.append(f"run folder: {run_dir}")
    out.append("")
    my_rank = ranks[me]
    rank_text = f"{my_rank:g}" if my_rank != int(my_rank) else f"{int(my_rank)}"
    out.append(f"final cash: {_fmt(final[me], 2)}   (start {_fmt(start_cash, 2)}, "
               f"change {final[me] - start_cash:+,.2f})   rank {rank_text} of {len(teams)}"
               + ("   BANKRUPT" if me in bankrupt else ""))
    median = sorted(final.values())[len(final) // 2]
    out.append(f"field: rank 1 = {_fmt(final[ordered[0]], 2)}   "
               f"rank 10 = {_fmt(final[ordered[min(9, len(ordered) - 1)]], 2)}   "
               f"median = {_fmt(median, 2)}   last = {_fmt(final[ordered[-1]], 2)}")
    end_inv = last[me]["inventory"]
    out.append("stock at the end (worth 0 in the score): "
               + ", ".join(f"{g} {end_inv.get(g, 0)}" for g in goods + materials))
    times = [r.get("ms", 0.0) for r in log.values()]
    if times:
        out.append(f"decide time: mean {sum(times) / len(times):.2f} ms, max {max(times):.2f} ms "
                   f"(limit 100 ms, measured inside the wrapper)")
    bad = sorted(flags)
    out.append(f"timeouts / rejected decisions: {len(bad)}" + (f" (turns {bad})" if bad else ""))

    # ------------------------------------------------------------------ per turn
    csv_rows: list[dict] = []
    overview = []
    material_rows = {m: [] for m in materials}
    product_rows = {g: [] for g in goods}
    totals_m = {m: {"bid": 0, "won": 0, "spent": 0.0} for m in materials}
    totals_g = {g: {"produced": 0, "listed": 0, "sold": 0, "revenue": 0.0, "mkt_rev": 0.0,
                    "mkt_units": 0, "list_value": 0.0} for g in goods}
    cash_series = [start_cash]

    for t in range(1, turns + 1):
        frame = frames[t]
        rep = frame["report"]
        mine = frame["teams"][me]
        before = frames[t - 1]["teams"][me]["capital"]
        cash_series.append(mine["capital"])
        entry = log.get(t, {})
        nxt = log.get(t + 1)
        spend = rep["auction_spend"].get(me, 0.0)
        revenue = rep["revenue"].get(me, 0.0)
        raw_stock = sum(mine["inventory"].get(m, 0) for m in materials)
        goods_stock = sum(mine["inventory"].get(g, 0) for g in goods)
        flag = "; ".join(flags.get(t, []) + ([entry["error"]] if "error" in entry else []))
        overview.append([t, _fmt(mine["capital"]), f"{mine['capital'] - before:+,.0f}",
                         _fmt(spend), _fmt(revenue), raw_stock, goods_stock,
                         _fmt(entry.get("ms"), 1), flag])

        lots = {lot[0]: lot for lot in entry.get("lots", [])}
        bids = entry.get("bids", []) if t not in flags else []
        for m in materials:
            my_bids = [b for b in bids if b[0] == m]
            bid_units = sum(int(b[1]) for b in my_bids)
            prices = sorted({round(float(b[2]), 2) for b in my_bids}, reverse=True)
            won = rep["units_won"].get(me, {}).get(m, 0)
            paid = None
            if nxt is not None:
                tx = [x for x in nxt.get("prev_auction", []) if x[0] == m]
                units = sum(x[1] for x in tx)
                paid = sum(x[1] * x[2] for x in tx) / units if units else None
            elif won:
                paid = _paid_from_bids(my_bids, won)
            reserve = lots[m][2] if m in lots else None
            material_rows[m].append([
                t, rep["lots"].get(m, 0), _fmt(reserve, 2), bid_units,
                "/".join(f"{p:g}" for p in prices) or DASH, won, _fmt(paid, 2),
                _fmt(rep["clearing_price"].get(m) or None, 2),
                _fmt(rep["highest_bid"].get(m) or None, 2),
            ])
            totals_m[m]["bid"] += bid_units
            totals_m[m]["won"] += won
            if paid is not None:
                totals_m[m]["spent"] += paid * won
            csv_rows.append({"turn": t, "kind": "material", "good": m, "lot": rep["lots"].get(m, 0),
                             "reserve": reserve, "bid_units": bid_units,
                             "bid_prices": "/".join(map(str, prices)), "won": won, "paid_per_unit": paid,
                             "market_low_win": rep["clearing_price"].get(m),
                             "market_high_win": rep["highest_bid"].get(m)})

        requested_build: dict[str, int] = {}
        for recipe, qty in entry.get("assembly", []) if t not in flags else []:
            requested_build[recipe] = requested_build.get(recipe, 0) + int(qty)
        for g in goods:
            produced = rep["produced"].get(me, {}).get(g, 0)
            listed = rep["listed"].get(me, {}).get(g, 0)
            my_price = rep["listed_price"].get(me, {}).get(g)
            sold = rep["units_sold"].get(me, {}).get(g, 0)
            stock = mine["inventory"].get(g, 0)
            sale_price = None
            if sold:
                if nxt is not None:
                    tx = [x for x in nxt.get("prev_sales", []) if x[0] == g]
                    units = sum(x[1] for x in tx)
                    sale_price = sum(x[1] * x[2] for x in tx) / units if units else None
                else:
                    ladder = sorted({float(x[2]) for x in entry.get("listings", []) if x[0] == g})
                    sale_price = ladder[0] if len(ladder) == 1 else (f"~{my_price:,.0f}" if my_price else None)
            mkt_units = rep["sold_by_good"].get(g, 0)
            mkt_price = rep["revenue_by_good"].get(g, 0.0) / mkt_units if mkt_units else None
            build_req = sum(q for r, q in requested_build.items() if recipe_output.get(r) == g)
            product_rows[g].append([
                t, build_req, produced, listed,
                _fmt(my_price, 2), sold, listed - sold, stock, _fmt(sale_price, 2),
                _fmt(mkt_price, 2), mkt_units, rep["stockouts"].get(g, 0),
            ])
            tg = totals_g[g]
            tg["produced"] += produced
            tg["listed"] += listed
            tg["sold"] += sold
            if my_price:
                tg["list_value"] += my_price * listed
            if isinstance(sale_price, float | int):
                tg["revenue"] += sale_price * sold
            tg["mkt_rev"] += rep["revenue_by_good"].get(g, 0.0)
            tg["mkt_units"] += mkt_units
            csv_rows.append({"turn": t, "kind": "product", "good": g, "requested_build": build_req,
                             "produced": produced, "listed": listed, "my_list_price": my_price,
                             "sold": sold, "unsold_listed": listed - sold, "stock_end": stock,
                             "my_sale_price": sale_price, "market_avg_sale_price": mkt_price,
                             "market_units_sold": mkt_units,
                             "market_unserved_customers": rep["stockouts"].get(g, 0)})
        csv_rows.append({"turn": t, "kind": "cash", "good": "", "cash_end": mine["capital"],
                         "auction_spend": spend, "revenue": revenue,
                         "decide_ms": entry.get("ms"), "flags": flag})

    out += ["", "CASH CURVE (start -> end)", _sparkline(cash_series),
            f"{_fmt(cash_series[0])} -> {_fmt(cash_series[-1])}   min {_fmt(min(cash_series))}   "
            f"max {_fmt(max(cash_series))}"]

    out += ["", "PER TURN -- cash, auction spend, sales revenue, stock held at end of turn",
            _table(["turn", "cash", "change", "spend", "revenue", "raw stock", "goods stock",
                    "decide ms", "flags"], overview, right=set(range(0, 8)))]

    out += ["", "PER MATERIAL -- lot = units offered to all teams; reserve = minimum bid;",
            "bid = your sealed bids (units, price levels); paid = what you paid per unit",
            "(pay-your-bid); market low/high win = lowest / highest winning price of all teams"]
    for m in materials:
        out += ["", f"[{m}]", _table(
            ["turn", "lot", "reserve", "bid units", "bid price(s)", "won", "paid/unit",
             "mkt low win", "mkt high win"], material_rows[m], right=set(range(0, 9)) - {4})]

    out += ["", "PER PRODUCT -- build req = units requested by your assembly orders; listed =",
            "units actually offered (capped by stock); my price = your average listed price;",
            "unsold = listed - sold this turn; stock = units held after the sales phase;",
            "my sale = average price of your sales; mkt avg = average sale price of all teams;",
            "mkt sold = units sold by all teams; unserved = customers wanting it who bought nothing"]
    for g in goods:
        out += ["", f"[{g}]", _table(
            ["turn", "build req", "produced", "listed", "my price", "sold", "unsold", "stock",
             "my sale", "mkt avg", "mkt sold", "unserved"], product_rows[g],
            right=set(range(0, 12)))]

    out += ["", "TOTALS -- materials"]
    rows = []
    for m in materials:
        tm = totals_m[m]
        fill = f"{100 * tm['won'] / tm['bid']:.0f}%" if tm["bid"] else DASH
        avg = tm["spent"] / tm["won"] if tm["won"] else None
        rows.append([m, tm["bid"], tm["won"], fill, _fmt(avg, 2), _fmt(tm["spent"])])
    out.append(_table(["material", "bid units", "won", "fill", "avg paid", "spent"], rows))

    out += ["", "TOTALS -- products (revenue counts sales whose price is known exactly)"]
    rows = []
    for g in goods:
        tg = totals_g[g]
        avg_list = tg["list_value"] / tg["listed"] if tg["listed"] else None
        mkt = tg["mkt_rev"] / tg["mkt_units"] if tg["mkt_units"] else None
        share = f"{100 * tg['sold'] / tg['mkt_units']:.1f}%" if tg["mkt_units"] else DASH
        rows.append([g, tg["produced"], tg["listed"], tg["sold"], end_inv.get(g, 0),
                     _fmt(avg_list, 2), _fmt(mkt, 2), share, _fmt(tg["revenue"])])
    out.append(_table(["product", "produced", "listed", "sold", "left", "avg my price",
                       "avg mkt price", "mkt share", "revenue"], rows))

    out += ["", "FINAL STANDINGS (this match)"]
    rows = []
    for t in ordered:
        r = ranks[t]
        rows.append([f"{r:g}", t + ("   <-- you" if t == me else ""), _fmt(final[t], 2),
                     "BANKRUPT" if t in bankrupt else ""])
    out.append(_table(["rank", "team", "final cash", ""], rows, right={0, 2}))

    png = _plot(run_dir, me, frames, teams)
    with (run_dir / "my_turns.csv").open("w", newline="", encoding="utf-8") as stream:
        fields: list[str] = []
        for row in csv_rows:
            for key in row:
                if key not in fields:
                    fields.append(key)
        writer = csv.DictWriter(stream, fieldnames=fields)
        writer.writeheader()
        writer.writerows(csv_rows)
    out += ["", "FILES",
            f"  full report : {run_dir / 'report.txt'}",
            f"  per-turn CSV: {run_dir / 'my_turns.csv'}",
            f"  cash plot   : {png}" if png else "  cash plot   : (matplotlib unavailable)",
            f"  dashboards  : {run_dir / 'dashboards'}",
            f"  replay      : uv run dme-sim --replay {run_dir / 'simulation.jsonl'}"]
    text = "\n".join(out)
    (run_dir / "report.txt").write_text(text + "\n", encoding="utf-8")
    return text


def _plot(run_dir: Path, me: str, frames: list[dict], teams: list[str]) -> Path | None:
    try:
        import matplotlib
        matplotlib.use("Agg")
        import matplotlib.pyplot as plt
    except ImportError:
        return None
    turns = list(range(len(frames)))
    figure, axis = plt.subplots(figsize=(11, 6))
    for team in teams:
        if team == me:
            continue
        axis.plot(turns, [f["teams"][team]["capital"] for f in frames],
                  color="#9aa0a6", linewidth=0.8, alpha=0.6)
    axis.plot(turns, [f["teams"][me]["capital"] for f in frames], color="#d93025",
              linewidth=2.6, label=f"{me} (you)")
    axis.plot([], [], color="#9aa0a6", linewidth=0.8, label="other 39 teams")
    axis.set_xlabel("turn")
    axis.set_ylabel("cash")
    axis.set_title("Practice match: cash over turns")
    axis.grid(alpha=0.3)
    axis.legend(loc="upper left")
    figure.tight_layout()
    path = run_dir / "cash_curve.png"
    figure.savefig(path, dpi=110)
    plt.close(figure)
    return path
