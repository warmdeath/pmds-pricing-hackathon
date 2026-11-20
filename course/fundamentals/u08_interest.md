# F8 · Money and interest | Accounting & finance

## F8.1 Why money has a time value
A euro today is worth more than a euro in a year because:

1. it can be **invested** and earn interest (opportunity cost of capital);
2. **inflation** may reduce what it buys;
3. the future is **uncertain** (you might not receive it).

The **interest rate** is the price of time: what a borrower pays to use money
now, what a lender earns for waiting. Comparing money at different dates
requires moving it to the same date (unit F8 and F13).

> **Example.** Offered €1,000 today or €1,000 in two years, everybody takes it
> today; offered €1,000 today or €1,150 in two years, the answer depends on the
> rate you can earn meanwhile.

@mcq Which is NOT a reason why money today is worth more than money later?
+ banknotes wear out
- money can earn interest meanwhile
- inflation reduces purchasing power
- future payments are uncertain
! The others are the three economic reasons.
@mcq The interest rate is best described as…
+ the price of using money over time
- a tax
- the inflation rate
- a bank fee
! Borrowers pay it, lenders earn it.
@mcq €1,000 now or €1,040 in one year; you can earn 5 % risk-free. Which is better?
+ €1,000 now (it grows to €1,050)
- €1,040 later | you'd have 1,050 by investing today.
- they're equal
- can't tell
! Compare at the same date.

## F8.2 Simple interest
**Simple interest** is paid only on the original principal:

```
interest = P × r × t          FV = P × (1 + r × t)
```

(t in years if r is annual). Common for short-term loans and some bonds'
coupons.

> **Example.** €5,000 at 4 % simple for 3 years: interest = 5,000 × 0.04 × 3 =
> €600; FV = €5,600.

For periods shorter than a year: t = days/365 (or /360 by banking
convention).

@num €8,000 at 5 % simple interest for 2 years. Total interest (€)?
= 800
! 8,000 × 0.05 × 2.
@num €10,000 at 6 % simple interest for 9 months. Interest (€)?
= 450
! 10,000 × 0.06 × 0.75.
@num A loan of €2,000 at simple interest became €2,300 after 3 years. Annual rate (%)?
= 5 %
! 300/(2,000 × 3).

## F8.3 Compound interest
With **compounding**, interest is added to the balance and earns interest
itself:

```
FV = P × (1 + r)^n
```

> **Example.** €5,000 at 4 % compounded annually for 3 years: 5,000 × 1.04³ =
> **€5,624.32** (vs €5,600 simple). Over 30 years the gap becomes huge: 5,000 ×
> 1.04³⁰ = €16,217 vs €11,000 simple.

Compounding is why small differences in rates matter so much over long periods.

@num €2,000 at 6 % compounded annually for 4 years. Future value (€)?
= 2524.95 ~0.05
x 2480 | that's simple interest; compound interest earns interest on interest.
! 2,000 × 1.06⁴ = 2,524.95.
@num €1,000 at 10 % compounded annually for 2 years. Interest earned (€)?
= 210
x 200 | year 2 also earns interest on year 1's interest.
! 1,000 × 1.21 − 1,000.
@num How much must you invest today at 5 % compound to have €1,157.63 in 3 years? (€)
= 1000 ~0.05
! 1,157.63/1.05³.

## F8.4 Compounding frequency and the effective rate
If interest is compounded m times a year at a nominal annual rate r:

```
FV = P × (1 + r/m)^(m·n)
effective annual rate EAR = (1 + r/m)^m − 1
```

More frequent compounding → higher EAR. Loans are often quoted with a nominal
rate (APR/TAN in Italy); the effective cost (TAEG includes fees too) is higher.

> **Example.** 12 % compounded monthly: EAR = 1.01¹² − 1 = **12.68 %**.

