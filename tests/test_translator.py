import unittest
from vm_translator.parser import Parser
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
        cmd = 'push local 1'
        eq_(parser.arg1(cmd), 'local')

    def test_get_2nd_arg(self):
        '''Test getting the 2nd arg of a command'''
        parser = Parser(code_1)
        cmd = 'push local 1'
        eq_(parser.arg2(cmd), '1')


if __name__ == '__main__':
    unittest.main()
