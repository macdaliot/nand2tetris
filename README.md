How to use assembler
====================

```bash
$ python assembler prog.asm

# prints
# 0000000000010000
# 0000000000010001
# 1110101110111000
# 1110000111111010
# 0000000000010010
# 1111010011111111
# 0000000000010011

# and creates file
# prog.hack
```


How to use vm_translator
========================

```bash
# test.vm
# // Pushes and adds two constants.
# push constant 7
# push constant 8
# add

$ python vm_translator test.vm

# outputs file in assembly (test.asm)
$ cat test.asm
@7
D=A
@SP
A=M
M=D
@SP
M=M+1
@8
D=A
@SP
A=M
M=D
@SP
M=M+1
@SP
M=M-1
A=M
D=M
@SP
M=M-1
A=M
D=D+M
M=D
@SP
M=M+1
```