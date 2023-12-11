from Classes.Decode import Decode


class Repair(Decode):

    def __init__(self, genotype, profit_table, num_cities, num_items, capacity):
        super().__init__(genotype, num_cities, num_items)
        self.genotype = genotype
        self.profit_table = profit_table
        self.capacity = capacity

    def calc_knapsack_weight(self, packing_plan):
        """ Helper function for the repair() function. It calculates the current weight of
        the knapsack."""
        # Getting list of weights
        weights = self.profit_table[self.profit_table.columns[2]]

        total_weight = 0
        # Looping through packing plan
        for i, plan in enumerate(packing_plan):
            if plan == 1:
                total_weight += weights[i]

        return total_weight

    def repair(self):
        """ Repairs solutions that have exceeded the maximum knapsack capacity."""
        weights = self.profit_table[self.profit_table.columns[2]]
        tour, packing_plan = self.decode()

        # Initializing current weight
        total_weight = self.calc_knapsack_weight(packing_plan)

        # Repeat until current weight is below capacity
        for i, plan in enumerate(packing_plan):
            if total_weight < self.capacity:
                break
            if plan == 1:
                packing_plan[i] = 0
                total_weight -= weights[i]

        return tour, packing_plan

    def validate_repair(self, packing_plan):
        for i, sol in enumerate(self.genotype):
            self.profit_table[f'Picked_{i}'] = packing_plan

        for i in range(len(self.genotype)):
            if (self.profit_table[self.profit_table[f'Picked_{i}'] == 1]['Weight'].sum()) > self.capacity:
                print('the following indexes need to be repaired', i)
