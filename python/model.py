# Authors: Haukur Pall Jonsson, Silvan Hungerbuhler, Max Rapp and Greg Liowski
# Date: 20th May 2017
import copy
import random
import math
import argparse
import data
import numpy as np


class Preference:
    """
    :param list_of_preferences: orderer list of integers, in which integer is a unique candidate, first candidate is 0
    """

    def __init__(self, preference_order):
        self.preference_order = [int(x) for x in preference_order]

    def __eq__(self, other):
        return self.preference_order == other.preference_order

    def __getitem__(self, index):
        return self.preference_order[index]

    """
    Returns True if x is more preferred than y
    """

    def is_x_more_preferred_than_y(self, x, y):
        return self.preference_order.index(x) < self.preference_order.index(y)

    """
    Returns a new preference order in which x has been placed first
    """

    def place_x_first(self, x):
        old_order = copy.deepcopy(self.preference_order)
        old_order.remove(x)
        return Preference([x] + old_order)

    """
    Returns a new preference order in which x has been placed last
    """

    def place_x_last(self, x):
        old_order = copy.deepcopy(self.preference_order)
        old_order.remove(x)
        return Preference(old_order + [x])

    """
    Returns a new preference order in which the list of preference order has been placed last
    """

    def place_preferences_last(self, list_of_preferences):
        old_order = copy.deepcopy(self.preference_order)
        for preference in list_of_preferences:
            old_order.remove(preference)
        return Preference(old_order + list_of_preferences)

    """
    Generates a random preference order over a uniform distribution.
    """

    @staticmethod
    def generate_random_preference_order(m):
        preference_set = set([x for x in range(0, m)])
        preference_list = random.sample(preference_set, m)
        return Preference(preference_list)

    def index_based_swap(self, candidate_index, other_candidate_index):
        tmp = self.preference_order[candidate_index]
        self.preference_order[candidate_index] = self.preference_order[other_candidate_index]
        self.preference_order[other_candidate_index] = tmp

    def get_copy(self):
        order = copy.deepcopy(self.preference_order)
        return Preference(order)

    def get_first_candidate(self):
        return self.preference_order[0]

    def get_number_of_candidates(self):
        return len(self.preference_order)

    def __str__(self):
        return str(self.preference_order)


class Profile:
    def __init__(self, number_of_voters, number_of_candidates, preference_list):
        self.number_of_voters = number_of_voters
        self.number_of_candidates = number_of_candidates
        self.preference_list = preference_list
        if self.number_of_voters != len(preference_list):
            raise Exception("The reported number of voters does not equal the ballot")
        if self.number_of_candidates != preference_list[0].get_number_of_candidates():
            raise Exception("The reported number of candidates does not equal the ballot")
        self.borda_score = [x for x in range(self.number_of_candidates - 1, -1, -1)]
        self.plurality_score = [0 for x in range(self.number_of_candidates)]
        self.plurality_score[0] = 1

    def __str__(self):
        profile = ""
        for preference_order_index, preference_order in enumerate(self.preference_list):
            profile += str(preference_order) + "\n"
        return profile

    def __getitem__(self, index):
        return self.preference_list[index]

    def compute_pairwise_wins(self):
        P = [[0 for x in range(self.number_of_candidates)] for x in range(self.number_of_candidates)]
        for preference_order in self.preference_list:
            for candidate in range(self.number_of_candidates):
                for other_candidate in range(self.number_of_candidates):
                    # majority contest against one self = win, for simplifying later computation
                    if other_candidate == candidate:
                        P[candidate][other_candidate] += 1
                        continue
                    if preference_order.is_x_more_preferred_than_y(candidate, other_candidate):
                        P[candidate][other_candidate] += 1
        P = [[wins / float(self.number_of_candidates) for wins in candidate] for candidate in P]
        return P

    def compute_utility_of_set(self, scoring_vector, winner_set):
        candidate_scores = VotingRule.compute_scores_with_vector(scoring_vector, self)
        return sum([candidate_scores[winner] for winner in winner_set])


class VotingRule:
    def __init__(self, name, number):
        self.name = name
        self.number = number

    def __str__(self):
        return str(self.number) + " " + self.name

    """
    Returns an ordered list of winners
    """

    def get_winners(self, profile, budget, cost_vector):
        pass

    """
    Returns a winner using a tiebreaker (lexicographically)
    """

    @staticmethod
    def break_ties(winners):
        first_winner = min(winners)
        tie_losers = copy.deepcopy(winners)
        tie_losers.remove(first_winner)
        return first_winner, tie_losers

    """
    Returns a list of winners using the score and cut method.
    Chooses the highest candidate which does not cost more than the remaining budget.
    """

    @staticmethod
    def cut_score(budget, candidate_scores, cost_vector):
        winners = []
        moneyh_to_spend = budget
        for index in range(0, len(cost_vector)):
            candidate = candidate_scores.index(max(candidate_scores))
            if moneyh_to_spend - cost_vector[candidate] < 0:
                # we can't afford more stuff - but there might be a cheaper candidate down the line.
                continue
            # we essentially mark it as terrible
            candidate_scores[candidate] = -math.inf
            winners.append(candidate)
            moneyh_to_spend -= cost_vector[candidate]
        return winners

    @staticmethod
    def compute_scores_with_vector(score_vector, profile):
        candidate_scores = [0] * len(score_vector)
        for preference_order in profile:
            for candidate_index, candidate in enumerate(preference_order):
                candidate_scores[candidate] += score_vector[candidate_index]
        return candidate_scores


