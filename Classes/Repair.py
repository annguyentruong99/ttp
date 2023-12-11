import numpy as np
import Decode
class Repair(Decode):

    def __init__(self, genotype, profit_table, num_cities, num_items, capacity):
        super.__init__(genotype, num_cities, num_items)
        self.genotype = genotype
        self.profit_table = profit_table
        self.capacity = capacity

    def calc_knapsack_weight(self):
        """ Helper function for the repair() function. It calculates the current weight of
        the knapsack."""

        tour, packing_plan = self.decode(self.genotype)


        # Getting list of weights
        weights = self.profit_table[self.profit_table.columns[2]]

        total_weight = 0
        # Looping through packing plan
        for i in range(1, len(tour)):
            # Adding relevant weight if packing plan element is 1
            if packing_plan[i - 1] == 1:
                total_weight += weights[(tour[i] - 2)]

        return total_weight
    def repair(self):
        """ Repairs solutions that have exceeded the maximum knapsack capacity."""
        weights = self.profit_table[self.profit_table.columns[2]]
        tour, packing_plan = self.decode(self.genotype)

        # Initializing current weight
        current_weight = self.calc_knapsack_weight()

        # Repeat until current weight is below capacity
        for i in range(1,len(tour)):
            # Desired condition reached
            if current_weight < self.capacity:
                break

            if packing_plan[i-1] == 1:
                # Directly changing in genotype
                packing_plan[i-1] = 0
                # Reducing current knapsack weight by correct value
                current_weight -= weights[(tour[i]-2)]

        return self.genotype
    def validate_repair(self):
        for i, sol in enumerate(self.genotype):
            packing_plan = self.get_packing_plan(sol)
            self.profit_table[f'Picked_{i}'] = packing_plan

        for i in range(len(self.genotype)):
            if (self.profit_table[self.profit_table[f'Picked_{i}'] == 1]['Weight'].sum()) > self.capacity:
                print('the following indexes need to be repaired', i)



    def get_packing_plan(self):
        self.genotype = np.array(self.genotype)
        half_length = len(self.genotype) // 2
        second_half = self.genotype[half_length+1:]
        packing_plan = np.where(second_half > 0.5, 1, 0)
        return packing_plan
