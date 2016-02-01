import parse


class Term(object):
    def __init__(self, name):
        self.name = name

    def __str__(self):
        return self.__repr__()

    def __repr__(self):
        return str(self.name)
    
    def __hash__(self):
        return hash(self.name)

    def is_symbol(self, s):  # -------> pou xreiazetai!?
        """A string s is a symbol if it starts with an alphabetic char."""
        return isinstance(s, str) and s[0].isalpha()

    def rename_vars(self, renamed_dict):
        return self

    def __eq__(self, term):
        return isinstance(term, Term) and self.name == term.name

    # logika mallon 8a t svisoume
    def make_bindings(self, bind_dict):  # dn 3erw an iparxei periptwsi na kanoume bind kapoio Term....
        return Term(self.name)

    def getVars(self):
        return []


class Variable(Term):
    new_num = 0  # "static" member to be used in produce_new_name function

    def __init__(self, name):
        super(Variable, self).__init__(name)

    def __str__(self):
        return self.__repr__()

    def __repr__(self):
        return '%s' % str(self.name)

    def is_prop_symbol(self, s):  # -------> pou xreiazetai!?
        """The first symbol is an uppercase character and the string s is not either TRUE or FALSE."""
        return (super(Variable, self).is_symbol(s) and s[0].isupper() and s != 'TRUE' and s != 'FALSE') or (s[0] == '_')

    def __eq__(self, var):
        return isinstance(var, Variable) and var.name == self.name

    def __hash__(self):
        return hash(self.name)

    def get_bindings(self, bind_dict):
        # print(self.name)
        if self not in bind_dict.keys():
            return Variable(self.name) # test---> self

        # vars_dict a dictionary -> variable:binding_values
        binding = bind_dict.get(self)
        closed_set = [self, binding]
        while isinstance(binding, Variable) and binding in bind_dict.keys() and bind_dict[binding] not in closed_set:
            binding = bind_dict.get(binding)
            closed_set.append(binding)
        # expand the bound relation

        # tr na kaneis unify me clause mallon api8ano...
        if isinstance(binding, Relation) or isinstance(binding, PList) or isinstance(binding, Term):
            return binding.make_bindings(bind_dict)

        # mporei na einai apla mia alli metavliti..it's ok
        if isinstance(binding, Variable):
            return binding

    def make_bindings(self, bind_dict):
        return self.get_bindings(bind_dict)

    @staticmethod
    def produce_new_name(self):
        # produce a new temporary name to avoid confusion between variable names
        Variable.new_num += 1
        return Variable('%s%d' % (self.name, Variable.new_num))

    def rename_vars(self, renamed_dict):
        if self in renamed_dict.keys():
            return renamed_dict[self]
        else:
            renamed_dict[self] = self.produce_new_name(self)
        return renamed_dict[self]

    
    def getVars(self):
        return [self]


class Relation(Term):
    def __init__(self, name, arguments):  # arguments of type Variable
        super(Relation, self).__init__(name)
        self.args = arguments

    def __str__(self):
        return self.__repr__()

    def __repr__(self):
        return '%s(%s)' % (self.name, ', '.join(map(str, self.args)))
        # den eimai sigourh an paei str dedomenou oti mporei n einai variable,atom,list

    def __eq__(self, relation):
        return isinstance(relation, Relation) and self.name == relation.name and list(self.args) == list(relation.args)

    def make_bindings(self, bind_dict):
        bound = []
        for arg in self.args:

            if isinstance(arg, Relation) or isinstance(arg, Variable) or isinstance(arg, PList):
                bound.append(arg.make_bindings(bind_dict))
            elif isinstance(arg, Term):
                bound.append(
                    arg)  # auto mporei na mpei kai sto panw if afou kai i Term exei make_bindings alla ekeini i make_bindings dn exei kai toso noima
                # gi auto t ekana etsi.....alliws t vazoume panw ok

        return Relation(self.name, bound)

    def produce_new_names4vars(self, renamed_dict):
        new_names = []
        for arg in self.args:
            new_names.append(arg.rename_vars(renamed_dict))
        return new_names

    def rename_vars(self, renamed_dict):
        return Relation(self.name, self.produce_new_names4vars(renamed_dict))

    def getVars(self):
        vars = []
        for v in self.args:
            vars.extend(v.getVars())

        return vars


