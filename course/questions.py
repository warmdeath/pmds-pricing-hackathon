"""Concept questions. In the source the correct option is always the first one;
the trainer shuffles options before showing them. `traps` maps a wrong option's
index to why it is tempting but wrong."""

QUESTIONS: list[dict] = []
_count: dict[str, int] = {}


def Q(lesson, question, options, why, traps=None):
    _count[lesson] = _count.get(lesson, 0) + 1
    QUESTIONS.append({"id": f"{lesson}-{_count[lesson]}", "lesson": lesson, "q": question,
                      "options": options, "answer": 0, "why": why, "traps": traps or {}})


# ----------------------------------------------------------------------------- 1.1
Q("1.1", "You paid €50 (non-refundable) for a concert ticket. On the night, a friend offers you a "
  "job worth €80 for the same evening. The concert is worth €60 to you. What should you do?",
  ["Take the job: €80 > €60; the €50 is sunk", "Go to the concert: you already paid €50",
   "Go to the concert: €60 + €50 > €80", "Indifferent"],
  "The ticket price is sunk — it is lost whatever you choose. Compare only the alternatives still "
  "open: €80 vs €60.", {1: "sunk cost fallacy.", 2: "the €50 is not a benefit of going; it's gone either way."})
Q("1.1", "The opportunity cost of a choice is…",
  ["the value of the best alternative forgone", "the money you spend on it",
   "the sum of all alternatives forgone", "the average cost of the activity"],
  "Only the single best alternative counts, and it includes non-monetary value.",
  {2: "you can only do one alternative instead, so only the best one is forgone."})
Q("1.1", "A firm's average cost is €10 per unit. The next unit would cost €14 to make and sell for "
  "€12. Should it make it?",
  ["No: the marginal cost (14) exceeds the marginal benefit (12)", "Yes: 12 > average cost of 10",
   "Yes: it lowers average cost", "Only if fixed costs are covered"],
  "Decisions at the margin compare the extra benefit with the extra cost of THIS unit.",
  {1: "averages include past units; the decision is about the next one."})
Q("1.1", "Anna makes 6 pizzas or 3 cakes per hour; Bruno 2 pizzas or 2 cakes. Who has the "
  "comparative advantage in cakes?",
  ["Bruno: a cake costs him 1 pizza vs 2 for Anna", "Anna: she makes more cakes per hour",
   "Neither: Anna is better at both", "Both equally"],
  "Comparative advantage = lower opportunity cost, not higher productivity.",
  {1: "that's absolute advantage.", 2: "absolute advantage in both doesn't remove comparative advantage."})
Q("1.1", "Why is the production possibilities frontier usually bowed outward?",
  ["Resources are specialised, so opportunity costs rise as you produce more of one good",
   "Because of inflation", "Because demand is downward sloping", "Because of economies of scale"],
  "Moving resources that are less and less suited to a good raises its opportunity cost.")

# ----------------------------------------------------------------------------- 1.2
Q("1.2", "The price of coffee rises. What happens in the market for tea (a substitute)?",
  ["Demand for tea shifts right; tea price and quantity rise", "Tea supply shifts left",
   "Movement along the tea demand curve", "Demand for tea shifts left"],
  "A substitute's price is a demand shifter.", {2: "only tea's OWN price causes a movement along its curve."})
Q("1.2", "Cheaper chips (an input) for phone makers. Effect on the phone market?",
  ["Supply shifts right: price falls, quantity rises", "Demand shifts right",
   "Supply shifts left: price rises", "No effect: chips are not phones"],
  "Input costs shift supply.")
Q("1.2", "At a price above equilibrium there is…",
  ["a surplus (excess supply) that pushes the price down", "a shortage that pushes the price up",
   "equilibrium", "a shift of the demand curve"],
  "Above p*, Qs > Qd: unsold stock accumulates and sellers cut prices.")
Q("1.2", "Demand rises and supply falls at the same time. What is certain?",
  ["The price rises; the quantity change is ambiguous", "Quantity rises; price ambiguous",
   "Both rise", "Both fall"],
  "Both shifts push the price up; they push quantity in opposite directions.")
Q("1.2", "The height of the demand curve at quantity q represents…",
  ["the willingness to pay of the q-th buyer", "the cost of the q-th unit",
   "the total revenue at q", "the equilibrium price"],
  "Read vertically, demand gives marginal willingness to pay.", {1: "that is the height of SUPPLY."})
Q("1.2", "In the cobweb model, why can prices oscillate?",
  ["Producers decide output on last period's price, so supply reacts with a lag",
   "Consumers have no budget", "Demand is perfectly elastic", "Because of taxes"],
  "Lagged supply responses overshoot: high price → big supply → low price → small supply…")

