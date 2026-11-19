"""Economics & finance crash course -- terminal trainer.

    course/run.sh                 interactive menu
    course/run.sh syllabus        list modules and lessons
    course/run.sh learn 1.3       read a lesson, then answer its check questions
    course/run.sh practice [1.3]  unlimited auto-checked numeric exercises
    course/run.sh quiz [M2]       10 concept questions (all or one module)
    course/run.sh exam [--minutes 60]   timed mixed exam graded out of 30
    course/run.sh review          spaced-repetition review of missed items
    course/run.sh glossary [term] search the glossary
    course/run.sh map             where each concept appears in the simulator
    course/run.sh progress        your stats
    course/run.sh selftest        integrity checks of the course content
"""

from __future__ import annotations

import argparse
import json
import math
import os
import random
import sys
import time
from datetime import date, timedelta
from pathlib import Path

sys.dont_write_bytecode = True
HERE = Path(__file__).resolve().parent
sys.path.insert(0, str(HERE))

from rich.console import Console  # noqa: E402
from rich.markdown import Markdown  # noqa: E402
from rich.panel import Panel  # noqa: E402
from rich.table import Table  # noqa: E402

from generators import GENERATORS, Exercise  # noqa: E402
from glossary import GLOSSARY  # noqa: E402
from questions import QUESTIONS  # noqa: E402
from simmap import SIM_MAP  # noqa: E402
from syllabus import MODULES, lesson_by_id, all_lessons  # noqa: E402

console = Console(highlight=False)
STATE_FILE = Path(os.environ.get("COURSE_STATE", HERE / ".progress.json"))
LEITNER_DAYS = {1: 0, 2: 1, 3: 3, 4: 7, 5: 16}


# =============================================================================
# progress
# =============================================================================

def load_state() -> dict:
    if STATE_FILE.exists():
        try:
            return json.loads(STATE_FILE.read_text())
        except json.JSONDecodeError:
            pass
    return {"read": {}, "stats": {}, "cards": {}, "exams": []}


def save_state(state: dict) -> None:
    STATE_FILE.write_text(json.dumps(state, indent=1))


def record(state: dict, lesson_id: str, card_id: str, correct: bool) -> None:
    stats = state["stats"].setdefault(lesson_id, {"right": 0, "wrong": 0})
    stats["right" if correct else "wrong"] += 1
    card = state["cards"].get(card_id, {"box": 1, "due": date.today().isoformat()})
    if correct:
        card["box"] = min(5, card["box"] + 1)
    else:
        card["box"] = 1
    card["due"] = (date.today() + timedelta(days=LEITNER_DAYS[card["box"]])).isoformat()
    card["lesson"] = lesson_id
    state["cards"][card_id] = card
    save_state(state)


# =============================================================================
# input helpers
# =============================================================================

class Quit(Exception):
    pass


def ask(prompt: str) -> str:
    try:
        answer = console.input(f"[bold cyan]{prompt}[/] ").strip()
    except EOFError:
        raise Quit from None
    if answer.lower() in {"q", "quit", "exit"}:
        raise Quit
    return answer


def pause(message: str = "Enter = continue, q = back") -> None:
    ask(f"\n{message} ›")


def parse_number(text: str) -> float | None:
    cleaned = text.replace(",", "").replace("€", "").replace("$", "").replace(" ", "")
    percent = cleaned.endswith("%")
    cleaned = cleaned.rstrip("%")
    try:
        if "/" in cleaned:
            num, den = cleaned.split("/", 1)
            value = float(num) / float(den)
        else:
            value = float(cleaned)
    except (ValueError, ZeroDivisionError):
        return None
    return value / 100 if percent else value


def numbers_match(given: float, expected: float, ex: Exercise) -> bool:
    return ex.matches(given, expected)


# =============================================================================
# asking questions
# =============================================================================

