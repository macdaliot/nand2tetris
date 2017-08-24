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
        for line in self.get_line():
            for t in self.get_tokens_from_line(line):
                yield t

    def get_tokens_from_line(self, line):
        tokens = []
        buf = ''
        for c in line:
            buf += c
            if buf in SYMBOLS:
                tokens.append(Token(buf, 'symbol'))
                buf = ''
            elif buf in KEYWORDS:
                tokens.append(Token(buf, 'keyword'))
                buf = ''
            print buf

        return tokens

    def get_next_nonspace(self, line, i):
        x = 1
        if i == len(line) or i + x == len(line):
            return ''
        while line[i + x] == ' ':
            x += 1
        return line[i + x]

    def get_line(self):
        for line in self.file:
            line = line.strip()
            if line and not re.match(r'\s*(/\*\*|//)', line):
                yield line.partition('//')[0].strip()


class Token():
    def __init__(self, val, _type):
        self.value = val
        self.type = _type

    def __repr__(self):
        return "'%s'" % self.value


if __name__ == '__main__':
    infile = sys.argv[1]
    if os.path.isdir(infile):
        files = [os.path.join(infile, f) for f in os.listdir(infile)]
    else:
        files = [infile]

    for file in files:
        for t in Tokenizer(file).tokenize():
            print t.type, t.value

