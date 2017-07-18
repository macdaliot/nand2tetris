class CodeWriter():
    def __init__(self, outfile=None):
        self.outfile = outfile
        if self.outfile:
            self.writer = open(self.outfile, 'w+')
        self.cond_ct = 0
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
            return self.cond(cmd)
        elif cmd == 'gt':
            return self.cond(cmd)
        elif cmd == 'lt':
            return self.cond(cmd)
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

    def cond(self, cmd):
        return (instructions()
                .pop_stack()
                .decrement_sp_and_deref()
                .cond(cmd, self)
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

    def push(self, cmd, segment, index):
        return (instructions()
                .get_segment_value(segment, index)
                .deref('SP')
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
        elif segment == 'constant':
            self.add('@%s' % index)
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
        if segment not in ('SP', 'constant', 'static'):
            self.add('@%s' % index)\
                .add('A=D+A')  # A = segment[index]
        return self

    def get_segment_value(self, segment, index=0):
        self.deref(segment, index)
        if segment == 'constant':
            self.add('D=A')
        else:
            self.add('D=M')
        return self

    def cond(self, condition, writer):
        condition = condition.upper()
        writer.cond_ct += 1
        (self.add('D=M-D')
             .add('M=-1')
             .add('@%s%s' % (condition, writer.cond_ct))
             .add('D;J%s' % condition)
             .deref('SP')
             .add('M=0')
             .add('(%s%s)' % (condition, writer.cond_ct)))
        return self
