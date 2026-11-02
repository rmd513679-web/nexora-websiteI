# NEXORA Protocol Notes — Draft v0.2

**Experimental specification only. Not production-ready.**

- Planned maximum supply: 30,000,000 NXR.
- Provisional internal unit: 100,000,000 smallest units per NXR.
- Proposed founder genesis allocation: 2,000,000 NXR, counted within the 30,000,000 cap.
- Proposed founder lock: spending/sale locked initially; duration and unlock schedule not yet decided.
- Remaining planned supply: 28,000,000 NXR, subject to finalized issuance and distribution rules; not automatically all market-released.
- Initial block reward: provisional 50 NXR in current demo code; requires final protocol decision.
- Halving interval: provisional 210,000 blocks in current demo notes; requires final protocol decision.
- Demo PoW: SHA-256 over canonical JSON with low difficulty; educational only.

## Critical implementation gap
The current experimental `blockchain_core.py` does **not** implement a genesis founder allocation or consensus-enforced lock. These notes describe a proposal, not an active lock or a real balance. Do not claim the founder's 2,000,000 NXR has been minted or secured until genesis, transaction/spend validation, lock enforcement, and tests exist.

## Not implemented
User transactions, digital signatures, balances/UTXO model, persistent storage, peer-to-peer networking, production difficulty adjustment, fork-choice rules, mempool, secure wallet/key management, genesis founder allocation, or founder lock enforcement. No real funds should be used.
