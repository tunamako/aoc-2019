from aocd.models import Puzzle
import cProfile
from collections import defaultdict, namedtuple, Counter, deque
from itertools import permutations, combinations, chain, cycle
import re
import math

from advent_machine import AdventMachine, Paintbot

nat_value = None

def parse_packets(packets, output):
    #print(output)
    for i in range(0, len(output), 3):
        dest, x, y = output[i:i+3]
        if dest == 255:
            nat_packet = (x,y)
            continue
        packets[dest].append((x,y))

def is_idle(machines, packets):
    for m in machines:
        if m.output != []:
            #print(m.output)
            return False

    for i, p in enumerate(packets):
        if p != []:
            #print(i, p)
            return False
    return True

def part_one(_input):
    machines = [AdventMachine(_input, return_output=True) for x in range(50)]

    for i in range(50):
        machines[i].execute(i)

    packets = [[] for x in range(50)]
    last_sent_nat_value = None
    while True:
        for i, m in enumerate(machines):
            if m.output:
                parse_packets(packets, m.output)

            if packets[i] == []:
                m.execute(-1)
            else:
                for x, y in packets[i]:
                    m.execute(x)
                    m.execute(y)

                    parse_packets(packets, m.output)

        if is_idle(machines, packets):
            print("wah")
            if nat_value[1] == last_sent_nat_value:
                return nat_value[1]
            last_sent_nat_value = nat_value[1]
            machines[0].execute(nat_value[0])
            machines[0].execute(nat_value[1])


def part_two(_input):
    pass


if __name__ == '__main__':
    puzzle = Puzzle(year=2019, day=23)
    _input = list(map(int, puzzle.input_data.split(',')))
    #_input = open('bigboy').readlines()

    print(part_one(_input))
    #print(part_two(_input))

    #cProfile.run('print(part_one(_input))')
    #cProfile.run('print(part_two(_input))')
