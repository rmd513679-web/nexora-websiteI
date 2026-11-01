# NEXORA Whitepaper
## Draft v0.1 — 1 November 2026

**Status:** Proposal for discussion. This document does not represent a launched blockchain,
an audited protocol, a guaranteed investment, or a promise of value.

## Abstract
NEXORA is a proposed independent blockchain using Proof of Work (PoW) to order blocks and
coordinate agreement among network participants. The current design target is a maximum supply
of 30,000,000 NEXORA. The consensus rules, issuance schedule, networking layer, transaction
system, wallet software and security properties remain under development.

## 1. Goals
- Provide a transparent, independently verifiable ledger.
- Use publicly specified rules for block production and coin issuance.
- Make software and protocol changes reviewable.
- Avoid representing unbuilt features as live functionality.

## 2. Current status
At the time of this draft, the project has a landing-page concept and starter documentation.
A production-grade chain, public testnet, mainnet, wallet, explorer, exchange listing, and mining
pool are **not confirmed as existing**. The educational prototype in this repository is not a
production blockchain.

## 3. Proposed monetary policy
- Planned maximum supply: **30,000,000 NEXORA**.
- Consensus concept: Proof of Work.
- Issuance: newly issued coins may be paid as block rewards, subject to final consensus rules.
- Halving: a possible mechanism, but interval and exact schedule have not been decided.
- Premine/genesis allocation: not specified in this draft; must be disclosed before launch.
- Fees: not specified; a future protocol specification must define their handling.

The maximum supply is only a design goal until the consensus implementation enforces it. Any
final reward schedule must be mathematically checked so total issuance never exceeds the cap,
including rounding and edge cases.

## 4. Proof of Work (concept)
A miner assembles candidate block data and searches for a nonce such that the block hash satisfies
the network's difficulty target. Nodes independently verify the proof and all other consensus
rules. Difficulty adjustment, target encoding, hash algorithm, timestamp bounds, and fork-choice
rules are undecided and must be specified and tested before a testnet launch.

PoW does not by itself make a system secure. Security depends on network participation,
implementation correctness, economic assumptions, and resistance to attacks and bugs.

## 5. Block and transaction model (planned)
A future block is expected to contain a version, previous-block hash, timestamp, transaction
commitment, nonce, difficulty target and reward information. The exact serialization and hash
algorithm must be canonical so every node computes identical results.

Transactions will need authenticated authorization, replay protection, fee rules, and validation
against the current ledger state. No production transaction format is defined yet.

## 6. Network architecture (planned)
A complete implementation needs:
- Node software and peer discovery
- Message framing, peer limits and abuse protection
- Block and transaction propagation
- Initial synchronization and chain reorganization rules
- Persistent storage and recovery
- Observability, logs and release/version management

These components are not included in the educational prototype.

## 7. Wallet and key safety (planned)
A wallet must securely generate and store private keys, sign transactions, and display clear
backup/recovery warnings. Private keys and recovery phrases must never be uploaded to GitHub,
sent to support staff, or embedded in source code. Wallet software should receive a separate
security review.

## 8. Governance and upgrades
Protocol changes should be proposed publicly, documented, reviewed, tested, and released with
clear versioning. The final governance process and project stewardship model are not yet defined.

## 9. Risks and limitations
Risks include software defects, consensus splits, low mining participation, network attacks,
key loss, privacy leakage, regulatory uncertainty, and market volatility. NEXORA makes no promise
of price, profits, liquidity, exchange listing, or future adoption. Do not invest money based on
this draft.

## 10. Roadmap
1. **Specification:** settle monetary policy and consensus parameters.
2. **Prototype:** local educational implementation and unit tests.
3. **Private testnet:** multiple nodes, deterministic test vectors, adversarial testing.
4. **Public testnet:** published binaries/source, explorer, bug-report process and monitoring.
5. **Audit and launch review:** independent security audit, legal review, documented launch plan.
6. **Mainnet consideration:** only after public review and consensus-critical tests pass.

No date is promised for any milestone.

## 11. Open questions
Before implementation can be considered complete, the project must decide:
- Hash algorithm and block interval
- Initial difficulty and adjustment algorithm
- Block reward, halving interval and final issuance rounding
- Smallest unit / decimal precision
- Transaction and signature formats
- Fee policy and unspent-output/account model
- Fork-choice and reorganization limits
- Genesis block and any allocation
- Node networking, storage and software release process

## Disclaimer
This is a draft for software development and discussion, not financial, legal, tax, or investment
advice. The starter repository is experimental software and must not be used to secure real value.
