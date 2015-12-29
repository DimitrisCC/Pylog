class Term(object):
    def __init__(self, name):
        self.name = name

    def __eq__(self, term):
        return isinstance(term, Term) and self.name == term.name

    def __hash__(self):
        return hash(self.var)


class Variable(Term):
    def __init__(self, name):
        super(Variable, self).__init__(name)

    def __eq__(self, var):
        return isinstance(var, Variable) and var.name == self.name

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

    def __eq__(self, relation):
        return isinstance(relation, Relation) and self.name == relation.pred and self.args == relation.args

    def make_bindings(self, bind_dict):
        bound = []
        for arg in self.args:
            if arg in bind_dict:
                bound.append(arg.get_bindings(bind_dict))
            else:
                bound.append(arg)

        return Relation(self.pred, bound)


class Clause(Term):
    def __init__(self, head, body=None):
        self.head = head
        if body is None:
            self.body = []
        else:
            self.body = body

    def __eq__(self, clause):
        return isinstance(clause, Clause) and self.head == clause.head and self.body == list(clause.body)

    def make_bindings(self, bind_dict):
        head = self.head.make_bindings(bind_dict)
        body = []
        for rel in self.body:
            body.append(rel.make_bindings(bind_dict))

        return Clause(head, body)


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
        unify_var(x, y, unifier)
    elif isinstance(y, Variable):
        unify_var(y, x, unifier)
    elif isinstance(x, Relation) and isinstance(y, Relation):
        if x.name != y.name or len(x.args) != len(y.args):
           return False
        for i,argx in enumerate(x.args):
           return unify(argx,y.args[i],unifier)
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
