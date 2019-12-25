#!/usr/bin/env python3

from sys import argv
from intcode import Intcode

# Constants
BLACK, WHITE = 0, 1
UP, RIGHT, DOWN, LEFT = (1, 0), (0, 1), (-1, 0), (0, -1)
DEBUG = False


def debug(msg):
    if DEBUG:
        print(msg)

def tuple_add(a, b):
    return (a[0] + b[0], a[1] + b[1])


def hull_painting_robot(code, starting_colour=BLACK):
    # co-ordinates are COL, ROW (or x, y)

    panels_painted = set()
    current_panel = (0, 0)
    panel_colours = {current_panel: starting_colour}
    direction_index = 0  # UP
    directions = (UP, RIGHT, DOWN, LEFT)

    ic = Intcode(code)

    try:
        while True:
            current_colour = panel_colours.get(current_panel, BLACK)
            debug(f'Panel {current_panel}, colour={current_colour}')
            paint_colour, direction_change = ic.send([current_colour])
            debug(f'  paint_colour={paint_colour}, direction_change={direction_change}')

            panel_colours[current_panel] = paint_colour
            panels_painted.add(current_panel)

            direction_change = -1 if direction_change == 0 else 1
            direction_index = (direction_index + direction_change) % 4

            current_panel = tuple_add(current_panel, directions[direction_index])

    except StopIteration:
        pass
    return len(panels_painted), panel_colours


def part2(code):
    _, panel_colours = hull_painting_robot(code, WHITE)
    x_span, y_span = [0, 0], [0, 0]
    for panel in panel_colours.keys():
        if panel[0] < x_span[0]:
            x_span[0] = panel[0]
        if panel[0] > x_span[1]:
            x_span[1] = panel[0]
        if panel[1] < y_span[0]:
            y_span[0] = panel[1]
        if panel[1] > y_span[1]:
            y_span[1] = panel[1]
    x_span = [x_span[1], x_span[0] - 1, -1]  # reverse so we paint high-x first, set step to -1
    y_span[1] += 1                           # and add 1 to draw entire range
    debug(f'x_span: {x_span}; y_span: {y_span}')
    for x in range(*x_span):
        for y in range(*y_span):
            colour = panel_colours.get((x, y), BLACK)
            c = '#' if colour == WHITE else ' '
            print(c, end='')
        print()




if __name__ == '__main__':
    fn = argv[1] if len(argv) >= 2 else 'input.txt'
    with open(fn, 'r') as f:
        code = [int(x) for x in f.read().split(',')]
    code.extend([0] * 1024)

    part1_res = hull_painting_robot(code.copy())
    print(f'Part 1: {part1_res[0]}')

    print(f'Part 2:')
    part2(code.copy())
