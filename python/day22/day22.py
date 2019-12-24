from aocd.models import Puzzle
import cProfile
from collections import defaultdict, namedtuple, Counter, deque
from itertools import permutations, combinations, chain
import re
import math
import unittest

from advent_machine import AdventMachine, Paintbot

def increment(deck, line):
    amt = int(line.split(' ')[-1])
    ret = [None for i in range(len(deck))]

    for i in range(len(deck)):
        ret[(i*amt) % len(deck)] = deck[i]

    return ret

def part_one(_input, deck_len=10):
    deck = list(range(deck_len))

    for line in _input:
        if "cut" in line:
            amt = int(line.split(' ')[-1])
            deck = deck[amt:] + deck[:amt]
        elif "new" in line:
            deck.reverse()
        elif "increment" in line:
            deck = increment(deck, line)

    return deck

def part_two(_input):
    pass


class ShuffleTest(unittest.TestCase):

    def test_cut(self):
        _input = [
            "cut 3",
        ]
        self.assertEqual(part_one(_input), [3,4,5,6,7,8,9,0,1,2])
        _input = [
            "cut -4",
        ]
        self.assertEqual(part_one(_input), [6,7,8,9,0,1,2,3,4,5])

    def test_one(self):
        _input = [
            "deal with increment 7",
            "deal into new stack",
            "deal into new stack",
        ]
        self.assertEqual(part_one(_input), [0,3,6,9,2,5,8,1,4,7])

    def test_two(self):
        _input = [
            "cut 6",
            "deal with increment 7",
            "deal into new stack",
        ]
        self.assertEqual(part_one(_input), [3,0,7,4,1,8,5,2,9,6])

    def test_three(self):
        _input = [
            "deal with increment 7",
            "deal with increment 9",
            "cut -2",
        ]
        self.assertEqual(part_one(_input), [6,3,0,7,4,1,8,5,2,9])

    def test_four(self):
        _input = [
            "deal into new stack",
            "cut -2",
            "deal with increment 7",
            "cut 8",
            "cut -4",
            "deal with increment 7",
            "cut 3",
            "deal with increment 9",
            "deal with increment 3",
            "cut -1",
        ]
        self.assertEqual(part_one(_input), [9,2,5,8,1,4,7,0,3,6])


if __name__ == '__main__':
    puzzle = Puzzle(year=2019, day=22)
    _input = puzzle.input_data.split('\n')
    #_input = [line[:-1] for line in open("input").readlines()]
    print(part_one(_input, 10007).index(2019))
    #print(part_two(_input))

    #cProfile.run('print(part_one(_input))')
    #cProfile.run('print(part_two(_input))')
    
    unittest.main()