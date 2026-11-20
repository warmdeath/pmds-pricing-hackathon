# F12 · Random variables and distributions | Statistics

## F12.1 Random variables
A **random variable** X assigns a number to each outcome of an experiment:
daily demand, number of defective units, profit of a project.

- **Discrete**: countable values (0, 1, 2, …) — described by a probability
  for each value, P(X = x), summing to 1.
- **Continuous**: any value in an interval (time, weight, price) — described by
  a density; probabilities are areas: P(a ≤ X ≤ b).

> **Example.** Daily orders X: P(0) = 0.1, P(1) = 0.3, P(2) = 0.4, P(3) = 0.2.
> P(X ≥ 2) = 0.6.

@num Daily orders X: P(0) = 0.1, P(1) = 0.3, P(2) = 0.4, P(3) = 0.2. P(X ≤ 1)?
= 0.4 %
! 0.1 + 0.3.
@num P(X=0)=0.2, P(X=1)=0.5, P(X=2)=k. What is k?
= 0.3 %
! Probabilities sum to 1.
@mcq The time a customer spends in a shop is a…
+ continuous random variable
- discrete random variable | time can take any value.
- constant
- categorical variable
! Continuous measurement.

## F12.2 Expected value of a random variable
```
E[X] = Σ x · P(X = x)
```

It is the **long-run average** of X.

> **Example.** Using F12.1: E[X] = 0·0.1 + 1·0.3 + 2·0.4 + 3·0.2 = **1.7**
> orders per day.

The expected value need not be a possible value (1.7 orders). Linearity:
E[a + bX] = a + b·E[X]; E[X + Y] = E[X] + E[Y] (always, even if dependent).

@num X: 10 w.p. 0.5, 20 w.p. 0.3, 50 w.p. 0.2. E[X]?
= 21
! 5 + 6 + 10.
@num E[X] = 4. E[3X + 5]?
= 17
! 3·4 + 5.
@num Daily demand has mean 12 units, price €15. Expected daily revenue if all demand is served (€)?
= 180
! 15 × 12.

## F12.3 Variance of a random variable
```
Var(X) = E[(X − μ)²] = E[X²] − μ²         SD = √Var
```

