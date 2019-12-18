from aocd.models import Puzzle
import cProfile
from collections import defaultdict, namedtuple, Counter, deque
from itertools import permutations, combinations, chain, cycle, islice
import re
import math

import numpy as np

def process_input(input_arr, phases, offset=0):

    for p in range(phases):
        print(p)
        remaining_sum = np.sum(input_arr[offset-1:])
        previous_val = input_arr[offset-1]

        for i in range(offset, len(input_arr)):
            remaining_sum -= previous_val
            previous_val = input_arr[i]
            input_arr[i] = abs(remaining_sum) % 10

    return ''.join(map(str, input_arr[offset:offset+8]))

def part_one(_input):
    return process_input(_input, 100)

def part_two(_input):
    offset = int(''.join(map(str, _input))[:7])

    return process_input(_input, 100, offset)

if __name__ == '__main__':
    puzzle = Puzzle(year=2019, day=16)
    _input = puzzle.input_data * 10000
    #_input = "03036732577212944063491565474664" * 10000
    _input = np.array(list(map(int, _input)))
    #_input = open('bigboy').readlines()

    #print(part_one(_input))
    print(part_two(_input))

    #cProfile.run('print(part_one(_input))')
    #cProfile.run('print(part_two(_input))')
