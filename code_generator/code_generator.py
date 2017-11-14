"""code_generator converts an intermediate representation into a mif file format text"""
from instruction_types import ALUI_INSTRUCTIONS, ALUR_INSTRUCTIONS, BRANCH_INSTRUCTIONS, \
CMPI_INSTRUCTIONS, CMPR_INSTRUCTIONS, LOAD_STORE_INSTRUCTIONS, IRR_BRANCHES, IR_BRANCHES

from functions import functions
import opcodes

WORD_WIDTH = 32
RAM_DEPTH = 2048

class CodeGenerator:

    def __init__(self, instructions):
        self.instructions = instructions
        self.text = ""

    def mif_format(self):
        self.text = self.mif_header(WORD_WIDTH, RAM_DEPTH)
        self.encode_instructions_mif(self.instructions)
        self.text += self.mif_footer()
        return self.text

    def mif_header(self, word_width, ram_depth):
        return "WIDTH=" + str(word_width) + ";\nDEPTH=" + str(ram_depth) + \
        ";\nADDRESS_RADIX=HEX;\nDATA_RADIX=HEX;\nCONTENT BEGIN\n"

    def encode_instructions_mif(self, instructions):
        noop_start = 0
        is_accumulating_noops = False
        for addr in range(0, RAM_DEPTH - 1, 4):
            if addr in instructions:
                if is_accumulating_noops:
                    self.write_noops(noop_start, addr - 1)
                    is_accumulating_noops = False
                self.write_word(addr, instructions[addr])
            else:
                if not is_accumulating_noops:
                    noop_start = addr
                    is_accumulating_noops = True
        if is_accumulating_noops:
            self.write_noops(noop_start, RAM_DEPTH - 1)

    def write_noops(self, noop_start, last_noop):
        # NOOP is ADD R9,R9,R9
        self.text += "[" + to_hex(noop_start) + ".." + to_hex(last_noop) + "] : 3f000999;\n"


    def write_word(self, addr, instruction):
        instr_name = instruction[0]
        encoded_instr = None
        if instr_name == ".WORD":
            encoded_instr = instruction[1]

        elif instr_name in ALUR_INSTRUCTIONS:
            encoded_instr = make_alur_fn_and_op(instr_name) | make_rrr_args(instruction)

        elif instr_name in ALUI_INSTRUCTIONS:
            if instr_name == "MVHI":
                encoded_instr = make_alui_fn_and_op(instr_name) | make_mvhi_args(instruction)
            else:
                encoded_instr = make_alui_fn_and_op(instr_name) | make_irr_args(instruction)

        elif instr_name in LOAD_STORE_INSTRUCTIONS:
            encoded_instr = make_loadstore_fn_and_op(instr_name) | make_loadstore_args(instruction)

        elif instr_name in CMPR_INSTRUCTIONS:
            encoded_instr = make_cmpr_fn_and_op(instr_name) | make_rrr_args(instruction)

        elif instr_name in CMPI_INSTRUCTIONS:
            encoded_instr = make_cmpi_fn_and_op(instr_name) | make_irr_args(instruction)

        elif instr_name in BRANCH_INSTRUCTIONS:
            if instr_name in IRR_BRANCHES:
                encoded_instr = make_branch_fn_and_op(instr_name) | make_irr_args(instruction)
            elif instr_name in IR_BRANCHES:
                encoded_instr = make_branch_fn_and_op(instr_name) | make_ir_args(instruction)
            else:
                raise RuntimeError("couldn't recognize branch arg type")

        self.write_at_addr(addr, encoded_instr)

    def write_at_addr(self, addr, number):
        self.text += to_hex(addr) + " : " + to_hex(number) + ";\n"

    def mif_footer(self):
        return "END;\n"

def to_hex(number):
    return hex(number & 0xffffffff)[2:]

def make_alur_fn_and_op(instr_name):
    return functions[instr_name] | opcodes.ALUR

def make_rrr_args(instruction):
    r_2 = encode_reg(instruction[1])
    r_1 = encode_reg(instruction[2])
    r_d = encode_reg(instruction[3])
    return (r_2 << 8) | (r_1 << 4) | r_d

def encode_reg(reg_string):
    return int(reg_string[1:])

def make_alui_fn_and_op(instr_name):
    if instr_name == "MVHI":
        return functions[instr_name] | opcodes.ALUI
    else:
        return functions[instr_name[0:-1]] | opcodes.ALUI

def make_irr_args(instruction):
    imm = instruction[1]
    r_1 = encode_reg(instruction[2])
    r_d = encode_reg(instruction[3])
    return (imm << 8) | (r_1 << 4) | r_d

def make_mvhi_args(instruction):
    imm = instruction[1]
    r_1 = encode_reg(instruction[2])
    return (imm << 8) | (r_1 << 4)

def make_loadstore_fn_and_op(instr_name):
    operation = None
    if instr_name == "LW":
        operation = opcodes.LW
    elif instr_name == "SW":
        operation = opcodes.SW
    else:
        raise RuntimeError("Couldn't recognize instruction name when encoding loadstore fn and op")
    return operation | functions[instr_name]

def make_loadstore_args(instruction):
    imm = instruction[1]
    r_1 = encode_reg(instruction[2])
    r_2 = encode_reg(instruction[3])
    return (imm << 8) | (r_1 << 4) | r_2

def make_cmpr_fn_and_op(instr_name):
    return functions[instr_name] | opcodes.ALUR

def make_cmpi_fn_and_op(instr_name):
    return functions[instr_name[0:-1]] | opcodes.CMPI

def make_branch_fn_and_op(instr_name):
    opcode = None
    if instr_name == "JAL":
        opcode = opcodes.JAL
    else:
        opcode = opcodes.BRANCH
    return functions[instr_name] | opcode

def make_ir_args(instruction):
    imm = instruction[1]
    r_1 = encode_reg(instruction[2])
    return (imm << 8) | r_1
