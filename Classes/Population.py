import numpy as np

from Classes.Encode import Encode


class Population(Encode):
    def __init__(self, num_initial_pop, seed, best_tsp_sol, best_kp_sol):
        super().__init__(best_tsp_sol, best_kp_sol)
        self.seed = seed
        self.best_tsp_sol = best_tsp_sol
        self.best_kp_sol = best_kp_sol
        self.num_initial_pop = num_initial_pop
        self.pop = None

    def init_pop(self):
        np.random.seed(self.seed)
        # Initialize random keys
        rand_initial_pop = np.array(
            [
                np.append(
                    np.random.random(len(self.best_tsp_sol)),
                    np.random.random(len(self.best_kp_sol))
                ) for _ in range(self.num_initial_pop - 1)
            ]
        )
        encoded_genotype = self.encode()
        self.pop = np.vstack([
            rand_initial_pop,
            encoded_genotype
        ])

    def replacement(self, elites, offspring, num_cities, num_items, num_pop):
        # Add the crossovered offspring into elites
        elites.append(offspring)
        # Generate random individuals to fill up the remaining spaces
        elites = elites + [
            np.append(
                np.random.random(num_cities),
                np.random.random(num_items)).tolist() for _ in range(num_pop - len(elites)
                                                                     )
        ]
        self.pop = np.array(elites)
