import unittest

from transaction import Transaction
from digital_signature import generate_key_pair, sign_message


class TransactionTests(unittest.TestCase):

    def setUp(self):
        self.private_key, self.public_key = generate_key_pair()

    def create_signed_transaction(self):
        tx = Transaction(
            sender="temporary",
            recipient="Bob",
            amount=100,
            fee=2,
            nonce=1,
            timestamp=1000,
        )
        tx.sign(self.private_key, self.public_key)
        return tx

    def test_valid_signed_transaction(self):
        tx = self.create_signed_transaction()
        self.assertTrue(tx.validate())
        self.assertTrue(tx.verify())

    def test_unsigned_transaction_rejected(self):
        tx = Transaction("Alice", "Bob", 100)
        self.assertFalse(tx.validate())

    def test_zero_amount_rejected(self):
        tx = Transaction("Alice", "Bob", 0)
        self.assertFalse(tx.validate())

    def test_negative_amount_rejected(self):
        tx = Transaction("Alice", "Bob", -10)
        self.assertFalse(tx.validate_fields())

    def test_negative_fee_rejected(self):
        tx = Transaction("Alice", "Bob", 100, fee=-1)
        self.assertFalse(tx.validate_fields())

    def test_same_sender_receiver_rejected(self):
        tx = Transaction("Alice", "Alice", 100)
        self.assertFalse(tx.validate_fields())

    def test_negative_nonce_rejected(self):
        tx = Transaction("Alice", "Bob", 100, nonce=-1)
        self.assertFalse(tx.validate_fields())

    def test_tampered_transaction_rejected(self):
        tx = self.create_signed_transaction()
        tx.amount = 500
        self.assertFalse(tx.validate())

    def test_wrong_public_key_rejected(self):
        tx = self.create_signed_transaction()
        _, wrong_public_key = generate_key_pair()

        tx.public_key = wrong_public_key

        self.assertFalse(tx.verify())

    def test_wrong_private_key_rejected(self):
        tx = Transaction("temporary", "Bob", 100)
        wrong_private, _ = generate_key_pair()

        with self.assertRaises(ValueError):
            tx.sign(wrong_private, self.public_key)

    def test_modified_signature_rejected(self):
        tx = self.create_signed_transaction()

        tx.signature = sign_message(
            b"Different transaction",
            self.private_key,
        )

        self.assertFalse(tx.verify())

    def test_transaction_id_is_stable(self):
        tx = Transaction("Alice", "Bob", 100)
        self.assertEqual(tx.tx_id, tx.calculate_id())

    def test_to_dict_contains_signature(self):
        tx = self.create_signed_transaction()
        data = tx.to_dict()

        self.assertIn("signature", data)
        self.assertIn("public_key", data)
        self.assertIn("tx_id", data)


if __name__ == "__main__":
    unittest.main()

 def test_json_round_trip(self):
        tx = self.create_signed_transaction()

        restored = Transaction.from_json(tx.to_json())

        self.assertEqual(restored.to_dict(), tx.to_dict())
        self.assertTrue(restored.validate())

    def test_dict_round_trip(self):
        tx = self.create_signed_transaction()

        restored = Transaction.from_dict(tx.to_dict())

        self.assertEqual(restored.to_dict(), tx.to_dict())
        self.assertTrue(restored.validate())

    def test_invalid_json_rejected(self):
        with self.assertRaises(ValueError):
            Transaction.from_json("not valid json")

    def test_missing_field_rejected(self):
        tx = self.create_signed_transaction()
        data = tx.to_dict()
        del data["signature"]

        with self.assertRaises(ValueError):
            Transaction.from_dict(data)

    def test_tampered_json_rejected(self):
        tx = self.create_signed_transaction()
        data = tx.to_dict()
        data["amount"] = 999

        with self.assertRaises(ValueError):
            Transaction.from_dict(data)

    def test_extra_field_rejected(self):
        tx = self.create_signed_transaction()
        data = tx.to_dict()
        data["unexpected"] = "value"

        with self.assertRaises(ValueError):
            Transaction.from_dict(data)
