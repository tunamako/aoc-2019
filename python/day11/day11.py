from aocd.models import Puzzle
from collections import namedtuple
import matplotlib.pyplot as plt

from advent_machine import AdventMachine, Paintbot


def part_one(_input):
    bot = Paintbot(_input)
    bot.run_program(0)
    return len(bot.grid)

def part_two(_input):
    bot = Paintbot(_input)
    bot.run_program(1)

    x, y = zip(*[p for p in bot.grid if bot.grid[p] == 1])
    plt.scatter(x,y)
    plt.show()


if __name__ == '__main__':
    puzzle = Puzzle(year=2019, day=11)
    _input = list(map(int, puzzle.input_data.split(',')))

    print(part_one(_input))
    print(part_two(_input))