@num 6 % nominal, compounded quarterly. EAR (%)?
= 6.136 % ~0.005
! 1.015⁴ − 1 = 0.06136.
@num 12 % nominal compounded monthly. EAR (%)?
= 12.68 % ~0.01
! 1.01¹² − 1.
@num €1,000 at 8 % nominal compounded semi-annually for 1 year. FV (€)?
= 1081.6
! 1,000 × 1.04².

## F8.5 Present value and discounting
**Discounting** is compounding in reverse: the value today of money received
later.

```
PV = FV / (1 + r)^n
```

The rate r is the **discount rate**: the return you could earn elsewhere on a
similar-risk investment. Higher rate or longer wait → lower PV.

> **Example.** €10,000 in 5 years at 6 %: PV = 10,000/1.06⁵ = **€7,472.58**.

@num PV of €5,000 received in 3 years at 8 % (€)?
= 3969.16 ~0.05
! 5,000/1.08³.
@num PV of €1,000 in 1 year at 25 % (€)?
= 800
! 1,000/1.25.
@mcq If the discount rate rises, the PV of a fixed future payment…
+ falls
- rises
- is unchanged
- doubles
! Dividing by a larger factor.

## F8.6 The rule of 72 for money
Money at r % per year doubles in about **72/r** years; at r % inflation,
purchasing power halves in about 72/r years.

> **Example.** At 6 % → 12 years; at 9 % → 8 years. A credit card at 24 %
> doubles a debt in about 3 years.

Exact: n = ln 2 / ln(1 + r).

@num Approximately how many years to double money at 4 % (rule of 72)?
= 18 ~0.3
! 72/4.
@num What rate doubles money in about 6 years (rule of 72)? (%)
= 12 ~0.3
! 72/6.
@num Exact doubling time at 8 % (years, 2 decimals)?
= 9.01 ~0.02
! ln 2/ln 1.08 = 9.006.

## F8.7 Inflation and real returns
**Real return** = return in purchasing power:

```
(1 + nominal) = (1 + real) × (1 + inflation)
real ≈ nominal − inflation
```

A deposit at 2 % with 5 % inflation has a real return of about −3 %: you end
the year able to buy less.

> **Example.** Nominal 7 %, inflation 3 %: real = 1.07/1.03 − 1 = **3.88 %**.

@num Nominal return 9 %, inflation 4 %. Exact real return (%)?
= 4.81 % ~0.01
! 1.09/1.04 − 1 = 0.0481.
@num You need a 3 % real return with expected inflation of 2 %. Required nominal return (exact, %)?
= 5.06 % ~0.01
! 1.03 × 1.02 − 1 = 0.0506.
@mcq Deposit 1 %, inflation 4 %. Your purchasing power…
+ falls by about 3 %
- rises by 1 %
- rises by 5 %
- is unchanged
! Real ≈ 1 − 4.

## F8.8 Annuities: series of equal payments
An **annuity** pays the same amount C at the end of each period for n
periods. Its present value:

```
PV = C × [1 − (1 + r)^−n] / r          (annuity factor)
FV = C × [(1 + r)^n − 1] / r
```

Examples: rent, salaries, loan instalments, savings plans.

> **Example.** €1,000 a year for 5 years at 5 %: factor = (1 − 1.05⁻⁵)/0.05 =
> 4.3295 → PV = **€4,329.48**.

@num PV of €2,000 per year for 3 years at 10 % (€)?
= 4973.7 ~0.05
! 2,000 × 2.48685 = 4,973.70.
@num FV of saving €1,000 at the end of each year for 4 years at 5 % (€)?
= 4310.13 ~0.05
! 1,000 × (1.05⁴ − 1)/0.05.
@mcq The PV of an annuity is less than C × n because…
+ later payments are discounted more
- of taxes
- the last payment is missing
- inflation is zero
! Time value of money.

## F8.9 Perpetuities
A **perpetuity** pays C every period forever:

