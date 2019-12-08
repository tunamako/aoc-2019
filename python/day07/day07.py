from aocd.models import Puzzle
import cProfile
from collections import defaultdict, namedtuple, Counter, deque
from itertools import permutations, combinations, chain, cycle
import re
import math
import time

class AdventMachine(object):

    def add(self, *args):
        self.tape[args[2]] = args[0] + args[1]

    def mul(self, *args):
        self.tape[args[2]] = args[0] * args[1]

    def inp(self, *args):
        if self.next_input is None:
            self.paused = True
            self.next_input_loc = args[0]
        else:
            self.tape[args[0]] = self.next_input
            self.next_input = None
            self.next_input_loc = None

    def outp(self, *args):
        #print(args[0])
        self.output.append(args[0])

    def jmpt(self, *args):
        if args[0]: self.ip = args[1]

    def jmpf(self, *args):
        if not args[0]: self.ip = args[1]

    def lt(self, *args):
        self.tape[args[2]] = int(args[0] < args[1])

    def eq(self, *args):
        self.tape[args[2]] = int(args[0] == args[1])

    def ascii(self, *args):
        print(chr(args[0]), end="")

    def __init__(self, tape=[99], start_input=None, return_output=False):
        self.opcodes = {
            1: (3, self.add),
            2: (3, self.mul),
            3: (1, self.inp),
            4: (1, self.outp),
            5: (2, self.jmpt),
            6: (2, self.jmpf),
            7: (3, self.lt),
            8: (3, self.eq),
            9: (1, self.ascii),
        }
        self.tape = tape.copy()
        self.ip = 0
        self.debug = False
        self.return_output = return_output

        self.next_input = start_input
        self.output = []
        self.paused = False

    def reinit(self, tape, start_input=None):
        self.tape = tape.copy()
        self.ip = 0
        self.next_input = start_input
        self.output = []
        self.paused = False

    def execute(self, next_input=None):
        if next_input is not None:
            self.next_input = next_input

        if self.paused:
            self.paused = False
            self.inp(self.next_input_loc)
            self.ip += 2
        else:
            self.output = []

        while (instr := self.tape[self.ip]) != 99:
            ip_start = self.ip
            code = instr % 100
            modes = [(instr // n) % 10 for n in [100, 1000, 10000]]
            args = self.tape[self.ip+1 : self.ip+4]

            argc, op = self.opcodes[code]

            for i in range(2):
                try:
                    if not modes[i] and code != 3:
                        args[i] = self.tape[args[i]]
                except:
                    break
            op(*args)

            if self.paused:
                return None

            if self.ip == ip_start:
                self.ip += argc + 1

        if self.return_output:
            return self.output


def part_one(_input):
    machine = AdventMachine(return_output=True)

    max_out = 0
    for order in permutations([0,1,2,3,4]):
        out_signal = 0
        for phase in order:
            machine.reinit(_input)
            machine.execute(phase)
            out_signal = machine.execute(out_signal).pop()

        max_out = max(max_out, out_signal)

    return max_out

def part_two(_input):
    max_out = 0

    for phases in permutations([5,6,7,8,9]):
        machines = [AdventMachine(_input, phase, True) for phase in phases]

        for m in machines:
            assert(m.execute() == None)

        next_input = 0

        for m in cycle(machines):
            if m.execute(next_input) is not None and m is machines[-1]:
                break
            else:
                next_input = m.output.pop()

        max_out = max(machines[-1].output.pop(), max_out)

    return max_out


if __name__ == '__main__':
    puzzle = Puzzle(year=2019, day=7)
    _input = list(map(int, puzzle.input_data.split(',')))
    #_input = open('bigboy').readlines()
    #_input = "3,26,1001,26,-4,26,3,27,1002,27,2,27,1,27,26,27,4,27,1001,28,-1,28,1005,28,6,99,0,0,5"
    #_input = "3,52,1001,52,-5,52,3,53,1,52,56,54,1007,54,5,55,1005,55,26,1001,54,-5,54,1105,1,12,1,53,54,53,1008,54,0,55,1001,55,1,55,2,53,55,53,4,53,1001,56,-1,56,1005,56,6,99,0,0,0,0,10"
    #_input = list(map(int, _input.split(',')))
    print(part_one(_input))
    print(part_two(_input))

    #cProfile.run('print(part_one(_input))')
    #cProfile.run('print(part_two(_input))')
