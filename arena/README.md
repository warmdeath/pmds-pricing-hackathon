# PMDS Pricing Hackathon — Practice Arena

> ## ⚠️ SPOILER WARNING — read this first
>
> This arena re-creates the hackathon day so you can play it on your own.
> **During your attempt, do NOT open:**
>
> - `arena/opponents/` — the 39 rival teams' code;
> - `arena/configs/final_*.yaml` — the held-out evaluation scenarios;
> - `arena/tools/gen_opponents.py`, `arena/tools/make_finals.py`,
>   `arena/tools/roster_spoiler.py` — the files that generate them.
>
> Everything else (this README, `run.sh`, `practice.yaml`, the portal and
> report tools, the tests) is safe to read. On the real day you could not read
> other teams' code or the private scenarios either.

You write **your own agent**. The arena adds the parts of the event you cannot
get from the public repository alone: 39 rival teams, held-out scenarios, the
upload portal with its validation, the leaderboard, the 5-hour clock, and a
facts-only feedback report after each practice run. It contains no strategy
advice.

---

## 1. Setup (Windows + WSL)

The arena uses `bash` and the Unix decision timer, so on Windows run it inside
WSL (the repository README lists WSL as a supported alternative).

1. Install WSL with Ubuntu, from **PowerShell as Administrator**, then reboot
   and open the *Ubuntu* app:

   ```powershell
   wsl --install -d Ubuntu
   ```

2. Inside Ubuntu, install Git and uv (same commands as the repository README,
   section 1.2, Ubuntu / Debian), then reopen the terminal:

   ```bash
   sudo apt-get update
   sudo apt-get install -y git curl ca-certificates
   curl -LsSf https://astral.sh/uv/install.sh | sh
   ```

3. Clone **inside the Linux home folder** (much faster than under `/mnt/c`),
   switch to the arena branch and install the locked dependencies:

   ```bash
   cd ~
   git clone https://github.com/YOUR-USERNAME/pmds-pricing-hackathon.git
   cd pmds-pricing-hackathon
   git checkout arena
   uv sync --locked --python 3.12
   ```

4. Check that everything works (about 40 s):

   ```bash
   arena/run.sh selftest
   ```

Run every command from the repository root. To edit in VS Code on Windows,
run `code .` from that folder in WSL (with the *WSL* extension installed).

## 2. Your agent

Your agent lives in `src/dme_simulator/agents/my_agent/agent.py`. It starts as
the README starter agent, unchanged. Edit it, add helper files in the same
folder, or create another folder and pass its path to the commands below.
The folder name is your team name on the leaderboard. Everything in the
repository README still applies (`uv run dme-sim …`, the window UI, recordings).

## 3. Commands

| Command | What it does |
| --- | --- |
| `arena/run.sh clock start` | Starts the 5-hour hackathon (shown as 14:00 → 19:00). |
| `arena/run.sh clock` | Shows the virtual time, a progress bar and the time left. |
| `arena/run.sh clock reset` | Discards the clock (to start a new attempt). |
| `arena/run.sh practice [AGENT_DIR] [--seed N] [--turns N] [--config YAML]` | One match on `arena/configs/practice.yaml` against the 39 rivals, then the feedback report. |
| `arena/run.sh submit [AGENT_DIR or ZIP] [--max-workers N]` | Portal validation; if it passes, the evaluation on the held-out scenarios and the leaderboard. |
| `arena/run.sh leaderboard` | The leaderboard of your latest counted submission, plus a cash-over-turns plot. |
| `arena/run.sh dashboards [AGENT_DIR] [--simulations N] [--seed N] [--max-workers N] [--turns N]` | The simulator's own batch mode on the practice scenario: mean-curve dashboards over N seeds. |
| `arena/run.sh selftest` | The arena's own tests. |

`AGENT_DIR` defaults to `src/dme_simulator/agents/my_agent`.

### practice

```bash
arena/run.sh practice
arena/run.sh practice --seed 7
```

Runs the unmodified simulator CLI
(`--config arena/configs/practice.yaml --agents-dir arena/opponents --extra-agent <your agent> --ui none --record …`)
and prints a report about **your** agent only. Facts, no advice:

- final cash, rank of 40, field reference points, stock left at the end;
- decide time (mean / max) and any timeout or rejected decision, per turn;
- per turn: cash, change, auction spend, sales revenue, raw and finished stock;
- per material and turn: units offered, reserve price, your bid units and price
  level(s), units won, price paid per unit, lowest/highest winning price of the market;
- per product and turn: units requested by your assembly orders, produced,
  listed, your listing price, sold, unsold, stock, your sale price, the
  market's average sale price, market units sold, unserved customers;
- totals per material and per product; final standings of the match.

Saved in `outputs/arena/practice/<timestamp>/`: `report.txt`, `my_turns.csv`,
`cash_curve.png`, the three simulator dashboards, and the recording
(`uv run dme-sim --replay …/simulation.jsonl` opens it in the window).

To see your sealed bids, the practice run wraps your agent in a pass-through
bundle that logs each decision and returns it unchanged (same team ID, same
random seed, same behaviour).

