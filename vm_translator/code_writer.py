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
        pass

    def write_goto(self, label):
        pass

    def write_if(self, label):
        pass

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
        out.append('@SP')
        out.append('M=M-1')  # Decrement SP
        out.append('A=M')
        out.append('D=M')  # Set D = M[SP]
        out.append('@SP')
        out.append('M=M-1')  # Decrement SP
        out.append('A=M')
        out.append('D=D+M')  # x + y
        out.append('M=D')  # Save result
        out.append('@SP')
        out.append('M=M+1')  # Increment SP
        return out

    def sub(self, cmd):
        out = []
        out.append('@SP')
        out.append('M=M-1')  # Decrement SP
        out.append('A=M')
        out.append('D=M')  # Set D = M[SP]
        out.append('@SP')
        out.append('M=M-1')  # Decrement SP
        out.append('A=M')
        out.append('D=M-D')  # x - y
        out.append('M=D')  # Save result
        out.append('@SP')
        out.append('M=M+1')  # Increment SP
        return out

    def neg(self, cmd):
        out = []
        out.append('@SP')
        out.append('M=M-1')  # Decrement SP
        out.append('A=M')
        out.append('M=-M')  # Set D = -M[SP]
        out.append('@SP')
        out.append('M=M+1')  # Increment SP
        return out

    def eq(self, cmd):
        out = []
        out.append('@SP')
        out.append('M=M-1')  # Decrement SP
        out.append('A=M')
        out.append('D=M')  # Set D = M[SP]
        out.append('@SP')
        out.append('M=M-1')  # Decrement SP
        out.append('A=M')
        out.append('D=M-D')
        out.append('M=-1')
        out.append('@EQ%s' % self.eq_ct)
        out.append('D;JEQ')  # If eq jump to EQ
        out.append('@SP')
        out.append('A=M')
        out.append('M=0')  # Set to false
        out.append('(EQ%s)' % self.eq_ct)
        out.append('@SP')
        out.append('M=M+1')  # Increment SP
        self.eq_ct += 1
        return out

    def gt(self, cmd):
        out = []
        out.append('@SP')
        out.append('M=M-1')  # Decrement SP
        out.append('A=M')
        out.append('D=M')  # Set D = M[SP]
        out.append('@SP')
        out.append('M=M-1')  # Decrement SP
        out.append('A=M')
        out.append('D=M-D')
        out.append('M=-1')
        out.append('@GT%s' % self.gt_ct)
        out.append('D;JGT')  # If greater than jump to GT
        out.append('@SP')
        out.append('A=M')
        out.append('M=0')  # Set to false
        out.append('(GT%s)' % self.gt_ct)
        out.append('@SP')
        out.append('M=M+1')  # Increment SP
        self.gt_ct += 1
        return out

    def lt(self, cmd):
        out = []
        out.append('@SP')
        out.append('M=M-1')  # Decrement SP
        out.append('A=M')
        out.append('D=M')  # Set D = M[SP]
        out.append('@SP')
        out.append('M=M-1')  # Decrement SP
        out.append('A=M')
        out.append('D=M-D')
        out.append('M=-1')
        out.append('@LT%s' % self.lt_ct)
        out.append('D;JLT')  # If less than jump to LT
        out.append('@SP')
        out.append('A=M')
        out.append('M=0')  # Set to false
        out.append('(LT%s)' % self.lt_ct)
        out.append('@SP')
        out.append('M=M+1')  # Increment SP
        self.lt_ct += 1
        return out

    def _and(self, cmd):
        out = []
        out.append('@SP')
        out.append('M=M-1')  # Decrement SP
        out.append('A=M')
        out.append('D=M')  # Set D = M[SP]
        out.append('@SP')
        out.append('M=M-1')  # Decrement SP
        out.append('A=M')
        out.append('D=D&M')  # x & y
        out.append('M=D')  # Save result
        out.append('@SP')
        out.append('M=M+1')  # Increment SP
        return out

    def _or(self, cmd):
        out = []
        out.append('@SP')
        out.append('M=M-1')  # Decrement SP
        out.append('A=M')
        out.append('D=M')  # Set D = M[SP]
        out.append('@SP')
        out.append('M=M-1')  # Decrement SP
        out.append('A=M')
        out.append('D=D|M')  # x | y
        out.append('M=D')  # Save result
        out.append('@SP')
        out.append('M=M+1')  # Increment SP
        return out

    def _not(self, cmd):
        out = []
        out.append('@SP')
        out.append('M=M-1')  # Decrement SP
        out.append('A=M')
        out.append('M=!M')  # Set D = !M[SP]
        out.append('@SP')
        out.append('M=M+1')  # Increment SP
        return out

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
            out.append('@%s' % segment)
            out.append('D=A')
            out.append('@%s' % index)
            out.append('A=D+A')  # A = segment[index]
            out.append('D=M')  # Store value at A
        out.append('@SP')
        out.append('A=M')  # Get addr of SP
        out.append('M=D')  # Set M[SP] = segment[index]
        out.append('@SP')
        out.append('M=M+1')  # Increment SP to next empty pos
        return out

    def pop(self, cmd, segment, index):
        out = []
        out.append('@SP')
        out.append('A=M')  # Get addr of SP
        out.append('M=0')  # Zero out M[SP]
        out.append('@SP')
        out.append('M=M-1')  # Decrement SP
        out.append('A=M')
        out.append('D=M')  # Set D = M[SP]
        out.append('@5')
        out.append('M=D')  # R5 = M[SP]
        out.append('@%s' % segment)
        out.append('D=A')
        out.append('@%s' % index)
        out.append('A=D+A')  # Set A to segment[index]
        out.append('@6')
        out.append('M=A')  # R6 = addr segment[index]
        out.append('@5')
        out.append('D=M')  # R5 = M[SP]
        out.append('@6')
        out.append('A=M')
        out.append('M=D')  # Set segment[index] = M[SP]
        return out


    def close(self):
        self.writer.close()

