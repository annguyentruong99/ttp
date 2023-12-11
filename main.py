import random
from itertools import product
import numpy as np
import logging
from utils import list_text_files, save_to_file
from KPComponent.solve_kp import solve_kp
from TSPComponent.ga import run_ga

from Classes.Parser import Parser
from Classes.Population import Population
from Classes.Decode import Decode
from Classes.Fitness import Fitness
from Classes.EliteDivision import EliteDivision
from Classes.Crossover import Crossover
from Classes.Repair import Repair

logging.basicConfig(filename='nic_log.log', level=logging.INFO, format='%(asctime)s - %(levelname)s: %(message)s')

def main():
    TERMINATION_CRITERION = 100
    RAND_SEED = 234

    # Get all test instances
    test_instances = list_text_files('./instances')

    # Define possible parameters
    init_pops = [100, 200, 500]
    nums_elites = [30, 50]
    parameters = product(init_pops, nums_elites)

    for instance in test_instances:
        parser = Parser(instance)

        # Instances variables dict
        variables = parser.parse_variables()

        # Get node coordinates & profit matrix
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
        df_items = parser.parse_item_section(10 + variables['dimension'] + 1, variables['dimension'])
        # Items weight array
        weights = df_items['Weight'].to_numpy()
        # Items profit array
        profits = df_items['Profit'].to_numpy()
        # Knapsack capacity
        kp_capacity = variables['knapsack_capacity']

        best_kp_sol = solve_kp(weights, profits, kp_capacity)

        logging.info(f"Initializing population for instance {instance}")

        """
        Find the best solution for TSP
        """
        # Distance matrix
        distance_matrix = np.array(
            parser.calculate_distance_matrix(node_coord)
        )

        best_tsp_sol = run_ga(
            250,
            4,
            2,
            0.8,
            2,
            0.02,
            distance_matrix
        )

        # Number of cities
        num_cities = len(distance_matrix)
        # Number of items
        num_items = len(weights)

        for param in parameters:

            NUM_POP = param[0]
            NUM_ELITE = param[1]

            results = []

            for i in range(TERMINATION_CRITERION):
                """
                Initial population
                """
                population = Population(
                    NUM_POP,
                    RAND_SEED,
                    best_tsp_sol,
                    best_kp_sol,
                )

                pop = population.pop

                """
                -----------------------
                2. Divide into elite and non-elite
                -----------------------
                """
                # Decode each genotype solution
                decoded_pop = [
                    Decode(genotype, num_cities, num_items).decode() for genotype in pop
                ]

                # Prepare the solution to be passed into EliteDivision
                division_pop = [{
                    'individual': individual,
                    'fitness': Fitness(
                        tour=np.insert((decoded_ind[0][decoded_ind[0] != 1]), 0, 1).tolist(),
                        packing_plan=decoded_ind[1].tolist(),
                        variables=variables,
                        distance_matrix=distance_matrix,
                        profit_table=profit_matrix
                    ).calculate_cost(),
                    'crowding_distance': 0
                } for individual, decoded_ind in zip(pop, decoded_pop)]

                # Initiate EliteDivision class
                elite_division = EliteDivision(NUM_ELITE, division_pop)

                # Split the population to elites and non-elites
                elites, non_elites = elite_division.nsga_ii_survival_selection()

                """
                -----------------------
                3. Perform biased crossover
                -----------------------
                """
                # Randomly select elite and non-elite genotypes
                elite_individual = random.choice(elites)
                non_elite_individual = random.choice(non_elites)

                # Perform the biased crossover
                offspring = Crossover(rho_e=0.7,
                                      elite_solution=elite_individual['individual'],
                                      non_elite_solution=non_elite_individual['individual'],
                                      crossover_type='biased'
                                      ).perform_crossover()

                """
                -----------------------
                4. Create new population
                -----------------------
                """
                # Map the individuals from elites
                elites = [x['individual'].tolist() for x in elites]
                # Generate random individuals to fill up the remaining spaces
                population.replacement(elites, offspring, num_cities, num_items, NUM_POP)

                """
                -----------------------
                5. Repair the solutions with total weight higher than knapsack capacity
                -----------------------
                """
                repaired = []
                for genotype in elites:
                    repair = Repair(
                        np.array(genotype),
                        profit_matrix,
                        num_cities,
                        num_items,
                        kp_capacity
                    )
                    repaired.append(repair.repair())

                """
                -----------------------
                6. Fitness Evaluation
                -----------------------
                """
                evaluation = [Fitness(
                    tour=np.insert((phenotype[0][phenotype[0] != 1]), 0, 1).tolist(),
                    packing_plan=phenotype[1].tolist(),
                    variables=variables,
                    distance_matrix=distance_matrix,
                    profit_table=profit_matrix
                ).calculate_cost() for phenotype in repaired]
                results.append(evaluation)

                logging.info(f"Iteration {i + 1} completed for instance {instance}, "
                             f"NUM_POP={NUM_POP}, NUM_ELITE={NUM_ELITE}")

            stripped_instance = instance.strip('./instances/').strip('.txt')
            save_to_file(results, file_name=f'./results/{stripped_instance}/{NUM_POP}_{NUM_ELITE}.txt')


if __name__ == '__main__':
    main()
