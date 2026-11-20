"""Fundamentals: ~200 micro-lessons that must be completed first.

Lesson files live in course/fundamentals/uNN_*.md. Format:

    # F3 · Unit title | Track
    ## F3.1 Lesson title
    markdown body ...
    @num Question text (continuation lines allowed)
    = 12.5 ~0.1 %        answer, optional ~tolerance, optional % (accept 0.125 / 12.5)
    ? hint
    x 25 | why this wrong value is tempting
    ! worked solution
    @mcq Question text
    + correct option
    - wrong option | why it is tempting
    - wrong option
    ! explanation

Unlock rules: lessons open in order; a lesson is passed when its mastery check
scores >= 75 %; the Fundamentals final exam opens when every lesson is passed;
a final grade >= 18/30 unlocks the general course.
"""

from __future__ import annotations

import math
import os
import random
import re
import time
from dataclasses import dataclass, field
from datetime import date
from pathlib import Path

from generators import Exercise

HERE = Path(__file__).resolve().parent
FUND_DIR = HERE / "fundamentals"
PASS_SHARE = 0.75
FINAL_QUESTIONS = 30
FINAL_MINUTES = 90
FINAL_PASS = 18


@dataclass
class FExercise:
    kind: str                  # "num" | "mcq"
    question: str
    answer: float | None = None
    rel_tol: float = 0.01
    abs_tol: float = 0.011
    percent_ok: bool = False
    hint: str = ""
    solution: str = ""
    options: list[str] = field(default_factory=list)
    correct: int = 0
    traps: dict = field(default_factory=dict)
    id: str = ""
    lesson: str = ""


@dataclass
class FLesson:
    id: str
    title: str
    unit: str
    body: str
    exercises: list[FExercise]


@dataclass
class FUnit:
    id: str
    title: str
    track: str
    lessons: list[FLesson]


def _parse_answer(text: str, ex: FExercise) -> None:
    tokens = text.split()
    ex.answer = float(tokens[0].replace(",", ""))
    for tok in tokens[1:]:
        if tok.startswith("~"):
            ex.abs_tol = float(tok[1:])
            ex.rel_tol = 0.0
        elif tok == "%":
            ex.percent_ok = True


def parse_unit(path: Path) -> FUnit:
    unit: FUnit | None = None
    lesson: FLesson | None = None
    ex: FExercise | None = None
    body: list[str] = []

    def close_lesson():
        nonlocal lesson, ex, body
        if lesson is not None:
            lesson.body = "\n".join(body).strip()
            unit.lessons.append(lesson)
        lesson, ex, body = None, None, []

    for raw in path.read_text(encoding="utf-8").splitlines():
        line = raw.rstrip()
        if line.startswith("# F") and not line.startswith("## "):
            head, _, track = line[2:].partition("|")
            uid, _, title = head.strip().partition("·")
            unit = FUnit(uid.strip(), title.strip(), track.strip(), [])
            continue
        if line.startswith("## F"):
            close_lesson()
            lid, _, title = line[3:].strip().partition(" ")
            lesson = FLesson(lid, title.strip(), unit.id, "", [])
            continue
        if lesson is None:
            continue
        if line.startswith("@num ") or line.startswith("@mcq "):
            ex = FExercise(kind=line[1:4], question=line[5:].strip(), lesson=lesson.id,
                           id=f"{lesson.id}-{len(lesson.exercises) + 1}")
            lesson.exercises.append(ex)
            continue
        if ex is None:
            body.append(raw)
            continue
        if not line.strip():
            continue
        tag, rest = line[:2], line[2:].strip()
        if tag == "= ":
            _parse_answer(rest, ex)
        elif tag == "? ":
            ex.hint = rest
        elif tag == "! ":
            ex.solution = (ex.solution + " " + rest).strip()
        elif tag == "+ ":
            ex.correct = len(ex.options)
            ex.options.append(rest)
        elif tag == "- ":
            option, _, why = rest.partition(" | ")
            if why:
                ex.traps[len(ex.options)] = why
            ex.options.append(option)
        elif tag == "x ":
            value, _, why = rest.partition(" | ")
            ex.traps[float(value)] = why
        else:
            ex.question += "\n" + line.strip()
    close_lesson()
    return unit


