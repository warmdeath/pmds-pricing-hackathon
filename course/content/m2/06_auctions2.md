# 2.6 Auctions II: multi-unit auctions, reserve prices, winner's curse

## The big picture

Many real auctions sell **many identical units at once**: treasury bonds,
electricity, emission permits, commodity lots. Bidders submit several
quantity-price pairs (a **demand schedule**). The rules for **who wins which
units** and **what each winner pays** create distinct strategic problems.
Sellers also add **reserve prices**, and bidders face **budget limits**.

> **Analogy.** A bakery sells its last 20 croissants by sealed offers. Do
> successful customers each pay what they wrote (pay-your-bid) or all pay the
> lowest accepted offer (uniform price)? Customers will write very different
> numbers under the two rules.

## Allocation in multi-unit sealed-bid auctions

Standard rule: sort all unit bids from highest to lowest and fill them until
supply runs out. The lowest accepted bid is the **clearing (stop-out) price**.
If several bids tie at the margin, units are **rationed** (pro-rata, random
order, or round robin). Bids below the **reserve price** are rejected.

*Example.* Supply 10 units, reserve 5. Bids: A 4 units @ 12, B 3 @ 10,
C 5 @ 8, D 6 @ 4. D is below the reserve. Fill: A 4, B 3, C gets the
remaining 3 of its 5. Clearing price 8.

## Payment rules

- **Discriminatory / pay-as-bid / pay-your-bid**: each winner pays **her own
  bid** for each unit won. In the example: A pays 48, B 30, C 24.
- **Uniform price**: every winner pays the clearing price (or highest losing
  bid): A 32, B 24, C 24.
- **Vickrey (multi-unit)**: each winner pays the externality she imposes on
  others; truthful but complex and rare.

## Strategic behaviour

- **Pay-as-bid**: like a first-price auction for each unit — bidders
  **shade** their bids below value, and the optimal bid for each unit trades
  off margin against the probability that the unit is among the winning ones.
  Bidders try to bid "just above the clearing price"; since the clearing price
  is uncertain, bids spread around it. A bid far above the clearing price
  wins the same units as one slightly above it, but pays more.
- **Uniform price**: a bidder's bid on her marginal units can **set** the
  price paid on all her units → **demand reduction** (bidding less for later
  units to lower the clearing price); large bidders can exploit this.
- Empirically, revenue comparisons are ambiguous; many treasuries switched
  between the two (US Treasury moved to uniform price in the 1990s; many
  European treasuries use discriminatory auctions).

## Repeated auctions and information

When the same kind of lot is auctioned every period, bidders observe past
outcomes (what they won, at what price; sometimes the clearing prices) and
update. Each period's clearing price depends on the lot size and on how many
units all bidders demand at each price. Supply that accumulates when unsold
and published reserve prices that move with the seller's stock are features
of some real commodity and procurement markets.

## Reserve prices

A **reserve price** r is the minimum acceptable bid.

- It protects the seller against low competition (few bidders).
- **Myerson's optimal auction**: with independent private values uniform on
  [0, 1] and seller value 0, the revenue-maximising reserve is **r = 1/2**,
  independent of the number of bidders. In general r solves
  r − (1 − F(r))/f(r) = seller's own value.
- From a bidder's perspective, the reserve is a **floor on what you pay** if
  competition is thin, and an exclusion threshold.

## Budget constraints

Bidders often face **budget limits**: they cannot pay more than they hold. If
the auction caps each winner's allocation at what her budget can afford, a
bidder who bids for many items across several simultaneous auctions may find
her budget exhausted by whichever auctions clear first. Budget constraints
break revenue equivalence and make **aggregate demand across lots**, not just
each bid, matter.

## The winner's curse

In **common-value** auctions, each bidder has a noisy estimate of the true
value. The winner is typically the one with the **most optimistic** estimate —
so winning is "bad news" about the value. Bidders who bid their unadjusted
estimate systematically overpay: the **winner's curse** (oil leases in the
1970s, company takeovers).

Rational bidders correct by bidding as if their estimate were the highest
among n: shade more when there are **more** bidders (opposite to the private
value case) and when estimates are noisier.

*Classroom example.* A jar of coins worth €8.00 is auctioned; students'
estimates average €8 but range from 3 to 15. The winning bid is often above
€8 — the winner loses money.

## Summary

- Multi-unit sealed bids: fill from highest to lowest; ration ties; reject
  below reserve.
- Pay-as-bid → shade every unit; uniform → demand reduction.
- Optimal reserve (uniform [0,1] values) = 1/2 regardless of n.
- Budgets break revenue equivalence; common values cause the winner's curse.
