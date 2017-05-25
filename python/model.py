# Authors: Haukur Pall Jonsson, Silvan Hungerbuhler, Max Rapp and Greg Liowski
# Date: 20th May 2017
import copy
import random
import math
import argparse
import data

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
        unique_preference_set = set()
        for preference in preference_list:
            if str(preference) not in unique_preference_set:
                unique_preference_set.add(str(preference))
        self.unique_votes = len(unique_preference_set)

    def __str__(self):
        profile = ""
        for preference_order_index, preference_order in enumerate(self.preference_list):
            profile += str(preference_order) + "\n"
        return profile

    def __getitem__(self, index):
        return self.preference_list[index]

    def is_x_majority_winner_over_y(self, our_candidate, other_candidate):
        wins = 0
        for preference_order in self.preference_list:
            if preference_order.is_x_more_preferred_than_y(our_candidate, other_candidate):
                wins += 1
        # strictly greater
        return float(wins)/float(self.number_of_voters) > 0.5


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


class PluralityRule(VotingRule):
    def __init__(self):
        super().__init__("Budget-Plurality rule", 0)

    def get_winners(self, profile, budget, cost_vector):
        candidate_scores = [0] * profile.number_of_candidates
        for preference in profile:
            candidate_scores[preference.get_first_candidate()] += 1
        return self.cut_score(budget, candidate_scores, cost_vector)


class BordaRule(VotingRule):
    def __init__(self):
        super().__init__("Budget-Borda rule", 1)

    def get_winners(self, profile, budget, cost_vector):
        candidate_scores = [0] * profile.number_of_candidates
        for preference_order in profile:
            score = profile.number_of_candidates - 1
            for candidate in preference_order:
                candidate_scores[candidate] += score
                score -= 1
        return self.cut_score(budget, candidate_scores, cost_vector)


class CopelandRule(VotingRule):
    def __init__(self):
        super().__init__("Copeland Rule", 2)

    def get_winners(self, profile, budget, cost_vector):
        candidate_scores = [0] * profile.number_of_candidates
        for candidate in range(0, profile.number_of_candidates):
            for other_candidate in range(0, profile.number_of_candidates):
                if other_candidate == candidate:
                    continue
                if profile.is_x_majority_winner_over_y(candidate, other_candidate):
                    candidate_scores[candidate] += 1
                else:
                    candidate_scores[candidate] -= 1

        return self.cut_score(budget, candidate_scores, cost_vector)


class Knapsack(VotingRule):
    def __init__(self):
        super().__init__("Knapsack Optimization", 3)

    def get_winners(self, profile, budget, cost_vector):
        candidate_scores = [0] * profile.number_of_candidates
        for preference_order in profile:
            # instead of using borda scores we use borda score + 1.
            # This solves a problem when we are finding the knapsack items.
            score = profile.number_of_candidates
            for candidate in preference_order:
                candidate_scores[candidate] += score
                score -= 1
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


def initialize_rule(rule):
    if rule == 0:
        return PluralityRule()
    if rule == 1:
        return BordaRule()
    if rule == 2:
        return CopelandRule()
    if rule == 3:
        return Knapsack()
    else:
        raise Exception("Illegal rule number: " + str(rule))


def create_cost_distribution(number_of_candidates, cost_distribution, distribution_parameter):
    # uniform
    if cost_distribution == 0:
        return [distribution_parameter] * number_of_candidates
    else:
        raise Exception("Illegal cost distribution: " + str(cost_distribution))

def main():
    from argparse import RawTextHelpFormatter
    parser = argparse.ArgumentParser(description='Computes the winner of given profile',
                                     formatter_class=RawTextHelpFormatter)
    parser.add_argument('preferences', help='A filepath either containing preferences or it does not exist\n'
                                            'If the param "write" is used then the generated preferences will be outputted there.')
    parser.add_argument('--write', action='store_true', help="Set if the generated profile should be saved to a file")
    parser.add_argument('-c', '--cost', type=int, default=0, help='The cost distribution to use over candidates\n'
                                                                  '0 = uniform cost of 1 for item')
    parser.add_argument('-r', '--rule', type=int, default=0, help='The rule to decide the winner\n'
                                                                  '0 = budget-plurality\n'
                                                                  '1 = budget-borda\n'
                                                                  '2 = copeland\n'
                                                                  '3 = knapsack\n')
    parser.add_argument('-b', '--budget', type=int, default=10, help='The total budget to be used')
    parser.add_argument('--voters', type=int, default=10, help='The number of voters')
    parser.add_argument('--candidates', type=int, default=10, help='The number of candidates')
    parser.add_argument('--base', type=int, default=3, help='The number base preference orders')
    parser.add_argument('--swaps', type=int, default=1, help='The number of swaps to do for each preference order')
    parser.add_argument('--noise', type=int, default=2, help='The noise parameter')
    #group = parser.add_mutually_exclusive_group()
    #group.add_argument('-v', '--verbose', action='store_true')
    #group.add_argument('-q', '--quiet', action='store_true')
    args = parser.parse_args()

    if not args.write:
        profile = data.read_from_file(args.preferences)
        rule = initialize_rule(args.rule)
        cost_vector = create_cost_distribution(profile.number_of_candidates, args.cost, 1)
        winner_set = rule.get_winners(profile, args.budget, cost_vector)
        total_cost = 0
        for winner in winner_set:
            print(str(winner) + " " + str(cost_vector[winner]))
            total_cost += cost_vector[winner]
        print(" ".join([str(total_cost), str(args.budget)]))
    else:
        profile = data.create_noisy_data(args.voters, args.candidates, args.base, args.swaps, args.noise)
        data.write_to_file(args.preferences, profile)


if __name__ == "__main__":
    main()
