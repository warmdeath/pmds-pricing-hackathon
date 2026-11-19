# 3.7 Financial markets: bonds, stocks, efficiency, arbitrage

## The big picture

Financial markets move savings to those who can use them: households buy
bonds and shares, firms and governments receive funds. Prices of financial
assets are present values of expected future cash flows (lesson 3.5),
adjusted for risk (lesson 3.6). This lesson covers the main instruments and
the big ideas of market efficiency and arbitrage.

> **Analogy.** A bond is a ticket entitling you to a fixed series of future
> payments. Its price today is how much those future payments are "worth now".
> When rates rise, every future euro is worth less today — so the ticket gets
> cheaper.

## Bonds

A bond pays **coupons** (C per year) and the **face value** F at maturity.

```
P = Σ_{t=1..n} C/(1 + y)^t + F/(1 + y)^n           y = yield to maturity
```

- **Price and yield move inversely.**
- If coupon rate = yield → price = face value (par); coupon < yield → below
  par (discount); coupon > yield → above par (premium).
- **Zero-coupon bond**: P = F/(1 + y)^n.
- **Duration** measures sensitivity to rate changes: long bonds lose more when
  rates rise. ΔP/P ≈ −D_mod · Δy.
- **Credit risk**: riskier issuers pay a **spread** over government yields;
  Italian BTP-Bund spread is the classic example.
- **Yield curve**: yields by maturity; usually upward sloping; an inverted
  curve has often preceded recessions.

*Worked example.* 3-year bond, face 1,000, coupon 5 %, yield 6 %:
50/1.06 + 50/1.06² + 1,050/1.06³ = 47.17 + 44.50 + 881.60 = **€973.27**.

## Stocks

A share is a claim on a firm's residual cash flows.

- **Dividend discount model**: P₀ = D₁/(r − g) (Gordon growth). D₁ = €2,
  r = 8 %, g = 3 % → P₀ = **€40**.
- **Multiples**: P/E (price/earnings), EV/EBITDA.
- Primary market (IPO, new shares) vs secondary market (trading among
  investors on exchanges such as Borsa Italiana / Euronext Milan).

## How exchanges trade

- **Order book**: limit orders (buy at ≤ p, sell at ≥ p) wait in the book;
  market orders execute immediately against the best price.
- **Bid-ask spread**: difference between best buy and best sell — the price of
  immediacy, earned by market makers.
- **Call auctions** (opening and closing auctions) collect orders and clear at
  one price; **continuous trading** matches orders as they arrive.
- **Liquidity**: ability to trade size quickly without moving the price.

## Market efficiency

**Efficient market hypothesis** (Fama): prices reflect available information.

- **Weak form**: past prices can't predict future returns.
- **Semi-strong**: all public information is in the price.
- **Strong**: even private information is.

Evidence: markets are hard to beat consistently after costs (most active funds
underperform index funds), but anomalies exist (momentum, value, behavioural
bubbles). Grossman-Stiglitz paradox: if prices were perfectly efficient,
nobody would pay to gather information — so markets must be "efficiently
inefficient".

## Arbitrage

**Arbitrage** is a riskless profit from price differences for the same asset
(buy cheap here, sell dear there). Arbitrageurs push prices together — the
**law of one price**. Most "arbitrage" in practice carries some risk (limits
to arbitrage). Related: **no-arbitrage pricing** of derivatives.

## Derivatives in one paragraph

**Forwards/futures** lock in a future price (a farmer sells wheat forward);
**options** give the right, not the obligation, to buy (call) or sell (put) at
a strike price; **swaps** exchange cash-flow streams. Used for **hedging**
(reducing risk) or speculation.

## Summary

- Bond price = PV of coupons and face value; price ↓ when yields ↑.
- Stock value = PV of dividends (Gordon: D₁/(r − g)).
- Order books, spreads, auctions and liquidity describe trading.
- EMH and arbitrage keep prices informative — but not perfectly.
