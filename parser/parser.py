"""This module handles parsing the assembly into an intermediate representation
that can be used to generate machine code."""
from numbers import Number

from instruction_formats import RRR_INSTRUCTIONS, IRR_INSTRUCTIONS, IR_INSTRUCTIONS, I_PARENR_R_INSTRUCTIONS, \
I_INSTRUCTIONS, RR_INSTRUCTIONS, I_PARENR_INSTRUCTIONS, NO_ARG_INSTRUCTIONS

from code_generator.instruction_types import BRANCH_INSTRUCTIONS

REGS = ["R0", "R1", "R2", "R3", "R4", "R5", "R6", "R7", "R8", "R9", "R10", "R11", "R12", \
        "R13", "R14", "R15"]

PSEUDO_INSTRUCTIONS = ["BR", "NOT", "BLE", "BGE", "CALL", "RET", "JMP"]

class Parser:

    def __init__(self, tokens):
        self.parse_index = 0
        self.current_address = 0x0
        self.instructions = {}
        self.symbols = {}
        self.tokens = tokens


    def add_symbol(self, name, value):
        if name in self.symbols:
            raise RuntimeError("Cannot redefine symbol \"" + name + "\"")
        else:
            self.symbols[name] = value

    def add_word(self, word):
        if self.current_address in self.instructions:
            raise RuntimeError("Improper use of .ORIG. Instructions or words overlap")
        else:
            self.instructions[self.current_address] = word
            self.current_address = self.current_address + 4


    def parse(self):
        """converts a list of tokens into an intermediate representation"""
        self.instructions.clear()
        self.symbols.clear()
        self.parse_index = 0
        self.current_address = 0x0

        self.first_pass(self.tokens)
        self.second_pass()

        return self.instructions


    def first_pass(self, tokens):
        """iterates over the list of tokens and identifies instructions and symbols.
        Both of these data structures should be populated when this returns. Also
        converts pseudo-instructions to machine instructions"""

        while self.parse_index < len(tokens):
            token_type = tokens[self.parse_index][0]

            if token_type == ".ORIG":
                self.orig(tokens)

            elif token_type == ".NAME":
                self.name(tokens)

            elif token_type == ".WORD":
                self.word(tokens)

            elif token_type == "symbol":
                self.label(tokens)

            elif token_type in RRR_INSTRUCTIONS:
                self.rrr_instruction(tokens)

            elif token_type in IRR_INSTRUCTIONS:
                self.irr_instruction(tokens)

            elif token_type in IR_INSTRUCTIONS:
                self.ir_instruction(tokens)

            elif token_type in I_PARENR_R_INSTRUCTIONS:
                self.i_parenr_r_instruction(tokens)

            elif token_type in I_INSTRUCTIONS:
                self.i_instruction(tokens)

            elif token_type in RR_INSTRUCTIONS:
                self.rr_instruction(tokens)

            elif token_type in I_PARENR_INSTRUCTIONS:
                self.i_parenr_instruction(tokens)

            elif token_type in NO_ARG_INSTRUCTIONS:
                self.no_arg_instruction(tokens)

            else:
                raise RuntimeError("unrecognized way to start a statement")


    def orig(self, tokens):
        next_token_type = tokens[self.parse_index + 1][0]
        next_token_value = tokens[self.parse_index + 1][1]
        if next_token_type == "number":
            self.current_address = parse_int(next_token_value)
            self.parse_index += 2
        else:
            raise RuntimeError(".ORIG statement must be followed by a number")

    def name(self, tokens):
        symbol_token = tokens[self.parse_index + 1]
        value_token = tokens[self.parse_index + 3]
        if symbol_token[0] == "symbol" and tokens[self.parse_index + 2][0] == "=" \
        and value_token[0] == "number":
            self.add_symbol(symbol_token[1], parse_int(value_token[1]))
            self.parse_index += 4
        else:
            raise RuntimeError(".NAME statement must be followed by \"=<number>\"")

    def word(self, tokens):
        next_token_type = tokens[self.parse_index + 1][0]
        next_token_value = tokens[self.parse_index + 1][1]
        if next_token_type == "number":
            self.add_word((".WORD", parse_int(next_token_value)))
            self.parse_index += 2
        elif next_token_type == "symbol":
            self.add_word((".WORD", next_token_value))
            self.parse_index += 2
        else:
            raise RuntimeError(".WORD statement must be followed by a number or a symbol")

    def label(self, tokens):
        next_token_type = tokens[self.parse_index + 1][0]
        label_name = tokens[self.parse_index][1]
        if next_token_type == ":":
            self.add_symbol(label_name, self.current_address)
            self.parse_index += 2
        else:
            raise RuntimeError("unexpected symbol \"" + label_name + \
            "\". Labels should be followed by :")

    def rrr_instruction(self, tokens):
        assert_commas(tokens[self.parse_index + 2], tokens[self.parse_index + 4])
        r1_token = tokens[self.parse_index + 1]
        r2_token = tokens[self.parse_index + 3]
        r3_token = tokens[self.parse_index + 5]
        assert_regs(r1_token, r2_token, r3_token)
        instr_name = tokens[self.parse_index][0]
        self.add_word((instr_name, r1_token[0], r2_token[0], r3_token[0]))
        self.parse_index += 6

    def irr_instruction(self, tokens):
        assert_commas(tokens[self.parse_index + 2], tokens[self.parse_index + 4])
        r1_token = tokens[self.parse_index + 3]
        r2_token = tokens[self.parse_index + 5]
        assert_regs(r1_token, r2_token)
        instr_name = tokens[self.parse_index][0]
        imm_token = tokens[self.parse_index + 1]
        imm_value = None
        if imm_token[0] == "number":
            imm_value = parse_int(imm_token[1])
        elif imm_token[0] == "symbol":
            imm_value = imm_token[1]
        else:
            raise RuntimeError("imm must be a number or a label")
        if instr_name == "BLE":
            self.add_word(("LTE", r1_token[0], r2_token[0], "R9"))
            self.add_word(("BNEZ", imm_value, "R9"))
        elif instr_name == "BGE":
            self.add_word(("GTE", r1_token[0], r2_token[0], "R9"))
            self.add_word(("BNEZ", imm_value, "R9"))
        else:
            self.add_word((instr_name, imm_value, r1_token[0], r2_token[0]))
        self.parse_index += 6


    def ir_instruction(self, tokens):
        assert_commas(tokens[self.parse_index + 2])
        r1_token = tokens[self.parse_index + 3]
        assert_regs(r1_token)
        instr_name = tokens[self.parse_index][0]
        imm_token = tokens[self.parse_index + 1]
        if imm_token[0] == "number":
            self.add_word((instr_name, parse_int(imm_token[1]), r1_token[0]))
            self.parse_index += 4
        elif imm_token[0] == "symbol":
            self.add_word((instr_name, imm_token[1], r1_token[0]))
            self.parse_index += 4
        else:
            raise RuntimeError("imm must be a number or a label")

    def i_parenr_r_instruction(self, tokens):
        assert_parens(tokens[self.parse_index + 2], tokens[self.parse_index + 4])
        assert_commas(tokens[self.parse_index + 5])
        r1_token = tokens[self.parse_index + 3]
        r2_token = tokens[self.parse_index + 6]
        assert_regs(r1_token, r2_token)
        instr_name = tokens[self.parse_index][0]
        imm_token = tokens[self.parse_index + 1]
        if imm_token[0] == "number":
            self.add_word((instr_name, parse_int(imm_token[1]), r1_token[0], r2_token[0]))
            self.parse_index += 7
        elif imm_token[0] == "symbol":
            self.add_word((instr_name, imm_token[1], r1_token[0], r2_token[0]))
            self.parse_index += 7
        else:
            raise RuntimeError("imm must be a number or a label")

    def i_instruction(self, tokens):
        instr_name = tokens[self.parse_index][0]
        imm_token = tokens[self.parse_index + 1]
        imm_value = None
        if imm_token[0] == "number":
            imm_value = parse_int(imm_token[1])
        elif imm_token[0] == "symbol":
            imm_value = imm_token[1]
        else:
            raise RuntimeError("imm must be a number or a label")
        if instr_name == "BR":
            self.add_word(("BEQ", imm_value, "R9", "R9"))
        else:
            self.add_word((instr_name, imm_value))
        self.parse_index += 2

    def rr_instruction(self, tokens):
        assert_commas(tokens[self.parse_index + 2])
        r1_token = tokens[self.parse_index + 1]
        r2_token = tokens[self.parse_index + 3]
        assert_regs(r1_token, r2_token)
        instr_name = tokens[self.parse_index][0]
        if instr_name == "NOT":
            self.add_word(("NAND", r1_token[0], r1_token[0], r2_token[0]))
        else:
            self.add_word((instr_name, r1_token[0], r2_token[0]))
        self.parse_index += 4

    def i_parenr_instruction(self, tokens):
        assert_parens(tokens[self.parse_index + 2], tokens[self.parse_index + 4])
        r1_token = tokens[self.parse_index + 3]
        assert_regs(r1_token)
        instr_name = tokens[self.parse_index][0]
        imm_token = tokens[self.parse_index + 1]
        imm_value = None
        if imm_token[0] == "number":
            imm_value = parse_int(imm_token[1])
        elif imm_token[0] == "symbol":
            imm_value = imm_token[1]
        else:
            raise RuntimeError("imm must be a number or a label")
        if instr_name == "CALL":
            self.add_word(("JAL", imm_value, r1_token[0], "R15"))
        elif instr_name == "JMP":
            self.add_word(("JAL", imm_value, r1_token[0], "R9"))
        else:
            self.add_word((instr_name, imm_token[1], r1_token[0]))
        self.parse_index += 5


    def no_arg_instruction(self, tokens):
        instr_name = tokens[self.parse_index][0]
        if instr_name == "RET":
            self.add_word(("JAL", "R15", "R9"))
        else:
            self.add_word((instr_name,))
        self.parse_index += 1

    def print_token_stream(self, tokens, span):
        for i in range(self.parse_index - span, self.parse_index + span):
            if i > 0 and i < len(tokens):
                print tokens[i][0], tokens[i][1]


    def second_pass(self):
        """Iterates over the parsed instructions and replaces symbolic
        immediate values with the correct numeric ones."""
        complete_instructions = {}

        for address in self.instructions.iterkeys():
            instruction = self.instructions[address]
            instruction_type = instruction[0]
            for i in range(1, len(instruction)):
                if not instruction[i] in REGS and not isinstance(instruction[i], Number):
                    instr_list = list(instruction)
                    instr_list[i] = self.symbol_imm_value(instruction_type, instruction[i], address)
                    complete_instructions[address] = tuple(instr_list)

        for address in complete_instructions.iterkeys():
            self.instructions[address] = complete_instructions[address]

    def symbol_imm_value(self, instruction_type, symbol, instruction_address):
        symbol_value = self.symbols[symbol]
        if instruction_type in BRANCH_INSTRUCTIONS:
            return ((symbol_value - instruction_address) / 4) - 1
        else:
            return symbol_value



def assert_commas(*comma_tokens):
    for token in comma_tokens:
        if token[0] != ",":
            raise RuntimeError("operands must be separated by commas")

def assert_regs(*reg_tokens):
    for token in reg_tokens:
        if not token[0] in REGS:
            raise RuntimeError("operands must be regs")

def assert_parens(*paren_tokens):
    for token in paren_tokens:
        if token[0] != "(" and token[0] != ")":
            raise RuntimeError("index reg must be wrapped in parens")

def parse_int(int_string):
    if int_string.find("0x") != -1 or int_string.find("0X") != -1:
        return int(int_string, 16)
    else:
        return int(int_string)
