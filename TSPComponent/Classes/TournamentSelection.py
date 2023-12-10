import numpy as np

from TSPComponent.Classes.Fitness import Fitness


class TournamentSelection(Fitness):
    def __init__(self, population, distance_matrix):
        super().__init__(distance_matrix)
        self.population = population
        self.parent1 = None
        self.parent2 = None

    def selection_pool(self, tour_selection_size):
        """
        Method to generate tournament selections pool
        :param tour_selection_size: int
        :return: pool_selections: ndarray
        """
        rng = np.random.default_rng()
        pool_selections = np.array(
            [self.population[rng.integers(len(self.population))] for _ in range(tour_selection_size)]
        )

        return pool_selections

    def select_single_parent(self, pool):
        """
        Method to select a best fit solution as a parent from a selection pool
        :param pool: ndarray
        :return: parent: ndarray
        """
        distances = np.array([self.calc_fitness(chromosome - 1) for chromosome in pool])
        best_score_idx = np.argmin(distances)
        parent = pool[best_score_idx]

        # Find the index of the parent in the population
        parent_index = np.where((self.population == parent).all(axis=1))[0]
        # If the parent is in the population, delete it
        if parent_index.size > 0:
            self.population = np.delete(self.population, parent_index[0], axis=0)

        return parent

    def parents_selection(self, tour_selection_size):
        """
        Method to select two best fit solutions as parents from the population using tournament selection.
        The first selected parent is removed from the population before selecting the second to avoid duplication.
        :param tour_selection_size: int
        :return: self.parent1, self.parent2: tuple[ndarray, ndarray]
        """
        # Select first parent
        pool = self.selection_pool(tour_selection_size)
        self.parent1 = self.select_single_parent(pool)

        # Select second parent
        pool = self.selection_pool(tour_selection_size)
        self.parent2 = self.select_single_parent(pool)

        return self.parent1, self.parent2
