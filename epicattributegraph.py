import json
import matplotlib.pyplot as plt
from pprint import pprint as pp
from epiccalc import calculate_epic_as_dict


def graph_epics():
    EPIC_ATTRIBUTES = calculate_epic_as_dict(12)

    plt.plot(EPIC_ATTRIBUTES.keys(), EPIC_ATTRIBUTES.values())
    plt.xlabel(f"Epic Attribute Scaling.")
    plt.show()
    return


if __name__ == "__main__":
    graph_epics()
