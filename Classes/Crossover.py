import random

class Crossover:
    def __init__(self, rho_e, elite_solution, non_elite_solution, crossover_type):
        self.rho_e = rho_e
        self.elite_solution = elite_solution
        self.non_elite_solution = non_elite_solution
        self.crossover_type = crossover_type

    def biased_crossover(self, elite_parent, non_elite_parent):
        # Ensure both parents have the same length
        assert len(elite_parent) == len(non_elite_parent)

        offspring = []

        for i in range(len(elite_parent)):
            # Generate a random number between 0 and 1
            rand_value = random.random()

            # Determine whether to inherit from the elite parent or non-elite parent
            if rand_value <= self.rho_e:
                offspring.append(elite_parent[i])
            else:
                offspring.append(non_elite_parent[i])

        return offspring

    def single_point_crossover(self, elite_parent, non_elite_parent):
        # Perform single-point crossover between two candidates
        crossover_point = random.randint(1, len(elite_parent) - 1)
        offspring1 = elite_parent[:crossover_point] + non_elite_parent[crossover_point:]
        offspring2 = non_elite_parent[:crossover_point] + elite_parent[crossover_point:]
        offspring1 = self.repair_offspring(offspring1, elite_parent)
        offspring2 = self.repair_offspring(offspring2, non_elite_parent)
        return offspring1, offspring2

    def ordered_crossover(self, elite_parent, non_elite_parent):
        # Perform ordered crossover between two parents
        crossover_points = sorted(random.sample(range(len(elite_parent)), 2))
        offspring1 = [None] * len(elite_parent)
        offspring2 = [None] * len(elite_parent)
        offspring1[crossover_points[0]:crossover_points[1] + 1] = elite_parent[crossover_points[0]:crossover_points[1] + 1]
        offspring2[crossover_points[0]:crossover_points[1] + 1] = non_elite_parent[crossover_points[0]:crossover_points[1] + 1]
        remaining_elements1 = [gene for gene in non_elite_parent if gene not in offspring1]
        remaining_elements2 = [gene for gene in elite_parent if gene not in offspring2]
        offspring_index1 = crossover_points[1] + 1
        offspring_index2 = crossover_points[1] + 1

        for gene1, gene2 in zip(remaining_elements1, remaining_elements2):
            if offspring1[offspring_index1] is None:
                offspring1[offspring_index1] = gene1
            if offspring2[offspring_index2] is None:
                offspring2[offspring_index2] = gene2
            offspring_index1 = (offspring_index1 + 1) % len(elite_parent)
            offspring_index2 = (offspring_index2 + 1) % len(elite_parent)

        return offspring1, offspring2

    def perform_crossover(self):
        # Perform crossover based on the specified type
        if self.crossover_type == 'fix':
            return self.single_point_crossover(self.elite_solution, self.non_elite_solution)
        elif self.crossover_type == 'ordered':
            return self.ordered_crossover(self.elite_solution, self.non_elite_solution)
        elif self.crossover_type == 'biased':
            return self.biased_crossover(self.elite_solution, self.non_elite_solution)
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
