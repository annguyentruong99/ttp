import pandas as pd
import numpy as np

class Fitness:
    def __init__(self, tour, packing_plan, variables, distance_matrix, profit_table):
        self.tour = tour
        self.packing_plan = packing_plan
        self.variables = variables
        self.distance_matrix = distance_matrix
        self.profit_table = profit_table
        self.weight = 0

    def calculate_current_velocity(self, weight, capacity, min_speed, max_speed):
        # Removed 'self.' from parameters as they are passed explicitly
        if weight <= capacity:
            return max_speed - (weight / capacity) * (max_speed - min_speed)
        else:
            return min_speed

    def calculate_cost(self):
        # Removed parameters, using self to access instance variables
        self.profit_table['Picked'] = self.packing_plan

        dimension = self.variables['dimension']
        max_speed = self.variables['max_speed']
        min_speed = self.variables['min_speed']
        capacity = self.variables['knapsack_capacity']

        total_time = 0
        current_velocity = max_speed
        current_weight = 0

        for i in range(dimension):
            from_city = self.tour[i]
            to_city = self.tour[(i + 1) % dimension]
            distance = round(self.distance_matrix[from_city - 1][to_city - 1])

            time_to_travel = distance / current_velocity

            if i < len(self.packing_plan):
                picked_item_weight = (self.profit_table[(self.profit_table['Assigned_Node'] == to_city)]['Weight'] * self.profit_table[(self.profit_table['Assigned_Node'] == to_city)]['Picked']).values[0]
                current_weight += picked_item_weight

            current_velocity = self.calculate_current_velocity(current_weight, capacity, min_speed, max_speed)

            total_time += time_to_travel

        total_profit = self.profit_table[self.profit_table['Picked'] == 1]['Profit'].sum()

        return total_time, total_profit
