from aocd.models import Puzzle
import cProfile
from collections import defaultdict, namedtuple, Counter, deque
from itertools import permutations, combinations, chain
import re
import math

from advent_machine import AdventMachine, Paintbot

class Chem(object):

    def __init__(self, output, reagents=[], chems={}):
        self.out_count, self.id = output.split(' ')
        
        self.reagents = []
        for r in reagents:
            amt, _id = r.split(' ')
            self.reagents.append([int(amt), chems[_id]])
        chems[self.id] = self

    def ore_count(self):
        count = 0
        for r in self.reagents:
            count += r[0] * r[1].ore_count()

        print(self.id, count * int(self.out_count))
        return count * int(self.out_count)

class ORE(Chem):

    def ore_count(self):
        return 1

def part_one(_input):
    _input = [x.split(" => ") for x in _input]
    _input = [(l[0].split(", "), l[1]) for l in _input]

    chems = {
        "ORE": ORE("1 ORE")
    }

    for react in _input:
        print(react)
        chem = Chem(react[1], react[0], chems)

    print(chems["FUEL"].ore_count())

def part_two(_input):
    pass


if __name__ == '__main__':
    puzzle = Puzzle(year=2019, day=14)
    _input = puzzle.input_data.split('\n')
    _input = [
        "10 ORE => 10 A",
        "1 ORE => 1 B",
        "7 A, 1 B => 1 C",
        "7 A, 1 C => 1 D",
        "7 A, 1 D => 1 E",
        "7 A, 1 E => 1 FUEL",
    ]
    #_input = open('bigboy').readlines()

    print(part_one(_input))
    print(part_two(_input))

    #cProfile.run('print(part_one(_input))')
    #cProfile.run('print(part_two(_input))')
