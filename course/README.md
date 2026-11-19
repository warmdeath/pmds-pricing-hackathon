# Markets, Economics & Finance — crash course

A terminal trainer that covers roughly the economics and finance content of a
first university semester in economics and management. It has four modules and
30 lessons, about 20,000 words in total. You get unlimited auto-checked exercises,
concept quizzes, timed exams graded out of 30, spaced repetition and a glossary.

It sits next to the practice arena (`arena/`), and its **mechanics map** shows
where each concept appears in the DME simulator. The map states facts only:
what the mechanic is and where it is defined. It never says what an agent should
do. The lessons teach general theory with textbook examples (bakeries, oil,
bonds, used cars), not strategy for your agent.

## Run it

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
| `course/run.sh selftest` | Content integrity checks |

Type `q` to go back or quit from anywhere. Numeric answers accept `12.5`,
`-0.8`, `25%` and `3/4`. Your progress is saved in `course/.progress.json`,
which git ignores.

## Syllabus

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

## A suggested pace

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
- Files: lessons in `content/`, concept questions in `questions.py`, exercise
  generators in `generators.py`, glossary in `glossary.py`, mechanics map in
  `simmap.py`, syllabus in `syllabus.py`, engine in `trainer.py`.
