# F4 · Describing data | Statistics

## F4.1 Variables and data types
A **variable** is a characteristic that varies across observations.

- **Categorical (qualitative)**: categories. *Nominal* (no order: country,
  product type) or *ordinal* (ordered: satisfaction low/medium/high).
- **Numerical (quantitative)**: *discrete* (counts: units sold, customers) or
  *continuous* (measurements: price, weight, time).

The type determines the right summary: you can average prices but not
countries; for categories use counts and shares.

Each row of a dataset is an **observation** (a customer, a day, a firm); each
column a **variable**.

@mcq "Customer satisfaction: 1 = very unhappy … 5 = very happy" is…
+ ordinal categorical
- nominal categorical | the categories have an order.
- continuous
- a ratio scale
! Ordered categories.
@mcq The number of customers entering a shop per hour is…
+ discrete numerical
- continuous numerical | counts take whole values.
- nominal
- ordinal
! A count.
@mcq For the variable "country of residence" the right summary is…
+ counts or shares per category
- the mean | you can't average categories.
- the standard deviation
- the median
! Nominal data → frequencies.

## F4.2 Frequency tables and relative frequencies
A **frequency table** counts observations per category or per **class**
(interval). **Relative frequency** = count / total; **cumulative** frequency
adds up classes in order.

| daily sales | days | relative | cumulative |
| --- | --- | --- | --- |
| 0–9 | 6 | 0.20 | 0.20 |
| 10–19 | 12 | 0.40 | 0.60 |
| 20–29 | 9 | 0.30 | 0.90 |
| 30–39 | 3 | 0.10 | 1.00 |

Relative frequencies sum to 1. Cumulative frequency answers "what share of
days sold fewer than 20?" → 60 %.

@num In a sample of 40 customers, 14 chose product A. Relative frequency of A?
= 0.35 %
! 14/40.
@num Using the table above (30 days), on how many days were sales at least 20?
= 12
! 9 + 3.
@num Same table: cumulative relative frequency up to 29 units (as a decimal)?
= 0.9 %
! 0.2 + 0.4 + 0.3.

## F4.3 Histograms and the shape of a distribution
A **histogram** plots frequencies of numerical classes as adjacent bars. Look
at:

- **centre** (where most values are);
- **spread** (how wide);
- **shape**: symmetric, **right-skewed** (long tail to the right: incomes,
  house prices, firm sizes), left-skewed; one peak (unimodal) or two (bimodal);
- **outliers**: isolated extreme values.

In right-skewed data the **mean > median** (the tail pulls the mean up).

> **Example.** Income in a country: most people earn modest amounts; a few earn
> very large ones → right skew; mean income exceeds median income.

@mcq Household income distributions are typically…
+ right-skewed
- left-skewed
- perfectly symmetric
- uniform
! A long tail of high incomes.
@mcq In a right-skewed distribution, usually…
+ mean > median
- mean < median | that's left skew.
- mean = median
- there is no mean
! The tail pulls the mean towards it.
@mcq A histogram with two clear peaks suggests…
+ the data may mix two different groups
- an error
- a normal distribution
- no variation
! Bimodal data often combine two populations (e.g. two customer segments).

## F4.4 The mean
The **arithmetic mean** = sum of values / number of values:

```
x̄ = (x₁ + x₂ + … + xₙ) / n
```

Properties: uses every value; the deviations from the mean sum to zero; it is
**sensitive to outliers** (one billionaire in a bar raises the mean income
enormously).

> **Example.** Daily sales 12, 15, 9, 20, 14 → mean = 70/5 = **14**.

From a frequency table: x̄ = Σ (value × frequency) / Σ frequency.

@num Mean of 4, 8, 15, 16, 23, 42?
= 18
! 108/6 = 18.
@num Daily sales over 4 days: 120, 80, 100, 140. Mean?
= 110
! 440/4.
@num 10 days with 3 sales, 6 days with 5 sales, 4 days with 8 sales. Mean daily sales?
= 4.6
x 5.33 | weight each value by its frequency.
! (30 + 30 + 32)/20 = 92/20 = 4.6.
@num The mean of 5 numbers is 12. Four of them are 10, 11, 13, 14. The fifth?
= 12
! Total 60 − 48 = 12.

## F4.5 The median and the mode
- **Median**: the middle value of the **sorted** data (average of the two
  middle values if n is even). Robust to outliers.
