# =============================================================================
#  !!! SPOILER WARNING !!!  ARENA OPPONENT -- DO NOT READ DURING YOUR ATTEMPT.
#  This file is one of the 39 simulated rival teams of the practice hackathon.
#  Reading it tells you how the field plays and spoils the exercise.
# =============================================================================
from dme_simulator.agents import (
    AssemblyOrder, BaseAgent, Bid, Decision, Listing, Observation,
)
from dme_simulator.config import GoodsConfig


PARAMS = {'per_recipe': 2, 'mult': 1.36, 'flat_price': 399.0}


class FlatPriceAgent(BaseAgent):
    """Build a few of every product and sell everything at one price."""

    def __init__(self):
        self.turns_played = 0

    def decide(self, state: Observation, goods_config: GoodsConfig) -> Decision:
        self.turns_played += 1
        n = PARAMS["per_recipe"]

        # How many of each material do we need to build n of every product?
        need = {}
        for recipe in goods_config.recipes.values():
            for material, units in recipe.inputs.items():
                need[material] = need.get(material, 0) + units * n

        bids = []
        for lot in state.auction_lots:
            qty = need.get(lot.good, 0)
            if qty > 0:
                bids.append(Bid(lot.good, int(qty), round(lot.reserve_price * PARAMS["mult"], 2)))

        assembly = [AssemblyOrder(name, n) for name in goods_config.recipes]

        # Sell what we have in the warehouse
        listings = []
        for good in goods_config.finished_goods:
            qty = state.inventory.get(good, 0)
            if qty > 0:
                listings.append(Listing(good, qty, PARAMS["flat_price"]))
        return Decision(bids=bids, assembly=assembly, listings=listings)
