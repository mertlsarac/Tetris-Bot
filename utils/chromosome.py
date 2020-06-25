import math

import numpy as np
import random

from utils.field import Field
from utils.tetromino import Tetromino

GENES = 5

class Chromosome():
    N_SIMULATIONS = 4
    MAX_SIMULATION_LENGTH = 1000
    MUTATION_CHANCE = 0.075

    def __init__(self, genes):
        self.genes = genes
        self.fitness = None
        self.field_score = None

    @staticmethod
    def random():
        # create random Chromosome
        genes = (np.random.random_sample(GENES) * 2) - 1
        return Chromosome(genes)

    def cross(self, other):
        # select 2 index genes
        mutated = [random.randint(0, GENES - 1) for _ in range(2)]

        # swap this with other for mutated index
        child = [i for i in self.genes]

        other_genes = np.array(other.genes, copy=True)

        child[mutated[0]] = other_genes[mutated[0]]
        child[mutated[1]] = other_genes[mutated[1]]

        # if a mutation occured, select one random index, and swap this with random value
        if Chromosome.MUTATION_CHANCE > random.random():
            rand_index = random.randint(0, GENES - 1)
            genes = (np.random.random_sample(1) * 2) - 1
            child[rand_index] = genes[0]

        return Chromosome(np.array(child, copy=True))

    def get_fitness(self):
        if self.fitness is not None:
            return self.fitness
        self.recalculate_fitness()
        return self.fitness

    def recalculate_fitness(self):
        # run the number of simulations
        scores = np.array([self._get_fitness() for _ in range(Chromosome.N_SIMULATIONS)])

        # get their average value
        self.fitness, self.field_score = np.mean(scores, axis=0)

    def _get_fitness(self):
        tetrominos = [
            Tetromino.ITetromino(),
            Tetromino.OTetromino(),
            Tetromino.TTetromino(),
            Tetromino.STetromino(),
            Tetromino.ZTetromino(),
            Tetromino.JTetromino(),
            Tetromino.LTetromino()
        ]
        field = Field()
        field_score = -1

        for length in range(Chromosome.MAX_SIMULATION_LENGTH):
            tetromino = random.choice(tetrominos)
            _, __, _field, _field_score, best_rotation = field.get_optimal_drop(tetromino, self.genes)

            if _field_score == math.inf:
                return length, field_score

            else:
                field = _field
                field_score = _field_score

        return length, field_score


"""Test cross
chromosome = Chromosome(np.array([1, 1, 1, 1, 1]))
chromosome2 = Chromosome(np.array([0.5, 0.5, 0.5, 0.5, 0.5]))

child = chromosome.cross(chromosome2)
print(chromosome2.genes)
print(chromosome.genes)
print(child.genes)
"""