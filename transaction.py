"""Educational NEXORA transaction model.
Experimental only; not for real funds.
"""

from dataclasses import dataclass
import hashlib
import json


def canonical_json(value):
    return json.dumps(
        value,
        sort_keys=True,
        separators=(",", ":"),
    )


@dataclass
class Transaction:
    sender: str
    recipient: str
    amount: int
    fee: int = 0
    nonce: int = 0
    timestamp: int = 0
    tx_id: str = ""

    def payload(self):
        return {
            "sender": self.sender,
            "recipient": self.recipient,
            "amount": self.amount,
            "fee": self.fee,
            "nonce": self.nonce,
            "timestamp": self.timestamp,
        }

    def calculate_id(self):
        data = canonical_json(self.payload()).encode("utf-8")
        return hashlib.sha256(data).hexdigest()

    def __post_init__(self):
        if not self.tx_id:
            self.tx_id = self.calculate_id()

    def validate(self):
        if not isinstance(self.sender, str) or not self.sender.strip():
            return False

        if not isinstance(self.recipient, str) or not self.recipient.strip():
            return False

        if self.sender == self.recipient:
            return False

        if not isinstance(self.amount, int) or isinstance(self.amount, bool):
            return False

        if self.amount <= 0:
            return False

        if not isinstance(self.fee, int) or isinstance(self.fee, bool):
            return False

        if self.fee < 0:
            return False

        if not isinstance(self.nonce, int) or isinstance(self.nonce, bool):
            return False

        if self.nonce < 0:
            return False

        if not isinstance(self.timestamp, int) or isinstance(self.timestamp, bool):
            return False

        if self.timestamp < 0:
            return False

        if not isinstance(self.tx_id, str):
            return False

        return self.tx_id == self.calculate_id()

    def to_dict(self):
        return {
            **self.payload(),
            "tx_id": self.tx_id,
          }
