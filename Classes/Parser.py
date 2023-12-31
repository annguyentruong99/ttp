import pandas as pd
import numpy as np
import concurrent.futures

class Parser:
    def __init__(self, file_name):
        # Initialize Parser with file_name
        with open(file_name, 'r') as file:
            self.lines = file.readlines()

    def parse_variables(self):
        """
        Extract information from the input file and return a dictionary.
        """
        variables = {}
        for line in self.lines:
            # Parse each line for relevant information
            if line.startswith("PROBLEM NAME:"):
                variables['problem_name'] = line.split(':')[1].strip()
            elif line.startswith("KNAPSACK DATA TYPE:"):
                variables['knapsack_data_type'] = line.split(':')[1].strip()
            elif line.startswith("DIMENSION:"):
                variables['dimension'] = int(line.split(':')[1].strip())
            elif line.startswith("NUMBER OF ITEMS:"):
                variables['num_items'] = int(line.split(':')[1].strip())
            elif line.startswith("CAPACITY OF KNAPSACK:"):
                variables['knapsack_capacity'] = int(line.split(':')[1].strip())
            elif line.startswith("MIN SPEED:"):
                variables['min_speed'] = float(line.split(':')[1].strip())
            elif line.startswith("MAX SPEED:"):
                variables['max_speed'] = float(line.split(':')[1].strip())
            elif line.startswith("RENTING RATIO:"):
                variables['renting_ratio'] = float(line.split(':')[1].strip())
            elif line.startswith("EDGE_WEIGHT_TYPE:"):
                variables['edge_weight_type'] = line.split(':')[1].strip()
        return variables

    def parse_node_coord(self, start_line, dimension):
        """
        Parse node coordinates from the input file.
        """
        data = []
        for line in self.lines[start_line:start_line + dimension]:
            # Parse each line for node coordinates
            parts = line.split()
            index = int(parts[0])
            x = float(parts[1])
            y = float(parts[2])
            data.append({'Index': index, 'X': x, 'Y': y})
        return pd.DataFrame(data)

    def parse_item_section(self, start_line, dimension):
        """
        Parse the item section from the input file.
        """
        data = []
        for line in self.lines[start_line:start_line + dimension]:
            # Parse each line for item details
            index, profit, weight, assigned_node = map(int, line.split())
            data.append({'Index': index, 'Profit': profit, 'Weight': weight, 'Assigned_Node': assigned_node})
        return pd.DataFrame(data).groupby('Assigned_Node').agg({'Profit':'sum','Weight':'sum'}).reset_index()

    def parse_file_parallel(self, dimension):
        """
        Parse node coordinates and item sections in parallel.
        """
        with concurrent.futures.ThreadPoolExecutor() as executor:
            future_node_coord = executor.submit(self.parse_node_coord, 10, dimension)
            future_profit_matrix = executor.submit(self.parse_item_section, 10 + dimension + 1, dimension)

        node_coord = future_node_coord.result()
        profit_matrix = future_profit_matrix.result()

        return node_coord, profit_matrix

    @staticmethod
    def calculate_distance_matrix(node_coord):
        """
        Calculate the distance matrix from node coordinates.
        """
        coordinates = node_coord[['X', 'Y']].values
        x, y = np.meshgrid(coordinates[:, 0], coordinates[:, 1])

        distance_matrix = np.sqrt((x - x.T) ** 2 + (y - y.T) ** 2)

        return distance_matrix
