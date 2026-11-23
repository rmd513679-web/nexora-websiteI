"""Educational NEXORA transaction model.
Experimental only; not for real funds.
"""

from dataclasses import dataclass
import base64
import hashlib
import json

from digital_signature import sign_message, verify_signature


def canonical_json(value):
    return json.dumps(
        value,
        sort_keys=True,
        separators=(",", ":"),
    )


def public_key_to_address(public_key_b64):
    """Create a NEXORA address from an Ed25519 public key."""

    try:
        public_bytes = base64.b64decode(
            public_key_b64,
            validate=True,
        )
    except (ValueError, TypeError):
        raise ValueError("Invalid public key.")

    if len(public_bytes) != 32:
        raise ValueError("Invalid public key length.")

    return hashlib.sha256(public_bytes).hexdigest()


@dataclass
class Transaction:
    sender: str
    recipient: str
    amount: int
    fee: int = 0
    nonce: int = 0
    timestamp: int = 0
    tx_id: str = ""
    public_key: str = ""
    signature: str = ""

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
        data = canonical_json(
            self.payload()
        ).encode("utf-8")

        return hashlib.sha256(data).hexdigest()

    def signing_data(self):
        return canonical_json({
            "payload": self.payload(),
            "tx_id": self.tx_id,
            "public_key": self.public_key,
        }).encode("utf-8")

    def __post_init__(self):
        if not self.tx_id:
            self.tx_id = self.calculate_id()

    def sign(self, private_key_b64, public_key_b64):
        """Sign the transaction using the sender's private key."""

        if not self.validate_fields():
            raise ValueError("Invalid transaction fields.")

        self.public_key = public_key_b64
        self.sender = public_key_to_address(public_key_b64)
        self.tx_id = self.calculate_id()

        self.signature = sign_message(
            self.signing_data(),
            private_key_b64,
        )

        if not self.verify():
            self.signature = ""
            raise ValueError("Key pair does not match.")

        return self.signature

    def verify(self):
        """Verify transaction identity and digital signature."""

        if not self.public_key or not self.signature:
            return False

        try:
            if self.sender != public_key_to_address(
                self.public_key
            ):
                return False

            if self.tx_id != self.calculate_id():
                return False

            return verify_signature(
                self.signing_data(),
                self.signature,
                self.public_key,
            )

        except (ValueError, TypeError):
            return False

    def validate_fields(self):
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

        return True

    def validate(self):
        """Validate transaction fields, ID, and signature."""

        if not self.validate_fields():
            return False

        return self.verify()

    def to_dict(self):
        return {
            **self.payload(),
            "tx_id": self.tx_id,
            "public_key": self.public_key,
            "signature": self.signature,
            }
