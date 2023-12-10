import random
import numpy as np
from tqdm import tqdm

from TSPComponent.Classes.Population import Population
from TSPComponent.Classes.TournamentSelection import TournamentSelection
from TSPComponent.Classes.Crossover import Crossover
from TSPComponent.Classes.Mutation import Mutation


def init_population(
        cities: np.ndarray,
        distance_matrix: np.ndarray,
        n_pop: int,
        seed: int
) -> Population:
    """
    Function to generate initial population
    :param cities: ndarray
    :param distance_matrix: ndarray
    :param n_pop: int
    :param seed: int
    :return: Population
    """
    # Set random seed
    np.random.seed(seed)
    return Population(
        np.array([np.random.permutation(cities) for _ in range(n_pop)]),
        distance_matrix
    )


def parent_selection(
        population: np.ndarray,
        distance_matrix: np.ndarray,
        tour_selection_size: int
) -> tuple[np.ndarray, np.ndarray]:
    """
    Function to generate parent solutions using tournament selection
    :param population: ndarray
    :param distance_matrix: ndarray
    :param tour_selection_size: int
    :return: parent1, parent2: tuple[ndarray, ndarray]
    """
    tour_selection = TournamentSelection(population, distance_matrix)
    parent1, parent2 = tour_selection.parents_selection(tour_selection_size)
    return parent1, parent2


def crossover(
        parent1: np.ndarray,
        parent2: np.ndarray,
        crossover_rate: float,
) -> Crossover:
    """
    Function to generate two child solutions using single-point crossover
    :param parent1: ndarray
    :param parent2: ndarray
    :param crossover_rate: float
    :return: child1, child2: tuple[ndarray, ndarray]
    """
    return Crossover(parent1, parent2, crossover_rate)


def mutation(
        child1: np.ndarray,
        child2: np.ndarray,
        mutation_rate: float,
) -> Mutation:
    """
    Function to perform swap mutation
    :param child1: ndarray
    :param child2: ndarray
    :param mutation_rate: float
    :return: mutated_child1, mutated_child2: tuple[ndarray, ndarray]
    """
    return Mutation(child1, child2, mutation_rate)


def run_ga(
        nums_init_pop,
        tour_size,
        crossover_points,
        crossover_rate,
        mutation_points,
        mutation_rate,
        distance_matrix
):
    """
    The function to run

    :param nums_init_pop: The size of the initial population
    :param tour_size: Tournament size
    :param crossover_points: Number of crossover points
    :param crossover_rate: The probability of crossover
    :param mutation_points: Number of mutation points
    :param mutation_rate: The probability of mutation
    :param distance_matrix: The distance matrix
    :return: best_sol: The best solution
    """
    # Termination criteria
    termination = 10000

    cities = np.array(list(i + 1 for i in range(len(distance_matrix))))

    # Initialize an array with random routes
    seed = np.random.randint(1, 10000)
    pop = init_population(cities, distance_matrix, nums_init_pop, seed)

    for i in tqdm(range(termination), desc='Finding best solution for TSP', unit='Evaluation'):
        # Tournament selection
        parent1, parent2 = parent_selection(pop.population, distance_matrix, tour_size)

        # Crossover
        crossover_operator = crossover(parent1, parent2, crossover_rate)
        child1, child2 = crossover_operator.crossover(crossover_points)

        # Mutation
        mutation_operator = mutation(child1, child2, mutation_rate)
        mutated_child1, mutated_child2 = mutation_operator.swap_mutation(mutation_points)

        # Replacement
        pop.replacement(mutated_child1)
        pop.replacement(mutated_child2)

    return pop.best_sol
