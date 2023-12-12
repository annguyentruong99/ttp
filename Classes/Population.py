import numpy as np

class Population:
    def __init__(self, num_initial_pop, seed, num_cities, num_items):
        self.seed = seed
        self.num_cities = num_cities
        self.num_items = num_items
        self.num_initial_pop = num_initial_pop
        self.pop = None

    def init_pop(self):
        np.random.seed(self.seed)
        # Initialize random keys
        self.pop = np.array(
            [
                np.append(
                    np.random.random(self.num_cities),
                    np.random.random(self.num_items)
                ) for _ in range(self.num_initial_pop - 1)
            ]
        )

    def replacement(self, elites, offspring, num_pop):
        # Add the crossover offspring into elites
        elites.append(offspring)
        # Generate random individuals to fill up the remaining spaces
        elites = elites + [
            np.append(
                np.random.random(self.num_cities),
                np.random.random(self.num_items)).tolist() for _ in range(num_pop - len(elites)
                                                                          )
        ]
        self.pop = np.array(elites)
