"""Educational NEXORA PoW core; experimental only, not for real funds."""
from dataclasses import dataclass, field
import hashlib
import json
import time
from typing import List

COIN = 100_000_000
MAX_SUPPLY = 30_000_000 * COIN
INITIAL_REWARD = 50 * COIN
# Working-draft parameter; review before any public network launch.
HALVING_INTERVAL = 200_000
DEMO_DIFFICULTY = 2


def canonical_json(value: dict) -> str:
    return json.dumps(value, sort_keys=True, separators=(",", ":"))


def block_reward(height: int, already_issued: int) -> int:
    """Return the block subsidy in smallest units for this educational draft."""
    if not isinstance(height, int) or isinstance(height, bool) or height < 1:
        raise ValueError("height must be an integer >= 1")
    if not isinstance(already_issued, int) or isinstance(already_issued, bool) or already_issued < 0:
        raise ValueError("issued supply must be a non-negative integer")
    if already_issued >= MAX_SUPPLY:
        return 0
    reward = INITIAL_REWARD >> ((height - 1) // HALVING_INTERVAL)
    return min(reward, MAX_SUPPLY - already_issued) if reward > 0 else 0


@dataclass
class Block:
    height: int
    timestamp: int
    previous_hash: str
    reward: int
    note: str = ""
    nonce: int = 0
    hash: str = ""

    def payload(self):
        return {
            "height": self.height,
            "timestamp": self.timestamp,
            "previous_hash": self.previous_hash,
            "reward": self.reward,
            "note": self.note,
            "nonce": self.nonce,
        }

    def calculate_hash(self):
        return hashlib.sha256(canonical_json(self.payload()).encode("utf-8")).hexdigest()

    def mine(self, difficulty=DEMO_DIFFICULTY):
        if not isinstance(difficulty, int) or isinstance(difficulty, bool) or not 1 <= difficulty <= 5:
            raise ValueError("demo difficulty must be an integer from 1 to 5")
        target = "0" * difficulty
        while True:
            h = self.calculate_hash()
            if h.startswith(target):
                self.hash = h
                return h
            self.nonce += 1


@dataclass
class NexoraChain:
    difficulty: int = DEMO_DIFFICULTY
    blocks: List[Block] = field(default_factory=list)
    issued_supply: int = 0

    def __post_init__(self):
        if not isinstance(self.difficulty, int) or isinstance(self.difficulty, bool) or not 1 <= self.difficulty <= 5:
            raise ValueError("demo difficulty must be an integer from 1 to 5")
        if not self.blocks:
            genesis = Block(0, int(time.time()), "0" * 64, 0, "Prototype genesis; no monetary value")
            genesis.mine(self.difficulty)
            self.blocks.append(genesis)

    @property
    def height(self):
        return self.blocks[-1].height

    def mine_block(self, note=""):
        if not isinstance(note, str):
            raise ValueError("note must be text")
        prev = self.blocks[-1]
        height = prev.height + 1
        reward = block_reward(height, self.issued_supply)
        block = Block(height, max(int(time.time()), prev.timestamp), prev.hash, reward, note)
        block.mine(self.difficulty)
        self.blocks.append(block)
        self.issued_supply += reward
        return block

    def validate(self):
        """Check this prototype's local chain structure and issuance accounting."""
        if not self.blocks or not isinstance(self.difficulty, int) or isinstance(self.difficulty, bool):
            return False
        if not 1 <= self.difficulty <= 5:
            return False
        total = 0
        target = "0" * self.difficulty
        try:
            for i, block in enumerate(self.blocks):
                if not isinstance(block, Block):
                    return False
                if not isinstance(block.height, int) or isinstance(block.height, bool):
                    return False
                if not isinstance(block.timestamp, int) or isinstance(block.timestamp, bool) or block.timestamp < 0:
                    return False
                if not isinstance(block.previous_hash, str) or len(block.previous_hash) != 64:
                    return False
                if not isinstance(block.reward, int) or isinstance(block.reward, bool) or block.reward < 0:
                    return False
                if not isinstance(block.nonce, int) or isinstance(block.nonce, bool) or block.nonce < 0:
                    return False
                if not isinstance(block.note, str):
                    return False
                if not isinstance(block.hash, str) or block.hash != block.calculate_hash():
                    return False
                if not block.hash.startswith(target):
                    return False
                if i == 0:
                    if block.height != 0 or block.previous_hash != "0" * 64 or block.reward != 0:
                        return False
                    continue
                previous = self.blocks[i - 1]
                if block.height != previous.height + 1 or block.previous_hash != previous.hash:
                    return False
                if block.timestamp < previous.timestamp:
                    return False
                if block.reward != block_reward(block.height, total):
                    return False
                total += block.reward
                if total > MAX_SUPPLY:
                    return False
        except (TypeError, ValueError, AttributeError, OverflowError):
            return False
        return (
            isinstance(self.issued_supply, int)
            and not isinstance(self.issued_supply, bool)
            and total == self.issued_supply
            and total <= MAX_SUPPLY
        )


if __name__ == "__main__":
    chain = NexoraChain()
    for i in range(3):
        block = chain.mine_block(f"educational block {i + 1}")
        print(f"height={block.height} hash={block.hash} reward={block.reward / COIN:.8f} NXR")
    print("valid:", chain.validate())
    print("Prototype only: no transferable real coins or transactions.")
