"""Parametric exercise generators: unlimited numeric problems with worked
solutions and diagnosis of typical wrong answers ("traps")."""

from __future__ import annotations

import math
from dataclasses import dataclass, field
from typing import Callable


@dataclass
class Exercise:
    prompt: str
    answer: float
    solution: str
    hint: str
    lesson: str = ""
    topic: str = ""
    unit: str = ""
    traps: dict = field(default_factory=dict)   # wrong value -> explanation
    rel_tol: float = 0.01
    abs_tol: float = 0.011
    percent_ok: bool = False
    decimals: int = 2

    def fmt(self, value: float) -> str:
        text = f"{value:,.{self.decimals}f}"
        return text.rstrip("0").rstrip(".") if "." in text else text

    def matches(self, value: float, target: float | None = None) -> bool:
        """Is `value` the right answer (or `target`)? Accepts 25 for 0.25 when percent_ok."""
        target = self.answer if target is None else target
        if math.isclose(value, target, rel_tol=self.rel_tol, abs_tol=self.abs_tol):
            return True
        if self.percent_ok:
            # scaled variants use relative tolerance only, so 4 never matches 0
            for scaled in (value / 100, value * 100):
                if math.isclose(scaled, target, rel_tol=self.rel_tol, abs_tol=1e-9):
                    return True
        return False

    def diagnose(self, value: float) -> str | None:
        for wrong, why in self.traps.items():
            if self.matches(value, wrong):
                return why
        return None


@dataclass
class Generator:
    lesson: str
    topic: str
    build: Callable

    def make(self, rng) -> Exercise:
        ex = self.build(rng)
        ex.lesson, ex.topic = self.lesson, self.topic
        # drop traps that coincide with the right answer for these numbers
        ex.traps = {k: v for k, v in ex.traps.items()
                    if not ex.matches(k) and not ex.matches(ex.answer, k)}
        return ex


GENERATORS: list[Generator] = []


def gen(lesson: str, topic: str):
    def wrap(fn):
        GENERATORS.append(Generator(lesson, topic, fn))
        return fn
    return wrap


def r2(x: float) -> float:
    return round(x, 2)


# =============================================================================
# M1 Microeconomics
# =============================================================================

@gen("1.1", "opportunity-cost")
def _(rng):
    a_x, a_y = rng.choice([(6, 3), (8, 2), (10, 5), (9, 3)])
    b_x, b_y = rng.choice([(2, 2), (3, 3), (4, 4), (2, 1)])
    # opportunity cost of 1 Y for each, in units of X
    oa, ob = a_x / a_y, b_x / b_y
    if math.isclose(oa, ob):
        b_x += 1
        ob = b_x / b_y
    who = "Anna" if oa < ob else "Bruno"
    return Exercise(
        prompt=(f"In one hour Anna makes {a_x} pizzas or {a_y} cakes; Bruno makes {b_x} pizzas or "
                f"{b_y} cakes.\nWhat is the opportunity cost of ONE cake for the person with the "
                "comparative advantage in cakes (in pizzas)?"),
        answer=min(oa, ob),
        solution=(f"Anna: 1 cake costs {a_x}/{a_y} = {oa:.2f} pizzas. Bruno: 1 cake costs "
                  f"{b_x}/{b_y} = {ob:.2f} pizzas.\n{who} gives up fewer pizzas per cake → comparative "
                  f"advantage in cakes, opportunity cost {min(oa, ob):.2f} pizzas."),
        hint="Opportunity cost of a cake = pizzas given up per cake = (pizzas per hour)/(cakes per hour).",
        traps={max(oa, ob): "that is the opportunity cost of the OTHER person — compare the two and take "
                            "the lower one.",
               1 / min(oa, ob): "you inverted the ratio: that is cakes per pizza."},
    )


@gen("1.1", "marginal-decision")
def _(rng):
    price = rng.choice([1.2, 1.5, 2.0, 2.5])
    mcs = sorted(r2(price * rng.uniform(0.3, 1.6)) for _ in range(6))
    units = sum(1 for m in mcs if m <= price)
    return Exercise(
        prompt=(f"Each extra unit sells for €{price}. Marginal costs of units 1–6 are "
                f"{', '.join(f'€{m}' for m in mcs)}.\nHow many units maximise profit?"),
        answer=units, decimals=0, abs_tol=0.01, rel_tol=0,
        solution=f"Produce every unit whose MC ≤ price (€{price}): {units} unit(s).",
        hint="Compare marginal benefit (the price) with each unit's marginal cost.",
        traps={6: "producing everything ignores that later units cost more than they earn."},
    )


@gen("1.2", "equilibrium-price")
def _(rng):
    b, d = rng.randint(1, 4), rng.randint(1, 4)
    p = rng.randint(10, 40)
    q = rng.randint(30, 90)
    a = q + b * p
    c = q - d * p
    return Exercise(
        prompt=f"Demand: Qd = {a} − {b}P.  Supply: Qs = {c:+d} + {d}P.\nFind the equilibrium price P*.",
        answer=p,
        solution=f"{a} − {b}P = {c} + {d}P ⇒ {a - c} = {b + d}P ⇒ P* = {p}; Q* = {a} − {b}·{p} = {q}.",
        hint="Set Qd = Qs and solve for P.",
        traps={q: "that is the equilibrium QUANTITY — the question asks for the price.",
               (a + c) / (b + d): "check the sign when you move the supply intercept across.",
               (a - c) / (b - d) if b != d else -1: "the slopes add up (b + d), they don't subtract."},
    )


@gen("1.2", "equilibrium-quantity-shift")
def _(rng):
    b, d = rng.randint(1, 3), rng.randint(1, 3)
    p0, q0 = rng.randint(10, 30), rng.randint(40, 80)
    a, c = q0 + b * p0, q0 - d * p0
    shift = rng.choice([10, 15, 20, 30])
    a2 = a + shift
    p1 = (a2 - c) / (b + d)
    q1 = a2 - b * p1
    return Exercise(
        prompt=(f"Initially Qd = {a} − {b}P and Qs = {c:+d} + {d}P. Demand rises to Qd = {a2} − {b}P.\n"
                "What is the NEW equilibrium quantity?"),
        answer=q1,
        solution=(f"{a2} − {b}P = {c} + {d}P ⇒ P = {a2 - c}/{b + d} = {p1:.2f}; "
                  f"Q = {a2} − {b}·{p1:.2f} = {q1:.2f} (was {q0})."),
        hint="Solve the new system exactly as before, with the new demand intercept.",
        traps={q0: "that is the OLD quantity.", q0 + shift: "the quantity does not rise by the full "
               "demand shift: the price also rises and chokes off part of it."},
    )