class Clause(Term):
    def __init__(self, head, body=None):
        self.head = head
        if body is None:
            self.body = []
        else:
            self.body = body

    def __str__(self):
        return self.__repr__()

    def __repr__(self):
        if self.body:
            return '%s :- %s' % (self.head, ', '.join(map(str, self.body)))

    def __eq__(self, clause):
        return isinstance(clause, Clause) and self.head == clause.head and list(self.body) == list(clause.body)

    def make_bindings(self, bind_dict):

        if isinstance(self.head, Relation):
            head = self.head.make_bindings(bind_dict)

        body = []
        for rel in self.body:
            if isinstance(rel, Relation):
                body.append(rel.make_bindings(bind_dict))

        return Clause(head, body)

    def produce_new_names4vars(self, renamed_dict):
        renamed_body = []
        for part in self.body:
            renamed_body.append(part.rename_vars(renamed_dict))
        return renamed_body

    def rename_vars(self, renamed_dict):
        
        return Clause(self.head.rename_vars(renamed_dict), self.produce_new_names4vars(renamed_dict))

    def getVars(self):
        vars = self.head.getVars()
        for v in self.body:
            vars.extend(v.getVars())

        return vars


# renaming to be used in proving goals


class PList(Term):
    def __init__(self, head = None , tail = [] , has_bar = False):
        self.head = head
        self.tail = tail
        self.has_bar = has_bar

    def get_tail(self):
        if self.has_bar:
            return self.tail
        elif self.is_empty() or self.tail == []:
            return PList()
        else:
            return PList(head = self.tail[0], tail = self.tail[1:])

    def __str__(self):
        return self.__repr__()

    def __repr__(self):
        if self.is_empty():
            return '[]'
        if self.has_bar:
            return '[%s|%s]' % (str(self.head),str(self.tail))
            # 8elei ftia3imo wste otan to tail einai ista na vazei kai [ ] kai otan einai metavliti na mn vazei
        elif self.tail == []:
            return '[%s]' % (str(self.head))           
        else:
            return '[%s, %s]' % (str(self.head),', '.join(map(str, self.tail)))

    def __eq__(self, alist):
        return isinstance(alist, PList) and self.head == alist.head and self.tail == alist.tail
        # evgala ena casting se list, den 3erw an xreiazetai

    def is_empty(self):
        return self.head == None


    '''
    def get_head(self):
        if self.is_empty():
            return None
        else:
            return self.head
    '''
    '''
    # def get_sublist(self, pos):
    def __getitem__(self, pos):  # overloading the [] operator
        if pos.start > len(self.arguments)-1 or pos is False:
            print("empty list")
            return PList()
        else:
            if isinstance(pos, slice):
                if pos.step is not None:
                    return PList(self.arguments[pos.start:pos.step:pos.stop])
                else:
                    print(self.arguments[pos.start:pos.stop])
                    return PList(self.arguments[pos.start:pos.stop])
            else:
                print("here")
                return self.arguments[pos] '''

    def rename_vars(self, renamed_dict):
        if self.is_empty():
            return self
        
        new_head =self.head.rename_vars(renamed_dict)
       
        if isinstance(self.tail,Variable):
            return PList(new_head, self.tail.rename_vars(renamed_dict), self.has_bar)
        
        renamed = [] 
        for arg in self.tail:
            renamed.append(arg.rename_vars(renamed_dict))
        return PList(new_head, renamed, self.has_bar)

    def make_bindings(self, bind_dict):
        if self.is_empty():
            return self

        if self.has_bar: # i oura i 8a einai variable i lista ki an einai lista dn 8a exei bar
            body = []
            tail = self.tail.make_bindings(bind_dict)
            if isinstance(tail, PList):
                if not tail.is_empty():
                    body.append(tail.head)
                    body.extend(tail.tail)

                
        else:
            body = []
            for term in self.tail:
                if isinstance(term, Variable) or isinstance(term, Term) or isinstance(term, PList) or isinstance(term,
                                                                                                                 Relation):
                    body.append(term.make_bindings(bind_dict))
                    
        return PList(self.head.make_bindings(bind_dict), body, False)

    def getVars(self):
        vars = self.head.getVars()

        if self.has_bar:
            if self.tail != []:
                vars.extend(self.tail.getVars())
        else:
            for v in self.tail:
                vars.extend(v.getVars())

        return vars