class PluralityRule(VotingRule):
    def __init__(self):
        super().__init__("Budget-Plurality rule", 0)

    def get_winners(self, profile, budget, cost_vector):
        candidate_scores = VotingRule.compute_scores_with_vector(profile.plurality_score, profile)
        return self.cut_score(budget, candidate_scores, cost_vector)


class BordaRule(VotingRule):
    def __init__(self):
        super().__init__("Budget-Borda rule", 1)

    def get_winners(self, profile, budget, cost_vector):
        candidate_scores = VotingRule.compute_scores_with_vector(profile.borda_score, profile)
        return self.cut_score(budget, candidate_scores, cost_vector)


class CopelandRule(VotingRule):
    def __init__(self):
        super().__init__("Copeland Rule", 2)

    @staticmethod
    def compute_copeland_score(profile):
        pairwise_wins = profile.compute_pairwise_wins()
        candidate_scores = [0] * profile.number_of_candidates
        for candidate in range(0, profile.number_of_candidates):
            for other_candidate in range(0, profile.number_of_candidates):
                if other_candidate == candidate:
                    continue
                if pairwise_wins[candidate][other_candidate] > 0.5:
                    candidate_scores[candidate] += 1
                else:
                    candidate_scores[candidate] -= 1
        return candidate_scores

    def get_winners(self, profile, budget, cost_vector):
        candidate_scores = CopelandRule.compute_copeland_score(profile)
        return self.cut_score(budget, candidate_scores, cost_vector)


class Knapsack(VotingRule):
    def __init__(self):
        super().__init__("Knapsack Optimization", 3)

    def get_winners(self, profile, budget, cost_vector):
        # we use borda score + 1 to avoid computational errors later on
        candidate_scores = VotingRule.compute_scores_with_vector([x + 1 for x in profile.borda_score], profile)
        ordered_candidate_cost = [(x, cost_vector[x], candidate_scores[x]) for x in range(len(cost_vector))]
        # we order the candidates after cost
        ordered_candidate_cost.sort(key=lambda tup: tup[1])
        candidates = [tup[0] for tup in ordered_candidate_cost]
        ordered_cost_vector = [tup[1] for tup in ordered_candidate_cost]
        # we order the scores according to that ordering
        values = [tup[2] for tup in ordered_candidate_cost]
        knapsack_table = solve_knapsack(budget, ordered_cost_vector, values)
        return get_knapsack_items(knapsack_table, budget, ordered_cost_vector, candidates)


def get_knapsack_items(K, weight, weights, candidates):
    selected_candidates = []
    current_weight = weight
    item_number = len(K) - 1
    while weight != 0 and item_number != 0:
        if K[item_number][current_weight] != K[item_number - 1][current_weight]:
            selected_candidates.append(candidates[item_number - 1])
            weight -= weights[item_number - 1]
        item_number -= 1
    return selected_candidates


def solve_knapsack(W, weights, values):
    n = len(weights)
    K = [[0 for x in range(W + 1)] for x in range(n + 1)]
    # Build table K[][], the knapsack table, in bottom up manner
    for item_count in range(n + 1):
        for weight in range(W + 1):
            # The knapsack table is padded with one extra row and column
            lookup_index = item_count - 1
            # K[0][x] => no items, K[x][0] => no weight
            if item_count == 0 or weight == 0:
                K[item_count][weight] = 0
            # if we can add the item, we should add it if it gives us better results than not
            elif weights[lookup_index] <= weight:
                K[item_count][weight] = max(values[lookup_index] + K[item_count - 1][weight - weights[lookup_index]],
                                            K[item_count - 1][weight])
            # we can't add it => we use previous items which fit
            else:
                K[item_count][weight] = K[item_count - 1][weight]

    return K


