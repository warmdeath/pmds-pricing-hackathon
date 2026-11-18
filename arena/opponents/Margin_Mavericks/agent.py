# =============================================================================
#  !!! SPOILER WARNING !!!  ARENA OPPONENT -- DO NOT READ DURING YOUR ATTEMPT.
#  This file is one of the 39 simulated rival teams of the practice hackathon.
#  Reading it tells you how the field plays and spoils the exercise.
# =============================================================================
from dme_simulator.agents import (
    AssemblyOrder, BaseAgent, Bid, Decision, Listing, Observation,
)
from dme_simulator.config import GoodsConfig


PARAMS = {'mult': 1.18, 'markup': 1.52}


class CostPlusAgent(BaseAgent):
    def decide(self, state: Observation, goods_config: GoodsConfig) -> Decision:
        reserve = {lot.good: lot.reserve_price for lot in state.auction_lots}

        bids = []
        for lot in state.auction_lots:
            qty = int(state.capital // 1000)  # more money -> buy more
            if qty > 0:
                bids.append(Bid(lot.good, qty, round(lot.reserve_price * PARAMS["mult"], 2)))

        assembly = [AssemblyOrder(name, 5) for name in goods_config.recipes]

        listings = []
        for recipe in goods_config.recipes.values():
            cost = 0.0
            for material, units in recipe.inputs.items():
                cost += reserve.get(material, 10.0) * units
            listings.append(Listing(recipe.output_good, 50, round(cost * PARAMS["markup"], 2)))
        return Decision(bids=bids, assembly=assembly, listings=listings)
