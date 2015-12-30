class Term(object):
    def __init__(self, name):
        self.name = name

    def __repr__(self):
        """A string s is a symbol if it starts with an alphabetic char."""
        if self.is_symbol(self.name) and self.name[0].islower():
           return str(self.name)

    def is_symbol(self,s):
        return isinstance(s, str) and s[0].isalpha()

    def __eq__(self, term):
        return isinstance(term, Term) and self.name == term.name


class Variable(Term):
    def __init__(self, name):
         super(Variable, self).__init__(name)

    def __repr__(self):
        if self.is_prop_symbol(self.name):
           return str(self.name)

    def is_prop_symbol(self,s):
         """The first symbol is an uppercase character and the string s is not either TRUE or FALSE."""
         return super(Variable,self).is_symbol(s) and s[0].isupper() or s[0]=='_' and s != 'TRUE' and s != 'FALSE'


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
        if super(Relation,self).is_symbol(self.name) and self.name[0].islower() and len(self.args)>0:
           return '%s(%s)' % (self.name, ', '.join(map(str, self.args)))#####den eimai sigourh an paei str dedomenou oti mporei n einai variable,atom,list


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
    def __init__(self, args = None):
        self.arguments = args

    def __eq__(self, list):
        return isinstance(list, List) and self.arguments == list(list.arguments)

    def isEmpty(self): return self.arguments == None

    def firstArg(self):
        if self.isEmpty(): return None
        else: return self.arguments[0]

    def getSubList(self, pos):
        if pos >  len(self.arguments): return List()
        else: return List(self.arguments[ pos :])

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
    elif isinstance(expr, Relation) and var in expr.args:
        return False
    else:
        unifier[var] = expr
        return unifier.append(var, expr)



def unify(x, y, unifier):
    #Failure
    if unifier == False:
        return False
    elif x==y:
        return unifier
    elif isinstance(x, Variable):
        return unify_var(x, y, unifier)
    elif isinstance(y, Variable):
        return unify_var(y, x, unifier)
    elif isinstance(x, Relation) and isinstance(y, Relation):
        #if x.name != y.name or len(x.args) != len(y.args):
        #   return False
        #for i,argx in enumerate(x.args):
        #   return unify(argx,y.args[i],unifier)
        return unify(x.args,y.args,unify(x.name,y.name,unifier))
    elif isinstance(x, Clause) and isinstance(y, Clause):
        if len(x.body) != len(y.body):
           return False
        unifier = unify(x.head, y.head, unifier)
        if unifier==False:
           return False
        for i,bodyx in enumerate(x.body):
           return unify(bodyx,y.body[i],unifier)
   #elif: lists
    else:
        return False


def createKB(file):
    # file = a list chars th file contains
    f = open(file, 'r')
    lines = f.readlines()
    kb = []
    for line in lines:
        kb.append(Lexer(line).ParseLine())
    return kb

