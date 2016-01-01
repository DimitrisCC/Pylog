# Dimaki Georgia 3130052
# Kolokathi Fotini 3090088
# Papatheodorou Dimitris 3130162
#########################################################

# parse.py

from logic import *

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

    def is_alpharethmetic(self):
        return self.is_letter() or self.is_number()

    def get_identifier(self):
        identifier = ''
        identifier += self.consume()
        if self.is_letter():
            raise "Not a correct identifier"
        identifier += self.consume()
        while self.is_alpharethmetic():
            identifier += self.consume()
        return identifier

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

    def is_if(self):
        if self.consume() == ':':
            if self.consume() == '-':
                return True
        return False

    def next_char(self):
        if self.pos + 1 > len(self.line) :
            return EOF
        else:
            return self.line[self.pos + 1]

    def isEndOfTerm(self, char):
        return char == ')' or char == ']'

# class Parser:

    # it parses only one line
    # to parse multiple lines (in a file maybe) run this until it returns EOF
    # no checking for invalid input is done but it maybe could
    def parse_line(self):
        token = ''
        self.char = ''
        term = None
        while self.char != EOF or self.char != ENDLINE:
            if self.char == '(':
                #  the you have a relation so a Relation must be created
                args = []
                while self.char != ")":
                    args.append(self.parse_line())
                term = Relation(name=token, body=args)

            elif self.char == ',' or self.isEndOfTerm(self.next_char()):
                # you probably have an argument for either a relation, a clause or a list
                # generally you have to return what u created already
                if not term:  # term is None ---> maybe check for correct line or sth
                    if token.isupper():  # then it is a variable
                        term = Variable(name=token)
                    else:
                        # the you have just a term (if it was not just a term you would have entered
                        term = Term(name=token)
                # else you have already created a list or a relation
                return term

                # elif self.char == '[':
                # list
            elif self.is_if():
                # create clause
                args = []

                while self.next_char() != ENDLINE or self.next_char() != EOF:
                    args.append(self.parse_line())

                term = Clause(head=token, body=args)
            else:
                # now you can just create the next word
                token += self.consume()

        # eof occurred
        # if term is not assigned to sth you must deal with the token first, create the term and then return it
        if not term:  # term is None ---> maybe check for correct line or sth
            if token == '':
                if self.char == ENDLINE:
                    return ENDLINE
                elif self.char == EOF:
                    return EOF
                else: return False

            if token.isupper():  # then it is a variable
                term = Variable(name=token)
            else:
                # the you have just a term (if it was not just a term you would have entered
                term = Term(name=token)
        return term
