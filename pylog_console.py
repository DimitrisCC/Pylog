import os.path

import logic
import parse


def pylog_console():

    manual = 'help.\n\n' \
             'Prints the manual page.\n\n\n' \
             'load <file>.\n\nLoads a prolog program (your knowledge base)\n\n\nlisting.\n\n' \
             'Prints your loaded program.\nAvailable only if you have already loaded a prolog program.\n\n\n' \
             'exit.\n\nExits the prolog console.\n\n\n' \
             'Everything else is considered a query.\n'

    flag = True
    kb = []
    unifs = []
    vars = []
    kb_file = ''
    next_unif = 0

    c = 1

    while flag:

        inputt = input('\n'+str(c)+" ?- ")
        inputt.strip('')


        if inputt == '?':
            printNextUnif(unifs, vars, next_unif)
            next_unif += 1
        elif inputt[-1] != '.': # and inputt[0:1] == '?-':
            print("Sorry bro you missed the dot! Repeat the command again using a \".\" at the end!")
        elif inputt == "listing.":

            if kb_file != '':
                
                for k in kb:
                    print(k)
                c += 1
            else:
                print("You have not loaded a file yet! Please load your file first with the command\n"
                      "load <name of your file>")
    
        elif inputt.startswith("load"):  # dn 3erw kan an sintasetai etsi
            kb_file = inputt.split()[1][:-1]

            if kb_file[-3:] != ".pl":
                print("You were supposed to load ONLY PROLOG FILES (.pl)!!! Please try again!!!")
            else:
                if os.path.exists(kb_file):
                    kb = logic.createKB(kb_file)
                    print("Your file was loaded successfully")
                    c += 1
                else:
                    print("Sorry! The file you tried to access does not exist.")

        elif inputt == "exit.":
            flag = False
        elif '=' in inputt:
            command = inputt.split()
            if command[1] != '=' or len(command) > 3:
                print("Well..you just gave me a totally wrong command to check equality...try again!")
            else:
                left = parse.Lexer(command[0]).parse_line()
                right = parse.Lexer(command[2][:-1]).parse_line()
                # estw oti ola kala stn parse_line...
                unifier = logic.unify(left, right, {})
                if unifier is False:
                    print("no.")
                else:
                    print("yes.")
                
                c += 1
                
        elif inputt == 'help.':
            print(manual)
            c += 1
            
        else:
            stripped = inputt[: -1].strip()
            command = parse.Lexer(stripped).parse_line()
            vars = command.getVars()
            # estw oti dn eixe la8os telos pantwn...kai dn epestrepse error dld
            unifs = logic.fol_bc_ask(kb, [command], {})
            next_unif = 1
            if not unifs or unifs[0] is False:
                print('no.')
            else:
                printNextUnif(unifs, vars, 0)
                print('yes.')
            c += 1


def printNextUnif(unifiers, variables, index):

    if len(unifiers) - 1 < index:
        print('no.')
    else:
        for v in variables:
            if v != None:
                print(str(v)+" = "+str(v.get_bindings(unifiers[index])))
            


if __name__ == "__main__":
    pylog_console()
