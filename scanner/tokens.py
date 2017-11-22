"""All tokens possible in assembly file. They are represented as a tuple
where the the first entry is a name for the token, and the second entry is
a regex that will match the token. They are mostly sorted by type, but the
scanner needs implement longest-match-first, so some tokens are outside
their category"""

LEXICALLY_DISTINCT_TOKENS = [("whitespace", "\s"),
              ("comment", ";.*"),

              #directives
              (".NAME", ".NAME"),
              (".ORIG", ".ORIG"),
              (".WORD", ".WORD"),

              #punctuation
              ("=", "="),
              (",", ","),
              ("(", "\("),
              (")", "\)"),
              (":", ":"),

              #registers with numbers in names
              ("R0", "(?:R0)|(?:A0)"),
              ("R10", "R10"),
              ("R11", "R11"),
              ("R12", "R12"),
              ("R13", "R13"),
              ("R14", "R14"),
              ("R15", "R15"),
              ("R1", "(?:R1)|(?:A1)"),
              ("R2", "(?:R2)|(?:A2)"),
              ("R3", "(?:R3)|(?:A3)|(?:RV)"),
              ("R4", "(?:R4)|(?:T0)"),
              ("R5", "(?:R5)|(?:T1)"),
              ("R6", "(?:R6)|(?:S0)"),
              ("R7", "(?:R7)|(?:S1)"),
              ("R8", "(?:R8)|(?:S2)"),
              ("R9", "R9"),

              #numbers, symbols, and catch-all
              ("number", "(?:0[xX][0-9A-Fa-f]{1,})|(?:-?[1-9][0-9]*)|(?:0)"),
              ("symbol", "[a-zA-Z]{1,}"),
              ("no_match", ".{1,}")]


KEYWORD_TOKENS = [("R13","FP"),# need to match FP before instruction F

            #instructions
            ("ADDI","ADDI"),
            ("SUBI","SUBI"),
            ("ANDI","ANDI"),
            ("ORI","ORI"),
            ("XORI","XORI"),
            ("NANDI","NANDI"),
            ("NORI","NORI"),
            ("XNORI","XNORI"),
            ("MVHI","MVHI"),
            ("ADD", "ADD"),
            ("SUB", "SUB"),
            ("AND", "AND"),
            ("OR", "OR"),
            ("XOR", "XOR"),
            ("NAND", "NAND"),
            ("NOR", "NOR"),
            ("XNOR", "XNOR"),
            ("LW","LW"),
            ("SW","SW"),
            ("F","F"),
            ("EQI","EQI"),
            ("LTI","LTI"),
            ("LTEI","LTEI"),
            ("TI","TI"),
            ("NEI","NEI"),
            ("GTEI","GTEI"),
            ("GTI","GTI"),
            ("EQ","EQ"),
            ("LTE","LTE"),
            ("LT","LT"),
            ("T","T"),
            ("NE","NE"),
            ("GTE","GTE"),
            ("GT","GT"),
            ("BF","BF"),
            ("BEQZ","BEQZ"),
            ("BEQ","BEQ"),
            ("BLTEZ","BLTEZ"),
            ("BLTE","BLTE"),
            ("BLTZ","BLTZ"),
            ("BLT","BLT"),
            ("BT","BT"),
            ("BNEZ","BNEZ"),
            ("BNE","BNE"),
            ("BGTEZ","BGTEZ"),
            ("BGTE","BGTE"),
            ("BGTZ","BGTZ"),
            ("BGT","BGT"),
            ("JAL","JAL"),
            ("NOT","NOT"),
            ("BLE","BLE"),
            ("BGE","BGE"),
            ("BR","(?:BR)|(?:B)"),
            ("CALL","CALL"),
            ("RET","RET"),
            ("JMP","JMP"),

              #registers
            ("R12", "GP"),
            ("R14", "SP"),
            ("R15", "RA")]
