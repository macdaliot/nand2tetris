from errors import *


class Parser():
    def __init__(self, data=None, writer=None):
        self.data = data
        self.writer = writer

    def write_command(self, cmd):
        if not self.writer:
            return
        c_type = self.command_type(cmd)
        arg1 = self.arg1(cmd)
        arg2 = self.arg2(cmd)
        if c_type == 'C_ARITHMETIC':
            instrs = self.writer.arithmetic(cmd)
        elif c_type == 'C_PUSH':
            instrs = self.writer.push(cmd, arg1, arg2)
        elif c_type == 'C_POP':
            instrs = self.writer.pop(cmd, arg1, arg2)
        elif c_type == 'C_LABEL':
            instrs = self.writer.label(arg1)
        elif c_type == 'C_GOTO':
            instrs = self.writer.goto(arg1)
        elif c_type == 'C_IF':
            instrs = self.writer.if_goto(arg1)
        self.writer.write_instructions(instrs)


    def parse(self):
        for cmd in self.next_command():
            self.write_command(cmd)
            yield cmd

    def next_command(self):
        for line in self.data:
            line = line.strip().split('//')[0]
            if line and not line.startswith('//'):
                yield line.strip()

    def command_type(self, cmd):
        cmd = cmd.strip()
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
        arg1 = cmd.split()[1]
        if arg1 in segment_map:
            return segment_map[arg1]
        return arg1

    def arg2(self, cmd):
        return cmd.split()[:3][-1]


segment_map = {
    'local': 'LCL',
    'argument': 'ARG',
    'this': 'THIS',
    'that': 'THAT'
}
