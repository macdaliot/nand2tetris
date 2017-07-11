from errors import *


class Parser():
    def __init__(self, data=None, writer=None):
        self.data = data
        self.writer = writer

    def parse(self):
        for cmd in self.next_command():
            if self.command_type(cmd) == 'C_ARITHMETIC':
                self.writer.write_arithmetic(cmd)
            if cmd.startswith('push') or cmd.startswith('pop'):
                arg1 = self.arg1(cmd)
                arg2 = self.arg2(cmd)
                self.writer.write_push_pop(cmd, arg1, arg2)
            yield cmd

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
        else:
            raise UnknownCmdError(cmd)

    def arg1(self, cmd):
        cmd_type = self.command_type(cmd)
        assert cmd_type != 'C_RETURN', \
            'Cannot get arg1 from return command.'
        if cmd_type == 'C_ARITHMETIC':
            return cmd
        return cmd.split()[1]

    def arg2(self, cmd):
        return cmd.split()[2]

