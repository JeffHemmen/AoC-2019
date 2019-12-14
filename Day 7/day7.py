#!/usr/bin/env python3

from sys import path, argv
path.insert(1, "../Day 5")
import day5
from itertools import permutations

# Monkey-patch input function
input_stack = list()
def read_input(params, param_modes, code):
    global input_stack
    code[params[0]] = input_stack.pop()
day5.operations[3] = (read_input, 1)
# Monkey-patch output function
output_stack = list()
def print_output(params, param_modes, code):
    if param_modes[0] == 0 : output_stack.append(code[params[0]])
    else                   : output_stack.append(params[0])
day5.operations[4] = (print_output, 1)


fn = "" # global
def amplifier(phase, input):
    global fn
    assert input_stack == [] # is empty
    input_stack.append(input)
    input_stack.append(phase)
    try:
        day5.main(fn, None)
    except SystemExit:
        pass
    assert len(output_stack) == 1
    return output_stack.pop()



if __name__ == '__main__':
    fn = argv[1] if len(argv) >= 2 else 'input.txt'
    combinations = permutations(range(0, 5))
    highest_signal = 0

    for phases in combinations:
        out = amplifier(phases[0], 0)
        out = amplifier(phases[1], out)
        out = amplifier(phases[2], out)
        out = amplifier(phases[3], out)
        out = amplifier(phases[4], out)
        if out > highest_signal:
            highest_signal = out
    print(highest_signal)

