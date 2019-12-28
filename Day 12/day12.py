#!/usr/bin/env python3

from sys import argv
from collections import namedtuple
from itertools import chain

Coordinates = namedtuple('Coordinates', ['x', 'y', 'z'])
Coordinates.__add__ = lambda self, other: self.__class__(*(a+b for a,b in zip(self, other)))
Coordinates.__sub__ = lambda self, other: self.__class__(*(a-b for a,b in zip(self, other)))
Coordinates.energy  = lambda self: abs(self.x) + abs(self.y) + abs(self.z)


def apply_gravity(positions, velocities):
    num_planets = len(positions)
    calc_delta = lambda a, b: 0 if a == b else (1 if b > a else -1)
    for p1_idx in range(num_planets):
        for p2_idx in range(p1_idx + 1, num_planets):
            deltas = [calc_delta(c1, c2) for c1, c2 in zip(positions[p1_idx], positions[p2_idx])]
            velocities[p1_idx] += deltas
            velocities[p2_idx] -= deltas


def apply_velocity(positions, velocities):
    for index in range(len(positions)):
        positions[index] += velocities[index]


def total_energy(positions, velocities):
    running_sum = 0
    for pos, vel in zip(positions, velocities):
        running_sum += pos.energy() * vel.energy()
    return running_sum


def part1(positions):
    velocities = []
    for _ in positions:
        velocities.append(Coordinates(x=0, y=0, z=0))

    for _ in range(1000):
        apply_gravity(positions, velocities)
        apply_velocity(positions, velocities)
    return total_energy(positions, velocities)


def fingerprint(*x, axis):
    return [getattr(coordinate, axis) for coordinate in chain(*x)]


def prime_numbers():
    yield 2
    yield 3
    factors = [2, 3]
    n = 3
    while True:
        n += 2
        if any((n % d == 0 for d in factors)):
            continue
        yield n
        factors.append(n)


def get_prime_factors(n):
    prime_factor_count = dict()
    primes = prime_numbers()
    f = next(primes)
    while True:
        if n % f != 0:
            f = next(primes)
            continue
        prime_factor_count[f] = prime_factor_count.get(f, 0) + 1
        n = n // f
        if n == 1:
            break
    return prime_factor_count


def part2(positions):
    velocities = []
    for _ in positions:
        velocities.append(Coordinates(x=0, y=0, z=0))

    starting_fingerprints = [fingerprint(positions, velocities, axis=axis) for axis in ['x', 'y', 'z']]
    completed_cycles = [False, False, False]
    cycle_periods = []

    num_steps = 0
    while completed_cycles != [True, True, True]:
        num_steps += 1
        apply_gravity(positions, velocities)
        apply_velocity(positions, velocities)
        axes = ['x', 'y', 'z']
        fingerprints = [fingerprint(positions, velocities, axis=axis) for axis in axes]
        for axis in range(3):
            if fingerprints[axis] == starting_fingerprints[axis]:
                # print(f'Axis {axes[axis]} cycle complete after {num_steps} steps.')
                cycle_periods.append(num_steps)
                completed_cycles[axis] = True

    prime_factor_dicts = [get_prime_factors(cycle) for cycle in cycle_periods]
    final_factors = prime_factor_dicts[0]
    for prime_factor_dict in prime_factor_dicts[1:]:
        for factor, count in prime_factor_dict.items():
            if count > final_factors.get(factor, 0):
                final_factors[factor] = count

    overall_period = 1
    for factor, count in final_factors.items():
        overall_period *= factor ** count

    return overall_period


if __name__ == '__main__':
    fn = argv[1] if len(argv) >= 2 else 'input.txt'
    positions = []
    with open(fn, 'r') as f:
        line = f.readline()
        while line:
            sanitised_line = line.strip('<>\n')
            exec(
                 f'positions.append(Coordinates({sanitised_line}))'
            )
            line = f.readline()

    res = part1(positions.copy())
    print(f'Part 1: {res}')

    res = part2(positions.copy())
    print(f'Part 2: {res}')

