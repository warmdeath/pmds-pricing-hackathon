# F15 · Sampling and inference | Statistics

## F15.1 Populations and samples
The **population** is the whole group you care about (all customers, all
transactions this year); a **sample** is the part you observe. A **parameter**
describes the population (μ, σ, p); a **statistic** is computed from the sample
(x̄, s, p̂) to estimate it.

Good samples are **random**: every member has a known chance of selection.
Bad samples are **biased**:

- **selection bias** (surveying only customers who stayed);
- **non-response bias** (only angry customers answer);
- **survivorship bias** (studying only firms that survived).

> **Example.** Asking only Monday shoppers about weekly habits misses weekend
> shoppers: a bigger sample won't fix a biased design.

@mcq The average spending of ALL our customers in 2025 is a…
+ parameter
- statistic | it describes the population.
- sample
- bias
! Population quantity.
@mcq Studying only companies still listed today to measure "average stock returns" suffers from…
+ survivorship bias
- non-response bias
- random error only
- no bias
! Failed firms are missing.
@mcq Doubling the size of a biased sample…
+ doesn't remove the bias
- removes the bias
- doubles the bias
- makes it random
! Bias is about design, not size.

## F15.2 Sampling distributions
A statistic varies from sample to sample. Its distribution across repeated
samples is the **sampling distribution**. For the sample mean of n
independent observations:

```
E[x̄] = μ           SD(x̄) = σ / √n       (the standard error)
```

By the central limit theorem, x̄ is approximately normal for large n.

> **Example.** Order values: μ = €60, σ = €30. Samples of 100 orders: the
> sample mean has SD 30/10 = €3; about 95 % of sample means fall in
> €54–€66.

@num σ = 40, n = 64. Standard error of the mean?
= 5
! 40/8.
@num σ = 12. Sample size needed for a standard error of 1.5?
= 64
! (12/1.5)² = 64.
@mcq Quadrupling the sample size makes the standard error…
+ half as large
- a quarter as large | it scales with √n.
- twice as large
- unchanged
! √4 = 2.

## F15.3 Standard error of a proportion
For a proportion (share of customers who buy, defect rate):

```
p̂ = successes / n          SE(p̂) = √( p̂(1 − p̂) / n )
```

> **Example.** 120 of 400 visitors bought: p̂ = 0.30, SE = √(0.3·0.7/400) =
> 0.0229.

The SE is largest at p̂ = 0.5; to halve it, quadruple n.

@num 50 of 200 customers churned. p̂?
= 0.25 %
! 50/200.
@num Same: standard error of p̂ (4 decimals)?
= 0.0306 ~0.0005
! √(0.25·0.75/200) = 0.0306.
@num p̂ = 0.5, n = 400. SE?
= 0.025
! √(0.25/400).

## F15.4 Confidence intervals for a mean (σ known)
A **confidence interval** gives a range of plausible values for a parameter:

```
x̄ ± z* · σ/√n           z* = 1.645 (90 %), 1.96 (95 %), 2.576 (99 %)
```

Interpretation: if we repeated the sampling many times, 95 % of such intervals
would contain μ. It is **not** "μ is in this interval with 95 % probability"
in the strict frequentist sense, though that's the practical reading.

> **Example.** x̄ = 52, σ = 10, n = 100 → 52 ± 1.96 = **[50.04, 53.96]**.

@num x̄ = 80, σ = 20, n = 64, 95 %. Lower bound?
= 75.1 ~0.01
! 80 − 1.96 × 2.5.
@num Same: margin of error (half-width)?
= 4.9 ~0.01
! 1.96 × 2.5.
@mcq A 99 % interval compared with a 95 % interval from the same data is…
+ wider
- narrower
- the same
- shifted
! More confidence needs a wider net.

## F15.5 t-intervals (σ unknown)
Usually σ is unknown and estimated by s. Then use the **t distribution** with
n − 1 degrees of freedom:

```
x̄ ± t* · s/√n
```

t* is larger than z* for small samples (fatter tails) and approaches z* as n
grows. Some 95 % values: t*(df 9) = 2.262, t*(df 24) = 2.064, t*(df 99) ≈ 1.984.

