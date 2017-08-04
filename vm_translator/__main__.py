import os
import sys
from parser import Parser
from code_writer import CodeWriter

vm_file = sys.argv[1]

writer = CodeWriter(vm_file + '.asm')

path = ''
if os.path.isdir(vm_file):
    path = vm_file
    vm_files = os.listdir(vm_file)
else:
    vm_files = [vm_file]

for vm_file in vm_files:
    print 'parsing:', vm_file
    with open(os.path.join(path, vm_file)) as f:
        writer.set_filename(vm_file.split('.')[0])
        parser = Parser(f, writer)
        for instr in parser.parse():
            print instr
