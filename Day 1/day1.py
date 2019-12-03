#!/usr/bin/env python3

from sys import argv
from functools import reduce
from operator import add

def fuelreq(mod: int) -> int:
    return mod // 3 - 2

def fuel_for_fuel(f):
    if fuelreq(f) <= 0:
        return 0
    additional_fuel = fuelreq(f)
    return additional_fuel + fuel_for_fuel(additional_fuel)

def main(fn):
    with open(fn, 'r') as f:
        mod_list = [int(x) for x in f.read().split()]
    fuel_req_mod = reduce(add, [fuelreq(x) + fuel_for_fuel(fuelreq(x)) for x in mod_list])
    # all_fuel = fuel_req_mod + fuel_for_fuel(fuel_req_mod)
    print(fuel_req_mod)


if __name__ == '__main__':
    input_file = argv[1] if len(argv) >= 2 else 'input.txt'
    main(input_file)