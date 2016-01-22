import sys
import parse
import logic
import os.path


def pylog_console():
    flag = True
    kb = []
    unifs = []
    kb_file = ''

    while flag:

        inputt = input(">>>")

        if inputt[-1] != '.':
            print("Sorry bro you missed the dot! Repeat the command again using a \".\" at the end!")
        elif inputt == "listing.":
            if kb_file != '':
                file = open(kb_file, 'r')
                if file:
                    print(file.read())
                    file.close()
            else:
                print("You have not loaded a file yet! Please load your file first with the command\n load <name of your file>")
                
        elif inputt.startswith("load"): #dn 3erw kan an sintasetai etsi
            kb_file = inputt.split()[1]

           
            if kb_file[-4:] != ".pl.":
                print("You were supposed to load ONLY PROLOG FILES (.pl)!!! Please try again!!!")
            else:
                if os.path.exists(kb_file):
                    kb = logic.createKB(kb_file)
                    print("Your file was loaded successfully")
                else:
                    print("Sorry! The file you tried to access does not exist.")
            
        elif inputt == '?':
            if len(unifs) < next_unif:
                print('no.')
            else:
                print(unifs[next_unif])
                next_unif += 1
        elif inputt == "exit." :
            flag = False
        elif '=' in inputt:
            command = inputt.split()
            if command[1] != '=' or len(command) > 3:
                print("Well..you just gave me a totally wrong command to check equality...try again!")
            else:
                left = parse.Lexer(command[0]).parse_line()
                right = parse.Lexer(command[2]).parse_line()
                #estw oti ola kala stn parse_line...
                unifier = logic.unify(left,right,{})
                if not unifier:
                    print("no.")
                else:
                    print("yes.")
        else:
            command = parse.Lexer(inputt).parse_line()
            #estw oti dn eixe la8os telos pantwn...kai dn epestrepse error dld
            unifs = logic.fol_bc_ask(kb, [command], {})
            next_unif = 1
            if len(unifs) == 0 or not unifs[0]:
                print ('no.')
            else:
                print (unifs[0])



if __name__ == "__main__":
    pylog_console()
