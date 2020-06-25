
#!/usr/bin/env python3

import random

from utils.chromosome import Chromosome


class Population():

    MAX_SIZE = 10
    def __init__(self):

        self.population = None
        self.generations = 0

    def run(self, generations):
        # cut the list
        cut = len(self.population) // 2

        for i in range(generations):
            # Sort the population of chromosomes by their fitness
            population_by_fitness = sorted(self.population, key=lambda gene: gene.get_fitness())

            print('Generation: {}'.format(self.generations))
            print([member.get_fitness() for member in population_by_fitness])

            # select the most succesful ones
            fittest = population_by_fitness[cut:]

            # Shuffle and cross breed the fittest members.
            random.shuffle(fittest)

            # create new chromosomes
            for i in range(0, cut, 2):
                fittest += [fittest[i].cross(fittest[i + 1])]
                fittest += [fittest[i].cross(fittest[i + 1])]

            self.population = fittest

            for chromosome in self.population:
                chromosome.recalculate_fitness()

            self.generations += 1

    def get_fittest_member(self):
        # sort the list and get the last element
        return sorted(self.population, key=lambda gene: gene.get_fitness())[-1]

    def init_first(self):
        # init the first population
        self.population = [Chromosome.random() for _ in range(Population.MAX_SIZE)]