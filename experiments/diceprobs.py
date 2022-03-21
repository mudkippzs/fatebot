def dice_roll(dice_input):
    """
    Takes a string input of the form 'XDY' and returns a list of all possible outcomes.
    """
    dice_input = dice_input.split('D')
    num_dice = int(dice_input[0])
    num_sides = int(dice_input[1])

    # Create a list of all possible outcomes for the given dice input.
    outcomes = []
    for i in range(num_dice):
        outcomes.append(list(range(1, num_sides + 1)))

    # Create a list of all possible combinations of the outcomes.
    combinations = []
    for combination in itertools.product(*outcomes):
        combinations.append(combination)

    # Create a list of all possible sums of the combinations.
    sums = []
    for combination in combinations:
        sums.append(sum(combination))

    return sums


def graph_probability(sums):
    """
    Takes a list of integers and graphs the probability curve of the integers.
    """
    # Create a dictionary with each integer as a key and the number of times it appears as the value.
    counts = {}
    for sum in sums:
        if sum not in counts:
            counts[sum] = 1
        else:
            counts[sum] += 1

    # Create a list of the keys and values from the dictionary.
    keys = list(counts.keys())
    values = list(counts.values())

    # Create a list of the probabilities of each integer.
    probabilities = []
    for value in values:
        probabilities.append(value / len(sums))

    # Graph the probability curve.
    plt.bar(keys, probabilities)
    plt.xlabel('Sum')
    plt.ylabel('Probability')
    plt.title('Probability Curve')
    plt.show()


def main():
    dice_input = input('Enter dice roll input: ')
    sums = dice_roll(dice_input)
    graph_probability(sums)


if __name__ == '__main__':
    main()