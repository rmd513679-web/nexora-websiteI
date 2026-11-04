import unittest
from prototype import Block, DemoChain


class PrototypeTests(unittest.TestCase):
    def test_chain_valid_after_adding_block(self):
        chain = DemoChain(difficulty=1)
        chain.add_demo_block("test")
        self.assertTrue(chain.is_valid())

    def test_tampering_is_detected(self):
        chain = DemoChain(difficulty=1)
        chain.add_demo_block("original")
        chain.blocks[1].data = "tampered"
        self.assertFalse(chain.is_valid())

    def test_wrong_previous_hash_is_detected(self):
        chain = DemoChain(difficulty=1)
        chain.add_demo_block("test")
        chain.blocks[1].previous_hash = "f" * 64
        self.assertFalse(chain.is_valid())

    def test_difficulty_range(self):
        block = Block(1, 1.0, "0" * 64, "test")
        with self.assertRaises(ValueError):
            block.mine(0)


if __name__ == "__main__":
    unittest.main()
