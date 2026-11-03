# NEXORA Protocol Notes — Experimental

## Draft constants
- 100,000,000 smallest units per NXR.
- Maximum cap: 30,000,000 NXR.
- Initial reward: 50 NXR.
- Working-draft halving interval: 200,000 blocks.
- Demo proof-of-work difficulty is only for local educational tests.

## Reward rule
For height h >= 1, nominal reward = INITIAL_REWARD >> ((h - 1) // HALVING_INTERVAL), limited by remaining room under the 30M cap. Rewards stop when the nominal reward becomes zero in smallest units.

## Allocation not yet implemented
The proposed 2M founder allocation and 8M reserve are policy intentions only. The current prototype tracks mining issuance only; it does not implement genesis allocation, locked balances, vesting, or reserve governance.

## Limitations
The demo has no transaction validation, persistent state, production difficulty adjustment, or production consensus. Do not use it for real funds.
