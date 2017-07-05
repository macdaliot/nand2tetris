import unittest
from vm_translator.parser import Parser
from io import BytesIO
from nose.tools import *

code_1 = BytesIO("""
push local 1
pop local 2
push this 3
add
gt this that
""")


class tests(unittest.TestCase):

    def test_1(self):
        '''Test vm translator parser'''
        out = Parser(code_1)
        print out


if __name__ == '__main__':
    unittest.main()
