import unittest
import data
import CR as cr

profile = data.read_from_file("unanimous_profile.txt")
budget = 1500
normal_cost_distribution = 0

class Tests(unittest.TestCase):

    def test_winner_determination_k_plurality(self):
        rule = cr.initialize_rule(0)
        cost = cr.create_cost_distribution(profile.number_of_candidates, normal_cost_distribution)
        winner_set = rule.get_winners(profile, budget, cost_vector=cost)
        self.assertEqual(len(winner_set), 10)
        self.assertTrue((lambda sum: sum >= 800, sum(cost)))
        axiom = cr.initialize_axiom(0)
        self.assertTrue(axiom.is_satisfied(rule, profile, budget, cost))
        axiom = cr.initialize_axiom(1)
        self.assertTrue(axiom.is_satisfied(rule, profile, 5, cost))

    def test_winner_determination_k_borda(self):
        rule = cr.initialize_rule(1)
        cost = cr.create_cost_distribution(profile.number_of_candidates, normal_cost_distribution)
        winner_set = rule.get_winners(profile, budget, cost_vector=cost)
        self.assertEqual(len(winner_set), 10)
        self.assertTrue((lambda sum: sum >= 800, sum(cost)))
        axiom = cr.initialize_axiom(0)
        self.assertTrue(axiom.is_satisfied(rule, profile, budget, cost))
        axiom = cr.initialize_axiom(1)
        self.assertTrue(axiom.is_satisfied(rule, profile, 5, cost))

    def test_winner_determination_copeland(self):
        rule = cr.initialize_rule(2)
        cost = cr.create_cost_distribution(profile.number_of_candidates, normal_cost_distribution)
        winner_set = rule.get_winners(profile, budget, cost_vector=cost)
        self.assertEqual(len(winner_set), 10)
        self.assertTrue((lambda sum: sum >= 800, sum(cost)))
        axiom = cr.initialize_axiom(0)
        self.assertTrue(axiom.is_satisfied(rule, profile, budget, cost))
        axiom = cr.initialize_axiom(1)
        self.assertTrue(axiom.is_satisfied(rule, profile, 5, cost))

    def test_winner_determination_knapsack(self):
        rule = cr.initialize_rule(3)
        cost = cr.create_cost_distribution(profile.number_of_candidates, normal_cost_distribution)
        winner_set = rule.get_winners(profile, budget, cost_vector=cost)
        self.assertEqual(len(winner_set), 10)
        self.assertTrue((lambda sum: sum >= 800, sum(cost)))
        axiom = cr.initialize_axiom(0)
        self.assertTrue(axiom.is_satisfied(rule, profile, budget, cost))
        axiom = cr.initialize_axiom(1)
        self.assertTrue(axiom.is_satisfied(rule, profile, 5, cost))

    def test_winner_determination_theta_rule(self):
        rule = cr.initialize_rule(4)
        cost = cr.create_cost_distribution(profile.number_of_candidates, normal_cost_distribution)
        winner_set = rule.get_winners(profile, budget, cost_vector=cost)
        self.assertEqual(len(winner_set), 10)
        self.assertTrue((lambda sum: sum >= 800, sum(cost)))
        axiom = cr.initialize_axiom(0)
        self.assertTrue(axiom.is_satisfied(rule, profile, budget, cost))
        axiom = cr.initialize_axiom(1)
        self.assertTrue(axiom.is_satisfied(rule, profile, 5, cost))

    def test_write(self):
        import os
        file_name = "test_out.txt"
        data.write_to_file(file_name, profile)
        os.remove(file_name)

    def test_normal_distribution(self):
        cost = cr.create_cost_distribution(profile.number_of_candidates, normal_cost_distribution)
        self.assertTrue(max(cost) <= 150)
        self.assertTrue(min(cost) >= 50)

    def test_read_sushi(self):
        shushi_profile = data.read_from_file("sushi_data.txt")


if __name__ == "__main__":
    unittest.main()