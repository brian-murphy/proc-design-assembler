"""This module keeps the values that represent the function codes in machine code.
They are bit shifted to what will be their final position in the instructions."""
functions = {
    "SUB": 2 << 28,
    "ADD": 3 << 28,
    "XOR": 5 << 28,
    "OR": 6 << 28,
    "AND": 7 << 28,
    "XNOR": 9 << 28,
    "NOR": 10 << 28,
    "NAND": 11 << 28,
    "MVHI": 15 << 28,

    "LW": 0 << 28,
    "SW": 0 << 28,

    "NE": 0 << 28,
    "GTE": 1 << 28,
    "LTE": 2 << 28,
    "F": 3 << 28,
    "EQ": 12 << 28,
    "LT": 13 << 28,
    "GT": 14 << 28,
    "T": 15 << 28,

    "BF": 0b0011 << 28,
    "BEQ": 0b1100 << 28,
    "BLT": 0b1101 << 28,
    "BLTE": 0b0010 << 28,
    "BEQZ": 0b1000 << 28,
    "BLTZ": 0b1001 << 28,
    "BLTEZ": 0b0110 << 28,
    "BT": 0b1111 << 28,
    "BNE": 0b0000 << 28,
    "BGTE": 0b0001 << 28,
    "BGT": 0b1110 << 28,
    "BNEZ": 0b0100 << 28,
    "BGTEZ": 0b0101 << 28,
    "BGTZ": 0b1010 << 28,

    "JAL": 0 << 28,
}