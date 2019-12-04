from aocd.models import Puzzle
import cProfile
from collections import defaultdict, namedtuple, Counter, deque
from itertools import permutations, combinations, chain
import re
import math
import copy


class AdventMachine(object):
    # opcode: (argc, op)
    opcodes = {
        1: (2, lambda a, b: a + b),
        2: (2, lambda a, b: a * b),
    }

    def __init__(self, *args, **kwargs):
        self.tape = [99]
        self.ip = 0

    def set_tape(self, tape):
        self.tape = tape.copy()
        self.ip = 0

    def execute(self):
        while (code := self.tape[self.ip]) != 99:
            op = self.opcodes[code]
            argc = op[0]
            args = self.tape[self.ip + 1 : self.ip + 1 + argc]
            args = [self.tape[a] for a in args]

            out_reg = self.tape[self.ip + 1 + argc]


            self.tape[out_reg] = op[1](*args)

            self.ip += argc + 2

        return self.tape[0]


def part_one(_input):
    _input[1] = 12
    _input[2] = 2

    machine = AdventMachine()
    machine.set_tape(_input)
    return machine.execute()


def part_two(_input):
    machine = AdventMachine()

    for noun in range(1, 99):
        for verb in range(1, 99):
            _input[1] = noun
            _input[2] = verb
            machine.set_tape(_input)

            if machine.execute() == 19690720:
                return 100 * noun + verb


if __name__ == '__main__':
    puzzle = Puzzle(year=2019, day=2)
    _input = list(map(int, puzzle.input_data.split(',')))
    #_input = list(map(int, open('bigboy').readlines()[0].split(',')))

    #_input = [1,9,10,3,2,3,11,0,99,30,40,50]
    print(part_one(_input))
    print(part_two(_input))
 
    #cProfile.run('print(part_one(_input))')
    #cProfile.run('print(part_two(_input))')