# ----------------------------------------------------------------------------- 1.3
Q("1.3", "Demand is elastic (|ε| > 1). A firm raises its price. Total revenue…",
  ["falls", "rises", "stays the same", "cannot be determined"],
  "Quantity falls proportionally more than price rises.", {1: "that is the inelastic case."})
Q("1.3", "On a straight-line demand curve, elasticity is…",
  ["higher (in absolute value) at high prices and lower at low prices", "constant along the line",
   "equal to the slope", "always 1"],
  "ε = slope × P/Q; P/Q falls as you move down the line.", {1: "constant SLOPE ≠ constant elasticity."})
Q("1.3", "Which product has the most elastic demand?",
  ["One specific brand of bottled water", "Water in general", "Insulin", "Salt"],
  "Narrowly defined goods with close substitutes are most elastic.")
Q("1.3", "Income elasticity of −0.4 means the good is…",
  ["inferior", "normal and a luxury", "a necessity with positive elasticity", "a complement"],
  "Negative income elasticity = inferior good.")
Q("1.3", "Cross-price elasticity between printers and ink is…",
  ["negative: they are complements", "positive: substitutes", "zero", "always −1"],
  "Pricier printers → fewer printers → less ink demanded.")
Q("1.3", "Why is the demand facing ONE seller more elastic than the market demand?",
  ["Buyers can switch to other sellers of the same product", "Because of income effects",
   "Because sellers have capacity limits", "It isn't"],
  "The firm-level demand includes switching between sellers; market demand only includes leaving "
  "the market.")

# ----------------------------------------------------------------------------- 1.4
Q("1.4", "Who bears most of a per-unit tax?",
  ["The less elastic side of the market", "Whoever legally pays it", "Always consumers",
   "Always producers"],
  "Incidence depends on elasticities, not on the law.", {1: "legal incidence ≠ economic incidence."})
Q("1.4", "A binding price ceiling causes…",
  ["a shortage", "a surplus", "no change", "higher quantity traded"],
  "Below p*, Qd > Qs; quantity traded falls to Qs.")
Q("1.4", "Deadweight loss from a tax grows with the tax rate…",
  ["roughly with its square", "proportionally", "not at all", "inversely"],
  "DWL = ½·t·ΔQ and ΔQ is proportional to t.")
Q("1.4", "Consumer surplus is the area…",
  ["under the demand curve and above the price paid", "above the supply curve and below the price",
   "under the supply curve", "between demand and supply to the right of equilibrium"],
  "WTP minus price, summed over buyers.", {1: "that's producer surplus."})
Q("1.4", "Perfect first-degree price discrimination results in…",
  ["efficient output but zero consumer surplus", "a larger deadweight loss than monopoly",
   "the competitive outcome with consumers keeping all surplus", "lower output than monopoly"],
  "Every unit with WTP ≥ MC is sold, but the firm captures all surplus.")

# ----------------------------------------------------------------------------- 1.5
Q("1.5", "At the consumer's optimum (interior)…",
  ["MU_X/P_X = MU_Y/P_Y", "MU_X = MU_Y", "P_X = P_Y", "all income goes to the cheapest good"],
  "The last euro spent on each good must give the same utility.")
Q("1.5", "With Cobb-Douglas utility U = X^0.3·Y^0.7, a rise in the price of Y…",
  ["leaves spending on X unchanged", "raises X demanded", "lowers X demanded", "makes Y inferior"],
  "Cobb-Douglas spends fixed shares: X = 0.3M/P_X, independent of P_Y.")
Q("1.5", "A customer's reservation price for a laptop is €900. At a price of €850 she…",
  ["buys and earns €50 consumer surplus", "doesn't buy", "buys and earns €850 surplus",
   "is indifferent"],
  "Buy if price ≤ WTP; surplus = WTP − price.")
Q("1.5", "Willingness to pay is uniform between €100 and €300 for 200 customers. How many buy at €250?",
  ["50", "150", "125", "200"],
  "Share with WTP ≥ 250 = (300 − 250)/(300 − 100) = 25 % → 50.", {1: "that counts those BELOW 250."})
Q("1.5", "The substitution effect of a price increase…",
  ["always reduces quantity demanded of that good", "can increase demand for normal goods",
   "only exists for inferior goods", "is the same as the income effect"],
  "Relative price ↑ → substitute away, always.")

# ----------------------------------------------------------------------------- 1.6
Q("1.6", "MC crosses ATC…",
  ["at the minimum of ATC", "at the maximum of ATC", "where ATC = AFC", "never"],
  "If the next unit costs less than average the average falls; if more, it rises.")
Q("1.6", "A bicycle needs 2 wheels and 1 frame. You have 9 wheels and 6 frames. Output?",
  ["4", "6", "9", "7"],
  "Fixed proportions: min(9//2, 6//1) = 4; wheels are the bottleneck.")
