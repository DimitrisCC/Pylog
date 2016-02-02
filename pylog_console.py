import os.path

import logic
import parse


def pylog_console():
    flag = True
    kb = []
    unifs = []
    vars = []
    kb_file = ''
    next_unif = 0

    manual = "load <filename>.\nLoads a prolog file (.pl only).\n\n" \
             "listing.\nPrints the knowledge base.\n\n" \
             "help.\nOpens the manual page.\n\n" \
             "exit.\nExits the prolog command line.\n\n" \
             "Everything else that ends with \'.\' is conidered a query. " \
             "\nPressing the Enter key you can see an answer to your query.\n" \
             "Using \';\' afterwards you can ask for another answer."

    c = 1
    print("~~~~~~~~~~~~~~~~~~~~ WELCOME TO PYLOG ~~~~~~~~~~~~~~~~~~~~\n\nUse \'help.\' to see the manual")
    while flag:

        inputt = input("\n" + str(c) + ". ?- ")
        inputt.strip('')

        if inputt[-1] != '.':
            print("Sorry bro you missed the dot! Repeat the command again using a \".\" at the end!")
        elif inputt == "help.":
            print(manual)
            c += 1
        elif inputt == "listing.":

            if kb_file != '':

                for k in kb:
                    print(k)
                c += 1

            else:
                print("You have not loaded a file yet! Please load your file first with the command\n"
                      "load <name of your file>")

        elif inputt.startswith("load"):
            kb_file = inputt.split()[1][:-1]

            if kb_file[-3:] != ".pl":
                print("You were supposed to load ONLY PROLOG FILES (.pl)!!! Please try again!!!")
            else:
                if os.path.exists(kb_file):
                    try:
                        kb = logic.createKB(kb_file)
                        print("Your file was loaded successfully")
                        c += 1
                    except parse.CommandException as e:
                        print(e)

                else:
                    print("Sorry! The file you tried to access does not exist.")


        elif inputt == "exit.":
            flag = False
        elif '=' in inputt:
            index = inputt.find('=')
            if index == 0 or index == len(inputt) - 1:
                print("Well..you just gave me a totally wrong command to check equality...try again!")
            else:
                cmd1 = inputt[0:index].strip(' =')
                cmd2 = inputt[index:].strip(' =.')
                left = parse.Lexer(cmd1).parse_line()
                right = parse.Lexer(cmd2).parse_line()
                # estw oti ola kala stn parse_line...
                unifier = logic.unify(left, right, {})
                vars = left.getVars()
                vars.extend(right.getVars())
                if unifier is False:
                    print("no.")
                else:
                    print_next_unif([unifier], vars, 0)
                    print("\nyes.")

                c += 1

        else:
            stripped = inputt.strip()
            try:
                command = parse.Lexer(stripped).parse_line()
            except parse.CommandException as e:
                print(e)

            vars = command.getVars()
            unifs = logic.fol_bc_ask(kb, [command], {})
            next_unif = 1

            if not unifs or unifs[0] is False:
                print('no.')
            else:
                if vars == []:
                    print('yes.')
                else:
                    print_next_unif(unifs, vars, 0)

                    inputt = input("")
                    while inputt == ';' or inputt == ';':
                        print_next_unif(unifs, vars, next_unif)
                        next_unif += 1
                        if next_unif > len(unifs) or inputt == '':
                            break
                        inputt = input("")
            c += 1


def print_next_unif(unifiers, variables, index):
    if len(unifiers) - 1 < index:
        print('no.')
    else:
        for i in range(len(variables)):
            if i == 0:
                print(str(variables[i]) + " = " + str(variables[i].make_bindings(unifiers[index])), end="")
                # if print doesn't work (works only for Python 3 and after)
                # sys.stdout.write(str(variables[i])+" = "+str(variables[i].make_bindings(unifiers[index])))
            else:
                print(', ' + str(variables[i]) + " = " + str(variables[i].make_bindings(unifiers[index])), end="")
                # if print doesn't work (works only for Python 3 and after)
                # sys.stdout.write(', '+str(variables[i])+" = "+str(variables[i].make_bindings(unifiers[index])))


if __name__ == "__main__":
    pylog_console()
