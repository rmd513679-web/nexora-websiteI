# NEXORA Whitepaper
## Draft v0.2 — 2 November 2026

**Status:** Proposal only. NEXORA has not been confirmed as launched. This document is not an investment offer, a promise of value, or evidence that a production blockchain exists.

## 1. Abstract
NEXORA is a proposed independent blockchain using Proof of Work (PoW). Its planning target is a maximum supply of 30,000,000 NXR. The protocol, transaction system, wallet, peer-to-peer network, and security model remain under development.

## 2. Project goals
- Publish transparent, independently verifiable consensus and issuance rules.
- Use integer arithmetic in the smallest unit for all consensus amounts.
- Make source code and changes reviewable.
- Clearly distinguish prototypes from production software.

## 3. Planned monetary parameters
- Maximum supply: **30,000,000 NXR** (planning target).
- Smallest unit: **1 NXR = 100,000,000 units** (provisional).
- Consensus: Proof of Work (proposed).
- Block reward and halving interval: provisional; must be finalized and tested before launch.
- Founder allocation: **2,000,000 NXR (6.6667% of the planned cap)**, intended to be assigned to a designated founder wallet at genesis and locked against spending/sale for an initial period.
- Remaining planned supply: **28,000,000 NXR** for issuance and other distributions under rules that must be published before launch. This does not mean all 28 million will be immediately released to a market.

## 4. Founder allocation and lock
The proposed founder allocation is 2,000,000 NXR. The allocation must be disclosed before launch and assigned to a clearly identified wallet or genesis output. A consensus-enforced lock is preferred; an informal promise or website statement is not sufficient. The lock duration, unlock schedule, and whether release is gradual or all-at-once are **not yet decided**. No implementation should be described as active until code, tests, and independent review verify it.

## 5. Supply accounting
With 100,000,000 smallest units per NXR, the planned cap corresponds to 3,000,000,000,000,000 smallest units. All amounts must be integers. Tests must verify that genesis allocation plus all issued block rewards and any other coin-creation paths never exceed the cap. The founder allocation must count toward—not be added on top of—the 30 million cap.

## 6. Proof of Work
PoW is a design goal, not yet a production-ready network. A usable protocol still needs a defined block format, target/difficulty adjustment, validation rules, fork-choice rule, networking, persistence, and adversarial testing. A low-difficulty single-process demonstration is not sufficient for launch.

## 7. Status and limitations
Current repository files are experimental starter code and documentation. A public testnet, mainnet, secure wallet, explorer, peer-to-peer network, production mining, audit, or exchange listing is not established by these files. Do not use this prototype to hold real funds or claim guaranteed mining income or market value.

## 8. Pre-launch requirements
1. Finalize all monetary parameters and genesis allocation.
2. Implement and test transactions, digital signatures, and spend validation.
3. Implement consensus-enforced founder lock and its exact unlock schedule.
4. Verify total supply across genesis and every issuance path.
5. Implement persistent storage, peer-to-peer networking, difficulty adjustment, and fork choice.
6. Add reproducible test vectors, security review, and independent audit.
7. Run a public testnet and publish risks and launch criteria before any mainnet release.
