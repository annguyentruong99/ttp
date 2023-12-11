import numpy as np

from Classes.Encode import Encode


class Population(Encode):
    def __init__(self, num_initial_pop, seed, best_tsp_sol, best_kp_sol):
        super().__init__(best_tsp_sol, best_kp_sol)
        np.random.seed(seed)
        # Initialize random keys
        rand_initial_pop = np.array(
            [
                np.append(
                    np.random.random(len(best_tsp_sol) - 1),
                    np.random.random(len(best_kp_sol))
                ) for _ in range(num_initial_pop)
            ]
        )
        encoded_genotype = self.encode()
        self.initial_pop = np.vstack([
            rand_initial_pop,
            encoded_genotype
        ])
