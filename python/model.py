# Authors: Haukur Pall Jonsson, Silvan Hungerbuhler, Max Rapp and Greg Liowski
# Date: 20th May 2017
import copy
import random
import numpy as np

class Preference:
    """
    :param list_of_preferences: orderer list of integers, in which integer is a unique candidate, first candidate is 0
    """

    def __init__(self, preference_order):
        self.preference_order = np.array([int(x) for x in preference_order])
        self.standard_set = set([x for x in range(0, len(preference_order))])

    def __eq__(self, other):
        return self.preference_order == other.preference_order

    def __getitem__(self, index):
        return self.preference_order[index]

    """
    Returns True if x is more preferred than y
    """

    def is_x_more_preferred_than_y(self, x, y):
        return np.where(self.preference_order == x) < np.where(self.preference_order == y)

    """
    Generates a random preference order over a uniform distribution.
    """

    def generate_random_preference_order(self):
        preference_list = random.sample(self.standard_set, len(self.standard_set))
        return Preference(preference_list)

    def reverse_preference_order(self):
        return Preference(self.preference_order[::-1])

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
            raise Exception("The reported number of voters {} does not equal the ballot {}".format(self.number_of_voters, len(preference_list)))
        if self.number_of_candidates != preference_list[0].get_number_of_candidates():
            raise Exception("The reported number of candidates "+ str(self.number_of_candidates) + " does not equal the ballot" + str(preference_list[0].get_number_of_candidates()))
        self.borda_score = [x for x in range(self.number_of_candidates - 1, -1, -1)]
        self.plurality_score = [0 for x in range(self.number_of_candidates)]
        self.plurality_score[0] = 1
        self.P = None
        self.computed = False

    def __add__(self, other):
        if self.number_of_candidates != other.number_of_candidates:
            raise Exception("Not the same number of candidates!")
        return Profile(self.number_of_voters + other.number_of_voters,
                       self.number_of_candidates,
                       self.preference_list + other.preference_list)

    def __str__(self):
        profile = ""
        for preference_order_index, preference_order in enumerate(self.preference_list):
            profile += str(preference_order) + "\n"
        return profile

    def __getitem__(self, index):
        return self.preference_list[index]

    def get_copy(self):
        new_list = []
        for preference_order in self.preference_list:
            new_list.append(copy.deepcopy(preference_order))
        return Profile(self.number_of_voters, self.number_of_candidates, new_list)

    def compute_pairwise_wins(self):
        if self.P:
            return self.P
        P = [[0 for x in range(self.number_of_candidates)] for x in range(self.number_of_candidates)]
        for preference_order in self.preference_list:
            for candidate in range(self.number_of_candidates):
                for other_candidate in range(self.number_of_candidates):
                    # majority contest against one self = win, for simplifying later computation
                    if other_candidate == candidate:
                        P[candidate][other_candidate] += 1
                        continue
                    if other_candidate < candidate:
                        continue
                    if preference_order.is_x_more_preferred_than_y(candidate, other_candidate):
                        P[candidate][other_candidate] += 1
                    else:
                        P[other_candidate][candidate] += 1
        P = [[wins / float(self.number_of_voters) for wins in candidate] for candidate in P]
        self.P = P
        return P

    #def compute_pairwise_wins(self):
    #    if self.computed:
    #        return self.P
    #    P = np.identity(self.number_of_candidates)
    #    for preference_order in self.preference_list:
    #        for i in range(self.number_of_candidates - 1):
    #            winner = preference_order[i]
    #            worse_candidates = preference_order[i + 1:]
    #           for loser in worse_candidates:
    #                P[winner][loser] += 1
    #   P /= float(self.number_of_voters)
    #    self.P = P
    #    self.computed = True
    #    return P

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

    def rank_candidates(self, profile):
        pass

    def has_scoring(self):
        pass

    """
    Returns a list of winners using the score and cut method.
    Chooses the highest candidate which does not cost more than the remaining budget.
    """
    @staticmethod
    def cut_score(budget, candidate_ranks, cost_vector):
        winners = []
        moneyh_to_spend = budget
        for index in range(len(cost_vector)):
            candidate = candidate_ranks[index]
            if moneyh_to_spend - cost_vector[candidate] < 0:
                # we can't afford more stuff - but there might be a cheaper candidate down the line.
                continue
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
        candidate_ranks = self.rank_candidates(profile)
        return self.cut_score(budget, candidate_ranks, cost_vector)

    def rank_candidates(self, profile):
        score = VotingRule.compute_scores_with_vector(profile.plurality_score, profile)
        ordered_score = [(x, score[x]) for x in range(len(score))]
        ordered_score.sort(key=lambda tup: tup[1])
        return [candidate[0] for candidate in ordered_score]

    def has_scoring(self):
        return True