_CACHE: list[FUnit] | None = None


def units() -> list[FUnit]:
    global _CACHE
    if _CACHE is None:
        _CACHE = [parse_unit(p) for p in sorted(FUND_DIR.glob("u*.md"))]
        _CACHE.sort(key=lambda u: int(u.id[1:]))
    return _CACHE


def lessons() -> list[FLesson]:
    return [lesson for unit in units() for lesson in unit.lessons]


def lesson(lid: str) -> FLesson | None:
    return next((x for x in lessons() if x.id.lower() == lid.lower()), None)


# =============================================================================
# progress and gating
# =============================================================================

def fstate(state: dict) -> dict:
    return state.setdefault("fund", {"passed": {}, "finals": [], "final_passed": False})


def general_unlocked(state: dict) -> bool:
    return os.environ.get("COURSE_UNLOCK_ALL") == "1" or fstate(state).get("final_passed", False)


def is_unlocked(state: dict, lid: str) -> bool:
    if os.environ.get("COURSE_UNLOCK_ALL") == "1":
        return True
    passed = fstate(state)["passed"]
    order = [x.id for x in lessons()]
    index = order.index(lid)
    return index == 0 or order[index - 1] in passed


def next_lesson(state: dict) -> FLesson | None:
    passed = fstate(state)["passed"]
    return next((x for x in lessons() if x.id not in passed), None)


def to_exercise(fx: FExercise) -> Exercise:
    return Exercise(prompt=fx.question, answer=fx.answer, solution=fx.solution or "—",
                    hint=fx.hint or "Re-read the lesson's worked example.", lesson=fx.lesson,
                    topic=fx.id, traps=dict(fx.traps), rel_tol=fx.rel_tol, abs_tol=fx.abs_tol,
                    percent_ok=fx.percent_ok, decimals=4)


def to_mcq(fx: FExercise) -> dict:
    return {"id": fx.id, "lesson": fx.lesson, "q": fx.question, "options": list(fx.options),
            "answer": fx.correct, "why": fx.solution or "", "traps": dict(fx.traps)}


# =============================================================================
# commands (UI helpers are passed in from trainer.py to avoid import cycles)
# =============================================================================

class UI:
    def __init__(self, console, ask, pause, run_mcq, run_exercise, shuffled, save, record, Markdown,
                 Panel, Table, Quit):
        self.__dict__.update(locals())


def cmd_overview(ui: UI, state: dict) -> None:
    fs = fstate(state)
    passed = fs["passed"]
    total = len(lessons())
    done = len([x for x in lessons() if x.id in passed])
    ui.console.print(ui.Panel(
        f"[bold]FUNDAMENTALS[/] — {done}/{total} lessons passed.  "
        + ("[green]General course UNLOCKED.[/]" if general_unlocked(state)
           else f"The general course unlocks after the final exam (≥ {FINAL_PASS}/30)."),
        border_style="green"))
    table = ui.Table(show_header=True, header_style="bold")
    table.add_column("unit")
    table.add_column("track")
    table.add_column("title")
    table.add_column("lessons", justify="right")
    table.add_column("status")
    for unit in units():
        n = len(unit.lessons)
        k = len([x for x in unit.lessons if x.id in passed])
        status = "✔ done" if k == n else ("▶ in progress" if k or is_unlocked(state, unit.lessons[0].id)
                                          else "🔒 locked")
        table.add_row(unit.id, unit.track, unit.title, f"{k}/{n}", status)
    ui.console.print(table)
    nxt = next_lesson(state)
    if nxt:
        ui.console.print(f"next: [bold]{nxt.id} {nxt.title}[/]  →  `f next`")
    elif not fs.get("final_passed"):
        ui.console.print("all lessons passed → `f final` to take the Fundamentals final exam")
    best = max((e["grade"] for e in fs["finals"]), default=None)
    if best is not None:
        ui.console.print(f"best final grade: {best:.0f}/30")


