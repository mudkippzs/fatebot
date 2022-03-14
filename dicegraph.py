from copy import deepcopy
import datetime
import json
import matplotlib.pyplot as plt
from pprint import pprint as pp

with open("dicelogs.json", "r") as f:
    SESSION_RESULTS = json.load(f)

with open("config.json", "r") as f:
    CONFIG = json.load(f)

# Invert the user list so its userid: username
INV_USERS = {v: k for k, v in {
    **CONFIG["players"][0], **CONFIG["gamemaster"][0]}.items()}
USERS = {k: v for k, v in {**CONFIG["players"]
                           [0], **CONFIG["gamemaster"][0]}.items()}


def strip(s):
    return str(s.replace("[", "").replace("]", ""))


def add_dicts(dicts):
    keys = dicts[0].keys()
    return {key: sum(d[key] for d in dicts) for key in keys}

# Build User Lookup


def user_id_to_user(user_id):
    return INV_USERS[str(user_id)]


def user_to_user_id(user):
    return USERS[user]


def get_users_logs(user_id):
    logs = []
    for uid in INV_USERS:
        if uid in SESSION_RESULTS.keys():
            if uid == user_id:
                logs.append(SESSION_RESULTS[uid])

    logs_merged = []
    for log in logs:
        logs_merged += log

    return logs_merged

# Get all logs


def get_all_logs():
    logs = []
    for uid in INV_USERS:
        if uid in SESSION_RESULTS.keys():
            logs.append(SESSION_RESULTS[uid])

    logs_merged = []
    for log in logs:
        logs_merged += log

    return logs_merged

# Get dice result distribution for a users logs


def get_dice_distribution_of_logs(log_list):
    distribution = {
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

    for log in log_list:
        stripped_log = strip(log[3])
        if len(stripped_log):
            roll_log = stripped_log.split(",")
            for v in roll_log:
                distribution[str(v)] += 1

    return distribution

# Create a plot for a given user and dice-log dictionary


def create_plot(label, logs, show=False):
    plt.clf()
    plt.plot(range(len(logs)), logs.values(), label=label.title())
    plt.xticks(range(len(logs)), list(logs.keys()))
    plt.xlabel(f"Roll distribution for {label}.")
    if show == False:
        timestamp = datetime.datetime.now().strftime("%H:%M:%S-%z")
        plt.savefig(f"dicelogs/{label}_dicegraph_{timestamp}.png")
    else:
        plt.show()


# Create a plot for a given user and dice-log dictionary
def create_group_plot(logs, show=False):
    plt.clf()
    for log in logs:
        plt.plot(range(len(logs[log])), logs[log].values(), label=log.title())

    all_logs = add_dicts([v for k, v in logs.items()])

    plt.xticks(range(len(all_logs)), list(all_logs.keys()))
    plt.legend()
    plt.xlabel(f"Roll distribution for all players.")
    if show == False:
        timestamp = datetime.datetime.now().strftime("%H:%M:%S-%z")
        plt.savefig(f"dicelogs/all_players_dicegraph_{timestamp}.png")
    else:
        plt.show()


def test():
    set_logs = get_dice_distribution_of_logs(
        get_users_logs("433097995832000513"))
    bob_logs = get_dice_distribution_of_logs(
        get_users_logs("382348220405383171"))
    vasily_logs = get_dice_distribution_of_logs(
        get_users_logs("514859386116767765"))
    ganj_logs = get_dice_distribution_of_logs(
        get_users_logs("218521566412013568"))
    group_logs = {
        "set": set_logs,
        "bob": bob_logs,
        "vasily": vasily_logs,
        "ganj": ganj_logs,
    }
    all_logs = add_dicts([set_logs, bob_logs, vasily_logs, ganj_logs])

    set_plot = create_plot("set", set_logs)
    bob_plot = create_plot("bob", bob_logs)
    vasily_plot = create_plot("vasily", vasily_logs)
    ganj_plot = create_plot("ganj", ganj_logs)
    all_plot = create_plot("all players", all_logs)
    layered_plot = create_group_plot(group_logs)


if __name__ == "__main__":
    # graph_dice_distribution("433097995832000513")
    # graph_dice_distribution("514859386116767765")
    # graph_dice_distribution("382348220405383171")
    # graph_dice_distribution(100000)
    test()
