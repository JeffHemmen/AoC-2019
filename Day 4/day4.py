#!/usr/bin/env python3

from sys import argv

def two_adjacent_digits_are_the_same(n):
    cs = str(n)
    left = None
    for c in cs:
        if c == left:
            return True
        left = c
    return False

def two_adjacent_digits_are_the_same_v2(n):
    cs = str(n)
    left, num_repeat = '', 1
    for c in cs:
        if c == left:
            num_repeat += 1
            # left = c
        else: # c != left
            if num_repeat == 2: return True
            else:
                num_repeat = 1
                left = c
    if num_repeat == 2: return True
    return False

def going_from_left_to_right_the_digits_never_decrease(n):
    cs = str(n)
    left = '0'
    for c in cs:
        if c < left:
            return False
        left = c
    return True


def main(lower, upper):
    c = 0
    for i in range(lower, upper+1):
        if not two_adjacent_digits_are_the_same_v2(i):
            continue
        if not going_from_left_to_right_the_digits_never_decrease(i):
            continue
        c += 1
    return c



if __name__ == '__main__':
    lower = argv[1] if len(argv) >= 3 else 382345
    upper = argv[2] if len(argv) >= 3 else 843167
    res = main(lower, upper)
    print(res)