```
PV = C / r
growing perpetuity (growth g < r):  PV = C₁ / (r − g)
```

Surprisingly, infinite payments have a finite value because far-away
payments are worth almost nothing today. Used to value stocks, real estate and
the "terminal value" of businesses.

> **Example.** €500 a year forever at 4 % → €12,500. If it grows 2 % a year:
> 500/(0.04 − 0.02) = €25,000.

@num PV of €300 per year forever at 6 % (€)?
= 5000
! 300/0.06.
@num First payment €100, growing 3 % forever, discount rate 8 %. PV (€)?
= 2000
! 100/0.05.
@num A perpetuity worth €40,000 pays €1,600 a year. Implied discount rate (%)?
= 4 %
! 1,600/40,000.

## F8.10 Loan payments
A standard (French) amortising loan has equal payments; each payment covers
the interest on the balance and repays part of the principal.

```
payment C = L × r / [1 − (1 + r)^−n]
```

> **Example.** €10,000 at 6 % for 5 years, annual payments:
> C = 10,000 × 0.06 / (1 − 1.06⁻⁵) = **€2,373.96**. Total paid €11,869.82,
> interest €1,869.82.

For monthly payments use r/12 and n in months.

@num Loan €20,000 at 5 % for 4 years, annual payments. Payment (€)?
= 5640.24 ~0.05
! 20,000 × 0.05 / (1 − 1.05⁻⁴) = 5,640.24.
@num Same loan: total interest paid over the life (€)?
= 2560.95 ~0.2
! 4 × 5,640.24 − 20,000.
@mcq Doubling a loan's length (same rate) makes each payment…
+ smaller, but total interest larger
- larger
- unchanged
- smaller and total interest smaller
! Lower instalment, more years of interest.

## F8.11 Amortisation schedules
An **amortisation schedule** shows, payment by payment: opening balance,
interest (= balance × r), principal repaid (= payment − interest), closing
balance. Early payments are mostly interest; later ones mostly principal.

| year | opening | interest 6 % | payment | principal | closing |
| --- | --- | --- | --- | --- | --- |
| 1 | 10,000.00 | 600.00 | 2,373.96 | 1,773.96 | 8,226.04 |
| 2 | 8,226.04 | 493.56 | 2,373.96 | 1,880.40 | 6,345.64 |

@num Using the schedule above: interest in year 3 (€)?
= 380.74 ~0.02
! 6,345.64 × 0.06.
@num Loan €50,000 at 4 %, annual payment €11,231.36. Principal repaid in year 1 (€)?
= 9231.36
! Interest 2,000; 11,231.36 − 2,000.
@mcq Over the life of an amortising loan, the interest part of each payment…
+ decreases
- increases
- is constant | the payment is constant, not its split.
- is zero
! The balance falls, so interest falls.

## F8.12 Comparing offers: effective cost and opportunity cost
To compare financial offers:

1. bring all cash flows to the **same date** (PV or FV);
2. use **effective** annual rates (include compounding and fees);
3. use your **opportunity cost** as the discount rate.

> **Example.** A shop offers 3 % off for paying cash now, or the full price in
> 60 days. Paying now saves 3 % for 60 days — about 3 %/(60/365) ≈ **18 %** per
> year, far more than a 3 % deposit: pay now if you have the cash.

@num Discount 2 % for paying today instead of in 30 days. Approximate annualised rate (%), using ×365/30?
= 24.33 % ~0.1
! 2 × 365/30 = 24.33 %.
@num Offer A: €1,000 now. Offer B: €1,100 in 2 years. Your rate is 6 %. PV of B (€)?
= 978.99 ~0.05
! 1,100/1.06² = 978.99 → A is better.
@mcq Which rate should you use to discount a personal investment's cash flows?
+ the return of your best alternative with similar risk
- always 0 %
- the inflation rate only
- the highest rate you've ever seen
! Opportunity cost of capital.
