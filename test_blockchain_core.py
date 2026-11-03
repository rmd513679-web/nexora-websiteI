import unittest
from blockchain_core import COIN, MAX_SUPPLY, INITIAL_REWARD, HALVING_INTERVAL, NexoraChain, block_reward

class CoreTests(unittest.TestCase):
    def test_initial_reward(self):
        self.assertEqual(block_reward(1, 0), 50 * COIN)
    def test_reward_before_halving(self):
        self.assertEqual(block_reward(HALVING_INTERVAL, 0), INITIAL_REWARD)
    def test_reward_after_halving(self):
        self.assertEqual(block_reward(HALVING_INTERVAL + 1, 0), INITIAL_REWARD // 2)
    def test_second_halving(self):
        self.assertEqual(block_reward(2 * HALVING_INTERVAL + 1, 0), INITIAL_REWARD // 4)
    def test_partial_reward_at_supply_cap(self):
        self.assertEqual(block_reward(1, MAX_SUPPLY - 7), 7)
    def test_no_reward_at_supply_cap(self):
        self.assertEqual(block_reward(1, MAX_SUPPLY), 0)
    def test_negative_supply_rejected(self):
        with self.assertRaises(ValueError):
            block_reward(1, -1)
    def test_invalid_height_rejected(self):
        with self.assertRaises(ValueError):
            block_reward(0, 0)
    def test_chain_valid(self):
        c = NexoraChain(difficulty=1)
        c.mine_block("one"); c.mine_block("two")
        self.assertTrue(c.validate())
    def test_tampering_detected(self):
        c = NexoraChain(difficulty=1)
        c.mine_block("original")
        c.blocks[1].note = "changed"
        self.assertFalse(c.validate())
    def test_supply_never_exceeds_cap(self):
        c = NexoraChain(difficulty=1)
        for _ in range(5):
            c.mine_block("supply test")
        self.assertLessEqual(c.issued_supply, MAX_SUPPLY)
        self.assertTrue(c.validate())

if __name__ == "__main__":
    unittest.main()
