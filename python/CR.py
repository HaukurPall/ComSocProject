import model
import data
import argparse
import os

def initialize_rule(rule):
    if rule == 0:
        return model.PluralityRule()
    if rule == 1:
        return model.BordaRule()
    if rule == 2:
        return model.CopelandRule()
    if rule == 3:
        return model.Knapsack()
    if rule == 4:
        return model.ThetaRule()
    else:
        raise Exception("Illegal rule number: " + str(rule))


def initialize_axiom(axiom):
    if axiom == 0:
        return model.Unanimity()
    if axiom == 1:
        return model.CommitteeMonotonicity(400, 100)
    if axiom == 2:
        return model.ThetaMinority()
    if axiom == 3:
        return model.Regret()
    if axiom == 4:
        return model.CopelandAxiom()
    if axiom == 5:
        return model.GiniCoefficient()
    if axiom == 6:
        return model.BudgetEfficiency()
    else:
        raise Exception("Illegal axiom number: " + str(axiom))


def create_cost_distribution(number_of_candidates, cost_distribution):
    if cost_distribution == 0:
        return model.NormalDistribution(100, 15).associate_cost(number_of_candidates)
    else:
        raise Exception("Illegal cost distribution: " + str(cost_distribution))


def main():
    from argparse import RawTextHelpFormatter
    parser = argparse.ArgumentParser(description='Computes the winner of given profile',
                                     formatter_class=RawTextHelpFormatter)
    parser.add_argument('--preferences', help='A filepath either containing preferences or it does not exist\n'
                                            'If the param "write" is used then the generated preferences will be outputted there.')
    parser.add_argument('--write', action='store_true', help="Set if the generated profile should be saved to a file")
    parser.add_argument('--generate', action='store_true', help="Run generate-profiles code block")
    parser.add_argument('--read', action='store_true', help="Run read-profiles code block")
    parser.add_argument('--cost', type=int, default=1, help='The cost distribution to use over candidates\n'
                                                                  '0 = Normal distribution with mean=100, and std=15\n')
    parser.add_argument('--rule', type=int, default=0, help='The rule to decide the winner\n'
                                                                  '0 = budget-plurality\n'
                                                                  '1 = budget-borda\n'
                                                                  '2 = copeland\n'
                                                                  '3 = knapsack\n'
                                                                  '4 = theta rule\n')
    parser.add_argument('--axiom', type=int, default=0, help='The axiom the check the rule against\n'
                                                             '0 = Unanimity\n'
                                                             '1 = Committee Monotonicity\n'
                                                             '2 = Theta Minority\n'
                                                             '3 = Regret\n'
                                                             '4 = Copeland Axiom\n'
                                                             '5 = Gini Coefficient\n')
    parser.add_argument('--budget', type=int, default=10, help='The total budget to be used')
    parser.add_argument('--voters', type=int, default=10, help='The number of voters')
    parser.add_argument('--candidates', type=int, default=10, help='The number of candidates')
    parser.add_argument('--base', type=int, default=3, help='The number base preference orders')
    parser.add_argument('--swaps', type=int, default=1, help='The number of swaps to do for each preference order')
    parser.add_argument('--noise', type=int, default=2, help='The noise parameter')
    # group = parser.add_mutually_exclusive_group()
    # group.add_argument('-v', '--verbose', action='store_true')
    # group.add_argument('-q', '--quiet', action='store_true')
    args = parser.parse_args()

    if args.generate:
        run_polar_generation()
        return

    if args.read:
        read_data_set()
        return

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


def run_base_generation():
    for i in range(100):
        voters = 5000
        candidates = 10
        bases = 1
        swaps = 2
        directory = "cluster_1"
        preference_order = model.Preference([x for x in range(0, candidates)])
        random_order = preference_order.generate_random_preference_order()
        profile = data.replicate_preference_order(random_order, int(voters/bases))
        for base in range(bases - 1):
            random_order = preference_order.generate_random_preference_order()
            profile = profile + data.replicate_preference_order(random_order, int(voters/bases))
        data.apply_noise(profile, swaps, 1)
        if not os.path.exists(directory):
            os.makedirs(directory)
        data.write_to_file(os.path.join(directory, "{}_v{}:c{}:b{}:s{}".format(i, voters, candidates, bases, swaps) + ".txt"), profile)


