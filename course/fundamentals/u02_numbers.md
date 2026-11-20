# F2 · The numbers of economics | Reasoning

## F2.1 Percentages
A percentage is a fraction of 100: 15 % = 15/100 = 0.15. Three standard
questions:

```
part   = rate × whole          15 % of 240 = 0.15 × 240 = 36
rate   = part / whole          36 of 240   = 36/240 = 0.15 = 15 %
whole  = part / rate           36 is 15 % of 36/0.15 = 240
```

Always ask **"percent of what?"** — the base matters. A 20 % discount on
€80 and a 20 % tip on €80 are the same amount, but "20 % of revenue" and "20 %
of profit" are very different numbers.

> **Example.** VAT of 22 % is included in a price of €61. The price without
> VAT is 61/1.22 = €50, not 61 × 0.78 = €47.58 (a classic error: 22 % is a
> percentage of the net price, not of the gross price).

@num What is 18 % of 350?
= 63
! 0.18 × 350 = 63.
@num 45 is what percentage of 180? (answer in %)
= 25 %
! 45/180 = 0.25 = 25 %.
@num A price of €122 includes 22 % VAT. Price without VAT (€)?
= 100
x 95.16 | 22 % is computed on the net price: divide by 1.22, don't subtract 22 % of the gross.
! 122 / 1.22 = 100.
@num 30 is 12 % of what number?
= 250
! 30 / 0.12 = 250.

## F2.2 Percentage change
```
% change = (new − old) / old × 100
```
The base is the **old** value. Consequences:

- A rise of 25 % followed by a fall of 25 % does **not** return to the start:
  100 → 125 → 93.75.
- To undo a fall of x %, you need a rise of x/(1 − x): after −50 % you need
  **+100 %**.

> **Example.** Sales go from 80,000 to 92,000 units: (92 − 80)/80 = +15 %.
> Next year they fall back to 80,000: (80 − 92)/92 = −13.0 %.

@num Price rises from €40 to €46. Percentage change (%)?
= 15 %
x 13.04 | the base is the OLD value (40), not the new one.
! (46 − 40)/40 = 0.15.
@num A share price falls from 200 to 150. Percentage change (%)?
= -25 %
x 25 | it is a fall: the change is negative.
! (150 − 200)/200 = −0.25.
@num After a 20 % fall, what percentage rise brings a value back to its starting level? (%)
= 25 %
x 20 | the base after the fall is smaller, so you need more than 20 %.
! 100 → 80; 80 × (1 + r) = 100 ⇒ r = 25 %.
@num A price rises 10 % and then falls 10 %. Overall change (%)?
= -1 %
x 0 | the two percentages apply to different bases.
! 1.1 × 0.9 = 0.99 → −1 %.

## F2.3 Percentages vs percentage points
When the variable itself is a percentage (interest rates, unemployment,
market shares), say clearly whether you mean:

- **percentage points (pp)**: simple difference. Unemployment 8 % → 10 % is
  **+2 pp**.
- **percent change**: relative change. 8 % → 10 % is **+25 %**.

Central banks move rates in **basis points**: 1 bp = 0.01 pp. "+50 bp" = +0.5 pp.

> **Example.** A party's vote share goes from 20 % to 22 %: +2 pp, or +10 % in
> relative terms. Both are correct — but only if labelled.

@num Interest rate rises from 4 % to 5 %. Change in percentage points?
= 1
x 25 | that's the relative (percent) change.
! 5 − 4 = 1 pp.
@num Same change (4 % → 5 %): relative change in percent?
= 25 %
x 1 | that's in percentage points.
! (5 − 4)/4 = 25 %.
@num The ECB raises its rate by 75 basis points. In percentage points?
= 0.75
! 75 × 0.01 = 0.75 pp.
@mcq Market share goes from 10 % to 12 %. Which description is WRONG?
+ "market share rose by 2 %"
- "market share rose by 2 percentage points"
- "market share rose by 20 %"
- "market share is 1.2 times what it was"
! 2 % would be a relative rise to 10.2 %; the rise is 2 pp = 20 %.

## F2.4 Growth over several periods (compounding)
Growth rates **multiply**, they don't add:

```
value after n periods = start × (1 + g)^n
```

Growth of 10 % for 3 years is ×1.1³ = 1.331 → **+33.1 %**, not +30 %.

Average growth over several periods is the **compound annual growth rate**:

```
CAGR = (end / start)^(1/n) − 1
```

> **Example.** Revenue grows from €2.0 m to €2.9 m in 4 years:
> CAGR = (2.9/2.0)^(1/4) − 1 = 1.45^0.25 − 1 = **9.73 %**. The simple average
> (45 %/4 = 11.25 %) overstates it.

