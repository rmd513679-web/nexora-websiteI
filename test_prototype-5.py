import unittest
from nexora.prototype import Block, DemoChain

class PrototypeTests(unittest.TestCase):
    def test_chain_valid_after_adding_block(self):
        chain = NexoraChain(difficulty=1)
        chain.mine_block("test")
        self.assertTrue(chain.validate())

    def test_tampering_is_detected(self):
        chain = NexoraChain(difficulty=1)
        chain.mine_block("original")
        chain.blocks[1].note = "tampered"
        self.assertFalse(chain.validate())

    def test_wrong_previous_hash_is_detected(self):
        chain = NexoraChain(difficulty=1)
        chain.mine_block("test")
        chain.blocks[1].previous_hash = "f" * 64
        self.assertFalse(chain.validate())

    def test_difficulty_range(self):
        block = Block(1, 1, "0" * 64, 0, "test")
        with self.assertRaises(ValueError):
            block.mine(0)


if __name__ == "__main__":
    unittest.main()
