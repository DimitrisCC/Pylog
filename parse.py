# Dimaki Georgia 3130052
# Kolokathi Fotini 3090088
# Papatheodorou Dimitris 3130162
#########################################################

# parse.py


ALPHABET = 'abcdefghijklmnopqrstuvwxyz'
NUMBERS = '0123456789'
EOF = 'EOF'
ENDLINE = '\n'
WHITESPACES = (' ', '\t', '\n')


class Lexer:
    def __init__(self, line):
        self.line = line  # the line to analyze
        self.pos = 0  # the current position in the line
        self.char = line[self.pos]  # the current character of the line analysis

    def is_whitespace(self):
        return self.char in WHITESPACES

    def is_number(self):
        return self.char in NUMBERS

    def is_letter(self):
        return self.char in ALPHABET or self.char in ALPHABET.upper()

    def consume(self):
        self.pos += 1
        if self.pos >= len(self.line):
            self.char = EOF
        else:
            self.char = self.line[self.pos]
        return self.char

    def is_comment(self):
        return self.char == '%'

    def consume_comment(self):
        while self.char != ENDLINE:
            self.consume()

# class Parser:
