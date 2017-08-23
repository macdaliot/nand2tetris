import sys
import os
import re

KEYWORDS = ['class', 'constructor', 'function', 'method',
            'field', 'static', 'var', 'int', 'char', 'boolean',
            'void', 'true', 'false', 'null', 'this', 'let',
            'do', 'if', 'else', 'while', 'return']

SYMBOLS = '{(})[].,;+-*/&|<>=_'


class Tokenizer():
    def __init__(self, file):
        self.file = open(file, 'r')

    def tokenize(self):
        sep = ' ,;{}()'
        token = ''
        for line in self.get_line():
            for c in line:
                if c not in sep:
                    token += c
                else:
                    if token:
                        yield token
                    token = ''

    def get_line(self):
        for line in self.file:
            line = line.strip()
            if line and not re.match(r'\s*(/\*\*|//)', line):
                yield line.partition('//')[0]




if __name__ == '__main__':
    infile = sys.argv[1]
    if os.path.isdir(infile):
        files = [os.path.join(infile, f) for f in os.listdir(infile)]
    else:
        files = [infile]

    for file in files:
        for t in Tokenizer(file).tokenize():
            print t

