class CodeWriter():
    def __init__(self, outfile):
        self.outfile = outfile
        self.writer = open(self.outfile, 'w+')

    def set_filename(self, filename):
        self.filename = filename

    def write_arithmetic(self, cmd):
        pass

    def write_push_pop(self, cmd):
        pass

    def close(self):
        self.writer.close()

