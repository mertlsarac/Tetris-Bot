#!/usr/bin/python

from utils.field import Field
from utils.population import Population
from utils.tetromino import Tetromino

import time
import random
import numpy as np

def create_file(genes):
    str = np.array_str(genes)
    str = str[1:-1]
    str.strip()
    print(str)
    with open("best_genes.txt", "w") as file:
        file.write(str)

def read_file():
    return np.loadtxt("best_genes.txt", dtype=np.float64)

def play(genes):
    field = Field()
    tetrominos_types = [
        Tetromino.ITetromino(),
        Tetromino.OTetromino(),
        Tetromino.TTetromino(),
        Tetromino.STetromino(),
        Tetromino.ZTetromino(),
        Tetromino.JTetromino(),
        Tetromino.LTetromino()
    ]
    while True:
        current_tetromino = random.choice(tetrominos_types)
        best_row, best_column, best_field, best_drop_score, best_rotation = field.get_optimal_drop(current_tetromino, genes)
        current_tetromino.rotate(best_rotation)
        if best_column is None:
            break
        field.drop(current_tetromino, best_column)
        print(field)
        time.sleep(0.2)

def bot(genes):
    pass

if __name__ == '__main__':

    print("Egitim icin 1'e, terminalden gozlemlemek icin 2'ye, tetris_bot icin 3'e basiniz: ")

    choice = int(input())

    if choice == 1:
        print("Jenerasyon sayisini giriniz (max=10, min=1): ")
        gen_number = int(input())

        assert 0 < gen_number <= 10

        population = Population()
        population.init_first()

        if gen_number - 1 >= 1:
            population.run(gen_number - 1)

        chromosome = population.get_fittest_member()

        create_file(chromosome.genes)

    elif choice == 2:
        genes = read_file()
        play(genes)

    elif choice == 3:
        pass

