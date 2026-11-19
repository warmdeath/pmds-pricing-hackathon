"""Course structure: 4 modules, 30 lessons."""

MODULES = [
    {"id": "M1", "title": "Microeconomics", "lessons": [
        {"id": "1.1", "title": "Scarcity, opportunity cost and thinking at the margin", "file": "m1/01_foundations.md"},
        {"id": "1.2", "title": "Demand, supply and market equilibrium", "file": "m1/02_supply_demand.md"},
        {"id": "1.3", "title": "Elasticity", "file": "m1/03_elasticity.md"},
        {"id": "1.4", "title": "Welfare, taxes and price controls", "file": "m1/04_welfare.md"},
        {"id": "1.5", "title": "Consumer theory: utility, budgets, willingness to pay", "file": "m1/05_consumer.md"},
        {"id": "1.6", "title": "Production and costs", "file": "m1/06_costs.md"},
        {"id": "1.7", "title": "Perfect competition", "file": "m1/07_competition.md"},
        {"id": "1.8", "title": "Monopoly, market power and price discrimination", "file": "m1/08_monopoly.md"},
        {"id": "1.9", "title": "Product differentiation and discrete-choice demand", "file": "m1/09_differentiation.md"},
        {"id": "1.10", "title": "Market failures and information", "file": "m1/10_market_failures.md"},
    ]},
    {"id": "M2", "title": "Game theory & auctions", "lessons": [
        {"id": "2.1", "title": "Strategic games and Nash equilibrium", "file": "m2/01_games.md"},
        {"id": "2.2", "title": "Mixed strategies and sequential games", "file": "m2/02_mixed_sequential.md"},
        {"id": "2.3", "title": "Oligopoly: Cournot, Bertrand, Stackelberg, collusion", "file": "m2/03_oligopoly.md"},
        {"id": "2.4", "title": "Repeated games, reputation and end-game effects", "file": "m2/04_repeated.md"},
        {"id": "2.5", "title": "Auctions I: formats, values, bid shading", "file": "m2/05_auctions1.md"},
        {"id": "2.6", "title": "Auctions II: multi-unit, reserve prices, winner's curse", "file": "m2/06_auctions2.md"},
        {"id": "2.7", "title": "Decisions under uncertainty: expected value, risk, learning", "file": "m2/07_uncertainty.md"},
    ]},
    {"id": "M3", "title": "Accounting & finance", "lessons": [
        {"id": "3.1", "title": "The balance sheet and double-entry bookkeeping", "file": "m3/01_balance_sheet.md"},
        {"id": "3.2", "title": "The income statement: revenue, costs, margins", "file": "m3/02_income_statement.md"},
        {"id": "3.3", "title": "Cash flow, working capital and inventory", "file": "m3/03_cash_inventory.md"},
        {"id": "3.4", "title": "Managerial accounting: break-even, contribution margin, relevant costs", "file": "m3/04_managerial.md"},
        {"id": "3.5", "title": "Time value of money: PV, FV, NPV, IRR", "file": "m3/05_tvm.md"},
        {"id": "3.6", "title": "Risk, return and diversification", "file": "m3/06_risk_return.md"},
        {"id": "3.7", "title": "Financial markets: bonds, stocks, efficiency, arbitrage", "file": "m3/07_markets.md"},
    ]},
    {"id": "M4", "title": "Macroeconomics", "lessons": [
        {"id": "4.1", "title": "Measuring the economy: GDP, real vs nominal, growth", "file": "m4/01_gdp.md"},
        {"id": "4.2", "title": "Money, inflation and interest rates", "file": "m4/02_inflation.md"},
        {"id": "4.3", "title": "Unemployment and the business cycle", "file": "m4/03_unemployment.md"},
        {"id": "4.4", "title": "Aggregate demand and supply, fiscal policy", "file": "m4/04_ad_as.md"},
        {"id": "4.5", "title": "Central banks and monetary policy", "file": "m4/05_monetary.md"},
        {"id": "4.6", "title": "The open economy: trade and exchange rates", "file": "m4/06_open_economy.md"},
    ]},
]


def all_lessons():
    return [lesson for module in MODULES for lesson in module["lessons"]]


def lesson_by_id(lesson_id):
    return next((lesson for lesson in all_lessons() if lesson["id"] == lesson_id), None)