def run_mcq(q: dict, state: dict, number: str = "") -> bool:
    letters = "abcdefgh"
    body = f"{number}{q['q']}\n\n" + "\n".join(
        f"  [bold]{letters[i]})[/] {opt}" for i, opt in enumerate(q["options"]))
    console.print(Panel(body, title=f"concept · lesson {q['lesson']}", border_style="blue"))
    while True:
        reply = ask("your answer (letter):").lower()
        if reply and reply[0] in letters[: len(q["options"])]:
            break
        console.print("type one of the letters shown, or q to stop")
    choice = letters.index(reply[0])
    correct = choice == q["answer"]
    if correct:
        console.print("[green]✔ correct.[/] " + q["why"])
    else:
        console.print(f"[red]✘ not quite.[/] The answer is [bold]{letters[q['answer']]})[/] "
                      f"{q['options'][q['answer']]}")
        trap = q.get("traps", {}).get(choice)
        if trap:
            console.print(f"[yellow]Why your choice is tempting but wrong:[/] {trap}")
        console.print("[dim]Explanation:[/] " + q["why"])
    record(state, q["lesson"], q["id"], correct)
    return correct


def run_exercise(ex: Exercise, state: dict, number: str = "", attempts: int = 2) -> bool:
    console.print(Panel(f"{number}{ex.prompt}", title=f"exercise · lesson {ex.lesson} · {ex.topic}",
                        border_style="magenta"))
    hint_shown = False
    for attempt in range(1, attempts + 1):
        while True:
            reply = ask("answer (number; 'h' = hint, 's' = show solution):")
            if reply.lower() == "h":
                console.print("[yellow]Hint:[/] " + ex.hint)
                hint_shown = True
                continue
            if reply.lower() == "s":
                console.print(Panel(ex.solution, title="worked solution", border_style="green"))
                record(state, ex.lesson, f"gen:{ex.topic}", False)
                return False
            value = parse_number(reply)
            if value is not None:
                break
            console.print("type a number (e.g. 12.5, -0.8, 25%, 3/4)")
        if numbers_match(value, ex.answer, ex):
            console.print(f"[green]✔ correct[/] ({ex.fmt(ex.answer)}{ex.unit})"
                          + (" — with a hint" if hint_shown else ""))
            console.print(Panel(ex.solution, title="worked solution", border_style="green"))
            record(state, ex.lesson, f"gen:{ex.topic}", True)
            return True
        diagnosis = ex.diagnose(value)
        if diagnosis:
            console.print(f"[red]✘[/] [yellow]Likely mistake:[/] {diagnosis}")
        else:
            console.print("[red]✘ not correct.[/]")
        if attempt < attempts:
            console.print("try once more (or 'h' for a hint).")
    console.print(f"The answer is [bold]{ex.fmt(ex.answer)}{ex.unit}[/].")
    console.print(Panel(ex.solution, title="worked solution", border_style="green"))
    record(state, ex.lesson, f"gen:{ex.topic}", False)
    return False


# =============================================================================
# commands
# =============================================================================

def cmd_syllabus(_args=None, state=None) -> None:
    state = state or load_state()
    for module in MODULES:
        table = Table(title=f"{module['id']} · {module['title']}", title_justify="left",
                      show_header=True, header_style="bold")
        table.add_column("lesson", justify="right")
        table.add_column("title")
        table.add_column("read", justify="center")
        table.add_column("exercises", justify="right")
        table.add_column("accuracy", justify="right")
        for lesson in module["lessons"]:
            stats = state["stats"].get(lesson["id"], {"right": 0, "wrong": 0})
            total = stats["right"] + stats["wrong"]
            acc = f"{100 * stats['right'] / total:.0f}% ({total})" if total else "-"
            gens = len([g for g in GENERATORS if g.lesson == lesson["id"]])
            table.add_row(lesson["id"], lesson["title"],
                          "✔" if lesson["id"] in state["read"] else "", str(gens) if gens else "-", acc)
        console.print(table)
    console.print("[dim]learn <id> to read · practice <id> for exercises · quiz / exam / review[/]")


