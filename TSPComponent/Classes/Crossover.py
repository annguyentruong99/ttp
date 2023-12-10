import numpy as np
from TSPComponent.utils import contains_duplicates


class Crossover:
    def __init__(self, parent1, parent2, crossover_rate):
        self.parent1 = parent1
        self.parent2 = parent2
        self.crossover_rate = crossover_rate

    @staticmethod
    def fix_child(child, parent):
        """
        Method to fix children if there are duplicates.
        :param child: ndarray
        :param parent: ndarray
        :return: child: ndarray
        """
        if contains_duplicates(child):
            unique_values = set()
            duplicate_indices = []

            # Identify duplicates and their indices
            for i, value in enumerate(child):
                if value in unique_values:
                    duplicate_indices.append(i)
                else:
                    unique_values.add(value)

            missing_values = list(set(parent) - unique_values)

            # Replace duplicates with missing values
            for i in duplicate_indices:
                if missing_values:
                    child[i] = missing_values.pop(0)
                else:
                    # This might need more sophisticated handling based on your problem specifics
                    raise ValueError("Ran out of unique values to replace duplicates")

        return child

    def crossover(self, num_points):
        """
        Method to generate 2 different children by crossover.
        :param num_points: Number of crossover points.
        :return: child1, child2: ndarray, ndarray
        """
        rng = np.random.default_rng()
        # Decide whether to perform crossover based on the crossover rate
        if rng.random() <= self.crossover_rate:
            # Randomly select unique crossover points
            crossover_points = sorted(rng.choice(len(self.parent1) - 2, size=num_points, replace=False) + 1)

            # Initialize children as copies of parents
            child1, child2 = self.parent1.copy(), self.parent2.copy()

            # Alternate segments from each parent based on crossover points
            for i in range(num_points):
                if i % 2 != 0:
                    continue

                end_point = crossover_points[i + 1] if i + 1 < len(crossover_points) else len(self.parent1)
                (child1[crossover_points[i]:end_point]
                 , child2[crossover_points[i]:end_point]) = (child2[crossover_points[i]:end_point],
                                                             child1[crossover_points[i]:end_point])

            fixed_child1 = self.fix_child(child1, self.parent1)
            fixed_child2 = self.fix_child(child2, self.parent2)

            return fixed_child1, fixed_child2
        else:
            # If crossover is not performed, children are copies of the parents
            return self.parent1.copy(), self.parent2.copy()
