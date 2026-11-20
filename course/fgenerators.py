"""Unlimited parametric practice for the Fundamentals section.

Re-uses tested builders from generators.py (re-tagged to Fundamentals lessons)
and adds builders specific to the Fundamentals syllabus."""

from __future__ import annotations

import math

from generators import GENERATORS, Exercise, Generator

FGENERATORS: list[Generator] = []

# --- builders reused from the general course, mapped to Fundamentals lessons ---
REUSE = {
    "marginal-decision": "F1.6", "opportunity-cost": "F5.12",
    "equilibrium-price": "F5.6", "equilibrium-quantity-shift": "F5.7",
    "arc-elasticity": "F5.8", "point-elasticity": "F5.8", "revenue-elasticity": "F5.8",
    "consumer-surplus": "F5.11", "wtp-demand": "F5.3", "hhi": "F5.10",
    "unit-cost-recipe": "F6.2", "cost-curves": "F6.3", "bottleneck": "F6.10",
    "markup-margin": "F6.5", "break-even": "F6.6", "competitive-supply": "F6.4",
    "accounting-equation": "F7.5",
    "future-value": "F8.3", "present-value": "F8.5", "annuity": "F8.8", "fisher": "F8.7",
    "expected-value": "F9.9",
    "cogs-vs-cash": "F10.4", "fifo-average": "F10.6",
    "scarce-resource": "F11.4", "evpi": "F11.6", "ema": "F11.8", "newsvendor": "F11.9",
    "npv": "F13.1", "bond-price": "F13.4", "gordon": "F13.5", "portfolio-risk": "F13.7",
    "cash-conversion": "F14.5",
    "real-growth": "F2.7", "inflation-real-wage": "F2.7",
}
for g in GENERATORS:
    if g.topic in REUSE:
        FGENERATORS.append(Generator(REUSE[g.topic], g.topic, g.build))


def fgen(lesson: str, topic: str):
    def wrap(fn):
        FGENERATORS.append(Generator(lesson, topic, fn))
        return fn
    return wrap


def phi(z: float) -> float:
    return 0.5 * (1 + math.erf(z / math.sqrt(2)))


# ============================================================ F2 numbers
@fgen("F2.1", "percent-of")
def _(rng):
    rate = rng.choice([5, 8, 12, 15, 18, 22, 25, 35])
    whole = rng.choice([80, 120, 240, 350, 480, 1250])
    return Exercise(f"What is {rate} % of {whole}?", rate * whole / 100,
                    f"{rate}/100 × {whole} = {rate * whole / 100:g}.", "part = rate × whole.")


@fgen("F2.1", "vat-net")
def _(rng):
    vat = rng.choice([4, 10, 22])
    net = rng.choice([25, 40, 50, 80, 120, 200])
    gross = round(net * (1 + vat / 100), 2)
    return Exercise(f"A price of €{gross:g} includes {vat} % VAT. Price without VAT (€)?", gross / (1 + vat / 100),
                    f"{gross:g}/(1 + {vat / 100:g}) = {net}.", "Divide by (1 + VAT rate).",
                    traps={gross * (1 - vat / 100): "VAT is a % of the NET price: divide, don't subtract."})


@fgen("F2.2", "percent-change")
def _(rng):
    old = rng.choice([40, 50, 80, 120, 200, 250])
    new = old + rng.choice([-30, -20, -10, 6, 10, 15, 30]) * old // 100
    ch = 100 * (new - old) / old
    return Exercise(f"A value goes from {old} to {new}. Percentage change (%)?", ch,
                    f"({new} − {old})/{old} × 100 = {ch:.2f} %.", "Divide by the OLD value.",
                    traps={100 * (new - old) / new: "the base is the old value, not the new one."},
                    percent_ok=True)


@fgen("F2.3", "points-vs-percent")
def _(rng):
    a = rng.choice([2, 4, 5, 8, 10])
    b = a + rng.choice([-1, 1, 2, 3])
    rel = 100 * (b - a) / a
    return Exercise(f"A rate moves from {a} % to {b} %. Relative change in percent?", rel,
                    f"({b} − {a})/{a} = {rel:.2f} % (the change is {b - a} percentage points).",
                    "Relative change divides by the starting rate.",
                    traps={b - a: "that's the change in percentage POINTS."})


