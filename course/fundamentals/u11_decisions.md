# F11 · Business decisions | Reasoning

## F11.1 Relevant costs and revenues
A cost or revenue is **relevant** to a decision only if it is (1) **in the
future** and (2) **different** between the alternatives.

Irrelevant: sunk costs, costs that are the same whatever you choose, and
allocated overheads that won't actually change.

> **Example.** Accept a one-off order of 100 units at €30? Variable cost €18,
> spare capacity, fixed costs unchanged. Relevant: revenue 3,000 − variable
> cost 1,800 = **+€1,200**. The "full cost" of €35 (including a share of rent)
> is irrelevant because the rent is paid anyway.

@num One-off order: 200 units at €25; variable cost €17; spare capacity; fixed costs unchanged. Gain from accepting (€)?
= 1600
! (25 − 17) × 200.
@mcq Which cost is relevant when deciding whether to accept a special order?
+ extra materials needed for the order
- last year's advertising spend
- the CEO's fixed salary
- the original price paid for a machine already owned | sunk.
! Future and differential.
@mcq "Full cost per unit is €35, so a €30 order loses money." The flaw is…
+ including fixed costs that don't change with the order
- ignoring taxes
- using the wrong price
- nothing
! Only incremental costs matter.

## F11.2 Opportunity cost of resources you already own
Materials, stock or capacity you already own are valued at their **best
alternative use**, not at what you paid.

- No alternative use, no resale value → relevant cost **0**.
- Can be resold → resale value.
- Needed for another profitable product → that product's lost contribution.

> **Example.** 50 kg of material bought at €10/kg. If unused it can be sold for
> €4/kg; it could also replace material you'd otherwise buy for €12/kg in
> another job. Best alternative: €12/kg → relevant cost **€600**.

@num 100 units of a component bought at €8; resale value €3; no other use. Relevant cost of using them (€)?
= 300
x 800 | the purchase price is sunk.
! Best alternative = resale 100 × 3.
@num 100 units of a component bought at €8; resale value €3; it could also replace a part you'd otherwise buy at €6 for another product. Relevant cost of using them (€)?
= 600
! Best alternative now 6 per unit.
@mcq Stock with no other use and no resale value has an opportunity cost of…
+ zero
- its purchase price
- its expected selling price
- its replacement cost | only if you'd otherwise need to buy it.
! Nothing is given up by using it.

## F11.3 Make or buy
Compare the **avoidable** costs of making with the price of buying, plus any
opportunity cost of the capacity freed.

> **Example.** Making a part: materials 6, labour 4, variable overhead 2, fixed
> overhead allocated 5 (unavoidable). Buying costs 13. Avoidable making cost =
> 12 < 13 → make. If the freed capacity could earn €3 per part elsewhere, buying
> becomes cheaper: 13 vs 12 + 3 = 15.

@num Make: variable cost €9 per unit; allocated fixed overhead €4 (unavoidable). Buy: €11. Saving per unit from making (€)?
= 2
! 11 − 9.
@num Make: variable cost €9 per unit; allocated fixed overhead €4 (unavoidable). Buy: €11. Freed capacity could earn €3 per unit elsewhere. Net advantage of BUYING per unit (€)?
= 1
! Make costs 9 + 3 = 12 vs buy 11.
@mcq In make-or-buy, allocated fixed costs that continue either way are…
+ irrelevant
- relevant
- always 50 % relevant
- the main factor
! They don't differ between options.

## F11.4 Product mix with one constraint
When a resource is scarce, maximise **contribution per unit of the scarce
resource**. Steps: (1) contribution per unit; (2) divide by resource use; (3)
rank; (4) fill demand in rank order until the resource runs out.

> **Example.** 300 kg of a scarce material. A: CM €60, 6 kg (€10/kg), max
> demand 30. B: CM €24, 2 kg (€12/kg), max demand 90. Rank B first: 90 B uses
> 180 kg (€2,160); remaining 120 kg → 20 A (€1,200). Total **€3,360**.

@num 120 hours. X: CM €50, 5 h, demand 20. Y: CM €18, 1.5 h, demand 40. Maximum contribution (€)?
= 1320
! Y €12/h first: 40 Y uses 60 h (€720); 60 h → 12 X (€600).
@num 120 hours. X: CM €50, 5 h, demand 20. Y: CM €18, 1.5 h, demand 100. Maximum contribution (€)?
= 1440
! 120 h / 1.5 = 80 Y × 18.
@mcq A has the higher contribution per unit but uses much more of the scarce input. Rank by…
+ contribution per unit of the scarce input
- contribution per unit of product
- selling price
- sales volume
! The constraint binds.

## F11.5 Several constraints
With two or more scarce resources, the best mix may use several products;
simple ranking can fail because the bottleneck changes. The general tool is
**linear programming** (maximise Σ CMᵢxᵢ subject to Σ aᵢⱼxᵢ ≤ capacityⱼ); for
two products, check the **corner points** of the feasible region.

> **Example.** A uses 1 kg material and 2 h; B uses 2 kg and 1 h. 80 kg and
> 100 h available. CM: A 30, B 40. Corners: (0,0)=0; A only: min(80, 50)=50 →
> 1,500; B only: min(40,100)=40 → 1,600; both binding: x + 2y = 80, 2x + y =
> 100 ⇒ x = 40, y = 20 → 1,200 + 800 = **2,000** (best).

