class CodeWriter():
    def __init__(self, outfile=None):
        self.outfile = outfile
        if self.outfile:
            self.writer = open(self.outfile, 'w+')

    def set_filename(self, filename):
        self.filename = filename

    def write_arithmetic(self, cmd):
        pass

    def write_push_pop(self, cmd):
        pass

    def make_arithmetic(self, cmd):
        pass

    def push_pop(self, cmd, segment, index):
            if cmd == 'push':
                return self.push(cmd, segment, index)
            elif cmd == 'pop':
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

