# Authors: Haukur Pall Jonsson, Silvan Hungerbuhler, Max Rapp and Greg Liowski
# Date: 20th May 2017
import copy
import unittest
import argparse


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
    def __init__(self, identifier, description, number_of_voters, number_of_candidates, preference_list):
        self.identifier = identifier
        self.description = description
        self.number_of_voters = number_of_voters
        self.number_of_candidates = number_of_candidates
        self.preference_list = preference_list
        if self.number_of_voters != len(preference_list):
            raise Exception("The reported number of voters does not equal the ballot")
        if self.number_of_candidates != preference_list[0].get_number_of_candidates():
            raise Exception("The reported number of candidates does not equal the ballot")

    def __str__(self):
        profile = "Identifier: " + self.identifier + "\n"
        profile += "Description: " + self.description + "\n"
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
            # we essentially mark it
            candidate_scores[candidate] = -1
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
            score = profile.get_number_of_candidates() - 1
            for candidate in preference_order:
                candidate_scores[candidate] += score
                score -= 1
        self.cut_score(budget, candidate_scores, cost_vector)


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


def initialize_rule(rule):
    if rule == 0:
        return PluralityRule()
    if rule == 1:
        return BordaRule()
    if rule == 2:
        return CopelandRule()
    else:
        raise Exception("Illegal rule number: " + str(rule))


def read_preferences(file_path):
    with open(file_path, "r") as file:
        file_list = list(file)
        indentifier = file_list[0].strip()
        description = file_list[1].strip()
        number_of_voters = int(file_list[2])
        number_of_candidates = int(file_list[3])
        preference_list = []
        for line in file_list[4:]:
            preference_list.append(Preference(line.strip().split(" ")))
        return Profile(indentifier, description, number_of_voters, number_of_candidates, preference_list)


def create_cost_distribution(number_of_candidates, cost_distribution, distribution_parameter):
    # uniform
    if cost_distribution == 0:
        return [distribution_parameter] * number_of_candidates
    else:
        raise Exception("Illegal cost distribution: " + str(cost_distribution))


def main():
    parser = argparse.ArgumentParser(description='Computes the winner of given profile')
    group = parser.add_mutually_exclusive_group()
    parser.add_argument('preferences', help='A file containing the preferences. '
                                            'The file needs to be formatted correctly')
    parser.add_argument('--cost', type=int, default=0, help='The cost distribution to use over candidates')
    parser.add_argument('--rule', type=int, default=0, help='The rule to decide the winner. 1=k-plurality')
    parser.add_argument('--budget', type=float, default=10.0, help='The total budget to be used')
    group.add_argument('-v', '--verbose', action='store_true')
    group.add_argument('-q', '--quiet', action='store_true')
    args = parser.parse_args()

    profile = read_preferences(args.preferences)
    rule = initialize_rule(args.rule)
    cost_vector = create_cost_distribution(profile.number_of_candidates, args.cost, 1)
    winner_set = rule.get_winners(profile, args.budget, cost_vector)
    total_cost = 0.0
    for winner in winner_set:
        print(str(winner) + " " + str(cost_vector[winner]))
        total_cost += cost_vector[winner]
    print(" ".join([str(total_cost), str(args.budget)]))


if __name__ == "__main__":
    main()
