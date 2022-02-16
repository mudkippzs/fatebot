import json
import matplotlib.pyplot as plt
from pprint import pprint as pp

def graph_dice_distribution():

    DICE_DISTRIBUTION = {
        "1": 0,
        "2": 0,
        "3": 0,
        "4": 0,
        "5": 0,
        "6": 0,
        "7": 0,
        "8": 0,
        "9": 0,
        "10": 0,
    }

    def strip(s):
        return str(s.replace("[","").replace("]",""))

    with open("dicelogs.json", "r") as f:
        SESSION_RESULTS = json.load(f)

    total_dice_rolls = 0
    for user_log in SESSION_RESULTS:
        for log in SESSION_RESULTS[user_log]:
            diceroll = [int(strip(dr)) for dr in log[3].split(",")]
            for dr in diceroll:
                DICE_DISTRIBUTION[str(dr)] += 1
                total_dice_rolls += 1
        
    plt.bar(range(len(DICE_DISTRIBUTION)), DICE_DISTRIBUTION.values(), align='center')
    plt.xticks(range(len(DICE_DISTRIBUTION)), list(DICE_DISTRIBUTION.keys()))
    plt.xlabel(f"Total Dice Rolls: {total_dice_rolls}")
    plt.show()
    return


if __name__ == "__main__":
    graph_dice_distribution()