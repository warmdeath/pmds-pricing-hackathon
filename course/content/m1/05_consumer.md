# 1.5 Consumer theory: utility, budgets, willingness to pay

## The big picture

Where does the demand curve come from? Consumer theory models a person with
**preferences** (what they like) and a **budget** (what they can afford), who
chooses the best affordable bundle. Changing a price and re-solving traces out
the demand curve.

> **Analogy.** Shopping with €50 in a supermarket is a puzzle with two pieces:
> the menu of what you'd like (preferences) and the size of your wallet
> (budget). The answer is the basket where the "last euro" spent on each item
> gives you the same satisfaction.

## Utility and marginal utility

**Utility** is a numerical representation of preferences: bundle A is
preferred to B if U(A) > U(B). Only the **ranking** matters (ordinal utility).

**Marginal utility (MU)** is the extra utility from one more unit. Usually it
**diminishes**: the first slice of pizza is great, the fifth much less so.

**Equal-marginal principle.** With goods X and Y, the optimum satisfies

```
MU_X / P_X = MU_Y / P_Y
```

— the last euro spent on each good yields the same utility. If MU_X/P_X were
higher, moving a euro from Y to X would raise utility.

## Budget constraint

With income M and prices P_X, P_Y:  P_X·X + P_Y·Y ≤ M.
The budget line has intercepts M/P_X and M/P_Y and slope −P_X/P_Y (the market
rate at which you can trade Y for X).

- Income ↑ → parallel outward shift.
- P_X ↑ → line pivots inward around the Y intercept.

## Indifference curves and the optimum

An **indifference curve** joins bundles with the same utility. Properties:
downward sloping, higher curves are better, they don't cross, and they are
usually convex. Their slope is the **marginal rate of substitution (MRS)** =
MU_X / MU_Y: how much Y you'd give up for one more X.

The optimum (interior) is where the highest reachable indifference curve is
tangent to the budget line:

```
MRS = MU_X / MU_Y = P_X / P_Y
```

*Worked example (Cobb-Douglas).* U = X·Y, M = 100, P_X = 2, P_Y = 5.
MU_X = Y, MU_Y = X ⇒ Y/X = 2/5 ⇒ 5Y = 2X. Budget: 2X + 5Y = 100 ⇒ 2X + 2X = 100
⇒ X = 25, Y = 10. With U = X^a·Y^(1−a) the consumer always spends share a of
income on X: X = a·M/P_X.

## Income and substitution effects

When P_X rises:

- **Substitution effect**: X is relatively dearer → buy less X (always).
- **Income effect**: real purchasing power falls → buy less X if X is normal,
  more if X is inferior.

For a normal good both effects point the same way, so demand slopes down. A
**Giffen good** (theoretical, very rare) is so inferior that the income effect
outweighs the substitution effect.

## Discrete purchases and reservation prices

Many goods are bought one at a time (a phone, a laptop, a concert ticket).
Then the useful concept is the **reservation price** (willingness to pay,
WTP): the maximum a person would pay for the item. The person buys if
price ≤ WTP and earns consumer surplus WTP − price.

If WTPs in a population are spread out, **market demand at price P = number of
people whose WTP ≥ P**. With WTP uniformly distributed between L and H and N
customers:

```
Q(P) = N · (H − P) / (H − L)      for L ≤ P ≤ H
```

*Worked example.* 100 customers, WTP uniform on [200, 400]. At P = 250,
Q = 100·(150/200) = 75. Revenue P·Q is maximised where
d[P·(H−P)]/dP = 0 ⇒ P = H/2 = 200 (here at the lower end, so 200 → Q = 100,
revenue 20,000). With L = 0 the revenue-maximising price is H/2.

## Heterogeneous consumers and segments

Real markets mix groups (**segments**) with different preferences and WTP —
students vs professionals, budget vs premium buyers. Aggregate demand is the
sum of segment demands, so it can have kinks where a new segment starts buying.
Firms study segments to design products and prices (lesson 1.8, price
discrimination; lesson 1.9, differentiated demand).

## Revealed preference and behavioural notes

**Revealed preference**: if you chose A when B was affordable, you reveal that
you prefer A. Behavioural economics adds that people use reference points
(loss aversion: losing €10 hurts more than gaining €10 pleases), anchor on
first prices seen, and are influenced by framing ("€99" vs "€100").

## Summary

- Optimum: MU_X/P_X = MU_Y/P_Y ⇔ MRS = price ratio.
- Price changes have substitution and income effects.
- For unit purchases, think in **reservation prices**: demand at P counts
  buyers with WTP ≥ P.
- Market demand aggregates heterogeneous segments.