@gen("1.3", "arc-elasticity")
def _(rng):
    p1 = rng.choice([4, 5, 8, 10, 20])
    p2 = p1 + rng.choice([1, 2, 4])
    q1 = rng.choice([100, 120, 150, 200])
    q2 = q1 - rng.choice([10, 20, 30, 40, 50])
    e = ((q2 - q1) / ((q1 + q2) / 2)) / ((p2 - p1) / ((p1 + p2) / 2))
    simple = ((q2 - q1) / q1) / ((p2 - p1) / p1)
    return Exercise(
        prompt=(f"Price rises from €{p1} to €{p2}; quantity falls from {q1} to {q2}.\n"
                "Midpoint (arc) price elasticity of demand? (give the negative number)"),
        answer=e,
        solution=(f"%ΔQ = ({q2}−{q1})/{(q1 + q2) / 2} = {(q2 - q1) / ((q1 + q2) / 2):.4f}; "
                  f"%ΔP = ({p2}−{p1})/{(p1 + p2) / 2} = {(p2 - p1) / ((p1 + p2) / 2):.4f}; "
                  f"ε = {e:.3f}."),
        hint="Use averages of the two quantities and of the two prices as bases.",
        traps={-e: "sign: quantity falls when price rises, so ε is negative.",
               simple: "you used the starting values as bases; the midpoint formula uses averages.",
               1 / e: "you inverted the ratio: elasticity is %ΔQ / %ΔP."},
    )


@gen("1.3", "point-elasticity")
def _(rng):
    a = rng.choice([100, 120, 200, 240])
    b = rng.choice([1, 2, 4])
    p = rng.randint(int(a / b * 0.15), int(a / b * 0.85))
    q = a - b * p
    e = -b * p / q
    return Exercise(
        prompt=f"Demand Q = {a} − {b}P. Point price elasticity at P = {p}?",
        answer=e,
        solution=f"Q = {q}; ε = dQ/dP · P/Q = −{b}·{p}/{q} = {e:.3f}.",
        hint="ε = (dQ/dP)·(P/Q); dQ/dP is the slope coefficient.",
        traps={-b: "that is just the slope dQ/dP — multiply by P/Q.",
               -e: "sign: demand slopes down.", -b * q / p: "the ratio is P/Q, not Q/P."},
    )


@gen("1.3", "revenue-elasticity")
def _(rng):
    a, b = rng.choice([(100, 2), (120, 3), (200, 4), (90, 1)])
    p = r2(a / (2 * b))
    return Exercise(
        prompt=f"Demand Q = {a} − {b}P. At what price is total revenue maximised?",
        answer=p,
        solution=(f"TR = P(a − bP); dTR/dP = {a} − {2 * b}P = 0 ⇒ P = {p}. "
                  "Here demand is unit elastic."),
        hint="Maximise P·Q, or find where |ε| = 1 (the midpoint of linear demand).",
        traps={a / b: "that is the choke price, where Q = 0 and revenue is zero.",
               a / 2: "that is the revenue-maximising QUANTITY, not the price."},
    )


@gen("1.4", "consumer-surplus")
def _(rng):
    b, d = rng.randint(1, 3), rng.randint(1, 3)
    p, q = rng.randint(10, 30), rng.randint(30, 80)
    a, c = q + b * p, q - d * p
    choke = a / b
    cs = 0.5 * (choke - p) * q
    return Exercise(
        prompt=(f"Qd = {a} − {b}P, Qs = {c:+d} + {d}P. Compute consumer surplus at the "
                "competitive equilibrium."),
        answer=cs, decimals=1,
        solution=(f"P* = {p}, Q* = {q}. Choke price = {a}/{b} = {choke:.2f}. "
                  f"CS = ½·({choke:.2f} − {p})·{q} = {cs:.1f}."),
        hint="CS = triangle under demand and above the price: ½ × (choke price − P*) × Q*.",
        traps={(choke - p) * q: "you forgot the ½ for a triangle.",
               0.5 * (p - (-c / d)) * q: "that is PRODUCER surplus."},
    )


@gen("1.4", "tax-incidence")
def _(rng):
    b, d = rng.randint(1, 4), rng.randint(1, 4)
    t = rng.choice([5, 10, 15, 20])
    share = d / (b + d)
    return Exercise(
        prompt=(f"Demand Qd = 200 − {b}P, supply Qs = −20 + {d}P. A per-unit tax of €{t} is "
                "levied on sellers. By how many euros does the price paid by BUYERS rise?"),
        answer=t * share,
        solution=(f"Buyers' share = d/(b + d) = {d}/{b + d} = {share:.3f} → buyers pay "
                  f"{t}·{share:.3f} = €{t * share:.2f} more; sellers absorb €{t * (1 - share):.2f}."),
        hint="The less elastic side bears more; with slopes b (demand) and d (supply), buyers bear d/(b+d).",
        traps={t: "the legal payer doesn't bear the whole tax unless demand is perfectly inelastic.",
               t * b / (b + d): "you swapped the shares: buyers bear d/(b + d).",
               0: "sellers paying legally doesn't mean buyers are unaffected."},
    )


@gen("1.4", "deadweight-loss")
def _(rng):
    b, d = rng.randint(1, 3), rng.randint(1, 3)
    t = rng.choice([4, 6, 10, 12])
    dq = t * b * d / (b + d)
    dwl = 0.5 * t * dq
    return Exercise(
        prompt=(f"Qd = 150 − {b}P, Qs = {d}P − 30. A €{t} per-unit tax is introduced. "
                "Deadweight loss?"),
        answer=dwl, decimals=2,
        solution=(f"Quantity falls by t·b·d/(b+d) = {t}·{b}·{d}/{b + d} = {dq:.3f}. "
                  f"DWL = ½·t·ΔQ = ½·{t}·{dq:.3f} = {dwl:.2f}."),
        hint="DWL = ½ × tax × reduction in quantity; ΔQ = t·b·d/(b+d) for linear curves.",
        traps={t * dq: "you forgot the ½ (it's a triangle).",
               dq: "that is the fall in quantity, not the surplus lost."},
    )


@gen("1.5", "cobb-douglas-demand")
def _(rng):
    a = rng.choice([0.2, 0.25, 0.4, 0.5, 0.6, 0.75])
    m = rng.choice([100, 120, 200, 300, 500])
    px = rng.choice([2, 4, 5, 10])
    x = a * m / px
    return Exercise(
        prompt=(f"U = X^{a}·Y^{round(1 - a, 2)}. Income €{m}, price of X €{px}. "
                "How many units of X does the consumer buy?"),
        answer=x,
        solution=f"Cobb-Douglas: spend share {a} of income on X → X = {a}·{m}/{px} = {x:.2f}.",
        hint="With U = X^a Y^(1−a) the expenditure share on X is a.",
        traps={(1 - a) * m / px: "that share belongs to Y.", m / px: "not all income goes to X."},
    )


@gen("1.5", "wtp-demand")
def _(rng):
    n = rng.choice([50, 100, 200, 400])
    low = rng.choice([100, 150, 200])
    high = low + rng.choice([100, 200, 300])
    p = rng.randint(low + 10, high - 10)
    q = n * (high - p) / (high - low)
    return Exercise(
        prompt=(f"{n} customers each want one unit; their willingness to pay is uniformly "
                f"distributed between €{low} and €{high}. How many buy at price €{p}?"),
        answer=q, decimals=1, rel_tol=0.02,
        solution=f"Buyers are those with WTP ≥ {p}: share ({high} − {p})/({high} − {low}) → {q:.1f}.",
        hint="Demand at P = number of customers whose reservation price is at least P.",
        traps={n * (p - low) / (high - low): "that counts customers with WTP BELOW the price."},
    )


