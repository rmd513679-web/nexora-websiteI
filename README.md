# NEXORA — Native Proof-of-Work Blockchain (Starter)

> **Status: experimental prototype / draft. Not production-ready.**
>
> This repository is a starting point for research and testnet development. It is not audited,
> does not provide a wallet or peer-to-peer network, and must not be used to hold real funds.

## Project plan
- Native coin on a planned independent blockchain
- Planned maximum supply: **30,000,000 NEXORA**
- Consensus concept: Proof of Work (PoW)
- Initial milestone: documentation + a small educational single-process prototype

## Repository map
- `whitepaper.md` — draft whitepaper
- `docs/tokenomics.md` — proposed issuance parameters and decisions still needed
- `docs/roadmap.md` — staged development roadmap
- `nexora/prototype.py` — educational block/hash/PoW demonstration
- `tests/test_prototype.py` — basic tests
- `index.html` — simple project landing page

## Important design decisions still open
1. Coin precision / smallest unit
2. Block interval and difficulty adjustment
3. Reward schedule and halving interval
4. Genesis allocation (recommended: none until transparently specified)
5. Transaction format, signatures, fee rules and mempool
6. Peer-to-peer networking and chain synchronization
7. Reorganization rules, anti-spam protections and denial-of-service limits
8. Independent security review and legal review

The 30,000,000 figure is a **planned cap**, not an implemented guarantee in this starter.
A production implementation must enforce the cap in consensus rules and pass adversarial tests.

## Run the educational prototype
Requires Python 3.10+ on a computer or a compatible Android Python environment.

```bash
python -m unittest discover -s tests -v
python -m nexora.prototype
```

This prototype mines toy blocks locally. It is **not a complete blockchain**, does not validate
real transactions, and does not connect to a network.

## Suggested next milestones
1. Agree and publish the whitepaper parameters.
2. Build a formal protocol specification and test vectors.
3. Implement transaction signatures and consensus validation.
4. Build a local multi-node testnet.
5. Add wallets only after key handling and transaction rules are reviewed.
6. Conduct independent security review before any public launch.
