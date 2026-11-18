# =============================================================================
#  !!! SPOILER WARNING !!!  ARENA OPPONENT -- DO NOT READ DURING YOUR ATTEMPT.
#  This file is one of the 39 simulated rival teams of the practice hackathon.
#  Reading it tells you how the field plays and spoils the exercise.
# =============================================================================
from dme_simulator.agents import (
    AssemblyOrder, BaseAgent, Bid, Decision, Listing, Observation,
)
from dme_simulator.config import GoodsConfig


PARAMS = {'qty': 16, 'overbid': 4.55}

# Premium positioning: we are a quality brand!
PREMIUM_PRICES = {'LAPTOP': 1203.0, 'CONSOLE': 918.2, 'PHONE': 522.5, 'TABLET': 515.4, 'SMARTWATCH': 204.7}


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