### submit

```bash
arena/run.sh submit
arena/run.sh submit path/to/my_team.zip
```

1. **Portal validation** (README section 1.5), in the portal's order: upload
   shape (one folder or one `.zip`), at most 64 files and 20 MiB, allowed
   extensions only (`.py` and the listed model formats), no hidden files, name
   and path rules, exactly one `agent.py` with every file inside its folder,
   UTF-8 and compilation of **every** Python file, then a disposable copy is
   imported, its single concrete `BaseAgent` subclass is constructed without
   arguments and plays **3 default-scenario turns** with **100 ms per
   decision** and a **10-second** total budget. Any failure rejects the upload
   and prints the reason.
2. The validated copy is stored in `arena/submissions/<id>/` and played in
   every evaluation match: 4 held-out scenarios × 8 seeds = **32 matches**,
   each a separate run of the simulator CLI with `--seed`.
3. The result is appended to `arena/submissions.csv` with a timestamp, and the
   leaderboard is shown.

A local folder you have run with `uv run dme-sim` usually contains
`__pycache__/`; like the real portal, the upload is then rejected. Remove it
before submitting:

```bash
find src/dme_simulator/agents/my_agent -name __pycache__ -prune -exec rm -rf {} +
```

(`arena/run.sh` itself never creates `__pycache__` in your folder.)

### leaderboard

All 40 teams: **rank | team name | final cash (mean across matches) | average
rank**, sorted by average rank, your row highlighted. The cash-over-turns plot
(one panel per evaluation scenario, mean over its seeds, your line
highlighted) is saved as `arena/submissions/<id>/leaderboard_cash.png`; the
path is printed.

## 4. Rules of the practice day

1. `arena/run.sh clock start` at the moment you begin. You have 5 hours
   (14:00 → 19:00).
2. Write your agent in your own folder. Do not read the spoiler files listed at
   the top. Your agent may use only its public inputs, its own memory and
   bundled files — not the simulator's internals, the recordings, other
   bundles or the scenario files.
3. Experiment with `practice` (and `uv run dme-sim` with any public config) as
   much as you like. Keep a lab notebook in `arena/EXPERIMENTS.md`.
4. Submit as often as you like. **Only your latest submission before the
   deadline counts.** Rejected uploads do not replace a valid one. Submissions
   after 19:00 are still validated and evaluated but marked `late` and do not
   count.
5. Score (README section 1.5): every (scenario, seed) is one match; each match
   ranks all 40 teams by **final cash** (inventory is worth nothing); your
   overall result is the arithmetic **mean of your ranks** across all matches,
   lower is better.
6. Simulation rules are the repository's (README section 2): sealed
   pay-your-bid auction, budget cap, production, sales to spawned customers,
   100 ms per decision (timeouts and invalid decisions become empty decisions).

To start a fresh attempt: `arena/run.sh clock reset`, then delete
`arena/submissions/` and `arena/submissions.csv`.

## 5. What is faithful and what is approximated

**Faithful (same as the real event)**

- The simulator: the unmodified repository code and CLI runs every match.
- The rules of README sections 1.5 and 2: 100 ms decision deadline (Unix
  interval timer), sealed pay-your-bid auction with the budget cap, final cash
  is the score, inventory is worth nothing, bankruptcy rules.
- 40 teams per match; scoring by mean rank over all (scenario, seed) matches;
  only the latest submission before the deadline counts.
- The portal's published file rules, the compile-everything check, the 3-turn
  default-scenario smoke test with the 100 ms and 10-second limits, and the
  working directory set to the agent's folder during validation.
- Default transaction visibility (`observe_all_transactions: false`): every
  team sees only its own transactions plus public inventories and capital.

**Approximated (the real versions are unknown or not public)**

- **Opponents.** 39 simulated teams of mixed level (about 40 % weak, 40 %
  medium, 20 % strong) written for this arena, not the real participants.
  They are deterministic programs; real teams were people who changed their
  code during the day.
- **Private scenarios.** Four held-out scenarios built in the spirit of
  `default.yaml` and `scaled_market.yaml` (40 and 80 turns; different seeds,
  supply, demand and capital), 8 seeds each. The real scenarios, their number
  and the number of matches are unknown. They keep the public goods and recipes.
- **Portal.** The CPU allowance is not published (20 s of CPU is used here);
  the opponents in the 3 validation turns are the built-in agents; the 10 s
  budget is measured around import + 3 turns on your machine, so timing
  differs from the organizers' evaluator. Validation output is a local
  printout instead of a web page.
- **Ties** in a match get the average of the tied ranks; bankrupt teams rank
  below every solvent team (README does not specify either).
- **Results timing.** Here the leaderboard appears right after each
  submission; on the real day official results came from the portal. If you
  want the real-day feeling, do not look at `leaderboard` until 19:00.
- **Hardware.** Matches run in parallel on your CPU cores; a slow or busy
  machine can turn a borderline-fast agent into timeouts that would not happen
  on the evaluator (and vice versa).

See `ARENA.md` at the repository root for every design decision.
