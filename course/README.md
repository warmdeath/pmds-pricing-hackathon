# Markets, Economics & Finance — crash course

A terminal trainer in two sections. **Fundamentals** (200 micro-lessons, done
first) builds the statistics, economic reasoning and accounting/finance basics.
The **general course** (4 modules, 30 lessons, about 20,000 words) then covers
roughly the economics and finance content of a first university semester. You get unlimited auto-checked exercises,
concept quizzes, timed exams graded out of 30, spaced repetition and a glossary.

It sits next to the practice arena (`arena/`), and its **mechanics map** shows
where each concept appears in the DME simulator. The map states facts only:
what the mechanic is and where it is defined. It never says what an agent should
do. The lessons teach general theory with textbook examples (bakeries, oil,
bonds, used cars), not strategy for your agent.

## Browser version (recommended): Margin Notes

The same course in the browser, with interactive charts in the graph-heavy lessons
(supply and demand with a tax, elasticity and revenue, cost curves, break-even,
compounding and discounting, skew, normal probabilities, binomial/Poisson, the
central limit theorem, regression, logit shares, monopoly, auction bid shading,
diversification, newsvendor). It applies the same rules: lessons unlock in order,
mastery checks need at least 75 %, and the Fundamentals final unlocks the general
course.

- **Published page** (laptop and phone):
  https://claude.ai/artifact/Fy1XmEDNyKsrTZhTrzEcKG. It is private to your account.
  Progress is saved there and syncs between devices; on the phone, use
  **Review** for 5-minute sessions.
- **Local** (offline, laptop only): run the command below and open
  http://localhost:8765. Progress is then stored in that browser only.

```bash
course/run.sh web
```

- **Moving progress over:** the Progress page has a box for pasting
  `course/.progress.json` from the terminal trainer, which merges it in.
- **How it is built:** `course/web/build.py` exports the lesson files,
  questions and glossary to `dist/data.json`. Python exercise generators can't
  run in the browser, so it samples about 3,800 concrete practice exercises from
  them. `course/web/app.html` is the app. After editing lessons, re-run the build
  (and republish the page).

## Start here: Fundamentals

Fundamentals is a separate section of **200 micro-lessons in 18 units**, built
from a high-school level up. It covers what a first-year economics student uses
everywhere: **probability & statistics**, **economic & business reasoning**,
and **accounting & financial literacy**. It is the first thing to do: the
general course stays **locked** until you pass the Fundamentals final.

| unit | track | topic | unit | track | topic |
| --- | --- | --- | --- | --- | --- |
| F1 | Reasoning | Thinking like an economist | F10 | Accounting & finance | Financial statements |
| F2 | Reasoning | The numbers of economics | F11 | Reasoning | Business decisions |
| F3 | Reasoning | Reading graphs and data | F12 | Statistics | Random variables & distributions |
| F4 | Statistics | Describing data | F13 | Accounting & finance | Investment & financing |
| F5 | Reasoning | Markets and prices | F14 | Accounting & finance | Analysing statements |
| F6 | Reasoning | Revenue, cost and profit | F15 | Statistics | Sampling & inference |
| F7 | Accounting & finance | Accounting foundations | F16 | Statistics | Correlation & regression |
| F8 | Accounting & finance | Money and interest | F17 | Statistics | Statistics at work |
| F9 | Statistics | Probability | F18 | Mixed | Capstone business cases |

The units interleave the three tracks so each one builds on the previous ones.
For example, descriptive statistics (F4) comes before the cost analysis in F6,
and interest (F8) comes before investment appraisal (F13).

**How it works**

- Every lesson is one concept: an explanation, a worked example and a
  **mastery check** of 3–4 questions (617 in total).
- You pass a lesson with **at least 75 %** of its check. With 3 questions that
  means all 3; with 4 questions, 3 of 4. Numeric questions allow a second
  attempt and a hint. Choosing "show solution" counts as wrong.
- Lessons open **in order**: passing one unlocks the next. You can re-read
  and retake any lesson you have unlocked.
- `f practice` gives unlimited auto-generated exercises on everything you
  have unlocked. There are 83 exercise types across all 18 units.
- When all 200 lessons are passed, `f final` opens: 30 questions drawn from
  every unit, 90 minutes, graded out of 30. **18 or more unlocks the general
  course.** You can retake the final.
- Lessons and exercises you miss feed the spaced-repetition `review`.

```bash
course/run.sh f
```

```bash
course/run.sh f next
```

| Command | What it does |
| --- | --- |
| `course/run.sh f` | Overview of the 18 units and your progress |
| `course/run.sh f next` | Read the next lesson, then take its mastery check |
| `course/run.sh f unit F4` | List one unit's lessons and their status |
| `course/run.sh f learn F4.3` | Re-read an unlocked lesson (`--no-pause` prints it without the check) |
| `course/run.sh f check F4.3` | Retake a lesson's mastery check |
| `course/run.sh f practice [F4 \| F4.3]` | Unlimited exercises on unlocked material |
| `course/run.sh f final` | The Fundamentals final (opens when all lessons are passed) |

