from aocd.models import Puzzle
import cProfile
from collections import defaultdict, namedtuple, Counter, deque
from itertools import permutations, combinations, chain
import re
import math

from advent_machine import AdventMachine, Paintbot

required = defaultdict(lambda: 0)
overflow = defaultdict(lambda: 0)
chems = {}

class Chem(object):

    def __init__(self, output, reagents=[]):
        self.out_count, self.id = output.split(' ')
        self.out_count = int(self.out_count)
        self.reagents = []
        for r in reagents:
            amt, _id = r.split(' ')
            self.reagents.append([int(amt), _id])

        chems[self.id] = self
        overflow[self.id] = 0
        required[self.id] = 0

    def create(self, amount):
        required[self.id] += amount

        if overflow[self.id] >= amount:
            overflow[self.id] -= amount
            return
        elif 0 < overflow[self.id] < amount:
            amount -= overflow[self.id]
            overflow[self.id] = 0

        react_count = math.ceil(amount / self.out_count)
        overflow[self.id] += (react_count * self.out_count) - amount

        #print(self.id)
        #print(react_count, self.out_count)

        for r in self.reagents:
            chems[r[1]].create(react_count * int(r[0]))            

class ORE(Chem):

    def __init__(self, *args, avail_ore=-1):
        self.avail_ore = avail_ore

        super().__init__(*args)

    def create(self, amount):
        self.avail_ore -= amount

        super().create(amount)


def part_one(_input):
    _input = [x.split(" => ") for x in _input]
    _input = [(l[0].split(", "), l[1]) for l in _input]

    chems["ORE"] = ORE("1 ORE")

    for react in _input:
        chem = Chem(react[1], react[0])

    chems["FUEL"].create(1)

    print(required.items())
    print(overflow.items())


    return required["ORE"]

def part_two(_input):
    _input = [x.split(" => ") for x in _input]
    _input = [(l[0].split(", "), l[1]) for l in _input]

    chems["ORE"] = ORE("1 ORE", avail_ore=1000000000000)
    for react in _input:
        chem = Chem(react[1], react[0])

    chems["FUEL"].create(998536)

    return required["FUEL"]


if __name__ == '__main__':
    puzzle = Puzzle(year=2019, day=14)
    _input = puzzle.input_data.split('\n')

    #print(part_one(_input))
    print(part_two(_input))

    #cProfile.run('print(part_one(_input))')
    #cProfile.run('print(part_two(_input))')
