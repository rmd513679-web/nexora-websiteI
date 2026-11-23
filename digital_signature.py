import base64

from cryptography.exceptions import InvalidSignature
from cryptography.hazmat.primitives import serialization
from cryptography.hazmat.primitives.asymmetric.ed25519 import (
    Ed25519PrivateKey,
    Ed25519PublicKey,
)


def generate_key_pair():
    """Generate a new Ed25519 private/public key pair."""

    private_key = Ed25519PrivateKey.generate()
    public_key = private_key.public_key()

    private_bytes = private_key.private_bytes(
        encoding=serialization.Encoding.Raw,
        format=serialization.PrivateFormat.Raw,
        encryption_algorithm=serialization.NoEncryption(),
    )

    public_bytes = public_key.public_bytes(
        encoding=serialization.Encoding.Raw,
        format=serialization.PublicFormat.Raw,
    )

    return (
        base64.b64encode(private_bytes).decode("ascii"),
        base64.b64encode(public_bytes).decode("ascii"),
    )


def sign_message(message: bytes, private_key_b64: str) -> str:
    """Sign a message using an Ed25519 private key."""

    if not isinstance(message, bytes):
        raise TypeError("Message must be bytes.")

    try:
        private_bytes = base64.b64decode(
            private_key_b64, validate=True
        )
        private_key = Ed25519PrivateKey.from_private_bytes(
            private_bytes
        )
    except (ValueError, TypeError) as exc:
        raise ValueError("Invalid private key.") from exc

    signature = private_key.sign(message)

    return base64.b64encode(signature).decode("ascii")


def verify_signature(
    message: bytes,
    signature_b64: str,
    public_key_b64: str,
) -> bool:
    """Verify an Ed25519 digital signature."""

    if not isinstance(message, bytes):
        raise TypeError("Message must be bytes.")

    try:
        public_bytes = base64.b64decode(
            public_key_b64, validate=True
        )
        signature = base64.b64decode(
            signature_b64, validate=True
        )

        public_key = Ed25519PublicKey.from_public_bytes(
            public_bytes
        )

        public_key.verify(signature, message)
        return True

    except (InvalidSignature, ValueError, TypeError):
        return False
