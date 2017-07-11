import code
from symbol import Symbol_Table


def init_labels(in_file):
    cmd_cnt = 0
    for cur_cmd in commands(in_file):
        com_type = command_type(cur_cmd)
        if com_type in ('A_COMMAND', 'C_COMMAND'):
            cmd_cnt += 1
        elif com_type == 'L_COMMAND':
            sym = symbol(cur_cmd, com_type)
            symbols.add_entry(sym, cmd_cnt)
    in_file.seek(0)


def build_vars(in_file):
    global last_ram_addr
    for cur_cmd in commands(in_file):
        com_type = command_type(cur_cmd)
        if com_type == 'A_COMMAND':
            sym = symbol(cur_cmd, com_type)
            # print symbols
            if not sym.isdigit() and sym not in symbols.table:
                # print 'adding', sym, last_ram_addr
                symbols.add_entry(sym, last_ram_addr)
                last_ram_addr += 1
    in_file.seek(0)


def parse(in_file):
    output = []
    for cur_cmd in commands(in_file):
        com_type = command_type(cur_cmd)
        if com_type in ('A_COMMAND'):
            sym = symbol(cur_cmd, com_type)
            addr = symbols.get_address(sym)
            b = binary(addr)
            add_to_out(b, output)
        elif com_type == 'C_COMMAND':
            c = cmd(dest(cur_cmd), comp(cur_cmd), jump(cur_cmd))
            add_to_out(c, output)
    return output


def commands(in_file):
    for cmd in in_file:
        cmd = cmd.partition('//')[0].strip()
        if cmd and not cmd.startswith('//'):
            yield cmd


# def advance():
#     pass

def add_to_out(l, out):
    out.append(l)
    # print l


def binary(num):
    return '{0:b}'.format(int(num)).rjust(16, '0')


def cmd(dest, comp, jump):
    return '111' + code.comp(comp) + code.dest(dest) + code.jump(jump)


def command_type(cmd):
    if cmd.startswith('@'):
        return 'A_COMMAND'
    elif cmd.startswith('('):
        return 'L_COMMAND'
    else:
        return 'C_COMMAND'


def symbol(cmd, _type):
    if _type == 'A_COMMAND':
        return cmd[1:]
    elif _type == 'L_COMMAND':
        return cmd[1:-1]


def dest(cmd):
    if '=' in cmd:
        return cmd.split('=')[0]


def comp(cmd):
    return cmd.split(';')[0].split('=')[-1]


def jump(cmd):
    if ';' in cmd:
        return cmd.split(';')[-1]


def main(in_file):
    global symbols
    symbols = Symbol_Table()
    global last_ram_addr
    last_ram_addr = 16

    init_labels(in_file)
    # pprint.pprint(symbols.table)
    build_vars(in_file)
    # pprint.pprint(symbols.table)
    out = parse(in_file)
    return '\n'.join(out)