> **Example.** n = 25, x̄ = 120, s = 15: 120 ± 2.064 × 3 = **[113.8, 126.2]**.

@num n = 10, x̄ = 50, s = 6. 95 % margin of error using t* = 2.262?
= 4.292 ~0.005
! 2.262 × 6/√10 = 2.262 × 1.897.
@num n = 100, x̄ = 30, s = 5. 95 % CI upper bound using t* = 1.984?
= 30.992 ~0.005
! 30 + 1.984 × 0.5.
@mcq For small samples with unknown σ, intervals use t instead of z because…
+ estimating σ adds uncertainty (fatter tails)
- t is always smaller
- data are not numeric
- it's tradition
! Extra uncertainty from s.

## F15.6 Confidence interval for a proportion
```
p̂ ± z* · √( p̂(1 − p̂)/n )
```

Valid when n·p̂ and n·(1 − p̂) are both at least about 10.

> **Example.** Poll: 540 of 1,200 prefer product A: p̂ = 0.45, SE = 0.01436;
> 95 % CI = 0.45 ± 0.028 = **[0.422, 0.478]**.

Sample size for a desired margin m (worst case p = 0.5):
n = (z*/m)² × 0.25. For ±3 % at 95 %: n ≈ 1,067.

@num 300 of 600 respond positively. 95 % margin of error (4 decimals)?
= 0.04 ~0.0005
! 1.96 × √(0.25/600) = 0.0400.
@num Worst-case sample size for a ±5 % margin at 95 %? (round up)
= 385 ~1
! (1.96/0.05)² × 0.25 = 384.2 → 385.
@mcq To halve the margin of error you must multiply the sample size by…
+ 4
- 2 | the margin falls with √n.
- 8
- 0.5
! √4 = 2.

## F15.7 Hypothesis testing: the logic
A **hypothesis test** asks whether data are consistent with a claim.

1. **Null hypothesis H₀**: the default ("no effect", "μ = 100").
2. **Alternative H₁**: what you want evidence for ("μ ≠ 100", "> 100").
3. Compute a **test statistic** measuring distance from H₀ in standard errors.
4. Compute the **p-value**: probability of data at least this extreme if H₀
   were true.
5. If p-value < **α** (often 0.05), reject H₀.

Not rejecting H₀ is **not** proof that H₀ is true — maybe the sample was too
small.

@mcq A p-value of 0.03 with α = 0.05 means…
+ reject H₀: data this extreme would be rare if H₀ were true
- accept H₁ with 97 % certainty | the p-value is not P(H₁).
- H₀ is true
- the effect is large | significance ≠ size.
! p < α → reject.
@mcq Failing to reject H₀ means…
+ the data don't provide enough evidence against H₀
- H₀ is proven true
- H₁ is true
- the test failed
! Absence of evidence ≠ evidence of absence.
@mcq "The new price doesn't change average sales" is a typical…
+ null hypothesis
- alternative hypothesis
- p-value
- confidence level
! The default "no effect".

## F15.8 The z-test for a mean
```
z = (x̄ − μ₀) / (σ/√n)
```

Two-sided test at α = 0.05: reject if |z| > 1.96. One-sided (H₁: μ > μ₀):
reject if z > 1.645.

> **Example.** Claimed mean delivery time 48 h; sample n = 36, x̄ = 51, σ = 9.
> z = 3/(9/6) = 2 > 1.96 → reject: deliveries take longer than claimed.

@num μ₀ = 100, x̄ = 104, σ = 12, n = 36. z statistic?
= 2
! 4/(12/6).
@num μ₀ = 50, x̄ = 48.5, σ = 6, n = 16. z statistic?
= -1
! −1.5/1.5.
@mcq In the previous question, two-sided α = 0.05: decision?
+ do not reject H₀ (|z| = 1 < 1.96)
- reject H₀
- accept H₁
- impossible to say
! Not enough evidence.

## F15.9 p-values in practice
For a z statistic:

- two-sided p = 2 × (1 − Φ(|z|));
- one-sided p = 1 − Φ(z) (in the direction of H₁).

