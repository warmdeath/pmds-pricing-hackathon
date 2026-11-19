# 3.6 Risk, return and diversification

## The big picture

Investors demand higher expected returns for bearing risk. But not all risk is
rewarded: risk that can be removed by **diversification** earns nothing; only
**systematic** (market) risk carries a premium. This lesson builds the
portfolio theory behind that statement and the CAPM.

> **Analogy.** Selling umbrellas and sunglasses on the same beach: each
> business alone is risky (it depends on the weather), together the income is
> steady. That is diversification.

## Return and risk of one asset

- Holding-period return = (P₁ − P₀ + dividend)/P₀.
- Expected return E[R] = Σ p_s R_s; risk = standard deviation σ.

*Worked example.* Boom (p 0.3) +30 %, normal (0.5) +10 %, recession (0.2)
−20 %: E[R] = 9 + 5 − 4 = **10 %**. Variance = 0.3·0.04 + 0.5·0 + 0.2·0.09 =
0.03 → σ = **17.3 %**.

## Portfolios

For a two-asset portfolio with weights w and 1 − w:

```
E[R_p] = w·E[R_A] + (1 − w)·E[R_B]
σ_p²   = w²σ_A² + (1 − w)²σ_B² + 2w(1 − w)·ρ·σ_A·σ_B
```

The expected return is a weighted average, but the risk is **less** than the
weighted average whenever the correlation ρ < 1. With ρ = −1, risk can be
eliminated entirely.

*Worked example.* σ_A = 20 %, σ_B = 30 %, ρ = 0, w = 0.5:
σ_p = √(0.25·0.04 + 0.25·0.09) = √0.0325 = **18.0 %** (< 25 % average).

## Diversifiable vs systematic risk

Adding many stocks drives portfolio variance down towards the **average
covariance**: firm-specific (idiosyncratic) risk disappears; market-wide
(systematic) risk remains. Because diversification is nearly free, markets do
not reward idiosyncratic risk.

## Efficient frontier and the CAPM

- The **efficient frontier** contains portfolios with the highest return for
  each level of risk (Markowitz).
- Adding a risk-free asset, all investors hold the same risky **market
  portfolio** combined with the risk-free asset (**capital market line**).
- **CAPM**: the expected return of any asset depends on its **beta**:

```
E[R_i] = R_f + β_i · (E[R_m] − R_f)          β_i = Cov(R_i, R_m) / Var(R_m)
```

*Worked example.* R_f = 3 %, market premium 6 %, β = 1.5 → E[R] = **12 %**.

β = 1 moves with the market; β > 1 amplifies it; β < 1 dampens it.

## Risk and leverage

Borrowing to invest amplifies both expected return and risk. Equity in a
levered firm is riskier than the firm's assets (Modigliani-Miller:
r_E = r_A + (D/E)(r_A − r_D)). Leverage turns small asset losses into large
equity losses — and can lead to insolvency.

## Risk in operations

The same ideas apply to a firm's operating choices: concentrating on one
product or one input supplier increases risk; spreading across products,
customers or suppliers reduces variance if their shocks are not perfectly
correlated. Whether to reduce variance depends on objectives: if what matters
is the average outcome, variance is not costly in itself; if the objective
punishes bad outcomes more than it rewards good ones (bankruptcy,
thresholds, ranks), variance matters.

## Measuring risk-adjusted performance

- **Sharpe ratio** = (R_p − R_f)/σ_p: excess return per unit of total risk.
- **Value at Risk** (VaR): loss not exceeded with a given probability.
- **Maximum drawdown**: largest peak-to-trough fall.

## Summary

- Expected return and σ describe one asset; portfolio risk depends on
  correlations.
- Diversification removes idiosyncratic risk; only systematic risk is priced.
- CAPM: E[R] = R_f + β(E[R_m] − R_f).
- Leverage amplifies risk; risk matters most when outcomes have thresholds.
