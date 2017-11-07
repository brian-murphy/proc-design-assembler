"""Scans input files for tokens"""
import re

from tokens import LEXICALLY_DISTINCT_TOKENS, KEYWORD_TOKENS


def tokenize(file_text):
    """converts a file's text into a list of tokens"""

    text_all_caps = file_text.upper()

    lexical_re = re.compile(make_regex_string(LEXICALLY_DISTINCT_TOKENS))
    keyword_re = re.compile(make_regex_string(KEYWORD_TOKENS))

    line_number = 1
    tokens = []
    pos = 0

    while pos < len(text_all_caps):
        lexical_match = lexical_re.match(text_all_caps, pos)

        token_type = LEXICALLY_DISTINCT_TOKENS[lexical_match.lastindex - 1][0]
        token_text = str(lexical_match.group(lexical_match.lastindex))

        if token_type == "no_match":
            raise RuntimeError("Lexical error when on line " + str(line_number) + \
            ". No match for \"" + token_text + "\"")

        elif token_type == "whitespace":
            if token_text == "\n":
                line_number += 1

        elif token_type == "symbol":
            # check if text is keyword
            keyword_match = keyword_re.match(token_text, 0)
            if keyword_match and keyword_match.end() == len(token_text):
                token_type = KEYWORD_TOKENS[keyword_match.lastindex - 1][0]

            tokens.append((token_type, token_text, line_number))

        elif token_type != "whitespace" and token_type != "comment":
            tokens.append((token_type, token_text, line_number))

        pos = lexical_match.end()

    return tokens


def make_regex_string(tokens):
    """forms the regular expression to tokenize the language"""

    def make_token_regex(token):
        return "(" + token[1] + ")"

    token_regexes = map(make_token_regex, tokens)

    return "|".join(token_regexes)