- **Mode**: the most frequent value; the only "average" for nominal data.

> **Example.** Salaries (€k): 28, 30, 31, 33, 35, 36, 250. Mean = 63.3; median
> = **33**. The median describes the typical employee; the mean is pulled by one
> executive.

Even n: 3, 7, 8, 12 → median = (7 + 8)/2 = 7.5.

@num Median of 7, 2, 9, 4, 11?
= 7
x 9 | sort first: 2, 4, 7, 9, 11.
! Sorted: 2, 4, 7, 9, 11 → middle 7.
@num Median of 10, 4, 6, 18, 12, 8?
= 9
! Sorted 4, 6, 8, 10, 12, 18 → (8 + 10)/2.
@mcq Which average best describes typical income in a company with one very highly paid CEO?
+ median
- mean | the CEO's salary pulls it up.
- maximum
- range
! Robust to the outlier.
@mcq The mode of: red, blue, red, green, red, blue is…
+ red
- blue
- there is none
- 3
! Most frequent category.

## F4.6 Weighted averages
When observations have different importance, use a **weighted mean**:

```
weighted mean = Σ wᵢ xᵢ / Σ wᵢ
```

Uses: average price paid (weights = quantities), portfolio return (weights =
amounts invested), grade point average (weights = credits), price indices
(weights = budget shares).

> **Example.** Exam 1 (6 credits) grade 27, exam 2 (12 credits) grade 24, exam
> 3 (9 credits) grade 30. Weighted average = (162 + 288 + 270)/27 = **26.67**.

@num Grades: 30 (6 credits), 22 (12 credits), 26 (6 credits). Weighted average?
= 25
x 26 | weight by credits.
! (180 + 264 + 156)/24 = 600/24 = 25.
@num Portfolio: €6,000 earns 5 %, €4,000 earns 10 %. Portfolio return (%)?
= 7 %
x 7.5 | weight by amounts invested.
! (300 + 400)/10,000 = 7 %.
@num A shop sells 30 % of units at €10, 50 % at €20 and 20 % at €40. Average price per unit (€)?
= 21
! 3 + 10 + 8 = 21.

## F4.7 Percentiles and quartiles
The **p-th percentile** is the value below which p % of the observations lie.

- **Q1** = 25th percentile, **Q2** = median, **Q3** = 75th percentile.
- **Interquartile range (IQR)** = Q3 − Q1: spread of the middle 50 %.

Simple method for small samples: sort, median splits the data, Q1 = median of
the lower half, Q3 = median of the upper half.

> **Example.** 2, 4, 5, 7, 8, 10, 12, 15 → lower half 2,4,5,7 → Q1 = 4.5;
> upper half 8,10,12,15 → Q3 = 11; IQR = 6.5.

Percentiles are everywhere: "top 10 % of earners", "delivered within 2 days
for 95 % of orders".

@num Data 1, 3, 4, 6, 9, 11, 14, 20. Q1 (median of the lower half)?
= 3.5
! Lower half 1,3,4,6 → (3 + 4)/2.
@num Same data: Q3?
= 12.5
! Upper half 9,11,14,20 → (11 + 14)/2.
@num Same data: IQR?
= 9
! 12.5 − 3.5.
@mcq "95 % of orders are delivered within 3 days" describes…
+ the 95th percentile of delivery time
- the mean delivery time
- the median
- the maximum
! 95 % of values lie below 3 days.

## F4.8 Range and outliers
The **range** = max − min: simple but depends only on two (possibly extreme)
values.

A common rule flags as **outliers** values below Q1 − 1.5·IQR or above
Q3 + 1.5·IQR (the "fences" of a box plot).

Outliers can be errors (a price typed as 1000 instead of 10.00) or real and
important (a huge order). Never delete them blindly — investigate.

> **Example.** Q1 = 20, Q3 = 30, IQR = 10. Fences: 20 − 15 = 5 and 30 + 15 =
> 45. A value of 52 is flagged as an outlier.

@num Data min 12, max 87. Range?
= 75
! 87 − 12.
@num Q1 = 40, Q3 = 60. Upper fence for outliers (Q3 + 1.5·IQR)?
= 90
! IQR 20; 60 + 30.
@num Same data: lower fence?
= 10
! 40 − 30.
@mcq An outlier should be…
+ investigated: it may be an error or an important real case
- always deleted | real extreme values can matter most.
- always kept without checking
- replaced with the mean
! Check its origin first.

