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
0000000000010000
0000000000010001
1110101110111000
1110000111111010
0000000000010010
1111010011111111
0000000000010011""")


class tests(unittest.TestCase):

    def test_1(self):
        out = parser.main(code_1)
        print out
        self.assertEqual(out, compiled_1)


if __name__ == '__main__':
    unittest.main()