@fgen("F2.4", "cagr")
def _(rng):
    start = rng.choice([100, 200, 500])
    n = rng.choice([2, 3, 4, 5])
    end = start * rng.choice([1.2, 1.3, 1.5, 1.8, 2.0])
    g = 100 * ((end / start) ** (1 / n) - 1)
    return Exercise(f"Revenue grows from {start} to {end:g} in {n} years. CAGR (%)?", g,
                    f"({end:g}/{start})^(1/{n}) − 1 = {g:.2f} %.", "CAGR = (end/start)^(1/n) − 1.",
                    traps={100 * (end / start - 1) / n: "simple averaging ignores compounding."},
                    percent_ok=True)


@fgen("F2.6", "index-change")
def _(rng):
    i1 = rng.choice([104, 110, 115, 120, 125, 132])
    i2 = i1 + rng.randint(3, 15)
    ch = 100 * (i2 - i1) / i1
    return Exercise(f"A price index goes from {i1} to {i2}. Percentage change?", ch,
                    f"({i2} − {i1})/{i1} = {ch:.2f} %.", "Divide the change by the old index.",
                    traps={float(i2 - i1): "that's the change in index POINTS."}, percent_ok=True)


@fgen("F2.9", "weighted-price")
def _(rng):
    q1, p1 = rng.choice([10, 20, 30]), rng.choice([4, 5, 6])
    q2, p2 = rng.choice([30, 40, 60]), rng.choice([8, 9, 12])
    avg = (q1 * p1 + q2 * p2) / (q1 + q2)
    return Exercise(f"You buy {q1} units at €{p1} and {q2} units at €{p2}. Average price paid (€)?", avg,
                    f"({q1 * p1} + {q2 * p2})/{q1 + q2} = {avg:.2f}.", "Weight each price by its quantity.",
                    traps={(p1 + p2) / 2: "weight by quantities."})


# ============================================================ F4 describing data
def _data(rng, n=None):
    n = n or rng.choice([5, 6, 7, 8])
    return [rng.randint(2, 40) for _ in range(n)]


@fgen("F4.4", "mean")
def _(rng):
    xs = _data(rng)
    m = sum(xs) / len(xs)
    return Exercise(f"Mean of {xs}?", m, f"{sum(xs)}/{len(xs)} = {m:.2f}.", "Sum / count.")


