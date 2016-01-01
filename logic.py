import parse as analysis


class Term(object):
    def __init__(self, name):
        self.name = name

    def __repr__(self):
        """A string s is a symbol if it starts with an alphabetic char."""
        if self.is_symbol(self.name) and self.name[0].islower():
           return str(self.name)

    def is_symbol(self, s):
        return isinstance(s, str) and s[0].isalpha()

    def __eq__(self, term):
        return isinstance(term, Term) and self.name == term.name


class Variable(Term):
    def __init__(self, name):
        super(Variable, self).__init__(name)

    def __repr__(self):
        if self.is_prop_symbol(self.name):
            return str(self.name)

    def is_prop_symbol(self, s):
        """The first symbol is an uppercase character and the string s is not either TRUE or FALSE."""
        return super(Variable, self).is_symbol(s) and s[0].isupper() or s[0] == '_' and s != 'TRUE' and s != 'FALSE'

    def __eq__(self, var):
        return isinstance(var, Variable) and var.name == self.name

    def __hash__(self):
        return hash(self.name)

    def get_bindings(self, bind_dict):
        # vars_dict a dictionary -> variable:binding_values
        binding = bind_dict.get(self)

        closed_set = [self, binding]
        while isinstance(binding, Variable) and binding in bind_dict and bind_dict[binding] not in closed_set:
            binding = bind_dict.get(binding)
            closed_set.append(binding)

        # expand the bound relation
        if isinstance(binding, Relation):
            return binding.make_bindings(bind_dict)

        return binding


class Relation(Term):
    def __init__(self, name, arguments):  # arguments of type Variable
        super(Relation, self).__init__(name)
        self.args = arguments

    def __repr__(self):
        if super(Relation, self).is_symbol(self.name) and self.name[0].islower() and len(self.args) > 0:
            return '%s(%s)' % (self.name, ', '.join(map(str, self.args)))
            # den eimai sigourh an paei str dedomenou oti mporei n einai variable,atom,list

    def __eq__(self, relation):
        return isinstance(relation, Relation) and self.name == relation.name and list(self.args) == list(relation.args)

    def make_bindings(self, bind_dict):
        bound = []
        for arg in self.args:
            if arg in bind_dict:
                bound.append(arg.get_bindings(bind_dict))
            else:
                bound.append(arg)

        return Relation(self.name, bound)


class Clause(Term):
    def __init__(self, head, body=None):
        self.head = head
        if body is None:
            self.body = []
        else:
            self.body = body

    def __repr__(self):
        if self.body:
            return '%s :- %s' % (self.head, ', '.join(map(str, self.body)))
        return str(self.head)

    def __eq__(self, clause):
        return isinstance(clause, Clause) and self.head == clause.head and list(self.body) == list(clause.body)

    def make_bindings(self, bind_dict):
        head = self.head.make_bindings(bind_dict)
        body = []
        for rel in self.body:
            body.append(rel.make_bindings(bind_dict))

        return Clause(head, body)


class List(Term):
    def __init__(self, args=None):
        self.arguments = args

    def __repr__(self):
        return '[%s]' % (', '.join(map(str, self.arguments)))

    def __eq__(self, alist):
        return isinstance(alist, List) and self.arguments == list(alist.arguments)

    def is_empty(self):
        return self.arguments is None

    def first_arg(self):
        if self.is_empty():
            return None
        else:
            return self.arguments[0]

    def get_sublist(self, pos):
        if pos > len(self.arguments):
            return List()
        else:
            return List(self.arguments[pos:])

    def make_bindings(self, bind_dict):
        body = []
        for term in self.arguments:
            body.append(term.make_bindings(bind_dict))
        return List(body)


def unify_var(var, expr, unifier):
    if var in unifier:
        return unify(unifier[var], expr, unifier)
    elif expr in unifier:
        return unify(var, unifier[expr], unifier)
    elif occur_check(var, expr):
        return None
    else:
        return extend(unifier, var, expr)


def occur_check(var, x):
    """Return true if var occurs anywhere in x."""
    if var == x:
        return True
    elif isinstance(x, Relation) and var in x.args:
        return True
    elif isinstance(x, List) and var in x.arguments:
        return True
    return False


def extend(unifier, var, val):
    #------->nomizw paizei na ginetai kai pio apla..epeidi dn eimai sigouri omws dn t peirazw
    #extend({x: 1}, y, 2)
    #{y: 2, x: 1}
    unifier2 = unifier.copy()
    unifier2[var] = val
    return unifier2


def compose(unifier1, unifier2): #----------> endexetai na mn xreiazetai!!!
    #--> dn xreiazetai an ginetai na kanoume apeu8eias extend se dictionaries omws dn t epsa3a poli
    for i in unifier2.items():
        unifier1 = extend(unifier1, i[0], i[1])

    return unifier1


def unify(x, y, unifier):
    # Failure
    if unifier == False:
        return False
    elif x == y:
        return unifier
    elif isinstance(x, Variable):
        return unify_var(x, y, unifier)
    elif isinstance(y, Variable):
        return unify_var(y, x, unifier)
    elif isinstance(x, Relation) and isinstance(y, Relation) and len(x.args) == len(y.args):
        return unify(x.args, y.args, unify(x.name, y.name, unifier))
    elif isinstance(x, List) and isinstance(y, List) and len(x.arguments) == len(y.arguments):
        return unify(x.get_sublist(1), y.get_sublist(1), unify(x.first_arg(), y.first_arg(), unifier))
    else:
        return False


def createKB(file):
    # file = a list chars th file contains
    f = open(file, 'r')
    lines = f.readlines()
    kb = []
    for line in lines:
        kb.append(analysis.Lexer(line).ParseLine())  # des mhpws anti gia appand paei extend kalutera
    return kb


# ----->PROSOXIIIII: deite ta TODO


def fol_bc_ask(KB, goals, unifier):
    if goals == []:
        return unifier
    ans = []

    b = goals.pop(0).make_bindings()  # TODO --> make_bindings for Variable
    # ---> nai 3erw exei to get alla einai allo to make_bindings + dn xreiazetai na
    # koitame ti einai auto sto opoio t kaloume

    for t in KB:
        t = t.new_vars()  # TODO
        new_unif = unify( t.head , b)
        if not new_unif : continue

        goals.extend(t.body)  # to extend einai gia na pros8eseis ta stoixeia
        # mias listas se iparxousa lista
        ans.append(fol_bc_ask(KB, goals, compose(unifier, new_unif)))
    return ans
