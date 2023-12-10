import pandas as pd
import numpy as np

class Fitness:
    # Class variables

    def __init__(self, tour, packing_plan, variables, distance_matrix, profit_table, min_speed, min_speed):
        self.tour = tour
        self.packing_plan = packing_plan
        self.variables = variables
        self.distance_matrix = distance_matrix
        self.profit_table = profit_table
        self.min_speed = min_speed
        self.min_speed = min_speed



    def calculate_current_velocity(weight, capacity, min_speed, max_speed):
        if weight <= capacity:
            return max_speed - (weight / capacity) * (max_speed - min_speed)
        else:
            return min_speed

    def calculate_cost(tour, packing_plan, variables, distance_matrix, profit_table):
        dimension = variables['dimension']
        max_speed = variables['max_speed']

        total_time = 0
        current_velocity = max_speed
        current_weight = 0

        for i in range(dimension):
            # Calculate the distance between consecutive cities
            from_city = tour[i]
            to_city = tour[(i + 1) % dimension]
            distance = round(distance_matrix[from_city - 1][to_city - 1])

            # Calculate the time taken to travel the distance
            time_to_travel = distance / current_velocity

            # Explain the current step
            print(f"At city {from_city}:")
            print(f"  Knapsack weight before picking: {current_weight}")
            print(f"  Current velocity: {current_velocity}")
            print(f"  Distance to next city ({to_city}): {distance}")
            print(f"  Time to travel: {time_to_travel}")

            if i < len(packing_plan):
                # Update current weight based on the packing plan
                picked_item_weight = (profit_table[(profit_table['Assigned_Node'] == to_city)]['Weight']*profit_table[(profit_table['Assigned_Node'] == to_city)]['Picked']).values[0]
                current_weight += picked_item_weight 
                print(f"  Knapsack weight after picking item {i + 1}: {current_weight}")

            # Calculate the current velocity
            current_velocity = calculate_current_velocity(current_weight, variables['knapsack_capacity'], variables['min_speed'], variables['max_speed'])
            print(f"  Updated velocity: {current_velocity}")

            # Accumulate the time taken for this step
            total_time += time_to_travel

        print(f"Total traveling time: {total_time}")
        total_profit = profit_table[profit_table['Picked'] == 1]['Profit'].sum()

        return total_time,total_profit
