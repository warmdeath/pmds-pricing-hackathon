# =============================================================================
#  !!! SPOILER WARNING !!!  ARENA OPPONENT -- DO NOT READ DURING YOUR ATTEMPT.
#  This file is one of the 39 simulated rival teams of the practice hackathon.
#  Reading it tells you how the field plays and spoils the exercise.
# =============================================================================
from dme_simulator.agents import (
    AssemblyOrder, BaseAgent, Bid, Decision, Listing, Observation,
)
from dme_simulator.config import GoodsConfig


PARAMS = {'markup': 1.47, 'budget_share': 0.25, 'target': {'LAPTOP': 1, 'CONSOLE': 3, 'PHONE': 1, 'TABLET': 3, 'SMARTWATCH': 1}}
PRICES = {'LAPTOP': 752.3, 'CONSOLE': 459.2, 'PHONE': 289.9, 'TABLET': 300.9, 'SMARTWATCH': 120.6}


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


class FixedPriceAgent(BaseAgent):
    """Sensible fixed price list, steady production, budget discipline."""

    def decide(self, state: Observation, goods_config: GoodsConfig) -> Decision:
        unit_cost = {lot.good: lot.reserve_price * PARAMS["markup"] for lot in state.auction_lots}
        plan = {}
        needs = {}
        for name, recipe in goods_config.recipes.items():
            good = recipe.output_good
            price = PRICES.get(good, 0.0)
            if price <= recipe_cost(recipe, unit_cost) * 1.5:
                continue
            target = PARAMS["target"].get(good, 1)
            units = max(0, target - state.inventory.get(good, 0))
            if units > 0:
                plan[name] = units
                for m, q in recipe.inputs.items():
                    needs[m] = needs.get(m, 0) + q * units
        bids = plan_bids(state, needs, PARAMS["markup"], state.capital * PARAMS["budget_share"])
        assembly = [AssemblyOrder(name, units) for name, units in plan.items()]
        listings = []
        for name, recipe in goods_config.recipes.items():
            good = recipe.output_good
            qty = state.inventory.get(good, 0) + plan.get(name, 0)
            if qty > 0 and good in PRICES:
                listings.append(Listing(good, qty, PRICES[good]))
        return Decision(bids=bids, assembly=assembly, listings=listings)
