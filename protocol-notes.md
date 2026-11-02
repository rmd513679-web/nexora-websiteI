# NEXORA Protocol Notes — Phase 2 Draft

**Experimental specification only.** Parameters are provisional and require review.

- Planned maximum supply: 30,000,000 NXR.
- Internal unit: 100,000,000 smallest units per NXR (provisional).
- Initial block reward: 50 NXR (provisional).
- Halving interval: 210,000 blocks (provisional).
- Demo proof-of-work: SHA-256 over canonical JSON with a low-difficulty leading-zero target.
- Block reward is limited to remaining supply in this prototype.

## Not implemented
No user transactions, signatures, balances, persistent storage, peer-to-peer network, production
difficulty adjustment, fork-choice rules, mempool, or wallet key management. This is not a production
protocol, has not been audited, and must not be used for real funds. The 30-million cap is only
checked by this prototype's reward accounting. Do not describe NEXORA as launched.
