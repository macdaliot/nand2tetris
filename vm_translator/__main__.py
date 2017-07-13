import sys
from parser import Parser
from code_writer import CodeWriter

in_file = sys.argv[1]

writer = CodeWriter(in_file + '.asm')

with open(in_file) as f:
    writer.set_filename(in_file.split('.')[0])
    parser = Parser(f, writer)
    for instr in parser.parse():
        print instr
