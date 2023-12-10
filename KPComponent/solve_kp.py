import numpy as np


def solve_kp(weights, profits, capacity):
    """
    The function to solve knapsack problem
    :param weights: The weights of the items
    :param profits: The profits of the items
    :param capacity: The maximum weight that the knapsack can hold
    :return: Array of binaries
    """
    n = len(weights)
    dp = np.zeros((n + 1, capacity + 1))

    for i in range(1, n + 1):
        for w in range(1, capacity + 1):
            if weights[i - 1] <= w:
                dp[i][w] = max(profits[i - 1] + dp[i - 1][w - weights[i - 1]], dp[i - 1][w])
            else:
                dp[i][w] = dp[i - 1][w]

    # Find items to be picked
    picked_items = np.zeros(n, dtype=int)
    w = capacity
    for i in range(n, 0, -1):
        if dp[i][w] != dp[i - 1][w]:
            picked_items[i - 1] = 1
            w -= weights[i - 1]

    return picked_items
