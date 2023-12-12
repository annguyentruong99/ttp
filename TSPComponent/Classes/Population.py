import numpy as np

from TSPComponent.Classes.Fitness import Fitness


class Population(Fitness):
    def __init__(self, population: np.ndarray, distance_matrix):
        super().__init__(distance_matrix)
        self.population = population
        self.parents = []
        self.best_score = 0
        self.best_sol = None
        self.worst_score = 0
        self.worst_sol = None

    def evaluate(self):
        """
        Method to determine the best solution from the initial population
        :return: None
        """
        # calculate the distance of each solution in population
        distances = np.array(
            [self.calc_fitness(chromosome - 1) for chromosome in self.population]
        )
        # determine the best and worst solution
        self.best_score = np.min(distances)
        self.best_sol = self.population[distances.tolist().index(self.best_score)]
        self.worst_score = np.max(distances)
        self.worst_sol = self.population[distances.tolist().index(self.worst_score)]

    def replacement(self, child):
        """
        Method to replace the solution in the population with child if child's distance is smaller or equal
        :param child: ndarray
        :return: None
        """
        # calculate the distance of the child
        child_score = self.calc_fitness(child - 1)
        # replace the solution in the population with child if child's distance is smaller or equal
        if child_score <= self.worst_score:
            worst_sol_ind = np.where(np.all(self.population == self.worst_sol, axis=1))[0][0]
            self.population[worst_sol_ind] = child
        # re-evaluate the population to make sure we get a new worst solution
        self.evaluate()
