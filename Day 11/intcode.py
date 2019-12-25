from collections.abc import Generator
from math import ceil, log
import operator


class Intcode(Generator):
    def __init__(self, code):
        self.code = code.copy()
        self.inputs = list()   # queue; use pop(0) and append() and extend()
        self.outputs = list()  # queue; use append() and return as a whole
        self.instruction_pointer = 0
        self.relative_base = 0
        self.operations = {
            1 : (self._arithmetic_op(operator.add), 3),
            2 : (self._arithmetic_op(operator.mul), 3),
            3 : (None, 1),
            4 : (None, 1),
            5 : (self._conditional_jump(True), 2),
            6 : (self._conditional_jump(False), 2),
            7 : (self._arithmetic_op(operator.lt), 3),
            8 : (self._arithmetic_op(operator.eq), 3),
            9 : (self._increase_relative_base, 1),
            99 : (None, 0)
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
                # check if `inputs` has elements
                if self.inputs:
                    if param_modes[0] == 0:
                        self.code[parameters[0]] = self.inputs.pop(0)
                    elif param_modes[0] == 2:
                        self.code[self.relative_base + parameters[0]] = self.inputs.pop(0)
                    else:
                        print(f'Unexpected parameter mode {param_modes[0]} for opcode {opcode}.')
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
                new_instruction_pointer = self.operations[opcode][0](parameters, param_modes)
                if new_instruction_pointer:
                    self.instruction_pointer = new_instruction_pointer
                else:
                    self.instruction_pointer += instruction_pointer_default_increment

    def throw(self, type=None, value=None, traceback=None):
        raise StopIteration

    def _arithmetic_op(self, op):
        def ret_func(params, param_modes):
            effective_params = []
            for m, p in zip(param_modes[0:2], params[0:2]):
                if m == 0   : effective_params.append(self.code[p])
                elif m == 1 : effective_params.append(p)
                elif m == 2 : effective_params.append(self.code[self.relative_base + p])

            for m, p in zip(param_modes[2:3], params[2:3]):
                if m == 0   : effective_params.append(p)
                elif m == 1 : pass
                elif m == 2 : effective_params.append(self.relative_base + p)

            res = op(*effective_params[0:2])
            self.code[effective_params[2]] = int(res)
        return ret_func

    def _output(self, params, param_modes):
        if   param_modes[0] == 0 : return self.code[params[0]]
        elif param_modes[0] == 1 : return params[0]
        elif param_modes[0] == 2 : return self.code[self.relative_base + params[0]]

    def _conditional_jump(self, bool):
        def ret_func(params, param_modes):
            nonlocal bool
            effective_params = []
            for m, p in zip(param_modes, params):
                if   m == 0 : effective_params.append(self.code[p])
                elif m == 1 : effective_params.append(p)
                elif m == 2 : effective_params.append(self.code[self.relative_base + p])
            if (effective_params[0] != 0) == bool:
                return effective_params[1]
            return None
        return ret_func

    def _increase_relative_base(self, params, param_modes):
        if   param_modes[0] == 0 : effective_param = self.code[params[0]]
        elif param_modes[0] == 1 : effective_param = params[0]
        elif param_modes[0] == 2 : effective_param = self.code[self.relative_base + params[0]]
        self.relative_base += effective_param

    @staticmethod
    def _get_param_modes(inst, length):
        modes = [0] * length
        for i in range(2, ceil(log(inst, 10))):
            modes[i - 2] = inst // int(pow(10, i)) % 10
        return modes
