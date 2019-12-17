from aocd.models import Puzzle
import cProfile
from collections import defaultdict, namedtuple, Counter, deque
from itertools import permutations, combinations, chain
import re
import math
import numpy as np
import matplotlib.pyplot as plt
import time

from advent_machine import AdventMachine, Paintbot

Point = namedtuple("Point", ['x', 'y'])

# 0 : North
# 1 : South
# 2 : West
# 3 : East
moves = {
    "N": (0, 1),
    "S": (0, -1),
    "E": (1, 0),
    "W": (-1, 0),
}


class RepairDroid(object):

    def __init__(self, tape):
        self.brain = AdventMachine(tape, return_output=True)
        self.path = {Point(0,0)}
        self.seen = {Point(0,0)}

        self.pos = Point(0,0)
        self.walls = set()
        self.facing = "N"

    def turn_left(self):
        turns = {"N": "W", "W": "S", "S": "E", "E": "N"}
        self.facing = turns[self.facing]

    def turn_right(self):
        turns = {"W": "N", "S": "W", "E": "S", "N": "E"}
        self.facing = turns[self.facing]

    def record_wall(self):
        move = moves[self.facing]
        wall_pos = Point(self.pos.x + move[0], self.pos.y + move[1])

        self.walls.add(wall_pos)

    def record_move(self):
        move = moves[self.facing]
        next_pos = Point(self.pos.x + move[0], self.pos.y + move[1])
        if next_pos == Point(-2, 2):
            print("wah")

        if next_pos in self.path:
            try:
                self.path.remove(self.pos)
            except:
                pass
            self.path.remove(next_pos)
        else:
            self.path.add(next_pos)

        self.seen.add(next_pos)
        self.pos = next_pos

    def play(self, stop_at_oxygen=True):
        # Move forward until wall found, then:
            # keep wall on right hand side, moving along it
        use_rhr = True
        while True:
            #time.sleep(0.1)
            self.brain.execute(' NSWE'.index(self.facing))
            #print(len(self.walls), len(self.seen))
            if len(self.walls) == 858 and len(self.seen) == 799:
                print("wahwah")
                use_rhr = False
            if self.brain.output[0] == 0:
                # Wall
                self.record_wall()
                if use_rhr:
                    self.turn_left()
                else:
                    self.turn_right()
            elif self.brain.output[0] == 1:
                # Moved
                self.record_move()
                if use_rhr:
                    self.turn_right()
                else:
                    self.turn_left()

            elif self.brain.output[0] == 2:
                # Oxygen
                if stop_at_oxygen:
                    return

                self.record_move()
                if use_rhr:
                    self.turn_right()
                else:
                    self.turn_left()

def part_one(_input):
    droid = RepairDroid(_input)
    droid.play(stop_at_oxygen=False)
    print(droid.pos)

    fig = plt.figure()
    ax1 = fig.add_subplot(111)
    #858, 799
    x, y = zip(*[(p.x, p.y) for p in droid.seen])
    ax1.scatter(x, y, c='b')
    x, y = zip(*[(p.x, p.y) for p in droid.walls])
    ax1.scatter(x, y, c='r')

    plt.show()

    return len(droid.path)

def part_two(_input):
    pass


if __name__ == '__main__':
    puzzle = Puzzle(year=2019, day=15)
    _input = list(map(int, puzzle.input_data.split(',')))
    #_input = list(map(int, open("input").readline().split(',')))
    #_input = open('bigboy').readlines()

    print(part_one(_input))
    print(part_two(_input))

    #cProfile.run('print(part_one(_input))')
    #cProfile.run('print(part_two(_input))')
