from tkinter import *


# maybe a class will be better


def lol():
    print("lol")


root = Tk()

menu = Menu(root)
root.geometry("500x300")
root.config(menu=menu)

sub_menu = Menu(menu)
menu.add_cascade(label='File', menu=sub_menu)
sub_menu.add_command(label='Save...', command=lol)
sub_menu.add_command(label='Load...', command=lol)

toolbar = Frame(root, bg='BLACK')
ndb_button = Button(toolbar, text='Load Knowledge Base...', command=lol)
ndb_button.pack(side=LEFT, padx=2, pady=2)
toolbar.pack(side=TOP, fill=X)

root.mainloop()
