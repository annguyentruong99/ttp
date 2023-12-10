import numpy as np


class Fitness:
    def __init__(self, distance_matrix):
        self.distance_matrix = distance_matrix

    def calc_fitness(self, chromosome: np.ndarray) -> float:
        """
        Method to calculate distance for each individual solution
        :param chromosome: ndarray
        :return: sum of the distance: int
        """
        return sum(
            [
                self.distance_matrix[chromosome[i], chromosome[i + 1]] for i in range(len(chromosome) - 1)
            ]
        ) + self.distance_matrix[chromosome[-1], chromosome[0]]
