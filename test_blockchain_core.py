import unittest

from blockchain_core import (
    COIN, MAX_SUPPLY, INITIAL_REWARD, HALVING_INTERVAL,
    NexoraChain, Block, block_reward,
)


class CoreTests(unittest.TestCase):
    def test_initial_reward(self):
        self.assertEqual(block_reward(1, 0), 50 * COIN)

    def test_reward_at_halving_boundary(self):
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

    def test_non_integer_inputs_rejected(self):
        for height, issued in [(1.5, 0), (True, 0), (1, 1.2), (1, False)]:
            with self.subTest(height=height, issued=issued):
                with self.assertRaises(ValueError):
                    block_reward(height, issued)

    def test_chain_valid(self):
        chain = NexoraChain(difficulty=1)
        chain.mine_block("one")
        chain.mine_block("two")
        self.assertTrue(chain.validate())

    def test_tampering_detected(self):
        chain = NexoraChain(difficulty=1)
        chain.mine_block("original")
        chain.blocks[1].note = "changed"
        self.assertFalse(chain.validate())

    def test_malformed_chain_detected(self):
        chain = NexoraChain(difficulty=1)
        chain.mine_block("valid")
        chain.blocks.append("not a block")
        self.assertFalse(chain.validate())

    def test_supply_never_exceeds_cap(self):
        chain = NexoraChain(difficulty=1)
        for _ in range(5):
            chain.mine_block("supply test")
        self.assertLessEqual(chain.issued_supply, MAX_SUPPLY)
        self.assertTrue(chain.validate())

    def test_zero_reward_after_integer_schedule_ends(self):
        height = 1
        while block_reward(height, 0) > 0:
            height += HALVING_INTERVAL
        self.assertEqual(block_reward(height, 0), 0)

    def test_total_emission_schedule_is_below_20m_due_to_integer_rounding(self):
        total = 0
        height = 1
        while True:
            reward = block_reward(height, 0)
            if reward == 0:
                break
            total += reward * HALVING_INTERVAL
            height += HALVING_INTERVAL
        self.assertLess(total, 20_000_000 * COIN)
        self.assertGreater(total, 19_999_000 * COIN)

    def test_bad_difficulty_rejected(self):
        for difficulty in [0, 6, True, 1.5]:
            with self.subTest(difficulty=difficulty):
                with self.assertRaises(ValueError):
                    NexoraChain(difficulty=difficulty)


if __name__ == "__main__":
    unittest.main()
