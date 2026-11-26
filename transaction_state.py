
"""Educational NEXORA transaction state.
Experimental only; not for real funds.
"""


class TransactionState:

    def __init__(self):
        self.next_nonce = {}
        self.processed_tx_ids = set()

    def expected_nonce(self, sender):
        """Return the next expected nonce for a sender."""
        return self.next_nonce.get(sender, 1)

    def accept(self, transaction):
        """Accept a valid transaction only once and in nonce order."""

        if not transaction.validate():
            return False

        if transaction.tx_id in self.processed_tx_ids:
            return False

        sender = transaction.sender
        expected = self.expected_nonce(sender)

        if transaction.nonce != expected:
            return False

        self.processed_tx_ids.add(transaction.tx_id)
        self.next_nonce[sender] = expected + 1

        return True
