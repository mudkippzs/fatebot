import json
import os
from collections import defaultdict


def main():
    # get the path of the log file
    dir_path = os.path.dirname(os.path.realpath("/home/dev/Code/fatebot/"))
    log_file = os.path.join(dir_path, 'fatebot', 'dicelogs.json')

    # open the log file and load it as a json object
    with open(log_file, 'r') as f:
        logs = json.load(f)

    # create a dictionary to store the success rate for each player
    success_rate = defaultdict(list)
    total_count = 0
    # iterate through each log in the logs list and calculate the success rate for each player
    for player in logs:
        # get the player name from the log and add it to the success rate dictionary if it doesn't exist already
        if player not in success_rate:
            success_rate[player] = []
        # get the dice roll results from the log and calculate the success rate for that player's dice rolls
        count = 0
        for log in logs[player]:
            count += 1
            total_count += 1
            log_clean = log[3].replace("[", "").replace("]", "")
            if len(log_clean):
                # convert string to list of ints and remove brackets from start and end of list
                rolls = [int(roll) for roll in log_clean.split(',')]
                # print(rolls)
                # count how many dice rolls were successful (7 or higher)
                successes = sum([roll >= 7 for roll in rolls])
                # calculate the success rate for this player's dice rolls
                success_rate[player].append(successes / len(rolls))
        print("{} has {} logs".format(player, count))

    # calculate the average success rate for all players
    total = 0
    for player in success_rate:
        # add up each player's average and divide by number of players to get overall average
        total += sum(success_rate[player]) / len(success_rate[player])

    print("Total Success Rate: {}%".format((total / len(success_rate) * 100)))

    # calculate the average success rate for each individual player and sort them from highest to lowest
    sorted_players = sorted([{"name": name, "avg": (sum(success) / len(success)) * 100}
                             for name, success in success_rate.items()], key=lambda x: x["avg"], reverse=True)

    print("\nTop 10 Players by Average Success Rate")
    i = 1
    # only show top 10 players with highest avg. successes rates (if there are more than 10)
    while i <= 10:
        if i > len(sorted_players):
            # stop when we reach end of list of sorted players (if there are less than or equal to 10)
            break

        # display rank, name and avg. successes rate as a percentage rounded to 2 decimal places
        print("{}. {} - {:0.2f}%".format((i),
                                         sorted_players[i - 1]["name"], sorted_players[i - 1]["avg"]))

        # increment counter so that next iteration will show next best ranked player etc...
        i += 1

    print("\nTop 10 Players by Total Success Rate")
    i = 1
    # only show top 10 players with highest total successes rates (if there are more than 10)
    while i <= 10:
        if i > len(sorted_players):
            # stop when we reach end of list of sorted players (if there are less than or equal to 10)
            break

        print("{}. {} - {:0.2f}%".format((i), sorted_players[i - 1]["name"], sum(success_rate[sorted_players[i - 1]["name"]]) / len(
            success_rate[sorted_players[i - 1]["name"]]) * 100))   # display rank, name and avg. successes rate as a percentage rounded to 2 decimal places

        # increment counter so that next iteration will show next best ranked player etc...
        i += 1

    print("\nTotal Log Count: {}".format(total_count))


if __name__ == "__main__":
    main()