class ThetaRule(VotingRule):
    def __init__(self, increment=0.05):
        super().__init__("Theta rule", 4)
        self.increment = increment
        self.final_theta = -1.0

    def get_winners(self, profile, budget, cost_vector):
        pairwise_wins = profile.compute_pairwise_wins()
        winners = []
        theta = 1.0
        budget_finished = False
        while len(winners) != profile.number_of_candidates and not budget_finished:
            for candidate, candidate_wins_prob in enumerate(pairwise_wins):
                if min(candidate_wins_prob) >= theta:
                    if budget - cost_vector[candidate] >= 0:
                        winners.append(candidate)
                        # we mark the candidate as terrible after it has been picked
                        pairwise_wins[candidate] = [-1] * profile.number_of_candidates
                        budget -= cost_vector[candidate]
                    else:
                        budget_finished = True
                        self.final_theta = theta
                        break
            theta -= self.increment
        return winners


class Axiom:
    def __init__(self, name, number):
        self.name = name
        self.number = number

    def is_satisfied(self, rule, profile, budget, cost):
        pass

    def has_value(self):
        pass

    def get_value(self):
        pass


class Unanimity(Axiom):
    def __init__(self):
        super().__init__("Unanimity", 0)

    def is_satisfied(self, rule, profile, budget, cost):
        winners = rule.get_winners(profile, budget, cost)
        winners.sort()
        unanimous_winners = []
        # we assume the profile has unanimous winners
        for candidate in profile[0]:
            if budget - cost[candidate] >= 0:
                unanimous_winners.append(candidate)
                budget -= cost[candidate]
            # if adding the next candidate would go over the budget we stop.
            else:
                break
        unanimous_winners.sort()
        return winners == unanimous_winners

    def has_value(self):
        return False

    def get_value(self):
        pass


class CommitteeMonotonicity(Axiom):
    def __init__(self, max_budget, increment):
        super().__init__("Committee Monotonicity", 1)
        self.max_budget = max_budget
        self.increment = increment

    def is_satisfied(self, rule, profile, budget, cost):
        first_winners = rule.get_winners(profile, budget, cost)
        while budget <= self.max_budget:
            budget += self.increment
            winners = rule.get_winners(profile, budget, cost)
            for winner in first_winners:
                if winner not in winners:
                    return False
        return True

    def has_value(self):
        return False

    def get_value(self):
        pass


class ThetaMinority(Axiom):
    def __init__(self):
        super().__init__("Theta Minority", 2)
        self.value = False
        self.is_present = False

    def is_satisfied(self, rule, profile, budget, cost):
        winners = rule.get_winners(profile, budget, cost)
        winners.sort()
        theta_rule = ThetaRule()
        theta_ority_winners = theta_rule.get_winners(profile, budget, cost)
        theta_ority_winners.sort()
        if winners == theta_ority_winners:
            self.value = theta_rule.final_theta
            self.is_present = True
            return True
        else:
            return False

    def has_value(self):
        return self.is_present

    def get_value(self):
        return self.value


class Regret(Axiom):
    def __init__(self):
        super().__init__("Regret Evaluation", 3)
        # should always be between 1 or 0
        self.value = -1.0

    def is_satisfied(self, rule, profile, budget, cost):
        winners = rule.get_winners(profile, budget, cost)
        knapsack_rule = Knapsack()
        # find optimal utility with knapsack rule
        knapsack_winners = knapsack_rule.get_winners(profile, budget, cost)
        knapsack_utility = profile.compute_utility_of_set(profile.borda_score, knapsack_winners)
        # compute total utility of winners based on borda score
        winners_utility = profile.compute_utility_of_set(profile.borda_score, winners)
        self.value = winners_utility/float(knapsack_utility)
        return True

    def has_value(self):
        return True

    def get_value(self):
        return self.value


class CopelandAxiom(Axiom):
    def __init__(self):
        super().__init__("Copeland Axiom", 4)
        # should always be between 1 or 0
        self.value = 2.0

    def is_satisfied(self, rule, profile, budget, cost):
        winners = rule.get_winners(profile, budget, cost)
        pairwise_wins = profile.compute_pairwise_wins()
        for winner in winners:
            wins = 0
            for competitor in pairwise_wins[winner]:
                if winner == competitor:
                    continue
                # strictly greater
                if pairwise_wins[winner][competitor] > 0.5:
                    wins += 1
            if self.value > wins/float(profile.number_of_candidates - 1):
                self.value = wins/float(profile.number_of_candidates - 1)
        return True

    def has_value(self):
        return True

    def get_value(self):
        return self.value


