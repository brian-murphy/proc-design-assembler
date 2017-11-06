"""Entry point for the assembler. Handles file i/o"""
import sys
from scanner.scanner import tokenize
from parser.parser import Parser

def main():
    """Entry point"""
    input_file_name = sys.argv[1]
    output_file_name = sys.argv[2]

    assembly_text = open(input_file_name).read()

    tokens = tokenize(assembly_text)

    parser = Parser(tokens)

    (instructions, symbols) = parser.parse()

    print instructions, symbols


if __name__ == '__main__':
    main()
