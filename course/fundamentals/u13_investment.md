# F13 · Investment and financing basics | Accounting & finance

## F13.1 Net present value (NPV)
To judge an investment, bring all its cash flows to today and add them:

```
NPV = −C₀ + CF₁/(1+r) + CF₂/(1+r)² + … + CFₙ/(1+r)ⁿ
```

**Rule**: invest if NPV > 0 — the project earns more than the opportunity
cost r. NPV is in euros of value created today.

> **Example.** Invest €1,000; receive €600 in each of 2 years; r = 10 %.
> NPV = −1,000 + 545.45 + 495.87 = **+€41.32** → accept.

@num Invest €2,000, receive €1,200 in each of 2 years, r = 8 %. NPV (€)?
= 139.92 ~0.05
! −2,000 + 1,111.11 + 1,028.81.
@num Invest €500, receive €550 in 1 year, r = 12 %. NPV (€)?
= -8.93 ~0.02
x 50 | discount the €550 at 12 %.
! 550/1.12 − 500.
@mcq Two mutually exclusive projects: NPV €120k and €90k. Choose…
+ the one with NPV €120k
- the cheaper one
- the faster one
- both
! Highest value created.

## F13.2 Internal rate of return (IRR)
The **IRR** is the discount rate that makes NPV = 0 — the project's own rate
of return. Rule: accept if IRR > cost of capital.

Simple cases can be solved directly:

- One-period: IRR = CF₁/C₀ − 1.
- C₀ now, single CFₙ later: IRR = (CFₙ/C₀)^(1/n) − 1.

For mutually exclusive projects of different size or timing, IRR can mislead;
NPV is the reliable criterion.

> **Example.** Invest 1,000, get 1,331 in 3 years → IRR = 1.331^(1/3) − 1 = 10 %.

@num Invest €800, receive €920 in one year. IRR (%)?
= 15 %
! 920/800 − 1.
@num Invest €1,000, receive €1,440 in 2 years. IRR (%)?
= 20 %
! √1.44 − 1.
@mcq IRR 14 %, cost of capital 10 %. The project's NPV at 10 % is…
+ positive
- negative
- zero
- undefined
! Discounting at a rate below the IRR gives NPV > 0.

## F13.3 Payback and its limits
**Payback period** = time until cumulative cash flows recover the investment.

> **Example.** Invest 1,000; flows 300, 400, 500 → after 2 years 700; 300 more
> needed out of 500 in year 3 → payback **2.6 years**.

Payback is simple and focuses on risk/liquidity, but ignores the time value of
money (unless discounted payback) and everything after the payback date.

@num Invest €900; flows €300 per year. Payback (years)?
= 3
! 900/300.
@num Invest €1,000; flows 400, 400, 600. Payback (years)?
= 2.33 ~0.01
! 800 after 2 years; 200/600 of year 3.
@mcq Main weakness of the payback rule?
+ it ignores cash flows after payback and the time value of money
- it's hard to compute
- it uses accounting profit
- it always rejects good projects
! Short-sighted.

## F13.4 Bonds
A **bond** is a loan in tradable form. It pays **coupons** (face × coupon rate)
and repays the **face value** at maturity.

```
price = Σ coupon/(1+y)^t + face/(1+y)^n          y = yield to maturity
```

- Price and yield move **inversely**.
- Coupon rate = yield → price = face (par).
- Zero-coupon: price = face/(1+y)^n.

> **Example.** Face 100, coupon 5 %, 2 years, yield 4 %: 5/1.04 + 105/1.04² =
> 4.81 + 97.08 = **101.89**.

@num Zero-coupon bond, face €1,000, 3 years, yield 5 %. Price (€)?
= 863.84 ~0.05
! 1,000/1.05³.
@num Bond: face €100, coupon 6 %, 1 year left, yield 4 %. Price (€)?
= 101.92 ~0.01
! 106/1.04.
@mcq When market interest rates rise, existing bond prices…
+ fall
- rise
- don't change
- double
! Fixed payments are worth less.

## F13.5 Shares and dividends
A **share** is a fraction of ownership: a claim on future profits (dividends)
and on the firm's value.

```
dividend yield = dividend / price
total return   = (P₁ − P₀ + dividend) / P₀
Gordon model   P₀ = D₁ / (r − g)
```

> **Example.** Bought at €40, dividend €2, price after a year €44 → return =
> (4 + 2)/40 = **15 %**.

Shareholders are paid **after** creditors: higher risk, higher expected return.

@num Bought at €50, dividend €1.50, sold at €54. Total return (%)?
= 11 %
! (4 + 1.5)/50.
@num Next dividend €3, growth 2 %, required return 8 %. Gordon price (€)?
= 50
! 3/0.06.
@num Price €80, annual dividend €2.40. Dividend yield (%)?
= 3 %
! 2.4/80.

