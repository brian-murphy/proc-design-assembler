"""Scans input files for tokens"""
import re

from tokens import ALL_TOKENS


def tokenize(file_text):
    """converts a file's text into a list of tokens"""

    pattern = re.compile(make_regex_string(ALL_TOKENS))

    tokens = []
    pos = 0

    while 1:
        m = pattern.match(file_text, pos)
        if pos == len(file_text):
            break

        token_type = ALL_TOKENS[m.lastindex - 1][0]
        token_text = repr(m.group(m.lastindex))

        if token_type == "no_match":
            raise RuntimeError("Lexical error when scanning assembly. No match for \"" + token_text + "\"")
        elif token_type != "whitespace" and token_type != "comment":
            tokens.append((token_type, token_text))
            print token_type, token_text

        pos = m.end()

    return tokens


def make_regex_string(tokens):
    """forms the regular expression to tokenize the language"""

    def make_token_regex(token):
        return "(" + token[1] + ")"

    token_regexes = map(make_token_regex, tokens)

    return "|".join(token_regexes)
