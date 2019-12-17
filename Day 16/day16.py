#!/usr/bin/env python3

import sys
from functools import reduce
from operator import add

signal_length = None

def get_pattern_generator(index): # generator
    base_pattern = [0, 1, 0, -1]
    yield from [0] * (index - 1)
    while(True):
        yield from [1] * index
        yield from [0] * index
        yield from [-1] * index
        yield from [0] * index


def get_pattern(index):
    base_pattern = [0, 1, 0, -1]
    new_pattern = [0] * (index - 1)
    new_length = len(new_pattern)
    while new_length < signal_length:
        new_pattern.extend([1] * index)
        new_length = len(new_pattern)
        if new_length >= signal_length:
            break
        new_pattern.extend([0] * index)
        new_length = len(new_pattern)
        if new_length >= signal_length:
            break
        new_pattern.extend([-1] * index)
        new_length = len(new_pattern)
        if new_length >= signal_length:
            break
        new_pattern.extend([0] * index)
        new_length = len(new_pattern)
    return new_pattern



def apply_phase(signal):
    new_signal = []
    for index in range(signal_length):
        # if index % 100 == 0: print(f'  index {index} of {signal_length}')
        pattern = get_pattern(index + 1)
        control_digit = reduce(add, (sig_digit * pattern_digit for (sig_digit, pattern_digit) in zip(signal, pattern)))
        control_digit = abs(control_digit) % 10
        new_signal.append(control_digit)
    return new_signal





def main(fn, num_phases=100):
    global signal_length
    with open(fn, 'r') as f:
        signal = [int(c) for c in f.read()]

    signal = signal
    signal_length = len(signal)

    print("Phases: ", end='')
    for _ in range(num_phases):
        print(f'{_+1}, ', end='')
        sys.stdout.flush()
        signal = apply_phase(signal)
    print("done.\n")
    return signal


if __name__ == '__main__':
    fn = sys.argv[1] if len(sys.argv) >= 2 else 'input.txt'

    import cProfile
    # cProfile.run('main(fn)')

    res = main(fn)
    print("".join(str(d) for d in res[:8]))
    print() # fflush(stdout)

    # Phase 2
    print("Please see `day16.c` for Part 2.")