class BordaRule(VotingRule):
    def __init__(self):
        super().__init__("Budget-Borda rule", 1)

    def get_winners(self, profile, budget, cost_vector):
        candidate_ranks = self.rank_candidates(profile)
        return self.cut_score(budget, candidate_ranks, cost_vector)

    def rank_candidates(self, profile):
        score = VotingRule.compute_scores_with_vector(profile.borda_score, profile)
        ordered_score = [(x, score[x]) for x in range(len(score))]
        ordered_score.sort(key=lambda tup: tup[1])
        return [candidate[0] for candidate in ordered_score]

    def has_scoring(self):
        return True


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
        candidate_ranks = self.rank_candidates(profile)
        return self.cut_score(budget, candidate_ranks, cost_vector)

    def rank_candidates(self, profile):
        score = CopelandRule.compute_copeland_score(profile)
        ordered_score = [(x, score[x]) for x in range(len(score))]
        ordered_score.sort(key=lambda tup: tup[1])
        return [candidate[0] for candidate in ordered_score]

    def has_scoring(self):
        return True


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

    def rank_candidates(self, profile):
        pass

    def has_scoring(self):
        return False


def get_knapsack_items(K, weight, weights, candidates):
    selected_candidates = []
    item_index = len(K) - 1
    while weight != 0 and item_index != 0:
        candidate_index = item_index - 1
        if K[item_index][weight] != K[item_index - 1][weight]:
            selected_candidates.append(candidates[candidate_index])
            weight -= weights[candidate_index]
            # we reset our counter
            item_index = len(K)
        item_index -= 1
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
    def __init__(self):
        super().__init__("Theta rule", 4)
        self.final_theta = -1.0

    def rank_by_theta(self, profile):
        pairwise_wins = profile.compute_pairwise_wins()
        ordered_domination = []
        for candidate, candidate_wins_prob in enumerate(pairwise_wins):
            ordered_domination.append((candidate, min(candidate_wins_prob)))
        ordered_domination.sort(key=lambda tup: tup[1], reverse=True)
        return ordered_domination

    def get_winners(self, profile, budget, cost_vector):
        winners = []
        budget_finished = False
        ordered_domination = self.rank_by_theta(profile)
        while not budget_finished and len(winners) == profile.number_of_candidates:
            candidate, obs_theta = ordered_domination[0]
            if budget - cost_vector[candidate] >= 0:
                budget -= cost_vector[candidate]
                ordered_domination = ordered_domination[1:]
                winners.append(candidate)
                self.final_theta = obs_theta
            else:
                budget_finished = True
        # we check if we can fill the budget even more
        for obs_pair in ordered_domination:
            candidate, obs_theta = obs_pair
            if budget - cost_vector[candidate] >= 0:
                budget -= cost_vector[candidate]
                winners.append(candidate)
        return winners

    def rank_candidates(self, profile):
        return [candidate[0] for candidate in self.rank_by_theta(profile)]

    def has_scoring(self):
        return True


class Axiom:
    def __init__(self, name, number):
        self.name = name
        self.number = number

    def is_satisfied(self, rule, winners, profile, budget, cost):
        pass

    def has_value(self):
        pass

    def get_value(self):
        pass


