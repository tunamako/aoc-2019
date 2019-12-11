from aocd.models import Puzzle
import cProfile
from collections import defaultdict, namedtuple, Counter, deque
from itertools import permutations, combinations, chain, cycle, islice
import re
import math
from pprint import pprint
import numpy as np
import sys

Point = namedtuple('Point', ['x', 'y'])

def get_asteroids(_input):
    grid = [list(y) for y in _input]
    grid = np.swapaxes(np.array(grid, str), 0, 1) 
    return np.argwhere(grid == '#')

def part_one(_input):
    asteroids = {Point(x, y): set() for (x, y) in get_asteroids(_input)}
   
    for A, B in permutations(asteroids, 2):
        asteroids[A].add(math.atan2(A.y - B.y, A.x - B.x))

    max_ass = max(asteroids, key=lambda a: len(asteroids[a]))
    return (max_ass, len(asteroids[max_ass]))

def part_two(_input):
    station = part_one(_input)[0]
    ass_angles = defaultdict(lambda: [])
    start_angle = -1 * math.pi/2

    for x, y in get_asteroids(_input):
        angle = math.atan2(y - station.y, x - station.x)
        ass_angles[angle].append(Point(x,y))

    if start_angle not in ass_angles:
        ass_angles[start_angle] = []

    angles = sorted(list(ass_angles))
    man_dist = lambda p: abs(station.x - p.x) + abs(station.y - p.y)

    for angle in angles:
        ass_angles[angle].sort(key=man_dist, reverse=True)

    destroyed = 0
    for angle in islice(cycle(angles), angles.index(start_angle), None):
        if ass_angles[angle] == []:
            del ass_angles[angle]
            continue

        next_destroyed = ass_angles[angle].pop()
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