Q("1.6", "Materials you already own have no other use and can't be resold. Their relevant cost for "
  "a decision today is…",
  ["zero", "what you paid", "the current market price of new materials", "the average past price"],
  "Relevant cost = opportunity cost; with no alternative use, it's zero.",
  {1: "historical cost is sunk.", 2: "only if you could resell them or would otherwise need to buy them."})
Q("1.6", "Diminishing marginal returns means…",
  ["adding more of one input, others fixed, eventually adds less output per unit",
   "long-run average cost rises", "total output falls", "prices fall"],
  "It's a short-run concept about one variable input.")
Q("1.6", "Economies of scope exist when…",
  ["producing several products together is cheaper than separately",
   "average cost falls with the output of one product", "MC is constant", "fixed costs are zero"],
  "Scope = variety; scale = volume.")

# ----------------------------------------------------------------------------- 1.7
Q("1.7", "A price-taking firm maximises profit where…",
  ["P = MC (on the rising part of MC)", "P = ATC", "MR > MC", "P = AVC"],
  "For a price taker MR = P.")
Q("1.7", "In the short run a competitive firm should shut down if…",
  ["P < minimum AVC", "P < minimum ATC", "it makes a loss", "P < MC"],
  "Fixed costs are paid anyway; produce as long as variable costs are covered.",
  {1: "below min ATC but above min AVC the firm loses less by producing.", 2: "a loss smaller than FC is still better than shutting."})
Q("1.7", "In long-run competitive equilibrium…",
  ["economic profit is zero and P = min ATC", "firms earn monopoly profits",
   "accounting profit is zero", "P > MC"],
  "Entry and exit remove economic profit; normal returns remain in accounting profit.")
Q("1.7", "Why is perfect competition allocatively efficient?",
  ["P = MC: the last unit's value equals its cost", "Firms produce at max ATC",
   "Profits are high", "Prices are zero"],
  "Every unit worth more than it costs is produced, none worth less.")

# ----------------------------------------------------------------------------- 1.8
Q("1.8", "For a monopolist with linear demand P = a − bQ, MR is…",
  ["a − 2bQ", "a − bQ", "a", "a/2"],
  "Same intercept, twice the slope.")
Q("1.8", "The Lerner index (P − MC)/P equals…",
  ["1/|ε| at the profit maximum", "|ε|", "MC/P", "always 0.5"],
  "From MR = P(1 − 1/|ε|) = MC.")
Q("1.8", "A monopolist never operates on the inelastic part of demand because…",
  ["there MR < 0: raising price would increase revenue and cut costs", "it is illegal",
   "demand is zero there", "MC is negative there"],
  "With |ε| < 1, a price rise increases revenue AND reduces output costs.")
Q("1.8", "In third-degree price discrimination the higher price goes to…",
  ["the segment with less elastic demand", "the larger segment", "the more elastic segment",
   "the segment with higher costs"],
  "MR = MC in each segment ⇒ markup 1/|ε| higher where demand is less elastic.")
Q("1.8", "'Basic' and 'Pro' versions sold to everyone at different prices is…",
  ["second-degree price discrimination (self-selection)", "first-degree", "third-degree",
   "not discrimination"],
  "Buyers sort themselves through the menu.")
Q("1.8", "With exponential demand Q = A·e^(−βP) and constant MC, the profit-maximising price is…",
  ["MC + 1/β", "MC·β", "1/β", "MC/(1 − β)"],
  "|ε| = βP; Lerner (P − MC)/P = 1/(βP) ⇒ P − MC = 1/β.")

# ----------------------------------------------------------------------------- 1.9
Q("1.9", "In a logit choice model with identical products, the cheapest seller…",
  ["gets the largest share but not all customers", "gets all customers",
   "gets an equal share", "gets nothing"],
  "Pr ∝ exp(−βP): lower price → higher probability, but every option keeps some probability.",
  {1: "that's the Bertrand assumption, not logit."})
Q("1.9", "If every seller raises its price by the same amount (all still affordable) in a logit model…",
  ["shares don't change", "the cheapest seller gains share", "all shares fall to zero",
   "the most expensive gains"],
  "Only differences in utility matter.")
Q("1.9", "A larger price-sensitivity parameter β means…",
  ["buyers concentrate more on the cheapest options", "prices matter less",
   "more customers buy the expensive option", "nothing changes"],
  "Odds between two sellers = exp(−β·ΔP).")
Q("1.9", "In long-run monopolistic competition…",
  ["profits are zero but price exceeds marginal cost", "price = MC", "profits are positive",
   "there is one firm"],
  "Demand is tangent to ATC on its downward part.")
Q("1.9", "HHI with shares 50 %, 50 % is…",
  ["5,000", "100", "2,500", "10,000"], "50² + 50² = 5,000.")
Q("1.9", "A customer only considers options priced at or below her reservation price, then picks "
  "among them with logit probabilities. A seller priced above her reservation price…",
  ["has zero probability of selling to her", "has a small probability",
   "gets the same probability as others", "gets the highest probability"],
  "Above WTP the option is not in her choice set at all.")

