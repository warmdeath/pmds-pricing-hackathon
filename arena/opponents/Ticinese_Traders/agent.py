# =============================================================================
#  !!! SPOILER WARNING !!!  ARENA OPPONENT -- DO NOT READ DURING YOUR ATTEMPT.
#  This file is one of the 39 simulated rival teams of the practice hackathon.
#  Reading it tells you how the field plays and spoils the exercise.
# =============================================================================
from dme_simulator.agents import (
    AssemblyOrder, BaseAgent, Bid, Decision, Listing, Observation,
)
from dme_simulator.config import GoodsConfig


PARAMS = {'qty': 13, 'overbid': 3.92}

# Premium positioning: we are a quality brand!
PREMIUM_PRICES = {'LAPTOP': 1227.6, 'CONSOLE': 825.4, 'PHONE': 528.7, 'TABLET': 466.2, 'SMARTWATCH': 213.2}


class PremiumBrandAgent(BaseAgent):
    def decide(self, state: Observation, goods_config: GoodsConfig) -> Decision:
        # Always win the auction: bid well above the reserve
        bids = []
        for lot in state.auction_lots:
            qty = min(lot.quantity, PARAMS["qty"])
            if qty > 0:
                bids.append(Bid(lot.good, int(qty), lot.reserve_price * PARAMS["overbid"]))

        # Build the expensive stuff first
        order = sorted(
            goods_config.recipes.items(),
            key=lambda item: -sum(item[1].inputs.values()),
        )
        assembly = [AssemblyOrder(name, 99) for name, _ in order]

        listings = []
        for good in goods_config.finished_goods:
            price = PREMIUM_PRICES.get(good, 999.0)
            listings.append(Listing(good, 1000, price))
        return Decision(bids=bids, assembly=assembly, listings=listings)
