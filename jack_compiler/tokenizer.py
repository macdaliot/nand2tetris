import sys
import os
import re
from xml.sax.saxutils import escape

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
        in_string = False
        buf = ''
        i = 0
        for i in range(len(line)):
            if line[i] == '"' and in_string is False:
                in_string = True
                continue
            if in_string is False and buf == '' and line[i] == ' ':
                continue

            if line[i] != '"':
                buf += line[i]
            print buf

            if in_string is True:
                if line[i] == '"':
                    tokens.append(Token(buf, 'stringConstant'))
                    in_string = False
                    buf = ''
                    continue
                else:
                    continue

            next_char = self.get_next_char(line, i)
            if buf in SYMBOLS:
                tokens.append(Token(buf, 'symbol'))
                buf = ''
            elif buf in KEYWORDS:
                tokens.append(Token(buf, 'keyword'))
                buf = ''
            elif next_char == ' ' or (next_char != '' and next_char in SYMBOLS):
                if buf[0].isdigit():
                    tokens.append(Token(buf, 'integerConstant'))
                else:
                    tokens.append(Token(buf, 'identifier'))
                buf = ''

            # if buf:
            #     print buf

        return tokens

    def get_next_char(self, line, i):
        if i + 1 < len(line):
            return line[i + 1]
        return ''

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


def get_files(name):
        if os.path.isdir(name):
            files = [os.path.join(name, f) for f in os.listdir(name)]
        else:
            files = [name]
        return [f for f in files if f.endswith('.jack')]


def tokenize_file(f):
    path = file.rpartition('.')[0]
    with open(path + '.xml', 'w') as outfile:
        outfile.write('<tokens>\n')
        for t in Tokenizer(file).tokenize():
            out = '<{0}> {1} </{0}>\n'.format(t.type, escape(t.value))
            outfile.write(out)
            print t.type, t.value
        outfile.write('</tokens>\n')


if __name__ == '__main__':
    name = sys.argv[1]
    files = get_files(name)

    for file in files:
        tokenize_file(file)
