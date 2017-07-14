class CodeWriter():
    def __init__(self, outfile=None):
        self.outfile = outfile
        if self.outfile:
            self.writer = open(self.outfile, 'w+')
        self.eq_ct = 0
        self.gt_ct = 0
        self.lt_ct = 0
        self.write_init()

    def set_filename(self, filename):
        self.filename = filename

    def write_init(self):
        instructions = self.init()
        self.write_instructions(instructions)

    def init(self):
        out = []
        out.append('@256')
        out.append('D=A')
        out.append('@SP')
        out.append('M=D')
        return out

    def write_arithmetic(self, cmd):
        instructions = self.arithmetic(cmd)
        self.write_instructions(instructions)

    def write_push_pop(self, cmd, segment, index):
        instructions = self.push_pop(cmd, segment, index)
        self.write_instructions(instructions)

    def write_label(self, label):
        instructions = self.label(label)
        self.write_instructions(instructions)

    def write_goto(self, label):
        instructions = self.goto(label)
        self.write_instructions(instructions)

    def write_if_goto(self, label):
        instructions = self.if_goto(label)
        self.write_instructions(instructions)

    def write_call(self, func_name, num_args):
        pass

    def write_function(self, func_name, num_locals):
        pass

    def write_instructions(self, instructions):
        for instr in instructions:
            self.writer.write('%s\n' % instr)

    def arithmetic(self, cmd):
        if cmd == 'add':
            return self.add(cmd)
        elif cmd == 'sub':
            return self.sub(cmd)
        elif cmd == 'neg':
            return self.neg(cmd)
        elif cmd == 'eq':
            return self.eq(cmd)
        elif cmd == 'gt':
            return self.gt(cmd)
        elif cmd == 'lt':
            return self.lt(cmd)
        elif cmd == 'and':
            return self._and(cmd)
        elif cmd == 'or':
            return self._or(cmd)
        elif cmd == 'not':
            return self._not(cmd)

    def add(self, cmd):
        out = []
        out.extend(self.pop_stack())
        out.extend(self.decrement_sp_and_deref())
        out.append('D=D+M')  # x + y
        out.append('M=D')  # Save result
        out.extend(self.increment_sp())
        return out

    def sub(self, cmd):
        out = []
        out.extend(self.pop_stack())
        out.extend(self.decrement_sp_and_deref())
        out.append('D=M-D')  # x - y
        out.append('M=D')  # Save result
        out.extend(self.increment_sp())
        return out

    def neg(self, cmd):
        out = []
        out.extend(self.decrement_sp_and_deref())
        out.append('M=-M')  # Set M = -M
        out.extend(self.increment_sp())
        return out

    def eq(self, cmd):
        out = []
        out.extend(self.pop_stack())
        out.extend(self.decrement_sp_and_deref())
        out.append('D=M-D')
        out.append('M=-1')
        out.append('@EQ%s' % self.eq_ct)
        out.append('D;JEQ')  # If eq jump to EQ
        out.extend(self.deref('SP'))
        out.append('M=0')  # Set to false
        out.append('(EQ%s)' % self.eq_ct)
        out.extend(self.increment_sp())
        self.eq_ct += 1
        return out

    def gt(self, cmd):
        out = []
        out.extend(self.pop_stack())
        out.extend(self.decrement_sp_and_deref())
        out.append('D=M-D')
        out.append('M=-1')
        out.append('@GT%s' % self.gt_ct)
        out.append('D;JGT')  # If greater than jump to GT
        out.extend(self.deref('SP'))
        out.append('M=0')  # Set to false
        out.append('(GT%s)' % self.gt_ct)
        out.extend(self.increment_sp())
        self.gt_ct += 1
        return out

    def lt(self, cmd):
        out = []
        out.extend(self.pop_stack())
        out.extend(self.decrement_sp_and_deref())
        out.append('D=M-D')
        out.append('M=-1')
        out.append('@LT%s' % self.lt_ct)
        out.append('D;JLT')  # If less than jump to LT
        out.extend(self.deref('SP'))
        out.append('M=0')  # Set to false
        out.append('(LT%s)' % self.lt_ct)
        out.extend(self.increment_sp())
        self.lt_ct += 1
        return out

    def _and(self, cmd):
        out = []
        out.extend(self.pop_stack())
        out.extend(self.decrement_sp_and_deref())
        out.append('D=D&M')  # x & y
        out.append('M=D')  # Save result
        out.extend(self.increment_sp())
        return out

    def _or(self, cmd):
        out = []
        out.extend(self.pop_stack())
        out.extend(self.decrement_sp_and_deref())
        out.append('D=D|M')  # x | y
        out.append('M=D')  # Save result
        out.extend(self.increment_sp())
        return out

    def _not(self, cmd):
        out = []
        out.extend(self.decrement_sp_and_deref())
        out.append('M=!M')  # Set M = !M
        out.extend(self.increment_sp())
        return out

    def decrement_sp_and_deref(self):
        return ['@SP', 'M=M-1', 'A=M']

    def increment_sp(self):
        return ['@SP', 'M=M+1']

    def push_pop(self, cmd, segment, index):
            if cmd.startswith('push'):
                return self.push(cmd, segment, index)
            elif cmd.startswith('pop'):
                return self.pop(cmd, segment, index)

    def push(self, cmd, segment, index):
        out = []
        if segment == 'constant':
            out.append('@%s' % index)
            out.append('D=A')
        else:
            out.extend(self.deref(segment, index))
            out.append('D=M')
        out.extend(self.deref('SP'))  # Get addr from SP
        out.append('M=D')  # Set M[SP] = segment[index] or constant
        out.extend(self.increment_sp())
        out[0] += '  // pushing %s %s' % (segment, index)
        return out

    def deref(self, segment, index=0):
        out = []
        if segment == 'pointer':
            out.append('@3')
            out.append('D=A')
        elif segment == 'temp':
            out.append('@5')
            out.append('D=A')
        elif segment == 'static':
            out.append('@%s.%s' % (self.filename, index))
        else:
            out.append('@%s' % segment)
            out.append('D=M')
        if segment != 'static' and segment != 'SP':
            out.append('@%s' % index)
            out.append('A=D+A')  # A = segment[index]
        return out

    def pop(self, cmd, segment, index):
        out = []
        out.extend(self.deref('SP'))  # Get addr of SP
        out.append('M=0')  # Zero out M[SP]
        out.extend(self.pop_stack())
        out.append('@13')
        out.append('M=D')  # R5 = M[SP]
        out.extend(self.deref(segment, index))
        out.append('D=A')
        out.append('@14')
        out.append('M=D')  # R6 = addr segment[index]
        out.append('@13')
        out.append('D=M')  # D = M[SP]
        out.append('@14')
        out.append('A=M')
        out.append('M=D')  # Set segment[index] = M[SP]
        out[0] += '  // popping %s %s' % (segment, index)
        return out

    def label(self, label):
        return ['(%s)' % label]

    def goto(self, label):
        out = []
        out.append('@%s' % label)
        out.append('0;JMP')
        return out

    def if_goto(self, label):
        out = []
        out.extend(self.pop_stack())
        out.append('@%s' % label)
        out.append('D;JGT')
        return out

    def pop_stack(self):
        out = []
        out.extend(self.decrement_sp_and_deref())
        out.append('D=M')
        return out

    def close(self):
        self.writer.close()

