import random


class Crossover:
    def __init__(self, rho_e, elite_solution, non_elite_solution, crossover_type):
        self.rho_e = rho_e
        self.elite_solution = elite_solution
        self.non_elite_solution = non_elite_solution
        self.crossover_type = crossover_type

    def biased_crossover(self):
        # Ensure both parents have the same length
        assert len(self.elite_solution) == len(self.non_elite_solution)

        offspring = []

        for i in range(len(self.elite_solution)):
            # Generate a random number between 0 and 1
            rand_value = random.random()

            # Determine whether to inherit from the elite parent or non-elite parent
            if rand_value <= self.rho_e:
                offspring.append(self.elite_solution[i])
            else:
                offspring.append(self.non_elite_solution[i])

        return offspring

    def single_point_crossover(self):
        # Perform single-point crossover between two candidates
        crossover_point = random.randint(1, len(self.elite_solution) - 1)
        offspring1 = self.elite_solution[:crossover_point] + self.non_elite_solution[crossover_point:]
        offspring2 = self.non_elite_solution[:crossover_point] + self.elite_solution[crossover_point:]
        offspring1 = self.repair_offspring(offspring1, self.elite_solution)
        offspring2 = self.repair_offspring(offspring2, self.non_elite_solution)
        return offspring1, offspring2

    def ordered_crossover(self):
        # Perform ordered crossover between two parents
        crossover_points = sorted(random.sample(range(len(self.elite_solution)), 2))
        offspring1 = [None] * len(self.elite_solution)
        offspring2 = [None] * len(self.elite_solution)
        offspring1[crossover_points[0]:crossover_points[1] + 1] = self.elite_solution[
                                                                  crossover_points[0]:crossover_points[1] + 1]
        offspring2[crossover_points[0]:crossover_points[1] + 1] = self.non_elite_solution[
                                                                  crossover_points[0]:crossover_points[1] + 1]
        remaining_elements1 = [gene for gene in self.non_elite_solution if gene not in offspring1]
        remaining_elements2 = [gene for gene in self.elite_solution if gene not in offspring2]
        offspring_index1 = crossover_points[1] + 1
        offspring_index2 = crossover_points[1] + 1

        for gene1, gene2 in zip(remaining_elements1, remaining_elements2):
            if offspring1[offspring_index1] is None:
                offspring1[offspring_index1] = gene1
            if offspring2[offspring_index2] is None:
                offspring2[offspring_index2] = gene2
            offspring_index1 = (offspring_index1 + 1) % len(self.elite_solution)
            offspring_index2 = (offspring_index2 + 1) % len(self.elite_solution)

        return offspring1, offspring2

    def perform_crossover(self):
        # Perform crossover based on the specified type
        if self.crossover_type == 'fix':
            return self.single_point_crossover()
        elif self.crossover_type == 'ordered':
            return self.ordered_crossover()
        elif self.crossover_type == 'biased':
            return self.biased_crossover()
        else:
            raise ValueError("Invalid crossover type")

    def repair_offspring(self, offspring, candidate):
        # Repair duplicated genes in offspring by replacing them with unused genes from the candidate
        seen = set()
        repaired_offspring = []

        for chromosome in offspring:
            if chromosome not in seen:
                seen.add(chromosome)
                repaired_offspring.append(chromosome)
            else:
                for replacement in candidate:
                    if replacement not in seen:
                        seen.add(replacement)
                        repaired_offspring.append(replacement)
                        break
        return repaired_offspring
