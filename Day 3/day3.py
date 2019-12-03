#!/usr/bin/env python3

from sys import argv
from collections import defaultdict
from operator import add


def populate_path(wire, line):
    move = {'U' : (0, 1), 'R': (1, 0), 'D': (0, -1), 'L': (-1, 0)}
    for instruction in line.split(','):
        dir, dist = instruction[0], int(instruction[1:])
        for _ in range(dist):
            _pos = wire[-1]
            _new = (_pos[0] + move[dir][0], _pos[1] + move[dir][1])
            wire.append(_new)



def manhattan(a: tuple) -> int:
    return abs(a[0]) + abs(a[1])


def part1(fn):
    with open(fn, 'r') as f:
        line1 = f.readline()
        line2 = f.readline()
    wire1, wire2 = [(0, 0)], [(0, 0)]

    populate_path(wire1, line1)
    populate_path(wire2, line2)

    intersections = set(wire1).intersection(set(wire2))

    res = manhattan(intersections.pop())
    for md in (manhattan(i) for i in intersections):
        if md == 0: continue
        if md < res:
            res = md

    return res


def part2(fn):
    with open(fn, 'r') as f:
        line1 = f.readline()
        line2 = f.readline()
    wire1, wire2 = [(0, 0)], [(0, 0)]

    populate_path(wire1, line1)
    populate_path(wire2, line2)

    intersections = set(wire1).intersection(set(wire2))

    steps_required = defaultdict(lambda: [None, None])

    for dist, pos in enumerate(wire1):
        if not pos in intersections: continue
        if steps_required[pos][0] == None:
            steps_required[pos][0] = dist

    for dist, pos in enumerate(wire2):
        if not pos in intersections: continue
        if steps_required[pos][1] == None:
            steps_required[pos][1] = dist

    min_sum = None
    for steps_combined in (add(*s) for s in steps_required.values()):
        if steps_combined == 0: continue
        if min_sum == None:
            min_sum = steps_combined
            continue
        if steps_combined < min_sum:
            min_sum = steps_combined
    return min_sum


if __name__ == '__main__':
    fn = argv[1] if len(argv) >= 2 else 'input.txt'

    # res = part1(fn)
    # print('Part 1:', res)

    res = part2(fn)
    print('Part 2:', res)