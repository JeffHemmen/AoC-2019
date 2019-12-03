#!/usr/bin/env python3

from sys import argv
import operator

def intcode(code: list):
    offset = 0
    op_list = (operator.add, operator.mul)
    while(code[offset] != 99):
        op_i, p1, p2, res = code[offset : offset + 4]
        op = op_list[op_i - 1]
        code[res] = op(code[p1], code[p2])
        offset += 4

def n_v_perm(fn, noun, verb):
    with open(fn, 'r') as f:
        code = [int(x) for x in f.read().split(',')]
    # before running the program, replace position 1 with the value 12 and replace position 2 with the value 2.
    code[1] = noun
    code[2] = verb
    # Run the programme
    intcode(code)
    # What value is left at position 0 after the program halts?
    return code[0]

def main(fn):
    for noun in range(0, 100):
        for verb in range(0, 100):
            if n_v_perm(fn, noun, verb) ==  19690720:
                print(f'noun = {noun}\nverb = {verb}\n100 * noun + verb = {100 * noun + verb}')

if __name__ == '__main__':
    fn = argv[1] if len(argv) >= 2 else 'input.txt'
    main(fn)