import unittest
from blockchain_core import COIN, MAX_SUPPLY, INITIAL_REWARD, HALVING_INTERVAL, NexoraChain, block_reward

class CoreTests(unittest.TestCase):
    def test_initial_reward(self):
        self.assertEqual(block_reward(1, 0), INITIAL_REWARD)
    def test_halving(self):
        self.assertEqual(block_reward(HALVING_INTERVAL+1, 0), INITIAL_REWARD//2)
    def test_cap_partial_reward(self):
        self.assertEqual(block_reward(1, MAX_SUPPLY-7), 7)
    def test_no_reward_at_cap(self):
        self.assertEqual(block_reward(1, MAX_SUPPLY), 0)
    def test_chain_valid(self):
        c=NexoraChain(difficulty=1); c.mine_block("one"); c.mine_block("two")
        self.assertTrue(c.validate())
    def test_tampering_detected(self):
        c=NexoraChain(difficulty=1); c.mine_block("original")
        c.blocks[1].note="changed"
        self.assertFalse(c.validate())
    def test_supply_cap_reward_rule(self):
        self.assertEqual(block_reward(1, MAX_SUPPLY-1), 1)
        self.assertEqual(block_reward(1, MAX_SUPPLY), 0)

if __name__ == "__main__": unittest.main()
