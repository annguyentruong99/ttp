import numpy as np


class Encode:
    def __init__(self, tour, packing_plan):
        self.tour = tour
        self.packing_plan = packing_plan

    def encode(self):
        # Number of cities and items
        num_cities = len(self.tour)
        num_items = len(self.packing_plan)

        # Generate random keys for tour
        tour_keys = [np.random.random() for _ in range(num_cities)]

        # Generate random keys for packing plan
        packing_keys = [np.random.random() for _ in range(num_items)]

        # Combine both parts into one genotype
        genotype = tour_keys + packing_keys
        return np.array(genotype)
