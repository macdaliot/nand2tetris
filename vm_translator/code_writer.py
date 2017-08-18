class CodeWriter():
    def __init__(self, outfile=None):
        self.outfile = outfile
        if self.outfile:
            self.writer = open(self.outfile, 'w+')
        self.cond_ct = 0
        self.num_func_calls = 0
        self.write_init()
        self.write_instructions(self.call('Sys.init', 0))

    @classmethod
    def set_filename(cls, filename):
        cls.filename = filename

    def write_init(self):
        self.write_instructions(
            instructions()
            .add('@256')
            .add('D=A')
            .set_value('SP'))

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
                .incr_ptr('SP'))

    def sub(self, cmd):
        return (instructions()
                .pop_stack()
                .decrement_sp_and_deref()
                .add('D=M-D')
                .add('M=D')
                .incr_ptr('SP'))

    def neg(self, cmd):
        return (instructions()
                .decrement_sp_and_deref()
                .add('M=-M')
                .incr_ptr('SP'))

    def cond(self, cmd):
        return (instructions()
                .pop_stack()
                .decrement_sp_and_deref()
                .cond(cmd, self)
                .incr_ptr('SP'))

    def _and(self, cmd):
        return (instructions()
                .pop_stack()
                .decrement_sp_and_deref()
                .add('D=D&M')
                .add('M=D')
                .incr_ptr('SP'))

    def _or(self, cmd):
        return (instructions()
                .pop_stack()
                .decrement_sp_and_deref()
                .add('D=D|M')
                .add('M=D')
                .incr_ptr('SP'))

    def _not(self, cmd):
        return (instructions()
                .decrement_sp_and_deref()
                .add('M=!M')
                .incr_ptr('SP'))

    def push(self, cmd, segment, index):
        return (instructions()
                .get_ptr_value(segment, index)
                .get_addr('SP')
                .add('M=D')
                .incr_ptr('SP'))

    def pop(self, cmd, segment, index):
        return (instructions()
                .pop_stack()
                .get_addr(segment, index)
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
                .add('D;JNE'))

    def call(self, name, num_args):
        self.num_func_calls += 1
        retr_addr = '%s-return-%s' % (name, self.num_func_calls)
        instrs = (instructions()
                  .push_addr_to_stack(retr_addr)
                  .push_val_at_addr_to_stack('LCL')
                  .push_val_at_addr_to_stack('ARG')
                  .push_val_at_addr_to_stack('THIS')
                  .push_val_at_addr_to_stack('THAT')
                  .get_value('SP')
                  .decr_value(int(num_args))
                  .decr_value(5)
                  .set_value('ARG')
                  .get_value('SP')
                  .set_value('LCL')
                  .extend(self.goto(name))
                  .extend(self.label(retr_addr)))
        return instrs

    def _return(self):
        return (instructions()
                .get_value('LCL')
                .set_value(13)
                .add('@5')
                .add('A=D-A')
                .add('D=M')
                .set_value(14)
                .pop_stack()  # repos retr value for caller
                .add('@ARG')
                .add('A=M')
                .add('M=D')
                .add('@ARG')
                .add('D=M+1')  # restore SP of the caller
                .set_value('SP')
                .restore_from_frame('THAT', 1)
                .restore_from_frame('THIS', 2)
                .restore_from_frame('ARG', 3)
                .restore_from_frame('LCL', 4)
                .add('@14')
                .add('A=M')
                .add('0;JMP')
                )

    def function(self, name, num_locals):
        instrs = instructions().extend(self.label(name))
        for i in range(int(num_locals)):
            instrs.add('@0') \
                  .add('D=A') \
                  .push_to_stack()
        return instrs

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

    def extend(self, i):
        self.instrs.extend(i)
        return self

    def decrement_sp_and_deref(self):
        self.decr_ptr('SP')\
            .add('A=M')
        return self

    def decr_value(self, num):
        (self.add('@%s' % num)
            .add('D=D-A'))
        return self

    def incr_ptr(self, ptr):
        self.add('@%s' % ptr)\
            .add('M=M+1')
        return self

    def decr_ptr(self, ptr):
        self.add('@%s' % ptr)\
            .add('M=M-1')
        return self

    def pop_stack(self):
        self.decrement_sp_and_deref()\
            .add('D=M')
        return self

    def push_to_stack(self):
        self.get_addr('SP')\
            .add('M=D')\
            .incr_ptr('SP')
        return self

    def get_addr(self, segment, index=0):
        self.add('// deref %s %s' % (segment, index))
        if isinstance(segment, int):
            self.add('@%s' % segment)
        elif segment == 'SP':
            self.add('@%s' % segment)\
                .add('A=M')
        elif segment == 'constant':
            self.add('@%s' % index)
        elif segment == 'pointer':
            self.add('@%s' % (3 + int(index)))
        elif segment == 'temp':
            self.add('@%s' % (5 + int(index)))
        elif segment == 'static':
            self.add('@%s.%s' % (CodeWriter.filename, index))
        else:
            (self.set_value(13)
                 .get_value(segment)
                 .add('@%s' % index)
                 .add('A=D+A')  # A = segment[index]
                 .add('D=A')
                 .set_value(14)
                 .get_value(13)
                 .add('@14')
                 .add('A=M'))
        return self

    def set_value(self, addr):
        (self.add('@%s' % addr)
             .add('M=D'))
        return self

    def get_value(self, addr):
        (self.add('@%s' % addr)
             .add('D=M'))
        return self

    def get_ptr_value(self, segment, index=0):
        self.get_addr(segment, index)
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
             .get_addr('SP')
             .add('M=0')
             .add('(%s%s)' % (condition, writer.cond_ct)))
        return self

    def push_addr_to_stack(self, addr):
        (self.add('@%s' % addr)
            .add('D=A')
            .push_to_stack())
        return self

    def push_val_at_addr_to_stack(self, addr):
        (self.add('@%s' % addr)
            .add('D=M')
            .push_to_stack())
        return self

    def restore_from_frame(self, loc, idx):
        (self.get_ptr_value(13)
            .decr_value(idx)
            .add('A=D')
            .add('D=M')
            .set_value(loc))
        return self
