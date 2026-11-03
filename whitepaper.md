# NEXORA — Whitepaper Working Draft

## Overview
NEXORA is an experimental proof-of-work blockchain project under development. This is a proposed design, not a live network or an investment offer.

## Supply proposal
Maximum supply cap: 30,000,000 NXR:
- 2,000,000 NXR proposed founder allocation (6.6667%).
- Approximately 20,000,000 NXR intended lifetime mining emission (66.6667%).
- 8,000,000 NXR planned unissued ecosystem/reserve allocation (26.6667%).

These allocations are plans, not implemented balances. The current code does not yet create or lock founder/reserve balances or support transfers.

## Proposed mining parameters
Initial block reward: 50 NXR. Halving interval: 200,000 blocks in this working draft. Rewards halve at each interval. The 30,000,000 NXR cap is a ceiling; the emission schedule must be independently tested before protocol freeze.

## Exchange and circulation
NXR will not automatically appear on exchanges. Trading requires an operational network, transferable balances, exchange acceptance, and sellers willing to provide liquidity. No listing, price, profit, or liquidity is guaranteed.

## Development status
The current Python code is an educational prototype. It demonstrates basic hashing, proof-of-work-style nonce search, block linking, and reward accounting. It is not production-ready and lacks signed transactions, secure wallets, persistent storage, peer-to-peer networking, and production consensus.

## Safety
Before a public testnet or mainnet, publish the finalized protocol specification, test vectors, supply calculations, allocation/vesting rules, threat model, and independent security-review results. Never request private keys or seed phrases.
