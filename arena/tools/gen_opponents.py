#!/usr/bin/env python3
# =============================================================================
#  !!! SPOILER WARNING !!!
#  This file generates the 39 arena opponents and contains every opponent's
#  strategy and parameters. Do NOT read it during your practice attempt.
# =============================================================================
"""Generate arena/opponents/<team>/agent.py for the 39 practice opponents.

Run from the repository root:  uv run python arena/tools/gen_opponents.py
Output is deterministic (fixed RNG seed), so regenerating is a no-op.
"""

from __future__ import annotations

import random
import shutil
from pathlib import Path

ROOT = Path(__file__).resolve().parents[2]
OUT = ROOT / "arena" / "opponents"
RNG = random.Random(20260514)

HEADER = '''# =============================================================================
#  !!! SPOILER WARNING !!!  ARENA OPPONENT -- DO NOT READ DURING YOUR ATTEMPT.
#  This file is one of the 39 simulated rival teams of the practice hackathon.
#  Reading it tells you how the field plays and spoils the exercise.
# =============================================================================
'''

IMPORTS = '''from dme_simulator.agents import (
    AssemblyOrder, BaseAgent, Bid, Decision, Listing, Observation,
)
from dme_simulator.config import GoodsConfig
'''

# Reference price table a team could derive by reading config/default.yaml.
PRIOR = {"LAPTOP": 760.0, "CONSOLE": 560.0, "PHONE": 300.0, "TABLET": 300.0,
         "SMARTWATCH": 130.0}

TEAM_NAMES = [
    "Overfit_Owls", "Pasta_Pricers", "Lambda_Llamas", "Supply_Side_Story",
    "Bid_and_Breakfast", "Spaghetti_Code", "Navigli_Nerds", "Risotto_Robots",
    "Sold_Out_Crew", "Deep_Pockets", "Bayes_Watch", "Monte_Carlo_Mafia",
    "Pareto_Pirates", "Nash_Equilibrators", "Markov_Chainsaw", "Cache_Money",
    "Poli_Traders", "Elasticity_Squad", "Last_Minute_Commit", "Git_Push_Force",
    "Coffee_Driven_Dev", "Milano_Hackers", "Bit_Bandits", "Team_404",
    "Quanti_Bros", "Margin_Mavericks", "Silicon_Sheep", "Greedy_Algorithms",
    "Dynamic_Duo", "Kernel_Panic", "Segfault_Society", "Byte_Me",
    "Gradient_Descenders", "Tensor_Tigers", "Loss_Function", "Brera_Bytes",
    "Ticinese_Traders", "Null_Pointers", "Stack_Overflowers",
]
assert len(TEAM_NAMES) == 39 and len(set(TEAM_NAMES)) == 39


def r(lo, hi, nd=3):
    return round(RNG.uniform(lo, hi), nd)


def perturbed_prior(lo, hi):
    return {g: round(p * RNG.uniform(lo, hi), 1) for g, p in PRIOR.items()}


# =============================================================================
# WEAK archetypes
# =============================================================================

W_STARTER = '''

PARAMS = %PARAMS%


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
'''

W_FLAT = '''

PARAMS = %PARAMS%


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
'''

W_OVERBID = '''

PARAMS = %PARAMS%

# Premium positioning: we are a quality brand!
PREMIUM_PRICES = %PRICES%


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
'''

W_KEEPER = '''

PARAMS = %PARAMS%
PRICES = %PRICES%


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
'''

W_QTYBUG = '''

PARAMS = %PARAMS%


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
'''

W_RESET = '''

PARAMS = %PARAMS%
START_PRICES = %PRICES%


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
'''

W_CHEAP = '''

PARAMS = %PARAMS%


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
'''

W_TABLET = '''

PARAMS = %PARAMS%

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
'''

# =============================================================================
# MEDIUM archetypes
# =============================================================================

M_COMMON = '''

def recipe_cost(recipe, unit_cost):
    return sum(unit_cost.get(m, 0.0) * q for m, q in recipe.inputs.items())


def plan_bids(state, needs, markup, budget):
    """Bid for missing materials at reserve * markup, scaled to a budget."""
    lots = {lot.good: lot for lot in state.auction_lots}
    wanted = {}
    for material, units in needs.items():
        missing = units - state.inventory.get(material, 0)
        if material in lots and missing > 0:
            wanted[material] = min(missing, lots[material].quantity)
    cost = sum(lots[m].reserve_price * markup * q for m, q in wanted.items())
    scale = 1.0 if cost <= budget or cost <= 0 else budget / cost
    bids = []
    for material, units in wanted.items():
        qty = int(units * scale)
        if qty > 0:
            bids.append(Bid(material, qty, round(lots[material].reserve_price * markup, 2)))
    return bids
'''

