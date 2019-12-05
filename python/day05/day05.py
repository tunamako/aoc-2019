from aocd.models import Puzzle
import cProfile
from collections import defaultdict, namedtuple, Counter, deque
from itertools import permutations, combinations, chain
import re
import math
import time

class AdventMachine(object):
    # opcode: (argc, op)

    def add(self, a, b, out_reg):
        self.tape[out_reg] = a + b

    def mul(self, a, b, out_reg):
        self.tape[out_reg] = a * b

    def _input(self, out_reg):
        self.tape[out_reg] = 1

    def _output(self, out_reg):
        print(self.tape[out_reg])

    def __init__(self, *args, **kwargs):
        self.opcodes = {
            1: (3, lambda a, b, c: a + b),
            2: (3, lambda a, b, c: a * b),
            3: (1, lambda a: 1),
            4: (1, lambda a: print(self.tape[a])),
        }
        self.tape = [99]
        self.ip = 0
        self.mode = 0

    def set_tape(self, tape):
        self.tape = tape.copy()
        self.ip = 0
        self.mode = 0

    def execute(self):
        output = []
        while (instr := str(self.tape[self.ip])) != "99":

            code = int(instr[-2:])
            #print(self.ip, instr)
            op = self.opcodes[code]
            argc = op[0]
            args = self.tape[self.ip + 1 : self.ip + 1 + argc]

            if len(instr) > 2:
                modes = instr[:-2][::-1].split()
                for i, m in enumerate(modes):
                    if m == 0:
                        args[i] = self.tape[args[i]]
            elif argc > 1:
                modes = []
                for i in range(argc - 1):
                    args[i] = self.tape[args[i]]
            else:
                modes = []

            print(code, modes, args)
            if (result := op[1](*args)) is not None:
                self.tape[args[-1]] = result

            #print(instr, code, modes, args)
            #time.sleep(0.5)

            self.ip += argc + 1

def part_one(_input):
    machine = AdventMachine()
    machine.set_tape(_input)
    return machine.execute()

def part_two(_input):
    pass


if __name__ == '__main__':
    puzzle = Puzzle(year=2019, day=5)
    _input = list(map(int, puzzle.input_data.split(',')))

    #_input = open('bigboy').readlines()

    part_one(_input)
    part_two(_input)

    #cProfile.run('print(part_one(_input))')
    #cProfile.run('print(part_two(_input))')