def cmd_unit(ui: UI, state: dict, uid: str) -> None:
    unit = next((u for u in units() if u.id.lower() == uid.lower()), None)
    if unit is None:
        ui.console.print(f"no unit {uid}")
        return
    passed = fstate(state)["passed"]
    table = ui.Table(title=f"{unit.id} · {unit.title} ({unit.track})", show_header=True)
    table.add_column("lesson")
    table.add_column("title")
    table.add_column("exercises", justify="right")
    table.add_column("status")
    for x in unit.lessons:
        status = "✔" if x.id in passed else ("open" if is_unlocked(state, x.id) else "🔒")
        table.add_row(x.id, x.title, str(len(x.exercises)), status)
    ui.console.print(table)


def cmd_learn(ui: UI, state: dict, lid: str | None, interactive: bool = True) -> None:
    target = lesson(lid) if lid else next_lesson(state)
    if target is None:
        ui.console.print("no such lesson" if lid else "all lessons passed — `f final`")
        return
    if not is_unlocked(state, target.id):
        nxt = next_lesson(state)
        ui.console.print(f"🔒 {target.id} is locked. Lessons open in order; next: {nxt.id} {nxt.title}.")
        return
    unit = next(u for u in units() if u.id == target.unit)
    ui.console.print(ui.Markdown(f"# {target.id} {target.title}\n*{unit.id} · {unit.title} — {unit.track}*"))
    ui.console.print(ui.Markdown(target.body))
    if not interactive:
        return
    ui.pause("Enter = mastery check, q = stop")
    cmd_check(ui, state, target.id)


def cmd_check(ui: UI, state: dict, lid: str) -> bool:
    target = lesson(lid)
    if target is None or not is_unlocked(state, target.id):
        ui.console.print("lesson locked or unknown")
        return False
    rng = random.Random()
    items = list(target.exercises)
    rng.shuffle(items)
    right = 0
    ui.console.print(f"[bold]Mastery check {target.id}[/] — {len(items)} questions, pass ≥ "
                     f"{math.ceil(PASS_SHARE * len(items))}.")
    for n, fx in enumerate(items, 1):
        label = f"({n}/{len(items)}) "
        if fx.kind == "mcq":
            right += ui.run_mcq(ui.shuffled(to_mcq(fx), rng), state, label)
        else:
            right += ui.run_exercise(to_exercise(fx), state, label)
    need = math.ceil(PASS_SHARE * len(items))
    passed = right >= need
    fs = fstate(state)
    if passed:
        fs["passed"].setdefault(target.id, date.today().isoformat())
        ui.save(state)
        nxt = next_lesson(state)
        ui.console.print(f"[green]✔ {right}/{len(items)} — {target.id} passed.[/] "
                         + (f"Unlocked: {nxt.id} {nxt.title} (`f next`)" if nxt else
                            "All lessons done → `f final`"))
    else:
        ui.console.print(f"[red]✘ {right}/{len(items)} — need {need}.[/] Re-read and `f check {target.id}` again.")
    return passed


def cmd_practice(ui: UI, state: dict, selector: str | None) -> None:
    from fgenerators import FGENERATORS
    passed = fstate(state)["passed"]
    pool = [g for g in FGENERATORS
            if is_unlocked(state, g.lesson) or g.lesson in passed]
    if selector:
        sel = selector.upper()
        pool = [g for g in pool if g.lesson == sel or g.lesson.split(".")[0] == sel]
    if not pool:
        ui.console.print("no unlocked practice for that selection yet (practice opens with each lesson).")
        return
    rng = random.Random()
    right = done = 0
    ui.console.print(f"[bold]Fundamentals practice[/] — {len(pool)} exercise type(s). q = stop.")
    try:
        while True:
            ex = rng.choice(pool).make(rng)
            done += 1
            right += ui.run_exercise(ex, state, f"#{done}  ")
    except ui.Quit:
        pass
    if done:
        ui.console.print(f"\nsession: {right}/{done} correct")


def final_items(rng: random.Random, n: int = FINAL_QUESTIONS):
    from fgenerators import FGENERATORS
    by_unit: dict[str, list] = {}
    for x in lessons():
        for fx in x.exercises:
            by_unit.setdefault(x.unit, []).append(("static", fx))
    for g in FGENERATORS:
        by_unit.setdefault(g.lesson.split(".")[0], []).append(("gen", g))
    unit_ids = list(by_unit)
    rng.shuffle(unit_ids)
    items = []
    i = 0
    while len(items) < n:
        pool = by_unit[unit_ids[i % len(unit_ids)]]
        items.append(rng.choice(pool))
        i += 1
    rng.shuffle(items)
    return items


