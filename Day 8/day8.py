#!/usr/bin/env python3

from sys import argv
from operator import mul
from itertools import chain

def read_layers(dimensions, code):
    assert len(code) % mul(*dimensions) == 0
    # num_layers = len(code) // mul(*dimensions)
    it_code = iter(code)
    layers = []
    try:
        while True:
            this_layer = []
            for row in range(dimensions[1]):
                this_row = []
                for col in range(dimensions[0]):
                    this_row.append(next(it_code))
                this_layer.append(this_row)
            layers.append(this_layer)
    except StopIteration:
            return layers

def process_layers(dimensions, layers, num_layers=100):
    layer = []
    for row in range(dimensions[1]):
        this_row = []
        layer.append(this_row)
        for col in range(dimensions[0]):
            # setting layer[row][col]
            for i in range(num_layers):
                if layers[i][row][col] == 2:
                    continue
                this_row.append(layers[i][row][col])
                break
    return layer



if __name__ == '__main__':
    fn = argv[1] if len(argv) >= 2 else 'input.txt'
    with open(fn, 'r') as f:
        code = [int(c) for c in f.read()]
    dimensions = (25, 6)
    layers = read_layers(dimensions, code)
    lowest_zero_count = None
    for index, layer in enumerate(layers):
        zero_count = len([x for x in chain(*layer) if x == 0])
        if lowest_zero_count is None or zero_count < lowest_zero_count:
            lowest_zero_count = zero_count
            wanted_layer_idx = index
    wanted_layer = layers[wanted_layer_idx]

    num_1s = len([x for x in chain(*wanted_layer) if x == 1])
    num_2s = len([x for x in chain(*wanted_layer) if x == 2])
    print(f'Part 1: {num_1s * num_2s}')

    processed_layer = process_layers(dimensions, layers)
    print('Part 2:')
    for row in processed_layer:
        for pixel in row:
            if pixel == 0:
                print('◼️', end='')
            else:
                print('◻️', end='')
        print()

