# 2.7 Decisions under uncertainty: expected value, risk, learning

## The big picture

Business decisions are made before outcomes are known: demand may be high or
low, a bid may win or lose. This lesson gives the tools to compare risky
options (expected value, variance, expected utility), to value information,
and to learn from data while acting (explore vs exploit).

> **Analogy.** A weather forecast doesn't tell you whether it will rain; it
> tells you the odds. Whether to carry an umbrella depends on the odds *and*
> on how much you hate getting wet versus carrying it.

## Expected value

For a random outcome X with values x_i and probabilities p_i:

```
E[X] = Σ p_i · x_i
```

*Worked example.* Launching a product: 30 % chance of €500k profit, 50 % of
€100k, 20 % of −€300k. E = 150 + 50 − 60 = **€140k**.

Expected value is linear: E[aX + b] = aE[X] + b and E[X + Y] = E[X] + E[Y].

## Variance and risk

```
Var(X) = Σ p_i (x_i − E[X])²        σ = √Var
```

Two options with the same mean can have very different spreads. A
**risk-neutral** decision maker cares only about E[X]; a **risk-averse** one
dislikes spread; a **risk-lover** seeks it.

## Expected utility

Von Neumann-Morgenstern: choose the option with the highest **expected
utility** E[u(X)]. A concave u (e.g. √x, log x) represents risk aversion
(diminishing marginal utility of wealth).

- **Certainty equivalent** (CE): the sure amount with the same utility as the
  gamble; **risk premium** = E[X] − CE.

*Worked example.* Wealth gamble: 50 % €0, 50 % €100, u = √x.
E[u] = 0.5·10 = 5 ⇒ CE = 25 ⇒ risk premium = 50 − 25 = **€25**.

Behavioural findings: **loss aversion** (losses weigh ~2× gains),
**probability weighting** (overweighting small probabilities), framing.

## Decision trees and the value of information

A **decision tree** alternates decision nodes (you choose) and chance nodes
(nature chooses). Solve backwards: at chance nodes take expectations, at
decision nodes take the best option.

**Expected value of perfect information (EVPI)** = expected payoff if you
could learn the outcome before deciding − expected payoff of the best decision
now. It is the maximum worth paying for information.

*Worked example.* Order 100 or 200 units; demand low (p = 0.5) or high.
Profits: order 100 → 1,000 either way; order 200 → 400 (low) or 2,000 (high).
Best now: order 200, E = 1,200. With perfect information: low → 1,000,
high → 2,000, E = 1,500. **EVPI = 300**.

## The newsvendor problem

How many units to stock when demand is uncertain and leftovers are worth less
than they cost? Let c_u = cost of **under**stocking one unit (lost margin)
and c_o = cost of **over**stocking one unit (what a leftover loses). The
optimal quantity Q\* satisfies:

```
Pr(Demand ≤ Q*) = c_u / (c_u + c_o)        (the critical ratio)
```

*Worked example.* Newspapers cost €1, sell for €3, leftovers worth €0:
c_u = 2, c_o = 1 ⇒ critical ratio 2/3. If demand is uniform on [50, 150],
Q\* = 50 + (2/3)·100 = **116.7 ≈ 117**. If leftovers could be sold tomorrow at
full price, c_o would be near zero and the ratio near 1 — stock more. The
salvage value of leftovers is a key input.

## Learning from data: estimation and Bayes

- **Sample mean** and **moving averages** estimate a stable quantity;
  **exponential smoothing** (EMA) S_t = α·x_t + (1 − α)·S_{t−1} weighs recent
  data more (α near 1 reacts fast but is noisy; α near 0 is smooth but slow).
- **Bayes' rule** updates beliefs: P(H|data) = P(data|H)·P(H)/P(data).
- **Censored data**: if you only observe sales, not demand, a sold-out period
  tells you demand was *at least* what you sold. Sales ≠ demand when supply
  is limited.

*Worked example (EMA).* α = 0.3, previous estimate 10, new observation 20 →
0.3·20 + 0.7·10 = **13**.

## Explore vs exploit

When you learn by acting (trying a price, a product, a supplier) you face the
**exploration-exploitation trade-off**: exploit the option that looks best now,
or explore others to learn whether they are better. Classic formalisation:
the **multi-armed bandit**. Simple policies:

- **ε-greedy**: exploit most of the time, explore with probability ε;
- **optimism under uncertainty (UCB)**: favour options with high estimated
  value plus an uncertainty bonus;
- **Thompson sampling**: act on a random draw from your current beliefs.

Exploration is worth more early (more time left to use what you learn) and
less near the end of a horizon.

## Summary

- Compare risky options with E[X]; risk attitude via expected utility, CE and
  risk premium.
- EVPI bounds the value of information.
- Newsvendor: stock up to the critical ratio c_u/(c_u + c_o).
- Learning: EMAs, Bayes, censored observations; explore early, exploit late.
