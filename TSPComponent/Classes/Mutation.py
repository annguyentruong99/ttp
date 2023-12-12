import numpy as np


class Mutation:
    def __init__(self, child1, child2, mutation_rate):
        self.child1 = child1
        self.child2 = child2
        self.mutation_rate = mutation_rate

    def swap_mutation(self, num_swaps):
        """
        Performs swap mutation
        :return: child1, child2: tuple[ndarray, ndarray]
        """
        def multi_swap(arr, num_swaps):
            for _ in range(num_swaps):
                idx1, idx2 = np.random.choice(len(arr), size=2, replace=False)
                arr[idx1], arr[idx2] = arr[idx2], arr[idx1]

        rng = np.random.default_rng()
        if rng.random() < self.mutation_rate:
            multi_swap(self.child1, num_swaps)
        if rng.random() < self.mutation_rate:
            multi_swap(self.child2, num_swaps)

        return self.child1, self.child2