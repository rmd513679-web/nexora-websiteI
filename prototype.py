"""Educational single-process PoW demo. Not a production blockchain."""
from dataclasses import dataclass, asdict
import hashlib
import json
import time


def canonical_json(data: dict) -> str:
    return json.dumps(data, sort_keys=True, separators=(",", ":"))


@dataclass
class Block:
    index: int
    timestamp: float
    previous_hash: str
    data: str
    nonce: int = 0
    hash: str = ""

    def header_payload(self) -> dict:
        return {
            "index": self.index,
            "timestamp": self.timestamp,
            "previous_hash": self.previous_hash,
            "data": self.data,
            "nonce": self.nonce,
        }

    def calculate_hash(self) -> str:
        raw = canonical_json(self.header_payload()).encode("utf-8")
        return hashlib.sha256(raw).hexdigest()

    def mine(self, difficulty: int = 3) -> str:
        """Find a hash with `difficulty` leading zero hex characters."""
        if not 1 <= difficulty <= 6:
            raise ValueError("Demo difficulty must be between 1 and 6")
        target = "0" * difficulty
        while True:
            candidate = self.calculate_hash()
            if candidate.startswith(target):
                self.hash = candidate
                return candidate
            self.nonce += 1


class DemoChain:
    def __init__(self, difficulty: int = 3):
        self.difficulty = difficulty
        genesis = Block(
            index=0,
            timestamp=time.time(),
            previous_hash="0" * 64,
            data="NEXORA educational genesis (no monetary value)",
        )
        genesis.mine(self.difficulty)
        self.blocks = [genesis]

    def add_demo_block(self, data: str) -> Block:
        previous = self.blocks[-1]
        block = Block(
            index=previous.index + 1,
            timestamp=time.time(),
            previous_hash=previous.hash,
            data=data,
        )
        block.mine(self.difficulty)
        self.blocks.append(block)
        return block

    def is_valid(self) -> bool:
        target = "0" * self.difficulty
        for i, block in enumerate(self.blocks):
            if block.hash != block.calculate_hash():
                return False
            if not block.hash.startswith(target):
                return False
            if i == 0:
                if block.previous_hash != "0" * 64:
                    return False
            else:
                prev = self.blocks[i - 1]
                if block.previous_hash != prev.hash:
                    return False
                if block.index != prev.index + 1:
                    return False
        return True


def main():
    chain = DemoChain(difficulty=3)
    for message in ("Prototype block one", "Prototype block two"):
        block = chain.add_demo_block(message)
        print(f"Block {block.index}: {block.hash} (nonce={block.nonce})")
    print("Chain valid:", chain.is_valid())
    print("Reminder: demo only; no real coins or transactions.")


if __name__ == "__main__":
    main()