M_FIXED = '''

PARAMS = %PARAMS%
PRICES = %PRICES%
''' + M_COMMON + '''

class FixedPriceAgent(BaseAgent):
    """Sensible fixed price list, steady production, budget discipline."""

    def decide(self, state: Observation, goods_config: GoodsConfig) -> Decision:
        unit_cost = {lot.good: lot.reserve_price * PARAMS["markup"] for lot in state.auction_lots}
        plan = {}
        needs = {}
        for name, recipe in goods_config.recipes.items():
            good = recipe.output_good
            price = PRICES.get(good, 0.0)
            if price <= recipe_cost(recipe, unit_cost) * 1.5:
                continue
            target = PARAMS["target"].get(good, 1)
            units = max(0, target - state.inventory.get(good, 0))
            if units > 0:
                plan[name] = units
                for m, q in recipe.inputs.items():
                    needs[m] = needs.get(m, 0) + q * units
        bids = plan_bids(state, needs, PARAMS["markup"], state.capital * PARAMS["budget_share"])
        assembly = [AssemblyOrder(name, units) for name, units in plan.items()]
        listings = []
        for name, recipe in goods_config.recipes.items():
            good = recipe.output_good
            qty = state.inventory.get(good, 0) + plan.get(name, 0)
            if qty > 0 and good in PRICES:
                listings.append(Listing(good, qty, PRICES[good]))
        return Decision(bids=bids, assembly=assembly, listings=listings)
'''

M_REACTIVE = '''

PARAMS = %PARAMS%
START_PRICES = %PRICES%
''' + M_COMMON + '''

class ReactivePricer(BaseAgent):
    """Raise the price when a product sells out, cut it when nothing sells."""

    def __init__(self):
        self.prices = dict(START_PRICES)
        self.listed = {}
        self.sales_seen = 0

    def decide(self, state: Observation, goods_config: GoodsConfig) -> Decision:
        sold = {}
        for sale in state.sales_transactions[self.sales_seen:]:
            sold[sale.good] = sold.get(sale.good, 0) + sale.quantity
        self.sales_seen = len(state.sales_transactions)

        unit_cost = {lot.good: lot.reserve_price * PARAMS["markup"] for lot in state.auction_lots}
        costs = {r.output_good: recipe_cost(r, unit_cost) for r in goods_config.recipes.values()}

        for good, listed in self.listed.items():
            if listed <= 0:
                continue
            if sold.get(good, 0) >= listed:
                self.prices[good] *= 1.0 + PARAMS["up"]
            elif sold.get(good, 0) == 0:
                self.prices[good] *= 1.0 - PARAMS["down"]
            floor = costs.get(good, 0.0) * PARAMS["floor"]
            self.prices[good] = max(self.prices[good], floor)

        plan = {}
        needs = {}
        for name, recipe in goods_config.recipes.items():
            good = recipe.output_good
            if good not in self.prices:
                self.prices[good] = costs.get(good, 50.0) * 4
            units = max(0, PARAMS["target"] - state.inventory.get(good, 0))
            if units > 0:
                plan[name] = units
                for m, q in recipe.inputs.items():
                    needs[m] = needs.get(m, 0) + q * units
        bids = plan_bids(state, needs, PARAMS["markup"], state.capital * PARAMS["budget_share"])
        assembly = [AssemblyOrder(name, units) for name, units in plan.items()]

        listings = []
        self.listed = {}
        for name, recipe in goods_config.recipes.items():
            good = recipe.output_good
            qty = state.inventory.get(good, 0) + plan.get(name, 0)
            if qty > 0:
                listings.append(Listing(good, qty, round(self.prices[good], 2)))
                # count only what we already hold; planned units may not be built
                self.listed[good] = max(1, state.inventory.get(good, 0))
        return Decision(bids=bids, assembly=assembly, listings=listings)
'''

