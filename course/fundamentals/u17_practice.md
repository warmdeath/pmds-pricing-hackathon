# F17 · Statistics at work | Statistics

## F17.1 Moving averages and trends
A **moving average** of the last k values smooths short-term noise to reveal
the trend. Larger k → smoother but slower to react.

A **centred** moving average is used for describing the past; a **trailing**
moving average (last k values) for forecasting.

> **Example.** Weekly sales 20, 24, 22, 30, 28, 34. Trailing 3-week averages:
> 22, 25.33, 26.67, 30.67 — the upward trend is clearer than in the raw
> data.

Moving averages lag behind turning points: when the trend changes, the
average notices late.

@num Sales 40, 44, 48, 52. 4-period moving average?
= 46
! 184/4.
@num Sales 10, 14, 12, 18, 20. Trailing 3-period moving average at the last period?
= 16.67 ~0.01
! (12 + 18 + 20)/3.
@mcq Increasing the moving-average window from 3 to 12 periods makes it…
+ smoother but slower to react
- noisier and faster
- unchanged
- more accurate always
! Trade-off between smoothing and lag.

## F17.2 Seasonality
**Seasonality** is a regular pattern that repeats with a fixed period (week,
month, year). Measure it with **seasonal indices**: average value in a season /
overall average.

> **Example.** Quarterly sales averages: Q1 80, Q2 100, Q3 90, Q4 130; overall
> 100 → indices 0.8, 1.0, 0.9, 1.3. A Q4 with 117 sales is **below** normal
> once adjusted: 117/1.3 = 90 deseasonalised.

Compare like with like: this December vs last December, or use seasonally
adjusted figures.

@num Overall monthly average 200; average December sales 280. December seasonal index?
= 1.4
! 280/200.
@num Seasonal index for August 0.6; August sales 150. Deseasonalised sales?
= 250
! 150/0.6.
@mcq Sales rose 40 % from November to December. Before concluding the promotion worked, check…
+ the usual November-to-December seasonal change
- the colour of the website
- next year's budget
- nothing
! Seasonality may explain it.

## F17.3 Measuring forecast accuracy
Forecast error eₜ = actual − forecast. Summaries:

- **MAE** = mean |eₜ| (in units);
- **MAPE** = mean |eₜ / actual| × 100 (in %);
- **RMSE** = √(mean eₜ²) (punishes big errors);
- **bias** = mean eₜ (systematically too high or too low?).

> **Example.** Actuals 100, 120, 80; forecasts 110, 110, 90 → errors −10, +10,
> −10: MAE 10, bias −3.33 (forecasts slightly high), MAPE (10 % + 8.33 % +
> 12.5 %)/3 = 10.28 %.

@num Errors −4, 6, −2. MAE?
= 4
! (4 + 6 + 2)/3.
@num Same errors: bias (mean error)?
= 0
! (−4 + 6 − 2)/3.
@num Actuals 50 and 200; forecasts 60 and 180. MAPE (%)?
= 15 %
! (20 % + 10 %)/2.

## F17.4 A/B testing in business
An **A/B test** randomly splits customers (or periods, or stores) between two
versions and compares an outcome (conversion, revenue per visitor).

Good practice:

- decide the **metric** and **sample size** before starting;
- **randomise** and run both versions **at the same time**;
- don't stop early as soon as it "looks significant" (peeking inflates false
  positives);
- check **practical** size, not only significance;
- watch for side effects (revenue per visitor, not just conversion).

> **Example.** Price €20: 4.0 % conversion; price €24: 3.5 %. Revenue per
> visitor: €0.80 vs €0.84 → the higher price earns more per visitor despite
> lower conversion.

@num Version A: 5 % conversion at €30; version B: 4 % at €40. Revenue per visitor of B minus A (€)?
= 0.1
! 1.60 − 1.50.
@mcq Running version A in May and version B in June is a poor test because…
+ other things change between months (season, competitors)
- May is too short
- B is always better
- it's illegal
! Run them simultaneously.
@mcq Stopping a test the first day p < 0.05 appears…
+ raises the false-positive rate
- is best practice
- lowers false positives
- has no effect
! Peeking problem.

## F17.5 Expected value decisions with data
Combine probability estimates from data with payoffs to choose actions.

