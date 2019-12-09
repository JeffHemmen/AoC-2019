#!/usr/bin/env python3

from sys import argv, exit
import operator
from math import ceil, log, pow

sys_id = 0


def arithmetic_op(op):
    def ret_func(params, param_modes, code):
        effective_params = []
        for m, p in zip(param_modes, params):
            if m == 1 : effective_params.append(p)
            else      : effective_params.append(code[p])
        res = op(*effective_params[0:2])
        code[params[2]] = res
    return ret_func


def read_input(params, param_modes, code):
    # can ignore param_modes, only one param here and it's in `position mode`
    code[params[0]] = sys_id


def print_output(params, param_modes, code):
    if param_modes[0] == 0 : print(code[params[0]])
    else                   : print(params[0])


def terminate(*args, **kvargs):
    exit(0)


operations = {
     1 : (arithmetic_op(operator.add), 3),
     2 : (arithmetic_op(operator.mul), 3),
     3: (read_input, 1),
     4 : (print_output, 1),
    99 : (terminate, 0)
}


def get_param_modes(inst, length):
    modes = [0] * length
    for i in range(2, ceil(log(inst, 10))):
        modes[i - 2] = inst // int(pow(10, i)) % 10
    return modes


def main(fn, _sys_id):
    global sys_id
    sys_id = _sys_id
    with open(fn, 'r') as f:
        code = [int(x) for x in f.read().split(',')]
    ptr = 0
    while True:
        inst = code[ptr]
        # print('Instruction:', inst)
        opcode = inst % 100
        num_params = operations[opcode][1]
        param_modes = get_param_modes(inst, num_params)
        # params = []
        # for _ in range(0, operations[opcode][1]):
        #     params.append(next(code_iter))
        params = code[ptr + 1 : ptr + 1 + num_params]
        ptr += num_params
        operations[opcode][0](params=params, param_modes=param_modes, code=code)
        ptr += 1


if __name__ == '__main__':
    fn = argv[1] if len(argv) >= 2 else 'input.txt'
    ret = main(fn, 1)


# 123450
#      0e0
#     5e1
#    4e2
#   3e3
#  2e4
# 1e5
#
# 0e6
#
# # OPCODES:
# 01 ADD 3
# 02 MUL 3
# 03 INP 1
# 04 OUT 1
# 99 HLT