@gen("1.6", "cost-curves")
def _(rng):
    fc = rng.choice([64, 100, 144, 225, 400])
    v = rng.choice([2, 4, 5, 10])
    q = math.sqrt(fc)
    atc = fc / q + v + q
    return Exercise(
        prompt=f"TC = {fc} + {v}Q + Q². What is the minimum average total cost?",
        answer=atc,
        solution=(f"MC = {v} + 2Q, ATC = {fc}/Q + {v} + Q. Min ATC where MC = ATC ⇒ Q² = {fc} ⇒ "
                  f"Q = {q:.0f}; ATC = {fc}/{q:.0f} + {v} + {q:.0f} = {atc:.0f}."),
        hint="ATC is minimal where it equals MC.",
        traps={q: "that is the quantity where ATC is minimal; the question asks for the cost.",
               v: "that is AVC as Q → 0, ignoring fixed cost."},
    )


@gen("1.6", "unit-cost-recipe")
def _(rng):
    names = ["chip", "screen", "battery", "case"]
    prices = {n: rng.choice([5, 6, 8, 10, 12, 15, 20, 25]) for n in names}
    qty = {n: rng.choice([0, 1, 1, 2, 3]) for n in names}
    if sum(qty.values()) == 0:
        qty["chip"] = 1
    cost = sum(prices[n] * qty[n] for n in names)
    recipe = ", ".join(f"{qty[n]} {n}" for n in names if qty[n])
    plist = ", ".join(f"{n} €{prices[n]}" for n in names)
    return Exercise(
        prompt=f"A product needs {recipe}. Input prices: {plist}. Unit variable cost?",
        answer=cost,
        solution=" + ".join(f"{qty[n]}·{prices[n]}" for n in names if qty[n]) + f" = €{cost}.",
        hint="Multiply each input's price by the units needed, then add.",
        traps={sum(prices[n] for n in names if qty[n]): "multiply by the quantity of each input."},
    )


