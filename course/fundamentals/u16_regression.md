# F16 · Relationships in data: correlation and regression | Statistics

## F16.1 Scatter plots
A **scatter plot** places each observation as a point (x, y). Read:

- **direction**: positive (up-right) or negative (down-right);
- **form**: linear, curved, clusters;
- **strength**: how tightly points follow a pattern;
- **outliers**: points far from the rest.

> **Example.** Price (x) vs units sold (y) across 30 weeks: points slope down —
> higher price weeks sold less — with scatter from other factors (season,
> competitors).

@mcq Points rising from bottom-left to top-right indicate…
+ a positive relationship
- a negative relationship
- no relationship
- causation | a pattern alone doesn't prove causation.
! Direction of association.
@mcq A scatter of price vs units sold slopes downward. This is consistent with…
+ the law of demand (but other factors may matter)
- increasing supply
- proof that price causes sales
- no relationship
! Association, not proof.
@mcq Points forming a clear U shape have a correlation close to zero. This means…
+ the relationship is non-linear, not absent
- there is no relationship
- the data are wrong
- the slope is positive
! Correlation measures LINEAR association.

## F16.2 Covariance
**Covariance** measures how two variables move together:

```
cov(x, y) = Σ (xᵢ − x̄)(yᵢ − ȳ) / (n − 1)
```

Positive: above-average x goes with above-average y. Its size depends on units,
so it's hard to interpret alone.

> **Example.** x: 1, 2, 3; y: 2, 4, 9. x̄ = 2, ȳ = 5. Products: (−1)(−3) +
> 0·(−1) + (1)(4) = 7 → cov = 7/2 = **3.5**.

@num x: 2, 4, 6; y: 1, 3, 5. Sample covariance?
= 4
! Deviations (−2,0,2),(−2,0,2): 4 + 0 + 4 = 8; /2.
@num x: 1, 2, 3; y: 6, 4, 2. Sample covariance?
= -2
! (−1)(2) + 0 + (1)(−2) = −4; /2.
@mcq Measuring price in cents instead of euros multiplies the covariance with sales by…
+ 100
- 1 | covariance depends on units.
- 0.01
- 10,000
! Unit-dependent.

## F16.3 Correlation
The **correlation coefficient** standardises covariance:

```
r = cov(x, y) / (s_x · s_y)        −1 ≤ r ≤ 1
```

r = 1 perfect positive line, r = −1 perfect negative line, r ≈ 0 no **linear**
relationship. Unit-free.

> **Example.** cov = 3.5, s_x = 1, s_y = 3.606 → r = 0.97.

Rules of thumb: |r| > 0.7 strong, 0.3–0.7 moderate, < 0.3 weak (context
matters).

@num cov = 12, s_x = 3, s_y = 5. Correlation?
= 0.8
! 12/15.
@num x: 2, 4, 6; y: 1, 3, 5. Correlation?
= 1
! An exact line.
@mcq r = −0.9 between price and units sold means…
+ a strong negative linear association
- price has no effect
- a weak relationship
- a 90 % fall in sales
! Strength and direction.

## F16.4 Correlation is not causation (again)
Even strong correlations can come from:

- **confounders** (a third variable drives both);
- **reverse causality**;
- **selection** (only some units observed);
- **chance**, especially when searching through many variables.

Evidence for causation: randomised experiments, natural experiments, a
plausible mechanism, dose-response, consistency across settings.

> **Example.** Shops with more staff have higher sales — partly because busy
> shops hire more staff.

@mcq Countries with more Nobel prizes eat more chocolate. The most plausible explanation…
+ a confounder such as national income
- chocolate makes people smarter
- Nobel prizes cause chocolate eating
- it proves causation
! Common cause.
@mcq Best evidence that a discount causes higher sales?
+ a randomised A/B test
- a correlation of 0.6
- a scatter plot
- a manager's opinion
! Randomisation.
@mcq "Busy shops hire more staff" illustrates…
+ reverse causality
- a confounder only
- chance
- measurement error
! Sales cause staffing.

## F16.5 The regression line
**Simple linear regression** fits ŷ = a + b·x by **least squares**
(minimising the sum of squared vertical errors):

```
b = cov(x, y) / var(x) = r · s_y / s_x
a = ȳ − b · x̄
```

The line always passes through (x̄, ȳ).

> **Example.** x: 1, 2, 3; y: 2, 4, 9. cov 3.5, var(x) 1 → b = 3.5; a = 5 −
> 3.5·2 = −2 → ŷ = −2 + 3.5x.

