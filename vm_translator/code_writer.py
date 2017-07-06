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

    def make_push_pop(self, cmd, segment, index):
            if cmd == 'C_PUSH':
                self.make_push(self, cmd, segment, index)
            elif cmd == 'C_POP':
                self.make_pop(self, cmd, segment, index)

    def make_push(self, cmd, segment, index):
        out = []
        out.append('@%s' % segment)
        out.append('D=M')
        return out


    def close(self):
        self.writer.close()

