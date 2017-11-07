"""This module keeps the values that represent the opcodes in machine code.
They are bit shifted to what will be their final position in the instructions."""

ALUR = 0b1111 << 24
ALUI = 0b1011 << 24
LW = 0b1000 << 24
SW = 0b1001 << 24
CMPR = 0b1110 << 24
CMPI = 0b1010 << 24
BRANCH = 0 << 24
JAL = 0b0001 << 24
