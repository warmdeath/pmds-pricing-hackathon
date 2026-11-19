# 2.4 Repeated games, reputation and end-game effects

## The big picture

Most business interactions repeat: the same rivals meet every day, the same
suppliers sell every week. Repetition changes incentives — today's action
affects tomorrow's reactions. Cooperation impossible in a one-shot game can
become sustainable, and **when** the game ends matters a lot.

> **Analogy.** Tipping in a restaurant you'll never visit again vs your
> neighbourhood café. The café remembers.

## Finitely repeated games and unravelling

Repeat the prisoner's dilemma a **known, finite** number of times T. In the
last round there is no future, so both defect. In round T − 1, knowing round T
is fixed, defection is again dominant… By backward induction, players defect
in **every** round (**unravelling**).

Experiments show people cooperate for most of a finite game and defect near
the end (**end-game effect**). Unravelling relies on everyone knowing the
exact last round and trusting everyone else's full rationality.

## Infinitely repeated games (or unknown end)

If the game continues with probability δ each period (or players discount the
future by δ), cooperation can be sustained by strategies such as:

- **Grim trigger**: cooperate until the other defects, then defect forever.
- **Tit-for-tat**: copy the other's last move (cooperative, retaliatory,
  forgiving, clear — it did well in Axelrod's tournaments).

Cooperation is sustainable if the one-time gain from defecting is smaller than
the discounted future loss from punishment. For the matrix in lesson 2.1
(R = 3 reward, T = 5 temptation, P = 1 punishment) with grim trigger:

```
cooperate forever:    R / (1 − δ)
defect once:          T + δ·P / (1 − δ)
cooperate if   δ ≥ (T − R)/(T − P) = (5 − 3)/(5 − 1) = 0.5
```

The **folk theorem**: with patient enough players, almost any outcome that
gives everyone more than their punishment payoff can be sustained.

*Worked example (cartel).* Two firms share monopoly profit 2,025 → 1,012.5
each per period (q = 22.5, P = 75). Cheating: the best response to the
partner's 22.5 is q = (90 − 22.5)/2 = 33.75, price 63.75, one-period profit
33.75 × 33.75 = 1,139.06; then Cournot 900 forever. Cooperation requires
δ ≥ (1139.06 − 1012.5)/(1139.06 − 900) = **0.529**.

## Reputation

Even in finite games, a small chance that a player is a "committed type"
(always cooperates, always fights entrants) makes it worthwhile for rational
players to imitate that type until near the end — the **reputation**
results of Kreps-Milgrom-Roberts-Wilson. Reputation is an asset built
slowly and destroyed quickly.

## Monitoring and noise

Cooperation needs players to detect deviations. With **public information**
(posted prices, published stocks), deviations are visible; with private or
noisy information (secret discounts, random demand), a sales drop might be bad
luck or a rival's undercut. Then punishments must be triggered by thresholds
and occasionally hit innocent periods (**Green-Porter** price wars).

## Learning and adaptation in repeated play

In repeated settings players also **learn**:

- **Fictitious play**: best-respond to the average of opponents' past play.
- **Reinforcement learning**: repeat what earned more in the past.
- **Adjustment rules**: raise price after selling out, lower after unsold
  stock — simple rules can converge to, cycle around, or diverge from an
  equilibrium depending on how fast they adjust.

Many players using adaptive rules generate market dynamics (price trends,
cycles) that a static equilibrium does not show.

## Tournaments and relative performance

When rewards depend on **rank** (sales contests, promotions, competitions),
incentives change: what matters is beating others, not maximising your own
absolute outcome. Variance becomes a tool — players behind tend to take more
risk; players ahead protect their lead (Lazear-Rosen tournament theory).

## Summary

- Known finite end → unravelling by backward induction; real people show
  end-game effects.
- Infinite / uncertain end → cooperation via trigger strategies if δ is
  high enough (δ ≥ (T − R)/(T − P)).
- Reputation, monitoring and learning shape repeated interactions.
- Rank-based rewards change risk incentives.
