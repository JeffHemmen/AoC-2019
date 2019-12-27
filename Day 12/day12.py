#!/usr/bin/env python3

from sys import argv
from collections import namedtuple

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

def main(positions):
    velocities = []
    for _ in positions:
        velocities.append(Coordinates(x=0, y=0, z=0))

    for _ in range(1000):
        apply_gravity(positions, velocities)
        apply_velocity(positions, velocities)
    return total_energy(positions, velocities)


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

    res = main(positions)
    print(f'Part 1: {res}')

