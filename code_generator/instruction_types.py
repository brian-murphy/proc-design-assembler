"""This file categorizes instructions into their various types."""

ALUR_INSTRUCTIONS = ["ADD", "SUB", "AND", "OR", "XOR", "NAND", "NOR", "XNOR", "NOT"]

ALUI_INSTRUCTIONS = ["ADDI", "SUBI", "ANDI", "ORI", "XORI", "NANDI", "NORI", "XNORI", "MVHI"]

LOAD_STORE_INSTRUCTIONS = ["LW", "SW"]

CMPR_INSTRUCTIONS = ["F", "EQ", "LT", "LTE", "T", "NE", "GTE", "GT"]

CMPI_INSTRUCTIONS = ["FI", "EQI", "LTI", "LTEI", "TI", "NEI", "GTEI", "GTI"]

BRANCH_INSTRUCTIONS = ["BF", "BEQ", "BLT", "BLTE", "BEQZ", "BLTZ", "BLTEZ", "BT", "BNE", "BGTE", \
"BGT", "BNEZ", "BGTEZ", "BGTZ", "JAL", "BR", "BLE", "BGE", "CALL", "RET", "JMP"]

PSEUDO_INSTRUCTIONS = ["BR", "NOT", "BLE", "BGE", "CALL", "RET", "JMP"]
