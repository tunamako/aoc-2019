#from aocd.models import Puzzle
import cProfile
from collections import defaultdict, namedtuple, Counter, deque
from itertools import permutations, combinations, chain, count
from copy import deepcopy
import re
import math
import numpy as np
import matplotlib.pyplot as plt
import time
from queue import Queue

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

def droid_id():
    for i in count(start=1, step=1):
        yield i

seen = {Point(0,0)}
walls = set()

class RepairDroid(object):

    get_droid_id = droid_id()

    def __init__(self, tape, facing="N", pos=Point(0,0), path={Point(0,0)}):
        self.brain = AdventMachine(tape, return_output=True)
        self.path = path
        self.pos = pos

        self.facing = facing
        self.id = next(self.get_droid_id)

    def are_opposite_dirs(self, a, b):
        return ((a + b == "NS") or \
                (a + b == "SN") or \
                (a + b == "EW") or \
                (a + b == "WE"))

    def duplicate(self, ignore_backtrack=True):
        new_droids = []
        for new_dir in "NSEW":
            if ignore_backtrack and (self.are_opposite_dirs(new_dir, self.facing)):
                continue
            new_droid = RepairDroid(self.brain.tape, new_dir, Point(self.pos.x, self.pos.y), deepcopy(self.path))
            new_droids.append(new_droid)
            #print(self.id, self.facing, new_droid.id, new_dir)
        return new_droids

    def record_wall(self):
        move = moves[self.facing]
        wall_pos = Point(self.pos.x + move[0], self.pos.y + move[1])

        walls.add(wall_pos)

    def record_move(self):
        move = moves[self.facing]
        next_pos = Point(self.pos.x + move[0], self.pos.y + move[1])

        self.path.add(next_pos)

        seen.add(next_pos)
        self.pos = next_pos

    def step(self):
        self.brain.execute(' NSWE'.index(self.facing))

        if self.brain.output[0] == 0:
            # Wall
            self.record_wall()
            return -1
        elif self.brain.output[0] == 1:
            # Moved
            self.record_move()
        elif self.brain.output[0] == 2:
            return 0

def part_one(_input, show_plot=True):

    #droid.play(stop_at_oxygen=False)
    #print(droid.pos)
    end_droid = None
    droids = [
        RepairDroid(_input, facing="N"),
        RepairDroid(_input, facing="S"),
    ]

    while droids:
        new_droids = []

        for droid in droids:
            for d in droid.duplicate():
                err = d.step()

                if err == 0:
                    oxy_pos = d.pos
                    oxy_path_len = len(d.path)
                    new_droids.append(d)
                elif err == -1:
                    continue
                else:
                    new_droids.append(d)

        droids = new_droids

    fig = plt.figure()
    ax1 = fig.add_subplot(111)
    x, y = zip(*[(p.x, p.y) for p in seen])
    ax1.scatter(x, y, c='b')
    x, y = zip(*[(p.x, p.y) for p in walls])
    ax1.scatter(x, y, c='r')

    if show_plot:
        plt.show()

    return oxy_path_len, oxy_pos

def part_two(_input):
    oxy_path_len, oxy_pos = part_one(_input, False)
    print(oxy_path_len)
    leads = [oxy_pos]
    mins = 0
    filled = {Point(12, -11)}
    while leads:
        mins += 1
        new_leads = []

        for p in leads:
            for adj in [Point(p.x + m[1][0], p.y + m[1][1]) for m in moves.items()]:
                if adj in filled or adj in walls:
                    continue
                filled.add(adj)
                new_leads.append(adj) 
        leads = new_leads

    return mins

if __name__ == '__main__':
    #puzzle = Puzzle(year=2019, day=15)
    #_input = list(map(int, puzzle.input_data.split(',')))
    _input = list(map(int, open("input").readline().split(',')))

    #print(part_one(_input))
    print(part_two(_input))

    #cProfile.run('print(part_one(_input))')
    #cProfile.run('print(part_two(_input))')
