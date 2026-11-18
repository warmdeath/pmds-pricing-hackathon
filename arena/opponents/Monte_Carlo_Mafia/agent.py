# =============================================================================
#  !!! SPOILER WARNING !!!  ARENA OPPONENT -- DO NOT READ DURING YOUR ATTEMPT.
#  This file is one of the 39 simulated rival teams of the practice hackathon.
#  Reading it tells you how the field plays and spoils the exercise.
# =============================================================================
from dme_simulator.agents import (
    AssemblyOrder, BaseAgent, Bid, Decision, Listing, Observation,
)
from dme_simulator.config import GoodsConfig


PARAMS = {'markup': 1.41, 'budget_share': 0.29, 'target': 2, 'up': 0.075, 'down': 0.07, 'floor': 1.62}
START_PRICES = {'LAPTOP': 812.5, 'CONSOLE': 612.9, 'PHONE': 275.8, 'TABLET': 271.4, 'SMARTWATCH': 118.4}


def recipe_cost(recipe, unit_cost):
    return sum(unit_cost.get(m, 0.0) * q for m, q in recipe.inputs.items())


def plan_bids(state, needs, markup, budget):
    """Bid for missing materials at reserve * markup, scaled to a budget."""
    lots = {lot.good: lot for lot in state.auction_lots}
    wanted = {}
    for material, units in needs.items():
        missing = units - state.inventory.get(material, 0)
        if material in lots and missing > 0:
            wanted[material] = min(missing, lots[material].quantity)
    cost = sum(lots[m].reserve_price * markup * q for m, q in wanted.items())
    scale = 1.0 if cost <= budget or cost <= 0 else budget / cost
    bids = []
    for material, units in wanted.items():
        qty = int(units * scale)
        if qty > 0:
            bids.append(Bid(material, qty, round(lots[material].reserve_price * markup, 2)))
    return bids


class ReactivePricer(BaseAgent):
    """Raise the price when a product sells out, cut it when nothing sells."""

    def __init__(self):
        self.prices = dict(START_PRICES)
        self.listed = {}
        self.sales_seen = 0

    def decide(self, state: Observation, goods_config: GoodsConfig) -> Decision:
        sold = {}
        for sale in state.sales_transactions[self.sales_seen:]:
            sold[sale.good] = sold.get(sale.good, 0) + sale.quantity
        self.sales_seen = len(state.sales_transactions)

        unit_cost = {lot.good: lot.reserve_price * PARAMS["markup"] for lot in state.auction_lots}
        costs = {r.output_good: recipe_cost(r, unit_cost) for r in goods_config.recipes.values()}

        for good, listed in self.listed.items():
            if listed <= 0:
                continue
            if sold.get(good, 0) >= listed:
                self.prices[good] *= 1.0 + PARAMS["up"]
            elif sold.get(good, 0) == 0:
                self.prices[good] *= 1.0 - PARAMS["down"]
            floor = costs.get(good, 0.0) * PARAMS["floor"]
            self.prices[good] = max(self.prices[good], floor)

        plan = {}
        needs = {}
        for name, recipe in goods_config.recipes.items():
            good = recipe.output_good
            if good not in self.prices:
                self.prices[good] = costs.get(good, 50.0) * 4
            units = max(0, PARAMS["target"] - state.inventory.get(good, 0))
            if units > 0:
                plan[name] = units
                for m, q in recipe.inputs.items():
                    needs[m] = needs.get(m, 0) + q * units
        bids = plan_bids(state, needs, PARAMS["markup"], state.capital * PARAMS["budget_share"])
        assembly = [AssemblyOrder(name, units) for name, units in plan.items()]

        listings = []
        self.listed = {}
        for name, recipe in goods_config.recipes.items():
            good = recipe.output_good
            qty = state.inventory.get(good, 0) + plan.get(name, 0)
            if qty > 0:
                listings.append(Listing(good, qty, round(self.prices[good], 2)))
                # count only what we already hold; planned units may not be built
                self.listed[good] = max(1, state.inventory.get(good, 0))
        return Decision(bids=bids, assembly=assembly, listings=listings)
