from aocd.models import Puzzle
import cProfile
from collections import defaultdict, namedtuple, Counter, deque
from itertools import permutations, combinations, chain
import re
import math


class AdventMachine(object):

    def extend_tape(self, loc):
        new_end = len(self.tape) + loc
        #print("Extending tape to ", new_end)
        self.tape += [0 for i in range(new_end)]

    def store(self, loc, value):
        try:
            self.tape[loc] = value
        except IndexError:
            self.extend_tape(loc)
            self.tape[loc] = value

    def read(self, loc):
        try:
            return self.tape[loc]
        except IndexError:
            self.extend_tape(loc)
            return self.tape[loc]


    def add(self, *args):
        self.store(args[2], args[0] + args[1])

    def mul(self, *args):
        self.store(args[2], args[0] * args[1])

    def inp(self, *args):
        if self.next_input is None:
            self.paused = True
            self.next_input_loc = args[0]
        else:
            self.store(args[0], self.next_input)
            self.next_input = None
            self.next_input_loc = None

    def outp(self, *args):
        self.output.append(args[0])

    def jmpt(self, *args):
        if args[0]: self.ip = args[1]

    def jmpf(self, *args):
        if not args[0]: self.ip = args[1]

    def lt(self, *args):
        self.store(args[2], int(args[0] < args[1]))

    def eq(self, *args):
        self.store(args[2], int(args[0] == args[1]))

    def adj_base(self, *args):
        self.relative_base += args[0]
        #print("Incremented base to ", self.relative_base)

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
            9: (1, self.adj_base),
        }
        self.tape = tape.copy()
        self.ip = 0
        self.debug = False
        self.return_output = return_output

        self.next_input = start_input
        self.output = []
        self.paused = False
        self.relative_base = 0

    def reinit(self, tape, start_input=None):
        self.tape = tape.copy()
        self.ip = 0
        self.next_input = start_input
        self.output = []
        self.paused = False
        self.relative_base = 0

    def execute(self, next_input=None):
        self.output = []

        if next_input is not None:
            self.next_input = next_input

        if self.paused:
            self.paused = False
            self.inp(self.next_input_loc)
            self.ip += 2

        while (instr := self.read(self.ip)) != 99:
            ip_start = self.ip
            code = instr % 100

            if len(str(instr)) > 2:
                modes = str(instr)[:-2][::-1].ljust(3, '0')
                modes = list(map(int, modes))
            else:
                modes = [0,0,0]

            args = self.tape[self.ip+1 : self.ip+4]

            argc, op = self.opcodes[code]

            if code == 3:
                if modes[0] == 2:
                    args[0] += self.relative_base
            elif code == 4:
                if modes[0] == 2:
                    args[0] = self.read(args[0] + self.relative_base)
                elif modes[0] == 0:
                    args[0] = self.read(args[0])
            elif code == 9:
                if modes[0] == 2:
                    args[0] = self.read(args[0] + self.relative_base)
                elif modes[0] == 0:
                    args[0] = self.read(args[0])
            else:
                for i in range(2):
                    if modes[i] == 0:
                        args[i] = self.read(args[i])
                    elif modes[i] == 2:
                        args[i] = self.read(args[i] + self.relative_base)

            if modes[2] == 2:
                args[2] += self.relative_base
            #print(instr, modes, args, self.output)

            op(*args)

            if self.paused:
                return None

            if self.ip == ip_start:
                self.ip += argc + 1

        if self.return_output:
            return self.output

Point = namedtuple("Point", ['x', 'y']) 

class Paintbot(object):

    def __init__(self, program):
        self.brain = AdventMachine(tape=program, return_output=True)
        self.pos = Point(0,0)
        self.facing = "N"
        self.panel = 0
        self.grid = dict()
        self.painted = 0

    def paint(self, color):
        if self.pos not in self.grid:
            self.painted += 1

        self.grid[self.pos] = color
        self.panel = color

    def step(self, count=1):
        moves = {
            'N': (0, 1),
            'S': (0, -1),
            'E': (1, 0),
            'W': (-1, 0),
        }

        move = moves[self.facing]
        self.pos = Point(self.pos.x + (count * move[0]), self.pos.y + (count * move[1]))

    def turn(self, direction):
        moves = [
            {'N':'W', 'E':'N', 'S':'E', 'W':'S'},
            {'N':'E', 'E':'S', 'S':'W', 'W':'N'},
        ]
        self.facing = moves[direction][self.facing]
        self.step()

    def run_program(self):
        
        while self.brain.execute(self.panel) is None:
            print(self.brain.output, self.pos, self.panel)
            next_panel, next_step = self.brain.output
            self.paint(next_panel)
            self.turn(next_step)

def part_one(_input):
    bot = Paintbot(_input)
    bot.run_program()
    print(bot.painted)

def part_two(_input):
    pass


if __name__ == '__main__':
    puzzle = Puzzle(year=2019, day=11)
    _input = list(map(int, puzzle.input_data.split(',')))
    #_input = open('bigboy').readlines()

    print(part_one(_input))
    #print(part_two(_input))

    #cProfile.run('print(part_one(_input))')
    #cProfile.run('print(part_two(_input))')
