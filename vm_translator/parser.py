class Parser():
    def __init__(self, data):
        self.data = data

    def parse(self):
        for cmd in self.next_command():
            print cmd

    def next_command(self):
        for line in self.data:
            line = line.strip().split('//')[0]
            if line and not line.startswith('//'):
                yield line

    def command_type(self, cmd):
        if cmd:
            return 'C_ARITHMETIC'
        elif cmd:
            return 'C_PUSH'
        elif cmd:
            return 'C_POP'
        elif cmd:
            return 'C_LABEL'
        elif cmd:
            return 'C_GOTO'
        elif cmd:
            return 'C_IF'
        elif cmd:
            return 'C_FUNCTION'
        elif cmd:
            return 'C_RETURN'
        elif cmd:
            return 'C_CALL'

    def arg1(self, cmd):
        return cmd.split()[1]

    def arg2(self, cmd):
        return cmd.split()[2]

