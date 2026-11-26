"""Educational NEXORA PoW core.
Experimental only; not for real funds.
"""

from dataclasses import dataclass, field
import hashlib
import json
import time
from typing import List

from transaction import Transaction


COIN = 100_000_000
MAX_SUPPLY = 30_000_000 * COIN
INITIAL_REWARD = 50 * COIN
HALVING_INTERVAL = 200_000
DEMO_DIFFICULTY = 2


def canonical_json(value):
    return json.dumps(
        value,
        sort_keys=True,
        separators=(",", ":"),
    )


def block_reward(height, already_issued):
    if (
        not isinstance(height, int)
        or isinstance(height, bool)
        or height < 1
    ):
        raise ValueError("height must be an integer >= 1")

    if (
        not isinstance(already_issued, int)
        or isinstance(already_issued, bool)
        or already_issued < 0
    ):
        raise ValueError("issued supply must be a non-negative integer")

    if already_issued >= MAX_SUPPLY:
        return 0

    reward = INITIAL_REWARD >> (
        (height - 1) // HALVING_INTERVAL
    )

    return min(reward, MAX_SUPPLY - already_issued) if reward > 0 else 0


@dataclass
class Block:
    height: int
    timestamp: int
    previous_hash: str
    reward: int
    note: str = ""
    transactions: List[Transaction] = field(default_factory=list)
    nonce: int = 0
    hash: str = ""

    def payload(self):
        return {
            "height": self.height,
            "timestamp": self.timestamp,
            "previous_hash": self.previous_hash,
            "reward": self.reward,
            "note": self.note,
            "transactions": [
                tx.to_dict() for tx in self.transactions
            ],
            "nonce": self.nonce,
        }

    def calculate_hash(self):
        data = canonical_json(self.payload()).encode("utf-8")
        return hashlib.sha256(data).hexdigest()

    def mine(self, difficulty=DEMO_DIFFICULTY):
        if (
            not isinstance(difficulty, int)
            or isinstance(difficulty, bool)
            or not 1 <= difficulty <= 5
        ):
            raise ValueError(
                "demo difficulty must be an integer from 1 to 5"
            )

        target = "0" * difficulty

        while True:
            current_hash = self.calculate_hash()

            if current_hash.startswith(target):
                self.hash = current_hash
                return current_hash

            self.nonce += 1


@dataclass
class NexoraChain:
    difficulty: int = DEMO_DIFFICULTY
    blocks: List[Block] = field(default_factory=list)
    issued_supply: int = 0

    def __post_init__(self):
        if (
            not isinstance(self.difficulty, int)
            or isinstance(self.difficulty, bool)
            or not 1 <= self.difficulty <= 5
        ):
            raise ValueError("invalid demo difficulty")

        if not self.blocks:
            genesis = Block(
                0,
                int(time.time()),
                "0" * 64,
                0,
                "Prototype genesis; no monetary value",
            )
            genesis.mine(self.difficulty)
            self.blocks.append(genesis)

    @property
    def height(self):
        return self.blocks[-1].height

    def mine_block(self, note="", transactions=None):
        if not isinstance(note, str):
            raise ValueError("note must be text")

        if transactions is None:
            transactions = []

        if not isinstance(transactions, list):
            raise ValueError("transactions must be a list")

        seen_ids = set()

        for tx in transactions:
            if not isinstance(tx, Transaction) or not tx.validate():
                raise ValueError("invalid transaction")

            if tx.tx_id in seen_ids:
                raise ValueError("duplicate transaction")

            seen_ids.add(tx.tx_id)

        previous = self.blocks[-1]
        height = previous.height + 1
        reward = block_reward(height, self.issued_supply)

        block = Block(
            height=height,
            timestamp=max(int(time.time()), previous.timestamp),
            previous_hash=previous.hash,
            reward=reward,
            note=note,
            transactions=list(transactions),
        )

        block.mine(self.difficulty)
        self.blocks.append(block)
        self.issued_supply += reward

        return block

    def validate(self):
        if (
            not self.blocks
            or not isinstance(self.difficulty, int)
            or isinstance(self.difficulty, bool)
            or not 1 <= self.difficulty <= 5
        ):
            return False

        total = 0
        target = "0" * self.difficulty
        all_tx_ids = set()

        try:
            for index, block in enumerate(self.blocks):
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

                if not isinstance(block.transactions, list):
                    return False

                if not isinstance(block.hash, str):
                    return False

                if block.hash != block.calculate_hash():
                    return False

                if not block.hash.startswith(target):
                    return False

                if index == 0:
                    if (
                        block.height != 0
                        or block.previous_hash != "0" * 64
                        or block.reward != 0
                        or block.transactions
                    ):
                        return False
                    continue

                previous = self.blocks[index - 1]

                if (
                    block.height != previous.height + 1
                    or block.previous_hash != previous.hash
                    or block.timestamp < previous.timestamp
                ):
                    return False

                if block.reward != block_reward(block.height, total):
                    return False

                for tx in block.transactions:
                    if not isinstance(tx, Transaction) or not tx.validate():
                        return False

                    if tx.tx_id in all_tx_ids:
                        return False

                    all_tx_ids.add(tx.tx_id)

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

    for index in range(3):
        block = chain.mine_block(
            f"educational block {index + 1}"
        )
        print(
            f"height={block.height} "
            f"hash={block.hash} "
            f"reward={block.reward / COIN:.8f} NXR"
        )

    print("valid:", chain.validate())
    print("Prototype only: no real transferable coins.")