M_PRICEWAR = '''

PARAMS = %PARAMS%
START_PRICES = %PRICES%
''' + M_COMMON + '''

class UndercutAgent(BaseAgent):
    """Sell under the last price we achieved; volume beats margin."""

    def __init__(self):
        self.prices = {}
        self.sales_seen = 0

    def decide(self, state: Observation, goods_config: GoodsConfig) -> Decision:
        last_price = {}
        sold = {}
        for sale in state.sales_transactions[self.sales_seen:]:
            last_price[sale.good] = sale.price
            sold[sale.good] = sold.get(sale.good, 0) + sale.quantity
        self.sales_seen = len(state.sales_transactions)

        unit_cost = {lot.good: lot.reserve_price * PARAMS["markup"] for lot in state.auction_lots}
        costs = {r.output_good: recipe_cost(r, unit_cost) for r in goods_config.recipes.values()}

        for good in goods_config.finished_goods:
            current = self.prices.get(good, START_PRICES.get(good, costs.get(good, 50.0) * 4))
            stock = state.inventory.get(good, 0)
            if good in last_price and stock == 0:
                current = last_price[good] * (1.0 + PARAMS["bounce"])
            elif good in last_price:
                current = last_price[good] * (1.0 - PARAMS["undercut"])
            elif stock > 0 and state.turn > 1:
                current *= 1.0 - PARAMS["undercut"]
            self.prices[good] = max(current, costs.get(good, 0.0) * PARAMS["floor"])

        plan = {}
        needs = {}
        for name, recipe in goods_config.recipes.items():
            units = max(0, PARAMS["target"] - state.inventory.get(recipe.output_good, 0))
            if units > 0:
                plan[name] = units
                for m, q in recipe.inputs.items():
                    needs[m] = needs.get(m, 0) + q * units
        bids = plan_bids(state, needs, PARAMS["markup"], state.capital * PARAMS["budget_share"])
        assembly = [AssemblyOrder(name, units) for name, units in plan.items()]
        listings = []
        for name, recipe in goods_config.recipes.items():
            good = recipe.output_good
            qty = state.inventory.get(good, 0) + plan.get(name, 0)
            if qty > 0:
                listings.append(Listing(good, qty, round(self.prices[good], 2)))
        return Decision(bids=bids, assembly=assembly, listings=listings)
'''

M_HOARDER = '''

PARAMS = %PARAMS%
PRICES = %PRICES%
''' + M_COMMON + '''

class StockpileAgent(BaseAgent):
    """Corner the materials early, then sell at premium prices."""

    def __init__(self):
        self.prices = dict(PRICES)
        self.sales_seen = 0

    def decide(self, state: Observation, goods_config: GoodsConfig) -> Decision:
        sold = {}
        for sale in state.sales_transactions[self.sales_seen:]:
            sold[sale.good] = sold.get(sale.good, 0) + sale.quantity
        self.sales_seen = len(state.sales_transactions)

        early = state.turn <= PARAMS["hoard_turns"]
        bids = []
        if early:
            budget = state.capital * PARAMS["hoard_budget"]
            per_lot = budget / max(1, len(state.auction_lots))
            for lot in state.auction_lots:
                price = lot.reserve_price * PARAMS["hoard_markup"]
                qty = min(lot.quantity, int(per_lot // price)) if price > 0 else 0
                if qty > 0:
                    bids.append(Bid(lot.good, qty, round(price, 2)))
        else:
            needs = {}
            for recipe in goods_config.recipes.values():
                for m, q in recipe.inputs.items():
                    needs[m] = needs.get(m, 0) + q * PARAMS["target"]
            bids = plan_bids(state, needs, 1.15, state.capital * 0.2)

        for good in goods_config.finished_goods:
            if good not in self.prices:
                self.prices[good] = 300.0
            if state.inventory.get(good, 0) > 6 and sold.get(good, 0) == 0:
                self.prices[good] *= 1.0 - PARAMS["down"]

        assembly = [AssemblyOrder(name, PARAMS["build"]) for name in goods_config.recipes]
        listings = []
        for recipe in goods_config.recipes.values():
            good = recipe.output_good
            qty = state.inventory.get(good, 0) + PARAMS["build"]
            listings.append(Listing(good, qty, round(self.prices[good], 2)))
        return Decision(bids=bids, assembly=assembly, listings=listings)
'''

