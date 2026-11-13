import unittest
from transaction import Transaction


class TransactionTests(unittest.TestCase):

    def test_valid_transaction(self):
        tx = Transaction("Alice", "Bob", 100)
        self.assertTrue(tx.validate())

    def test_zero_amount_rejected(self):
        tx = Transaction("Alice", "Bob", 0)
        self.assertFalse(tx.validate())

    def test_negative_amount_rejected(self):
        tx = Transaction("Alice", "Bob", -10)
        self.assertFalse(tx.validate())

    def test_negative_fee_rejected(self):
        tx = Transaction("Alice", "Bob", 100, fee=-1)
        self.assertFalse(tx.validate())

    def test_same_sender_receiver_rejected(self):
        tx = Transaction("Alice", "Alice", 100)
        self.assertFalse(tx.validate())

    def test_negative_nonce_rejected(self):
        tx = Transaction("Alice", "Bob", 100, nonce=-1)
        self.assertFalse(tx.validate())

    def test_tampered_transaction_rejected(self):
        tx = Transaction("Alice", "Bob", 100)
        tx.amount = 500
        self.assertFalse(tx.validate())

    def test_transaction_id_is_stable(self):
        tx = Transaction("Alice", "Bob", 100)
        self.assertEqual(tx.tx_id, tx.calculate_id())


if __name__ == "__main__":
    unittest.main()
