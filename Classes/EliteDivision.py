class EliteDivision():
    def __init__(self, num_elite, population):
        self.num_elite = num_elite
        self.population = population

    def dominates(self, individual_a, individual_b):
        better_in_any = False
        for a, b in zip(individual_a['fitness'], individual_b['fitness']):
            if a > b:
                return False
            elif a < b:
                better_in_any = True
        return better_in_any

    def non_dominated_sort(self):
        fronts = [[]]
        for individual in self.population:
            individual['dominated_by'] = []
            individual['dominates'] = 0
            for other in self.population:
                if self.dominates(individual, other):
                    individual['dominated_by'].append(other)
                elif self.dominates(other, individual):
                    individual['dominates'] += 1
            if individual['dominates'] == 0: fronts[0].append(individual)
        i = 0
        while fronts[i]:
            next_front = []
            for individual in fronts[i]:
                for other in individual['dominated_by']:
                    other['dominates'] -= 1
                    if other['dominates'] == 0: next_front.append(other)
            i += 1
            fronts.append(next_front)
        return fronts[:-1]

    def calculate_crowding_distances(self, front):
        num_objectives = len(front[0]['fitness'])
        for individual in front: individual['crowding_distance'] = 0
        for i in range(num_objectives):
            front.sort(key=lambda x: x['fitness'][i])
            front[0]['crowding_distance'] = front[-1]['crowding_distance'] = float('inf')
            for j in range(1, len(front) - 1):
                distance = front[j + 1]['fitness'][i] - front[j - 1]['fitness'][i]
                range_objective = front[-1]['fitness'][i] - front[0]['fitness'][i]
                if range_objective != 0: distance /= range_objective
                front[j]['crowding_distance'] += distance

    def nsga_ii_survival_selection(self):
        sorted_fronts = self.non_dominated_sort()
        elites = []
        non_elites = []
        for front in sorted_fronts:
            self.calculate_crowding_distances(front)
            if len(elites) + len(front) <= self.num_elite:
                elites.extend(front)
            else:
                front.sort(key=lambda x: x['crowding_distance'], reverse=True)
                remaining_spots = self.num_elite - len(elites)
                elites.extend(front[:remaining_spots])
                non_elites.extend(front[remaining_spots:])
                break
        non_elites.extend(self.population[len(elites):])
        return elites, non_elites