@num cov(x, y) = 30, var(x) = 10. Slope b?
= 3
! 30/10.
@num Same, x̄ = 4, ȳ = 20. Intercept a?
= 8
! 20 − 3·4.
@num r = 0.5, s_y = 8, s_x = 2. Slope?
= 2
! 0.5 × 8/2.

## F16.6 Interpreting slope and intercept
- **Slope b**: the predicted change in y for a one-unit increase in x (an
  association, causal only with a good design).
- **Intercept a**: predicted y at x = 0 — often meaningless if x = 0 is far
  from the data.

> **Example.** Units sold = 900 − 30 × price (€). Each €1 increase in price is
> associated with 30 fewer units. At price €20, predicted sales = 300.

@num ŷ = 900 − 30x. Predicted y at x = 25?
= 150
! 900 − 750.
@num Same model: predicted change in y when x rises by 2?
= -60
! −30 × 2.
@mcq Weight = −100 + 1.0 × height (cm). The intercept −100 at height 0…
+ has no practical meaning: height 0 is far outside the data
- means negative weight is possible
- is the most important number
- is an error
! Extrapolation.

## F16.7 R² and residuals
A **residual** = actual − predicted: eᵢ = yᵢ − ŷᵢ.

**R²** = share of the variance of y explained by the regression:

```
R² = 1 − Σeᵢ² / Σ(yᵢ − ȳ)²       simple regression: R² = r²
```

R² = 0.64 → the model explains 64 % of the variation in y. A low R² isn't
"wrong": many outcomes have large unexplained variation.

Plot residuals: patterns (curves, fanning out) signal a misspecified model.

@num Actual 120, predicted 112. Residual?
= 8
! 120 − 112.
@num r = 0.7. R² of the simple regression?
= 0.49 %
! 0.7².
@num Total sum of squares 500, residual sum of squares 150. R²?
= 0.7 %
! 1 − 150/500.

## F16.8 Prediction and extrapolation
Use the regression to **predict** y for new x — but only **within the range
of the data**. Outside it (**extrapolation**) the linear pattern may break.

Predictions also have uncertainty: residual standard error tells you the
typical size of errors; prediction intervals are wider than the line suggests.

> **Example.** A model of sales vs price estimated with prices €10–€20 predicts
> negative sales at €40 — nonsense: demand isn't linear that far out.

@num Sales = 500 − 20 × price, fitted on prices €5–€15. Prediction at price €12?
= 260
! 500 − 240.
@mcq Same model at price €30 predicts −100. This illustrates…
+ the danger of extrapolation
- negative demand exists
- a good prediction
- a large R²
! Outside the data range.
@mcq Typical prediction error of a regression is measured by…
+ the residual standard error
- the intercept
- the slope
- the number of observations
! Spread of residuals.

## F16.9 Multiple regression (intuition)
With several explanatory variables:

```
ŷ = a + b₁x₁ + b₂x₂ + …
```

Each bᵢ is the association of xᵢ with y **holding the other x's constant** —
a statistical "ceteris paribus". Adding controls (season, competitor price)
can change a coefficient a lot when variables are correlated.

> **Example.** Sales = 1,000 − 25·price + 15·competitor_price + 200·december.
> Raising own price by €1, with the competitor's price and month fixed, is
> associated with 25 fewer units.

@num Sales = 1,000 − 25·P + 15·Pc. P = 20, Pc = 22. Predicted sales?
= 830
! 1,000 − 500 + 330.
@num Same model: effect of a €2 rise in the competitor's price?
= 30
! 15 × 2.
@mcq In multiple regression, b₁ measures the association of x₁ with y…
+ holding the other included variables constant
- ignoring all other variables
- only in December
- causally, always
! Partial effect.

## F16.10 Log models and elasticities
Taking logs turns multiplicative relations into linear ones:

```
ln(Q) = a + b · ln(P)        b = elasticity of Q with respect to P
ln(y) = a + b · x            100·b ≈ % change in y per unit of x
```

Log-log regressions of quantity on price estimate the **price elasticity**
directly: b = −1.8 means a 1 % price rise goes with 1.8 % fewer units.

> **Example.** ln(sales) = 8 − 1.5 ln(price): a 10 % price increase is
> associated with ≈ 15 % lower sales.

@num ln(Q) = 6 − 2.2 ln(P). Elasticity?
= -2.2
! The coefficient on ln(P).
@num Same model: approximate % change in Q for a 5 % price rise?
= -11 %
! −2.2 × 5.
@num ln(wage) = 2 + 0.08 × years_of_education. Approximate % wage increase per extra year?
= 8 %
! 100 × 0.08.
