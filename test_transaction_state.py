import unittest

from digital_signature import generate_key_pair
from transaction import Transaction
from transaction_state import TransactionState


class TransactionStateTests(unittest.TestCase):

    def setUp(self):
        self.state = TransactionState()
        self.private_key, self.public_key = generate_key_pair()

    def create_signed_transaction(
        self, nonce=1, amount=100, recipient="Bob"
    ):
        tx = Transaction(
            sender="temporary",
            recipient=recipient,
            amount=amount,
            fee=2,
            nonce=nonce,
            timestamp=1000,
        )
        tx.sign(self.private_key, self.public_key)
        return tx

    def test_first_transaction_accepted(self):
        tx = self.create_signed_transaction()

        self.assertTrue(self.state.accept(tx))
        self.assertEqual(self.state.expected_nonce(tx.sender), 2)

    def test_next_nonce_accepted(self):
        tx1 = self.create_signed_transaction(nonce=1)
        tx2 = self.create_signed_transaction(
            nonce=2,
            recipient="Charlie",
        )

        self.assertTrue(self.state.accept(tx1))
        self.assertTrue(self.state.accept(tx2))
        self.assertEqual(self.state.expected_nonce(tx1.sender), 3)

    def test_wrong_nonce_rejected(self):
        tx = self.create_signed_transaction(nonce=2)

        self.assertFalse(self.state.accept(tx))
        self.assertEqual(self.state.expected_nonce(tx.sender), 1)

    def test_duplicate_transaction_rejected(self):
        tx = self.create_signed_transaction()

        self.assertTrue(self.state.accept(tx))
        self.assertFalse(self.state.accept(tx))

    def test_invalid_transaction_rejected(self):
        tx = self.create_signed_transaction()
        tx.amount = 999

        self.assertFalse(self.state.accept(tx))

    def test_nonce_order_enforced(self):
        tx1 = self.create_signed_transaction(nonce=1)
        tx2 = self.create_signed_transaction(
            nonce=2,
            recipient="Charlie",
        )
        tx3 = self.create_signed_transaction(
            nonce=3,
            recipient="David",
        )

        self.assertTrue(self.state.accept(tx1))
        self.assertFalse(self.state.accept(tx3))
        self.assertTrue(self.state.accept(tx2))

    def test_different_senders_have_independent_nonces(self):
        tx1 = self.create_signed_transaction(nonce=1)

        private_key2, public_key2 = generate_key_pair()

        tx2 = Transaction(
            sender="temporary",
            recipient="Charlie",
            amount=100,
            fee=2,
            nonce=1,
            timestamp=1000,
        )
        tx2.sign(private_key2, public_key2)

        self.assertTrue(self.state.accept(tx1))
        self.assertTrue(self.state.accept(tx2))


if __name__ == "__main__":
    unittest.main()
