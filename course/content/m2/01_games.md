# 2.1 Strategic games and Nash equilibrium

## The big picture

In the market models so far, each decision maker reacted to prices it took as
given. When there are only a few players, or each player's best choice
depends on what the others do, we need **game theory**: the study of
**strategic interdependence**.

> **Analogy.** Choosing a route home at 6 pm is a game: the best road depends
> on which roads everyone else chooses. If everybody follows the same app, the
> "fast" road becomes the slow one.

## Elements of a game

- **Players** (firms, bidders, countries).
- **Strategies**: complete plans of action.
- **Payoffs**: what each player gets for each combination of strategies
  (profit, utility, rank).
- **Information**: what each player knows when choosing; **simultaneous**
  (sealed) vs **sequential** moves.

A two-player simultaneous game is written as a **payoff matrix** (normal
form). Convention: (row player's payoff, column player's payoff).

## Dominant strategies

A strategy is **strictly dominant** if it gives a higher payoff than any other
strategy **whatever the opponents do**. A rational player always plays a
dominant strategy if one exists.

**Prisoner's dilemma.**

| | Cooperate | Defect |
| --- | --- | --- |
| **Cooperate** | 3, 3 | 0, 5 |
| **Defect** | 5, 0 | 1, 1 |

Defect is dominant for both (5 > 3 and 1 > 0), so the outcome is (Defect,
Defect) = (1, 1), although (Cooperate, Cooperate) = (3, 3) is better for both.
Individual rationality ≠ collective rationality. Business versions: two firms
choosing high or low prices, advertising wars, overfishing.

## Iterated elimination of dominated strategies

Remove strictly dominated strategies, then check whether new strategies
become dominated in the reduced game, and repeat. It assumes **common
knowledge of rationality** (I know you're rational, you know I know, …).

*Example: the "guess 2/3 of the average" game.* Everyone picks 0–100; the
winner is closest to 2/3 of the average. Numbers above 66.7 are dominated;
once removed, above 44.4 are dominated; … iterated elimination leads to 0. In
experiments people pick around 20–35: real players reason a few steps, not
infinitely (**level-k thinking**). Knowing *how many* steps others take
matters as much as the theory.

## Best responses and Nash equilibrium

A **best response** is the strategy that maximises your payoff given the
others' strategies. A **Nash equilibrium** is a combination of strategies in
which **every player is playing a best response to the others** — nobody can
gain by deviating alone.

How to find pure-strategy Nash equilibria in a matrix: for each column,
underline the row player's best payoff; for each row, underline the column
player's best payoff; cells with both underlined are equilibria.

*Example: coordination (battle of the sexes).*

| | Opera | Football |
| --- | --- | --- |
| **Opera** | 2, 1 | 0, 0 |
| **Football** | 0, 0 | 1, 2 |

Two pure equilibria: (Opera, Opera) and (Football, Football). Game theory says
which outcomes are stable, not always which one happens; **focal points**
(Schelling), conventions and communication select among them.

## Continuous strategies

When strategies are numbers (prices, quantities, bids), best responses are
**functions** (reaction functions) and the equilibrium is their intersection.

*Worked example.* Two firms choose effort e₁, e₂. Payoff of 1:
π₁ = e₁(10 + e₂ − e₁). Best response: ∂π₁/∂e₁ = 10 + e₂ − 2e₁ = 0 ⇒
e₁ = (10 + e₂)/2. Symmetric equilibrium: e = (10 + e)/2 ⇒ **e = 10**.
Lesson 2.3 uses exactly this method for Cournot and Bertrand.

## Zero-sum and relative payoffs

In a **zero-sum** game one player's gain is another's loss (poker, a fixed
prize). When payoffs are **ranks** in a tournament rather than absolute
profits, the game becomes (partly) zero-sum: what matters is doing better
than others, which can change which strategies are optimal (e.g. taking more
risk when behind, less when ahead).

## Summary

- Game = players, strategies, payoffs, information.
- Dominant strategies; prisoner's dilemma shows the clash between individual
  and joint interest.
- Nash equilibrium = mutual best responses; may be multiple.
- Real players reason a limited number of steps (level-k).
