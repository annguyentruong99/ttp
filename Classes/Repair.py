import Decode
class Repair(Decode):

    def __init__(self, genotype, profit_table, num_cities, num_items, capacity):
        super.__init__(genotype,num_cities, num_items)
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
