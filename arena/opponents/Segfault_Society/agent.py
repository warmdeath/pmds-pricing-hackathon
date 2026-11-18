# =============================================================================
#  !!! SPOILER WARNING !!!  ARENA OPPONENT -- DO NOT READ DURING YOUR ATTEMPT.
#  This file is one of the 39 simulated rival teams of the practice hackathon.
#  Reading it tells you how the field plays and spoils the exercise.
# =============================================================================
from dme_simulator.agents import (
    AssemblyOrder, BaseAgent, Bid, Decision, Listing, Observation,
)
from dme_simulator.config import GoodsConfig


PARAMS = {'markup': 1.32, 'qty': 3}


class SmartPricingAgent(BaseAgent):
    """Cost-plus pricing agent.

    Step 1: compute the production cost of each product.
    Step 2: add a markup.
    Step 3: buy materials and produce.
    """

    def decide(self, state: Observation, goods_config: GoodsConfig) -> Decision:
        # Step 1: Calculate the production cost for each product
        cost = {}
        for name, recipe in goods_config.recipes.items():
            c = 0
            for lot in state.auction_lots:
                if lot.good in recipe.inputs:
                    c += lot.quantity * recipe.inputs[lot.good]
            cost[recipe.output_good] = c

        # Step 2: Apply the markup to get the optimal selling price
        listings = []
        for good in goods_config.finished_goods:
            price = max(1.0, cost.get(good, 100) * PARAMS["markup"])
            listings.append(Listing(good, 100, round(price, 2)))

        # Step 3: Buy materials for production
        bids = []
        for lot in state.auction_lots:
            bids.append(Bid(lot.good, PARAMS["qty"], round(lot.reserve_price * 1.2, 2)))

        assembly = []
        for name in goods_config.recipes:
            assembly.append(AssemblyOrder(name, 2))

        return Decision(bids=bids, assembly=assembly, listings=listings)
