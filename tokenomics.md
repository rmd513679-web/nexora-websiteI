# NEXORA Tokenomics — Draft v0.2

All figures below are planning targets, not live balances or deployed consensus rules.

## Supply plan
- Planned maximum supply: **30,000,000 NXR**.
- Smallest unit: **100,000,000 units per NXR** (provisional).
- Founder allocation: **2,000,000 NXR (6.6667%)**, proposed for a designated founder wallet at genesis and initially locked against spending/sale.
- Remaining planned supply: **28,000,000 NXR (93.3333%)** for block issuance and any other disclosed distributions. It is not all automatically released to the market at launch.
- Founder lock duration and release method: **not yet decided**.
- Initial block reward, halving interval, transaction fees, and exact issuance formula: provisional/not finalized.

## Required accounting rules
1. Founder allocation is included inside the 30,000,000 NXR cap, never added on top.
2. Use integer smallest units; do not use floating-point amounts in consensus code.
3. Genesis outputs plus cumulative rewards and every other issuance path must remain at or below 3,000,000,000,000,000 smallest units.
4. Define what happens when remaining supply is less than a scheduled reward.
5. Implement a consensus-enforced lock; a written allocation alone does not prevent spending.
6. Test edge cases, unlock boundaries, invalid spends, and supply-cap invariants before launch.

## Transparency
Publish the founder wallet/address and lock terms before launch, with appropriate privacy/security care. Do not imply that an address or allocation has been created until verified. Do not promise price, profit, exchange listing, or mining income.
