import parse

# Dimaki Georgia 3130052
# Kolokathi Fotini 3090088
# Papatheodorou Dimitrios 3130162

'''
Each class contains the basic methods:
__init__ : the constructor
__str__ : returns the string representation of the class
__repr__: same as str
__hash__: makes the object hashable (used only for classes used as dictionary keys-all apart from PList)
__eq__: returns whether the object is equal with the one passed as argument or not
getVars: returns the variables contained in the specific term
rename_vars: renames all the variables contained in the specific term
make_bindings: makes the bindings of the variables in the specific term (used in fol-bc-ask)

Some classes contain also some helping methods explained in their class
'''


# TERM ###################################################################################################
class Term(object):
    def __init__(self, name):
        self.name = name

    def __str__(self):
        return self.__repr__()

    def __repr__(self):
        return str(self.name)

    def __hash__(self):
        return hash(self.name)

    def __eq__(self, term):
        return isinstance(term, Term) and self.name == term.name

    def getVars(self):
        return []

    def rename_vars(self, renamed_dict):
        return self

    def make_bindings(self, bind_dict):
        return self


###########################################################################################################


# VARIABLE ################################################################################################
class Variable(Term):
    new_num = 0  # "static" member to be used in produce_new_name function

    def __init__(self, name):
        super(Variable, self).__init__(name)

    def __str__(self):
        return self.__repr__()

    def __repr__(self):
        return '%s' % str(self.name)

    def __hash__(self):
        return hash(self.name)

    def __eq__(self, var):
        return isinstance(var, Variable) and var.name == self.name

    def getVars(self):
        if self.name == '_':
            return []

        return [self]

    # produce a new temporary name to avoid confusion between variable names
    @staticmethod
    def produce_new_name(self):
        Variable.new_num += 1
        return Variable('%s%d' % (self.name, Variable.new_num))

    def rename_vars(self, renamed_dict):
        if self.name == '_':
            return self.produce_new_name(self)

        if self in renamed_dict.keys():
            return renamed_dict[self]
        else:
            renamed_dict[self] = self.produce_new_name(self)
        return renamed_dict[self]

    def make_bindings(self, bind_dict):
        # print(self.name)
        if self not in bind_dict.keys():
            return self

        # vars_dict a dictionary -> variable:binding_values
        binding = bind_dict.get(self)

        return binding.make_bindings(bind_dict)


###########################################################################################################


# RELATION ################################################################################################
class Relation(Term):
    def __init__(self, name, arguments):
        super(Relation, self).__init__(name)
        self.args = arguments

    def __str__(self):
        return self.__repr__()

    def __repr__(self):
        return '%s(%s)' % (self.name, ', '.join(map(str, self.args)))

    def __eq__(self, relation):
        return isinstance(relation, Relation) and self.name == relation.name and list(self.args) == list(relation.args)

    def getVars(self):
        vars = []
        for v in self.args:
            vars.extend(v.getVars())

        return vars

    def rename_vars(self, renamed_dict):
        new_names = []
        for arg in self.args:
            new_names.append(arg.rename_vars(renamed_dict))

        return Relation(self.name, new_names)

    def make_bindings(self, bind_dict):
        bound = []
        for arg in self.args:
            bound.append(arg.make_bindings(bind_dict))

        return Relation(self.name, bound)


###########################################################################################################


# CLAUSE ##################################################################################################
class Clause(Term):
    def __init__(self, head, body=[]):
        self.head = head
        self.body = body

    def __str__(self):
        return self.__repr__()

    def __repr__(self):
        if self.body:
            return '%s :- %s' % (self.head, ', '.join(map(str, self.body)))

    def __eq__(self, clause):
        return isinstance(clause, Clause) and self.head == clause.head and list(self.body) == list(clause.body)

    def getVars(self):
        vars = self.head.getVars()
        for v in self.body:
            vars.extend(v.getVars())

        return vars

    def rename_vars(self, renamed_dict):
        renamed_body = []
        for part in self.body:
            renamed_body.append(part.rename_vars(renamed_dict))

        return Clause(self.head.rename_vars(renamed_dict), renamed_body)

    def make_bindings(self, bind_dict):

        head = self.head.make_bindings(bind_dict)

        body = []
        for rel in self.body:
            body.append(rel.make_bindings(bind_dict))

        return Clause(head, body)


###########################################################################################################


