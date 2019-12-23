from aocd.models import Puzzle
import cProfile
from collections import defaultdict, namedtuple, Counter, deque
from itertools import permutations, combinations, chain
import re
import math
import numpy as np
import resource, sys
import time
from advent_machine import AdventMachine, Paintbot
sys.setrecursionlimit(2000)
resource.setrlimit(resource.RLIMIT_STACK, (2**29,-1))
moves = [
    (1, 0),
    (-1, 0),
    (0, 1),
    (0, -1),
]

class Portal(object):

    def __init__(self, name, locations):
        self.name = name
        self.inner = locations["in"]
        self.outer = locations["out"]
        self.neighbors = []

    def add_neighbor(self, neighbor_portal, distance, orientation):
        #print(self.name, neighbor_portal.name, distance, orientation)
        #print(self.inner, self.outer)
        self.neighbors.append((neighbor_portal, distance, orientation))

    def shortest_path(self, target, cur_path=None):
        if cur_path is None:
            cur_path = set()
        if self.name == target:
            return 0

        best_len = None

        for portal, dist, _ in self.neighbors:
            if portal.name in cur_path:
                continue

            next_len = dist
            if self.name != "AA":
                next_len += 1

            next_len += portal.shortest_path(target, cur_path | {self.name})

            if best_len is None or next_len < best_len:
                best_len = next_len

        return best_len if best_len else np.inf

    def shortest_path_with_layers(self, target, cur_path=None, cur_layer=0):
        if cur_path is None:
            cur_path = set()
        if self.name == target and cur_layer == 0:
            return 0
        elif cur_layer > 10:
            return np.inf
        elif str((self.name, cur_layer)) in cur_path:
            return np.inf

        #print(cur_path)
        best_len = None
        for portal, distance, orientation in self.neighbors:
            mod = 0
            if portal.name in ["AA", "ZZ"] and cur_layer > 0:
                continue
            elif cur_layer == 0 and "out" in orientation:
                continue
            elif orientation == "in":
                mod += 1
            elif orientation == "out":
                mod -= 1

            #print(self.name, portal.name, cur_layer, mod, orientation)

            next_len = distance
            if self.name != "AA":
                next_len += 1

            next_len += portal.shortest_path_with_layers(target, cur_path | {str((self.name, cur_layer))}, cur_layer + mod)

            if best_len is None or next_len < best_len:
                best_len = next_len

        return best_len if best_len else np.inf

def parse_portals(grid):
    portals = defaultdict(lambda: {"out":None, "in":None})

    for x, y in np.ndindex((grid.shape[0]-1, grid.shape[1]-1)):
        if grid[x,y].isupper():

            if x < len(grid) and grid[x+1,y].isupper():
                key = grid[x,y] + grid[x+1,y]
                try:
                    val = (x-3, y-2) if grid[x-1,y] == '.' else (x, y-2) 
                except:
                    continue

                if x == 0 or x + 2 == len(grid):
                    portals[key]["out"] = val
                else:
                    portals[key]["in"] = val

            elif y < len(grid[0]) and grid[x,y+1].isupper():
                key = grid[x,y] + grid[x,y+1]
                try:
                    val = (x-2, y-3) if grid[x,y-1] == '.' else (x-2, y) 
                except:
                    continue
                if y == 0 or y + 2 == len(grid[0]):
                    portals[key]["out"] = val
                else:
                    portals[key]["in"] = val

    return portals


def get_edge_orientation(port_A, port_B, pos_A, pos_B):
    A_is_outer = pos_A == port_A.outer
    B_is_outer = pos_B == port_B.outer

    if A_is_outer and B_is_outer:
        return "neutral_out"
    elif not A_is_outer and not B_is_outer:
        return "neutral_in"
    elif A_is_outer and not B_is_outer:
        return "in"
    elif not A_is_outer and B_is_outer:
        return "out"

def construct_graph(grid, portals):
    portals_by_coord = dict()

    for p in portals.values():
        portals_by_coord[p.outer] = p

        if p.name not in ["AA", "ZZ"]:
            portals_by_coord[p.inner] = p

    for start_loc, start_portal in sorted(portals_by_coord.items(), key=lambda p: p[1].name):
        que = deque([start_loc, None])
        depth = 0
        seen_positions = set()

        while que:
            pos = que.popleft()
            seen_positions.add(pos)

            if pos is None:
                depth += 1
                que.append(None)
                if que[0] is None:
                    break
            elif pos in portals_by_coord and pos != start_loc:
                found_portal = portals_by_coord[pos]
                orient = get_edge_orientation(start_portal, found_portal, start_loc, pos)
                start_portal.add_neighbor(found_portal, depth, orient)
            else:
                for m in moves:
                    next_move = (pos[0] + m[0], pos[1] + m[1])
                    if next_move[0] < 0 or next_move[1] < 0:
                        continue
                    try:
                        value = grid[next_move[0]][next_move[1]]
                    except:
                        continue

                    if next_move in seen_positions:
                        continue
                    elif value == '.':
                        que.append(next_move)

def part_one(_input):
    grid = np.swapaxes(np.array(_input), 0, 1)
    portals = {name: Portal(name, locs) for name, locs in parse_portals(grid).items()}
    grid = grid[2:-2, 2:-2]

    construct_graph(grid, portals)
    return portals["AA"].shortest_path("ZZ")

def part_two(_input):
    grid = np.swapaxes(np.array(_input), 0, 1)
    portals = {name: Portal(name, locs) for name, locs in parse_portals(grid).items()}
    grid = grid[2:-2, 2:-2]

    construct_graph(grid, portals)
    #return portals["AA"].shortest_path_with_layers("ZZ")

    que = deque([(portals["AA"], 0, 0)])

    while que:
        #print(que)
        #etime.sleep(0.1)
        portal, distance, cur_layer = que.popleft()

        if portal.name == "ZZ" and cur_layer == 0:
            return distance
        elif cur_layer > 10:
            continue
        else:
            for adj_portal, adj_dist, adj_orient in portal.neighbors:
                layer_mod = 0
                if cur_layer == 0 and "out" in adj_orient:
                    continue
                elif adj_orient == "in":
                    layer_mod = 1
                elif adj_orient == "out":
                    layer_mod = -1
                #print(portal.name, adj_portal.name, cur_layer, layer_mod, adj_orient)
                next_dist = adj_dist + distance
                if portal.name != "AA":
                    next_dist += 1

                que.append((adj_portal, next_dist, cur_layer + layer_mod))


if __name__ == '__main__':
    #puzzle = Puzzle(year=2019, day=20)
    _input = [list(line[:-1]) for line in open("input").readlines()]

    #_input = open('bigboy').readlines()

    #print(part_one(_input))
    print(part_two(_input))

    #cProfile.run('print(part_one(_input))')
    #cProfile.run('print(part_two(_input))')
