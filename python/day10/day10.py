from aocd.models import Puzzle
import cProfile
from collections import defaultdict, namedtuple, Counter, deque
from itertools import permutations, combinations, chain, cycle, islice
import re
import math
from pprint import pprint
import numpy as np
import sys

np.set_printoptions(threshold=sys.maxsize)

Point = namedtuple('Point', ['x', 'y'])

def dist(A, B):
    return abs(A.x - B.x) + abs(A.y - B.y)

def part_one(_input):
    grid = [list(y) for y in _input]
    grid = np.swapaxes(np.array(grid, str), 0, 1)

    asteroids = {}

    for x in range(len(grid)):
        for y in range(len(grid[0])):
            if grid[x][y] == '#':
                asteroids[Point(x,y)] = set()

    
    for A in asteroids:
        angles = set()
        for B in asteroids:
            if A is not B:
                asteroids[A].add(math.atan2(A.y - B.y, A.x - B.x))

    max_ass = max(asteroids, key=lambda a: len(asteroids[a]))
    return len(asteroids[max_ass])

def part_two(_input):
    grid = [list(y) for y in _input]
    grid = np.swapaxes(np.array(grid, str), 0, 1)

    station = (Point(26, 28), defaultdict(lambda: []))
    asteroids = set()

    for x in range(len(grid)):
        for y in range(len(grid[0])):
            if grid[x][y] == '#':
                if Point(x,y) != station[0]:
                    angle = -1 * math.atan2(y - station[0].y, x - station[0].x)
                    station[1][angle].append(Point(x,y))

    angles = sorted(list(station[1].keys()), reverse=True)
    if math.pi/2 not in angles:
        angles.append(math.pi/2)
        angles.sort(reverse=True)

    for a in angles:
        station[1][a].sort(key=lambda p: dist(station[0], p), reverse=True)

    start_idx = angles.index(math.pi/2)
    destroyed = 0
    for angle in islice(cycle(angles), start_idx, None):
        try:
            next_destroyed = station[1][angle].pop()
        except IndexError:
            continue
        destroyed += 1

        if destroyed == 200:
            return (100 * next_destroyed.x) + next_destroyed.y

if __name__ == '__main__':
    puzzle = Puzzle(year=2019, day=10)
    _input = puzzle.input_data.split('\n')
    #_input = [line[:-1] for line in open('input').readlines()]

    print(part_one(_input))
    print(part_two(_input))

    #cProfile.run('print(part_one(_input))')
    #cProfile.run('print(part_two(_input))')
