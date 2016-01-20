import sys
import parse
import logic

flag = True
kb = []
unifs = []
kb_file = ''

while flag:

    inputt = input(">>>")

    if inputt == "listing.":
        file = open(filename, 'r')
        if file:
            print(file.read())
            file.close()
    elif inputt.startswith("load"): #dn 3erw kan an sintasetai etsi
        kb__file = input.split()[1]
    elif inputt == '?':
        if len(unifs) < next_unif:
            print('no.')
        else:
            print(unifs[next_unif])
            next_unif += 1
    elif inputt == "exit.":
        flag = False
    else:
        command = parse.Lexer(inputt).parse_line()
        #estw oti dn eixe la8os telos pantwn...kai dn epestrepse error dld
        unifs = logic.fol_bc_ask(kb, command, {})
        next_unif = 1
        if len(unifs) == 0 or not unifs[0]:
            print ('no.')
        else:
            print (unifs[0])