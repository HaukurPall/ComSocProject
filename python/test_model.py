import unittest
import model as model
import data

profile = data.read_from_file("unanimous_profile.txt")
budget = 10

class Tests(unittest.TestCase):

    def test_winner_determination_k_plurality(self):
        rule = model.initialize_rule(0)
        cost = model.create_cost_distribution(profile.number_of_candidates, 0, 1)
        winner_set = rule.get_winners(profile, budget, cost_vector=cost)
        self.assertEqual(len(winner_set), 10)
        self.assertEqual(sum(cost), 10)
        axiom = model.initialize_axiom(0)
        self.assertTrue(axiom.is_satisfied(rule, profile, budget, cost))
        axiom = model.initialize_axiom(1)
        self.assertTrue(axiom.is_satisfied(rule, profile, 5, cost))

    def test_winner_determination_k_borda(self):
        rule = model.initialize_rule(1)
        cost = model.create_cost_distribution(profile.number_of_candidates, 0, 1)
        winner_set = rule.get_winners(profile, 10, cost_vector=cost)
        self.assertEqual(len(winner_set), 10)
        self.assertEqual(sum(cost), 10)
        axiom = model.initialize_axiom(0)
        self.assertTrue(axiom.is_satisfied(rule, profile, budget, cost))
        axiom = model.initialize_axiom(1)
        self.assertTrue(axiom.is_satisfied(rule, profile, 5, cost))

    def test_winner_determination_copeland(self):
        rule = model.initialize_rule(2)
        cost = model.create_cost_distribution(profile.number_of_candidates, 0, 1)
        winner_set = rule.get_winners(profile, 10, cost_vector=cost)
        self.assertEqual(len(winner_set), 10)
        self.assertEqual(sum(cost), 10)
        axiom = model.initialize_axiom(0)
        self.assertTrue(axiom.is_satisfied(rule, profile, budget, cost))
        axiom = model.initialize_axiom(1)
        self.assertTrue(axiom.is_satisfied(rule, profile, 5, cost))

    def test_winner_determination_knapsack(self):
        rule = model.initialize_rule(3)
        cost = model.create_cost_distribution(profile.number_of_candidates, 0, 1)
        winner_set = rule.get_winners(profile, 10, cost_vector=cost)
        self.assertEqual(len(winner_set), 10)
        self.assertEqual(sum(cost), 10)
        axiom = model.initialize_axiom(0)
        self.assertTrue(axiom.is_satisfied(rule, profile, budget, cost))
        axiom = model.initialize_axiom(1)
        self.assertTrue(axiom.is_satisfied(rule, profile, 5, cost))

    def test_winner_determination_theta_rule(self):
        rule = model.initialize_rule(4)
        cost = model.create_cost_distribution(profile.number_of_candidates, 0, 1)
        winner_set = rule.get_winners(profile, 10, cost_vector=cost)
        self.assertEqual(len(winner_set), 10)
        self.assertEqual(sum(cost), 10)
        axiom = model.initialize_axiom(0)
        self.assertTrue(axiom.is_satisfied(rule, profile, budget, cost))
        axiom = model.initialize_axiom(1)
        self.assertTrue(axiom.is_satisfied(rule, profile, 5, cost))

    def test_write(self):
        import os
        file_name = "test_out.txt"
        data.write_to_file(file_name, profile)
        os.remove(file_name)

    def test_normal_distribution(self):
        cost = model.create_cost_distribution(profile.number_of_candidates, 1, 15)
        print(cost)
        self.assertTrue(max(cost) <= 150)
        self.assertTrue(min(cost) >= 50)

if __name__ == "__main__":
    unittest.main()