@num A town of 50,000 people grows 2 % a year for 5 years. Population after 5 years? (round to the unit)
= 55204 ~2
x 55000 | growth compounds: use (1.02)^5, not 1 + 5 × 2 %.
! 50,000 × 1.02^5 = 55,204.
@num Revenue goes from 100 to 150 in 3 years. CAGR (%)?
= 14.47 % ~0.05
x 16.67 | that's the simple average; growth compounds.
! (1.5)^(1/3) − 1 = 0.1447.
@num Prices rise 5 %, 3 % and 4 % in three years. Total rise (%)?
= 12.48 % ~0.02
x 12 | rates multiply: 1.05 × 1.03 × 1.04.
! 1.05 × 1.03 × 1.04 = 1.12476.

## F2.5 Doubling time and the rule of 70
How long does it take for something growing at g % per year to double?

```
doubling time ≈ 70 / g        (g in %)
```

(72 is also used: it divides nicely by 2, 3, 4, 6, 8, 9, 12.) The exact
answer is ln 2 / ln(1 + g).

> **Example.** A country growing at 3.5 % doubles its GDP in about 20 years; at
> 1 % it needs about 70 years. Small differences in growth rates create huge
> differences over decades.

The same rule works for **halving** under decline, and for prices under
inflation: at 7 % inflation prices double in about 10 years.

@num Approximate doubling time at 5 % growth (years), rule of 70?
= 14 ~0.5
! 70/5 = 14.
@num Inflation is 10 % per year. Approximately how many years until prices double (rule of 70)?
= 7 ~0.3
! 70/10 = 7.
@num A city doubled its population in 35 years. Approximate annual growth rate (%)?
= 2 ~0.1
! 70/35 = 2 %.

## F2.6 Index numbers
An **index** expresses values relative to a **base period** set to 100:

```
index_t = value_t / value_base × 100
```

Indices make series with different units comparable and turn changes into
easy percentages: an index of 118 means +18 % since the base.

Change between two non-base periods: (I₂ − I₁)/I₁, **not** I₂ − I₁ (that's
index points).

> **Example.** House prices: 2020 = 100, 2023 = 115, 2024 = 121. Change
> 2023→2024 = (121 − 115)/115 = **5.2 %** (6 index points).

@num Sales were 400 units in the base year and 520 units now. Index value now?
= 130
! 520/400 × 100 = 130.
@num A price index goes from 125 to 140. Percentage change (%)?
= 12 %
x 15 | 15 is the change in index POINTS; divide by the old value 125.
! (140 − 125)/125 = 0.12.
@num Index (base 100 in 2020) is 108 in 2024. Value in 2020 was €250. Value in 2024 (€)?
= 270
! 250 × 1.08 = 270.

## F2.7 Nominal vs real
**Nominal** values are in current euros; **real** values remove inflation,
measuring purchasing power or volume:

```
real value = nominal value / price index × 100
real growth ≈ nominal growth − inflation     (exact: (1+n)/(1+π) − 1)
```

> **Example.** A salary rises from €30,000 to €31,500 (+5 %) while prices rise
> 3 %. Real growth = 1.05/1.03 − 1 = **+1.94 %** (≈ 2 %). If prices rose 7 %,
> the real salary would **fall** by 1.87 %.

Always ask whether a number is nominal or real before comparing across years.

@num Nominal GDP grows 6 %, inflation is 4 %. Approximate real growth (%)?
= 2 % ~0.05
! 6 − 4 = 2 % (exact: 1.06/1.04 − 1 = 1.92 %).
@num A wage rises 2 % while inflation is 5 %. Exact real change (%)?
= -2.857 % ~0.01
x 7 | inflation reduces real wages: subtract, don't add.
! 1.02/1.05 − 1 = −0.02857.
@num Nominal income €40,000, price index 125 (base 100). Real income in base-year euros?
= 32000
! 40,000/125 × 100 = 32,000.

## F2.8 Ratios, per-unit and per-capita figures
Raw totals hide size. Divide by a sensible denominator:

- **per capita**: GDP per person, cars per 1,000 inhabitants;
- **per unit**: cost per unit, revenue per customer;
- **ratios**: debt/GDP, profit/revenue (margin), stock/sales.

> **Example.** Country A: GDP €2,000 bn, 60 m people → €33,333 per person.
> Country B: GDP €400 bn, 10 m people → €40,000 per person. B is smaller but
> richer per person.

Watch the denominator: "accidents per car" vs "accidents per km driven" can
tell opposite stories.