# ----------------------------------------------------------------------------- 1.10
Q("1.10", "A factory pollutes a river. Without intervention the market…",
  ["overproduces relative to the social optimum", "underproduces", "is efficient",
   "stops producing"],
  "Marginal social cost exceeds private cost.")
Q("1.10", "Used-car buyers can't tell good cars from lemons; good cars leave the market. This is…",
  ["adverse selection", "moral hazard", "a public good problem", "an externality"],
  "Hidden type before the deal.")
Q("1.10", "A fish stock everyone can access but that is depleted by use is…",
  ["a common resource (rival, non-excludable)", "a public good", "a club good", "a private good"],
  "Rival but non-excludable → tragedy of the commons.")
Q("1.10", "After buying full insurance, a driver drives less carefully. This is…",
  ["moral hazard", "adverse selection", "signalling", "screening"], "Hidden action after the deal.")

# ----------------------------------------------------------------------------- 2.1
Q("2.1", "In the prisoner's dilemma, the Nash equilibrium is…",
  ["both defect, although both cooperating would be better", "both cooperate",
   "one cooperates, one defects", "there is none"],
  "Defect is dominant for each player.")
Q("2.1", "A Nash equilibrium is a profile of strategies where…",
  ["no player can gain by changing strategy alone", "total payoff is maximised",
   "every player uses a dominant strategy", "players cooperate"],
  "Mutual best responses.", {1: "efficiency is not required (see the prisoner's dilemma)."})
Q("2.1", "In 'guess 2/3 of the average', typical players choose 20–35 rather than 0 because…",
  ["they reason only a few steps (level-k)", "they don't understand the rules",
   "0 is dominated", "the equilibrium is 33"],
  "Full iterated elimination leads to 0; real players stop after 1–3 steps.")
Q("2.1", "A strategy that is best whatever the others do is…",
  ["dominant", "mixed", "a Nash equilibrium by itself", "focal"], "Definition.")
Q("2.1", "When payoffs are ranks rather than profits, the game becomes…",
  ["closer to zero-sum: what matters is beating others", "fully cooperative",
   "identical to profit maximisation in every case", "a coordination game"],
  "Your gain in rank is someone else's loss.")

# ----------------------------------------------------------------------------- 2.2
Q("2.2", "In a mixed-strategy equilibrium, each player's mix makes…",
  ["the OTHER player indifferent between her pure strategies", "herself indifferent",
   "payoffs equal for both", "the outcome certain"],
  "Indifference principle.")
Q("2.2", "Backward induction eliminates…",
  ["non-credible threats", "dominant strategies", "mixed strategies", "all Nash equilibria"],
  "Subgame perfection requires optimal play at every node.")
Q("2.2", "Two firms submit sealed price lists on different days, neither sees the other's before the "
  "market opens. Strategically this is…",
  ["a simultaneous-move game", "a sequential game with a first mover",
   "a game of perfect information", "a cooperative game"],
  "What matters is information, not clock time.")
Q("2.2", "Why can limiting your own options raise your payoff?",
  ["It makes threats/commitments credible and changes rivals' behaviour",
   "Fewer options always mean higher payoffs", "It reduces costs", "It never can"],
  "Commitment changes the subgame the rival faces.")
Q("2.2", "Every finite game has at least one Nash equilibrium…",
  ["possibly in mixed strategies", "in pure strategies", "that is efficient", "that is unique"],
  "Nash's existence theorem.")

# ----------------------------------------------------------------------------- 2.3
Q("2.3", "Bertrand duopoly, identical products, no capacity limits, constant MC: price equals…",
  ["marginal cost", "the monopoly price", "the Cournot price", "average of costs and monopoly price"],
  "Any higher price is undercut.")
Q("2.3", "Which feature does NOT soften Bertrand competition?",
  ["Identical products and buyers who always buy the cheapest", "Capacity constraints",
   "Product differentiation", "Repeated interaction"],
  "That feature is exactly what produces the Bertrand paradox.")
Q("2.3", "As the number of Cournot firms grows, the price…",
  ["converges to marginal cost", "rises", "stays at the monopoly level", "becomes zero"],
  "P = (a + nc)/(n + 1) → c.")
Q("2.3", "In differentiated Bertrand, prices are strategic…",
  ["complements: a rival's higher price raises your best price", "substitutes", "independent",
   "dominant"],
  "Best responses slope upward.")
Q("2.3", "Why are cartels unstable?",
  ["Each member gains by secretly producing more / undercutting at the cartel price",
   "Cartel prices are too low", "Members have identical costs", "Demand is inelastic"],
  "Individual incentive vs joint interest — a prisoner's dilemma.")
