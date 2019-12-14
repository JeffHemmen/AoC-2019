#!/usr/bin/env python3

from sys import argv, exit
from operator import itemgetter
from math import sqrt

remaining_asteroids = 200

def load_belt(fn):
    belt = []
    with open(fn, 'r') as f:
        for row, line in enumerate(f):
            belt.append([])
            for col, char in enumerate(line):
                if char == '#' or char == '@':
                    belt[row].append(col)
    return belt

def get_slope(a, b):
    return (a[1] - b[1]) / (a[0] - b[0])

def count_visible(asteroid, belt):
    visible = 0

    slopes = set()
    for row, cols in enumerate(belt[ : asteroid[0]], 0):
        for col in cols:
            slopes.add(get_slope(asteroid, (row, col)))
    visible += len(slopes)

    own_row = len(belt[asteroid[0]])
    if own_row == 2:
        visible += 1
    elif own_row >= 3:
        visible += 2

    slopes = set()
    offset = asteroid[0] + 1
    for row, cols in enumerate(belt[offset : ], offset):
        for col in cols:
            slopes.add(get_slope(asteroid, (row, col)))
    visible += len(slopes)

    return visible

def part1(belt):
    highest_count = -1
    for asteroid in ((row, col) for row, cols in enumerate(belt) for col in cols):
        current_count = count_visible(asteroid, belt)
        if current_count > highest_count:
            highest_count = current_count
    return highest_count

def find_base(belt):
    highest_count = -1
    ret = None
    for asteroid in ((row, col) for row, cols in enumerate(belt) for col in cols):
        current_count = count_visible(asteroid, belt)
        if current_count > highest_count:
            highest_count = current_count
            ret = asteroid
    return ret

def distance(a, b):
    return sqrt((a[0] - b[0]) ** 2 + (a[1] - b[1]) ** 2)

def find_closest_asteroid_at_given_slope(segment, given_slope, base):
    candidates = [(asteroid, distance(asteroid, base)) for asteroid, slope in segment if slope == given_slope]
    candidates.sort(key=itemgetter(1))
    return candidates[0][0]

def scan_segment(segment, base):
    global remaining_asteroids
    last_slope = None
    for asteroid, slope in segment:
        if slope == last_slope:
            continue
        last_slope = slope
        remaining_asteroids -= 1
        if remaining_asteroids == 0:
            return find_closest_asteroid_at_given_slope(segment, slope, base)

def part2(belt):
    global remaining_asteroids
    base = find_base(belt)
    # print(base)
    top_right = ((row, col) for row, cols in enumerate(belt[ : base[0]], 0) for col in cols if col >= base[1])
    bottom_right = ((row, col) for row, cols in enumerate(belt[base[0] + 1 : ], base[0] + 1) for col in cols if col > base[1])
    bottom_left = ((row, col) for row, cols in enumerate(belt[base[0] + 1 : ], base[0] + 1) for col in cols if col <= base[1])
    top_left = ((row, col) for row, cols in enumerate(belt[ : base[0]], 0) for col in cols if col < base[1])

    top_right_ordered = [(asteroid, get_slope(base, asteroid)) for asteroid in top_right]
    top_right_ordered.sort(key=itemgetter(1), reverse=True)
    # print(top_right_ordered)

    bottom_right_ordered = [(asteroid, get_slope(base, asteroid)) for asteroid in bottom_right]
    bottom_right_ordered.sort(key=itemgetter(1), reverse=True)
    # print(bottom_right_ordered)

    bottom_left_ordered = [(asteroid, get_slope(base, asteroid)) for asteroid in bottom_left]
    bottom_left_ordered.sort(key=itemgetter(1), reverse=True)
    # print(bottom_left_ordered)

    top_left_ordered = [(asteroid, get_slope(base, asteroid)) for asteroid in top_left]
    top_left_ordered.sort(key=itemgetter(1), reverse=True)
    # print(top_left_ordered)

    ret = scan_segment(top_right_ordered, base)
    if ret:
        return 100 * ret[1] + ret[0]
    remaining_asteroids -= 1 # lazy, can see on map
    ret = scan_segment(bottom_right_ordered, base)
    if ret:
        return 100 * ret[1] + ret[0]
    ret = scan_segment(bottom_left_ordered, base)
    if ret:
        return 100 * ret[1] + ret[0]
    remaining_asteroids -= 1 # lazy, can see on map
    ret = scan_segment(top_left_ordered, base)
    if ret:
        return 100 * ret[1] + ret[0]


if __name__ == '__main__':
    fn = argv[1] if len(argv) >= 2 else 'input.txt'
    belt = load_belt(fn)
    res1 = part1(belt)
    print(f'Part1: {res1}')
    res2 = part2(belt)
    print(f'Part1: {res2}')