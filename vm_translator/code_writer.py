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
        return (instructions()
                .add('@256')
                .add('D=A')
                .add('@SP')
                .add('M=D'))

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
        return (instructions()
                .pop_stack()
                .decrement_sp_and_deref()
                .add('D=D+M')
                .add('M=D')
                .increment_sp())

    def sub(self, cmd):
        return (instructions()
                .pop_stack()
                .decrement_sp_and_deref()
                .add('D=M-D')
                .add('M=D')
                .increment_sp())

    def neg(self, cmd):
        return (instructions()
                .decrement_sp_and_deref()
                .add('M=-M')
                .increment_sp())

    def eq(self, cmd):
        self.eq_ct += 1
        return (instructions()
                .pop_stack()
                .decrement_sp_and_deref()
                .add('D=M-D')
                .add('M=-1')
                .add('@EQ%s' % self.eq_ct)
                .add('D;JEQ')
                .deref('SP')
                .add('M=0')
                .add('(EQ%s)' % self.eq_ct)
                .increment_sp())

    def gt(self, cmd):
        self.gt_ct += 1
        return (instructions()
                .pop_stack()
                .decrement_sp_and_deref()
                .add('D=M-D')
                .add('M=-1')
                .add('@GT%s' % self.gt_ct)
                .add('D;JGT')
                .deref('SP')
                .add('M=0')
                .add('(GT%s)' % self.gt_ct)
                .increment_sp())

    def lt(self, cmd):
        self.lt_ct += 1
        return (instructions()
                .pop_stack()
                .decrement_sp_and_deref()
                .add('D=M-D')
                .add('M=-1')
                .add('@LT%s' % self.lt_ct)
                .add('D;JLT')
                .deref('SP')
                .add('M=0')
                .add('(LT%s)' % self.lt_ct)
                .increment_sp())

    def _and(self, cmd):
        return (instructions()
                .pop_stack()
                .decrement_sp_and_deref()
                .add('D=D&M')
                .add('M=D')
                .increment_sp())

    def _or(self, cmd):
        return (instructions()
                .pop_stack()
                .decrement_sp_and_deref()
                .add('D=D|M')
                .add('M=D')
                .increment_sp())

    def _not(self, cmd):
        return (instructions()
                .decrement_sp_and_deref()
                .add('M=!M')
                .increment_sp())

    def push_pop(self, cmd, segment, index):
            if cmd.startswith('push'):
                return self.push(cmd, segment, index)
            elif cmd.startswith('pop'):
                return self.pop(cmd, segment, index)

    def push(self, cmd, segment, index):
        instrs = instructions()
        if segment == 'constant':
            (instrs.add('@%s' % index)
                   .add('D=A'))
        else:
            (instrs.deref(segment, index)
                   .add('D=M'))
        return (instrs.deref('SP')
                      .add('M=D')
                      .increment_sp())

    def pop(self, cmd, segment, index):
        return (instructions()
                .deref('SP')
                .add('M=0')
                .pop_stack()
                .add('@13')
                .add('M=D')
                .deref(segment, index)
                .add('D=A')
                .add('@14')
                .add('M=D')
                .add('@13')
                .add('D=M')
                .add('@14')
                .add('A=M')
                .add('M=D'))

    def label(self, label):
        return ['(%s)' % label]

    def goto(self, label):
        return (instructions()
                .add('@%s' % label)
                .add('0;JMP'))

    def if_goto(self, label):
        return (instructions()
                .pop_stack()
                .add('@%s' % label)
                .add('D;JGT'))

    def pop_stack(self):
        return (instructions()
                .decrement_sp_and_deref()
                .add('D=M'))

    def close(self):
        self.writer.close()


class instructions():
    def __init__(self):
        self.instrs = []

    def __getitem__(self, i):
        return self.instrs[i]

    def add(self, i):
        self.instrs.append(i)
        return self

    def decrement_sp_and_deref(self):
        self.add('@SP')\
            .add('M=M-1')\
            .add('A=M')
        return self

    def increment_sp(self):
        self.add('@SP')\
            .add('M=M+1')
        return self

    def pop_stack(self):
        self.decrement_sp_and_deref()\
            .add('D=M')
        return self

    def deref(self, segment, index=0):
        if segment == 'SP':
            self.add('@%s' % segment)\
                .add('A=M')
        elif segment == 'pointer':
            self.add('@3')\
                .add('D=A')
        elif segment == 'temp':
            self.add('@5')\
                .add('D=A')
        elif segment == 'static':
            self.add('@%s.%s' % (self.filename, index))
        else:
            self.add('@%s' % segment)\
                .add('D=M')
        if segment != 'static' and segment != 'SP':
            self.add('@%s' % index)\
                .add('A=D+A')  # A = segment[index]
        return self

