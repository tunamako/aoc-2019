from aocd.models import Puzzle
import cProfile
from collections import defaultdict, namedtuple, Counter, deque
from itertools import permutations, combinations, chain
import re
import math
from pprint import pprint
import numpy as np
import os
import sys
import time

from advent_machine import AdventMachine, Paintbot

Point = namedtuple("Point", ['x', 'y'])

tile_types = [' ', 'X', 'O', '_', '*']


class ArcadeCabinet(object):

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

        while True:
            self.gen_grid()
            print(self)
            time.sleep(0.1)

            if len(np.argwhere(self.grid == 'O')) == 0:
                return

            paddle_x = np.argwhere(self.grid == '_')[0][0]
            ball_x = np.argwhere(self.grid == '*')[0][0]

            if paddle_x < ball_x:
                next_input = 1
            elif paddle_x > ball_x:
                next_input = -1
            elif paddle_x == ball_x:
                next_input = 0

            self.brain.execute(next_input)
            #time.sleep(1)




def part_one(_input):
    cab = ArcadeCabinet(_input)
    cab.run_program()
    count = 0
    for i in range(0, len(cab.brain.output), 3):
        if cab.brain.output[i+2] == 2:
            count += 1
    return count

def part_two(_input):
    _input[0] = 2
    cab = ArcadeCabinet(_input)
    cab.play()
    print(cab.score)

if __name__ == '__main__':
    puzzle = Puzzle(year=2019, day=13)
    _input = list(map(int, puzzle.input_data.split(',')))
    #_input = open('bigboy').readlines()

    #print(part_one(_input))
    print(part_two(_input))

    #cProfile.run('print(part_one(_input))')
    #cProfile.run('print(part_two(_input))')