Q("2.3", "Stackelberg leader vs Cournot: the leader produces…",
  ["more and earns more", "less and earns more", "the same", "less and earns less"],
  "Commitment to a large quantity pushes the follower back.")
Q("2.3", "Edgeworth cycles describe…",
  ["gradual undercutting followed by sudden price jumps when capacity-constrained firms compete",
   "business cycles", "inventory cycles", "seasonal demand"],
  "Capacity limits make undercutting pay only up to a point.")

# ----------------------------------------------------------------------------- 2.4
Q("2.4", "A prisoner's dilemma repeated exactly 10 times (known to all). Backward induction predicts…",
  ["defection in every round", "cooperation in every round", "cooperation until round 10",
   "random play"], "Unravelling from the last round.")
Q("2.4", "With grim trigger, cooperation is sustainable if…",
  ["δ ≥ (T − R)/(T − P)", "δ ≤ (T − R)/(T − P)", "T < R", "δ = 0"],
  "Future loss from punishment must exceed the one-shot gain.")
Q("2.4", "Experimental subjects in finitely repeated games typically…",
  ["cooperate for a while and defect near the end", "defect from round 1", "always cooperate",
   "alternate"], "End-game effect.")
Q("2.4", "Public, transparent information about rivals' actions tends to make tacit collusion…",
  ["easier, because deviations are detected quickly", "impossible", "irrelevant", "illegal by itself"],
  "Monitoring supports trigger strategies.")
Q("2.4", "In a rank-based tournament, a player far behind near the end tends to…",
  ["take more risk", "take less risk", "stop playing", "copy the leader"],
  "Variance is the only way up when the mean outcome loses anyway.")

# ----------------------------------------------------------------------------- 2.5
Q("2.5", "In a second-price sealed-bid auction with private values, the dominant strategy is…",
  ["bid your true value", "shade your bid", "bid above value", "bid the reserve"],
  "Your bid decides whether you win, not what you pay.")
Q("2.5", "In a first-price (pay-your-bid) auction, rational bidders…",
  ["bid below their value", "bid their value", "bid above value", "bid the reserve price"],
  "Bidding value guarantees zero surplus.")
Q("2.5", "As the number of bidders in a first-price auction grows, equilibrium shading…",
  ["decreases: bids approach values", "increases", "is unaffected", "becomes negative"],
  "b = (n − 1)/n · v.")
Q("2.5", "The Dutch (descending) auction is strategically equivalent to…",
  ["the first-price sealed-bid auction", "the English auction", "the second-price auction",
   "a lottery"], "You choose the price at which you accept, and pay it.")
Q("2.5", "Revenue equivalence fails when bidders are…",
  ["risk averse (first-price then yields more)", "risk neutral", "symmetric", "many"],
  "Risk-averse bidders shade less in first-price.")
Q("2.5", "In a pay-your-bid auction your expected surplus from bid b is…",
  ["(v − b) × Pr(win with b)", "v − b", "Pr(win)", "v × Pr(win)"],
  "Margin times winning probability — the shading trade-off.")

# ----------------------------------------------------------------------------- 2.6
Q("2.6", "Multi-unit sealed auction: supply 10. Bids: A 4@12, B 3@10, C 5@8. Under pay-as-bid, C pays…",
  ["3 × 8 = 24", "5 × 8 = 40", "3 × 10 = 30", "0"],
  "C gets the remaining 3 units and pays its own bid.")
Q("2.6", "Same auction under a uniform-price rule (clearing price 8). A pays…",
  ["4 × 8 = 32", "4 × 12 = 48", "4 × 10 = 40", "0"], "Everyone pays the clearing price.")
Q("2.6", "Demand reduction is a strategic problem mainly of…",
  ["uniform-price multi-unit auctions", "pay-as-bid auctions", "single-unit Vickrey auctions",
   "Dutch auctions"], "Your marginal bid can set the price for all your units.")
Q("2.6", "The winner's curse arises in…",
  ["common-value auctions where the winner tends to have the most optimistic estimate",
   "private-value second-price auctions", "any auction with a reserve", "posted-price markets"],
  "Winning is bad news about the value.")
Q("2.6", "With values uniform on [0, 1] and seller value 0, Myerson's optimal reserve is…",
  ["0.5 regardless of the number of bidders", "0", "(n−1)/n", "1"], "r − (1 − F(r))/f(r) = 0 ⇒ r = 1/2.")
Q("2.6", "If an auction caps each bidder's winnings at what her budget can pay, and lots clear one "
  "after another, a bidder bidding on many lots…",
  ["may see her budget used up by lots that clear first", "always gets all lots",
   "pays nothing", "loses solvency"],
  "Budget caps make outcomes depend on which lots clear first.")
Q("2.6", "In a pay-as-bid auction, a bid far above the clearing price compared with one just above it…",
  ["wins the same units but pays more", "wins more units", "pays the same", "loses"],
  "Pay-your-bid: the price paid is your own bid, not the clearing price.")