@num A uses 1 kg of material and 2 h; B uses 2 kg and 1 h. 80 kg and 100 h available; CM A €30, B €40. The best mix is 40 A and 20 B. Material used at the optimum (kg)?
= 80
! 40 + 2×20.
@num A uses 1 kg of material and 2 h; B uses 2 kg and 1 h. 80 kg and 100 h available. CM A €30, B €10. Best total contribution (€)?
= 1500
! A only (50 units, hours bind) = 1,500 beats the mixed corner 1,400.
@mcq With two binding constraints, the optimum of a linear programme lies…
+ at a corner of the feasible region
- in the middle
- always where only one product is made
- outside the region
! Linear objective → corner solution.

## F11.6 Decision trees
A **decision tree** maps choices (squares) and chance events (circles) with
probabilities and payoffs. Solve **backwards**: at chance nodes compute
expected values; at decision nodes pick the best branch.

> **Example.** Launch: 60 % success (+€200k), 40 % failure (−€100k) → EV
> €80k. Don't launch: €0. Test market first for €10k: ... compare EVs.

Trees make assumptions explicit and show where better information is worth
paying for.

@num Option A: 50 % → €100k, 50 % → €20k. Option B: certain €55k. Higher EV (€k)?
= 60
! A: 50 + 10 = 60 > 55.
@num Launch: 30 % → +€500k, 70 % → −€100k. EV of launching (€k)?
= 80
! 150 − 70.
@mcq Decision trees are solved…
+ backwards: expectations at chance nodes, best choice at decision nodes
- forwards from the first decision
- by averaging all payoffs
- by picking the best outcome
! Roll back.

## F11.7 Sensitivity analysis
Forecasts are uncertain. **Sensitivity analysis** asks how the result changes
when one input changes, and which inputs matter most.

- **What-if**: profit if price −10 %? if volume −20 %?
- **Break-even of an input**: at what volume/price does profit become zero?
- **Scenarios**: pessimistic / base / optimistic.

> **Example.** Profit = (P − v)Q − F = (50 − 30)·1,000 − 15,000 = 5,000. If P
> falls 10 % to 45: (15)·1,000 − 15,000 = 0. A 10 % price fall wipes out profit
> — price is a critical input.

@num Profit = (P − 20)·Q − 10,000, P = 30, Q = 1,500. Profit at base case (€)?
= 5000
! 15,000 − 10,000.
@num Profit = (P − 20)·Q − 10,000 with Q = 1,500. Price at which profit becomes zero?
= 26.67 ~0.01
! (P − 20)·1,500 = 10,000 ⇒ P = 26.67.
@num Profit = (P − 20)·Q − 10,000, P = 30, base Q = 1,500. Profit if Q falls 20 % (€)?
= 2000
! 10 × 1,200 − 10,000.

## F11.8 Forecasting basics
Simple forecasts:

- **Naive**: next = last value.
- **Moving average**: mean of the last k values (smooths noise, lags trends).
- **Exponential smoothing**: Fₜ₊₁ = α·xₜ + (1 − α)·Fₜ.
- **Seasonal naive**: next December = last December.

Measure accuracy: **MAE** (mean absolute error), **MAPE** (mean absolute %
error). Check forecasts against what actually happened, and update.

> **Example.** Sales 40, 46, 52. 3-period moving average forecast = 46; naive =
> 52; with a clear upward trend both under-predict.

@num Sales: 30, 34, 38, 42. 3-period moving average forecast for the next period?
= 38
! (34 + 38 + 42)/3.
@num Forecast 50, actual 40; α = 0.2. Exponential smoothing forecast for next period?
= 48
! 0.2×40 + 0.8×50.
@num Actuals 100, 80; forecasts 90, 100. MAE?
= 15
! (10 + 20)/2.

## F11.9 Inventory decisions
Holding stock balances two risks: **running out** (lost sales) and **holding
too much** (cash tied up, obsolescence, unsold leftovers).

- **Reorder point** = demand during the lead time + safety stock.
- **Newsvendor rule** (one selling season): stock up to the demand level whose
  probability of not being exceeded equals c_u/(c_u + c_o), where c_u = margin
  lost per unit short, c_o = loss per unit left over.

> **Example.** Margin €6 per unit sold, leftovers lose their €4 cost → ratio
> 6/10 = 0.6: stock the 60th percentile of demand.

@num Demand 20 units per day, lead time 5 days, safety stock 30. Reorder point?
= 130
! 100 + 30.
@num Margin per unit sold €3, loss per unsold unit €1. Critical ratio?
= 0.75 %
! 3/4.
@mcq If leftover units at the end are worth nothing, compared with when they can be sold later at full price, you should stock…
+ less
- more
- the same
- zero always
! Higher overstock cost lowers the critical ratio.

## F11.10 KPIs and dashboards
**Key performance indicators** turn goals into numbers: revenue growth, gross
margin, conversion rate, average order value, inventory days, cash balance,
market share. A good KPI is tied to a goal, measurable, timely, and hard to
game.

Watch **ratios and trends**, not just levels, and pair KPIs that pull in
opposite directions (volume with margin, growth with cash).

> **Example.** Conversion = orders/visitors = 300/12,000 = 2.5 %. Average order
> value = revenue/orders = 18,000/300 = €60.

@num 450 orders from 15,000 visitors. Conversion rate (%)?
= 3 %
! 450/15,000.
@num Revenue €27,000 from 450 orders. Average order value (€)?
= 60
! 27,000/450.
@mcq Rewarding staff only on sales volume risks…
+ deep discounts that hurt margin
- higher margins
- lower volume
- nothing
! Pair volume KPIs with margin KPIs.