@gen("1.6", "bottleneck")
def _(rng):
    req = {"A": rng.choice([1, 2, 3]), "B": rng.choice([1, 2]), "C": rng.choice([1, 2, 3])}
    stock = {k: rng.randint(5, 40) for k in req}
    units = min(stock[k] // req[k] for k in req)
    return Exercise(
        prompt=("One unit of output needs " + ", ".join(f"{v} {k}" for k, v in req.items()) +
                ". You hold " + ", ".join(f"{stock[k]} {k}" for k in req) + ".\nMaximum output?"),
        answer=units, decimals=0, rel_tol=0, abs_tol=0.01,
        solution="Fixed proportions: output = min over inputs of floor(stock/requirement) = "
                 + ", ".join(f"{stock[k]}//{req[k]}={stock[k] // req[k]}" for k in req) + f" → {units}.",
        hint="The scarcest input relative to its requirement is the bottleneck.",
        traps={min(stock.values()): "divide each stock by how many units ONE output needs."},
    )


@gen("1.7", "competitive-supply")
def _(rng):
    v = rng.choice([2, 4, 6])
    p = rng.choice([20, 24, 30, 36, 40])
    fc = rng.choice([50, 100, 150])
    q = (p - v) / 2
    profit = p * q - (fc + v * q + q * q)
    return Exercise(
        prompt=f"Price-taking firm, TC = {fc} + {v}Q + Q², market price {p}. Profit at the optimal Q?",
        answer=profit,
        solution=(f"P = MC: {p} = {v} + 2Q ⇒ Q = {q:.1f}. TR = {p * q:.1f}; "
                  f"TC = {fc} + {v * q:.1f} + {q * q:.2f} = {fc + v * q + q * q:.2f}; profit = {profit:.2f}."),
        hint="Set price equal to marginal cost, then profit = TR − TC.",
        traps={p * q - (v * q + q * q): "don't forget the fixed cost in profit.",
               q: "that is the quantity, not the profit."},
    )


@gen("1.8", "monopoly-price")
def _(rng):
    a = rng.choice([80, 100, 120, 150])
    b = rng.choice([1, 2])
    c = rng.choice([10, 20, 30])
    q = (a - c) / (2 * b)
    p = a - b * q
    return Exercise(
        prompt=f"Monopolist: demand P = {a} − {b}Q, constant MC = {c}. Profit-maximising price?",
        answer=p,
        solution=f"MR = {a} − {2 * b}Q = {c} ⇒ Q = {q:.1f}; P = {a} − {b}·{q:.1f} = {p:.1f}.",
        hint="MR has twice the slope of linear demand. Set MR = MC, then read P from demand.",
        traps={c: "P = MC is the competitive outcome (or you read the price off the MR curve instead "
                  "of the demand curve).",
               q: "that is the quantity; read the price from the demand curve."},
    )


@gen("1.8", "lerner-markup")
def _(rng):
    e = rng.choice([1.25, 1.5, 2, 2.5, 3, 4, 5])
    mc = rng.choice([10, 20, 40, 50, 80])
    p = mc * e / (e - 1)
    return Exercise(
        prompt=f"Constant MC = €{mc}; the demand facing the firm has |ε| = {e}. Optimal price?",
        answer=p,
        solution=f"P = MC·|ε|/(|ε| − 1) = {mc}·{e}/{e - 1} = {p:.2f}  (Lerner index 1/|ε| = {1 / e:.2f}).",
        hint="(P − MC)/P = 1/|ε|.",
        traps={mc * (1 + 1 / e): "the markup 1/|ε| is on the PRICE, not on cost.",
               mc: "pricing at MC ignores market power."},
    )


@gen("1.8", "third-degree")
def _(rng):
    c = rng.choice([4, 10, 20])
    a1 = rng.choice([50, 60, 80, 100])
    q1 = (a1 - c) / 2
    p1 = a1 - q1
    return Exercise(
        prompt=(f"Third-degree price discrimination. MC = {c}. Segment A has demand P = {a1} − Q_A.\n"
                "Price in segment A?"),
        answer=p1,
        solution=f"MR_A = {a1} − 2Q_A = {c} ⇒ Q_A = {q1}; P_A = {a1} − {q1} = {p1}.",
        hint="In each segment set MR = MC separately.",
        traps={c: "that's the competitive price.", q1: "that's the quantity."},
    )


@gen("1.9", "logit-share")
def _(rng):
    beta = rng.choice([0.01, 0.02, 0.05])
    prices = sorted(rng.sample(range(80, 200, 10), 3))
    w = [math.exp(-beta * p) for p in prices]
    share = 100 * w[0] / sum(w)
    return Exercise(
        prompt=(f"Logit choice with identical quality and price sensitivity β = {beta}. Three sellers "
                f"at prices {prices}. Market share (%) of the cheapest seller?"),
        answer=share, decimals=1, rel_tol=0.02, percent_ok=True,
        solution=("weights e^(−βP): " + ", ".join(f"{x:.4f}" for x in w) +
                  f"; share = {w[0]:.4f}/{sum(w):.4f} = {share:.1f}%."),
        hint="Pr(j) = exp(−βP_j) / Σ exp(−βP_k).",
        traps={100.0: "in the logit model the cheapest seller does not take everyone.",
               100 / 3: "prices matter: the shares are not equal."},
    )


@gen("1.9", "hhi")
def _(rng):
    shares = rng.sample([5, 10, 15, 20, 25, 30, 35, 40], 4)
    total = sum(shares)
    shares = [round(100 * s / total) for s in shares]
    shares[0] += 100 - sum(shares)
    hhi = sum(s * s for s in shares)
    return Exercise(
        prompt=f"Market shares (%): {shares}. Herfindahl-Hirschman Index?",
        answer=hhi, decimals=0, rel_tol=0, abs_tol=0.5,
        solution=" + ".join(f"{s}²" for s in shares) + f" = {hhi}.",
        hint="Square each percentage share and add.",
        traps={sum(s * s for s in shares) / 10000: "use shares in %, not fractions."},
    )


# =============================================================================
# M2 Game theory & auctions
# =============================================================================

@gen("2.1", "best-response")
def _(rng):
    k = rng.choice([6, 8, 10, 12, 20])
    e = k
    return Exercise(
        prompt=(f"Two players choose effort e₁, e₂ ≥ 0. Player 1's payoff: π₁ = e₁({k} + e₂ − e₁), "
                "symmetric for player 2. Symmetric Nash equilibrium effort?"),
        answer=e,
        solution=f"BR: ∂π₁/∂e₁ = {k} + e₂ − 2e₁ = 0 ⇒ e₁ = ({k} + e₂)/2. Symmetric: e = ({k} + e)/2 ⇒ e = {k}.",
        hint="Find the best-response function, then impose e₁ = e₂.",
        traps={k / 2: "that is the best response to e₂ = 0, not the equilibrium."},
    )


@gen("2.2", "mixed-strategy")
def _(rng):
    a, b, c, d = (r2(rng.uniform(0.4, 0.95)) for _ in range(4))
    # striker scores: (L,L)=a (L,R)=b (R,L)=c (R,R)=d ; need b>a, c>d for interior mix
    a, b = min(a, b), max(a, b)
    d, c = min(c, d), max(c, d)
    if math.isclose(b - a + c - d, 0):
        c += 0.05
    q = (b - d) / ((b - a) + (c - d))
    return Exercise(
        prompt=("Penalty kick. Probability the striker scores:\n"
                f"  shoot L vs keeper L: {a}   shoot L vs keeper R: {b}\n"
                f"  shoot R vs keeper L: {c}   shoot R vs keeper R: {d}\n"
                "With what probability does the keeper dive LEFT in the mixed equilibrium?"),
        answer=q, decimals=3, percent_ok=True,
        solution=(f"Keeper makes striker indifferent: {a}q + {b}(1−q) = {c}q + {d}(1−q) ⇒ "
                  f"q = ({b}−{d})/(({b}−{a}) + ({c}−{d})) = {q:.3f}."),
        hint="The keeper's mix must make the STRIKER indifferent between L and R.",
        traps={1 - q: "that is the probability of diving RIGHT."},
    )


@gen("2.3", "cournot")
def _(rng):
    a = rng.choice([100, 120, 150, 200])
    c = rng.choice([10, 20, 30])
    n = rng.choice([2, 2, 3, 4])
    q = (a - c) / (n + 1)
    p = (a + n * c) / (n + 1)
    return Exercise(
        prompt=f"Cournot with {n} identical firms, inverse demand P = {a} − Q, MC = {c}. Market price?",
        answer=p,
        solution=f"Each q = (a − c)/(n + 1) = {q:.2f}; Q = {n * q:.2f}; P = {a} − {n * q:.2f} = {p:.2f}.",
        hint="Each firm: q = (a − c − Q_others)/2; in symmetric equilibrium q = (a − c)/(n + 1).",
        traps={(a + c) / 2: "that is the monopoly price.", float(c): "that is Bertrand / competition.",
               q: "that is one firm's quantity."},
    )


@gen("2.3", "stackelberg")
def _(rng):
    a = rng.choice([100, 120, 160])
    c = rng.choice([10, 20, 40])
    q1 = (a - c) / 2
    return Exercise(
        prompt=f"Stackelberg duopoly, P = {a} − Q, MC = {c}. Leader's quantity?",
        answer=q1,
        solution=(f"Follower: q₂ = (a − c − q₁)/2. Leader maximises (a − q₁ − q₂ − c)q₁ = "
                  f"((a − c − q₁)/2)·q₁ ⇒ q₁ = (a − c)/2 = {q1}; q₂ = {q1 / 2}."),
        hint="Substitute the follower's best response into the leader's profit.",
        traps={(a - c) / 3: "that's the Cournot quantity — the leader commits to more.",
               (a - c) / 4: "that's the follower's quantity."},
    )


@gen("2.4", "cooperation-threshold")
def _(rng):
    p_ = rng.choice([0, 1, 2])
    r = p_ + rng.choice([1, 2, 3])
    t = r + rng.choice([1, 2, 3])
    delta = (t - r) / (t - p_)
    return Exercise(
        prompt=(f"Infinitely repeated prisoner's dilemma: mutual cooperation pays R = {r}, temptation "
                f"T = {t}, mutual defection P = {p_}. Minimum discount factor δ for grim-trigger "
                "cooperation?"),
        answer=delta, decimals=3,
        solution=f"δ ≥ (T − R)/(T − P) = ({t} − {r})/({t} − {p_}) = {delta:.3f}.",
        hint="Compare R/(1−δ) with T + δP/(1−δ).",
        traps={(r - p_) / (t - p_): "numerator is the one-shot GAIN from defecting, T − R."},
    )


@gen("2.5", "first-price-shading")
def _(rng):
    n = rng.choice([2, 3, 4, 5, 10])
    vmax = rng.choice([100, 200, 1000])
    v = rng.randint(int(vmax * 0.3), vmax)
    b = (n - 1) / n * v
    return Exercise(
        prompt=(f"First-price sealed-bid auction, {n} risk-neutral bidders, independent private "
                f"values uniform on [0, {vmax}]. Equilibrium bid of a bidder with value {v}?"),
        answer=b,
        solution=f"b(v) = (n − 1)/n · v = {n - 1}/{n} · {v} = {b:.2f}.",
        hint="Symmetric equilibrium with uniform values: b = (n − 1)/n · v.",
        traps={float(v): "bidding your value guarantees zero surplus in a pay-your-bid auction "
                         "(that's the second-price strategy).",
               v / n: "you shaded far too much: the formula is (n − 1)/n · v."},
    )


@gen("2.5", "expected-revenue")
def _(rng):
    n = rng.choice([2, 3, 4, 5, 9])
    vmax = rng.choice([1, 100, 1000])
    rev = (n - 1) / (n + 1) * vmax
    return Exercise(
        prompt=(f"{n} bidders, values uniform on [0, {vmax}], second-price auction, no reserve. "
                "Seller's expected revenue?"),
        answer=rev, decimals=3,
        solution=f"Expected 2nd-highest of n uniforms = (n − 1)/(n + 1)·max = {n - 1}/{n + 1}·{vmax} = {rev:.3f}.",
        hint="Revenue = expected second-highest value: (n−1)/(n+1) × upper bound.",
        traps={n / (n + 1) * vmax: "that's the expected HIGHEST value."},
    )


@gen("2.6", "multi-unit-clearing")
def _(rng):
    supply = rng.randint(8, 20)
    reserve = rng.choice([4, 5, 6])
    bids = sorted([(rng.choice("ABCDE"), rng.randint(1, 6), rng.randint(3, 15)) for _ in range(5)],
                  key=lambda b: -b[2])
    left = supply
    clearing = None
    for _, q, p in bids:
        if p < reserve or left <= 0:
            continue
        take = min(q, left)
        left -= take
        clearing = p
    if clearing is None:
        clearing = 0
    desc = "; ".join(f"{who}: {q} units @ {p}" for who, q, p in bids)
    return Exercise(
        prompt=(f"Pay-your-bid multi-unit auction: {supply} units, reserve {reserve}. Bids: {desc}.\n"
                "Lowest accepted bid price (clearing price)? (0 if nothing sells)"),
        answer=clearing, decimals=0,
        solution=f"Sort bids high → low, skip those below {reserve}, fill until supply runs out; "
                 f"the last bid filled is at {clearing}.",
        hint="Fill bids from the highest price down; ignore bids under the reserve.",
        traps={float(reserve): "the reserve is only a floor; the clearing price is the last bid filled."},
    )


@gen("2.6", "pay-as-bid-payment")
def _(rng):
    q1, p1 = rng.randint(2, 6), rng.randint(15, 25)
    q2, p2 = rng.randint(2, 6), rng.randint(8, 14)
    won = rng.randint(q1 + 1, q1 + q2)
    pay = q1 * p1 + (won - q1) * p2
    return Exercise(
        prompt=(f"You bid {q1} units @ {p1} and {q2} units @ {p2} in a pay-your-bid auction and win "
                f"{won} units (the clearing price was {p2}). What do you pay in total?"),
        answer=pay, decimals=0,
        solution=f"Pay-your-bid: {q1}·{p1} + {won - q1}·{p2} = {pay}. (Uniform price would be {won * p2}.)",
        hint="Each unit costs the price you bid for it; your higher bids fill first.",
        traps={won * p2: "that's the uniform-price payment.", won * p1: "only the first block was bid at the high price."},
    )


@gen("2.7", "expected-value")
def _(rng):
    probs = rng.choice([(0.3, 0.5, 0.2), (0.25, 0.5, 0.25), (0.1, 0.6, 0.3), (0.4, 0.4, 0.2)])
    vals = (rng.randint(200, 600), rng.randint(0, 200), -rng.randint(100, 400))
    ev = sum(p * v for p, v in zip(probs, vals))
    return Exercise(
        prompt=("Outcomes (€k) and probabilities: " +
                ", ".join(f"{v} with p={p}" for p, v in zip(probs, vals)) + ". Expected value?"),
        answer=ev, decimals=1,
        solution=" + ".join(f"{p}·{v}" for p, v in zip(probs, vals)) + f" = {ev:.1f}.",
        hint="Σ probability × outcome.",
        traps={sum(vals) / 3: "outcomes are not equally likely; weight by probabilities."},
    )


@gen("2.7", "newsvendor")
def _(rng):
    cost = rng.choice([1, 2, 4, 5])
    price = cost + rng.choice([1, 2, 3, 5])
    salvage = rng.choice([0, 0, cost / 2])
    lo, hi = rng.choice([(50, 150), (0, 100), (100, 300)])
    cu, co = price - cost, cost - salvage
    ratio = cu / (cu + co)
    q = lo + ratio * (hi - lo)
    return Exercise(
        prompt=(f"Unit cost €{cost}, price €{price}, leftovers salvage €{salvage:g}. Demand uniform "
                f"on [{lo}, {hi}]. Optimal order quantity (newsvendor)?"),
        answer=q, decimals=1, rel_tol=0.01,
        solution=(f"c_u = {price} − {cost} = {cu}; c_o = {cost} − {salvage:g} = {co:g}; critical ratio "
                  f"{ratio:.3f}; Q* = {lo} + {ratio:.3f}·{hi - lo} = {q:.1f}."),
        hint="Q* is the demand quantile at c_u/(c_u + c_o).",
        traps={(lo + hi) / 2: "ordering the mean ignores the asymmetry between under- and over-stocking.",
               lo + co / (cu + co) * (hi - lo): "you swapped c_u and c_o."},
    )


@gen("2.7", "ema")
def _(rng):
    alpha = rng.choice([0.1, 0.2, 0.3, 0.5])
    prev = rng.randint(5, 50)
    obs = rng.randint(0, 80)
    new = alpha * obs + (1 - alpha) * prev
    return Exercise(
        prompt=f"Exponential smoothing, α = {alpha}. Previous estimate {prev}, new observation {obs}. New estimate?",
        answer=new,
        solution=f"{alpha}·{obs} + {1 - alpha:.1f}·{prev} = {new:.2f}.",
        hint="S = α·x + (1 − α)·S_prev.",
        traps={(1 - alpha) * obs + alpha * prev: "α multiplies the NEW observation."},
    )


@gen("2.7", "evpi")
def _(rng):
    p = rng.choice([0.3, 0.4, 0.5, 0.6])
    safe = rng.randint(800, 1200)
    low, high = rng.randint(200, 600), rng.randint(1500, 2500)
    ev_now = max(safe, p * low + (1 - p) * high)
    ev_info = p * max(safe, low) + (1 - p) * max(safe, high)
    return Exercise(
        prompt=(f"Safe option pays {safe}. Risky option pays {low} if demand is low (p = {p}) or "
                f"{high} if high. Expected value of perfect information?"),
        answer=ev_info - ev_now, decimals=1,
        solution=(f"Best now: max({safe}, {p * low + (1 - p) * high:.1f}) = {ev_now:.1f}. With perfect info: "
                  f"{p}·max({safe},{low}) + {1 - p:.1f}·max({safe},{high}) = {ev_info:.1f}. EVPI = {ev_info - ev_now:.1f}."),
        hint="EVPI = E[best payoff knowing the state] − best expected payoff without knowing it.",
        traps={ev_info: "subtract the value of the best decision without information."},
    )


# =============================================================================
# M3 Accounting & finance
# =============================================================================

@gen("3.1", "accounting-equation")
def _(rng):
    cash = rng.randint(5, 20) * 1000
    inv = rng.randint(1, 8) * 1000
    pay = rng.randint(0, 5) * 1000
    loan = rng.randint(0, 6) * 1000
    eq = cash + inv - pay - loan
    return Exercise(
        prompt=f"Cash {cash:,}, inventory {inv:,}, payables {pay:,}, bank loan {loan:,}. Equity?",
        answer=eq, decimals=0,
        solution=f"Equity = assets − liabilities = ({cash:,} + {inv:,}) − ({pay:,} + {loan:,}) = {eq:,}.",
        hint="Assets = Liabilities + Equity.",
        traps={cash + inv + pay + loan: "liabilities are subtracted, not added.", cash - pay - loan: "inventory is an asset too."},
    )


@gen("3.2", "markup-margin")
def _(rng):
    cost = rng.choice([40, 50, 60, 80, 100])
    markup = rng.choice([0.25, 0.4, 0.5, 0.6, 1.0])
    price = cost * (1 + markup)
    margin = (price - cost) / price
    return Exercise(
        prompt=f"Unit cost €{cost}, price €{price:g}. Gross margin on price (as a decimal, e.g. 0.25)?",
        answer=margin, decimals=4, percent_ok=True,
        solution=f"Margin = (P − C)/P = {price - cost:g}/{price:g} = {margin:.4f}; markup on cost = {markup:.0%}.",
        hint="Margin divides by price; markup divides by cost.",
        traps={markup: "that's the markup on COST; margin is on PRICE."},
    )


@gen("3.2", "cogs-vs-cash")
def _(rng):
    bought = rng.randint(4, 10) * 1000
    share = rng.choice([0.4, 0.5, 0.6, 0.75])
    rev = rng.randint(6, 15) * 1000
    gp = rev - share * bought
    return Exercise(
        prompt=(f"A firm buys materials for €{bought:,}, turns them into goods and sells {share:.0%} of "
                f"those goods for €{rev:,}. Gross profit (accrual accounting)?"),
        answer=gp, decimals=0,
        solution=f"COGS = {share:.0%} × {bought:,} = {share * bought:,.0f}; GP = {rev:,} − {share * bought:,.0f} = {gp:,.0f}.",
        hint="COGS counts only the cost of the goods SOLD.",
        traps={rev - bought: "matching principle: unsold goods stay in inventory, not in COGS."},
    )


@gen("3.3", "cash-conversion")
def _(rng):
    dio, dso, dpo = rng.randint(20, 90), rng.randint(0, 60), rng.randint(10, 70)
    ccc = dio + dso - dpo
    return Exercise(
        prompt=f"DIO = {dio} days, DSO = {dso} days, DPO = {dpo} days. Cash conversion cycle (days)?",
        answer=ccc, decimals=0, rel_tol=0, abs_tol=0.5,
        solution=f"CCC = DIO + DSO − DPO = {dio} + {dso} − {dpo} = {ccc}.",
        hint="Payables finance you, so they are subtracted.",
        traps={dio + dso + dpo: "subtract DPO: paying suppliers later shortens the cycle."},
    )


@gen("3.3", "fifo-average")
def _(rng):
    q1, c1 = rng.randint(5, 15), rng.randint(10, 30)
    q2, c2 = rng.randint(5, 15), c1 + rng.randint(2, 10)
    sold = rng.randint(q1 + 1, q1 + q2)
    fifo = q1 * c1 + (sold - q1) * c2
    method = rng.choice(["FIFO", "weighted average"])
    avg = sold * (q1 * c1 + q2 * c2) / (q1 + q2)
    ans = fifo if method == "FIFO" else avg
    return Exercise(
        prompt=f"Bought {q1} units @ €{c1}, then {q2} @ €{c2}. Sold {sold}. COGS under {method}?",
        answer=ans, decimals=2,
        solution=(f"FIFO: {q1}·{c1} + {sold - q1}·{c2} = {fifo}. Weighted average: {sold} × "
                  f"{(q1 * c1 + q2 * c2) / (q1 + q2):.3f} = {avg:.2f}."),
        hint="FIFO: oldest costs first. Average: total cost / total units × units sold.",
        traps={(fifo if method != "FIFO" else avg): "that's the other method.",
               float(sold * c2 if sold <= q2 else q2 * c2 + (sold - q2) * c1): "that's LIFO."},
    )


@gen("3.4", "break-even")
def _(rng):
    p = rng.choice([20, 25, 40, 50, 80])
    vc = p - rng.choice([5, 10, 15, 20])
    fc = rng.choice([10000, 20000, 30000, 45000, 60000])
    q = fc / (p - vc)
    return Exercise(
        prompt=f"Price €{p}, variable cost €{vc}/unit, fixed costs €{fc:,}. Break-even quantity?",
        answer=q, decimals=1,
        solution=f"CM = {p} − {vc} = {p - vc}; Q_BE = {fc:,}/{p - vc} = {q:,.1f}.",
        hint="Break-even Q = fixed costs / contribution margin per unit.",
        traps={fc / p: "divide by the contribution margin (P − VC), not the price."},
    )


@gen("3.4", "scarce-resource")
def _(rng):
    hours = rng.choice([60, 100, 120])
    cm_x, h_x = rng.choice([30, 40, 50]), rng.choice([3, 4, 5])
    cm_y, h_y = rng.choice([18, 20, 24]), rng.choice([1, 2])
    cap_y = rng.choice([10, 20, 30, 1000])
    per_x, per_y = cm_x / h_x, cm_y / h_y
    if per_y >= per_x:
        y = min(cap_y, hours // h_y)
        x = (hours - y * h_y) // h_x
    else:
        x = hours // h_x
        y = min(cap_y, (hours - x * h_x) // h_y)
    best = x * cm_x + y * cm_y
    cap_text = f" Demand for Y is at most {cap_y} units." if cap_y < 1000 else ""
    return Exercise(
        prompt=(f"{hours} machine hours available. Product X: CM €{cm_x}, uses {h_x} h. "
                f"Product Y: CM €{cm_y}, uses {h_y} h.{cap_text} Maximum total contribution "
                "(whole units)?"),
        answer=best, decimals=0,
        solution=(f"CM per hour: X {per_x:.2f}, Y {per_y:.2f}. Fill the best per-hour product first "
                  f"(respecting demand), then the other: {x} X + {y} Y = €{best}."),
        hint="Rank by contribution per unit of the scarce resource (per hour), not per product.",
        traps={(hours // h_x) * cm_x: "X has the higher CM per unit, but compare CM per HOUR."}
        if per_y > per_x else {},
    )


@gen("3.5", "future-value")
def _(rng):
    pv = rng.choice([500, 1000, 2000, 5000])
    r = rng.choice([0.02, 0.03, 0.05, 0.07, 0.1])
    n = rng.choice([3, 5, 10, 20])
    fv = pv * (1 + r) ** n
    return Exercise(
        prompt=f"€{pv:,} invested at {r:.0%} per year, compounded annually, for {n} years. Future value?",
        answer=fv,
        solution=f"FV = {pv}·(1 + {r})^{n} = {fv:,.2f}.",
        hint="FV = PV(1 + r)^n.",
        traps={pv * (1 + r * n): "that's simple interest; compound interest earns interest on interest."},
    )


@gen("3.5", "present-value")
def _(rng):
    fv = rng.choice([1000, 5000, 10000])
    r = rng.choice([0.04, 0.05, 0.08, 0.1])
    n = rng.choice([2, 3, 5, 10])
    pv = fv / (1 + r) ** n
    return Exercise(
        prompt=f"Present value of €{fv:,} received in {n} years at a {r:.0%} discount rate?",
        answer=pv,
        solution=f"PV = {fv}/(1 + {r})^{n} = {pv:,.2f}.",
        hint="PV = FV/(1 + r)^n.",
        traps={fv * (1 + r) ** n: "you compounded instead of discounting.", fv / (1 + r * n): "discount with compounding."},
    )


@gen("3.5", "annuity")
def _(rng):
    c = rng.choice([100, 250, 500, 1000])
    r = rng.choice([0.03, 0.05, 0.06, 0.08])
    n = rng.choice([5, 10, 20])
    pv = c * (1 - (1 + r) ** -n) / r
    return Exercise(
        prompt=f"An annuity pays €{c} at the end of each year for {n} years. r = {r:.0%}. Present value?",
        answer=pv,
        solution=f"PV = C·[1 − (1 + r)^−n]/r = {c}·{(1 - (1 + r) ** -n) / r:.4f} = {pv:,.2f}.",
        hint="Annuity factor = [1 − (1 + r)^−n]/r.",
        traps={c * n: "undiscounted sum ignores the time value of money.", c / r: "that's a perpetuity."},
    )


@gen("3.5", "npv")
def _(rng):
    c0 = rng.choice([1000, 2000, 5000])
    cfs = [rng.randint(int(c0 * 0.2), int(c0 * 0.5)) for _ in range(rng.choice([3, 4]))]
    r = rng.choice([0.05, 0.08, 0.1, 0.12])
    npv = -c0 + sum(cf / (1 + r) ** (t + 1) for t, cf in enumerate(cfs))
    return Exercise(
        prompt=f"Invest €{c0:,} today; cash flows at the end of years 1..{len(cfs)}: {cfs}. r = {r:.0%}. NPV?",
        answer=npv, abs_tol=0.6, rel_tol=0.002,
        solution=("NPV = −" + f"{c0}" + "".join(f" + {cf}/{1 + r}^{t + 1}" for t, cf in enumerate(cfs))
                  + f" = {npv:,.2f}."),
        hint="Discount each cash flow by (1 + r)^t, add, subtract the investment.",
        traps={sum(cfs) - c0: "you forgot to discount."},
    )


@gen("3.5", "fisher")
def _(rng):
    i = rng.choice([0.02, 0.03, 0.04, 0.05, 0.08])
    pi = rng.choice([0.01, 0.02, 0.03, 0.06, 0.1])
    real = (1 + i) / (1 + pi) - 1
    return Exercise(
        prompt=f"Nominal rate {i:.0%}, inflation {pi:.0%}. Exact real interest rate (decimal)?",
        answer=real, decimals=4, abs_tol=0.0006, percent_ok=True,
        solution=f"(1 + i)/(1 + π) − 1 = {1 + i}/{1 + pi} − 1 = {real:.4f} (≈ i − π = {i - pi:.2f}).",
        hint="1 + i = (1 + r)(1 + π).",
        traps={pi - i: "sign: real = nominal − inflation."},
    )


@gen("3.6", "portfolio-risk")
def _(rng):
    sa, sb = rng.choice([0.1, 0.15, 0.2]), rng.choice([0.2, 0.25, 0.3])
    rho = rng.choice([-0.5, 0, 0.3, 0.5])
    w = rng.choice([0.3, 0.5, 0.6])
    var = w * w * sa * sa + (1 - w) ** 2 * sb * sb + 2 * w * (1 - w) * rho * sa * sb
    sd = math.sqrt(var)
    return Exercise(
        prompt=(f"Two assets: σ_A = {sa:.0%}, σ_B = {sb:.0%}, correlation {rho}. Weight {w:.0%} in A. "
                "Portfolio standard deviation (decimal)?"),
        answer=sd, decimals=4, abs_tol=0.0006, percent_ok=True,
        solution=f"σ² = w²σA² + (1−w)²σB² + 2w(1−w)ρσAσB = {var:.5f} → σ = {sd:.4f}.",
        hint="Don't average the σ's — use the variance formula with the correlation term.",
        traps={w * sa + (1 - w) * sb: "the weighted average of σ's ignores diversification."},
    )


@gen("3.6", "capm")
def _(rng):
    rf = rng.choice([0.01, 0.02, 0.03])
    mp = rng.choice([0.04, 0.05, 0.06])
    beta = rng.choice([0.5, 0.8, 1.2, 1.5, 2.0])
    er = rf + beta * mp
    return Exercise(
        prompt=f"Risk-free {rf:.0%}, market risk premium {mp:.0%}, β = {beta}. CAPM expected return (decimal)?",
        answer=er, decimals=4, abs_tol=0.0006, percent_ok=True,
        solution=f"E[R] = {rf} + {beta}·{mp} = {er:.4f}.",
        hint="E[R] = R_f + β·(market premium).",
        traps={beta * mp: "add the risk-free rate.", rf + beta * (mp - rf): "the PREMIUM is already E[R_m] − R_f."},
    )


@gen("3.7", "bond-price")
def _(rng):
    face = 1000
    coupon = rng.choice([0.02, 0.04, 0.05, 0.06])
    y = rng.choice([0.03, 0.04, 0.05, 0.06, 0.07])
    n = rng.choice([2, 3, 5])
    price = sum(face * coupon / (1 + y) ** t for t in range(1, n + 1)) + face / (1 + y) ** n
    return Exercise(
        prompt=f"Bond: face €1,000, annual coupon {coupon:.0%}, {n} years to maturity, yield {y:.0%}. Price?",
        answer=price, abs_tol=0.6, rel_tol=0.001,
        solution=f"P = Σ {face * coupon:g}/(1+{y})^t + 1000/(1+{y})^{n} = {price:,.2f}.",
        hint="Discount every coupon and the face value at the yield.",
        traps={float(face): "price equals face value only when coupon rate = yield."},
    )


@gen("3.7", "gordon")
def _(rng):
    d1 = rng.choice([1, 2, 3, 5])
    r = rng.choice([0.07, 0.08, 0.1, 0.12])
    g = rng.choice([0.01, 0.02, 0.03, 0.04])
    p = d1 / (r - g)
    return Exercise(
        prompt=f"Next dividend €{d1}, growing {g:.0%} forever, required return {r:.0%}. Share price?",
        answer=p,
        solution=f"P₀ = D₁/(r − g) = {d1}/({r} − {g}) = {p:.2f}.",
        hint="Gordon growth model.",
        traps={d1 / r: "that ignores growth.", d1 / (r + g): "subtract g from r."},
    )


# =============================================================================
# M4 Macroeconomics
# =============================================================================

@gen("4.1", "gdp-expenditure")
def _(rng):
    c, i, g = rng.randint(800, 1300), rng.randint(200, 450), rng.randint(300, 500)
    x, m = rng.randint(300, 700), rng.randint(300, 700)
    y = c + i + g + x - m
    return Exercise(
        prompt=f"C = {c}, I = {i}, G = {g}, exports {x}, imports {m}. GDP?",
        answer=y, decimals=0,
        solution=f"Y = C + I + G + (X − M) = {c} + {i} + {g} + ({x} − {m}) = {y}.",
        hint="Y = C + I + G + NX.",
        traps={c + i + g + x + m: "imports are subtracted.", c + i + g + x: "subtract imports."},
    )


@gen("4.1", "real-growth")
def _(rng):
    q1, p1 = rng.randint(8, 15), rng.randint(5, 10)
    q2, p2 = q1 + rng.randint(0, 4), p1 + rng.randint(0, 3)
    b1, pb1 = rng.randint(3, 8), rng.randint(15, 25)
    b2, pb2 = b1 + rng.randint(0, 3), pb1 + rng.randint(-2, 3)
    real1 = q1 * p1 + b1 * pb1
    real2 = q2 * p1 + b2 * pb1
    g = 100 * (real2 / real1 - 1)
    nom2 = q2 * p2 + b2 * pb2
    return Exercise(
        prompt=(f"Year 1: {q1} pizzas @ {p1}, {b1} books @ {pb1}. Year 2: {q2} pizzas @ {p2}, "
                f"{b2} books @ {pb2}. Real GDP growth in % (year-1 prices)?"),
        answer=g, decimals=2, percent_ok=True, abs_tol=0.05,
        solution=(f"Real Y1 = {real1}; real Y2 (year-1 prices) = {q2}·{p1} + {b2}·{pb1} = {real2}; "
                  f"growth = {g:.2f}%. (Nominal Y2 = {nom2}.)"),
        hint="Value year-2 quantities at year-1 prices.",
        traps={100 * (nom2 / real1 - 1): "that's NOMINAL growth — it includes price changes."},
    )


@gen("4.2", "inflation-real-wage")
def _(rng):
    w1 = rng.choice([25000, 30000, 40000])
    gw = rng.choice([0.02, 0.03, 0.04, 0.05])
    pi = rng.choice([0.02, 0.04, 0.06, 0.08])
    real = 100 * ((1 + gw) / (1 + pi) - 1)
    return Exercise(
        prompt=f"Your salary rises {gw:.0%} from €{w1:,}; inflation is {pi:.0%}. Real wage change in %?",
        answer=real, decimals=2, percent_ok=True, abs_tol=0.05,
        solution=f"(1.{int(gw * 100):02d}/1.{int(pi * 100):02d} − 1)·100 = {real:.2f}%.",
        hint="Deflate the new salary by (1 + inflation).",
        traps={100 * (gw + pi): "inflation reduces real wages."},
    )


@gen("4.2", "quantity-theory")
def _(rng):
    m = rng.choice([3, 5, 7, 10])
    y = rng.choice([1, 2, 3])
    v = rng.choice([0, 0, 1, -1])
    pi = m + v - y
    return Exercise(
        prompt=(f"Money supply grows {m}%, velocity changes {v:+d}%, real GDP grows {y}%. "
                "Approximate inflation (%)?"),
        answer=pi, decimals=1, abs_tol=0.05,
        solution=f"%ΔM + %ΔV ≈ %ΔP + %ΔY ⇒ π ≈ {m} + {v} − {y} = {pi}%.",
        hint="Quantity theory in growth rates.",
        traps={m + v + y: "real growth absorbs part of the money growth: subtract it."},
    )


@gen("4.3", "unemployment-rate")
def _(rng):
    emp = rng.randint(18, 28)
    unemp = rng.randint(1, 4)
    pop = emp + unemp + rng.randint(10, 25)
    rate = 100 * unemp / (emp + unemp)
    return Exercise(
        prompt=f"Working-age population {pop} m, employed {emp} m, unemployed {unemp} m. Unemployment rate (%)?",
        answer=rate, decimals=2, percent_ok=True, abs_tol=0.05,
        solution=f"Labour force = {emp + unemp} m; rate = {unemp}/{emp + unemp} = {rate:.2f}%.",
        hint="Divide by the LABOUR FORCE, not the population.",
        traps={100 * unemp / pop: "divide by the labour force, not the working-age population.",
               100 * unemp / emp: "the labour force includes the unemployed."},
    )


@gen("4.4", "multiplier")
def _(rng):
    mpc = rng.choice([0.6, 0.75, 0.8, 0.9])
    t = rng.choice([0, 0, 0.2, 0.25])
    m = rng.choice([0, 0, 0.1])
    k = 1 / (1 - mpc * (1 - t) + m)
    dg = rng.choice([5, 10, 20])
    return Exercise(
        prompt=(f"MPC = {mpc}, tax rate {t}, marginal propensity to import {m}. Government spending "
                f"rises by €{dg} bn. Change in GDP (simple Keynesian model)?"),
        answer=dg * k,
        solution=f"k = 1/(1 − MPC(1 − t) + m) = 1/(1 − {mpc}·{1 - t} + {m}) = {k:.3f}; ΔY = {dg}·{k:.3f} = {dg * k:.2f}.",
        hint="Multiplier 1/(1 − MPC(1 − t) + m).",
        traps={dg / (1 - mpc): "you ignored taxes/imports leakages." if (t or m) else "check the formula.",
               float(dg): "spending has knock-on effects through income."},
    )


@gen("4.5", "taylor-rule")
def _(rng):
    rstar = rng.choice([0.5, 1, 2])
    pi = rng.choice([1, 2, 3, 4, 6])
    gap = rng.choice([-2, -1, 0, 1, 2])
    i = rstar + pi + 0.5 * (pi - 2) + 0.5 * gap
    return Exercise(
        prompt=f"Taylor rule with r* = {rstar}%, inflation {pi}%, target 2%, output gap {gap}%. Policy rate (%)?",
        answer=i, decimals=2, abs_tol=0.01,
        solution=f"i = {rstar} + {pi} + 0.5·({pi} − 2) + 0.5·({gap}) = {i:.2f}%.",
        hint="i = r* + π + 0.5(π − π*) + 0.5·gap.",
        traps={rstar + 0.5 * (pi - 2) + 0.5 * gap: "don't forget the current inflation term π."},
    )


@gen("4.6", "exchange-rate")
def _(rng):
    eur = rng.choice([20, 40, 50, 80, 120])
    e1 = rng.choice([1.05, 1.1, 1.15])
    e2 = e1 + rng.choice([-0.1, 0.1, 0.15])
    change = 100 * (e2 / e1 - 1)
    return Exercise(
        prompt=(f"An Italian product costs €{eur}. EUR/USD moves from {e1} to {e2:.2f} (dollars per euro). "
                "By what % does its dollar price change?"),
        answer=change, decimals=2, percent_ok=True, abs_tol=0.05,
        solution=f"${eur * e1:.2f} → ${eur * e2:.2f}: {change:+.2f}%.",
        hint="Dollar price = euro price × dollars per euro.",
        traps={-change: "a stronger euro makes European goods DEARER in dollars."},
    )
