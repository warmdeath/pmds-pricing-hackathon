# =============================================================================
#  !!! SPOILER WARNING !!!  ARENA OPPONENT -- DO NOT READ DURING YOUR ATTEMPT.
#  This file is one of the 39 simulated rival teams of the practice hackathon.
#  Reading it tells you how the field plays and spoils the exercise.
# =============================================================================
from dme_simulator.agents import (
    AssemblyOrder, BaseAgent, Bid, Decision, Listing, Observation,
)
from dme_simulator.config import GoodsConfig

from math import ceil

PARAMS = {'bid_start': 1.083, 'bid_up': 1.092, 'bid_max': 3.23, 'budget_share': 0.32, 'ema': 0.353, 'demand_prior': 1.08, 'cover': 1.26, 'buffer': 1, 'up': 0.03, 'down': 0.115, 'low_through': 0.55, 'glut': 3.33, 'glut_cut': 0.017, 'floor': 1.54, 'horizon_guess': True, 'wind_down': 3, 'clearance': 0.839, 'tiers': True}
PRIOR_PRICES = {'LAPTOP': 775.2, 'CONSOLE': 525.7, 'PHONE': 325.8, 'TABLET': 282.1, 'SMARTWATCH': 125.4}


class AdaptiveTrader(BaseAgent):
    """Learns prices from its own sell-through, rations scarce inputs by
    margin per unit of the scarcest material, keeps inventory lean, and
    reads rivals' public inventories."""

    def __init__(self):
        self.price = {}
        self.demand = {}
        self.listed = {}
        self.sales_seen = 0
        self.auction_seen = 0
        self.paid = {}
        self.bid_factor = {}
        self.wanted = {}

    # -- helpers --------------------------------------------------------------
    @staticmethod
    def _cost(recipe, unit_cost):
        return sum(unit_cost.get(m, 0.0) * q for m, q in recipe.inputs.items())

    def _winding_down(self, turn):
        if not PARAMS["horizon_guess"]:
            return False, 0
        for horizon in (40, 80):
            left = horizon - turn
            if 0 <= left < PARAMS["wind_down"]:
                return True, left
        return False, 0

    def decide(self, state: Observation, goods_config: GoodsConfig) -> Decision:
        goods = goods_config.finished_goods
        recipes = goods_config.recipes
        lots = {lot.good: lot for lot in state.auction_lots}

        # 1. digest what happened last turn (own transactions only)
        sold = {}
        for sale in state.sales_transactions[self.sales_seen:]:
            sold[sale.good] = sold.get(sale.good, 0) + sale.quantity
        self.sales_seen = len(state.sales_transactions)
        won = {}
        for buy in state.auction_transactions[self.auction_seen:]:
            won[buy.good] = won.get(buy.good, 0) + buy.quantity
            old = self.paid.get(buy.good, buy.price)
            self.paid[buy.good] = 0.7 * old + 0.3 * buy.price
        self.auction_seen = len(state.auction_transactions)

        # 2. bid aggressiveness follows the fill rate
        for material, wanted in self.wanted.items():
            factor = self.bid_factor.get(material, PARAMS["bid_start"])
            if wanted > 0 and won.get(material, 0) < 0.8 * wanted:
                factor = min(PARAMS["bid_max"], factor * PARAMS["bid_up"])
            else:
                factor = max(1.01, factor * 0.97)
            self.bid_factor[material] = factor

        unit_cost = {}
        for material in goods_config.raw_materials:
            reserve = lots[material].reserve_price if material in lots else 0.0
            unit_cost[material] = max(reserve * self.bid_factor.get(material, PARAMS["bid_start"]),
                                      self.paid.get(material, 0.0))
        cost = {r.output_good: self._cost(r, unit_cost) for r in recipes.values()}

        # 3. rivals' stock of each finished good (public inventories)
        total_stock = {g: 0 for g in goods}
        for inventory in state.public_inventories.values():
            for g in goods:
                total_stock[g] += inventory.get(g, 0)
        rivals = max(1, len(state.public_inventories) - 1)
        rival_stock = {g: (total_stock[g] - state.inventory.get(g, 0)) / rivals for g in goods}

        # 4. learn prices from sell-through
        for g in goods:
            if g not in self.price:
                self.price[g] = PRIOR_PRICES.get(g, cost.get(g, 50.0) * 4)
                self.demand[g] = PARAMS["demand_prior"]
            self.demand[g] = (1 - PARAMS["ema"]) * self.demand[g] + PARAMS["ema"] * sold.get(g, 0)
            listed = self.listed.get(g, 0)
            if listed > 0:
                through = sold.get(g, 0) / listed
                if through >= 0.999:
                    self.price[g] *= 1.0 + PARAMS["up"]
                elif through < PARAMS["low_through"]:
                    self.price[g] *= 1.0 - PARAMS["down"] * (1.0 - through)
            if rival_stock[g] > PARAMS["glut"]:
                self.price[g] *= 1.0 - PARAMS["glut_cut"]
            self.price[g] = max(self.price[g], cost.get(g, 0.0) * PARAMS["floor"])

        winding, left = self._winding_down(state.turn)

        # 5. plan production: margin per unit of the scarcest input
        scarcity = {}
        for material in goods_config.raw_materials:
            offered = lots[material].quantity if material in lots else 0
            scarcity[material] = 1.0 / max(1.0, offered)
        scarcest = max(scarcity, key=scarcity.get) if scarcity else None
        ranked = []
        for name, recipe in recipes.items():
            g = recipe.output_good
            margin = self.price[g] - cost.get(g, 0.0)
            per = recipe.inputs.get(scarcest, 0) or sum(recipe.inputs.values())
            ranked.append((margin / per, name, recipe))
        ranked.sort(key=lambda item: -item[0])

        plan = {}
        needs = {}
        if not winding:
            budget = state.capital * PARAMS["budget_share"]
            spent = 0.0
            for score, name, recipe in ranked:
                if score <= 0:
                    continue
                g = recipe.output_good
                target = ceil(self.demand[g] * PARAMS["cover"]) + PARAMS["buffer"]
                if rival_stock[g] > PARAMS["glut"]:
                    target = max(0, target - 1)
                units = max(0, target - state.inventory.get(g, 0))
                unit_spend = cost.get(g, 0.0)
                if unit_spend > 0:
                    units = min(units, int(max(0.0, budget - spent) // unit_spend))
                if units <= 0:
                    continue
                plan[name] = units
                spent += units * unit_spend
                for m, q in recipe.inputs.items():
                    needs[m] = needs.get(m, 0) + q * units

        bids = []
        self.wanted = {}
        for material, units in needs.items():
            missing = units - state.inventory.get(material, 0)
            if material not in lots or missing <= 0:
                continue
            lot = lots[material]
            price = lot.reserve_price * self.bid_factor.get(material, PARAMS["bid_start"])
            qty = min(missing, lot.quantity)
            if qty > 0:
                bids.append(Bid(material, int(qty), round(price, 2)))
                self.wanted[material] = qty

        assembly = [AssemblyOrder(name, units) for name, units in plan.items()]

        # 6. listings; clear stock while winding down
        listings = []
        self.listed = {}
        for name, recipe in recipes.items():
            g = recipe.output_good
            have = state.inventory.get(g, 0)
            qty = have + plan.get(name, 0)
            if qty <= 0:
                continue
            price = self.price[g]
            if winding:
                price = max(cost.get(g, 0.0) * 1.05,
                            price * (PARAMS["clearance"] ** (PARAMS["wind_down"] - left)))
            if PARAMS["tiers"] and qty >= 2:
                high = qty // 2
                listings.append(Listing(g, high, round(price * 1.08, 2)))
                listings.append(Listing(g, qty - high, round(price * 0.95, 2)))
            else:
                listings.append(Listing(g, qty, round(price, 2)))
            self.listed[g] = max(1, have)
        return Decision(bids=bids, assembly=assembly, listings=listings)
