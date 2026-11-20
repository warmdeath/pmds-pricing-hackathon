# F9 · Probability | Statistics

## F9.1 Experiments, outcomes, events
A random **experiment** has uncertain outcomes (a customer arrives or not, a
bid wins or not, demand tomorrow). The **sample space** S is the set of all
possible outcomes; an **event** is a subset of S.

> **Example.** Rolling a die: S = {1,2,3,4,5,6}; event "even" = {2,4,6}.
> Tomorrow's demand for a product: S = {0, 1, 2, …}; event "at least 10".

Probability P(A) is a number between 0 (impossible) and 1 (certain).
Interpretations: **classical** (equally likely outcomes: favourable/total),
**frequentist** (long-run relative frequency), **subjective** (degree of
belief, e.g. "70 % chance the deal closes").

@num A fair die. Probability of rolling a number greater than 4?
= 0.3333 ~0.001 %
! {5, 6}: 2/6.
@num A bag has 3 red, 5 blue, 2 green balls. Probability of drawing a blue ball?
= 0.5 %
! 5/10.
@mcq "Out of 1,000 past days, 120 had more than 50 orders, so P(> 50 orders) ≈ 0.12" uses the…
+ frequentist interpretation
- classical interpretation | outcomes aren't equally likely by construction.
- subjective interpretation
- axiomatic definition only
! Long-run relative frequency.

## F9.2 Basic rules and the complement
Every probability satisfies 0 ≤ P(A) ≤ 1 and P(S) = 1. The **complement** of A
("not A") has

```
P(not A) = 1 − P(A)
```

The complement is often the easy route: "at least one" = 1 − "none".

> **Example.** Each of 3 independent machines fails today with probability 0.1.
> P(at least one fails) = 1 − 0.9³ = 1 − 0.729 = **0.271**.

@num P(rain) = 0.35. P(no rain)?
= 0.65 %
! 1 − 0.35.
@num A coin is tossed 4 times. Probability of at least one head?
= 0.9375 %
! 1 − 0.5⁴.
@num Each of 5 independent suppliers delivers late with probability 0.2. Probability that at least one is late?
= 0.6723 ~0.001 %
! 1 − 0.8⁵ = 1 − 0.32768.

## F9.3 The addition rule
For two events:

```
P(A or B) = P(A) + P(B) − P(A and B)
```

