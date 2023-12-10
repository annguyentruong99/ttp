import numpy as np


class EncodeDecode:
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

    def decode(self, genotype):
        num_cities = len(self.tour)
        num_items = len(self.packing_plan)

        # Split the genotype into tour part and packing plan part
        tour_keys = genotype[:num_cities]
        packing_keys = genotype[num_cities:num_cities + num_items]

        # Decode the tour: sort cities based on their associated random keys
        tour = list(range(1, num_cities + 1))  # Assuming cities are numbered from 1 to num_cities
        decoded_tour = [x for _, x in sorted(zip(tour_keys, tour), key=lambda pair: pair[0])]

        # Decode the packing plan: an item is picked if its key is greater than 0.5
        decoded_packing_plan = [1 if key > 0.5 else 0 for key in packing_keys]

        return np.array(decoded_tour), np.array(decoded_packing_plan)
