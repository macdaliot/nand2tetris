import unittest
from vm_translator.parser import Parser, UnknownCmdError
from vm_translator.code_writer import *
from io import BytesIO
from nose.tools import *

code_1 = BytesIO("""
push local 1
pop local 2
push this 3 // test comment
add
gt this that""")

blank_lines = BytesIO("""

""")

comments = BytesIO("""
// a comment
an inline comment // commented
""")


class test_parser(unittest.TestCase):

    def test_parser(self):
        '''Test vm translator parser'''
        parser = Parser(code_1)
        parser.parse()

    def test_skip_blank_lines(self):
        parser = Parser(blank_lines)
        self.assertRaises(StopIteration, parser.parse().next)

    def test_skip_comments(self):
        parser = Parser(comments)
        eq_(parser.parse().next(), 'an inline comment ')

    def test_get_1st_arg(self):
        '''Test getting the 1st arg of a command'''
        parser = Parser(code_1)
        eq_(parser.arg1('push local 1'), 'local')
        eq_(parser.arg1('add'), 'add')

    def test_get_1st_arg_from_return(self):
        '''Test getting the 1st arg of return command'''
        parser = Parser(code_1)
        self.assertRaises(AssertionError, parser.arg1, 'return')

    def test_get_2nd_arg(self):
        '''Test getting the 2nd arg of a command'''
        parser = Parser(code_1)
        eq_(parser.arg2('push local 1'), '1')

    def test_unknown_command(self):
        '''Raises error when passed unknown command type'''
        parser = Parser()
        self.assertRaises(UnknownCmdError, parser.command_type, 'blah')

    def test_command_type_arithmetic(self):
        '''Test getting command type of arithmetic commands'''
        parser = Parser(code_1)
        eq_(parser.command_type('add'), 'C_ARITHMETIC')
        eq_(parser.command_type('sub'), 'C_ARITHMETIC')
        eq_(parser.command_type('neg'), 'C_ARITHMETIC')
        eq_(parser.command_type('eq'), 'C_ARITHMETIC')
        eq_(parser.command_type('gt'), 'C_ARITHMETIC')
        eq_(parser.command_type('lt'), 'C_ARITHMETIC')
        eq_(parser.command_type('and'), 'C_ARITHMETIC')
        eq_(parser.command_type('or'), 'C_ARITHMETIC')
        eq_(parser.command_type('not'), 'C_ARITHMETIC')


class test_code_writer(unittest.TestCase):

    def test_make_push(self):
        writer = CodeWriter()
        eq_(writer.make_push('push', 'local', 5),
            ['@local', 'D=M'])


if __name__ == '__main__':
    unittest.main()