| z | 1.0 | 1.5 | 1.645 | 1.96 | 2.0 | 2.58 |
| --- | --- | --- | --- | --- | --- | --- |
| two-sided p | 0.317 | 0.134 | 0.10 | 0.05 | 0.0455 | 0.01 |

Small p-values say the data are surprising **under H₀**; they don't measure
importance. With huge samples, trivial differences become "significant".

@num z = 2 (Φ(2) = 0.9772). Two-sided p-value?
= 0.0456 ~0.0005 %
! 2 × 0.0228.
@num z = 1.5 (Φ(1.5) = 0.9332). One-sided p-value?
= 0.0668 ~0.0005 %
! 1 − 0.9332.
@mcq With 10 million observations a 0.1 % difference is "highly significant". This shows…
+ statistical significance ≠ practical importance
- the difference is large
- the test is wrong
- p-values can't be small
! Huge n detects tiny effects.

## F15.10 Errors, significance level and power
| | H₀ true | H₀ false |
| --- | --- | --- |
| reject H₀ | **Type I error** (false alarm), prob α | correct (power) |
| don't reject | correct | **Type II error** (miss), prob β |

- Lowering α reduces false alarms but increases misses.
- **Power** = 1 − β: probability of detecting a real effect; grows with
  sample size and effect size.

> **Example.** A fraud alarm that flags everything has no Type II errors but
> many Type I errors.

@mcq Concluding a new ad works when in reality it doesn't is a…
+ Type I error
- Type II error | that's missing a real effect.
- correct decision
- power
! False positive.
@num α = 0.05, β = 0.2. Power of the test?
= 0.8 %
! 1 − 0.2.
@mcq To increase power without changing α, the simplest way is…
+ increase the sample size
- decrease the sample size
- use a two-sided test always
- ignore the data
! More data → smaller SE.

## F15.11 Comparing two groups
To compare two means (A/B tests, two regions):

```
z (or t) = (x̄_A − x̄_B) / √( s_A²/n_A + s_B²/n_B )
```

For two proportions: (p̂_A − p̂_B)/√(p̂(1 − p̂)(1/n_A + 1/n_B)) with the pooled p̂.

> **Example.** Price A: 1,000 visitors, 50 buy (5 %). Price B: 1,000, 70 buy
> (7 %). Pooled p̂ = 0.06; SE = √(0.06·0.94·0.002) = 0.0106; z = 0.02/0.0106 =
> 1.88 → p ≈ 0.06: suggestive, not significant at 5 %.

@num Means 52 and 48; s_A = 10, s_B = 10; n_A = n_B = 50. Test statistic?
= 2
! SE = √(2 + 2) = 2; 4/2.
@num A: 40/400 convert; B: 60/400. Pooled conversion rate?
= 0.125 %
! 100/800.
@mcq In an A/B test, the key requirement for a causal conclusion is…
+ random assignment of visitors to A or B
- large revenue
- a two-sided test
- equal prices
! Randomisation removes confounders.

## F15.12 Statistical thinking checklist
Before trusting any number:

1. **Where do the data come from?** Random sample? Biased?
2. **How big is the sample?** What's the standard error?
3. **Compared with what?** Baseline, control group, last year.
4. **Is the difference larger than the noise?** Interval, test.
5. **Is it large enough to matter?** Practical significance.
6. **Could something else explain it?** Confounders, seasonality.
7. **Would it replicate?** Many tests → some false positives (5 % of 20 tests
   ≈ 1 false alarm).

@num You run 40 independent tests at α = 0.05 where no real effects exist. Expected number of false positives?
= 2
! 40 × 0.05.
@mcq Sales rose 3 % after a website change; normal week-to-week variation is ±8 %. The best conclusion is…
+ the change is within normal noise; no evidence yet
- the change caused a 3 % rise
- the change hurt sales
- variation doesn't matter
! Compare the effect with the noise.
@mcq Which question is NOT on the checklist?
+ "Which result do I prefer?"
- "Compared with what?"
- "Is the difference larger than the noise?"
- "Could something else explain it?"
! Preferences are not evidence.
