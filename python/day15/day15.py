from aocd.models import Puzzle
import cProfile
from collections import defaultdict, namedtuple, Counter, deque
from itertools import permutations, combinations, chain
import re
import math
import numpy as np

from advent_machine import AdventMachine, Paintbot

Point = namedtuple("Point", ['x', 'y'])

moves = [' NSWE']

class RepairDroid(object):

    def __init__(self, tape):
        self.brain = AdventMachine(tape, return_output=True)
        self.grid = np.full((42, 23), ' ')

        self.score = 0

        self.brain.execute()
        self.gen_grid()

    def gen_grid(self):
        output = self.brain.output
        for i in range(0, len(output), 3):
            if output[i] == -1 and output[i+1] == 0:
                self.score = output[i+2]
                continue

            self.grid[output[i]][output[i+1]] = tile_types[output[i+2]]

    def __str__(self):
        out = str(self.score) + "\n"
        for x in np.swapaxes(self.grid, 0, 1):
            out += ''.join(x) + "\n"

        return out

    def play(self):
        next_input = 1

        while self.brain.execute(next_input) == None:
            if self.brain.output[0] == 0:
                # Wall
            elif self.brain.output[0] == 2:
                # Oxygen

def part_one(_input):
    brain = RepairDroid(_input)
    #self.grid = np.full((42, 23), ' ')


def part_two(_input):
    pass


if __name__ == '__main__':
    puzzle = Puzzle(year=2019, day=15)
    _input = list(map(int, puzzle.input_data.split(',')))
    #_input = open('bigboy').readlines()

    print(part_one(_input))
    print(part_two(_input))

    #cProfile.run('print(part_one(_input))')
    #cProfile.run('print(part_two(_input))')
