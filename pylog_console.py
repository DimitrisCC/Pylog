import sys
import parse
import logic

flag = True
kb = []
unifs = []

while flag:
    sys.stdout.write(">>>")
    input = sys.stdin.read(1)

    if input == "listing.":
        #TODO
        #print kb
    elif "load" in input: #dn 3erw kan an sintasetai etsi
        #TODO
        #pare to path kai anoi3e t arxeio gia na fortwseis tn kb
    elif input == '?':
        #TODO tipwse to epomeno stous enopoiites i no an dn exei allous
    elif input == "exit":
        flag = False
    else:
        command = parse.Lexer(input).parse_line()
        #estw oti dn eixe la8os telos pantwn...kai dn epestrepse error dld
        unifs = fol_bc_ask(kb, command, {})

        #TODO tipwse tn prwto unifier sto unif....me erwtimatiko 8a tipwseis tn epomeno