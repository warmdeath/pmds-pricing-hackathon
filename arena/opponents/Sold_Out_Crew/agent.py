# =============================================================================
#  !!! SPOILER WARNING !!!  ARENA OPPONENT -- DO NOT READ DURING YOUR ATTEMPT.
#  This file is one of the 39 simulated rival teams of the practice hackathon.
#  Reading it tells you how the field plays and spoils the exercise.
# =============================================================================
from dme_simulator.agents import (
    AssemblyOrder, BaseAgent, Bid, Decision, Listing, Observation,
)
from dme_simulator.config import GoodsConfig


PARAMS = {'qty': 3, 'mult': 1.36, 'price': 420.0}

MATERIALS_WE_USE = ["CHIP", "DISPLAY", "BATTERY"]


class TabletFocusAgent(BaseAgent):
    """We focus on tablets and phones, the mainstream products."""

    def decide(self, state: Observation, goods_config: GoodsConfig) -> Decision:
        bids = []
        for lot in state.auction_lots:
            if lot.good in MATERIALS_WE_USE:
                bids.append(Bid(lot.good, PARAMS["qty"], round(lot.reserve_price * PARAMS["mult"], 2)))

        assembly = []
        for name in ("RECIPE_TABLET", "RECIPE_PHONE"):
            if name in goods_config.recipes:
                assembly.append(AssemblyOrder(name, PARAMS["qty"]))

        listings = []
        for good in ("TABLET", "PHONE"):
            if good in goods_config.finished_goods:
                listings.append(Listing(good, PARAMS["qty"] * 3, PARAMS["price"]))
        return Decision(bids=bids, assembly=assembly, listings=listings)