M_FOCUSED = '''

PARAMS = %PARAMS%
START_PRICES = %PRICES%
''' + M_COMMON + '''

class NicheAgent(BaseAgent):
    """Specialise in a few products and price them carefully."""

    def __init__(self):
        self.prices = dict(START_PRICES)
        self.listed = {}
        self.sales_seen = 0

    def decide(self, state: Observation, goods_config: GoodsConfig) -> Decision:
        sold = {}
        for sale in state.sales_transactions[self.sales_seen:]:
            sold[sale.good] = sold.get(sale.good, 0) + sale.quantity
        self.sales_seen = len(state.sales_transactions)
        for good, listed in self.listed.items():
            if sold.get(good, 0) >= listed:
                self.prices[good] *= 1.0 + PARAMS["up"]
            elif sold.get(good, 0) == 0:
                self.prices[good] *= 1.0 - PARAMS["down"]

        unit_cost = {lot.good: lot.reserve_price * PARAMS["markup"] for lot in state.auction_lots}
        focus = [g for g in PARAMS["focus"] if g in goods_config.finished_goods]
        if not focus:
            focus = list(goods_config.finished_goods)
        plan = {}
        needs = {}
        for name, recipe in goods_config.recipes.items():
            good = recipe.output_good
            if good not in focus:
                continue
            cost = recipe_cost(recipe, unit_cost)
            self.prices[good] = max(self.prices.get(good, cost * 4), cost * 1.5)
            units = max(0, PARAMS["target"] - state.inventory.get(good, 0))
            if units > 0:
                plan[name] = units
                for m, q in recipe.inputs.items():
                    needs[m] = needs.get(m, 0) + q * units
        bids = plan_bids(state, needs, PARAMS["markup"], state.capital * PARAMS["budget_share"])
        assembly = [AssemblyOrder(name, units) for name, units in plan.items()]
        listings = []
        self.listed = {}
        for name, recipe in goods_config.recipes.items():
            good = recipe.output_good
            qty = state.inventory.get(good, 0) + plan.get(name, 0)
            if qty > 0 and good in self.prices:
                listings.append(Listing(good, qty, round(self.prices[good], 2)))
                self.listed[good] = max(1, state.inventory.get(good, 0))
        return Decision(bids=bids, assembly=assembly, listings=listings)
'''

# =============================================================================
# STRONG archetype
# =============================================================================

S_ADAPTIVE = '''
from math import ceil

PARAMS = %PARAMS%
PRIOR_PRICES = %PRICES%


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
'''


# =============================================================================
# roster
# =============================================================================

def weak_specs():
    specs = []
    for price in (250.0, 199.0, 300.0, 275.0):
        specs.append(("weak", "starter", W_STARTER, {
            "qty": RNG.choice([1, 1, 2]), "mult": r(1.05, 1.3, 2), "price": price}, None))
    for _ in range(3):
        specs.append(("weak", "flat", W_FLAT, {
            "per_recipe": RNG.choice([1, 2]), "mult": r(1.1, 1.5, 2),
            "flat_price": float(RNG.choice([350, 399, 450, 499, 550]))}, None))
    for _ in range(3):
        specs.append(("weak", "overbid", W_OVERBID, {
            "qty": RNG.randint(10, 25), "overbid": r(2.5, 5.0, 2)},
            perturbed_prior(1.45, 1.8)))
    for _ in range(2):
        specs.append(("weak", "keeper", W_KEEPER, {
            "build_per_turn": RNG.choice([1, 2]), "mult": r(1.2, 1.4, 2),
            "keep": RNG.randint(2, 4)}, perturbed_prior(0.9, 1.15)))
    specs.append(("weak", "qtybug", W_QTYBUG, {"markup": r(1.3, 1.8, 2), "qty": 3}, None))
    specs.append(("weak", "reset", W_RESET, {
        "budget_share": r(0.08, 0.15, 2), "mult": r(1.1, 1.3, 2), "build": 2},
        perturbed_prior(1.1, 1.4)))
    specs.append(("weak", "cheap", W_CHEAP, {"mult": r(1.1, 1.2, 2), "markup": r(1.4, 1.7, 2)}, None))
    specs.append(("weak", "tablet", W_TABLET, {
        "qty": 3, "mult": r(1.2, 1.4, 2), "price": float(RNG.choice([420, 450, 480]))}, None))
    return specs


def target_table(lo, hi):
    return {g: RNG.randint(lo, hi) for g in PRIOR}


