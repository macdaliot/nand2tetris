import sys
import parser

in_filename = sys.argv[1]
out_filename = sys.argv[1].rpartition('.')[0] + '.hack'

in_file = open(in_filename)
out_file = open(out_filename, 'w')

compiled = parser.main(in_file)
out_file.writelines(compiled)