def cmd_learn(lesson_id: str | None, state: dict, interactive: bool = True) -> None:
    if lesson_id is None:
        cmd_syllabus(state=state)
        lesson_id = ask("lesson id (e.g. 1.3):")
    lesson = lesson_by_id(lesson_id)
    if lesson is None:
        console.print(f"no lesson {lesson_id!r}; see `syllabus`")
        return
    text = (HERE / "content" / lesson["file"]).read_text(encoding="utf-8")
    sections = _split_sections(text)
    for index, section in enumerate(sections, 1):
        console.print(Markdown(section))
        if interactive and index < len(sections):
            console.print(f"[dim]— section {index}/{len(sections)} —[/]")
            pause()
    related = [g for g in GLOSSARY if g.get("lesson") == lesson["id"]]
    if related:
        console.print(Markdown("### Key terms\n" + ", ".join(f"**{g['term']}**" for g in related)
                               + "\n\n`glossary <term>` for definitions; `map` shows where "
                                 "terms appear in the simulator."))
    state["read"][lesson["id"]] = date.today().isoformat()
    save_state(state)
    if not interactive:
        return
    questions = [q for q in QUESTIONS if q["lesson"] == lesson["id"]]
    if questions and ask("check your understanding now? [Y/n]").lower() != "n":
        right = 0
        rng = random.Random()
        for n, q in enumerate(questions, 1):
            right += run_mcq(_shuffled(q, rng), state, f"({n}/{len(questions)}) ")
        console.print(f"\n[bold]{right}/{len(questions)}[/] correct.")
        gens = [g for g in GENERATORS if g.lesson == lesson["id"]]
        if gens:
            console.print(f"`practice {lesson['id']}` gives unlimited exercises on this lesson.")


def _split_sections(text: str) -> list[str]:
    parts: list[str] = []
    current: list[str] = []
    for line in text.splitlines():
        if line.startswith("## ") and current:
            parts.append("\n".join(current))
            current = []
        current.append(line)
    if current:
        parts.append("\n".join(current))
    return parts


def _pick_generators(selector: str | None):
    if not selector:
        return list(GENERATORS)
    sel = selector.upper()
    if sel.startswith("M"):
        return [g for g in GENERATORS if g.lesson.split(".")[0] == sel[1:]]
    return [g for g in GENERATORS if g.lesson == selector or g.topic == selector]


def cmd_practice(selector: str | None, state: dict, count: int | None = None, seed: int | None = None) -> None:
    pool = _pick_generators(selector)
    if not pool:
        console.print(f"no exercises for {selector!r}. Lessons with exercises: "
                      + ", ".join(sorted({g.lesson for g in GENERATORS}, key=_lesson_key)))
        return
    rng = random.Random(seed)
    right = done = 0
    console.print(f"[bold]Practice[/] — {len(pool)} exercise type(s). q = stop.")
    try:
        while count is None or done < count:
            gen = rng.choice(pool)
            ex = gen.make(rng)
            done += 1
            right += run_exercise(ex, state, f"#{done}  ")
    except Quit:
        pass
    if done:
        console.print(f"\nsession: {right}/{done} correct")


def cmd_quiz(selector: str | None, state: dict, count: int = 10, seed: int | None = None) -> None:
    pool = QUESTIONS
    if selector:
        sel = selector.upper()
        if sel.startswith("M"):
            pool = [q for q in QUESTIONS if q["lesson"].split(".")[0] == sel[1:]]
        else:
            pool = [q for q in QUESTIONS if q["lesson"] == selector]
    if not pool:
        console.print("no questions match")
        return
    rng = random.Random(seed)
    chosen = rng.sample(pool, min(count, len(pool)))
    right = 0
    try:
        for n, q in enumerate(chosen, 1):
            right += run_mcq(_shuffled(q, rng), state, f"({n}/{len(chosen)}) ")
    except Quit:
        pass
    console.print(f"\nquiz: [bold]{right}/{len(chosen)}[/]")


def _shuffled(q: dict, rng: random.Random) -> dict:
    order = list(range(len(q["options"])))
    if q.get("fixed_order"):
        return q
    rng.shuffle(order)
    new = dict(q)
    new["options"] = [q["options"][i] for i in order]
    new["answer"] = order.index(q["answer"])
    new["traps"] = {order.index(k): v for k, v in q.get("traps", {}).items()}
    return new


