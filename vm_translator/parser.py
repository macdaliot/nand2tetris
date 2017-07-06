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
        if cmd in ('add', 'sub', 'neg', 'eq',
                   'gt', 'lt', 'and', 'or', 'not'):
            return 'C_ARITHMETIC'
        elif cmd.startswith('push'):
            return 'C_PUSH'
        elif cmd.startswith('pop'):
            return 'C_POP'
        elif cmd.startswith('label'):
            return 'C_LABEL'
        elif cmd.startswith('goto'):
            return 'C_GOTO'
        elif cmd.startswith('if-goto'):
            return 'C_IF'
        elif cmd.startswith('function'):
            return 'C_FUNCTION'
        elif cmd == 'return':
            return 'C_RETURN'
        elif cmd.startswith('call'):
            return 'C_CALL'

    def arg1(self, cmd):
        cmd_type = self.command_type(cmd)
        assert cmd_type != 'C_RETURN', \
            'Cannot get arg1 from return command.'
        if cmd_type == 'C_ARITHMETIC':
            return cmd
        return cmd.split()[1]

    def arg2(self, cmd):
        return cmd.split()[2]