Rules: Var(a + bX) = b²·Var(X) (adding a constant doesn't change spread);
for **independent** X and Y: Var(X + Y) = Var(X) + Var(Y). Standard deviations
do **not** add.

> **Example.** X = 0 or 10 with prob 0.5 each: μ = 5, Var = 0.5·25 + 0.5·25 =
> 25, SD = 5.

@num X = 0 w.p. 0.5 and 4 w.p. 0.5. Variance?
= 4
! μ = 2; 0.5·4 + 0.5·4.
@num Var(X) = 9. Var(2X + 3)?
= 36
x 21 | constants don't add variance and the multiplier is squared.
! 4 × 9.
@num Independent X, Y with SD 3 and 4. SD of X + Y?
= 5
x 7 | variances add, not standard deviations.
! √(9 + 16).

## F12.4 The Bernoulli distribution
A **Bernoulli** variable is 1 ("success") with probability p and 0 otherwise:
a customer buys or not, a bid wins or not.

```
E[X] = p        Var(X) = p(1 − p)
```

Variance is largest at p = 0.5 (maximum uncertainty). Many business events are
Bernoulli: a lead converts or not, a delivery is late or not, a product is
defective or not. Summing many of them gives the binomial (next lesson).

> **Example.** A visitor buys with p = 0.04: mean 0.04, variance 0.0384.

@num p = 0.3. Variance of a Bernoulli variable?
= 0.21
! 0.3 × 0.7.
@num A bid wins with probability 0.25 and then earns €400. Expected profit (€)?
= 100
! 0.25 × 400.
@mcq For which p is a Bernoulli variance largest?
+ 0.5
- 1 | at p = 1 there is no uncertainty.
- 0.1
- 0
! p(1 − p) peaks at 0.5.

## F12.5 The binomial distribution
Number of successes in n **independent** trials with the same p:

```
P(X = k) = C(n,k) · p^k · (1 − p)^(n−k)
E[X] = n·p        Var(X) = n·p·(1 − p)
```

> **Example.** 10 customers, each buys with p = 0.2. P(exactly 2 buy) =
> 45 · 0.04 · 0.8⁸ = **0.302**. Expected buyers 2, SD √1.6 = 1.26.

@num n = 5, p = 0.5. P(X = 2)?
= 0.3125 %
! C(5,2)·0.5⁵ = 10/32.
@num n = 20, p = 0.1. Expected number of successes?
= 2
! 20 × 0.1.
@num n = 100, p = 0.3. Standard deviation of X?
= 4.583 ~0.005
! √(100·0.3·0.7) = √21.
@num n = 4, p = 0.2. P(X = 0)?
= 0.4096 %
! 0.8⁴.

## F12.6 The Poisson distribution
Counts of events in a fixed interval (customers per hour, orders per day,
defects per batch) when events occur independently at an average rate λ:

```
P(X = k) = e^(−λ) λ^k / k!        E[X] = Var(X) = λ
```

> **Example.** On average 3 customers arrive per 10 minutes. P(no customer) =
> e^(−3) = 0.0498; P(exactly 2) = e^(−3)·9/2 = 0.224.

@num λ = 2. P(X = 0)?
= 0.1353 ~0.0005 %
! e^(−2).
@num λ = 2. P(X = 1)?
= 0.2707 ~0.0005 %
! 2e^(−2).
@num A Poisson count has mean 6. Its variance?
= 6
! Mean = variance = λ.

## F12.7 Continuous distributions and the uniform
For a continuous X, probabilities are **areas under the density**; P(X = one
exact value) = 0.

**Uniform on [a, b]**: every value equally likely.

```
P(c ≤ X ≤ d) = (d − c)/(b − a)      E[X] = (a + b)/2     Var = (b − a)²/12
```

> **Example.** A customer's willingness to pay is uniform between €100 and
> €300. P(WTP ≥ 250) = 50/200 = 0.25; mean €200.

@num X uniform on [0, 50]. P(X > 40)?
= 0.2 %
! 10/50.
@num WTP uniform on [200, 500]. P(WTP ≥ 320)?
= 0.6 %
! 180/300.
@num X uniform on [10, 30]. Mean?
= 20
! (10 + 30)/2.
@num X uniform on [0, 12]. Variance?
= 12
! 144/12.

## F12.8 The normal distribution
The **normal** (Gaussian) N(μ, σ²) is bell-shaped and symmetric around μ.
Rules of thumb:

- ≈ 68 % of values within μ ± 1σ;
- ≈ 95 % within μ ± 2σ (exactly ±1.96σ);
- ≈ 99.7 % within μ ± 3σ.

Many quantities are approximately normal (measurement errors, sums of many
small effects — see F12.12).

> **Example.** Weekly sales ~ N(500, 50²): about 95 % of weeks sell between
> 400 and 600 units.

@num Heights ~ N(170, 10²). Approximately what % lie between 160 and 180?
= 68 % ~1
! μ ± 1σ.
@num Sales ~ N(1,000, 100²). Approximately what % of days exceed 1,200?
= 2.5 % ~0.3
! Above μ + 2σ: (1 − 0.95)/2.
@mcq A normal distribution is fully described by…
+ its mean and standard deviation
- its median only
- its maximum
- its range
! Two parameters.

## F12.9 Standard normal and z-tables
Convert any normal X to the **standard normal** Z ~ N(0, 1):

```
z = (x − μ)/σ          P(X ≤ x) = Φ(z)
```

Useful values of Φ (area to the left):

| z | 0.5 | 1.0 | 1.28 | 1.5 | 1.645 | 1.96 | 2.0 | 2.33 |
| --- | --- | --- | --- | --- | --- | --- | --- | --- |
| Φ(z) | 0.6915 | 0.8413 | 0.90 | 0.9332 | 0.95 | 0.975 | 0.9772 | 0.99 |

Symmetry: Φ(−z) = 1 − Φ(z).

> **Example.** Demand ~ N(200, 40²). P(D ≤ 260) = Φ(1.5) = 0.9332.

@num X ~ N(50, 10²). P(X ≤ 60)?
= 0.8413 ~0.0005 %
! z = 1.
@num X ~ N(50, 10²). P(X > 65)?
= 0.0668 ~0.0005 %
! z = 1.5 → 1 − 0.9332.
@num X ~ N(100, 20²). P(X < 90)?
= 0.3085 ~0.0005 %
! z = −0.5 → 1 − 0.6915.

## F12.10 Normal quantiles (inverse problems)
Sometimes you know the probability and need the value:

```
x = μ + z·σ        with z from the table
```

> **Example.** Daily demand ~ N(200, 40²). Stock that covers demand on 95 % of
> days: x = 200 + 1.645 × 40 = **265.8** units. For 99 %: 200 + 2.33 × 40 = 293.2.

Safety stock = z·σ: the price of reliability grows quickly at high service
levels.

@num Demand ~ N(500, 60²). Stock covering 95 % of days?
= 598.7 ~0.1
! 500 + 1.645 × 60.
@num Exam scores ~ N(22, 4²). Score needed to be in the top 10 %?
= 27.12 ~0.02
! 22 + 1.28 × 4.
@num Demand ~ N(80, 15²), 90 % service level. Safety stock (above the mean)?
= 19.2 ~0.05
! 1.28 × 15.

## F12.11 Sums of random variables and risk pooling
For sums: means add; for independent variables, **variances** add.

```
n independent copies with mean μ and SD σ:
sum: mean n·μ, SD √n·σ          average: mean μ, SD σ/√n
```

The SD grows only with √n: combining many independent risks makes the total
relatively more predictable (**risk pooling**, the basis of insurance and of
holding stock centrally).

> **Example.** One store's weekly demand: mean 100, SD 30. Four independent
> stores pooled: mean 400, SD 60 (not 120). CV falls from 0.30 to 0.15.

@num 9 independent days, each with demand SD 20. SD of total demand?
= 60
x 180 | standard deviations don't add; variances do.
! √9 × 20.
@num 25 independent observations with SD 10. SD of their average?
= 2
! 10/√25.
@num Weekly demand per store: mean 50, SD 20. 16 independent stores: CV of total demand?
= 0.1 ~0.001 %
! mean 800, SD 80.

## F12.12 The central limit theorem (intuition)
The **central limit theorem**: the sum (or average) of many independent
random variables is approximately **normal**, whatever their individual
distribution, once n is large enough (often n ≥ 30).

That is why normal distributions appear everywhere and why sample means can
be analysed with normal tables (unit F15).

> **Example.** Each customer spends a skewed amount (mean €40, SD €30). The
> total of 100 customers is ≈ N(4,000, 300²): P(total < 3,500) = Φ(−1.67) ≈
> 0.048.

@num Each order: mean €50, SD €20. Total of 100 independent orders: mean (€)?
= 5000
! 100 × 50.
@num Each order: mean €50, SD €20. SD of the total of 100 independent orders (€)?
= 200
! √100 × 20.
@num Each order: mean €50, SD €20. Total of 100 independent orders: P(total > 5,400)? (use Φ(2) = 0.9772)
= 0.0228 ~0.0005 %
! z = 400/200 = 2.
