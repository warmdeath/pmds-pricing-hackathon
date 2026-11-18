# =============================================================================
#  !!! SPOILER WARNING !!!  ARENA OPPONENT -- DO NOT READ DURING YOUR ATTEMPT.
#  This file is one of the 39 simulated rival teams of the practice hackathon.
#  Reading it tells you how the field plays and spoils the exercise.
# =============================================================================
from dme_simulator.agents import (
    AssemblyOrder, BaseAgent, Bid, Decision, Listing, Observation,
)
from dme_simulator.config import GoodsConfig


PARAMS = {'hoard_turns': 12, 'hoard_budget': 0.46, 'hoard_markup': 1.52, 'target': 1, 'build': 3, 'down': 0.057}
PRICES = {'LAPTOP': 856.3, 'CONSOLE': 655.1, 'PHONE': 373.7, 'TABLET': 369.8, 'SMARTWATCH': 137.3}


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


class StockpileAgent(BaseAgent):
    """Corner the materials early, then sell at premium prices."""

    def __init__(self):
        self.prices = dict(PRICES)
        self.sales_seen = 0

    def decide(self, state: Observation, goods_config: GoodsConfig) -> Decision:
        sold = {}
        for sale in state.sales_transactions[self.sales_seen:]:
            sold[sale.good] = sold.get(sale.good, 0) + sale.quantity
        self.sales_seen = len(state.sales_transactions)

        early = state.turn <= PARAMS["hoard_turns"]
        bids = []
        if early:
            budget = state.capital * PARAMS["hoard_budget"]
            per_lot = budget / max(1, len(state.auction_lots))
            for lot in state.auction_lots:
                price = lot.reserve_price * PARAMS["hoard_markup"]
                qty = min(lot.quantity, int(per_lot // price)) if price > 0 else 0
                if qty > 0:
                    bids.append(Bid(lot.good, qty, round(price, 2)))
        else:
            needs = {}
            for recipe in goods_config.recipes.values():
                for m, q in recipe.inputs.items():
                    needs[m] = needs.get(m, 0) + q * PARAMS["target"]
            bids = plan_bids(state, needs, 1.15, state.capital * 0.2)

        for good in goods_config.finished_goods:
            if good not in self.prices:
                self.prices[good] = 300.0
            if state.inventory.get(good, 0) > 6 and sold.get(good, 0) == 0:
                self.prices[good] *= 1.0 - PARAMS["down"]

        assembly = [AssemblyOrder(name, PARAMS["build"]) for name in goods_config.recipes]
        listings = []
        for recipe in goods_config.recipes.values():
            good = recipe.output_good
            qty = state.inventory.get(good, 0) + PARAMS["build"]
            listings.append(Listing(good, qty, round(self.prices[good], 2)))
        return Decision(bids=bids, assembly=assembly, listings=listings)
