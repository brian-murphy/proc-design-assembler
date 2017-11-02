"""Entry point for the assembler. Handles file i/o"""
import sys
from scanner.scanner import tokenize

def main():
    """Entry point"""
    input_file_name = sys.argv[1]
    output_file_name = sys.argv[2]

    assembly_text = open(input_file_name).read()

    print repr(tokenize(assembly_text))


if __name__ == '__main__':
    main()