def cmd_final(ui: UI, state: dict, minutes: float = FINAL_MINUTES, n: int = FINAL_QUESTIONS,
              seed: int | None = None, force: bool = False) -> None:
    fs = fstate(state)
    if next_lesson(state) is not None and not force and os.environ.get("COURSE_UNLOCK_ALL") != "1":
        nxt = next_lesson(state)
        ui.console.print(f"🔒 the final opens when all lessons are passed. Next: {nxt.id} {nxt.title}.")
        return
    rng = random.Random(seed)
    items = final_items(rng, n)
    ui.console.print(ui.Panel(
        f"FUNDAMENTALS FINAL — {len(items)} questions from every unit, {minutes:.0f} minutes, graded out "
        f"of 30. ≥ {FINAL_PASS} unlocks the general course. One attempt per numeric question, no hints.",
        border_style="red"))
    ui.pause("Enter = start the clock")
    deadline = time.time() + minutes * 60
    right = 0
    try:
        for k, (kind, item) in enumerate(items, 1):
            left = deadline - time.time()
            if left <= 0:
                ui.console.print("[red]time is up[/]")
                break
            ui.console.print(f"[dim]time left {int(left // 60)}:{int(left % 60):02d}[/]")
            label = f"({k}/{len(items)}) "
            if kind == "gen":
                ex = item.make(rng)
                ex.hint = "(no hints in the final)"
                ok = ui.run_exercise(ex, state, label, attempts=1)
            elif item.kind == "mcq":
                ok = ui.run_mcq(ui.shuffled(to_mcq(item), rng), state, label)
            else:
                ex = to_exercise(item)
                ex.hint = "(no hints in the final)"
                ok = ui.run_exercise(ex, state, label, attempts=1)
            if time.time() > deadline:
                ui.console.print("[red]answered after the deadline — not counted[/]")
                break
            right += ok
    except ui.Quit:
        pass
    grade = 30 * right / len(items)
    passed = grade >= FINAL_PASS
    fs["finals"].append({"date": date.today().isoformat(), "right": right, "total": len(items),
                         "grade": round(grade, 1)})
    if passed:
        fs["final_passed"] = True
    ui.save(state)
    label = "30 e lode" if right == len(items) else f"{grade:.0f}/30"
    ui.console.print(ui.Panel(
        f"{right}/{len(items)} → [bold]{label}[/] · " +
        ("[green]PASSED — the general course is now unlocked.[/]" if passed
         else "[red]NOT PASSED[/] — review weak units (`f practice`, `review`) and retry."),
        title="Fundamentals final", border_style="red"))


def selftest_problems() -> tuple[list[str], dict]:
    problems: list[str] = []
    ids: set[str] = set()
    words = 0
    n_ex = 0
    for unit in units():
        if not unit.lessons:
            problems.append(f"unit {unit.id} has no lessons")
        for x in unit.lessons:
            if x.id in ids:
                problems.append(f"duplicate lesson {x.id}")
            ids.add(x.id)
            if not x.id.startswith(unit.id + "."):
                problems.append(f"lesson {x.id} filed under {unit.id}")
            w = len(x.body.split())
            words += w
            if w < 55:
                problems.append(f"{x.id} body is short ({w} words)")
            if len(x.exercises) < 3:
                problems.append(f"{x.id} has {len(x.exercises)} exercises (< 3)")
            for fx in x.exercises:
                n_ex += 1
                if fx.kind == "num":
                    if fx.answer is None or not math.isfinite(fx.answer):
                        problems.append(f"{fx.id} has no numeric answer")
                    elif any(to_exercise(fx).matches(v) for v in fx.traps):
                        problems.append(f"{fx.id} has a trap equal to the answer")
                else:
                    if len(fx.options) < 2 or fx.correct >= len(fx.options):
                        problems.append(f"{fx.id} has bad options")
                    if sum(1 for o in fx.options if o) != len(fx.options):
                        problems.append(f"{fx.id} has an empty option")
                if not fx.solution:
                    problems.append(f"{fx.id} has no solution/explanation")
    stats = {"units": len(units()), "lessons": len(ids), "words": words, "exercises": n_ex}
    return problems, stats