def unify_var(var, expr, unifier):
    if var in unifier:
        return unify(unifier[var], expr, unifier)
    elif isinstance(expr, PList):
        '''if expr.has_bar:
            return extend(unifier, var, PList(expr.head, [expr.tail], False))
        else:'''
        return extend(unifier, var, expr)
    elif isinstance(expr, list):
        return extend(unifier, var, expr)
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
    elif isinstance(x, PList):
        if var in x.tail or var in x.head:
            return True
    return False


def extend(unifier, var, val):
    # ------->nomizw paizei na ginetai kai pio apla..epeidi dn eimai sigouri omws dn t peirazw
    # extend({x: 1}, y, 2)
    # {y: 2, x: 1}
    unifier2 = unifier.copy()
    unifier2[var] = val
    return unifier2


def compose(unifier1, unifier2):  # ----------> endexetai na mn xreiazetai!!!
    # --> dn xreiazetai an ginetai na kanoume apeu8eias extend se dictionaries omws dn t epsa3a poli
    for i in unifier2.items():
        unifier1 = extend(unifier1, i[0], i[1])
    # print("in compose")
    # print(unifier1)
    return unifier1


def unify(x, y, unifier):
    # Failure
    # print(x)
    # print(y)
    if unifier is False:
        return False
    elif x == y:
        return unifier
    elif isinstance(x, Variable):
        return unify_var(x, y, unifier)
    elif isinstance(y, Variable):
        return unify_var(y, x, unifier)
    elif isinstance(x, Relation) and isinstance(y, Relation) and len(x.args) == len(y.args):
        return unify(x.args, y.args, unify(x.name, y.name, unifier))
    elif isinstance(x, PList) and isinstance(y, PList): # and len(x.arguments) == len(y.arguments):
        if x.is_empty() and y.is_empty():
            #print("both empty")
            return unifier
        if x.is_empty():
            # print("x empty")
            return False
        elif y.is_empty():
            # print("y empty")
            return False
        # print("UNIFY------------------------------> PList")
        return unify(x.get_tail(), y.get_tail(), unify(x.head, y.head, unifier))
    elif isinstance(x, list) and isinstance(y, list): # exoume idi koita3ei pio panw gia idio ari8mo arguments
        # print("UNIFY------------------------------>  listes")
        return unify(x[1:], y[1:], unify(x[0], y[0], unifier))
    else:
        # print("Flash")
        return False


def createKB(file):
    # file = a list chars th file contains
    f = open(file, 'r')
    lines = f.readlines()
    f.close()
    kb = []
    for line in lines:
        k = parse.Lexer(line).parse_line()
        # print("------------")
        # print(k)
        # print("------------")
        # print(type(k))
        kb.append(k)  # des mhpws anti gia appand paei extend kalutera.To append einai kalutero otan theloume na prosthesoume ena mono element.Ara asto etsi

    return kb


# ----->PROSOXIIIII: deite ta TODO


def fol_bc_ask(KB, goals, unifier):
    # print("-------------IN FOL-------------")
    if not goals:
        return unifier
    ans = []

    b = goals[0].make_bindings(unifier)  # TODO --> make_bindings for Variable
    # ---> nai 3erw exei to get alla einai allo to make_bindings + dn xreiazetai na
    # koitame ti einai auto sto opoio t kaloume
    # print(b)

    for t in KB:  # sullegoume ta clauses apo th KB pou exoun idio head me to relation pou theloume na apodeixoume kai kanoume unify wste na vroume ayta pou tairiazoun.
        t = t.rename_vars({})  # nomizw einai ok
        if isinstance(t, Clause):
            # print('checking the CLAUSE '+str(t))
            new_unif = unify(t.head, b, unifier)
            if new_unif is False:
                continue
            
            # print(new_unif)
            goals.extend(t.body)  # to extend einai gia na pros8eseis ta stoixeia
            # mias listas se iparxousa lista
            x = fol_bc_ask(KB, goals[1:], compose(unifier, new_unif))
            if isinstance(x, list):
                ans.extend(x)
            else:
                ans.append(x)

        if isinstance(t, Relation) or isinstance(t, Term): #tqra akiri metavliti mesa stn vasi gnwsis diskolo
            
            # print('checking '+str(t))
            new_unif = unify(t, b, unifier)
            if new_unif is False:
                # print("FALSE UNIF")
                continue
            # print(new_unif)
            
            # print("before append "+str(ans))
            x = fol_bc_ask(KB, goals[1:], compose(unifier, new_unif))
            if isinstance(x, list):
                ans.extend(x)
            else:
                ans.append(x)
            # print("after append "+str(ans))
            
    #print(ans)
    return ans