@fgen("F4.5", "median")
def _(rng):
    xs = _data(rng)
    s = sorted(xs)
    n = len(s)
    med = s[n // 2] if n % 2 else (s[n // 2 - 1] + s[n // 2]) / 2
    return Exercise(f"Median of {xs}?", med, f"Sorted: {s} → {med:g}.", "Sort first.",
                    traps={xs[len(xs) // 2] if len(xs) % 2 else (xs[n // 2 - 1] + xs[n // 2]) / 2:
                           "sort the data before taking the middle value."})


@fgen("F4.9", "sample-sd")
def _(rng):
    xs = _data(rng, rng.choice([4, 5]))
    m = sum(xs) / len(xs)
    ss = sum((x - m) ** 2 for x in xs)
    sd = math.sqrt(ss / (len(xs) - 1))
    return Exercise(f"Sample standard deviation of {xs}?", sd,
                    f"mean {m:.2f}; squared deviations sum {ss:.2f}; /(n−1) = {ss / (len(xs) - 1):.3f}; √ = {sd:.3f}.",
                    "s = √(Σ(x − x̄)²/(n − 1)).",
                    traps={math.sqrt(ss / len(xs)): "for a SAMPLE divide by n − 1.",
                           ss / (len(xs) - 1): "that's the variance; take the square root."})


@fgen("F4.10", "z-score")
def _(rng):
    mu, sd = rng.choice([(50, 8), (100, 15), (200, 25), (70, 5)])
    x = mu + sd * rng.choice([-2, -1.5, -1, 0.5, 1.2, 2, 2.5])
    z = (x - mu) / sd
    return Exercise(f"Mean {mu}, SD {sd}. z-score of {x:g}?", z, f"({x:g} − {mu})/{sd} = {z:.2f}.",
                    "z = (x − mean)/SD.")


@fgen("F4.12", "cv")
def _(rng):
    m = rng.choice([40, 80, 200, 500])
    sd = m * rng.choice([0.1, 0.15, 0.2, 0.25, 0.4])
    return Exercise(f"Mean {m}, SD {sd:g}. Coefficient of variation (decimal)?", sd / m,
                    f"{sd:g}/{m} = {sd / m:.3f}.", "CV = SD/mean.", percent_ok=True, decimals=3)


# ============================================================ F5/F6
@fgen("F6.4", "profit")
def _(rng):
    p, v = rng.choice([(50, 30), (80, 45), (25, 15), (120, 70)])
    fc = rng.choice([5000, 8000, 12000])
    q = rng.choice([200, 400, 600, 800])
    prof = (p - v) * q - fc
    return Exercise(f"Price €{p}, variable cost €{v}, fixed costs €{fc:,}, quantity {q}. Profit (€)?", prof,
                    f"({p} − {v})·{q} − {fc:,} = {prof:,}.", "profit = (P − v)Q − FC.",
                    traps={(p - v) * q: "don't forget fixed costs."}, decimals=0)


@fgen("F6.12", "multi-product-breakeven")
def _(rng):
    sa = rng.choice([0.5, 0.6, 0.75])
    ca, cb = rng.choice([10, 20, 24]), rng.choice([30, 40, 45])
    fc = rng.choice([30000, 48000, 60000])
    w = sa * ca + (1 - sa) * cb
    return Exercise(f"Sales mix {sa:.0%} A (CM €{ca}) / {1 - sa:.0%} B (CM €{cb}); fixed costs €{fc:,}. "
                    "Total break-even units?", fc / w,
                    f"weighted CM = {w:.2f}; {fc:,}/{w:.2f} = {fc / w:,.1f}.", "Use the mix-weighted CM.",
                    traps={fc / ((ca + cb) / 2): "weight the CMs by the sales mix."}, decimals=1)


# ============================================================ F7/F10/F14 accounting
@fgen("F7.6", "transaction-cash")
def _(rng):
    cap = rng.choice([10000, 15000, 20000])
    buy = rng.choice([3000, 4000, 5000])
    share = rng.choice([0.5, 0.75, 1.0])
    sale = round(buy * share * rng.choice([1.5, 1.6, 2.0]))
    return Exercise(f"Start with €{cap:,} cash (owners' capital). Buy stock for €{buy:,} cash; sell {share:.0%} of it "
                    f"for €{sale:,} cash. Equity now (€)?", cap + sale - buy * share,
                    f"profit = {sale:,} − {buy * share:,.0f} = {sale - buy * share:,.0f}; equity = {cap:,} + profit.",
                    "Equity changes by the profit, not by cash movements.",
                    traps={cap - buy + sale: "that's CASH; unsold stock is still an asset."}, decimals=0)


@fgen("F10.5", "depreciation")
def _(rng):
    cost = rng.choice([20000, 30000, 50000, 80000])
    res = rng.choice([0, 2000, 5000, 10000])
    life = rng.choice([4, 5, 8])
    yrs = rng.randint(1, life - 1)
    dep = (cost - res) / life
    return Exercise(f"Asset cost €{cost:,}, residual €{res:,}, life {life} years, straight-line. Book value after "
                    f"{yrs} years (€)?", cost - dep * yrs,
                    f"depreciation {dep:,.0f}/year; {cost:,} − {yrs}·{dep:,.0f} = {cost - dep * yrs:,.0f}.",
                    "Book value = cost − accumulated depreciation.",
                    traps={cost - cost / life * yrs: "subtract the residual value before dividing by the life."})


@fgen("F10.9", "ocf-indirect")
def _(rng):
    ni, dep = rng.randint(40, 120), rng.randint(10, 40)
    dinv, drec, dpay = rng.randint(-20, 60), rng.randint(-20, 40), rng.randint(-15, 30)
    ocf = ni + dep - dinv - drec + dpay
    return Exercise(f"Net profit {ni}, depreciation {dep}, change in inventory {dinv:+d}, change in receivables "
                    f"{drec:+d}, change in payables {dpay:+d}. Operating cash flow?", ocf,
                    f"{ni} + {dep} − ({dinv}) − ({drec}) + ({dpay}) = {ocf}.",
                    "Add back depreciation; increases in inventory/receivables use cash; payables provide it.",
                    traps={ni + dep + dinv + drec + dpay: "increases in inventory and receivables REDUCE cash."},
                    decimals=0)


@fgen("F14.3", "liquidity-ratios")
def _(rng):
    ca = rng.choice([300, 450, 600])
    inv = int(ca * rng.choice([0.3, 0.5, 0.6]))
    cl = rng.choice([200, 250, 300, 400])
    q = (ca - inv) / cl
    return Exercise(f"Current assets {ca} (of which inventory {inv}), current liabilities {cl}. Quick ratio?", q,
                    f"({ca} − {inv})/{cl} = {q:.3f}.", "Exclude inventory.",
                    traps={ca / cl: "that's the current ratio; the quick ratio excludes inventory."}, decimals=3)


@fgen("F14.7", "dupont")
def _(rng):
    m, t, em = rng.choice([0.03, 0.05, 0.08]), rng.choice([1.2, 1.5, 2.0, 2.5]), rng.choice([1.5, 2.0, 2.5])
    roe = 100 * m * t * em
    return Exercise(f"Net margin {m:.0%}, asset turnover {t}, equity multiplier {em}. ROE (%)?", roe,
                    f"{m} × {t} × {em} = {roe / 100:.4f}.", "ROE = margin × turnover × multiplier.", percent_ok=True)


# ============================================================ F8/F13 finance
@fgen("F8.2", "simple-interest")
def _(rng):
    p, r, months = rng.choice([2000, 5000, 10000]), rng.choice([3, 4, 5, 6]), rng.choice([6, 9, 18, 24])
    i = p * r / 100 * months / 12
    return Exercise(f"€{p:,} at {r} % simple interest for {months} months. Interest (€)?", i,
                    f"{p:,} × {r / 100} × {months}/12 = {i:,.2f}.", "Interest = P·r·t with t in years.",
                    traps={p * r / 100 * months: "convert months to years."})


@fgen("F8.4", "ear")
def _(rng):
    r, m = rng.choice([4, 6, 8, 12]), rng.choice([2, 4, 12])
    ear = 100 * ((1 + r / 100 / m) ** m - 1)
    return Exercise(f"Nominal {r} % compounded {m} times a year. Effective annual rate (%)?", ear,
                    f"(1 + {r / 100}/{m})^{m} − 1 = {ear:.3f} %.", "EAR = (1 + r/m)^m − 1.",
                    traps={float(r): "compounding within the year raises the effective rate."},
                    abs_tol=0.005, rel_tol=0, percent_ok=True, decimals=3)


@fgen("F8.9", "perpetuity")
def _(rng):
    c, r = rng.choice([100, 300, 500, 1200]), rng.choice([0.04, 0.05, 0.06, 0.08])
    g = rng.choice([0, 0, 0.01, 0.02])
    pv = c / (r - g)
    return Exercise(f"Payment €{c} next year, growing {g:.0%} a year forever, discount rate {r:.0%}. PV (€)?", pv,
                    f"{c}/({r} − {g}) = {pv:,.2f}.", "Growing perpetuity: C/(r − g).",
                    traps={c / r: "subtract the growth rate."} if g else {})


@fgen("F8.10", "loan-payment")
def _(rng):
    loan, r, n = rng.choice([10000, 20000, 50000]), rng.choice([0.03, 0.04, 0.05, 0.06]), rng.choice([3, 4, 5, 10])
    pay = loan * r / (1 - (1 + r) ** -n)
    return Exercise(f"Loan €{loan:,} at {r:.0%} for {n} years, equal annual payments. Payment (€)?", pay,
                    f"{loan:,} × {r}/(1 − {1 + r}^−{n}) = {pay:,.2f}.", "C = L·r/(1 − (1 + r)^−n).",
                    traps={loan / n: "that ignores interest.", loan * (1 + r) / n: "interest is on the declining balance."})


@fgen("F13.2", "irr-simple")
def _(rng):
    c0, n, g = rng.choice([500, 800, 1000, 2000]), rng.choice([1, 2, 3]), rng.choice([0.05, 0.08, 0.1, 0.12, 0.2])
    cf = round(c0 * (1 + g) ** n, 2)
    return Exercise(f"Invest €{c0:,} today, receive €{cf:,} in {n} year(s). IRR (%)?", 100 * g,
                    f"({cf}/{c0})^(1/{n}) − 1 = {g:.2%}.", "Solve c0·(1 + IRR)^n = CF.",
                    traps={100 * (cf / c0 - 1) / n: "growth compounds; take the n-th root."} if n > 1 else {},
                    percent_ok=True, abs_tol=0.02, rel_tol=0)


@fgen("F13.3", "payback")
def _(rng):
    c0 = rng.choice([900, 1000, 1500])
    while True:
        flows = [rng.choice([200, 300, 400, 500]) for _ in range(5)]
        if sum(flows) >= c0:
            break
    cum, year = 0.0, 0.0
    for t, f in enumerate(flows, 1):
        if cum + f >= c0:
            year = t - 1 + (c0 - cum) / f
            break
        cum += f
    return Exercise(f"Invest €{c0:,}; cash flows {flows} at the end of years 1–5. Payback (years)?", year,
                    f"cumulative reaches {c0} during year {math.ceil(year)}: {year:.2f} years.",
                    "Add flows until the investment is recovered; interpolate within the year.", abs_tol=0.01,
                    rel_tol=0)


@fgen("F13.8", "leverage-roe")
def _(rng):
    assets, ret = rng.choice([100, 200, 500]), rng.choice([0.03, 0.06, 0.08, 0.1])
    debt_share, rate = rng.choice([0.3, 0.5, 0.6]), rng.choice([0.03, 0.04, 0.05])
    d = assets * debt_share
    e = assets - d
    roe = 100 * (assets * ret - d * rate) / e
    return Exercise(f"Assets €{assets} earn {ret:.0%}; debt €{d:g} at {rate:.0%}; no taxes. ROE (%)?", roe,
                    f"({assets * ret:g} − {d * rate:g})/{e:g} = {roe:.2f} %.", "ROE = (EBIT − interest)/equity.",
                    traps={100 * ret: "that's the return on ASSETS; leverage changes ROE."}, percent_ok=True)


@fgen("F13.10", "wacc")
def _(rng):
    we, re_, rd, t = rng.choice([0.5, 0.6, 0.7]), rng.choice([0.08, 0.1, 0.12]), rng.choice([0.03, 0.04, 0.05]), rng.choice([0, 0.24, 0.25])
    w = 100 * (we * re_ + (1 - we) * rd * (1 - t))
    return Exercise(f"{we:.0%} equity at {re_:.0%}, {1 - we:.0%} debt at {rd:.0%}, tax {t:.0%}. WACC (%)?", w,
                    f"{we}·{re_} + {1 - we:.1f}·{rd}·(1 − {t}) = {w:.3f} %.", "Weight each cost; debt after tax.",
                    traps={100 * (we * re_ + (1 - we) * rd): "debt cost is after tax."} if t else {},
                    percent_ok=True, decimals=3)


# ============================================================ F9/F12 probability
@fgen("F9.2", "at-least-one")
def _(rng):
    p, n = rng.choice([0.05, 0.1, 0.2, 0.3]), rng.choice([2, 3, 4, 5, 6])
    ans = 1 - (1 - p) ** n
    return Exercise(f"Each of {n} independent events happens with probability {p}. P(at least one)?", ans,
                    f"1 − (1 − {p})^{n} = {ans:.4f}.", "Use the complement: 1 − P(none).",
                    traps={min(1.0, n * p): "probabilities of overlapping events don't simply add."},
                    abs_tol=0.0005, rel_tol=0, percent_ok=True, decimals=4)


@fgen("F9.4", "table-conditional")
def _(rng):
    a, b, c, d = (rng.randint(10, 90) for _ in range(4))
    return Exercise(f"Table — saw ad: bought {a}, didn't {b}; no ad: bought {c}, didn't {d}. P(bought | saw ad)?",
                    a / (a + b), f"{a}/({a} + {b}) = {a / (a + b):.4f}.", "Restrict to the 'saw ad' row.",
                    traps={a / (a + c): "that's P(saw ad | bought).", a / (a + b + c + d): "that's the JOINT probability."},
                    abs_tol=0.0005, rel_tol=0, percent_ok=True, decimals=4)


@fgen("F9.8", "bayes")
def _(rng):
    base = rng.choice([0.01, 0.02, 0.05, 0.1])
    sens = rng.choice([0.8, 0.9, 0.95, 0.99])
    fpr = rng.choice([0.02, 0.05, 0.1])
    post = sens * base / (sens * base + fpr * (1 - base))
    return Exercise(f"Prevalence {base:.0%}; a test detects {sens:.0%} of true cases and flags {fpr:.0%} of negatives. "
                    "P(true case | flagged)?", post,
                    f"{sens}·{base} / ({sens}·{base} + {fpr}·{1 - base:.2f}) = {post:.4f}.",
                    "Bayes: P(case|flag) = P(flag|case)P(case)/P(flag).",
                    traps={sens: "that's P(flagged | case), not the reverse."},
                    abs_tol=0.0005, rel_tol=0, percent_ok=True, decimals=4)


@fgen("F9.11", "combinations")
def _(rng):
    n, k = rng.choice([6, 8, 9, 10, 12]), rng.choice([2, 3, 4])
    return Exercise(f"How many ways to choose {k} items from {n} (order doesn't matter)?", math.comb(n, k),
                    f"C({n},{k}) = {math.comb(n, k)}.", "n!/(k!(n − k)!).",
                    traps={math.perm(n, k): "that counts ordered arrangements (permutations)."}, decimals=0)


@fgen("F12.2", "rv-expectation")
def _(rng):
    xs = sorted(rng.sample([0, 1, 2, 3, 4, 5, 10], 3))
    ps = rng.choice([(0.2, 0.5, 0.3), (0.1, 0.6, 0.3), (0.3, 0.3, 0.4)])
    e = sum(x * p for x, p in zip(xs, ps))
    return Exercise("X takes " + ", ".join(f"{x} w.p. {p}" for x, p in zip(xs, ps)) + ". E[X]?", e,
                    " + ".join(f"{x}·{p}" for x, p in zip(xs, ps)) + f" = {e:.2f}.", "Σ x·P(x).")


@fgen("F12.5", "binomial")
def _(rng):
    n, p, k = rng.choice([4, 5, 6, 8, 10]), rng.choice([0.1, 0.2, 0.3, 0.5]), rng.randint(0, 3)
    pk = math.comb(n, k) * p ** k * (1 - p) ** (n - k)
    return Exercise(f"Binomial n = {n}, p = {p}. P(X = {k})?", pk,
                    f"C({n},{k})·{p}^{k}·{1 - p:.1f}^{n - k} = {pk:.4f}.", "C(n,k) p^k (1−p)^(n−k).",
                    traps={p ** k * (1 - p) ** (n - k): "multiply by C(n,k), the number of orderings."},
                    abs_tol=0.0005, rel_tol=0, percent_ok=True, decimals=4)


@fgen("F12.6", "poisson")
def _(rng):
    lam, k = rng.choice([1, 2, 3, 4]), rng.randint(0, 3)
    pk = math.exp(-lam) * lam ** k / math.factorial(k)
    return Exercise(f"Poisson with mean {lam}. P(X = {k})?", pk,
                    f"e^−{lam}·{lam}^{k}/{k}! = {pk:.4f}.", "e^(−λ) λ^k / k!.",
                    abs_tol=0.0005, rel_tol=0, percent_ok=True, decimals=4)


@fgen("F12.9", "normal-prob")
def _(rng):
    mu, sd = rng.choice([(50, 10), (100, 20), (200, 40), (500, 50)])
    z = rng.choice([-1.5, -1, -0.5, 0.5, 1, 1.5, 2])
    x = mu + z * sd
    above = rng.random() < 0.5
    ans = 1 - phi(z) if above else phi(z)
    return Exercise(f"X ~ N({mu}, {sd}²). P(X {'>' if above else '<'} {x:g})?  (Φ(0.5)=0.6915, Φ(1)=0.8413, "
                    "Φ(1.5)=0.9332, Φ(2)=0.9772)", ans,
                    f"z = {z}; {'1 − Φ(z)' if above else 'Φ(z)'} = {ans:.4f}.", "Standardise, then use Φ; Φ(−z) = 1 − Φ(z).",
                    traps={1 - ans: "check the direction (above vs below)."},
                    abs_tol=0.0006, rel_tol=0, percent_ok=True, decimals=4)


@fgen("F12.10", "normal-quantile")
def _(rng):
    mu, sd = rng.choice([(200, 40), (500, 60), (80, 15), (1000, 120)])
    lvl, z = rng.choice([(90, 1.28), (95, 1.645), (99, 2.33)])
    return Exercise(f"Demand ~ N({mu}, {sd}²). Stock covering demand on {lvl} % of days? (z = {z})", mu + z * sd,
                    f"{mu} + {z}·{sd} = {mu + z * sd:.1f}.", "x = μ + z·σ.", decimals=1)


@fgen("F12.11", "pooling")
def _(rng):
    n, sd = rng.choice([4, 9, 16, 25]), rng.choice([10, 20, 30])
    return Exercise(f"{n} independent quantities, each with SD {sd}. SD of their sum?", math.sqrt(n) * sd,
                    f"√{n}·{sd} = {math.sqrt(n) * sd:g}.", "Variances add for independent variables.",
                    traps={float(n * sd): "standard deviations don't add."})


# ============================================================ F15/F16 inference & regression
@fgen("F15.2", "standard-error")
def _(rng):
    sd, n = rng.choice([12, 20, 30, 40]), rng.choice([16, 25, 36, 64, 100])
    return Exercise(f"σ = {sd}, n = {n}. Standard error of the mean?", sd / math.sqrt(n),
                    f"{sd}/√{n} = {sd / math.sqrt(n):.3f}.", "σ/√n.",
                    traps={sd / n: "divide by √n, not n."}, decimals=3)


@fgen("F15.4", "ci-mean")
def _(rng):
    xbar, sd, n = rng.choice([50, 80, 120]), rng.choice([10, 15, 20]), rng.choice([25, 36, 64, 100])
    lo = xbar - 1.96 * sd / math.sqrt(n)
    return Exercise(f"x̄ = {xbar}, σ = {sd}, n = {n}. Lower bound of the 95 % confidence interval?", lo,
                    f"{xbar} − 1.96·{sd}/√{n} = {lo:.3f}.", "x̄ − 1.96·σ/√n.",
                    traps={xbar - 1.96 * sd: "use the standard ERROR σ/√n."}, abs_tol=0.01, rel_tol=0, decimals=3)


@fgen("F15.6", "ci-proportion")
def _(rng):
    n = rng.choice([200, 400, 600, 1000])
    k = int(n * rng.choice([0.2, 0.3, 0.45, 0.5]))
    p = k / n
    m = 1.96 * math.sqrt(p * (1 - p) / n)
    return Exercise(f"{k} of {n} respond yes. 95 % margin of error for the proportion (decimal)?", m,
                    f"1.96·√({p:.2f}·{1 - p:.2f}/{n}) = {m:.4f}.", "z*·√(p̂(1−p̂)/n).",
                    abs_tol=0.0005, rel_tol=0, percent_ok=True, decimals=4)


@fgen("F15.8", "z-test")
def _(rng):
    mu0, sd, n = rng.choice([50, 100, 200]), rng.choice([8, 12, 20]), rng.choice([16, 36, 64])
    se = sd / math.sqrt(n)
    xbar = mu0 + se * rng.choice([-2.5, -1.5, -1, 1, 1.5, 2, 3])
    z = (xbar - mu0) / se
    return Exercise(f"H₀: μ = {mu0}. Sample n = {n}, x̄ = {xbar:g}, σ = {sd}. z statistic?", z,
                    f"({xbar:g} − {mu0})/({sd}/√{n}) = {z:.2f}.", "z = (x̄ − μ₀)/(σ/√n).",
                    traps={(xbar - mu0) / sd: "divide by the standard error, σ/√n."})


@fgen("F16.5", "regression-slope")
def _(rng):
    xs = [1, 2, 3, 4, 5]
    b, a = rng.choice([-3, -2, 2, 3, 4]), rng.choice([10, 20, 30])
    ys = [a + b * x + rng.choice([-1, 0, 1]) for x in xs]
    mx, my = 3, sum(ys) / 5
    sxy = sum((x - mx) * (y - my) for x, y in zip(xs, ys))
    slope = sxy / 10
    return Exercise(f"x = {xs}, y = {ys}. Least-squares slope?", slope,
                    f"Σ(x−x̄)(y−ȳ) = {sxy:.2f}; Σ(x−x̄)² = 10; b = {slope:.3f}.", "b = Sxy/Sxx.", decimals=3)


@fgen("F16.7", "r-squared")
def _(rng):
    sst = rng.choice([200, 500, 800, 1000])
    sse = int(sst * rng.choice([0.1, 0.25, 0.4, 0.6]))
    return Exercise(f"Total sum of squares {sst}, residual sum of squares {sse}. R²?", 1 - sse / sst,
                    f"1 − {sse}/{sst} = {1 - sse / sst:.3f}.", "R² = 1 − SSE/SST.",
                    traps={sse / sst: "R² is the EXPLAINED share: 1 − SSE/SST."}, percent_ok=True, decimals=3)


# ============================================================ F17 statistics at work
@fgen("F17.1", "moving-average")
def _(rng):
    xs = [rng.randint(10, 60) for _ in range(6)]
    k = rng.choice([3, 4])
    ma = sum(xs[-k:]) / k
    return Exercise(f"Sales {xs}. Trailing {k}-period moving average at the last period?", ma,
                    f"{xs[-k:]} → {ma:.2f}.", "Average the last k values.")


@fgen("F17.2", "seasonal-index")
def _(rng):
    idx = rng.choice([0.6, 0.8, 1.2, 1.25, 1.4])
    sales = rng.choice([150, 240, 300, 420])
    return Exercise(f"Seasonal index {idx}; actual sales {sales}. Deseasonalised sales?", sales / idx,
                    f"{sales}/{idx} = {sales / idx:.2f}.", "Divide by the seasonal index.",
                    traps={sales * idx: "divide by the index, don't multiply."})


@fgen("F17.3", "mape")
def _(rng):
    acts = [rng.choice([50, 80, 100, 200]) for _ in range(3)]
    fcs = [a + rng.choice([-20, -10, 10, 20]) for a in acts]
    mape = 100 * sum(abs(a - f) / a for a, f in zip(acts, fcs)) / 3
    return Exercise(f"Actuals {acts}, forecasts {fcs}. MAPE (%)?", mape,
                    f"mean of |error|/actual = {mape:.2f} %.", "Average the absolute % errors.",
                    traps={100 * sum(abs(a - f) / f for a, f in zip(acts, fcs)) / 3: "divide by the ACTUAL values."},
                    percent_ok=True)


# ============================================================ F3 graphs, F18 cases
@fgen("F3.2", "slope")
def _(rng):
    x1, x2 = rng.randint(0, 10), rng.randint(12, 40)
    y1 = rng.randint(10, 100)
    b = rng.choice([-3, -2, -0.5, 0.5, 2, 4])
    y2 = y1 + b * (x2 - x1)
    return Exercise(f"Slope of the line through ({x1}, {y1}) and ({x2}, {y2:g})?", b,
                    f"({y2:g} − {y1})/({x2} − {x1}) = {b}.", "rise / run = Δy/Δx.",
                    traps={1 / b: "slope is Δy/Δx, not Δx/Δy."})


@fgen("F18.3", "special-order")
def _(rng):
    cap, util = 10000, rng.choice([0.7, 0.8, 0.9])
    p, v = rng.choice([(50, 30), (60, 35), (40, 25)])
    order = rng.choice([2000, 3000, 4000])
    offer = v + rng.choice([4, 6, 8, 10])
    spare = int(cap * (1 - util))
    lost = max(0, order - spare)
    gain = (offer - v) * order - lost * (p - v)
    return Exercise(f"Capacity {cap:,} units, used at {util:.0%}; regular price €{p}, variable cost €{v}. A one-off "
                    f"order of {order:,} units at €{offer}. Net gain from accepting (€)?", gain,
                    f"spare {spare:,}; lost regular sales {lost:,} × {p - v} = {lost * (p - v):,}; "
                    f"order contribution {(offer - v) * order:,}; net {gain:,}.",
                    "Count the contribution lost on regular sales displaced by the order.",
                    traps={float((offer - v) * order): "beyond spare capacity the order displaces regular sales."},
                    decimals=0)