class GiniCoefficient(Axiom):
    def __init__(self):
        super().__init__("Gini Coefficient", 5)
        # should always be between 1 or 0
        self.value = 2.0

    def is_satisfied(self, rule, profile, budget, cost):
        winners = rule.get_winners(profile, budget, cost)

        voter_scores = [0] * profile.number_of_candidates() #initialize a list of individual voters' regret count
        for preference_order in profile:		#look at one voter in profile
            score = profile.number_of_candidates - 1	#this is the utility score for the top-ranked item of this voter
            for candidate in preference_order:		#go through all candidates in voter's preference_order
                if candidate in winners:		#only add utility if candidate is not in winner set
                    voter_scores[preference_order] += score
                else:
                    continue
                score -= 1
        total_score = 0
        for score1 in voter_scores:
            total_score += score1

        for score1 in voter_scores:		#the following corresponds to two sums over set of voters
            for score2 in voter_scores:
                self.value = abs(score1-score2)/2*len(voter_scores)*total_score

        return True

    def has_value(self):
        return True

    def get_value(self):
        return self.value


def initialize_rule(rule):
    if rule == 0:
        return PluralityRule()
    if rule == 1:
        return BordaRule()
    if rule == 2:
        return CopelandRule()
    if rule == 3:
        return Knapsack()
    if rule == 4:
        return ThetaRule()
    else:
        raise Exception("Illegal rule number: " + str(rule))


def initialize_axiom(axiom, axiom_parameter_1=200, axiom_parameter_2=1):
    if axiom == 0:
        return Unanimity()
    if axiom == 1:
        return CommitteeMonotonicity(axiom_parameter_1, axiom_parameter_2)
    if axiom == 2:
        return ThetaMinority()
    if axiom == 3:
        return Regret()
    if axiom == 4:
        return CopelandAxiom()
    if axiom == 5:
        return GiniCoefficient()
    else:
        raise Exception("Illegal axiom number: " + str(axiom))


def create_cost_distribution(number_of_candidates, cost_distribution, distribution_parameter):
    # uniform
    if cost_distribution == 0:
        return [distribution_parameter] * number_of_candidates
    if cost_distribution == 1:
        std = float(distribution_parameter)
        mean = 100
        size = number_of_candidates
        X = np.random.normal(mean, std, size)
        # we simply round it up
        return X.round().astype(int)
    else:
        raise Exception("Illegal cost distribution: " + str(cost_distribution))


def main():
    from argparse import RawTextHelpFormatter
    parser = argparse.ArgumentParser(description='Computes the winner of given profile',
                                     formatter_class=RawTextHelpFormatter)
    parser.add_argument('preferences', help='A filepath either containing preferences or it does not exist\n'
                                            'If the param "write" is used then the generated preferences will be outputted there.')
    parser.add_argument('--write', action='store_true', help="Set if the generated profile should be saved to a file")
    parser.add_argument('-c', '--cost', type=int, default=1, help='The cost distribution to use over candidates\n'
                                                                  '0 = uniform cost of 1 for item\n'
                                                                  '1 = Normal distribution with mean=100, and std=15')
    parser.add_argument('-r', '--rule', type=int, default=0, help='The rule to decide the winner\n'
                                                                  '0 = budget-plurality\n'
                                                                  '1 = budget-borda\n'
                                                                  '2 = copeland\n'
                                                                  '3 = knapsack\n')
    parser.add_argument('--axiom', type=int, default=0, help='The axiom the check the rule against\n'
                                                             '0 = Unanimity\n')
    parser.add_argument('-b', '--budget', type=int, default=10, help='The total budget to be used')
    parser.add_argument('--voters', type=int, default=10, help='The number of voters')
    parser.add_argument('--candidates', type=int, default=10, help='The number of candidates')
    parser.add_argument('--base', type=int, default=3, help='The number base preference orders')
    parser.add_argument('--swaps', type=int, default=1, help='The number of swaps to do for each preference order')
    parser.add_argument('--noise', type=int, default=2, help='The noise parameter')
    # group = parser.add_mutually_exclusive_group()
    # group.add_argument('-v', '--verbose', action='store_true')
    # group.add_argument('-q', '--quiet', action='store_true')
    args = parser.parse_args()

    if not args.write:
        profile = data.read_from_file(args.preferences)
        rule = initialize_rule(args.rule)
        cost_vector = create_cost_distribution(profile.number_of_candidates, args.cost, 15)
        winner_set = rule.get_winners(profile, args.budget, cost_vector)
        axiom = initialize_axiom(args.axiom)
        satisfied = axiom.is_satisfied(rule, profile, args.budget, cost_vector)
        if satisfied:
            print(rule.name + " satisfies " + axiom.name)
            if axiom.has_value():
                print("value: " + str(axiom.get_value()))
        else:
            print(rule.name + " does not satisfy " + axiom.name)
        #        total_cost = 0
        #        for winner in winner_set:
        #            print(str(winner) + " " + str(cost_vector[winner]))
        #           total_cost += cost_vector[winner]
        #        print(" ".join([str(total_cost), str(args.budget)]))

    else:
        profile = data.create_noisy_data(args.voters, args.candidates, args.base, args.swaps, args.noise)
        data.write_to_file(args.preferences, profile)


if __name__ == "__main__":
    main()