# ----------------------------------------------------------------------------- 2.7
Q("2.7", "A risk-averse person's certainty equivalent of a gamble is…",
  ["below its expected value", "above its expected value", "equal to it", "zero"],
  "Risk premium = E[X] − CE > 0.")
Q("2.7", "Newsvendor: margin per unit sold €2, loss per unsold unit €1. Critical ratio?",
  ["2/3", "1/3", "1/2", "2"], "c_u/(c_u + c_o) = 2/3.")
Q("2.7", "When sales are capped by your available stock, the sales you observe are…",
  ["a lower bound on demand (censored data)", "exactly demand", "an upper bound on demand",
   "unrelated to demand"], "A sell-out hides how many more would have bought.")
Q("2.7", "Exploration is most valuable…",
  ["early, when there is a lot of time left to use what you learn", "at the end", "never",
   "only if there is no uncertainty"], "The value of information falls as the horizon shrinks.")
Q("2.7", "A higher smoothing parameter α in exponential smoothing makes the estimate…",
  ["react faster but noisier", "smoother and slower", "constant", "biased upward"],
  "α weights the newest observation.")
Q("2.7", "If leftovers can be salvaged at almost full cost, the newsvendor should stock…",
  ["more (critical ratio near 1)", "less", "exactly the mean", "zero"],
  "c_o → 0 ⇒ ratio → 1.")

# ----------------------------------------------------------------------------- 3.1
Q("3.1", "Buying inventory with cash…",
  ["changes the composition of assets but not the total", "increases equity",
   "increases liabilities", "is an expense"], "Cash down, inventory up.")
Q("3.1", "Equity equals…",
  ["assets − liabilities", "assets + liabilities", "cash", "revenue − costs"], "Accounting equation.")
Q("3.1", "Inventory that can never be sold should be valued at…",
  ["zero (lower of cost and net realisable value)", "its cost", "its expected selling price",
   "replacement cost"], "Prudence.")
Q("3.1", "Buying materials on credit…",
  ["increases inventory and payables", "decreases cash", "increases equity", "is revenue"],
  "Asset up, liability up.")
Q("3.1", "Straight-line depreciation of a €10,000 machine over 5 years (no residual value) costs per year…",
  ["€2,000", "€10,000", "€5,000", "€0"], "10,000/5.")

# ----------------------------------------------------------------------------- 3.2
Q("3.2", "Under accrual accounting, COGS for the period includes…",
  ["the cost of the units sold in the period", "all purchases in the period",
   "all cash paid to suppliers", "inventory at period end"], "Matching principle.")
Q("3.2", "Price €150, cost €100. Markup and margin are…",
  ["50 % markup on cost, 33.3 % margin on price", "33.3 % markup, 50 % margin",
   "50 % both", "33.3 % both"], "Markup divides by cost, margin by price.")
Q("3.2", "A firm can be profitable and still run out of cash because…",
  ["cash is tied up in inventory and receivables", "profit always equals cash",
   "depreciation is a cash cost", "revenue is recorded when cash arrives"], "Profit ≠ cash.")
Q("3.2", "DuPont: ROE = …",
  ["net margin × asset turnover × leverage", "ROA × net margin", "EBIT / equity",
   "revenue / equity"], "NI/Sales × Sales/Assets × Assets/Equity.")
Q("3.2", "EBITDA adds back to EBIT…",
  ["depreciation and amortisation", "interest and taxes", "COGS", "dividends"], "Non-cash charges.")

# ----------------------------------------------------------------------------- 3.3
Q("3.3", "An increase in inventory, other things equal, makes operating cash flow…",
  ["lower than net income", "higher than net income", "equal to net income", "negative always"],
  "Cash went into stock.")
Q("3.3", "The cash conversion cycle is…",
  ["DIO + DSO − DPO", "DIO + DSO + DPO", "DPO − DIO", "Revenue/COGS"], "Payables finance you.")
Q("3.3", "The quick ratio excludes inventory because…",
  ["inventory may not turn into cash quickly or at full value", "it is a liability",
   "it is already cash", "of taxes"], "Liquidity test.")
Q("3.3", "With rising purchase prices, FIFO compared with weighted average reports…",
  ["lower COGS and higher profit", "higher COGS", "the same profit", "lower revenue"],
  "Oldest (cheapest) costs go to COGS.")
Q("3.3", "Higher inventory turnover means…",
  ["stock is sold faster, less cash tied up", "more stock held", "lower sales", "higher prices"],
  "COGS / average inventory.")

# ----------------------------------------------------------------------------- 3.4
Q("3.4", "Break-even quantity equals…",
  ["fixed costs / contribution margin per unit", "fixed costs / price", "variable cost / price",
   "price / fixed costs"], "Each unit contributes P − VC towards fixed costs.")