## F4.9 Variance and standard deviation
Spread around the mean:

```
sample variance   s² = Σ (xᵢ − x̄)² / (n − 1)
standard deviation s  = √s²          (same units as the data)
```

(Divide by n for a whole population; n − 1 corrects the bias of estimating
from a sample.)

> **Example.** 4, 6, 8: mean 6, deviations −2, 0, 2, squares 4, 0, 4, sum 8.
> s² = 8/2 = 4, s = **2**. Population version: 8/3, σ = 1.63.

@num Sample variance of 2, 4, 6, 8 (divide by n − 1)?
= 6.6667 ~0.01
x 5 | for a SAMPLE divide by n − 1 = 3.
! Mean 5; squares 9, 1, 1, 9 = 20; 20/3.
@num Sample standard deviation of 10, 12, 14?
= 2
! Mean 12; squares 4, 0, 4 = 8; 8/2 = 4; √4.
@num Population standard deviation of 3, 3, 3, 3?
= 0
! No variation.
@mcq Standard deviation is preferred to variance for reporting because…
+ it is in the same units as the data
- it is always larger | false for variance > 1.
- it ignores outliers
- it is easier to compute
! √ brings units back (€ rather than €²).

## F4.10 z-scores
A **z-score** says how many standard deviations a value is from the mean:

```
z = (x − mean) / sd
```

z-scores make values on different scales comparable. Roughly: |z| > 2 is
unusual, |z| > 3 very unusual (for bell-shaped data).

> **Example.** Shop A sells 130 units on a day when its mean is 100 (sd 15):
> z = 2. Shop B sells 260 with mean 240 (sd 20): z = 1. A's day was more
> exceptional, although B sold more.

@num Mean 50, sd 8. z-score of 66?
= 2
! (66 − 50)/8.
@num Mean 200, sd 25. Which value has z = −1.6?
= 160
! 200 − 1.6·25.
@num Exam A: you scored 27, mean 22, sd 2.5. z-score?
= 2
! 5/2.5.

## F4.11 Box plots and five-number summaries
The **five-number summary**: min, Q1, median, Q3, max. A **box plot** draws a
box from Q1 to Q3 with a line at the median and "whiskers" to the most extreme
non-outlier values; outliers appear as dots.

Box plots are ideal to **compare groups**: delivery times of three couriers,
prices across five regions. Look at medians (centre), box widths (spread),
whisker length and outliers, and skew (median not centred in the box).

> **Example.** Courier X: median 2 days, IQR 1; courier Y: median 2 days, IQR
> 4. Same typical time, but Y is far less predictable.

@mcq Two box plots have the same median but very different box widths. This means…
+ same typical value, different spread
- different typical values
- different sample sizes only
- one has errors
! Box width = IQR.
@mcq Which is NOT part of the five-number summary?
+ mean
- median
- Q1
- maximum
! Min, Q1, median, Q3, max.
@mcq A median line close to the left edge of the box (Q1) with a long right whisker suggests…
+ right skew
- left skew
- symmetry
- no data
! Long upper tail.

## F4.12 Coefficient of variation
Standard deviations of variables with different means aren't directly
comparable. The **coefficient of variation**:

```
CV = sd / mean
```

is unit-free: it measures **relative** variability.

> **Example.** Product A: mean weekly sales 1,000, sd 200 → CV = 0.20. Product
> B: mean 50, sd 20 → CV = 0.40. B is relatively twice as volatile, although
> its sd is smaller. Planning stock for B needs a bigger relative buffer.

Use CV only for ratio-scale positive data (not temperatures in °C).

@num Mean 80, sd 12. Coefficient of variation (decimal)?
= 0.15 %
! 12/80.
@num Product X: mean 500, sd 100. Product Y: mean 40, sd 12. CV of Y minus CV of X (decimal)?
= 0.1 ~0.005
! 0.30 − 0.20.
@mcq Which is relatively more variable: mean 1,000 & sd 100, or mean 10 & sd 3?
+ mean 10 & sd 3 (CV 0.30 vs 0.10)
- mean 1,000 & sd 100 | compare relative, not absolute spread.
- equal
- can't tell
! CV compares relative variability.
