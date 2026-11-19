# 2.3 Oligopoly: Cournot, Bertrand, Stackelberg, collusion

## The big picture

An **oligopoly** is a market with a few interdependent sellers. Each firm's
profit depends on the others' choices, so we model it as a game. The
predictions depend crucially on **what firms choose** (quantities or prices),
whether products are identical, and whether capacity is limited.

> **Analogy.** Two ice-cream sellers on a beach. If they compete only on price
> for identical cones, they undercut each other to cost. If each has limited
> freezers (quantities), prices stay higher. If they can talk, they are
> tempted to agree on a high price — and each is tempted to cheat.

## Cournot: competition in quantities

Firms choose quantities simultaneously; the price clears the market:
P = a − b(q₁ + q₂). Constant marginal cost c.

Firm 1: π₁ = (a − b(q₁ + q₂) − c)·q₁. Best response:
∂π₁/∂q₁ = a − c − 2bq₁ − bq₂ = 0 ⇒ **q₁ = (a − c − bq₂)/(2b)**.

Symmetric equilibrium: q = (a − c)/(3b) each, Q = 2(a − c)/(3b),
P = (a + 2c)/3.

With **n** identical firms: q = (a − c)/((n + 1)b), P = (a + nc)/(n + 1).
As n → ∞, P → c: Cournot converges to perfect competition.

*Worked example.* P = 120 − Q, c = 30, two firms: q = 90/3 = **30** each,
Q = 60, P = **60**, profit each = (60 − 30)·30 = **900**. Monopoly would be
Q = 45, P = 75, profit 2,025; competition Q = 90, P = 30.

## Bertrand: competition in prices

Firms set prices simultaneously; identical products; buyers buy from the
cheapest (split ties). Any price above c is undercut by a rival charging
slightly less, taking the whole market. Equilibrium: **P = c** with just two
firms, zero profit — the **Bertrand paradox**.

The paradox is resolved by things real markets have:

- **Capacity constraints** (Edgeworth): if your rival cannot serve everyone,
  undercutting does not steal the whole market; prices stay above cost and
  may cycle (**Edgeworth cycles**: gradual undercutting, then a jump back up).
- **Product differentiation** (lesson 1.9): undercutting steals only some
  customers; equilibrium P > c.
- **Repeated interaction** (lesson 2.4): undercutting today triggers
  punishment tomorrow.
- **Search costs and loyalty**.

*Differentiated Bertrand.* q₁ = a − bP₁ + dP₂. Best response
P₁ = (a + bc + dP₂)/(2b). Prices are **strategic complements**: if a rival
raises its price, your best response is to raise yours. (In Cournot,
quantities are **strategic substitutes**: if a rival produces more, you
produce less.)

## Stackelberg: leader and follower

The leader chooses quantity first; the follower observes it and best-responds.
The leader anticipates this (backward induction).

With P = a − bQ and cost c: follower q₂ = (a − c − bq₁)/(2b). Leader
maximises (a − b(q₁ + q₂(q₁)) − c)q₁ ⇒ **q₁ = (a − c)/(2b)**,
q₂ = (a − c)/(4b). The leader produces more and earns more than in Cournot:
commitment pays.

*Worked example.* P = 120 − Q, c = 30: q₁ = 45, q₂ = 22.5, P = 52.5.

## Collusion and cartels

If firms jointly act as a monopoly they maximise joint profit (Q = 45,
P = 75 above). But each member then has an incentive to **cheat**: at the
cartel price, producing more is profitable for the individual firm
(prisoner's dilemma). Cartels are illegal in the EU and US; tacit collusion
(coordination without agreement) is the grey zone. Factors helping collusion:
few firms, repeated interaction, transparency (easy to see cheating), stable
demand, similar costs. Factors hurting it: many firms, secret prices, lumpy
orders, a definite last period.

## Comparing outcomes (P = a − bQ, cost c)

| model | total Q | price |
| --- | --- | --- |
| monopoly / cartel | (a − c)/2b | (a + c)/2 |
| Stackelberg (2) | 3(a − c)/4b | (a + 3c)/4 |
| Cournot (2) | 2(a − c)/3b | (a + 2c)/3 |
| Cournot (n) | n(a − c)/((n+1)b) | (a + nc)/(n+1) |
| Bertrand (identical) | (a − c)/b | c |

## Summary

- Quantities (Cournot): prices above cost, falling with the number of firms.
- Prices (Bertrand) with identical goods: price = cost even with 2 firms;
  capacity, differentiation and repetition soften this.
- Leaders gain from commitment (Stackelberg).
- Collusion is profitable jointly but unstable individually.
