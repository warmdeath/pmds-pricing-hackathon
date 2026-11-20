"""Export the course (both sections) to course/web/dist/ for the browser app.

    uv run python course/web/build.py

Lessons, questions and glossary are copied as data; the Python exercise
generators are sampled into a large bank of concrete exercises, since the
browser can't run Python. The lesson files stay the single source of truth.
"""

from __future__ import annotations

import json
import random
import sys
from pathlib import Path

sys.dont_write_bytecode = True
WEB = Path(__file__).resolve().parent
COURSE = WEB.parent
sys.path.insert(0, str(COURSE))

import fundamentals as F  # noqa: E402
from fgenerators import FGENERATORS  # noqa: E402
from generators import GENERATORS  # noqa: E402
from glossary import GLOSSARY  # noqa: E402
from questions import QUESTIONS  # noqa: E402
from simmap import SIM_MAP  # noqa: E402
from syllabus import MODULES  # noqa: E402

BANK_PER_GENERATOR = 30

# Interactive charts shown in each lesson (ids defined in app.html)
WIDGETS = {
    "F3.2": ["slope-line"], "F3.3": ["slope-line"], "F3.4": ["supply-demand"], "F3.8": ["log-scale"],
    "F2.4": ["compound-growth"], "F2.5": ["compound-growth"],
    "F4.3": ["histogram-skew"], "F4.4": ["histogram-skew"], "F4.5": ["histogram-skew"],
    "F4.11": ["histogram-skew"],
    "F5.2": ["supply-demand"], "F5.3": ["wtp-staircase"], "F5.6": ["supply-demand"], "F5.7": ["supply-demand"],
    "F5.8": ["elasticity-revenue"], "F5.11": ["supply-demand"],
    "F6.3": ["cost-curves"], "F6.6": ["break-even"], "F6.7": ["cost-curves"], "F6.9": ["price-profit"],
    "F8.3": ["compound-growth"], "F8.5": ["discounting"], "F8.6": ["compound-growth"],
    "F11.7": ["break-even"], "F11.9": ["newsvendor"],
    "F12.5": ["binomial"], "F12.6": ["binomial"], "F12.8": ["normal"], "F12.9": ["normal"],
    "F12.10": ["normal"], "F12.11": ["clt"], "F12.12": ["clt"],
    "F13.1": ["discounting"], "F13.7": ["diversification"],
    "F15.2": ["clt"], "F15.4": ["normal"], "F15.8": ["normal"],
    "F16.1": ["scatter-regression"], "F16.3": ["scatter-regression"], "F16.5": ["scatter-regression"],
    "F16.7": ["scatter-regression"],
    "F18.2": ["price-profit"], "F18.8": ["newsvendor"],
    "1.1": ["ppf"], "1.2": ["supply-demand"], "1.3": ["elasticity-revenue"], "1.4": ["supply-demand"],
    "1.5": ["wtp-staircase"], "1.6": ["cost-curves"], "1.7": ["cost-curves"], "1.8": ["monopoly"],
    "1.9": ["logit-shares"], "2.5": ["bid-shading"], "2.6": ["bid-shading"], "2.7": ["newsvendor"],
    "3.4": ["break-even"], "3.5": ["discounting"], "3.6": ["diversification"], "4.1": ["compound-growth"],
}


def ex_record(ex) -> dict:
    return {"prompt": ex.prompt, "answer": float(ex.answer), "sol": ex.solution, "hint": ex.hint,
            "rel": ex.rel_tol, "abs": ex.abs_tol, "pct": bool(ex.percent_ok), "dec": ex.decimals,
            "traps": [[float(k), v] for k, v in ex.traps.items()]}


def bank(generators, seed: int) -> list[dict]:
    rng = random.Random(seed)
    out = []
    for g in generators:
        items, seen = [], set()
        for _ in range(BANK_PER_GENERATOR * 6):
            ex = g.make(rng)
            if ex.prompt in seen:
                continue
            seen.add(ex.prompt)
            items.append(ex_record(ex))
            if len(items) >= BANK_PER_GENERATOR:
                break
        out.append({"lesson": g.lesson, "topic": g.topic, "items": items})
    return out