Q("3.4", "With one scarce resource, rank products by…",
  ["contribution margin per unit of the scarce resource", "contribution margin per unit of product",
   "price", "revenue share"], "The resource is what limits you.")
Q("3.4", "Which cost is relevant for a special-order decision?",
  ["Incremental future costs that differ between accepting and rejecting", "Allocated head-office overhead",
   "Sunk R&D", "Last year's materials cost"], "Relevant = future + differential.")
Q("3.4", "Cost-plus pricing with a fixed markup is profit-maximising…",
  ["only if the markup happens to match the demand elasticity", "always", "never",
   "only for monopolies"], "Optimal markup depends on elasticity (lesson 1.8).")
Q("3.4", "High operating leverage means profits are…",
  ["more sensitive to changes in volume", "less sensitive", "always higher", "always lower"],
  "High fixed costs amplify volume effects.")

# ----------------------------------------------------------------------------- 3.5
Q("3.5", "€100 in two years at 10 % is worth today…",
  ["€82.64", "€80", "€121", "€90.91"], "100/1.21.")
Q("3.5", "Accept a project if…",
  ["NPV > 0", "payback < 10 years", "undiscounted cash inflows > investment", "IRR < cost of capital"],
  "NPV measures value created.")
Q("3.5", "A perpetuity of €50/year at 5 % is worth…",
  ["€1,000", "€2,500", "€50", "€250"], "C/r.")
Q("3.5", "Nominal rate 5 %, inflation 3 %: real rate ≈",
  ["2 %", "8 %", "−2 %", "1.67 %"], "Fisher.")
Q("3.5", "Cash flows arriving after a hard deadline at which value is measured are worth…",
  ["nothing for that measure", "their PV", "their face value", "double"],
  "Only what is realised by the deadline counts for an end-dated objective.")

# ----------------------------------------------------------------------------- 3.6
Q("3.6", "Diversification reduces…",
  ["idiosyncratic (firm-specific) risk", "systematic risk", "expected return", "all risk always"],
  "Market risk remains.")
Q("3.6", "A stock with β = 0 has CAPM expected return equal to…",
  ["the risk-free rate", "zero", "the market return", "infinity"], "No systematic risk.")
Q("3.6", "Two assets with correlation +1: portfolio σ is…",
  ["the weighted average of σs", "lower than the average", "zero", "higher than both"],
  "No diversification benefit at ρ = 1.")
Q("3.6", "Leverage…",
  ["amplifies both expected returns and risk of equity", "reduces risk", "has no effect",
   "only increases returns"], "MM proposition II.")
Q("3.6", "The Sharpe ratio measures…",
  ["excess return per unit of total risk", "beta", "dividend yield", "market share"], "(R − Rf)/σ.")

# ----------------------------------------------------------------------------- 3.7
Q("3.7", "When market yields rise, existing bond prices…",
  ["fall", "rise", "don't change", "go to par"], "PV of fixed payments falls.")
Q("3.7", "A bond with coupon rate below its yield trades…",
  ["below par (at a discount)", "at par", "above par", "at zero"], "Investors need a capital gain.")
Q("3.7", "Gordon model: D₁ = €3, r = 9 %, g = 3 %. Price?",
  ["€50", "€33.3", "€100", "€25"], "3/0.06.")
Q("3.7", "The semi-strong efficient market hypothesis says prices reflect…",
  ["all public information", "only past prices", "all private information", "nothing"], "Definition.")
Q("3.7", "Arbitrage is…",
  ["a riskless profit from price differences for the same asset", "any profitable trade",
   "long-term investing", "hedging"], "Law of one price.")
Q("3.7", "The bid-ask spread is…",
  ["the gap between the best buy and best sell prices", "the coupon", "the yield curve slope",
   "a tax"], "The price of immediacy.")

# ----------------------------------------------------------------------------- 4.1
Q("4.1", "GDP counts…",
  ["final goods and services produced domestically", "all transactions", "second-hand sales",
   "intermediate goods separately"], "Avoid double counting.")
Q("4.1", "Goods produced this year but unsold are…",
  ["included as inventory investment", "excluded", "counted next year", "counted as imports"],
  "GDP measures production.")
Q("4.1", "Nominal GDP grows 5 %, the deflator 3 %. Real GDP grows about…",
  ["2 %", "8 %", "5 %", "−2 %"], "Real ≈ nominal − prices.")
Q("4.1", "Value added of a baker who buys flour for €150 and sells bread for €250 is…",
  ["€100", "€250", "€400", "€150"], "Output − intermediate inputs.")
Q("4.1", "At 3.5 % growth, output doubles in about…",
  ["20 years", "35 years", "10 years", "3.5 years"], "Rule of 70.")

# ----------------------------------------------------------------------------- 4.2
Q("4.2", "Unexpected inflation redistributes wealth…",
  ["from lenders to borrowers", "from borrowers to lenders", "not at all", "to savers"],
  "Debts are repaid in cheaper euros.")
