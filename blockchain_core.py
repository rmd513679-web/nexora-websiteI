"""Educational NEXORA PoW core; experimental only, not for real funds."""
from dataclasses import dataclass, field
import hashlib, json, time
from typing import List

COIN = 100_000_000
MAX_SUPPLY = 30_000_000 * COIN
INITIAL_REWARD = 50 * COIN
HALVING_INTERVAL = 210_000
DEMO_DIFFICULTY = 2

def canonical_json(value: dict) -> str:
    return json.dumps(value, sort_keys=True, separators=(",", ":"))

def block_reward(height: int, already_issued: int) -> int:
    if height < 1 or already_issued < 0:
        raise ValueError("height must be >= 1 and issued supply must be >= 0")
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
        return {"height": self.height, "timestamp": self.timestamp,
                "previous_hash": self.previous_hash, "reward": self.reward,
                "note": self.note, "nonce": self.nonce}
    def calculate_hash(self):
        return hashlib.sha256(canonical_json(self.payload()).encode()).hexdigest()
    def mine(self, difficulty=DEMO_DIFFICULTY):
        if not 1 <= difficulty <= 5:
            raise ValueError("demo difficulty must be 1..5")
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
        if not 1 <= self.difficulty <= 5:
            raise ValueError("difficulty must be 1..5")
        if not self.blocks:
            g = Block(0, int(time.time()), "0"*64, 0, "Prototype genesis; no monetary value")
            g.mine(self.difficulty)
            self.blocks.append(g)
    @property
    def height(self):
        return self.blocks[-1].height
    def mine_block(self, note=""):
        prev = self.blocks[-1]
        h = prev.height + 1
        reward = block_reward(h, self.issued_supply)
        b = Block(h, max(int(time.time()), prev.timestamp), prev.hash, reward, note)
        b.mine(self.difficulty)
        self.blocks.append(b)
        self.issued_supply += reward
        return b
    def validate(self):
        if not self.blocks:
            return False
        total, target = 0, "0" * self.difficulty
        for i, b in enumerate(self.blocks):
            if b.hash != b.calculate_hash() or not b.hash.startswith(target) or b.reward < 0:
                return False
            if i == 0:
                if b.height != 0 or b.previous_hash != "0"*64 or b.reward != 0:
                    return False
                continue
            p = self.blocks[i-1]
            if b.height != p.height+1 or b.previous_hash != p.hash:
                return False
            if b.reward != block_reward(b.height, total):
                return False
            total += b.reward
            if total > MAX_SUPPLY:
                return False
        return total == self.issued_supply and total <= MAX_SUPPLY

if __name__ == "__main__":
    c = NexoraChain()
    for i in range(3):
        b = c.mine_block(f"educational block {i+1}")
        print(f"height={b.height} hash={b.hash} reward={b.reward/COIN:.8f} NXR")
    print("valid:", c.validate())
    print("Prototype only: no transferable real coins or transactions.")
