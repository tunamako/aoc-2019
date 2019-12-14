from aocd.models import Puzzle
import cProfile
from collections import defaultdict, namedtuple, Counter, deque
from itertools import permutations, combinations, chain
import re
import math
from functools import reduce

from advent_machine import AdventMachine


class Moon(object):

    def __init__(self, x, y, z):
        self.start_coords = [x, y, z]
        self.coords = [x, y, z]
        self.vel = [0, 0, 0]

        self.cyc_lens = [0, 0, 0]

    def __str__(self):
        return "Coords: {} Vel: {}\n".format(self.coords, self.vel)

    def apply_gravity(self, B):
        for v in range(3):
            if self.coords[v] > B.coords[v]:
                self.vel[v] += -1
                B.vel[v] += 1
            elif self.coords[v] < B.coords[v]:
                self.vel[v] += 1
                B.vel[v] += -1

    def apply_velocity(self):
        for v in range(3):
            self.coords[v] += self.vel[v]

    def check_cycles(self, step):
        for v in range(3):
            if (self.coords[v] == self.start_coords[v] and \
                self.cyc_lens[v] == 0):

                self.cyc_lens[v] = step
                print("len found! ", step)

    def pot_energy(self):
        return sum(map(abs, self.coords))

    def kin_energy(self):
        return sum(map(abs, self.vel))

    def tot_energy(self):
        return self.pot_energy() * self.kin_energy()


def part_one(_input):
    moons = [list(filter(lambda x: x not in ['x','y','z','=',' ','<','>'], m)) for m in _input]
    moons = [Moon(*map(int, (''.join(m)).split(','))) for m in moons]

    for i in range(1000):
        for A, B in combinations(moons, 2):
            A.apply_gravity(B)

        for m in moons:
            m.apply_velocity()

    return sum([m.tot_energy() for m in moons])

def part_two(_input):
    _moons = [list(filter(lambda x: x not in ['x','y','z','=',' ','<','>'], m)) for m in _input]

    cyc_lens = []
    for v in range(3):
        moons = [Moon(*map(int, (''.join(m)).split(','))) for m in _moons]
        initial_states = [m.coords[v] for m in moons]

        step = 1
        while True:
            for A, B in combinations(moons, 2):
                A.apply_gravity(B)

            for m in moons:
                m.apply_velocity()
            step += 1

            if initial_states == [m.coords[v] for m in moons]:
                cyc_lens.append(step)
                break

    lcm = lambda a,b: int(a * b / math.gcd(a, b))
    return reduce(lcm, cyc_lens)

if __name__ == '__main__':
    puzzle = Puzzle(year=2019, day=12)
    _input = puzzle.input_data.split('\n')
    #_input = open('bigboy').readlines()

    print(part_one(_input))
    print(part_two(_input))

    #cProfile.run('print(part_one(_input))')
    #cProfile.run('print(part_two(_input))')