def fund_export() -> list[dict]:
    units = []
    for u in F.units():
        lessons = []
        for lesson in u.lessons:
            exs = []
            for fx in lesson.exercises:
                rec = {"id": fx.id, "kind": fx.kind, "q": fx.question, "sol": fx.solution, "hint": fx.hint}
                if fx.kind == "num":
                    rec.update(answer=fx.answer, rel=fx.rel_tol, abs=fx.abs_tol, pct=fx.percent_ok,
                               traps=[[float(k), v] for k, v in fx.traps.items()])
                else:
                    rec.update(options=fx.options, correct=fx.correct,
                               traps={str(k): v for k, v in fx.traps.items()})
                exs.append(rec)
            lessons.append({"id": lesson.id, "title": lesson.title, "body": lesson.body,
                            "widgets": WIDGETS.get(lesson.id, []), "ex": exs})
        units.append({"id": u.id, "title": u.title, "track": u.track, "lessons": lessons})
    return units


def general_export() -> list[dict]:
    mods = []
    for m in MODULES:
        lessons = []
        for lesson in m["lessons"]:
            body = (COURSE / "content" / lesson["file"]).read_text(encoding="utf-8")
            body = "\n".join(body.splitlines()[1:]).strip()   # drop the "# 1.3 Title" line
            lessons.append({"id": lesson["id"], "title": lesson["title"], "body": body,
                            "widgets": WIDGETS.get(lesson["id"], [])})
        mods.append({"id": m["id"], "title": m["title"], "lessons": lessons})
    return mods


def main() -> None:
    dist = WEB / "dist"
    dist.mkdir(exist_ok=True)
    data = {
        "config": {"passShare": F.PASS_SHARE, "finalQuestions": F.FINAL_QUESTIONS,
                   "finalMinutes": F.FINAL_MINUTES, "finalPass": F.FINAL_PASS,
                   "leitnerDays": {"1": 0, "2": 1, "3": 3, "4": 7, "5": 16}},
        "fund": fund_export(),
        "general": general_export(),
        "questions": [{**q, "traps": {str(k): v for k, v in q.get("traps", {}).items()}} for q in QUESTIONS],
        "bank": {"fund": bank(FGENERATORS, 11), "general": bank(GENERATORS, 22)},
        "glossary": GLOSSARY,
        "map": SIM_MAP,
    }
    text = json.dumps(data, ensure_ascii=False, separators=(",", ":"))
    (dist / "data.json").write_text(text, encoding="utf-8")
    skeleton = ('<!doctype html><html lang="en"><head><meta charset="utf-8">'
                '<meta name="viewport" content="width=device-width,initial-scale=1,viewport-fit=cover">'
                '<style>:root{padding-top:env(safe-area-inset-top,0px);padding-bottom:env(safe-area-inset-bottom,0px)}'
                'body{margin:0}img{max-width:100%}[hidden]{display:none!important}</style></head><body>')
    (dist / "index.html").write_text(skeleton + (WEB / "app.html").read_text(encoding="utf-8") + "</body></html>",
                                     encoding="utf-8")
    n_bank = sum(len(g["items"]) for g in data["bank"]["fund"] + data["bank"]["general"])
    n_ex = sum(len(x["ex"]) for u in data["fund"] for x in u["lessons"])
    print(f"wrote {dist / 'data.json'} ({len(text) / 1e6:.2f} MB): "
          f"{sum(len(u['lessons']) for u in data['fund'])} fundamentals lessons, {n_ex} mastery exercises, "
          f"{sum(len(m['lessons']) for m in data['general'])} general lessons, {len(QUESTIONS)} questions, "
          f"{n_bank} practice exercises from {len(FGENERATORS) + len(GENERATORS)} generators")


if __name__ == "__main__":
    main()
