"""Mechanics map: where each concept appears in the DME simulator.

Facts only -- each entry states what the mechanic IS and where it is defined.
It deliberately says nothing about what an agent should do about it.
"""

SIM_MAP = [
    {"concept": "Sealed-bid, pay-your-bid multi-unit auction", "lesson": "2.6",
     "terms": ["Pay-as-bid auction", "Sealed-bid auction", "Multi-unit auction", "First-price auction"],
     "mechanic": "Each raw material is sold every turn to sealed bids sorted by price, highest first; "
                 "each winner pays its own bid per unit.",
     "where": "README §2.2; simulation.py _clear_auction"},
    {"concept": "Reserve price", "lesson": "2.6", "terms": ["Reserve price"],
     "mechanic": "Bids below the lot's reserve_price are discarded. The reserve is "
                 "base_price × max(price_floor_multiplier, 1 − price_stock_factor·ln(1 + stock/production_max)).",
     "where": "README §2.2; simulation.py _publish_lots; config suppliers.*"},
    {"concept": "Rationing of tied bids", "lesson": "1.4", "terms": ["Rationing"],
     "mechanic": "Bids at exactly the same price share the remaining units by round robin in random team order.",
     "where": "README §2.2 'Ties'; simulation.py _allocate"},
    {"concept": "Bidder budget constraint", "lesson": "2.6", "terms": ["Budget constraint (bidder)"],
     "mechanic": "Units won are capped by the capital the team still holds during the auction; "
                 "materials clear in a random order each turn.",
     "where": "README §2.2 'The budget cap'; simulation.py _clear_auction"},
    {"concept": "Supply that responds to stock (adaptive supply)", "lesson": "1.2",
     "terms": ["Supply curve"],
     "mechanic": "Suppliers replenish a random amount each turn; unsold stock carries over up to a capacity; "
                 "persistently empty or full stock changes replenishment and capacity.",
     "where": "README §2.2; simulation.py _publish_lots, _adapt_supply; config suppliers.*.adaptation"},
    {"concept": "Fixed-proportions production", "lesson": "1.6",
     "terms": ["Fixed-proportions technology", "Bottleneck", "Production function"],
     "mechanic": "Recipes convert fixed quantities of raw materials into one finished unit; assembly orders "
                 "run in the order given, limited by materials held.",
     "where": "README §2.3; config goods.recipes; simulation.py _produce"},
    {"concept": "Capacity constraint", "lesson": "1.6", "terms": ["Capacity constraint"],
     "mechanic": "Optional production.capacity_per_turn caps total units built per team per turn (null = no cap).",
     "where": "README §2.3; config production"},
    {"concept": "Reservation prices and segments", "lesson": "1.5",
     "terms": ["Willingness to pay", "Reservation price", "Market segment"],
     "mechanic": "Each customer belongs to a segment, picks a good by the segment's preference weights and "
                 "draws a private valuation uniformly from the segment's willingness_to_pay range for that good.",
     "where": "README §2.4; config consumer_market.segments; simulation.py _draw_customers"},
    {"concept": "Choice set + logit choice", "lesson": "1.9",
     "terms": ["Logit model", "Price sensitivity", "Choice set"],
     "mechanic": "A customer considers only listings priced at or below her valuation, then picks one with "
                 "probability proportional to exp(−β·price), β = price_sensitivity_beta.",
     "where": "README §2.4; simulation.py _clear_sales; config consumer_market.price_sensitivity_beta"},
    {"concept": "Demand fluctuating over time", "lesson": "4.3", "terms": ["Seasonality", "Business cycle"],
     "mechanic": "Customers per turn = base_customers + amplitude·sin(turn / period_divisor).",
     "where": "simulation.py _draw_customers; config consumer_market"},
    {"concept": "Unserved demand", "lesson": "2.7", "terms": ["Censored demand"],
     "mechanic": "A customer with no affordable, available listing leaves without buying (counted as a "
                 "'stockout' in the dashboards).",
     "where": "README §2.4; simulation.py _clear_sales"},
    {"concept": "Multiple prices for one good", "lesson": "1.8", "terms": ["Price discrimination"],
     "mechanic": "A team may split one finished good across several listings at different prices; listings "
                 "are capped by the inventory actually held.",
     "where": "README §2.4; simulation.py _collect_listings"},
    {"concept": "Inventory carry-over without holding cost", "lesson": "3.3",
     "terms": ["Inventory", "Working capital"],
     "mechanic": "Unsold raw materials and finished goods carry over to the next turn for free; there are "
                 "no workforce or storage costs.",
     "where": "README §2 (intro)"},
    {"concept": "Score = cash; leftover stock worth nothing", "lesson": "2.7",
     "terms": ["Salvage value", "Net realisable value"],
     "mechanic": "Each match ranks teams by final capital (cash); inventory adds no value to the score.",
     "where": "README §1.5 'Official scoring'"},
    {"concept": "Cash flow = sales − purchases", "lesson": "3.3", "terms": ["Cash flow statement"],
     "mechanic": "Capital leaves only through auction purchases and returns only through sales revenue, "
                 "paid immediately.",
     "where": "README §2 (intro); dashboards 'Cash flow' chart"},
    {"concept": "Bankruptcy / liquidation", "lesson": "3.3", "terms": ["Bankruptcy", "Solvency"],
     "mechanic": "If capital is below zero at the end of a turn, the team is liquidated: inventory cleared, "
                 "no further turns.",
     "where": "README §2.6; simulation.py _declare_bankruptcy"},
    {"concept": "Simultaneous sealed decisions each turn", "lesson": "2.2",
     "terms": ["Simultaneous game", "Repeated game"],
     "mechanic": "Every turn each team returns one Decision (bids, assembly, listings) without seeing the "
                 "others' current decisions; the same game is played turn after turn.",
     "where": "README §2.1; docs/agent_interface.md"},
    {"concept": "Public information", "lesson": "1.10",
     "terms": ["Public information", "Asymmetric information"],
     "mechanic": "public_inventories and public_capital show every team's holdings; auction and sales "
                 "transaction lists include only the observing team's own transactions unless "
                 "agents.observe_all_transactions is true.",
     "where": "README §2.5; docs/agent_interface.md §1.1"},
    {"concept": "Number of competitors", "lesson": "2.3", "terms": ["Oligopoly", "Market share"],
     "mechanic": "Every discovered agent bundle is a team in the match; the arena field has 40 teams.",
     "where": "README §3.1; arena/README.md"},
    {"concept": "Rank-based overall score", "lesson": "2.4", "terms": ["Tournament"],
     "mechanic": "Overall ranking = arithmetic mean of each agent's ranks across all matches; lower is better.",
     "where": "README §1.5 'Official scoring'"},
    {"concept": "Length of the game", "lesson": "2.4", "terms": ["Finite horizon"],
     "mechanic": "Each scenario has a fixed number of turns (config 'turns'); the fields an agent observes "
                 "each turn are listed in the interface reference.",
     "where": "config/*.yaml 'turns'; docs/agent_interface.md §1.1"},
    {"concept": "Decision time limit", "lesson": "2.7", "terms": [],
     "mechanic": "Each decision must return within agents.decide_timeout_ms (100 ms); a timeout, exception "
                 "or invalid decision becomes an empty decision for that turn.",
     "where": "README §2.1; runner.py _decide_with_timeout, _validate_decision"},
]
