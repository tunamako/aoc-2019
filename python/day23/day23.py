from aocd.models import Puzzle
import cProfile
from collections import defaultdict, namedtuple, Counter, deque
from itertools import permutations, combinations, chain, cycle
import re
import math

from advent_machine import AdventMachine, Paintbot

global nat_pack

nat_pack = None

def parse_packets(packets, output):
    global nat_pack

    for i in range(0, len(output), 3):
        dest, x, y = output[i:i+3]
        if dest == 255:
            nat_pack = (x,y)
            continue

        packets[dest].append((x,y))

def is_idle(machines, packets):
    return all(m.output == [] for m in machines) and \
           all(p == [] for p in packets)

def simulate_network(program, use_nat=False):
    global nat_pack
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
                while packets[i]:
                    p = packets[i].pop(0)
                    m.execute(p[0])
                    m.execute(p[1])
                    parse_packets(packets, m.output)

        if not use_nat and nat_pack:
            return nat_pack[1]
        elif is_idle(machines, packets) and nat_pack:
            if nat_pack[1] == last_sent_nat_value and last_sent_nat_value:
                return nat_pack[1]
                
            machines[0].execute(nat_pack[0])
            machines[0].execute(nat_pack[1])
            last_sent_nat_value = nat_pack[1]
            nat_pack = None

def part_one(_input):
    return simulate_network(_input, use_nat=False)

def part_two(_input):
    return simulate_network(_input, use_nat=True)


if __name__ == '__main__':
    puzzle = Puzzle(year=2019, day=23)
    _input = list(map(int, puzzle.input_data.split(',')))
    #_input = open('bigboy').readlines()

    print(part_one(_input))
    print(part_two(_input))

    #cProfile.run('print(part_one(_input))')
    #cProfile.run('print(part_two(_input))')
