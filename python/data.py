import model
import random
import math
import copy
from collections import Counter as Counter


def read_from_file(file_path):
    with open(file_path, "r") as file:
        file_list = list(file)
        index = 0
        number_of_candidates = int(file_list[index].strip())
        index += 1

        for i in range(0, number_of_candidates):
            number, name = file_list[index].strip().split(",")
            index += 1
            # we consider candidates to be [0;m-1], not [1;m]
            number = int(number) - 1
        number_of_voters, vote_count, unique_ballots = file_list[index].strip().split(",")
        index += 1
        number_of_voters = int(number_of_voters)

        preference_list = []
        for line in file_list[index:]:
            preference_order = line.strip().split(",")
            preference_order = [int(x) for x in preference_order]
            preference_count = preference_order[0]
            for count in range(preference_count):
                preference_list.append(model.Preference([x - 1 for x in preference_order[1:]]))
        return model.Profile(number_of_voters, number_of_candidates, preference_list)


def write_to_file(file_name, profile):
    with open(file_name, "w") as file:
        file.write(str(profile.number_of_candidates) + "\n")
        for candidate in range(profile.number_of_candidates):
            file.write(str(candidate + 1) + ",candidate" + "\n")

        counter = Counter()
        for preference in profile:
            preference_name = ",".join([str(x + 1) for x in preference])
            counter[preference_name] += 1
        file.write(",".join([str(sum(counter.values())), str(sum(counter.values())), str(len(list(counter)))]) + "\n")

        for preference_name, preference_count in counter.most_common():
            file.write(",".join([str(preference_count), preference_name]) + "\n")


def replicate_preference_order(preference_order, number_of_times):
    list_of_preferences = []
    for i in range(number_of_times):
        list_of_preferences.append(preference_order)
    return model.Profile(number_of_times, len(preference_order.preference_order), list_of_preferences)


def apply_noise(profile, swaps=1,
                noisy_parameter=2):
    # apply noise to the whole profile
    profile = profile.get_copy()
    for preference_order in profile:
        for swap in range(swaps):
            swap_candidate = random.randint(0, profile.number_of_candidates - 1)
            direction = random.randint(0, 1)
            distance = 1
            # we swap upwards
            if direction == 0:
                while swap_candidate - distance >= 0:
                    if random.random() <= noisy_distribution(distance, noisy_parameter):
                        preference_order.index_based_swap(swap_candidate, swap_candidate - distance)
                        break
                    distance += 1

            else:
                while swap_candidate + distance <= preference_order.get_number_of_candidates() - 1:
                    if random.random() <= noisy_distribution(distance, noisy_parameter):
                        preference_order.index_based_swap(swap_candidate, swap_candidate + distance)
                        break
                    distance += 1

    return profile


def noisy_distribution(distance, noisy_parameter):
    return 1 / math.pow(distance + 1, noisy_parameter)
