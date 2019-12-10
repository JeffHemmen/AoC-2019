#!/usr/bin/env python3

from sys import argv, exit
import operator
from math import ceil, log, pow

sys_id = 0
relative_base = 0

def arithmetic_op(op):
    global relative_base
    def ret_func(params, param_modes, code):
        global relative_base
        effective_params = []
        for m, p in zip(param_modes[0:2], params[0:2]):
            if m == 0   : effective_params.append(code[p])
            elif m == 1 : effective_params.append(p)
            elif m == 2 : effective_params.append(code[relative_base + p])

        for m, p in zip(param_modes[2:3], params[2:3]):
            if m == 0   : effective_params.append(p)
            elif m == 1 : pass
            elif m == 2 : effective_params.append(relative_base + p)

        res = op(*effective_params[0:2])
        code[effective_params[2]] = int(res)
    return ret_func


def read_input(params, param_modes, code):
    global sys_id, relative_base

    # print(f'params={params}, param_modes={param_modes}, relative_base={relative_base}')

    if   param_modes[0] == 0 : effective_param = params[0]
    elif param_modes[0] == 1 : pass
    elif param_modes[0] == 2 : effective_param = relative_base + params[0]

    # print(f'effective_param={effective_param}, code[effective_param]={code[effective_param]}')

    code[effective_param] = sys_id
    # print(f'effective_param={effective_param}, code[effective_param]={code[effective_param]}')



def print_output(params, param_modes, code):
    global relative_base
    # print(f'print_output called with params: {params}\n    and param_modes: {param_modes}\n')
    if   param_modes[0] == 0 : print(code[params[0]])
    elif param_modes[0] == 1 : print(params[0])
    elif param_modes[0] == 2 : print(code[relative_base + params[0]])

def conditional_jump(bool):
    global relative_base
    def ret_func(params, param_modes, code):
        global relative_base
        nonlocal bool
        effective_params = []
        for m, p in zip(param_modes, params):
            if m == 0   : effective_params.append(code[p])
            elif m == 1 : effective_params.append(p)
            elif m == 2 : effective_params.append(code[relative_base + p])
        # print()
        # print(f'params={params}, param_modes={param_modes}')
        # print(f'conditional_jump({bool}) with effective_params[0]={effective_params[0]}; returning: ', end='')
        if (effective_params[0] != 0) == bool:
            print(effective_params[1])
            return effective_params[1]
        # print("None")
        return None
    return ret_func

def increase_relative_base(params, param_modes, code):
    global relative_base
    # print(f'relative_base before: {relative_base}')
    # print(f'REL :: params={params}, param_modes={param_modes}', end=', ')
    if   param_modes[0] == 0 : effective_param = code[params[0]]
    elif param_modes[0] == 1 : effective_param = params[0]
    elif param_modes[0] == 2 : effective_param = code[relative_base + params[0]]
    # print(f'effective_param={effective_param}')
    relative_base += effective_param
    # print(f'relative_base after: {relative_base}')


def terminate(*args, **kvargs):
    exit(0)


operations = {
    1 : (arithmetic_op(operator.add), 3),
    2 : (arithmetic_op(operator.mul), 3),
    3 : (read_input, 1),
    4 : (print_output, 1),
    5 : (conditional_jump(True), 2),
    6 : (conditional_jump(False), 2),
    7 : (arithmetic_op(operator.lt), 3),
    8 : (arithmetic_op(operator.eq), 3),
    9 : (increase_relative_base, 1),
   99 : (terminate, 0)
}


def get_param_modes(inst, length):
    modes = [0] * length
    for i in range(2, ceil(log(inst, 10))):
        modes[i - 2] = inst // int(pow(10, i)) % 10
    # print(modes)
    return modes


def main(fn, _sys_id):
    global sys_id
    sys_id = _sys_id
    with open(fn, 'r') as f:
        code = [int(x) for x in f.read().split(',')]
    code += [0] * 2048
    ptr = 0
    while True:
        inst = code[ptr]
        # print('Instruction:', inst)
        opcode = inst % 100
        # if opcode == 3: print(f'XXX {inst}')
        num_params = operations[opcode][1]
        param_modes = get_param_modes(inst, num_params)
        # params = []
        # for _ in range(0, operations[opcode][1]):
        #     params.append(next(code_iter))
        params = code[ptr + 1 : ptr + 1 + num_params]
        ptr += num_params
        new_ptr = operations[opcode][0](params=params, param_modes=param_modes, code=code)
        # print(f'new_ptr = {new_ptr}')
        ptr = new_ptr if new_ptr is not None else ptr + 1


if __name__ == '__main__':
    fn = argv[1] if len(argv) >= 2 else 'input.txt'
    ret = main(fn, 1)

