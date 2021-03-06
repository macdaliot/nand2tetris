import os
import sys
from tokenizer import Tokenizer
from xml.sax.saxutils import escape
from functools import wraps

class Parser():
    def __init__(self, infile):
        self.infile = infile
        path = infile.rpartition('.')[0]
        self.outfile = open(path + '.xml', 'w')
        self.tokenizer = Tokenizer(infile).tokenize()
        self.tokens = []
        self.indent = 0

    def writeln(self, txt):
        self.outfile.write(' ' * self.indent + '%s\n' % txt)

    def write_t(self, t):
        self.writeln('<{0}> {1} </{0}>'.format(t.type, escape(t.value)))

    def assert_write_next_t(self, value='', _type='', msg=''):
        t = self.tokenizer.next()
        assert (t.value in value or t.type in _type), '%s:%s: %s: %s' % (self.infile, t.line, t, msg)
        self.write_t(t)

    def incr_indent(self):
        self.indent += 2

    def decr_indent(self):
        if self.indent >= 0:
            self.indent -= 2

    def struct(name):
        def decorator(f):
            @wraps(f)
            def wrapper(self, *args, **kwargs):
                self.writeln('<%s>' % name)
                self.incr_indent()
                f(self, *args, **kwargs)
                self.decr_indent()
                self.writeln('</%s>' % name)
            return wrapper
        return decorator

    @struct('class')
    def compile_class(self):
        self.assert_write_next_t(value='class',
            msg='File should start with a class')
        self.assert_write_next_t(_type='identifier',
            msg='class keyword should be followed by and identifier')
        self.assert_write_next_t(value='{',
            msg='class declaration should end with "{"')
        for t in self.tokenizer:
            self.tokens.append(t)
            if t.value in ('static', 'field'):
                self.compile_classvardec()
            if t.value in ('constructor', 'function', 'method'):
                self.compile_subroutine()

    @struct('classVarDec')
    def compile_classvardec(self):
        t = self.tokens.pop()
        self.write_t(t)
        self.assert_write_next_t(value=('int', 'char', 'boolean'), _type='identifier',
            msg='a type should follow the beginning of a classVarDec')
        for t in self.tokenizer:
            if t.value == ',' or t.type == 'identifier':
                self.write_t(t)
            elif t.value == ';':
                self.write_t(t)
                break

    def compile_subroutine(self):
        pass

    def compile_parameterlist(self):
        pass

    def compile_vardec(self):
        pass

    def compile_statements(self):
        pass

    def compile_do(self):
        pass

    def compile_let(self):
        pass

    def compile_while(self):
        pass

    def compile_return(self):
        pass

    def compile_if(self):
        pass

    def compile_expression(self):
        pass

    def compile_term(self):
        pass
        # t = self.tokens.pop(0)
        # self.writeln('<{0}> {1} </{0}>'.format(t.type, escape(t.value)))

    def compile_exressionlist(self):
        pass


def get_files(name):
        if os.path.isdir(name):
            files = [os.path.join(name, f) for f in os.listdir(name)]
        else:
            files = [name]
        return [f for f in files if f.endswith('.jack')]


if __name__ == '__main__':
    name = sys.argv[1]
    files = get_files(name)

    for file in files:
        Parser(file).compile_class()
