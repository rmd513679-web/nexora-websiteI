# Upload instructions (Android / GitHub)

Proposed replacement files:
- blockchain_core.py
- test_blockchain_core.py
- whitepaper.md
- tokenomics.md
- roadmap.md
- protocol-notes.md

Keep a copy of the old files and review changes before replacing them. This draft uses HALVING_INTERVAL = 200,000 blocks. The emission schedule is just under 20M NXR due to integer rounding. This is a protocol parameter decision; after launch, changing it would require coordinated consensus rules.

Suggested commit message: `Improve NEXORA draft validation and emission tests`

This remains an educational prototype. Founder allocation and reserve are not implemented in code. These tests are not a security audit, and the project is not safe for real funds.
