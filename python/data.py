import model


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
        file.write(str(profile.number_of_candidates))
        for candidate in range(profile.number_of_candidates):
            file.write(str(candidate + 1) + ",candidate")
        file.write(",".join([str(profile.number_of_voters), str(profile.number_of_voters), str(profile.unique_votes)]))

        for preference in profile:
            file.write(",".join([str(x + 1) for x in preference]))