@num A firm sells €3.6 m to 12,000 customers. Revenue per customer (€)?
= 300
! 3,600,000 / 12,000 = 300.
@num Debt €2,800 bn, GDP €2,000 bn. Debt-to-GDP ratio (%)?
= 140 %
! 2,800/2,000 = 1.4.
@num A shop holds 600 units of stock and sells 150 per week. How many weeks of stock does it hold?
= 4
! 600 / 150 = 4 weeks.

## F2.9 Averages of rates (and why simple averages mislead)
Averaging ratios needs the right weights.

- Average **price** paid: total spent / total units, **not** the average of
  prices.
- Average **speed** over equal distances: harmonic mean.
- Average **growth** over time: geometric (CAGR, F2.4).

> **Example.** You buy 10 units at €4 and 30 units at €8. Average price paid =
> (40 + 240)/40 = **€7**, not (4 + 8)/2 = €6.

> **Example.** Investment returns +50 % then −50%: arithmetic mean 0 %, but
> €100 → €150 → €75: you lost 25 %.

@num You buy 20 units at €5 and 60 units at €9. Average price paid per unit (€)?
= 8
x 7 | weight each price by the quantity bought.
! (100 + 540)/80 = 8.
@num An investment returns +20 % then −20 %. Overall change (%)?
= -4 %
x 0 | returns compound: 1.2 × 0.8.
! 1.2 × 0.8 = 0.96.
@mcq To average growth rates over several years, use…
+ the geometric mean (CAGR)
- the arithmetic mean of the rates | it ignores compounding.
- the median
- the largest rate
! Growth multiplies.

## F2.10 Orders of magnitude and units
Economic numbers span huge ranges. Keep units straight:

| word | number | power |
| --- | --- | --- |
| thousand (k) | 1,000 | 10³ |
| million (m) | 1,000,000 | 10⁶ |
| billion (bn) | 1,000,000,000 | 10⁹ |
| trillion (tn) | 10¹² | |

Italian *miliardo* = billion (10⁹). Sanity checks: Italy's GDP ≈ €2 tn, about
59 m people → about €35k per person. If your calculation gives €35 or €35 m per
person, a unit is wrong.

Convert before dividing: €1.2 bn / 4 m people = 1,200,000,000 / 4,000,000 =
**€300**.

@num €2.4 billion divided among 8 million people is how many € per person?
= 300
! 2.4×10⁹ / 8×10⁶ = 300.
@num How many millions are in 3.5 billion?
= 3500
! 3.5 × 1,000 = 3,500 million.
@num A firm's revenue is €45 million and it has 300 employees. Revenue per employee in € thousands?
= 150
! 45,000,000/300 = 150,000 = 150k.

## F2.11 Simple linear equations in economics
Many economic problems reduce to solving one linear equation.

```
a + b·x = c   ⇒   x = (c − a)/b
```

> **Example (break-even).** Fixed costs €12,000, each unit earns €30 above its
> variable cost. Units needed to cover fixed costs: 30x = 12,000 ⇒ x = 400.

> **Example (budget).** You have €500, rent is €200, each meal costs €12. How
> many meals? 200 + 12x = 500 ⇒ x = 25.

Check the answer by substituting back, and check the units (meals, euros,
units per month).

@num Solve for x: 150 + 6x = 420.
= 45
! 6x = 270 ⇒ x = 45.
@num A taxi charges €3 plus €1.50 per km. A ride cost €21. How many km?
= 12
! 3 + 1.5k = 21 ⇒ k = 12.
@num Fixed costs €18,000; each unit contributes €45. Units to break even?
= 400
! 18,000/45 = 400.

## F2.12 Two equations, two unknowns
Markets often give two equations (e.g. demand and supply). Solve by
**substitution** or **elimination**.

```
Qd = 100 − 2P,   Qs = 20 + 2P,   equilibrium: Qd = Qs
100 − 2P = 20 + 2P  ⇒  80 = 4P  ⇒  P = 20,  Q = 60
```

> **Example (mix).** A shop sells 50 items, some at €10 and some at €4, for
> €320 total. x + y = 50 and 10x + 4y = 320 ⇒ 10x + 4(50 − x) = 320 ⇒ 6x = 120
> ⇒ x = 20 at €10, y = 30 at €4.

@num Qd = 120 − 3P and Qs = 20 + 2P. Equilibrium price?
= 20
! 120 − 3P = 20 + 2P ⇒ 100 = 5P ⇒ P = 20.
@num Same market: equilibrium quantity?
= 60
! 120 − 3·20 = 60.
@num 40 tickets were sold, some at €15 and some at €25, for €720. How many at €25?
= 12
! x + y = 40, 15x + 25y = 720 ⇒ 15(40 − y) + 25y = 720 ⇒ 10y = 120 ⇒ y = 12.