> **Example.** Past data: 30 % of discounted offers convert (profit €50 each),
> 20 % of full-price offers convert (profit €90 each). Expected profit per
> offer: discount €15, full price €18 → full price, *if* the samples are
> comparable.

Sensitivity: how wrong could the probabilities be before the decision flips?
Here, full price wins as long as its conversion is above 15/90 = 16.7 %.

@num Option A: 40 % chance of €30 profit. Option B: 25 % chance of €60. Expected profit of B minus A (€)?
= 3
! 15 − 12.
@num In the lesson example, minimum full-price conversion at which full price still matches the discount (%)?
= 16.67 % ~0.02
! 15/90.
@mcq Expected-value decisions are most appropriate when…
+ the decision is repeated many times and no single loss is catastrophic
- a single loss could bankrupt you
- probabilities are unknown and unknowable
- payoffs are infinite
! Long-run averages apply.

## F17.6 Simulation (Monte Carlo)
When a problem is too complex for formulas, **simulate** it: draw random
inputs many times from their distributions, compute the outcome each time,
and study the distribution of results.

Steps: model → random inputs → many runs (1,000+) → summarise (mean,
percentiles, probability of loss).

> **Example.** Profit = (price − cost) × demand − fixed, with uncertain demand
> and cost. 10,000 runs show mean profit €12k, 10 % chance of a loss, 5th
> percentile −€4k.

More runs reduce the simulation's own noise (by √n).

@num In 2,000 simulation runs, 140 show a loss. Estimated probability of loss (%)?
= 7 %
! 140/2,000.
@num A simulated mean has SD 400 across single runs. Standard error of the mean of 10,000 runs?
= 4
! 400/√10,000.
@mcq Monte Carlo simulation is mainly useful to…
+ study the distribution of outcomes when inputs are uncertain
- avoid any assumptions
- find exact formulas
- remove uncertainty
! It quantifies risk.

## F17.7 Data pitfalls: Simpson's paradox and friends
**Simpson's paradox**: a trend in every group reverses when groups are
combined, because the group sizes differ.

> **Example.** Two shops. Promotion A converts better than B **in each shop**,
> but A was used mostly in the low-converting shop, so overall A looks worse.
> Always check whether a comparison mixes groups with different baselines.

Other pitfalls: **regression to the mean** (extreme results tend to be followed
by less extreme ones — the "Sports Illustrated jinx"); **survivorship**;
**look-elsewhere** (searching many variables until something correlates).

@mcq Last month's worst-performing store improved this month after a manager was replaced. A cautious analyst first suspects…
+ regression to the mean
- the new manager is a genius
- data error
- seasonality only
! Extreme results tend to move back towards average.
@mcq Each department shows women hired at a higher rate than men, but overall the rate is lower. This is…
+ Simpson's paradox
- survivorship bias
- a Type II error
- impossible
! Group composition differs.
@num Shop 1: A 30/100, B 280/1,000. Shop 2: A 50/1,000, B 4/100. Overall conversion of A (%)?
= 7.27 % ~0.02
! 80/1,100.

## F17.8 Communicating numbers
Good quantitative communication:

- lead with the **answer** and its **uncertainty** ("revenue +8 % ± 3 %");
- give **context**: compared with what, over what period;
- round sensibly (3 significant figures);
- prefer **absolute and relative** together ("+€2 m, +4 %");
- choose the **right chart** (F3.5) and label axes and units;
- state **assumptions** and **limitations**.

> **Example.** Weak: "Sales improved." Strong: "Weekly units rose from 1,200 to
> 1,320 (+10 %) in the 4 weeks after the price change; normal week-to-week
> variation is ±4 %, so the rise is unlikely to be noise."

@mcq Which is the best summary?
+ "Units +10 % (1,200 → 1,320) vs normal variation ±4 %"
- "Sales went up a lot"
- "Units: 1,320"
- "Sales increased 10%!!!"
! Answer, context and uncertainty.
@num Revenue €48.3 m → €50.2 m. Relative change to one decimal (%)?
= 3.9 % ~0.05
! 1.9/48.3.
@mcq Why give both absolute and relative changes?
+ each alone can mislead (big % of a tiny base, or small % of a huge one)
- to make reports longer
- regulations require it
- they're the same
! Context.
