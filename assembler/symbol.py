
predefined = {
    'SP': 0,
    'LCL': 1,
    'ARG': 2,
    'THIS': 3,
    'THAT': 4,
    'R1': 1,
    'R2': 2,
    'R3': 3,
    'R4': 4,
    'R5': 5,
    'R6': 6,
    'R7': 7,
    'R8': 8,
    'R9': 9,
    'R11': 11,
    'R12': 12,
    'R13': 13,
    'R14': 14,
    'R15': 15,
    'SCREEN': 16834,
    'KBD': 24576
}



class Symbol_Table():
    def __init__(self):
        self.table = predefined

    def add_entry(self, symbol, address):
        self.table[symbol] = address

    def contains(self, symbol):
        return symbol in self.table

    def get_address(self, symbol):
        if symbol in self.table:
            return self.table[symbol]
        else:
            return symbol


if __name__ == '__main__':
    st = Symbol_Table()
    st.add_entry('test', 5)
    st.add_entry('test2', 2)
    st.contains('test')
    print st.contains('test')
    print st.get_address('test2')
