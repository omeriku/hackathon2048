
import random

def divide_to_groups(all_teams):
    one_group = []
    two_group = []
    all_teams = dict(all_teams)
    data = []
    for team in all_teams:
        data.append((team, all_teams[team]))

    random.shuffle(data)
    half_num_of_teams = int(len(all_teams)/2)

    one_group = data[:half_num_of_teams]
    two_group = data[half_num_of_teams:]

    return one_group, two_group
