import numpy as np
from utils import list_text_files

from KPComponent.solve_kp import solve_kp
from TSPComponent.ga import run_ga

from Classes.Parser import Parser
from Classes.Population import Population
from Classes.Encode import Encode
from Classes.Decode import Decode
from Classes.Fitness import Fitness
from Classes.EliteDivision import EliteDivision


def main():
    RAND_SEED = 234

    # Get all test instances
    test_instances = list_text_files('./instances')

    for instance in test_instances:
        parser = Parser(instance)

        # Instances variables dict
        variables = parser.parse_variables()

        # Get node coordinates
        node_coord, profit_matrix = parser.parse_file_parallel(variables['dimension'])

        """
        -----------------------
        1. Initialize population
        -----------------------
        """

        """
        Find the best solution for KP
        """
        # Items dataframe
        df_items = parser.parse_item_section(291, variables['dimension'])
        # Items weight array
        weights = df_items['Weight'].to_numpy()
        # Items profit array
        profits = df_items['Profit'].to_numpy()
        # Knapsack capacity
        kp_capacity = variables['knapsack_capacity']

        best_kp_sol = solve_kp(weights, profits, kp_capacity)

        """
        Find the best solution for TSP
        """
        # Distance matrix
        distance_matrix = np.array(
            parser.calculate_distance_matrix(node_coord)
        )

        best_tsp_sol = run_ga(
            10,
            4,
            2,
            0.8,
            2,
            0.02,
            distance_matrix
        )

        """
        Initial population
        """
        init_pop = Population(
            100,
            RAND_SEED,
            best_tsp_sol,
            best_kp_sol,
        ).initial_pop

        # Number of cities
        num_cities = len(distance_matrix)
        # Number of items
        num_items = len(weights)

        """
        -----------------------
        2. Divide into elite and non-elite
        -----------------------
        """
        decoded_pop = [
            Decode(genotype, num_cities, num_items).decode() for genotype in init_pop
        ]

        division_pop = [{
            'individual': individual,
            'fitness': Fitness(
                tour=np.insert((decoded_ind[0][decoded_ind[0]!=1]), 0, 1).tolist(),
                packing_plan=decoded_ind[1].tolist(),
                variables=variables,
                distance_matrix=distance_matrix,
                profit_table=profit_matrix,
                min_speed=variables['min_speed'],
                max_speed=variables['max_speed'],
                capacity=kp_capacity
            ).calculate_cost(),
            'crowding_distance': 0
        } for individual, decoded_ind in zip(init_pop, decoded_pop)]

        elite_division = EliteDivision(20, division_pop)

        elites, non_elites = elite_division.nsga_ii_survival_selection()

        print(len(elites), len(non_elites))


if __name__ == '__main__':
    main()
