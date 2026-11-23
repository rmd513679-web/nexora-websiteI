import unittest

from digital_signature import (
    generate_key_pair,
    sign_message,
    verify_signature,
)


class DigitalSignatureTests(unittest.TestCase):

    def setUp(self):
        self.private_key, self.public_key = generate_key_pair()
        self.message = b"NEXORA blockchain transaction"

    def test_key_pair_generation(self):
        self.assertTrue(self.private_key)
        self.assertTrue(self.public_key)

    def test_valid_signature(self):
        signature = sign_message(self.message, self.private_key)

        self.assertTrue(
            verify_signature(
                self.message,
                signature,
                self.public_key,
            )
        )

    def test_modified_message_rejected(self):
        signature = sign_message(self.message, self.private_key)

        self.assertFalse(
            verify_signature(
                b"Modified transaction",
                signature,
                self.public_key,
            )
        )

    def test_wrong_signature_rejected(self):
        signature = sign_message(self.message, self.private_key)
        wrong_private, _ = generate_key_pair()
        wrong_signature = sign_message(
            self.message, wrong_private
        )

        self.assertFalse(
            verify_signature(
                self.message,
                wrong_signature,
                self.public_key,
            )
        )

    def test_wrong_public_key_rejected(self):
        signature = sign_message(self.message, self.private_key)
        _, wrong_public = generate_key_pair()

        self.assertFalse(
            verify_signature(
                self.message,
                signature,
                wrong_public,
            )
        )


if __name__ == "__main__":
    unittest.main()
