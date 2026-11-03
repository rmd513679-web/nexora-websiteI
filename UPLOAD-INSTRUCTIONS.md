# Upload instructions (Android / GitHub)

Proposed replacement files:
- blockchain_core.py
- test_blockchain_core.py
- whitepaper.md
- tokenomics.md
- roadmap.md
- protocol-notes.md

Keep a copy of the old files and review changes before replacing them. This draft changes HALVING_INTERVAL from 210,000 to 200,000 blocks to align the theoretical lifetime mining emission with approximately 20M NXR. This is a protocol parameter decision; after launch, changing it would require coordinated consensus rules.

Suggested commit message: Align NEXORA draft supply and mining schedule

This remains an educational prototype. The founder allocation and reserve are not implemented in code.