# PLIST ###################################################################################################
class PList(Term):
    '''
    PLists are of the form:
    if they have bar:
        head = elements before bar
        tail = element after bar (this can be either variable or PList).
               it represents the sublist of the whole PList after the head elements
        has_bar = True
    else:
        head = all the elements of the PList
        tail --> not used
        has_bar = False
    '''

    def __init__(self, head=[], tail=[], has_bar=False):
        '''
        when it has bar then it has a tail too.
        otherwise all the arguments are in head list
        '''
        self.head = head
        self.tail = tail
        self.has_bar = has_bar

    def __str__(self):
        return self.__repr__()

    def __repr__(self):
        if self.is_empty():
            return '[]'
        if self.has_bar:
            return '[%s|%s]' % (', '.join(map(str, self.head)), str(self.tail))
        elif self.tail == []:
            return '[%s]' % (', '.join(map(str, self.head)))

    def __eq__(self, alist):
        return isinstance(alist, PList) and self.head == alist.head and self.tail == alist.tail

    # returns whether the PList is empty or not (it is empty if head has no elements)
    def is_empty(self):
        return self.head == []

    # returns the first element of the PList
    def get_first(self):
        if self.is_empty():
            return None
        else:
            return self.head[0]

    # returns the sublist after the first element
    # ATTENTION : if it has a bar but it still has elements after the first element in the head
    # then the sublist returned will have a bar too
    def get_rest(self):
        if self.is_empty():
            return PList()
        elif self.has_bar:  # tail will be either a variable or a PList
            if len(self.head) == 1:
                return self.tail
            else:
                return PList(self.head[1:], self.tail, True)
        else:
            return PList(head=self.head[1:])

    def getVars(self):
        if self.is_empty():
            return []

        vars = []
        for arg in self.head:
            vars.extend(arg.getVars())

        if self.has_bar:  # then it has a tail too (tail != [])
            vars.extend(self.tail.getVars())

        return vars

    def rename_vars(self, renamed_dict):
        if self.is_empty():
            return self

        new_head = []
        for arg in self.head:
            new_head.append(arg.rename_vars(renamed_dict))

        if self.has_bar:
            return PList(new_head, self.tail.rename_vars(renamed_dict), self.has_bar)
        else:
            return PList(new_head)

    def make_bindings(self, bind_dict):
        if self.is_empty():
            return self

        new_head = []
        for arg in self.head:
            new_head.append(arg.make_bindings(bind_dict))

        if self.has_bar:  # the new PList should not have a bar and if it is a PList it's elements will be appended to the new_head
            # self.tail after the bindings are made will be either a PList with has_bar = False or a variable
            tail = self.tail.make_bindings(bind_dict)
            if isinstance(tail, PList):
                new_head.extend(tail.head)
                return PList(new_head)
            else:  # it is a variable again so...
                return PList(new_head, tail, True)
        else:
            return PList(new_head)


###########################################################################################################



# BACKWARD CHAINING #######################################################################################

# unifies a variable with expr
def unify_var(var, expr, unifier):
    if var in unifier:
        return unify(unifier[var], expr, unifier)
    elif isinstance(expr, PList):
        return extend(unifier, var, expr)
    elif isinstance(expr, list):
        return extend(unifier, var, expr)
    elif expr in unifier:
        return unify(var, unifier[expr], unifier)
    elif occur_check(var, expr):
        return None
    else:
        return extend(unifier, var, expr)


"""Return true if var occurs anywhere in x."""


def occur_check(var, x):
    if var == x:
        return True
    elif isinstance(x, Relation) and var in x.args:
        return True
    elif isinstance(x, PList):
        if var in x.tail or var in x.head:
            return True
    return False


# extend({x: 1}, y, 2)
# {y: 2, x: 1}
def extend(unifier, var, val):
    unifier2 = unifier.copy()
    unifier2[var] = val
    return unifier2


# it joins unifier1 and unifier2
def compose(unifier1, unifier2):
    for i in unifier2.items():
        unifier1 = extend(unifier1, i[0], i[1])
    return unifier1


# returns a unifier of x and y if they can unify and False otherwise
def unify(x, y, unifier):
    if unifier is False:  # Failure on previous call of the function
        return False
    elif x == y:
        return unifier
    elif isinstance(x, Variable):
        return unify_var(x, y, unifier)
    elif isinstance(y, Variable):
        return unify_var(y, x, unifier)
    elif isinstance(x, Relation) and isinstance(y, Relation) and len(x.args) == len(y.args):
        return unify(x.args, y.args, unify(x.name, y.name, unifier))
    elif isinstance(x, PList) and isinstance(y, PList):
        if x.is_empty() and y.is_empty():
            return unifier
        if x.is_empty():
            return False
        elif y.is_empty():
            return False
        return unify(x.get_rest(), y.get_rest(), unify(x.get_first(), y.get_first(), unifier))
    elif isinstance(x, list) and isinstance(y, list):
        return unify(x[1:], y[1:], unify(x[0], y[0], unifier))
    else:  # Failure case
        return False


# creates the knowledge base from the file given
def createKB(file):
    f = open(file, 'r')
    lines = f.readlines()
    f.close()
    kb = []
    for line in lines:
        k = parse.Lexer(line).parse_line()
        kb.append(k)

    return kb


# The backward chaining algorithm
def fol_bc_ask(KB, goals, unifier):
    if not goals:
        return unifier
    ans = []

    b = goals[0].make_bindings(unifier)

    for t in KB:  # for each term in knowledge base

        t = t.rename_vars({})
        if isinstance(t, Clause):
            # if it is a clause and b unifies with the head of the clause we add in the goals the body of the clause
            new_unif = unify(t.head, b, unifier)
            if new_unif is False:
                continue

            goals.extend(t.body)
            x = fol_bc_ask(KB, goals[1:], compose(unifier, new_unif))
            if isinstance(x, list):
                ans.extend(x)
            else:
                ans.append(x)

        if isinstance(t, Relation) or isinstance(t, Term):
            # if it is relation or term we try to unify b with it
            new_unif = unify(t, b, unifier)
            if new_unif is False:
                continue

            x = fol_bc_ask(KB, goals[1:], compose(unifier, new_unif))
            if isinstance(x, list):
                ans.extend(x)
            else:
                ans.append(x)

    # returns all the possible unifiers it found
    return ans

###########################################################################################################