def run_polar_generation():
    for i in range(100):
        voters = 5000
        candidates = 10
        bases = 2
        swaps = 2
        directory = "cluster_2_polar"
        preference_order = model.Preference([x for x in range(0, candidates)])
        first_order = preference_order.generate_random_preference_order()
        second_order = first_order.reverse_preference_order()
        first_profile = data.replicate_preference_order(first_order, int(voters / bases))
        second_profile = data.replicate_preference_order(second_order, int(voters / bases))
        profile = first_profile + second_profile
        data.apply_noise(profile, swaps, 1)

        if not os.path.exists(directory):
            os.makedirs(directory)
        data.write_to_file(os.path.join(directory, "{}_v{}:c{}:b{}:s{}".format(i, voters, candidates, bases, swaps) + ".txt"), profile)


def run_similar_generation():
    for i in range(100):
        voters = 5000
        candidates = 10
        bases = 2
        swaps = 3
        directory = "cluster_2_similar"
        preference_order = model.Preference([x for x in range(0, candidates)])
        first_order = preference_order.generate_random_preference_order()
        profile, swaps = get_similar_profile(bases, first_order, swaps, voters)

        if not os.path.exists(directory):
            os.makedirs(directory)
        data.write_to_file(os.path.join(directory, "{}_v{}:c{}:b{}:s{}".format(i, voters, candidates, bases, swaps) + ".txt"), profile)


def get_similar_profile(bases, first_order, swaps, voters):
    second_order = first_order.get_copy()
    first_profile = data.replicate_preference_order(first_order, int(voters / bases))
    second_profile = data.replicate_preference_order(second_order, 1)
    data.apply_noise(second_profile, swaps, 1)
    second_profile = data.replicate_preference_order(second_profile.preference_list[0], int(voters / bases))
    profile = first_profile + second_profile
    swaps = 250
    data.apply_noise(profile, swaps, 1)
    return profile, swaps


def read_data_set():
    from os import listdir
    from os.path import isfile, join
    directory = "random"
    onlyfiles = [f for f in listdir(directory) if isfile(join(directory, f))]

    budget = 500

    rules = [model.PluralityRule(),
             model.BordaRule(),
             model.CopelandRule(),
             model.Knapsack(),
             model.ThetaRule()]
    axioms_but_unanimity = [model.CommitteeMonotonicity(budget*10, budget),
                            model.ThetaMinority(),
                            model.Regret(),
                            model.CopelandAxiom(),
                            model.GiniCoefficient(),
                            model.BudgetEfficiency()]
    profile_number = 0
    outcome = []
    for file in onlyfiles:
        if "c1000:" not in file:
            continue
        profile_number += 1
        profile = data.read_from_file(join(directory, file))
        cost_vector = create_cost_distribution(profile.number_of_candidates, 0)
        print(str(profile_number))
        for rule in rules:
            winners = rule.get_winners(profile, budget, cost_vector)
            for axiom in axioms_but_unanimity:
                satisfied = axiom.is_satisfied(rule, winners, profile, budget, cost_vector)
                if satisfied:
                    if axiom.has_value():
                        outcome.append((rule.number, axiom.number, profile_number, axiom.get_value()))
                    else:
                        outcome.append((rule.number, axiom.number, profile_number, 1))
                else:
                    outcome.append((rule.number, axiom.number, profile_number, 0))
    write_conlusions_to_file(outcome, "greg_test.csv")


def write_conlusions_to_file(outcome, filename):
    with open(filename, "w") as file:
        for line in outcome:
            file.write(",".join([str(line[0]), str(line[1]), str(line[2]), str(line[3])]) + "\n")

if __name__ == "__main__":
    main()
