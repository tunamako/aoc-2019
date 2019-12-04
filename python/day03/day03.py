from aocd.models import Puzzle
import cProfile
from collections import defaultdict, namedtuple, Counter, deque
from itertools import permutations, combinations, chain
import re
import math


directions = {'L': (-1, 0), 'R': (1, 0), 'U': (0, 1), 'D': (0, -1)}


def get_points(wire, existing_wire=None):
    points = dict()
    x, y, stepcount = 0, 0, 0

    for entry in wire:
        mod = directions[entry[0]]
        distance = int(entry[1:])

        for i in range(1, distance + 1):
            x, y = x + mod[0], y + mod[1]

            tmp = (x, y)
            if existing_wire:
                if tmp not in points and tmp in existing_wire:
                    points[tmp] = stepcount + i
            else:
                if tmp not in points:
                    points[tmp] = stepcount + i

        stepcount += distance

    return points


def solve(_input):
    wire_A = get_points(_input[0].split(','))
    wire_B = get_points(_input[1].split(','), wire_A)

    def dist_from_start(p):
        return sum(map(abs, p))

    def total_stepcount(p):
        return wire_A[p] + wire_B[p]

    min_by_dist = min(wire_B, key=dist_from_start)
    min_by_steps = min(wire_B, key=total_stepcount)

    print("Part One: {}".format(dist_from_start(min_by_dist)))
    print("Part Two: {}".format(total_stepcount(min_by_steps)))


if __name__ == '__main__':
    puzzle = Puzzle(year=2019, day=3)
    _input = puzzle.input_data.split('\n')

    #_input = open('input').readlines()

    #solve(_input)

    cProfile.run('solve(_input)')
