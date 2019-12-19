from aocd.models import Puzzle
import cProfile
from collections import defaultdict, namedtuple, Counter, deque
from itertools import permutations, combinations, chain
import itertools
import re
import math

from advent_machine import AdventMachine, Paintbot

def is_pulled(machine, _input, x, y):
    machine.reinit(_input)
    machine.execute(x)
    machine.execute(y)

    try:
        return machine.output[0] == 1
    except:
        return False

def part_one(_input):
    machine = AdventMachine(_input, return_output=True)
    count = 0
    min_y = 0

    for i in range(5, 50):
        min_y_set = False

        for j in itertools.count(min_y, 1):
            if is_pulled(machine, _input, i, j):
                #print(min_y_set, i, j, machine.output)
                if not min_y_set:
                    min_y = j
                    min_y_set = True
                count += machine.output[0]

            elif min_y_set:
                break

    return count + 1



def part_two(_input):
    machine = AdventMachine(_input, return_output=True)
    min_y = 0
    ship_size = 99

    for x in itertools.count(5, 1):
        for y in range(min_y, min_y + 5):
            if is_pulled(machine, _input, x, y):
                if is_pulled(machine, _input, x-ship_size, y+ship_size):
                    return (x-ship_size) * 10000 + y

                min_y = y
                break


if __name__ == '__main__':
    puzzle = Puzzle(year=2019, day=19)
    _input = list(map(int, puzzle.input_data.split(',')))
    #_input = open('bigboy').readlines()

    #print(part_one(_input))
    #print(part_two(_input))

    #cProfile.run('print(part_one(_input))')
    cProfile.run('print(part_two(_input))')
