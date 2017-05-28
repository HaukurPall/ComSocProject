import model
import random
import math


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
            preference_order = [int(x) - 1 for x in preference_order]
            preference_list.append(model.Preference(preference_order))
        return model.Profile(number_of_voters, number_of_candidates, preference_list)


def write_to_file(file_name, profile):
    with open(file_name, "w") as file:
        file.write(str(profile.number_of_candidates) + "\n")
        for candidate in range(profile.number_of_candidates):
            file.write(str(candidate + 1) + ",candidate" + "\n")
        file.write(",".join([str(profile.number_of_voters), str(profile.number_of_voters), str(profile.unique_votes)]) + "\n")

        for preference in profile:
            file.write(",".join([str(x + 1) for x in preference]) + "\n")


def create_noisy_data(number_of_voters=10,
                      number_of_candidates=10,
                      number_of_base_preferences=1,
                      swaps=1,
                      noisy_parameter=2):
    list_of_preferences = []
    avg = number_of_voters / number_of_base_preferences
    last = 0.0
    # generate all the base profiles
    while last < number_of_voters:
        preference_order = model.Preference.generate_random_preference_order(number_of_candidates)
        for voter in range(int(last), int(last + avg)):
            list_of_preferences.append(preference_order.get_copy())
        last += avg

    # apply noise to the whole profile
    for preference in list_of_preferences:
        for swap in range(swaps):
            swap_candidate = random.randint(0, number_of_candidates - 1)
            direction = random.randint(0, 1)
            distance = 1
            # we swap upwards
            if direction == 0:
                while swap_candidate - distance >= 0:
                    if random.random() <= noisy_distribution(distance, noisy_parameter):
                        preference.index_based_swap(swap_candidate, swap_candidate - distance)
                        break
                    distance += 1

            else:
                while swap_candidate + distance <= preference.get_number_of_candidates() - 1:
                    if random.random() <= noisy_distribution(distance, noisy_parameter):
                        preference.index_based_swap(swap_candidate, swap_candidate + distance)
                        break
                    distance += 1

    return model.Profile(number_of_voters, number_of_candidates, list_of_preferences)


def noisy_distribution(distance, noisy_parameter):
    return 1 / math.pow(distance + 1, noisy_parameter)
