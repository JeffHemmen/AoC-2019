#!/usr/bin/env python3

from sys import argv

def part1(fn) -> int:
    with open(fn, 'r') as f:
        lines =  f.read().split('\n')
    total_orbits = 0
    known_orbits = {'COM': 0}
    queue = []

    for orbitee, satellite in (pair.split(')') for pair in lines):
        if orbitee in known_orbits.keys():
            known_orbits[satellite] = known_orbits[orbitee] + 1
            total_orbits += known_orbits[satellite]
            continue
        queue.append((orbitee, satellite))

    for orbitee, satellite in queue:
        if orbitee in known_orbits.keys():
            known_orbits[satellite] = known_orbits[orbitee] + 1
            total_orbits += known_orbits[satellite]
            continue
        queue.append((orbitee, satellite))

    return total_orbits

def part2(fn):
    with open(fn, 'r') as f:
        lines =  f.read().split('\n')
    queue = []
    for orbitee, satellite in (pair.split(')') for pair in lines):
        queue.append((orbitee, satellite))
    YOU_path = ['YOU']
    SAN_path = ['SAN']
    for orbitee, satellite in queue:
        # print(orbitee, satellite)
        processed = False
        if satellite in YOU_path:
            YOU_path.append(orbitee)
            processed = True
        if satellite in SAN_path:
            SAN_path.append(orbitee)
            processed = True
        common_node_set = set(YOU_path).intersection(set(SAN_path))
        if common_node_set != set():
            break
        if not processed:
            queue.append((orbitee, satellite))
    else:
        print("Something went wrong.")
    # print(YOU_path)
    # print(SAN_path)
    common_node = common_node_set.pop()
    path_length = -2 + YOU_path.index(common_node) + SAN_path.index(common_node)
    return path_length


if __name__ == '__main__':
    fn = argv[1] if len(argv) >= 2 else 'input.txt'
    res1 = part1(fn)
    print(res1)
    res2 = part2(fn)
    print(res2)
