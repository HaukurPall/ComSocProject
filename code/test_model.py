import unittest
import model as model

class Tests(unittest.TestCase):
    def test_winner_determination_k_plurality(self):
        profile = model.read_preferences("test_preferences.txt")
        rule = model.initialize_rule(0)
        cost = model.create_cost_distribution(profile.number_of_candidates, 0, 1)
        winner_set = rule.get_winners(profile, 10, cost_vector=cost)
        self.assertEqual(len(winner_set), 10)
        self.assertEqual(sum(cost), 10.0)

unittest.main()