from aocd.models import Puzzle
import cProfile
from collections import defaultdict, namedtuple, Counter, deque
from itertools import permutations, combinations, chain
import re
import math
import numpy as np

from advent_machine import AdventMachine, Paintbot

def print_grid(grid):
    out = ""
    for x in np.swapaxes(grid, 0, 1):
        out += ''.join(x) + "\n"

    print(out)

def parse_portals(grid):
    portals = defaultdict(lambda: [])

    for x, y in np.ndindex((grid.shape[0]-1, grid.shape[1]-1)):
        if grid[x,y].isupper():

            if x < len(grid) and grid[x+1,y].isupper():
                key = grid[x,y] + grid[x+1,y]
                try:
                    val = (x-3, y-2) if grid[x-1,y] == '.' else (x, y-2) 
                except:
                    continue
                portals[key].append(val)

            elif y < len(grid[0]) and grid[x,y+1].isupper():
                key = grid[x,y] + grid[x,y+1]
                try:
                    val = (x-2, y-3) if grid[x,y-1] == '.' else (x-2, y) 
                except:
                    continue
                portals[key].append(val)

    return portals

def part_one(_input):
    grid = np.swapaxes(np.array(_input), 0, 1)
    portals = parse_portals(grid)
    grid = grid[2:-2, 2:-2]
    print_grid(grid)

    start, end = portals['AA'][0], portals['ZZ'][0]

    

def part_two(_input):
    pass


if __name__ == '__main__':
    #puzzle = Puzzle(year=2019, day=20)
    _input = [list(line[:-1]) for line in open("input").readlines()]

    #_input = open('bigboy').readlines()

    print(part_one(_input))
    #print(part_two(_input))

    #cProfile.run('print(part_one(_input))')
    #cProfile.run('print(part_two(_input))')