def medium_specs():
    specs = []
    for _ in range(4):
        specs.append(("medium", "fixed", M_FIXED, {
            "markup": r(1.15, 1.5, 2), "budget_share": r(0.15, 0.35, 2),
            "target": target_table(1, 3)}, perturbed_prior(0.8, 1.1)))
    for _ in range(5):
        specs.append(("medium", "reactive", M_REACTIVE, {
            "markup": r(1.15, 1.5, 2), "budget_share": r(0.15, 0.3, 2),
            "target": RNG.randint(2, 3), "up": r(0.03, 0.08), "down": r(0.04, 0.1),
            "floor": r(1.4, 2.0, 2)}, perturbed_prior(0.85, 1.15)))
    for _ in range(3):
        specs.append(("medium", "pricewar", M_PRICEWAR, {
            "markup": r(1.2, 1.6, 2), "budget_share": r(0.2, 0.35, 2),
            "target": RNG.randint(2, 4), "undercut": r(0.03, 0.08),
            "bounce": r(0.02, 0.05), "floor": r(1.3, 1.8, 2)}, perturbed_prior(0.75, 0.95)))
    for _ in range(2):
        specs.append(("medium", "hoarder", M_HOARDER, {
            "hoard_turns": RNG.randint(8, 14), "hoard_budget": r(0.3, 0.5, 2),
            "hoard_markup": r(1.3, 1.7, 2), "target": 1, "build": RNG.randint(2, 4),
            "down": r(0.03, 0.06)}, perturbed_prior(1.05, 1.3)))
    for focus in (["LAPTOP", "CONSOLE"], ["SMARTWATCH", "PHONE", "TABLET"]):
        specs.append(("medium", "focused", M_FOCUSED, {
            "focus": focus, "markup": r(1.2, 1.5, 2), "budget_share": r(0.2, 0.35, 2),
            "target": RNG.randint(3, 5), "up": r(0.03, 0.07), "down": r(0.04, 0.08)},
            perturbed_prior(0.85, 1.1)))
    return specs


def strong_specs():
    specs = []
    for i in range(7):
        specs.append(("strong", "adaptive", S_ADAPTIVE, {
            "bid_start": r(1.05, 1.25), "bid_up": r(1.05, 1.15), "bid_max": r(2.0, 3.5, 2),
            "budget_share": r(0.25, 0.45, 2), "ema": r(0.2, 0.4), "demand_prior": r(0.8, 1.5, 2),
            "cover": r(1.0, 1.6, 2), "buffer": RNG.choice([0, 1]),
            "up": r(0.03, 0.07), "down": r(0.05, 0.12), "low_through": r(0.4, 0.6, 2),
            "glut": r(2.0, 4.0, 2), "glut_cut": r(0.01, 0.03),
            "floor": r(1.3, 1.8, 2), "horizon_guess": i % 3 != 2,
            "wind_down": RNG.randint(3, 5), "clearance": r(0.8, 0.9),
            "tiers": i % 2 == 0}, perturbed_prior(0.9, 1.1)))
    return specs


def render(template, params, prices):
    body = template.replace("%PARAMS%", repr(params))
    if "%PRICES%" in body:
        body = body.replace("%PRICES%", repr(prices or {}))
    return HEADER + IMPORTS + body


def main():
    specs = weak_specs() + medium_specs() + strong_specs()
    assert len(specs) == 39, len(specs)
    names = list(TEAM_NAMES)
    RNG.shuffle(names)
    for child in OUT.iterdir() if OUT.exists() else []:
        if child.is_dir():
            shutil.rmtree(child)
    OUT.mkdir(parents=True, exist_ok=True)
    roster = []
    for name, (tier, kind, template, params, prices) in zip(names, specs):
        folder = OUT / name
        folder.mkdir()
        (folder / "agent.py").write_text(render(template, params, prices), encoding="utf-8")
        roster.append((name, tier, kind))
    # spoiler roster for maintainers/tests only
    lines = [HEADER, "ROSTER = {\n"]
    for name, tier, kind in sorted(roster):
        lines.append(f"    {name!r}: ({tier!r}, {kind!r}),\n")
    lines.append("}\n")
    (ROOT / "arena" / "tools" / "roster_spoiler.py").write_text("".join(lines), encoding="utf-8")
    print(f"wrote {len(roster)} opponents to {OUT}")


if __name__ == "__main__":
    main()
