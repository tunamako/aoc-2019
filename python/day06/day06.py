from aocd.models import Puzzle
import cProfile
from collections import defaultdict, namedtuple, Counter, deque
from itertools import permutations, combinations, chain
import re
import math
import queue

def gen_graph(lines):
    orbits = defaultdict(lambda: ['', []])

    for line in _input:
        parent, child = line.split(')')
        orbits[parent][1].append(child)
        orbits[child][0] = parent

    return orbits

def part_one(_input):
    orbits = gen_graph(_input)

    levels = dict(orbits).copy()
    que = queue.Queue()

    levels['COM'] = 0
    orbit_count = 0
    que.put('COM')

    while not que.empty():
        cur_node = que.get()
        orbit_count += levels[cur_node]

        if cur_node not in orbits:
            continue

        for child in orbits[cur_node][1]:
            que.put(child)
            levels[child] = levels[cur_node] + 1

    return orbit_count

def part_two(_input):
    orbits = gen_graph(_input)

    san_travel, you_travel = 0, 0
    san_path, you_path = [], []
    san_idx, you_idx = 'SAN', 'YOU'

    while True:
        san_path.append(san_idx)
        you_path.append(you_idx)

        if you_idx in san_path:
            san_path = san_path[1:san_path.index(you_idx)]
            you_path = you_path[1:]
            break
        elif san_idx in you_path:
            you_path = you_path[1:you_path.index(san_idx)]
            san_path = san_path[1:]
            break
        else:
            san_idx = orbits[san_idx][0]
            you_idx = orbits[you_idx][0]

    return len(san_path) + len(you_path) - 1


if __name__ == '__main__':
    puzzle = Puzzle(year=2019, day=6)
    _input = puzzle.input_data.split('\n')

    #_input = open('bigboy').readlines()

    print(part_one(_input))
    print(part_two(_input))

    #cProfile.run('print(part_one(_input))')
    #cProfile.run('print(part_two(_input))')
