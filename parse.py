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
        identifier = self.char
        if not self.is_letter() and self.char != '_':
            raise CommandException('identifier', 'Your identifiers should start either with letter or with \'_\'')
            return error
        self.consume()
        
        while self.is_alpharethmetic() and not self.is_end_of_term():
            identifier += self.char
            self.consume()
            
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
        while (self.char != ENDLINE and self.char != EOF):
            self.consume()


    def is_end(self):
        return (self.char == '.' or self.char == EOF or self.char == ENDLINE)

    def next_char(self):
        if self.pos + 1 > len(self.line) - 1:
            return EOF
        else:
            return self.line[self.pos + 1]

    def is_end_of_term(self):
        return self.next_char() == ')' or self.next_char() == ']'

    def is_relation(self):
        return self.char == '('

    def consume_relation(self, relation_name):
        args = []
        while self.consume() != ')': 
            if self.is_end():
                raise CommandException('relation', 'You probably forgot \')\'')
                return error
            args.append(self.parse_line())
            
        if relation_name == '':  # you need a name for the Relation
            raise CommandException('relation', 'Your relation should have a name')
            return error

        return logic.Relation(name=relation_name, arguments=args)

    def is_list(self):
        return self.char == '['

    def consume_list(self):
        argums = []
        has_b = False
        index_of_bar = 0
        arg = 0 
        while self.consume() != ']':
            if self.is_end():
                raise CommandException('list', 'You probably forgot \']\'')
                return error
                        
            argums.append(self.parse_line())
            arg += 1 # the position the bar was found
            if self.char == '|':
                has_b = True
                index_of_bar = arg

        if not argums:
            return logic.PList()
        else:
            if has_b:
                return logic.PList(head=argums[0:index_of_bar], tail=argums[index_of_bar], has_bar = has_b)             
            else:    
                return logic.PList(argums)

    def is_clause(self):
        return self.char == ':' and self.next_char() == '-'

    def consume_clause(self, head):
        self.consume() # consuming ':'

        if not head:
            raise CommandException('clause', 'Your clause should have a term before \':-\'')
            return error
        
        args = []
        
        self.consume() # consuming '-'
        while not self.is_end():
            args.append(self.parse_line())
            self.consume()

        return logic.Clause(head=head, body=args)

    def is_argument(self):
        return self.char == ',' or self.char == '|' or self.is_end_of_term() 

    def consume_var_or_term(self, token):
        if token == '':
            raise CommandException('variable or term', 'You forgot the variable or term')
            return error
        elif token[0].isupper() or token[0] == '_':
            return logic.Variable(name=token)
        else:
            return logic.Term(name=token)
    
            

    # Parser:

    # it parses only one line
    # to parse multiple lines (in a file maybe) run this until it returns EOF
    # no checking for invalid input is done but it maybe could
    
    def parse_line(self):
        token = ''
        term = None

        while not self.is_end():
            if self.is_whitespace():
                self.consume()
                continue
            elif self.is_comment():
                self.consume_comment()  # an dn exei ENDLINE? prosoxi...
            elif self.is_relation():
                try:
                    term = self.consume_relation(token)
                except CommandException as c:
                    raise c
                
                if self.is_end_of_term():
                    return term
                else:
                    self.consume()

            elif self.is_list():
                try:
                    term = self.consume_list()
                except CommandException as c:
                    raise c
                
                if self.is_end_of_term():
                    return term
                else:
                    self.consume()

            elif self.is_argument():  # arguments case
                
                if self.is_end_of_term():
                    token += self.char

                if not term:
                    try:
                        term = self.consume_var_or_term(token)
                    except CommandException as c:
                        raise c
                    
                return term

            elif self.is_clause():
                try:
                    term = self.consume_clause(term)
                except CommandException as c:
                    raise c
            else:
                try:
                    token = self.get_identifier()
                except CommandException as c:
                    raise c
        
        # eof occurred
        # if term is not assigned to sth you must deal with the token first, create the term and then return it
        if not term:  # term is None ---> maybe check for correct line or sth
            try:
                term = self.consume_var_or_term(token)
            except CommandException as c:
                    raise c
            '''if term == error:
                if self.char == ENDLINE:
                    return ENDLINE
                elif self.char == EOF:
                    return EOF
                else:
                    return error'''

            
        return term


    
class CommandException(Exception):
    """Exception raised when wrong commands occur.

    Attributes:
        cmd -- type of command in which the error occurred
        msg -- explanation of the error
    """

    def __init__(self, cmd_type, msg):
        self.cmd = cmd_type
        self.msg = msg
        
    def __str__(self):
        return '\nCommand Exception\n\ncommand type: '+self.cmd+'\n'+self.msg
