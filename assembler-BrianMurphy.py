"""Entry point for the assembler. Handles file i/o"""
import sys
from scanner.scanner import tokenize
from parser.parser import Parser
from code_generator.code_generator import CodeGenerator

def main():
    """Entry point"""
    input_file_name = sys.argv[1]
    output_file_name = sys.argv[2]

    input_file = open(input_file_name, "r")
    assembly_text = input_file.read()
    input_file.close()

    try:
        tokens = tokenize(assembly_text)

        parser = Parser(tokens)
        instructions = parser.parse()

        code_gen = CodeGenerator(instructions)
        mif_text = code_gen.mif_format()

        output_file = open(output_file_name, "w")
        output_file.write(mif_text)
        output_file.close()

    except RuntimeError as err:
        print err.message




if __name__ == '__main__':
    main()