def cmd_exam(state: dict, minutes: float = 60, questions: int = 20, seed: int | None = None,
             module: str | None = None) -> None:
    rng = random.Random(seed)
    mcq_pool = QUESTIONS if not module else [q for q in QUESTIONS if q["lesson"].split(".")[0] == module.upper().lstrip("M")]
    gen_pool = _pick_generators(module.upper() if module else None)
    n_num = min(questions // 2, len(gen_pool) * 3) if gen_pool else 0
    n_mcq = questions - n_num
    items = [("mcq", _shuffled(q, rng)) for q in rng.sample(mcq_pool, min(n_mcq, len(mcq_pool)))]
    items += [("num", rng.choice(gen_pool).make(rng)) for _ in range(n_num)]
    rng.shuffle(items)
    console.print(Panel(
        f"{len(items)} questions · {minutes:.0f} minutes · graded out of 30 (pass ≥ 18, 30 e lode = all "
        "correct).\nNumeric questions allow one attempt, no hints. Unanswered questions after the "
        "deadline score zero.", title="EXAM", border_style="red"))
    pause("Enter = start the clock")
    deadline = time.time() + minutes * 60
    right = 0
    answered = 0
    try:
        for n, (kind, item) in enumerate(items, 1):
            left = deadline - time.time()
            if left <= 0:
                console.print("[red]time is up.[/]")
                break
            console.print(f"[dim]time left {int(left // 60)}:{int(left % 60):02d}[/]")
            if kind == "mcq":
                ok = run_mcq(item, state, f"({n}/{len(items)}) ")
            else:
                item.hint = "(no hints during the exam)"
                ok = run_exercise(item, state, f"({n}/{len(items)}) ", attempts=1)
            if time.time() > deadline:
                console.print("[red]answered after the deadline — not counted.[/]")
                break
            answered += 1
            right += ok
    except Quit:
        pass
    grade = 30 * right / len(items) if items else 0
    label = "30 e lode" if items and right == len(items) else f"{grade:.0f}/30"
    verdict = "PASSED" if grade >= 18 else "NOT PASSED"
    console.print(Panel(f"{right}/{len(items)} correct ({answered} answered) → [bold]{label}[/] · {verdict}",
                        title="exam result", border_style="red"))
    state["exams"].append({"date": date.today().isoformat(), "right": right, "total": len(items),
                           "grade": round(grade, 1)})
    save_state(state)


def cmd_review(state: dict, limit: int = 15, seed: int | None = None) -> None:
    today = date.today().isoformat()
    due = [cid for cid, card in state["cards"].items() if card["due"] <= today and card["box"] < 5]
    if not due:
        console.print("nothing due. Items you miss come back here (spaced repetition: 0, 1, 3, 7, 16 days).")
        return
    rng = random.Random(seed)
    rng.shuffle(due)
    by_id = {q["id"]: q for q in QUESTIONS}
    gens = {f"gen:{g.topic}": g for g in GENERATORS}
    console.print(f"[bold]Review[/] — {len(due)} item(s) due; doing up to {limit}.")
    done = 0
    try:
        for cid in due[:limit]:
            done += 1
            if cid in by_id:
                run_mcq(_shuffled(by_id[cid], rng), state, f"[{done}] ")
            elif cid in gens:
                run_exercise(gens[cid].make(rng), state, f"[{done}] ")
    except Quit:
        pass


def cmd_glossary(term: str | None, state: dict | None = None) -> None:
    if not term:
        table = Table(title="Glossary", show_header=True, header_style="bold")
        table.add_column("term")
        table.add_column("lesson", justify="right")
        table.add_column("definition")
        for g in sorted(GLOSSARY, key=lambda g: g["term"].lower()):
            table.add_row(g["term"], g.get("lesson", ""), _short(g["definition"]))
        console.print(table)
        console.print("[dim]glossary <word> shows the full entry[/]")
        return
    needle = term.lower()
    hits = [g for g in GLOSSARY if needle in g["term"].lower()]
    if not hits:
        hits = [g for g in GLOSSARY if needle in g["definition"].lower()]
    if not hits:
        console.print(f"no entry for {term!r}")
        return
    for g in hits[:8]:
        body = g["definition"]
        if g.get("example"):
            body += f"\n\n[bold]Example:[/] {g['example']}"
        if g.get("formula"):
            body += f"\n\n[bold]Formula:[/] {g['formula']}"
        sims = [m for m in SIM_MAP if g["term"] in m.get("terms", [])]
        for m in sims:
            body += f"\n\n[bold]In the simulator:[/] {m['mechanic']} [dim]({m['where']})[/]"
        console.print(Panel(body, title=f"{g['term']}  ·  lesson {g.get('lesson', '-')}",
                            border_style="cyan"))


def _short(text: str, width: int = 90) -> str:
    return text if len(text) <= width else text[: width - 1] + "…"


def cmd_map() -> None:
    console.print(Panel(
        "Each row names an economic concept and states, as a fact, where the corresponding mechanic "
        "lives in the simulator (README section or source function). It does not say what to do "
        "about it — drawing conclusions is your job.", title="Mechanics map", border_style="yellow"))
    table = Table(show_header=True, header_style="bold", show_lines=True)
    table.add_column("concept (lesson)")
    table.add_column("mechanic in the simulator")
    table.add_column("where")
    for m in SIM_MAP:
        table.add_row(f"{m['concept']} ({m['lesson']})", m["mechanic"], m["where"])
    console.print(table)


def cmd_progress(state: dict) -> None:
    lessons = all_lessons()
    read = len([lesson for lesson in lessons if lesson["id"] in state["read"]])
    right = sum(s["right"] for s in state["stats"].values())
    wrong = sum(s["wrong"] for s in state["stats"].values())
    console.print(f"lessons read: [bold]{read}/{len(lessons)}[/]   answers: {right + wrong} "
                  f"({100 * right / max(1, right + wrong):.0f}% correct)")
    boxes = {b: 0 for b in range(1, 6)}
    for card in state["cards"].values():
        boxes[card["box"]] += 1
    console.print("spaced-repetition boxes (1 = shaky … 5 = mastered): "
                  + "  ".join(f"{b}:{n}" for b, n in boxes.items()))
    weak = sorted(((s["right"] / (s["right"] + s["wrong"]), lid) for lid, s in state["stats"].items()
                   if s["right"] + s["wrong"] >= 3))[:5]
    if weak:
        console.print("weakest lessons: " + ", ".join(f"{lid} ({100 * acc:.0f}%)" for acc, lid in weak))
    if state["exams"]:
        console.print("exams: " + ", ".join(f"{e['date']} {e['grade']:.0f}/30" for e in state["exams"][-5:]))


def cmd_selftest() -> int:
    problems: list[str] = []
    ids = {lesson["id"] for lesson in all_lessons()}
    for lesson in all_lessons():
        path = HERE / "content" / lesson["file"]
        if not path.exists():
            problems.append(f"missing lesson file {path}")
        elif len(path.read_text().split()) < 300:
            problems.append(f"lesson {lesson['id']} is short")
    seen = set()
    for q in QUESTIONS:
        if q["id"] in seen:
            problems.append(f"duplicate question id {q['id']}")
        seen.add(q["id"])
        if q["lesson"] not in ids:
            problems.append(f"question {q['id']} has unknown lesson {q['lesson']}")
        if not 0 <= q["answer"] < len(q["options"]):
            problems.append(f"question {q['id']} answer out of range")
        for k in q.get("traps", {}):
            if not 0 <= k < len(q["options"]) or k == q["answer"]:
                problems.append(f"question {q['id']} has a bad trap index {k}")
    for g in GLOSSARY:
        if g.get("lesson") and g["lesson"] not in ids:
            problems.append(f"glossary {g['term']} unknown lesson")
    terms = {g["term"] for g in GLOSSARY}
    for m in SIM_MAP:
        for t in m.get("terms", []):
            if t not in terms:
                problems.append(f"map entry {m['concept']} references unknown term {t!r}")
        if m["lesson"] not in ids:
            problems.append(f"map entry {m['concept']} unknown lesson")
    rng = random.Random(0)
    for g in GENERATORS:
        if g.lesson not in ids:
            problems.append(f"generator {g.topic} unknown lesson")
        for _ in range(200):
            ex = g.make(rng)
            if not isinstance(ex.answer, float | int) or not math.isfinite(ex.answer):
                problems.append(f"generator {g.topic} produced a non-finite answer")
                break
            for wrong in ex.traps:
                if numbers_match(wrong, ex.answer, ex):
                    problems.append(f"generator {g.topic}: a trap equals the answer ({ex.prompt[:60]}…)")
                    break
    words = sum(len((HERE / "content" / lesson["file"]).read_text().split()) for lesson in all_lessons()
                if (HERE / "content" / lesson["file"]).exists())
    console.print(f"{len(all_lessons())} lessons ({words:,} words), {len(QUESTIONS)} concept questions, "
                  f"{len(GENERATORS)} exercise generators, {len(GLOSSARY)} glossary terms, "
                  f"{len(SIM_MAP)} mechanics-map entries")
    if problems:
        for p in problems[:50]:
            console.print(f"[red]✘[/] {p}")
        return 1
    console.print("[green]all checks passed[/]")
    return 0


def _lesson_key(lid: str):
    a, b = lid.split(".")
    return int(a), int(b)


# =============================================================================
# interactive menu
# =============================================================================

MENU = [
    ("1", "Syllabus", "all modules and lessons, with your progress"),
    ("2", "Learn", "read a lesson, then check questions"),
    ("3", "Practice", "unlimited auto-checked numeric exercises"),
    ("4", "Quiz", "10 concept questions"),
    ("5", "Exam", "timed mixed exam graded out of 30"),
    ("6", "Review", "spaced repetition of what you missed"),
    ("7", "Glossary", "look up a term"),
    ("8", "Mechanics map", "where concepts appear in the simulator"),
    ("9", "Progress", "your statistics"),
]


def menu() -> None:
    state = load_state()
    console.print(Panel(
        "[bold]Markets, Economics & Finance — crash course[/]\n"
        "Microeconomics · Game theory & auctions · Accounting & finance · Macroeconomics\n"
        "[dim]q goes back / quits from anywhere[/]", border_style="green"))
    while True:
        table = Table(show_header=False, box=None)
        for key, name, desc in MENU:
            table.add_row(f"[bold]{key}[/]", name, f"[dim]{desc}[/]")
        console.print(table)
        try:
            choice = ask("choose:")
        except Quit:
            console.print("bye — keep going!")
            return
        try:
            if choice == "1":
                cmd_syllabus(state=state)
            elif choice == "2":
                cmd_learn(None, state)
            elif choice == "3":
                sel = ask("lesson id or module (e.g. 1.3, M2; Enter = everything):") or None
                cmd_practice(sel, state)
            elif choice == "4":
                sel = ask("module (M1..M4) or lesson id; Enter = everything:") or None
                cmd_quiz(sel, state)
            elif choice == "5":
                cmd_exam(state)
            elif choice == "6":
                cmd_review(state)
            elif choice == "7":
                cmd_glossary(ask("term (Enter = list all):") or None)
            elif choice == "8":
                cmd_map()
            elif choice == "9":
                cmd_progress(state)
        except Quit:
            continue


def main() -> int:
    parser = argparse.ArgumentParser(prog="course/run.sh", description=__doc__,
                                     formatter_class=argparse.RawDescriptionHelpFormatter)
    sub = parser.add_subparsers(dest="cmd")
    sub.add_parser("syllabus")
    p = sub.add_parser("learn")
    p.add_argument("lesson", nargs="?")
    p.add_argument("--no-pause", action="store_true", help="print the whole lesson, no questions")
    p = sub.add_parser("practice")
    p.add_argument("selector", nargs="?")
    p.add_argument("--count", type=int)
    p.add_argument("--seed", type=int)
    p = sub.add_parser("quiz")
    p.add_argument("selector", nargs="?")
    p.add_argument("--count", type=int, default=10)
    p.add_argument("--seed", type=int)
    p = sub.add_parser("exam")
    p.add_argument("--minutes", type=float, default=60)
    p.add_argument("--questions", type=int, default=20)
    p.add_argument("--module")
    p.add_argument("--seed", type=int)
    p = sub.add_parser("review")
    p.add_argument("--limit", type=int, default=15)
    p = sub.add_parser("glossary")
    p.add_argument("term", nargs="*")
    sub.add_parser("map")
    sub.add_parser("progress")
    sub.add_parser("selftest")
    args = parser.parse_args()

    state = load_state()
    try:
        if args.cmd is None:
            menu()
        elif args.cmd == "syllabus":
            cmd_syllabus(state=state)
        elif args.cmd == "learn":
            cmd_learn(args.lesson, state, interactive=not args.no_pause)
        elif args.cmd == "practice":
            cmd_practice(args.selector, state, args.count, args.seed)
        elif args.cmd == "quiz":
            cmd_quiz(args.selector, state, args.count, args.seed)
        elif args.cmd == "exam":
            cmd_exam(state, args.minutes, args.questions, args.seed, args.module)
        elif args.cmd == "review":
            cmd_review(state, args.limit)
        elif args.cmd == "glossary":
            cmd_glossary(" ".join(args.term) or None)
        elif args.cmd == "map":
            cmd_map()
        elif args.cmd == "progress":
            cmd_progress(state)
        elif args.cmd == "selftest":
            return cmd_selftest()
    except Quit:
        pass
    return 0


if __name__ == "__main__":
    sys.exit(main())
