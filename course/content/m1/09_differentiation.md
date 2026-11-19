# 1.9 Product differentiation and discrete-choice demand

## The big picture

Most markets sit between perfect competition and monopoly: many sellers with
products that are similar but not identical — **monopolistic competition**.
Each seller has a little market power because buyers differ in tastes,
location, loyalty or information. Discrete-choice models describe how each
individual customer picks **one** option among many, and how that aggregates
into market shares.

> **Analogy.** On a street with ten restaurants, you don't always go to the
> cheapest; the price matters, but so do mood, distance and habit. Raise the
> price a little and you lose *some* customers, not all of them.

## Monopolistic competition (Chamberlin)

- Many firms, differentiated products, free entry.
- Short run: each firm acts like a small monopolist (MR = MC, P > MC).
- Long run: entry steals customers until profits are zero; each firm's demand
  is **tangent** to its ATC curve. Price > MC and firms produce below
  minimum ATC — "excess capacity", the price of variety.

## Horizontal and vertical differentiation

- **Vertical**: everybody agrees on the ranking (quality: more battery life is
  better). Higher quality sells at higher prices to buyers with higher WTP for
  quality.
- **Horizontal**: tastes differ (colour, location). **Hotelling's linear
  city**: consumers live along a street, two shops; each consumer buys from
  the shop with the lowest price + travel cost. Price competition is softened
  by "distance"; in equilibrium P = MC + t (t = transport cost parameter):
  the more differentiated, the higher the markup.

## Discrete choice: the logit model

Each customer i chooses the option j that gives the highest utility

```
U_ij = V_j + ε_ij        V_j = quality_j − β · P_j
```

where ε_ij is a random taste shock. If the shocks follow a particular
(Gumbel) distribution, the probability of choosing j is the **logit
formula**:

```
Pr(j) = exp(V_j) / Σ_k exp(V_k)
```

Properties worth knowing:

- Every option with finite price has a **positive** probability: the cheapest
  seller does not take everybody.
- Only **differences** matter: raising every price by the same amount leaves
  the shares unchanged (if all options remain available).
- With identical qualities, the ratio of two sellers' shares is
  exp(−β(P_1 − P_2)): a price gap of 1/β multiplies the cheaper seller's
  odds by e ≈ 2.72. β measures **price sensitivity** — large β makes buyers
  almost always pick the cheapest; β → 0 makes price irrelevant.
- An **outside option** (not buying) can be included as option 0.
- **Independence of irrelevant alternatives (IIA)**: the ratio between two
  options does not depend on the others — a known limitation (the "red bus /
  blue bus" problem).

*Worked example.* Three sellers at prices 100, 120, 150, same quality,
β = 0.02. Weights: e^(−2) = 0.135, e^(−2.4) = 0.091, e^(−3) = 0.050; sum 0.276.
Shares: **49 %, 33 %, 18 %**.

## Own-price elasticity in the logit model

For seller j with share s_j:  ε_jj = −β · P_j · (1 − s_j).
A small seller (s_j ≈ 0) faces elasticity ≈ −βP_j: the markup rule of lesson
1.8 gives P − MC ≈ 1/β for a single-product firm with small share — the logit
version of "differentiation softens competition".

## Combining WTP thresholds with choice

A common modelling pattern combines both lessons: a customer first looks only
at options priced at or below her **reservation price** (lesson 1.5), then
chooses among those with probabilities that favour cheaper ones. Two
consequences follow mechanically: pricing above a customer's reservation price
removes you from her choice set entirely; and among eligible options the
choice is probabilistic, not winner-take-all.

## Market shares, concentration, competition policy

- **Market share** = firm sales / market sales.
- **HHI** (Herfindahl-Hirschman Index) = Σ (share in %)². 10,000 = monopoly;
  below 1,500 unconcentrated; above 2,500 highly concentrated.

*Worked example.* Shares 40 %, 30 %, 20 %, 10 % → HHI = 1600 + 900 + 400 +
100 = **3,000**.

## Summary

- Differentiation gives each firm a downward-sloping demand.
- Long-run monopolistic competition: zero profit, P > MC.
- Logit: Pr(j) ∝ exp(V_j); price sensitivity β; cheapest is most likely, not
  certain; elasticity −βP(1 − s).
- Reservation prices define the choice set; logit allocates within it.
