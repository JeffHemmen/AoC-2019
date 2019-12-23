#!/usr/bin/env python3
from collections.abc import Generator
from math import ceil, log
from sys import argv
import operator
from itertools import cycle


class Intcode(Generator):
    def __init__(self, code):
        self.code = code.copy()
        self.inputs = list()  # queue; use pop(0) and append() and extend()
        self.outputs = list() # queue; use append() and return as a whole
        self.instruction_pointer = 0
        self.operations = {
            1 : (self._arithmetic_op(operator.add), 3),
            2 : (self._arithmetic_op(operator.mul), 3),
            3 : (None, 1),
            4 : (None, 1),
            5 : (self._conditional_jump(True), 2),
            6 : (self._conditional_jump(False), 2),
            7 : (self._arithmetic_op(operator.lt), 3),
            8 : (self._arithmetic_op(operator.eq), 3),
            99: (None, 0)
        }

    def send(self, inputs):
        # Main logic
        if inputs:
            self.inputs.extend(inputs)
        while True:
            instruction = self.code[self.instruction_pointer]
            # print('Instruction:', inst)
            opcode = instruction % 100
            num_params = self.operations[opcode][1]
            param_modes = Intcode._get_param_modes(instruction, num_params)
            # params = []
            # for _ in range(0, operations[opcode][1]):
            #     params.append(next(code_iter))
            parameters = self.code[self.instruction_pointer + 1: self.instruction_pointer + 1 + num_params]
            instruction_pointer_default_increment = num_params + 1
            if opcode == 3:             # INPUT
                # can ignore param_modes, only one param here and it's in `position mode`
                # check if `inputs` has elements
                if self.inputs:
                    self.code[parameters[0]] = self.inputs.pop(0)
                    self.instruction_pointer += instruction_pointer_default_increment
                    continue
                # otherwise 'yield', so caller can send more inputs
                # N.B. do not advance instruction_pointer, as it has to resume from here again
                outputs = self.outputs.copy()
                self.outputs.clear()
                return outputs
            elif opcode == 4:           # OUTPUT
                self.instruction_pointer += instruction_pointer_default_increment
                output = self._output(parameters, param_modes)
                self.outputs.append(output)
            elif opcode == 99:          # TERMINATE
                # return any unflushed outputs
                # N.B. do not advance instruction_pointer, as it has to resume from here again
                if self.outputs:
                    outputs = self.outputs.copy()
                    self.outputs.clear()
                    return outputs
                raise StopIteration
            else:                       # ANY OTHER
                new_instruction_pointer = self.operations[opcode][0](self, params=parameters, param_modes=param_modes)
                if new_instruction_pointer:
                    self.instruction_pointer = new_instruction_pointer
                else:
                    self.instruction_pointer += instruction_pointer_default_increment

    def throw(self, type=None, value=None, traceback=None):
        raise StopIteration

    # def __iter__(self):
    #     return self
    #
    # def __next__(self):
    #     return self.send(None)
    #
    # def close(self):
    #     try:
    #         self.throw(GeneratorExit)
    #     except (GeneratorExit, StopIteration):
    #         pass
    #     else:
    #         raise RuntimeError("Intcode ignored GeneratorExit")

    def _arithmetic_op(self, op):
        def ret_func(self, params, param_modes):
            effective_params = []
            for m, p in zip(param_modes, params):
                if m == 1 : effective_params.append(p)
                else      : effective_params.append(self.code[p])
            res = op(*effective_params[0:2])
            self.code[params[2]] = res
        return ret_func

    def _output(self, params, param_modes):
        if param_modes[0] == 0:
            return self.code[params[0]]
        return params[0]

    def _conditional_jump(self, bool):
        def ret_func(self, params, param_modes):
            effective_params = []
            for m, p in zip(param_modes, params):
                if m == 1 : effective_params.append(p)
                else      : effective_params.append(self.code[p])
            if (effective_params[0] != 0) == bool:
                return effective_params[1]
            return None
        return ret_func

    @staticmethod
    def _get_param_modes(inst, length):
        modes = [0] * length
        for i in range(2, ceil(log(inst, 10))):
            modes[i - 2] = inst // int(pow(10, i)) % 10
        return modes


def main(fn, phase_setting):
    with open(fn, 'r') as f:
        code = [int(x) for x in f.read().split(',')]
    amplifiers = dict()
    for phase_setting, amplifier_name in enumerate('ABCDE', 5):
        amplifiers[amplifier_name] = Intcode(code)
        next(amplifiers[amplifier_name])
        amplifiers[amplifier_name].send(phase_setting)
    signal = 0
    for amplifier_name in cycle('ABCDE'):
        try:
            outputs = amplifiers[amplifier_name].send([signal])
        except StopIteration:
            if amplifier_name == 'E':
                break
            print(f'Amp {amplifier_name} terminated.')
        assert len(outputs) == 1
        signal = outputs[0]
    print(f'Last output: {signal}')


if __name__ == '__main__':
    fn = argv[1] if len(argv) >= 2 else 'input.txt'
    with open('../Day 5/input.txt', 'r') as f:
        code = [int(x) for x in f.read().split(',')]
    day5_part1 = Intcode(code)
    outputs = day5_part1.send([1])
    print(f'Day 5 Part 1: {outputs}')

    day5_part2 = Intcode(code)
    outputs = day5_part2.send([5])
    print(f'Day 5 Part 2: {outputs}')

    # Day 7 to be done