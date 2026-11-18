# =============================================================================
#  !!! SPOILER WARNING !!!  ARENA OPPONENT -- DO NOT READ DURING YOUR ATTEMPT.
#  This file is one of the 39 simulated rival teams of the practice hackathon.
#  Reading it tells you how the field plays and spoils the exercise.
# =============================================================================
from dme_simulator.agents import (
    AssemblyOrder, BaseAgent, Bid, Decision, Listing, Observation,
)
from dme_simulator.config import GoodsConfig


PARAMS = {'build_per_turn': 1, 'mult': 1.28, 'keep': 2}
PRICES = {'LAPTOP': 733.0, 'CONSOLE': 585.7, 'PHONE': 308.7, 'TABLET': 341.7, 'SMARTWATCH': 134.4}


class SafetyStockAgent(BaseAgent):
    """Keep a safety stock of every product so we never run out."""

    def decide(self, state: Observation, goods_config: GoodsConfig) -> Decision:
        target = PARAMS["build_per_turn"]
        need = {}
        for recipe in goods_config.recipes.values():
            for material, units in recipe.inputs.items():
                need[material] = need.get(material, 0) + units * target
        bids = []
        for lot in state.auction_lots:
            missing = need.get(lot.good, 0) - state.inventory.get(lot.good, 0)
            if missing > 0:
                bids.append(Bid(lot.good, int(missing), round(lot.reserve_price * PARAMS["mult"], 2)))

        assembly = [AssemblyOrder(name, target) for name in goods_config.recipes]

        listings = []
        for good in goods_config.finished_goods:
            # never sell the safety stock
            sellable = state.inventory.get(good, 0) - PARAMS["keep"]
            if sellable > 0:
                listings.append(Listing(good, sellable, PRICES.get(good, 300.0)))
        return Decision(bids=bids, assembly=assembly, listings=listings)
