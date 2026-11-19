# 3.5 Time value of money: PV, FV, NPV, IRR

## The big picture

A euro today is worth more than a euro next year: you could invest it and earn
interest, prices may rise, and the future is uncertain. The **time value of
money** lets us compare cash flows at different dates by converting them to a
common date. It is the foundation of investment decisions, bond pricing and
company valuation.

> **Analogy.** Money is like a seed: planted today (invested) it grows. A
> promise of a plant next year is worth the seed you would need to plant
> today to grow it.

## Compounding and future value

```
FV = PV · (1 + r)^n
```

*Worked example.* €1,000 at 5 % for 10 years: 1,000 · 1.05^10 = **€1,628.89**.
Simple interest would give only €1,500 — compounding earns interest on
interest.

- **Compounding frequency**: m times per year → FV = PV(1 + r/m)^(mn).
  Continuous: FV = PV·e^(rn).
- **Effective annual rate** EAR = (1 + r/m)^m − 1. 12 % compounded monthly
  → EAR = 12.68 %.
- **Rule of 72**: money doubles in ≈ 72/r years (r in %). At 6 %: ≈ 12 years.

## Discounting and present value

```
PV = FV / (1 + r)^n
```

*Worked example.* €1,000 received in 3 years at 8 %: 1,000/1.08³ = **€793.83**.

The **discount rate** r is the **opportunity cost of capital**: the return
available on an investment of similar risk.

## Annuities and perpetuities

- **Perpetuity** paying C forever from next year: PV = C / r.
- **Growing perpetuity** (growth g < r): PV = C / (r − g).
- **Annuity** paying C for n years:

```
PV = C · [1 − (1 + r)^−n] / r
```

*Worked example.* €500 a year for 10 years at 6 %:
500 · (1 − 1.06^−10)/0.06 = 500 · 7.3601 = **€3,680.04**.

*Mortgage example.* Borrow €200,000 at 3 % for 25 years, annual payments:
C = 200,000 · 0.03 / (1 − 1.03^−25) = **€11,485.56** per year.

## Net present value (NPV)

```
NPV = −C₀ + Σ_{t=1..n} CF_t / (1 + r)^t
```

**Rule**: accept projects with NPV > 0; among mutually exclusive projects
choose the highest NPV. NPV measures the value created today.

*Worked example.* Invest €1,000; receive €400 per year for 3 years; r = 10 %.
PV of inflows = 400·(1/1.1 + 1/1.21 + 1/1.331) = 400 · 2.4869 = 994.74.
NPV = **−€5.26** → reject, although undiscounted inflows (1,200) exceed 1,000.

## Internal rate of return (IRR)

The IRR is the discount rate that makes NPV = 0. Accept if IRR > cost of
capital. Pitfalls: multiple IRRs with non-conventional cash flows; IRR can
rank mutually exclusive projects wrongly (scale and timing) — NPV is the
reliable criterion.

*Worked example.* Invest 1,000 today, receive 1,210 in 2 years:
1,000 = 1,210/(1+IRR)² ⇒ IRR = **10 %**.

## Payback period

Years until cumulative cash flows recover the investment. Simple and popular,
but ignores the time value of money and everything after payback.

## Real vs nominal rates

```
(1 + nominal) = (1 + real) · (1 + inflation)      ⇒  real ≈ nominal − inflation
```

Discount nominal cash flows at nominal rates, real cash flows at real rates
(lesson 4.2).

## Holding cash with a deadline

If an investment's value is realised only at a fixed date, cash flows after
that date count for nothing, and assets still held at that date are valued at
whatever they can be converted into by then — possibly zero. The same logic
decides whether to keep an asset or liquidate it before a deadline: compare
the PV of keeping it with what liquidation brings now.

## Summary

- FV = PV(1 + r)^n; PV = FV/(1 + r)^n; r = opportunity cost of capital.
- Perpetuity C/r; annuity C·[1 − (1 + r)^−n]/r.
- NPV > 0 creates value; IRR is the rate that zeroes NPV.
- Real ≈ nominal − inflation.