## F13.6 Risk and return
Investors demand a higher **expected return** for more **risk** (variability
of outcomes). Measure risk with the standard deviation of returns.

| asset | typical expected return | risk |
| --- | --- | --- |
| government bills | low | very low |
| corporate bonds | medium | medium |
| shares | higher | high |

The **risk premium** = expected return − risk-free rate. The **Sharpe ratio**
= risk premium / SD: return per unit of risk.

> **Example.** Fund A: 8 %, SD 10 %; fund B: 12 %, SD 20 %; risk-free 2 %.
> Sharpe A = 0.6, B = 0.5 → A offers more return per unit of risk.

@num Expected return 9 %, risk-free 3 %, SD 15 %. Sharpe ratio?
= 0.4
! 6/15.
@num Returns −10 % or +30 % with equal probability. Expected return (%)?
= 10 %
! (−10 + 30)/2.
@num Returns −10 % or +30 % with equal probability. Standard deviation (%)?
= 20 % ~0.05
! Deviations ±20.

## F13.7 Diversification
Combining assets whose returns are not perfectly correlated reduces risk
without reducing expected return proportionally. For two assets with weights
w and 1 − w:

```
σ² = w²σ₁² + (1−w)²σ₂² + 2w(1−w)ρσ₁σ₂
```

ρ = 1: no benefit; ρ = 0: big benefit; ρ = −1: risk can vanish.
**Idiosyncratic** risk diversifies away; **systematic** (market) risk doesn't.

> **Example.** Two assets, each σ = 20 %, ρ = 0, half in each: σ = √(0.01 +
> 0.01) = 14.1 %.

@num σ₁ = σ₂ = 30 %, ρ = 0, 50/50. Portfolio σ (%)?
= 21.21 % ~0.05
! √(0.25·0.09·2) = 0.2121.
@num σ₁ = σ₂ = 30 %, ρ = 1, 50/50. Portfolio σ (%)?
= 30 %
! No diversification at ρ = 1.
@mcq Which risk can diversification remove?
+ firm-specific (idiosyncratic) risk
- market-wide risk
- all risk
- none
! Systematic risk remains.

## F13.8 Debt, equity and leverage
Firms finance assets with **debt** (fixed claims, interest, must be repaid)
and **equity** (residual claims). **Leverage** (more debt) amplifies returns
to equity both ways.

> **Example.** Assets €100 earn 10 % (€10). All equity: ROE 10 %. With €50 debt
> at 4 % (interest €2): profit 8 on equity 50 → ROE **16 %**. If assets earn
> only 2 % (€2): profit 0 → ROE 0 % (vs 2 % unlevered).

Too much debt raises the risk of insolvency.

@num Assets €200 earn 8 %; debt €100 at 5 %; no taxes. ROE (%)?
= 11 %
! (16 − 5)/100.
@num Assets €200 earn 3 %; debt €100 at 5 %; no taxes. ROE (%)?
= 1 %
! (6 − 5)/100.
@num Debt €60, equity €40. Debt-to-equity ratio?
= 1.5
! 60/40.

## F13.9 Liquidity and solvency
- **Liquidity**: can the firm pay its bills **now**? Cash and assets quickly
  convertible to cash vs short-term obligations.
- **Solvency**: are assets worth more than liabilities in the **long run**?

A firm can be solvent but illiquid (valuable assets, no cash this month) — or
liquid but insolvent. Running out of cash or having negative capital ends a
firm's life even if the business model is sound.

> **Example.** €2 m of factories, €10k of cash, €200k of bills due this week:
> solvent, illiquid.

@mcq A firm with valuable property but no cash to pay this week's wages is…
+ solvent but illiquid
- insolvent and illiquid
- liquid but insolvent
- fine
! Assets exist but aren't cash.
@num Cash €30k, receivables due this month €50k, bills due this month €95k. Shortfall (€k)?
= 15
! 95 − 80.
@mcq Which asset is usually LEAST liquid?
+ specialised machinery
- cash
- short-term deposits
- receivables due next week
! Hard to sell quickly at full value.

## F13.10 Cost of capital
The **cost of capital** is the return investors require to fund the firm —
the discount rate for its projects. With debt and equity:

```
WACC = E/V · r_E + D/V · r_D · (1 − tax)
```

> **Example.** 60 % equity at 10 %, 40 % debt at 5 %, tax 25 % → WACC =
> 6 + 1.5 = **7.5 %**.

A project should earn more than the WACC (for average-risk projects) to
create value.

@num 70 % equity at 12 %, 30 % debt at 4 %, tax 25 %. WACC (%)?
= 9.3 %
! 8.4 + 0.9.
@num 50 % equity at 9 %, 50 % debt at 5 %, no tax. WACC (%)?
= 7 %
! 4.5 + 2.5.
@mcq A project returns 6 % while the WACC is 8 %. It…
+ destroys value
- creates value
- breaks even
- can't be judged
! Returns below the cost of capital.