Q("4.2", "The ECB's inflation target is…",
  ["2 % over the medium term", "0 %", "5 %", "below 1 %"], "Symmetric 2 %.")
Q("4.2", "MV = PY with constant V: money grows 6 %, real output 2 %. Inflation ≈",
  ["4 %", "8 %", "6 %", "2 %"], "6 − 2.")
Q("4.2", "Cost-push inflation is caused by…",
  ["rising input costs such as energy", "excess demand", "money destruction", "falling wages"],
  "Supply-side shock.")
Q("4.2", "Deflation is dangerous because…",
  ["it raises the real burden of debt and can delay spending", "it raises wages", "it lowers real rates",
   "it never happens"], "Debt deflation.")

# ----------------------------------------------------------------------------- 4.3
Q("4.3", "The unemployment rate is unemployed divided by…",
  ["the labour force", "the working-age population", "the employed", "total population"],
  "Labour force = employed + unemployed.")
Q("4.3", "Discouraged workers who stop searching make the unemployment rate…",
  ["fall, misleadingly", "rise", "unchanged", "negative"], "They leave the labour force.")
Q("4.3", "The natural rate of unemployment includes…",
  ["frictional and structural unemployment", "cyclical unemployment", "only frictional", "nothing"],
  "Cyclical is the deviation from it.")
Q("4.3", "Okun's law links…",
  ["the output gap and unemployment", "inflation and money", "rates and exchange rates",
   "trade and growth"], "≈ ½ point per 1 % gap.")
Q("4.3", "A predictable December spike in retail sales is…",
  ["seasonality", "a business cycle expansion", "a structural break", "inflation"],
  "Repeats with a fixed period.")

# ----------------------------------------------------------------------------- 4.4
Q("4.4", "An oil price shock shifts SRAS left, causing…",
  ["stagflation: lower output and higher prices", "boom", "deflation", "no change"],
  "Supply shocks move output and prices in opposite directions.")
Q("4.4", "With MPC = 0.8 (closed economy, no taxes) the spending multiplier is…",
  ["5", "0.8", "1.25", "4"], "1/(1 − 0.8).")
Q("4.4", "Crowding out means…",
  ["government borrowing raises rates and reduces private investment", "imports fall",
   "taxes fall", "the multiplier rises"], "Reduces the fiscal multiplier.")
Q("4.4", "The long-run aggregate supply curve is vertical because…",
  ["potential output depends on resources and technology, not on the price level",
   "prices are fixed", "demand is vertical", "of taxes"], "Classical long run.")
Q("4.4", "Debt/GDP tends to fall when…",
  ["growth exceeds the interest rate and/or there is a primary surplus", "rates exceed growth",
   "deficits rise", "inflation is zero"], "Δd ≈ (r − g)d − primary surplus.")

# ----------------------------------------------------------------------------- 4.5
Q("4.5", "Raising the policy rate tends to…",
  ["reduce spending and inflation with a lag", "raise inflation immediately", "weaken the currency",
   "raise bond prices"], "Contractionary.")
Q("4.5", "Quantitative easing works mainly by…",
  ["buying bonds to lower long-term yields", "raising short-term rates", "printing banknotes for "
   "households", "cutting taxes"], "Asset purchases.")
Q("4.5", "Central bank independence matters because…",
  ["it anchors inflation expectations and prevents deficit monetisation", "it raises growth directly",
   "it fixes exchange rates", "it lowers unemployment permanently"], "Credibility.")
Q("4.5", "Taylor rule with r* = 1 %, π = 3 %, target 2 %, gap 0: i =",
  ["4.5 %", "4 %", "3 %", "5 %"], "1 + 3 + 0.5 + 0.")

# ----------------------------------------------------------------------------- 4.6
Q("4.6", "If the euro appreciates against the dollar, European exports to the US become…",
  ["more expensive for Americans", "cheaper", "unaffected", "duty-free"], "More dollars per euro.")
Q("4.6", "A current-account surplus means the country…",
  ["saves more than it invests and lends abroad", "borrows from abroad", "has a budget surplus",
   "imports more than it exports"], "S − I = NX.")
Q("4.6", "A tariff on imports…",
  ["raises domestic prices and creates a deadweight loss", "lowers domestic prices", "has no cost",
   "always raises total welfare"], "Protects producers at consumers' expense.")
Q("4.6", "Trade between similar countries in similar goods is explained by…",
  ["economies of scale and love of variety (new trade theory)", "Ricardian comparative advantage only",
   "tariffs", "PPP"], "Krugman.")
Q("4.6", "A shortage of one component halting production of finished goods illustrates…",
  ["fixed-proportions production: output limited by the scarcest input", "economies of scope",
   "PPP", "moral hazard"], "Bottleneck input (lesson 1.6).")