class Unanimity(Axiom):
    def __init__(self):
        super().__init__("Unanimity", 0)

    def is_satisfied(self, rule, winners, profile, budget, cost):
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

    def is_satisfied(self, rule, winners, profile, budget, cost):
        if rule.has_scoring():
            candidate_ranking = rule.rank_candidates(profile)
            total_winners = len(winners)
            for winner in winners:
                if candidate_ranking.index(winner) >= total_winners:
                    return False
        else:
            while budget <= self.max_budget:
                budget += self.increment
                new_winners = rule.get_winners(profile, budget, cost)
                for winner in winners:
                    if winner not in new_winners:
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

    def is_satisfied(self, rule, winners, profile, budget, cost):
        theta_rule = ThetaRule()
        theta_ority_winners = theta_rule.get_winners(profile, budget, cost)
        pairwise_wins = profile.compute_pairwise_wins()
        last_theta = 1.0
        for winner_index, winner in enumerate(theta_ority_winners):
            if min(pairwise_wins[winner]) < theta_rule.final_theta:
                last_theta = theta_rule.final_theta
                break
            if winner in winners:
                last_theta = min(pairwise_wins[winner])
            else:
                break
        self.value = last_theta
        return True

    def has_value(self):
        return True

    def get_value(self):
        return self.value


class Regret(Axiom):
    def __init__(self):
        super().__init__("Regret Evaluation", 3)
        # should always be between 1 or 0
        self.value = -1.0

    def is_satisfied(self, rule, winners, profile, budget, cost):
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

    def is_satisfied(self, rule, winners, profile, budget, cost):
        score = CopelandRule.compute_copeland_score(profile)
        ordered_score = [(x, score[x]) for x in range(len(score))]
        ordered_score.sort(key=lambda tup: tup[1])
        copland_ranks = [candidate[0] for candidate in ordered_score]
        pairwise_wins = profile.compute_pairwise_wins()
        lowest = 1.0
        for winner in copland_ranks:
            if winner not in winners:
                break
            else:
                wins = 0
                for competitor in pairwise_wins[winner]:
                    if winner == competitor:
                        continue
                    else:
                        wins += 1
                lowest = wins/(profile.number_of_candidates - 1)
        self.value = lowest
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

    def is_satisfied(self, rule, winners, profile, budget, cost):
        voter_scores = [0] * profile.number_of_candidates #initialize a list of individual voters' regret count
        for preference_order in profile:		#look at one voter in profile
            score = profile.number_of_candidates - 1	#this is the utility score for the top-ranked item of this voter
            for candidate in preference_order:		#go through all candidates in voter's preference_order
                if candidate in winners:		#only add utility if candidate is not in winner set
                    voter_scores[candidate] += score
                else:
                    continue
                score -= 1
        total_score = 0.0
        for score1 in voter_scores:
            total_score += score1

        score = 0.0
        for score1 in voter_scores:		#the following corresponds to two sums over set of voters
            for score2 in voter_scores:
                score += abs(score1-score2)
        self.value = score/float(2*len(voter_scores)*total_score)

        return True

    def has_value(self):
        return True

    def get_value(self):
        return self.value


class BudgetEfficiency(Axiom):
    def __init__(self):
        super().__init__("Budget Efficiency", 6)
        self.value = 0.0

    def is_satisfied(self, rule, winners, profile, budget, cost):
        used_budget = 0
        for winner in winners:
            used_budget += cost[winner]
        self.value = used_budget/budget
        return True

    def has_value(self):
        return True

    def get_value(self):
        return self.value


class CostDistribution:

    def __init__(self, name, number):
        self.name = name
        self.number = number

    def associate_cost(self, number_of_candidates):
        pass


class NormalDistribution(CostDistribution):

    def __init__(self, mean, std):
        super().__init__("Normal distribution", 0)
        self.mean = mean
        self.std = std

    def associate_cost(self, number_of_candidates):
        X = np.random.normal(self.mean, self.std, number_of_candidates)
        # we simply round it up
        return X.round().astype(int)