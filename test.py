import unittest
import assembler.parser as parser
from textwrap import dedent
from io import BytesIO

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
        out = parser.main(code_1)
        print out
        self.assertEqual(out, compiled_1)


if __name__ == '__main__':
    unittest.main()
