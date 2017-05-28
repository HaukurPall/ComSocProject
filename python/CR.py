import model
import data
import argparse
import numpy as np

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


def initialize_axiom(axiom, axiom_parameter_1=200, axiom_parameter_2=1):
    if axiom == 0:
        return model.Unanimity()
    if axiom == 1:
        return model.CommitteeMonotonicity(axiom_parameter_1, axiom_parameter_2)
    if axiom == 2:
        return model.ThetaMinority()
    if axiom == 3:
        return model.Regret()
    if axiom == 4:
        return model.CopelandAxiom()
    if axiom == 5:
        return model.GiniCoefficient()
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
    parser.add_argument('preferences', help='A filepath either containing preferences or it does not exist\n'
                                            'If the param "write" is used then the generated preferences will be outputted there.')
    parser.add_argument('--write', action='store_true', help="Set if the generated profile should be saved to a file")
    parser.add_argument('-c', '--cost', type=int, default=1, help='The cost distribution to use over candidates\n'
                                                                  '0 = Normal distribution with mean=100, and std=15\n')
    parser.add_argument('-r', '--rule', type=int, default=0, help='The rule to decide the winner\n'
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
