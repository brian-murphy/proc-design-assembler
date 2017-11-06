"""This file categorizes instructions according to the format of their parameters"""

RRR_INSTRUCTIONS = ["ADD", "SUB", "AND", "OR", "XOR", "NAND", "NOR", "XNOR", "F", "EQ", "LT", \
                    "LTE", "T", "NE", "GTE", "GT"]

IRR_INSTRUCTIONS = ["ADDI", "SUBI", "ANDI", "ORI", "XORI", "NANDI", "NORI", "XNORI", "FI", "EQI", \
                    "LTI", "LTEI", "TI", "NEI", "GTEI", "GTI", "BF", "BEQ", "BLT", "BLTE", "BT", \
                    "BNE", "BGTE", "BGT", "BLE", "BGE"]

IR_INSTRUCTIONS = ["MVHI", "BEQZ", "BLTZ", "BLTEZ", "BNEZ", "BGTEZ", "BGTZ"]

I_PARENR_R_INSTRUCTIONS = ["LW", "SW", "JAL"]

I_INSTRUCTIONS = ["BR"]

RR_INSTRUCTIONS = ["NOT"]

I_PARENR_INSTRUCTIONS = ["CALL", "JMP"]

NO_ARG_INSTRUCTIONS = ["RET"]

INSTRUCTION_TYPES = {
    'ADD': "RRR",
    'SUB': "RRR",
    'AND': "RRR",
    'OR': "RRR",
    'XOR': "RRR",
    'NAND': "RRR",
    'NOR': "RRR",
    'XNOR': "RRR",
    'F': "RRR",
    'EQ': "RRR",
    'LT': "RRR",
    'LTE': "RRR",
    'T': "RRR",
    'NE': "RRR",
    'GTE': "RRR",
    'GT': "RRR",
    "ADDI": "IRR",
    "SUBI": "IRR",
    "ANDI": "IRR",
    "ORI": "IRR",
    "XORI": "IRR",
    "NANDI": "IRR",
    "NORI": "IRR",
    "XNORI": "IRR",
    "FI": "IRR",
    "EQI": "IRR",
    "LTI": "IRR",
    "LTEI": "IRR",
    "TI": "IRR",
    "NEI": "IRR",
    "GTEI": "IRR",
    "GTI": "IRR",
    "BF": "IRR",
    "BEQ": "IRR",
    "BLT": "IRR",
    "BLTE": "IRR",
    "BT": "IRR",
    "BNE": "IRR",
    "BGTE": "IRR",
    "BGT": "IRR",
    "BLE": "IRR",
    "BGE": "IRR",
    "MVHI": "IR",
    "BEQZ": "IR",
    "BLTZ": "IR",
    "BLTEZ": "IR",
    "BNEZ": "IR",
    "BGTEZ": "IR",
    "BGTZ": "IR",
    "LW": "I(R)R",
    "SW": "I(R)R",
    "JAL": "I(R)R",
    "BR": "I",
    "NOT": "RR",
    "CALL": "I(R)",
    "JMP": "I(R)",
    "RET": "NO_ARG",
 }
