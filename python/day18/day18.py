import cProfile
from collections import defaultdict, namedtuple, Counter, deque
from itertools import permutations, combinations, chain
import re
import math
import numpy as np
from pprint import pprint
import time
import sys

sys.setrecursionlimit(2000)

def print_grid(grid):
    out = ""
    for x in np.swapaxes(grid, 0, 1):
        out += ''.join(x) + "\n"

    print(out)

moves = [
    (1, 0),
    (-1, 0),
    (0, 1),
    (0, -1),
]

def get_available_paths(grid, pos, cur_path=None):
    if cur_path is None:
        cur_path = set()
    cur_path.add(pos)

    all_paths = dict()

    for m in moves:
        next_move = (pos[0] + m[0], pos[1] + m[1])
        value = grid[next_move[0]][next_move[1]]

        if next_move in cur_path:
            continue
        elif value == '.':
            all_paths.update(get_available_paths(grid, next_move, cur_path))
        elif value.islower():
            all_paths[value] = (next_move, len(cur_path))

    cur_path.remove(pos)
    return all_paths

seen_subpaths = dict()

def get_shortest_path_from(grid, pos):
    grid = np.copy(grid)
    key = grid[pos[0]][pos[1]]

    if key.islower():
        grid[pos[0]][pos[1]] = '.'
        if (door := np.argwhere(grid == key.upper())).any():
            grid[door[0][0]][door[0][1]] = '.'

    paths = get_available_paths(grid, pos, {pos})
    if not paths:
        return 0

    paths_as_str = ''.join(sorted(list(paths.keys())))
    #if len(paths_as_str) > 6:
    #print(key, paths_as_str)

    if key + paths_as_str in seen_subpaths:
        #print("wah")
        return seen_subpaths[key + paths_as_str]

    best_choice = None

    for k, path in paths.items():
        step_count = path[1]
        step_count += get_shortest_path_from(grid, path[0])

        if best_choice is None or step_count < best_choice:
            best_choice = step_count

    if best_choice is not None:
        seen_subpaths[key + paths_as_str] = best_choice
        return best_choice
    else:
        seen_subpaths[key + paths_as_str] = 0
        return 0

def part_one(_input):

    grid = np.swapaxes(np.array(_input), 0, 1)
    #print_grid(grid)
    pos = np.argwhere(grid == '@')[0]
    pos = (pos[0], pos[1])

    grid[pos[0]][pos[1]] = '.'

    return get_shortest_path_from(grid, pos)

    # while True:

        # Find all targets and the shortest paths to them (keys)
        # Choose which one to move to
        # Move to chosen target
        # Replace unlocked door with a '.'


def part_two(_input):
    pass

if __name__ == '__main__':
    #puzzle = Puzzle(year=2019, day=17)
    _input = [list(line[:-1]) for line in open("input").readlines()]
    #_input = open('bigboy').readlines()

    #print(part_one(_input))
    #print(part_two(_input))

    cProfile.run('print(part_one(_input))')
    #cProfile.run('print(part_two(_input))')
