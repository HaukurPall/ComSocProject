import unittest
import model as model

profile = model.read_preferences("test_preferences.txt")

class Tests(unittest.TestCase):
    def test_winner_determination_k_plurality(self):
        rule = model.initialize_rule(0)
        cost = model.create_cost_distribution(profile.number_of_candidates, 0, 1)
        winner_set = rule.get_winners(profile, 10, cost_vector=cost)
        self.assertEqual(len(winner_set), 10)
        self.assertEqual(sum(cost), 10)

    def test_winner_determination_k_borda(self):
        rule = model.initialize_rule(1)
        cost = model.create_cost_distribution(profile.number_of_candidates, 0, 1)
        winner_set = rule.get_winners(profile, 10, cost_vector=cost)
        self.assertEqual(len(winner_set), 10)
        self.assertEqual(sum(cost), 10)

    def test_winner_determination_copeland(self):
        rule = model.initialize_rule(2)
        cost = model.create_cost_distribution(profile.number_of_candidates, 0, 1)
        winner_set = rule.get_winners(profile, 10, cost_vector=cost)
        self.assertEqual(len(winner_set), 10)
        self.assertEqual(sum(cost), 10)

    def test_winner_determination_knapsack(self):
        rule = model.initialize_rule(3)
        cost = model.create_cost_distribution(profile.number_of_candidates, 0, 1)
        winner_set = rule.get_winners(profile, 10, cost_vector=cost)
        self.assertEqual(len(winner_set), 10)
        self.assertEqual(sum(cost), 10)

if __name__ == "__main__":
    unittest.main()