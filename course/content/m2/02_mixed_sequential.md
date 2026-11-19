# 2.2 Mixed strategies and sequential games

## The big picture

Some games have no equilibrium in pure strategies — any predictable choice is
exploited. Players then **randomise**. Other games are played in sequence, and
the order of moves (and what is observed) changes the outcome. This lesson
covers both.

> **Analogy.** A penalty kick: if the goalkeeper always dives left, the
> striker always shoots right. The only stable plan is to be unpredictable.

## Mixed strategies

A **mixed strategy** assigns probabilities to pure strategies.
**Matching pennies**: both show heads or tails; player 1 wins if they match.
No pure equilibrium; the mixed equilibrium is 50/50 for both.

**Indifference principle.** In a mixed equilibrium each player randomises so
that the **other** player is indifferent between their pure strategies (if
they weren't, they would not mix).

*Worked example (penalty).* Striker scores with probabilities:

| | Keeper dives L | Keeper dives R |
| --- | --- | --- |
| **Shoot L** | 0.6 | 0.9 |
| **Shoot R** | 0.95 | 0.5 |

Keeper dives L with probability q making the striker indifferent:
0.6q + 0.9(1 − q) = 0.95q + 0.5(1 − q) ⇒ 0.9 − 0.3q = 0.5 + 0.45q ⇒
q = 0.4/0.75 = **0.533**.

Every finite game has at least one Nash equilibrium, possibly mixed
(**Nash's theorem**). In pricing, mixed strategies explain **price
dispersion** and sales: with some informed shoppers and some loyal ones,
stores randomise between high prices (milking the loyal) and sales
(capturing shoppers) — Varian's model of sales.

## Sequential games and game trees

In **extensive form** the game is a tree: nodes are decisions, branches are
actions, leaves are payoffs. With **perfect information** (each player sees
previous moves) we solve by **backward induction**: start at the last
decision, choose the best action, replace the node with its payoff, move
backwards.

*Worked example (entry deterrence).* An entrant decides In or Out. If In, the
incumbent decides Fight (payoffs −1, −1) or Accommodate (1, 1). If Out:
(0, 2) (entrant, incumbent). Backward induction: if In, the incumbent prefers
Accommodate (1 > −1); knowing this, the entrant enters (1 > 0). Outcome
(In, Accommodate).

## Credibility and subgame perfection

The incumbent may *threaten* "I will fight if you enter". There is a Nash
equilibrium (Out, Fight-if-In), but the threat is **not credible**: once
entry happens, fighting hurts the incumbent. **Subgame perfect equilibrium**
(SPE) — the result of backward induction — rules out non-credible threats.

Ways to make threats credible: **commitment** (sinking capacity in advance,
contracts, reputation), reducing your own options ("burning bridges").
Paradoxically, limiting your flexibility can increase your payoff.

## First-mover and second-mover advantage

- **First-mover advantage**: committing first to a quantity or capacity
  forces rivals to adapt (Stackelberg, lesson 2.3).
- **Second-mover advantage**: in price competition, moving second lets you
  undercut slightly; in uncertain markets, letting others experiment first
  reveals information.

Note what "first" means: what matters is not the clock but **what is
observed** before the others choose. Sealed simultaneous decisions are a
simultaneous game even if submitted at different times.

## Information sets

When a player does not observe a previous move, her decision nodes are joined
in an **information set**: she must choose the same action at all of them.
Games of **imperfect information** mix sequential timing with hidden actions —
e.g. each period you see what happened last period but not what rivals are
choosing now.

## Summary

- No pure equilibrium → mix; mix to make the opponent indifferent.
- Sequential games: solve by backward induction → subgame perfect equilibrium.
- Non-credible threats don't count; commitment can create credibility.
- Observation, not timing, defines whether moves are sequential.
