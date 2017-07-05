import unittest
import assembler.parser as parser
from assembler.symbol import Symbol_Table
from textwrap import dedent
from io import BytesIO
from nose.tools import *

code_1 = BytesIO("""
(START)
@1
@arg
D=M+1
1;JEQ
@0
(TEST)
AM=D+1;JMP
@156
(END)""")

compiled_1 = dedent("""\
0000000000000001
0000000000010000
1111110111010000
1110111111000010
0000000000000000
1110011111101111
0000000010011100""")


class tests(unittest.TestCase):

    def test_1(self):
        '''Test parser'''
        out = parser.main(code_1)
        print out
        self.assertEqual(out, compiled_1)


class symbol_tests(unittest.TestCase):

    def test_symbols(self):
        '''Test Symbol_Table'''
        st = Symbol_Table()
        st.add_entry('test', 5)
        st.add_entry('test2', 2)
        ok_(st.contains('test'))
        eq_(st.get_address('test2'), 2)


if __name__ == '__main__':
    unittest.main()
