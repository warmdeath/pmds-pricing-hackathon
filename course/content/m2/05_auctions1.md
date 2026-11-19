# 2.5 Auctions I: formats, values, bid shading

## The big picture

An **auction** is a market mechanism with explicit rules that turn bids into
an allocation (who gets what) and payments (who pays what). Auctions sell
spectrum licences, government bonds, electricity, online ads, art and
commodities. Auction theory (Vickrey, Myerson, Milgrom-Wilson — several Nobel
prizes) predicts how rational bidders bid under each set of rules.

> **Analogy.** An auction is a game whose rulebook is printed in advance. Two
> games with the same prize but different rulebooks ("you pay your bid" vs
> "you pay the second-highest bid") make the same players behave very
> differently.

## The four classic single-unit formats

| format | how it works | strategically equivalent to |
| --- | --- | --- |
| **English** (ascending, open) | price rises until one bidder remains; she pays the last price | second-price sealed (with private values) |
| **Dutch** (descending, open) | price falls until someone accepts | first-price sealed |
| **First-price sealed-bid** | sealed bids; highest wins, **pays own bid** | Dutch |
| **Second-price sealed-bid** (Vickrey) | sealed bids; highest wins, **pays the second-highest bid** | English |

## Values: private vs common

- **Private values**: each bidder knows her own value v_i, which doesn't
  depend on others' information (a painting you want to hang at home; an
  input whose value to you depends on what *you* can do with it).
- **Common value**: the object has the same (unknown) value for everyone,
  each bidder has a noisy estimate (an oil field, a company). Lesson 2.6
  discusses the winner's curse this creates.
- Real auctions often mix the two (affiliated values).

## Second-price: bid your value

In a Vickrey auction, bidding your true value is a **weakly dominant
strategy**:

- Bidding above v: only changes the outcome when the second-highest bid lies
  between v and your bid — you win but pay more than v → loss.
- Bidding below v: only changes the outcome when the second-highest bid lies
  between your bid and v — you lose an item you would have gained from.

Your bid determines **whether** you win, not **what you pay**.

## First-price: shade your bid

In a first-price (pay-your-bid) auction, bidding your value guarantees zero
surplus. You face a trade-off:

```
expected surplus = (v − b) × Pr(win with b)
```

Lowering b increases the margin (v − b) but reduces the chance of winning.
The optimum is **below** v: **bid shading**.

**Benchmark result.** n bidders, independent private values uniform on [0, 1]
(or [0, V], scaling everything), risk-neutral, symmetric equilibrium:

```
b(v) = (n − 1)/n · v
```

*Derivation sketch (n = 2).* If the rival bids b(v) = k·v, bidding b wins when
k·v_rival < b, probability b/k. Maximise (v − b)·b/k ⇒ v − 2b = 0 ⇒ b = v/2.

*Worked example.* 5 bidders, values uniform on [0, 100]: a bidder with value
80 bids 4/5·80 = **64**. With 2 bidders she would bid 40; with 20 bidders 76.
**More competition → less shading.**

Shading in practice depends on beliefs about rivals' bids, not on a formula:
the general principle is "bid where the extra margin from a lower bid just
offsets the lost probability of winning", i.e. maximise (v − b)·F(b) where
F(b) is the probability that b wins.

## Revenue equivalence

**Revenue equivalence theorem**: with risk-neutral bidders, independent
private values from the same distribution, and the highest-value bidder
always winning, all these standard formats give the seller the **same
expected revenue**. With uniform [0, 1] values:

```
expected revenue = expected 2nd-highest value = (n − 1)/(n + 1)
```

In first-price, the winner pays her shaded bid; in second-price, the
unshaded second value; on average the same. *Example:* n = 4 → 3/5 = 0.6.

The theorem breaks with **risk aversion** (risk-averse bidders shade less in
first-price → first-price yields more), **asymmetric bidders**, **budget
constraints**, and **common values** (English auctions reveal information and
reduce the winner's curse → higher revenue).

## Bidding when you are risk averse

A risk-averse bidder fears losing more than she values the extra margin, so
she bids **closer to her value** in a first-price auction. In second-price,
truthful bidding remains dominant regardless of risk attitude.

## Summary

- English ≈ second-price; Dutch ≈ first-price.
- Second-price: bid your value. First-price: shade, b = (n−1)/n·v in the
  uniform benchmark; shading falls as the number of bidders rises.
- Revenue equivalence: same expected revenue under standard assumptions;
  breaks with risk aversion, asymmetry, budgets, common values.
