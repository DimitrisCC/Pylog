# Dimaki Georgia 3130052
# Kolokathi Fotini 3090088
# Papatheodorou Dimitris 3130162
#########################################################

# parse.py
import logic

ALPHABET = 'abcdefghijklmnopqrstuvwxyz'
NUMBERS = '0123456789'
EOF = 'EOF'
ENDLINE = '\n'
WHITESPACES = (' ', '\t', '\n')
error = "wrong command"


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
        if self.char == ':':
            self.consume()
            if self.char == '-':
                self.consume()
                return True
            else:
                return error
        return False

    def next_char(self):
        if self.pos + 1 > len(self.line) - 1:
            return EOF
        else:
            return self.line[self.pos + 1]

    def is_end_of_term(self, char):
        return char == ')' or char == ']'

    # class Parser:

    # it parses only one line
    # to parse multiple lines (in a file maybe) run this until it returns EOF
    # no checking for invalid input is done but it maybe could
    def parse_line(self):
        # print("**********************")
        token = ''
        term = None

        while self.char != '.' and self.char != EOF and self.char != ENDLINE:
            # an evaza edw consume 8a t ekane 2 fores! mia gia ton ena elegxo kai mia gia ton allo
            if self.char == ' ':
                self.consume()
                continue
            elif self.is_comment():
                self.consume_comment()  # an dn exei ENDLINE? prosoxi...
            elif self.char == '(':  # relation case
                # print("in relation")
                args = []
                while self.consume() != ')':  # exei katanalw8ei?
                    #print(self.char)
                    if self.char == '.' or self.char == EOF or self.char == ENDLINE:
                        # print("97" + self.char)
                        return error
                    #print("100")
                    args.append(self.parse_line())
                if token == '':  # you need a name for the Relation
                    return error

                # print("relation " + token + " created")
                term = logic.Relation(name=token, arguments=args)

                if self.is_end_of_term(self.next_char()):
                    return term
                else:
                    self.consume()

            elif self.char == '[':  # list case
                # print("in list")
                argums = []
                while self.consume() != ']':
                    if self.char == '.' or self.char == EOF or self.char == ENDLINE:
                        return error
                    argums.append(self.parse_line())

                # print("list created")
                term = logic.PList(args=argums)

                if self.is_end_of_term(self.next_char()):
                    return term
                else:
                    self.consume()

            elif self.char == ',' or self.is_end_of_term(self.next_char()) or self.char == '|':  # arguments case
                # print("in comma")
                if self.is_end_of_term(self.next_char()):
                    # print("end of term")
                    token += self.char

                if not term:
                    if token == '':
                        return None
                    elif token[0].isupper or token[0] == '_':
                        # print("variable " + token + " created")
                        return logic.Variable(name=token)
                    else:
                        # print("term " + token + " created")
                        return logic.Term(name=token)

                return term

            elif self.char == ':':  # clause case
                # print("in clause")

                if self.consume() != '-' or not term:
                    return error

                args = []

                self.consume()
                while self.char != '.' and self.char != EOF and self.char != ENDLINE:  # mono komata mporei na exei ki auta katanalwnontai ston kwdika tous
                    args.append(self.parse_line())
                    self.consume()

                # print("clause created")
                term = logic.Clause(head=term, body=args)
                # print(self.char)

            else:
                token += self.char
                self.consume()

        # print("end of while")
        
        # eof occurred
        # if term is not assigned to sth you must deal with the token first, create the term and then return it
        if not term:  # term is None ---> maybe check for correct line or sth
            if token == '':
                if self.char == ENDLINE:
                    return ENDLINE
                elif self.char == EOF:
                    return EOF
                else:
                    return False  # i error

            if token[0].isupper() or token[0] == '_':  # then it is a variable
                # print("variable " + token + " created")
                term = logic.Variable(name=token)
            else:
                # print("term " + token + " created")
                # the you have just a term (if it was not just a term you would have entered
                term = logic.Term(name=token)
        return term
