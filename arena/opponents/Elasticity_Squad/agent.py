# =============================================================================
#  !!! SPOILER WARNING !!!  ARENA OPPONENT -- DO NOT READ DURING YOUR ATTEMPT.
#  This file is one of the 39 simulated rival teams of the practice hackathon.
#  Reading it tells you how the field plays and spoils the exercise.
# =============================================================================
from dme_simulator.agents import (
    AssemblyOrder, BaseAgent, Bid, Decision, Listing, Observation,
)
from dme_simulator.config import GoodsConfig


PARAMS = {'focus': ['LAPTOP', 'CONSOLE'], 'markup': 1.33, 'budget_share': 0.26, 'target': 3, 'up': 0.064, 'down': 0.068}
START_PRICES = {'LAPTOP': 764.2, 'CONSOLE': 510.3, 'PHONE': 263.6, 'TABLET': 264.1, 'SMARTWATCH': 112.7}


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


class NicheAgent(BaseAgent):
    """Specialise in a few products and price them carefully."""

    def __init__(self):
        self.prices = dict(START_PRICES)
        self.listed = {}
        self.sales_seen = 0

    def decide(self, state: Observation, goods_config: GoodsConfig) -> Decision:
        sold = {}
        for sale in state.sales_transactions[self.sales_seen:]:
            sold[sale.good] = sold.get(sale.good, 0) + sale.quantity
        self.sales_seen = len(state.sales_transactions)
        for good, listed in self.listed.items():
            if sold.get(good, 0) >= listed:
                self.prices[good] *= 1.0 + PARAMS["up"]
            elif sold.get(good, 0) == 0:
                self.prices[good] *= 1.0 - PARAMS["down"]

        unit_cost = {lot.good: lot.reserve_price * PARAMS["markup"] for lot in state.auction_lots}
        focus = [g for g in PARAMS["focus"] if g in goods_config.finished_goods]
        if not focus:
            focus = list(goods_config.finished_goods)
        plan = {}
        needs = {}
        for name, recipe in goods_config.recipes.items():
            good = recipe.output_good
            if good not in focus:
                continue
            cost = recipe_cost(recipe, unit_cost)
            self.prices[good] = max(self.prices.get(good, cost * 4), cost * 1.5)
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
            if qty > 0 and good in self.prices:
                listings.append(Listing(good, qty, round(self.prices[good], 2)))
                self.listed[good] = max(1, state.inventory.get(good, 0))
        return Decision(bids=bids, assembly=assembly, listings=listings)
