import numpy as np

class Decode:
    def __init__(self, genotype, num_cities, num_items):
        self.genotype = genotype
        self.num_cities = num_cities
        self.num_items = num_items

    def decode(self):
        # Split the genotype into tour part and packing plan part
        tour_keys = self.genotype[:self.num_cities]
        packing_keys = self.genotype[self.num_cities:self.num_cities + self.num_items]

        # Decode the tour: sort cities based on their associated random keys
        tour = list(range(1, self.num_cities + 1))  # Assuming cities are numbered from 1 to num_cities
        decoded_tour = [x for _, x in sorted(zip(tour_keys, tour), key=lambda pair: pair[0])]

        # Decode the packing plan: an item is picked if its key is greater than 0.5
        decoded_packing_plan = [1 if key > 0.5 else 0 for key in packing_keys]

        return np.array(decoded_tour), np.array(decoded_packing_plan)