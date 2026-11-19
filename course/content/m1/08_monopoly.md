# 1.8 Monopoly, market power and price discrimination

## The big picture

A firm has **market power** when it can raise its price without losing all its
customers — its demand curve slopes down. The extreme case is a **monopoly**
(single seller, no close substitutes), but market power exists in degrees in
most real markets (brands, location, differentiation). This lesson explains
how a price-setting firm chooses prices and why the outcome is inefficient.

> **Analogy.** The only café on a mountain top: if it raises the price of
> coffee, some hikers skip it, but not all. It trades off "fewer cups" against
> "more per cup".

## Marginal revenue

For a price setter, selling one more unit requires lowering the price on
**all** units (if one price is charged). So marginal revenue is less than the
price:

```
MR = P + Q · dP/dQ          linear demand P = a − bQ  ⇒  MR = a − 2bQ
```

MR also relates to elasticity:  MR = P · (1 − 1/|ε|). MR > 0 only where demand
is elastic — a monopolist never operates on the inelastic part of demand.

## Profit maximisation

```
MR = MC    then read the price from the demand curve
```

*Worked example.* Demand P = 100 − 2Q, constant MC = 20.
MR = 100 − 4Q = 20 ⇒ Q = 20, P = 100 − 40 = **60**. Profit = (60 − 20)·20 =
**800**. Compare competition: P = MC = 20 ⇒ Q = 40.
DWL = ½ · (60 − 20) · (40 − 20) = **400**.

## The markup rule (Lerner index)

Combining MR = MC with MR = P(1 − 1/|ε|):

```
(P − MC) / P = 1 / |ε|            ⇔        P = MC · |ε| / (|ε| − 1)
```

The **Lerner index** (P − MC)/P measures market power. The more elastic the
demand facing the firm, the smaller the optimal markup. With |ε| = 3:
P = 1.5 · MC; with |ε| = 1.25: P = 5 · MC.

*Exponential demand* Q = A·e^(−βP) has |ε| = βP and gives the elegant result
P = MC + 1/β: the optimal markup is a fixed **amount** 1/β above marginal cost.

## Why monopoly is inefficient

The monopolist stops producing while buyers still value units above MC
(between Q_m and Q_c). Those trades would create surplus but are not made →
deadweight loss. Part of consumer surplus is also **transferred** to the
firm. Sources of monopoly power: legal barriers (patents, licences), control
of a key input, economies of scale (**natural monopoly**), network effects.

## Price discrimination

Charging **different prices for the same good** to different buyers, when
that is not explained by cost differences. Requires (1) market power,
(2) a way to sort buyers, (3) no resale (arbitrage).

- **First degree (perfect)**: each buyer pays their exact WTP. The firm
  captures all surplus; output is efficient (no DWL) but CS = 0.
- **Second degree (self-selection)**: the same menu for everyone, buyers
  sort themselves: quantity discounts, versions ("basic" vs "pro"), time
  (hardback before paperback, early-bird tickets).
- **Third degree (segments)**: different prices for observable groups
  (students, seniors, countries). Optimal rule: MR in each segment = MC, so
  the segment with **less elastic** demand pays more.

*Worked example (3rd degree).* MC = 10. Segment A: P = 50 − Q_A;
segment B: P = 30 − Q_B. A: MR = 50 − 2Q_A = 10 ⇒ Q_A = 20, P_A = 30.
B: 30 − 2Q_B = 10 ⇒ Q_B = 10, P_B = 20. The less elastic segment A pays more.

**Peak-load and dynamic pricing** (airlines, hotels, ride sharing) combine
these ideas with capacity and time: when capacity is fixed, prices rise as
remaining seats become scarce relative to expected demand.

## Two-part tariffs and bundling

- **Two-part tariff**: entry fee + per-unit price (gym, theme park). Optimal
  with identical buyers: per-unit price = MC, fee = CS.
- **Bundling**: selling goods together extracts more surplus when buyers'
  valuations are negatively correlated.

## Summary

- MR < P for a price setter; choose Q with MR = MC, price from demand.
- Markup rule: (P − MC)/P = 1/|ε|.
- Monopoly creates DWL; price discrimination can raise output and profits.
- Discrimination degrees: perfect, self-selection, segment-based.