In the interactive menu (`course/run.sh`) Fundamentals is option **0**. The
locked general-course options are marked 🔒. The glossary, review and progress
stay available throughout.

## The general course (unlocks after Fundamentals)

### Run it

From the repository root (WSL / Linux / macOS), after `uv sync`:

```bash
course/run.sh
```

| Command | What it does |
| --- | --- |
| `course/run.sh` | Interactive menu |
| `course/run.sh syllabus` | Modules, lessons, what you've read, accuracy per lesson |
| `course/run.sh learn 1.3` | Read a lesson section by section, then answer its check questions |
| `course/run.sh learn 1.3 --no-pause` | Print the whole lesson at once |
| `course/run.sh practice [1.3 \| M2]` | Unlimited numeric exercises with hints, worked solutions and diagnosis of typical mistakes |
| `course/run.sh quiz [M1 \| 2.5] [--count N]` | Concept questions (multiple choice) |
| `course/run.sh exam [--minutes 60] [--questions 20] [--module M3]` | Timed mixed exam graded out of 30 (pass ≥ 18, *30 e lode* if all correct) |
| `course/run.sh review` | Spaced repetition: items you missed come back after 0, 1, 3, 7, 16 days |
| `course/run.sh glossary [term]` | About 200 terms with definitions, formulas, examples and where they appear in the simulator |
| `course/run.sh map` | Mechanics map: concept → mechanic → file or README section |
| `course/run.sh progress` | Lessons read, accuracy, weakest lessons, exam history |
| `course/run.sh selftest` | Content integrity checks (both sections) |

Type `q` to go back or quit from anywhere. Numeric answers accept `12.5`,
`-0.8`, `25%` and `3/4`. Your progress is saved in `course/.progress.json`,
which git ignores.

### Syllabus

**M1 Microeconomics.**
- 1.1 Scarcity, opportunity cost and marginal thinking
- 1.2 Supply and demand
- 1.3 Elasticity
- 1.4 Welfare, taxes and price controls
- 1.5 Consumer theory and willingness to pay
- 1.6 Production and costs
- 1.7 Perfect competition
- 1.8 Monopoly and price discrimination
- 1.9 Product differentiation and logit demand
- 1.10 Market failures and information

**M2 Game theory & auctions.**
- 2.1 Nash equilibrium
- 2.2 Mixed strategies and sequential games
- 2.3 Oligopoly: Cournot, Bertrand, Stackelberg, collusion
- 2.4 Repeated games and end-game effects
- 2.5 Auction formats and bid shading
- 2.6 Multi-unit auctions, reserve prices, winner's curse
- 2.7 Decisions under uncertainty, newsvendor, learning

**M3 Accounting & finance.**
- 3.1 Balance sheet
- 3.2 Income statement
- 3.3 Cash flow, working capital, inventory
- 3.4 Managerial accounting: break-even and scarce resources
- 3.5 Time value of money: NPV, IRR
- 3.6 Risk, return, CAPM
- 3.7 Bonds, stocks, market efficiency

**M4 Macroeconomics.**
- 4.1 GDP
- 4.2 Money and inflation
- 4.3 Unemployment and cycles
- 4.4 AD-AS and fiscal policy
- 4.5 Monetary policy
- 4.6 Trade and exchange rates

Each lesson has a big-picture intro, an analogy, worked numerical examples,
common pitfalls and a summary.

### A suggested pace

About 2–3 lessons a day:

1. `learn` the lesson.
2. Do `practice <id>` until you get 5 right in a row.
3. Start every session with `review`.
4. At the end of each module, take `exam --module Mx`.

M1 and M2 are the closest to the competition. M3 covers cash, inventory and
the time value of money. M4 is general background.

## Notes

- This is a self-study crash course written for this repository. It is not an
  official syllabus and it does not replace a textbook. Standard references
  for going deeper: Pindyck & Rubinfeld or Varian (micro), Dixit & Skeath (games),
  Krishna (auctions), Berk & DeMarzo (finance), Blanchard (macro).
- Tests: `uv run python -m unittest discover -s course/tests`. Setting
  `COURSE_UNLOCK_ALL=1` bypasses the lock; it exists for testing.
- Fundamentals files: lessons in `fundamentals/uNN_*.md` (lesson text plus
  mastery exercises in a simple format described in `fundamentals.py`),
  practice generators in `fgenerators.py`.
- General course files: lessons in `content/`, concept questions in `questions.py`, exercise
  generators in `generators.py`, glossary in `glossary.py`, mechanics map in
  `simmap.py`, syllabus in `syllabus.py`, engine in `trainer.py`.
