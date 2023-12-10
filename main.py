import numpy as np
from utils import list_text_files

from KPComponent.solve_kp import solve_kp
from TSPComponent.ga import run_ga

from Classes.Parser import Parser
from Classes.Population import Population
from Classes.EncodeDecode import EncodeDecode


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
            50,
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
        # encode_decode = EncodeDecode(best_tsp_sol, best_kp_sol)
        # encoded_genotype = encode_decode.encode()
        #
        # print(encoded_genotype)

        init_pop = Population(
            100,
            RAND_SEED,
            best_tsp_sol,
            best_kp_sol,
        ).initial_pop

        """
        -----------------------
        2. Divide into elite and non-elite
        -----------------------
        """


# Press the green button in the gutter to run the script.
if __name__ == '__main__':
    main()

# See PyCharm help at https://www.jetbrains.com/help/pycharm/