Subtract the overlap so it isn't counted twice. If A and B are **mutually
exclusive** (can't happen together), P(A and B) = 0 and probabilities simply
add.

> **Example.** 40 % of customers buy product X, 30 % buy Y, 10 % buy both.
> P(X or Y) = 0.4 + 0.3 − 0.1 = **0.6**; 40 % buy neither.

@num P(A) = 0.5, P(B) = 0.4, P(A and B) = 0.2. P(A or B)?
= 0.7 %
x 0.9 | subtract the overlap P(A and B).
! 0.5 + 0.4 − 0.2.
@num A card from a 52-card deck. P(heart or king)?
= 0.3077 ~0.001 %
! 13/52 + 4/52 − 1/52 = 16/52.
@num 60 % of shoppers use the app, 50 % the website, 30 % both. Share using neither (%)?
= 20 %
! 1 − (0.6 + 0.5 − 0.3).

## F9.4 Contingency tables
A **contingency table** cross-tabulates two categorical variables. From it
read **joint**, **marginal** and **conditional** probabilities.

| | bought | didn't buy | total |
| --- | --- | --- | --- |
| saw ad | 60 | 140 | 200 |
| no ad | 40 | 360 | 400 |
| total | 100 | 500 | 600 |

- P(bought) = 100/600 = 0.167 (marginal)
- P(saw ad and bought) = 60/600 = 0.10 (joint)
- P(bought | saw ad) = 60/200 = 0.30 (conditional: restrict to the row)

@num Using the table: P(bought | no ad)?
= 0.1 %
! 40/400.
@num Using the table: P(saw ad | bought)?
= 0.6 %
! 60/100.
@num Using the table: P(saw ad)?
= 0.3333 ~0.001 %
! 200/600.

## F9.5 Conditional probability
The probability of A **given** that B happened:

```
P(A | B) = P(A and B) / P(B)
```

Conditioning restricts the world to the cases where B is true. In general
P(A | B) ≠ P(B | A): P(rich | owns a yacht) is high; P(owns a yacht | rich) is
much lower. Confusing the two is the **prosecutor's fallacy**.

> **Example.** P(order large and customer is a business) = 0.12; P(business) =
> 0.20 → P(large | business) = 0.6.

@num P(A and B) = 0.15, P(B) = 0.5. P(A | B)?
= 0.3 %
! 0.15/0.5.
@num 30 % of days are rainy; 12 % of days are rainy AND have low sales. P(low sales | rainy)?
= 0.4 %
! 0.12/0.30.
@mcq P(fluent in Italian | lives in Milan) vs P(lives in Milan | fluent in Italian). Which is larger?
+ the first
- the second | most Italian speakers don't live in Milan.
- equal
- can't be compared
! Conditioning direction matters.

## F9.6 The multiplication rule and independence
```
P(A and B) = P(A) × P(B | A)
```

A and B are **independent** if knowing one doesn't change the other's
probability: P(B | A) = P(B), so P(A and B) = P(A) × P(B).

Independence is an **assumption** to check: daily sales of umbrellas and rain
are not independent; two different customers' coin tosses are.

> **Example.** P(first customer buys) = 0.3, independent customers → P(both
> buy) = 0.09. Drawing 2 cards without replacement: P(both aces) =
> 4/52 × 3/51 = 0.0045 (dependent).

@num P(A) = 0.6, P(B | A) = 0.5. P(A and B)?
= 0.3 %
! 0.6 × 0.5.
@num Two independent events with P = 0.2 and 0.7. Probability both happen?
= 0.14 %
! 0.2 × 0.7.
@num Draw 2 cards without replacement. P(both hearts)?
= 0.0588 ~0.001 %
! 13/52 × 12/51 = 0.0588.
@mcq P(A) = 0.4, P(B) = 0.5, P(A and B) = 0.3. Are A and B independent?
+ No: 0.3 ≠ 0.4 × 0.5
- Yes
- Only if mutually exclusive
- Can't tell
! Independence requires P(A and B) = P(A)P(B) = 0.2.

## F9.7 Probability trees
A **tree** lays out sequential uncertain events. Multiply along branches to get
joint probabilities; add the branches that lead to the same final event.

> **Example.** 60 % of leads come from ads, 40 % from referrals. Conversion: 5 %
> for ad leads, 15 % for referrals.
> P(convert) = 0.6 × 0.05 + 0.4 × 0.15 = 0.03 + 0.06 = **0.09**.

This sum over branches is the **law of total probability**:
P(A) = Σ P(A | Bᵢ) P(Bᵢ).

@num 70 % of orders are online (2 % returned), 30 % in store (5 % returned). Overall return rate (%)?
= 2.9 %
! 0.7×0.02 + 0.3×0.05 = 0.029.
@num A supplier is reliable with P = 0.8; reliable suppliers deliver on time 95 % of the time, unreliable 60 %. P(on time)?
= 0.88 %
! 0.8×0.95 + 0.2×0.6.
@num Two machines: A makes 40 % of output with 3 % defects, B makes 60 % with 1 % defects. Overall defect rate (%)?
= 1.8 %
! 0.012 + 0.006.

## F9.8 Bayes' theorem
Reverse a conditional probability:

```
P(B | A) = P(A | B) × P(B) / P(A)
```

where P(A) comes from the law of total probability.

> **Example (testing).** 1 % of products are defective. A test flags 95 % of
> defective items and 10 % of good ones. P(defective | flagged) =
> 0.95×0.01 / (0.95×0.01 + 0.10×0.99) = 0.0095/0.1085 = **0.088**.
> Only about 9 %! When the base rate is low, most alarms are false — the
> **base-rate fallacy**.

@num Using the example's numbers: P(flagged)?
= 0.1085 ~0.0005 %
! 0.0095 + 0.099.
@num Same setting from F9.7: P(lead came from referrals | converted)?
= 0.6667 ~0.001 %
! 0.06/0.09.
@num 5 % of customers are fraudulent. A filter flags 90 % of frauds and 2 % of honest customers. P(fraud | flagged)?
= 0.7031 ~0.001 %
! 0.045/(0.045 + 0.019) = 0.7031.

## F9.9 Expected value of a gamble
For outcomes xᵢ with probabilities pᵢ:

```
E[X] = Σ pᵢ × xᵢ
```

The expected value is the long-run average if the situation repeats many
times. It guides repeated decisions; for one-off, high-stakes choices risk
also matters (unit F12).

> **Example.** A bid wins with probability 0.3 and then earns €500 profit;
> otherwise €0. E = 0.3 × 500 = €150. If preparing the bid costs €100, the
> expected net gain is €50.

@num 40 % chance of €1,000, 60 % chance of −€200. Expected value (€)?
= 280
! 400 − 120.
@num A €2 lottery ticket wins €100 with probability 0.01, otherwise nothing. Expected net gain (€)?
= -1
! 0.01 × 100 − 2.
@num A product launch: 25 % → +€80k, 50 % → +€20k, 25 % → −€60k. Expected profit (€k)?
= 15
! 20 + 10 − 15.

## F9.10 Counting: the multiplication principle and permutations
If a choice has n₁ options and another n₂, together there are n₁ × n₂
combinations.

**Permutations** (order matters): arranging k items out of n distinct ones:

```
n! / (n − k)!          all n items: n! = n × (n−1) × … × 1
```

> **Example.** 3 sizes × 4 colours × 2 materials = 24 product versions.
> Ranking 3 winners among 10 teams: 10 × 9 × 8 = 720 ordered podiums.

@num 5 shirts, 3 trousers, 2 pairs of shoes. Number of outfits?
= 30
! 5×3×2.
@num In how many orders can 5 different products be displayed in a row?
= 120
! 5!.
@num Gold, silver, bronze among 8 teams. Number of possible podiums?
= 336
! 8×7×6.

## F9.11 Combinations
**Combinations** (order doesn't matter): choosing k items out of n:

```
C(n, k) = n! / (k! (n − k)!)
```

> **Example.** Choosing 3 products out of 10 for a promotion: C(10,3) = 120.
> Probability that a random selection of 3 includes your favourite product:
> C(9,2)/C(10,3) = 36/120 = 0.3.

Combinations power the binomial distribution (F12.5).

@num C(6, 2)?
= 15
! 6!/(2!·4!) = 15.
@num A committee of 4 from 9 people. Number of possible committees?
= 126
! C(9,4).
@num 5 cards from 52. P(all hearts)? (decimal, 5 places)
= 0.000495 ~0.00001
! C(13,5)/C(52,5) = 1,287/2,598,960.

## F9.12 Common probability mistakes
- **Gambler's fallacy**: after 5 reds, black is "due". Independent spins have
  no memory.
- **Base-rate neglect**: ignoring how rare the condition is (F9.8).
- **Conjunction fallacy**: thinking "A and B" is more likely than "A" alone —
  impossible, P(A and B) ≤ P(A).
- **Confusing P(A|B) with P(B|A)**.
- **Assuming independence** when events share a common cause (all suppliers
  hit by the same strike).

> **Example.** "Our last three launches failed, so the next will succeed" —
> only if outcomes are linked; otherwise the past doesn't change the odds.

@mcq A fair coin landed heads 6 times in a row. P(heads on the 7th toss)?
+ 0.5
- less than 0.5 | the gambler's fallacy.
- more than 0.5
- 1/128
! Independent tosses.
@mcq P(Linda is a bank teller) vs P(Linda is a bank teller AND an activist). Which is larger or equal?
+ P(bank teller)
- P(bank teller and activist) | conjunction fallacy.
- they're always equal
- can't tell
! A conjunction can't be more likely than its parts.
@mcq Ten suppliers all located in the same port. Treating their delays as independent…
+ understates the risk that many are late at once
- is exactly right
- overstates the risk
- doesn't matter
! A common cause links them.
