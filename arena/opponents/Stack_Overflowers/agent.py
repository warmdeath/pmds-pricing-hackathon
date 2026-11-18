# =============================================================================
#  !!! SPOILER WARNING !!!  ARENA OPPONENT -- DO NOT READ DURING YOUR ATTEMPT.
#  This file is one of the 39 simulated rival teams of the practice hackathon.
#  Reading it tells you how the field plays and spoils the exercise.
# =============================================================================
from dme_simulator.agents import (
    AssemblyOrder, BaseAgent, Bid, Decision, Listing, Observation,
)
from dme_simulator.config import GoodsConfig


PARAMS = {'budget_share': 0.1, 'mult': 1.26, 'build': 2}
START_PRICES = {'LAPTOP': 1026.0, 'CONSOLE': 697.2, 'PHONE': 406.1, 'TABLET': 331.3, 'SMARTWATCH': 180.0}


class AdaptiveAgent(BaseAgent):
    """Adaptive pricing: lower the price if a product does not sell."""

    def __init__(self):
        self.last_listed = {}

    def decide(self, state: Observation, goods_config: GoodsConfig) -> Decision:
        price_memory = {}
        for good in goods_config.finished_goods:
            if good not in price_memory:
                price_memory[good] = START_PRICES.get(good, 300.0)

        # adjust prices based on what happened last turn
        for good, listed in self.last_listed.items():
            if listed > 0 and state.inventory.get(good, 0) >= listed:
                # nothing sold -> make it cheaper
                price_memory[good] = price_memory[good] * 0.95

        budget = state.capital * PARAMS["budget_share"]
        per_lot = budget / max(1, len(state.auction_lots))
        bids = []
        for lot in state.auction_lots:
            price = lot.reserve_price * PARAMS["mult"]
            qty = int(per_lot // price) if price > 0 else 0
            if qty > 0:
                bids.append(Bid(lot.good, qty, round(price, 2)))

        assembly = [AssemblyOrder(name, PARAMS["build"]) for name in goods_config.recipes]

        listings = []
        self.last_listed = {}
        for good in goods_config.finished_goods:
            qty = state.inventory.get(good, 0)
            if qty > 0:
                listings.append(Listing(good, qty, round(price_memory[good], 2)))
                self.last_listed[good] = qty
        return Decision(bids=bids, assembly=assembly, listings=listings)
