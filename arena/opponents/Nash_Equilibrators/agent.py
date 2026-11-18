# =============================================================================
#  !!! SPOILER WARNING !!!  ARENA OPPONENT -- DO NOT READ DURING YOUR ATTEMPT.
#  This file is one of the 39 simulated rival teams of the practice hackathon.
#  Reading it tells you how the field plays and spoils the exercise.
# =============================================================================
from dme_simulator.agents import (
    AssemblyOrder, BaseAgent, Bid, Decision, Listing, Observation,
)
from dme_simulator.config import GoodsConfig


PARAMS = {'qty': 2, 'mult': 1.19, 'price': 275.0}


class StarterAgent(BaseAgent):
    def decide(self, state: Observation, goods_config: GoodsConfig) -> Decision:
        return Decision(
            bids=[
                Bid(lot.good, PARAMS["qty"], lot.reserve_price * PARAMS["mult"])
                for lot in state.auction_lots
            ],
            assembly=[
                AssemblyOrder(name, 1) for name in goods_config.recipes
            ],
            listings=[
                Listing(good, 1_000, PARAMS["price"])
                for good in goods_config.finished_goods
            ],
        )
